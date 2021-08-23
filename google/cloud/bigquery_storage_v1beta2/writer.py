# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import division

import concurrent.futures
import logging
import queue
import threading
from typing import Optional

import grpc

from google.api_core import bidi
from google.api_core.future import polling as polling_future
from google.api_core import exceptions
import google.api_core.retry
from google.cloud.bigquery_storage_v1beta2 import types as gapic_types
from google.cloud.bigquery_storage_v1beta2.services import big_query_write

_LOGGER = logging.getLogger(__name__)
_REGULAR_SHUTDOWN_THREAD_NAME = "Thread-RegularStreamShutdown"
_RPC_ERROR_THREAD_NAME = "Thread-OnRpcTerminated"
_RETRYABLE_STREAM_ERRORS = (
    exceptions.DeadlineExceeded,
    exceptions.ServiceUnavailable,
    exceptions.InternalServerError,
    exceptions.Unknown,
    exceptions.GatewayTimeout,
    exceptions.Aborted,
)
_TERMINATING_STREAM_ERRORS = (exceptions.Cancelled,)


def _wrap_as_exception(maybe_exception):
    """Wrap an object as a Python exception, if needed.
    Args:
        maybe_exception (Any): The object to wrap, usually a gRPC exception class.
    Returns:
         The argument itself if an instance of ``BaseException``, otherwise
         the argument represented as an instance of ``Exception`` (sub)class.
    """
    if isinstance(maybe_exception, grpc.RpcError):
        return exceptions.from_grpc_error(maybe_exception)
    elif isinstance(maybe_exception, BaseException):
        return maybe_exception

    return Exception(maybe_exception)


def _wrap_callback_errors(callback, on_callback_error, message):
    """Wraps a user callback so that if an exception occurs the message is
    nacked.
    Args:
        callback (Callable[None, Message]): The user callback.
        message (~Message): The Pub/Sub message.
    """
    try:
        callback(message)
    except Exception as exc:
        # Note: the likelihood of this failing is extremely low. This just adds
        # a message to a queue, so if this doesn't work the world is in an
        # unrecoverable state and this thread should just bail.
        _LOGGER.exception(
            "Top-level exception occurred in callback while processing a message"
        )
        message.nack()
        on_callback_error(exc)


