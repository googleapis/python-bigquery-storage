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
import itertools
import logging
import queue
import time
import threading
from typing import Callable, Optional, Sequence, Tuple

from google.api_core import bidi
from google.api_core.future import polling as polling_future
from google.api_core import exceptions
import google.api_core.retry
import grpc

from google.cloud.bigquery_storage_v1beta2 import exceptions as bqstorage_exceptions
from google.cloud.bigquery_storage_v1beta2 import types as gapic_types
from google.cloud.bigquery_storage_v1beta2.services import big_query_write

_LOGGER = logging.getLogger(__name__)
_REGULAR_SHUTDOWN_THREAD_NAME = "Thread-RegularStreamShutdown"
_RPC_ERROR_THREAD_NAME = "Thread-OnRpcTerminated"

# open() takes between 0.25 and 0.4 seconds to be ready. Wait each loop before
# checking again. This interval was chosen to result in about 3 loops.
_WRITE_OPEN_INTERVAL = 0.08


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


class AppendRowsStream(object):
    """A manager object which can append rows to a stream."""

    def __init__(
        self,
        client: big_query_write.BigQueryWriteClient,
        metadata: Sequence[Tuple[str, str]] = (),
    ):
        """Construct a stream manager.

        Args:
            client:
                Low-level (generated) BigQueryWriteClient, responsible for
                making requests.
            metadata:
                Extra headers to include when sending the streaming request.
        """
        self._client = client
        self._closing = threading.Lock()
        self._closed = False
        self._close_callbacks = []
        self._futures_queue = queue.Queue()
        self._inital_request = None
        self._metadata = metadata
        self._rpc = None
        self._stream_name = None

        # The threads created in ``.open()``.
        self._consumer = None

    @property
    def is_active(self) -> bool:
        """bool: True if this manager is actively streaming.

        Note that ``False`` does not indicate this is complete shut down,
        just that it stopped getting new messages.
        """
        return self._consumer is not None and self._consumer.is_active

    def add_close_callback(self, callback: Callable):
        """Schedules a callable when the manager closes.
        Args:
            callback (Callable): The method to call.
        """
        self._close_callbacks.append(callback)

    def open(
        self,
        initial_request: gapic_types.AppendRowsRequest,
        timeout: Optional[float] = None,
    ) -> "AppendRowsFuture":
        """Open an append rows stream.

        This method is not intended to be called by end users. Instead, call
        ``BigQueryWriteClient.append_rows``.

        Args:
            initial_request:
                The initial request to start the stream. Must have
                :attr:`google.cloud.bigquery_storage_v1beta2.types.AppendRowsRequest.write_stream`
                and ``proto_rows.writer_schema.proto_descriptor`` and
                properties populated.
            timeout:
                How long (in seconds) to wait for the stream to be ready.

        Returns:
            A future, which can be used to process the response to the initial
            request when it arrives.
        """
        if self.is_active:
            raise ValueError("This manager is already open.")

        if self._closed:
            raise bqstorage_exceptions.StreamClosedError(
                "This manager has been closed and can not be re-used."
            )

        start_time = time.monotonic()
        self._inital_request = initial_request
        self._stream_name = initial_request.write_stream

        inital_response_future = AppendRowsFuture()
        self._futures_queue.put(inital_response_future)

        self._rpc = bidi.BidiRpc(
            self._client.append_rows,
            initial_request=self._inital_request,
            # TODO: pass in retry and timeout. Blocked by
            # https://github.com/googleapis/python-api-core/issues/262
            metadata=tuple(
                itertools.chain(
                    self._metadata,
                    # This header is required so that the BigQuery Storage API
                    # knows which region to route the request to.
                    (("x-goog-request-params", f"write_stream={self._stream_name}"),),
                )
            ),
        )
        self._rpc.add_done_callback(self._on_rpc_done)

        self._consumer = bidi.BackgroundConsumer(self._rpc, self._on_response)
        self._consumer.start()

        # Make sure RPC has started before returning.
        # Without this, consumers may get:
        #
        # ValueError: Can not send() on an RPC that has never been open()ed.
        #
        # when they try to send a request.
        while not self._rpc.is_active and self._consumer.is_active:
            # Avoid 100% CPU while waiting for RPC to be ready.
            time.sleep(_WRITE_OPEN_INTERVAL)

            # TODO: Check retry.deadline instead of (per-request) timeout.
            # Blocked by
            # https://github.com/googleapis/python-api-core/issues/262
            if timeout is None:
                continue
            current_time = time.monotonic()
            if current_time - start_time > timeout:
                break

        # Something went wrong when opening the RPC.
        if not self._consumer.is_active:
            # TODO: Share the exception from _rpc.open(). Blocked by
            # https://github.com/googleapis/python-api-core/issues/268
            inital_response_future.set_exception(
                exceptions.Unknown(
                    "There was a problem opening the stream. "
                    "Try turning on DEBUG level logs to see the error."
                )
            )

        return inital_response_future

    def send(self, request: gapic_types.AppendRowsRequest) -> "AppendRowsFuture":
        """Send an append rows request to the open stream.

        Args:
            request:
                The request to add to the stream.

        Returns:
            A future, which can be used to process the response when it
            arrives.
        """
        if self._closed:
            raise bqstorage_exceptions.StreamClosedError(
                "This manager has been closed and can not be used."
            )

        # For each request, we expect exactly one response (in order). Add a
        # future to the queue so that when the response comes, the callback can
        # pull it off and notify completion.
        future = AppendRowsFuture()
        self._futures_queue.put(future)
        self._rpc.send(request)
        return future

    def _on_response(self, response: gapic_types.AppendRowsResponse):
        """Process a response from a consumer callback."""
        # If the stream has closed, but somehow we still got a response message
        # back, discard it. The response futures queue has been drained, with
        # an exception reported.
        if self._closed:
            raise bqstorage_exceptions.StreamClosedError(
                f"Stream closed before receiving response: {response}"
            )

        # Since we have 1 response per request, if we get here from a response
        # callback, the queue should never be empty.
        future: AppendRowsFuture = self._futures_queue.get_nowait()
        if response.error.code:
            exc = exceptions.from_grpc_status(
                response.error.code, response.error.message
            )
            future.set_exception(exc)
        else:
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
        self._regular_shutdown_thread = threading.Thread(
            name=_REGULAR_SHUTDOWN_THREAD_NAME,
            daemon=True,
            target=self._shutdown,
            kwargs={"reason": reason},
        )
        self._regular_shutdown_thread.start()

    def _shutdown(self, reason=None):
        """Run the actual shutdown sequence (stop the stream and all helper threads).

        Args:
            reason (Any): The reason to close the stream. If ``None``, this is
                considered an "intentional" shutdown.
        """
        with self._closing:
            if self._closed:
                return

            # Stop consuming messages.
            if self.is_active:
                _LOGGER.debug("Stopping consumer.")
                self._consumer.stop()
            self._consumer = None

            self._rpc.close()
            self._rpc = None
            self._closed = True
            _LOGGER.debug("Finished stopping manager.")

            # We know that no new items will be added to the queue because
            # we've marked the stream as closed.
            while not self._futures_queue.empty():
                # Mark each future as failed. Since the consumer thread has
                # stopped (or at least is attempting to stop), we won't get
                # response callbacks to populate the remaining futures.
                future = self._futures_queue.get_nowait()
                exc = bqstorage_exceptions.StreamClosedError(
                    "Stream closed before receiving a response."
                )
                future.set_exception(exc)

            for callback in self._close_callbacks:
                callback(self, reason)

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
