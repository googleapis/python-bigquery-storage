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

import logging
import threading

import grpc

from google.api_core import bidi
from google.api_core import exceptions
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

    Then again, maybe it makes sense to retry the last unacknowledge message
    always? If you write to _default / without offset, then you get semantics
    more like REST streaming method.
    """

    def __init__(
        self,
        client: big_query_write.BigQueryWriteClient,
        initial_request: gapic_types.AppendRowsRequest,
    ):
        self._client = client
        self._inital_request = initial_request
        self._stream_name = initial_request.write_stream
        self._rpc = None

        # The threads created in ``.open()``.
        self._consumer = None

    def open(self):  # , callback, on_callback_error):
        self._rpc = bidi.BidiRpc(
            self._client.append_rows,
            initial_request=self._inital_request,
            # TODO: allow additional metadata
            # This header is required so that the BigQuery Storage API knows which
            # region to route the request to.
            metadata=(("x-goog-request-params", f"write_stream={self._stream_name}"),),
        )
        self._rpc.open()

    def send(self, request):
        self._rpc.send(request)

    def recv(self):
        return self._rpc.recv()

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
        self._rpc.close()

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