class AppendRowsStream(object):
    """Does _not_ automatically resume, since it might be a stream where offset
    should not be set, like the _default stream.

    TODO: Then again, maybe it makes sense to retry the last unacknowledge message
    always? If you write to _default / without offset, then you get semantics
    more like REST streaming method.
    """

    def __init__(
        self, client: big_query_write.BigQueryWriteClient,
    ):
        self._client = client
        self._inital_request = None
        self._stream_name = None
        self._rpc = None
        self._futures_queue = queue.Queue()

        # The threads created in ``.open()``.
        self._consumer = None

    def open(
        self,
        # TODO: Why does whereever I copied this from have: callback, on_callback_error?
        initial_request: gapic_types.AppendRowsRequest,
    ):
        # TODO: Error or no-op if already open?

        # TODO: _inital_request should be a callable to allow for stream
        # resumption based on oldest request that hasn't been processed.
        self._inital_request = initial_request
        self._stream_name = initial_request.write_stream
        # TODO: save trace ID too for _initial_request callable.

        # TODO: Do I need to avoid this when resuming stream?
        inital_response_future = AppendRowsFuture()
        self._futures_queue.put(inital_response_future)

        self._rpc = bidi.BidiRpc(
            self._client.append_rows,
            initial_request=self._inital_request,
            # TODO: allow additional metadata
            # This header is required so that the BigQuery Storage API knows which
            # region to route the request to.
            metadata=(("x-goog-request-params", f"write_stream={self._stream_name}"),),
        )

        self._consumer = bidi.BackgroundConsumer(self._rpc, self._on_response)
        self._consumer.start()
        return inital_response_future

    def send(self, request):
        # https://github.com/googleapis/python-pubsub/blob/master/google/cloud/pubsub_v1/subscriber/client.py#L228-L244
        # TODO: Return a future that waits for response. Maybe should be async?
        # https://github.com/googleapis/python-api-core/blob/master/google/api_core/future/polling.py
        # create future, add to queue
        future = AppendRowsFuture()
        self._futures_queue.put(future)
        self._rpc.send(request)
        return future

    def _on_response(self, response: gapic_types.AppendRowsResponse):
        """Process a response from a consumer callback."""
        # Since we have 1 response per request, if we get here from a response
        # callback, the queue should never be empty.
        future: AppendRowsFuture = self._futures_queue.get()
        # TODO: look at error and process (set exception or ignore "ALREAD_EXISTS")
        future.set_result(response)

    def close(self, reason=None):
        """Stop consuming messages and shutdown all helper threads.
        This method is idempotent. Additional calls will have no effect.
        The method does not block, it delegates the shutdown operations to a background
        thread.
        Args:
            reason (Any): The reason to close this. If ``None``, this is considered
                an "intentional" shutdown. This is passed to the callbacks
                specified via :meth:`add_close_callback`.
        """
        # TODO: Stop accepting new requests. Wait for in-flight futures?
        self._rpc.close()
        self._consumer.stop()

    def _should_recover(self, exception):
        """Determine if an error on the RPC stream should be recovered.
        If the exception is one of the retryable exceptions, this will signal
        to the consumer thread that it should "recover" from the failure.
        This will cause the stream to exit when it returns :data:`False`.
        Returns:
            bool: Indicates if the caller should recover or shut down.
            Will be :data:`True` if the ``exception`` is "acceptable", i.e.
            in a list of retryable / idempotent exceptions.
        """
        exception = _wrap_as_exception(exception)
        # If this is in the list of idempotent exceptions, then we want to
        # recover.
        if isinstance(exception, _RETRYABLE_STREAM_ERRORS):
            _LOGGER.info("Observed recoverable stream error %s", exception)
            return True
        _LOGGER.info("Observed non-recoverable stream error %s", exception)
        return False

    def _should_terminate(self, exception):
        """Determine if an error on the RPC stream should be terminated.
        If the exception is one of the terminating exceptions, this will signal
        to the consumer thread that it should terminate.
        This will cause the stream to exit when it returns :data:`True`.
        Returns:
            bool: Indicates if the caller should terminate or attempt recovery.
            Will be :data:`True` if the ``exception`` is "acceptable", i.e.
            in a list of terminating exceptions.
        """
        exception = _wrap_as_exception(exception)
        if isinstance(exception, _TERMINATING_STREAM_ERRORS):
            _LOGGER.info("Observed terminating stream error %s", exception)
            return True
        _LOGGER.info("Observed non-terminating stream error %s", exception)
        return False

    def _on_rpc_done(self, future):
        """Triggered whenever the underlying RPC terminates without recovery.
        This is typically triggered from one of two threads: the background
        consumer thread (when calling ``recv()`` produces a non-recoverable
        error) or the grpc management thread (when cancelling the RPC).
        This method is *non-blocking*. It will start another thread to deal
        with shutting everything down. This is to prevent blocking in the
        background consumer and preventing it from being ``joined()``.
        """
        _LOGGER.info("RPC termination has signaled streaming pull manager shutdown.")
        error = _wrap_as_exception(future)
        thread = threading.Thread(
            name=_RPC_ERROR_THREAD_NAME, target=self._shutdown, kwargs={"reason": error}
        )
        thread.daemon = True
        thread.start()


# https://github.com/googleapis/python-pubsub/blob/master/google/cloud/pubsub_v1/futures.py
# https://github.com/googleapis/python-pubsub/blob/master/google/cloud/pubsub_v1/publisher/futures.py
# https://github.com/googleapis/python-pubsub/blob/master/google/cloud/pubsub_v1/subscriber/futures.py
class AppendRowsFuture(concurrent.futures.Future, polling_future.PollingFuture):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from long-running BigQuery Storage API calls, and
    is the interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.
    """

    def done(self, retry: Optional[google.api_core.retry.Retry] = None) -> bool:
        """Check the status of the future.

        Args:
            retry:
                Not used. Included for compatibility with base clase. Future
                status is updated by a background thread.

        Returns:
            ``True`` if the request has finished, otherwise ``False``.
        """
        # Consumer should call set_result or set_exception method, where this
        # gets set to True *after* first setting _result.
        #
        # Consumer runs in a background thread, but this access is thread-safe:
        # https://docs.python.org/3/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
        return self._result_set

    def set_running_or_notify_cancel(self):
        """Not implemented.

        This method is needed to make the future API compatible with the
        concurrent.futures package, but since this is not constructed by an
        executor of the concurrent.futures package, no implementation is
        needed. See: https://github.com/googleapis/python-pubsub/pull/397
        """
        raise NotImplementedError(
            "Only used by executors from `concurrent.futures` package."
        )
