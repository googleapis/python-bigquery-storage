# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
from distutils import util
import os
import re
from typing import Callable, Dict, Iterable, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigquery.storage_v1beta1.types import arrow
from google.cloud.bigquery.storage_v1beta1.types import avro
from google.cloud.bigquery.storage_v1beta1.types import storage
from google.cloud.bigquery.storage_v1beta1.types import (
    table_reference as gcbs_table_reference,
)
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import BigQueryStorageTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BigQueryStorageGrpcTransport
from .transports.grpc_asyncio import BigQueryStorageGrpcAsyncIOTransport


class BigQueryStorageClientMeta(type):
    """Metaclass for the BigQueryStorage client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BigQueryStorageTransport]]
    _transport_registry["grpc"] = BigQueryStorageGrpcTransport
    _transport_registry["grpc_asyncio"] = BigQueryStorageGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[BigQueryStorageTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class BigQueryStorageClient(metaclass=BigQueryStorageClientMeta):
    """BigQuery storage API.
    The BigQuery storage API can be used to read data stored in
    BigQuery.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "bigquerystorage.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def read_session_path(project: str, location: str, session: str,) -> str:
        """Return a fully-qualified read_session string."""
        return "projects/{project}/locations/{location}/sessions/{session}".format(
            project=project, location=location, session=session,
        )

    @staticmethod
    def parse_read_session_path(path: str) -> Dict[str, str]:
        """Parse a read_session path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/sessions/(?P<session>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def stream_path(project: str, location: str, stream: str,) -> str:
        """Return a fully-qualified stream string."""
        return "projects/{project}/locations/{location}/streams/{stream}".format(
            project=project, location=location, stream=stream,
        )

    @staticmethod
    def parse_stream_path(path: str) -> Dict[str, str]:
        """Parse a stream path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/streams/(?P<stream>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, BigQueryStorageTransport] = None,
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the big query storage client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigQueryStorageTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT if is_mtls else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, BigQueryStorageTransport):
            # transport is a BigQueryStorageTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                ssl_channel_credentials=ssl_credentials,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def create_read_session(
        self,
        request: storage.CreateReadSessionRequest = None,
        *,
        table_reference: gcbs_table_reference.TableReference = None,
        parent: str = None,
        requested_streams: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.ReadSession:
        r"""Creates a new read session. A read session divides
        the contents of a BigQuery table into one or more
        streams, which can then be used to read data from the
        table. The read session also specifies properties of the
        data to be read, such as a list of columns or a push-
        down filter describing the rows to be returned.

        A particular row can be read by at most one stream. When
        the caller has reached the end of each stream in the
        session, then all the data in the table has been read.

        Read sessions automatically expire 24 hours after they
        are created and do not require manual clean-up by the
        caller.

        Args:
            request (:class:`~.storage.CreateReadSessionRequest`):
                The request object. Creates a new read session, which
                may include additional options such as requested
                parallelism, projection filters and constraints.
            table_reference (:class:`~.gcbs_table_reference.TableReference`):
                Required. Reference to the table to
                read.
                This corresponds to the ``table_reference`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parent (:class:`str`):
                Required. String of the form ``projects/{project_id}``
                indicating the project this ReadSession is associated
                with. This is the project that will be billed for usage.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requested_streams (:class:`int`):
                Initial number of streams. If unset
                or 0, we will provide a value of streams
                so as to produce reasonable throughput.
                Must be non-negative. The number of
                streams may be lower than the requested
                number, depending on the amount
                parallelism that is reasonable for the
                table and the maximum amount of
                parallelism allowed by the system.
                Streams must be read starting from
                offset 0.
                This corresponds to the ``requested_streams`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.storage.ReadSession:
                Information returned from a ``CreateReadSession``
                request.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([table_reference, parent, requested_streams])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.CreateReadSessionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.CreateReadSessionRequest):
            request = storage.CreateReadSessionRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if table_reference is not None:
                request.table_reference = table_reference
            if parent is not None:
                request.parent = parent
            if requested_streams is not None:
                request.requested_streams = requested_streams

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_read_session]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("table_reference.project_id", request.table_reference.project_id),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def read_rows(
        self,
        request: storage.ReadRowsRequest = None,
        *,
        read_position: storage.StreamPosition = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[storage.ReadRowsResponse]:
        r"""Reads rows from the table in the format prescribed by
        the read session. Each response contains one or more
        table rows, up to a maximum of 10 MiB per response; read
        requests which attempt to read individual rows larger
        than this will fail.

        Each request also returns a set of stream statistics
        reflecting the estimated total number of rows in the
        read stream. This number is computed based on the total
        table size and the number of active streams in the read
        session, and may change as other streams continue to
        read data.

        Args:
            request (:class:`~.storage.ReadRowsRequest`):
                The request object. Requesting row data via `ReadRows`
                must provide Stream position information.
            read_position (:class:`~.storage.StreamPosition`):
                Required. Identifier of the position
                in the stream to start reading from. The
                offset requested must be less than the
                last row read from ReadRows. Requesting
                a larger offset is undefined.
                This corresponds to the ``read_position`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[~.storage.ReadRowsResponse]:
                Response from calling ``ReadRows`` may include row data,
                progress and throttling information.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([read_position])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.ReadRowsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.ReadRowsRequest):
            request = storage.ReadRowsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if read_position is not None:
                request.read_position = read_position

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.read_rows]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("read_position.stream.name", request.read_position.stream.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_create_read_session_streams(
        self,
        request: storage.BatchCreateReadSessionStreamsRequest = None,
        *,
        session: storage.ReadSession = None,
        requested_streams: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.BatchCreateReadSessionStreamsResponse:
        r"""Creates additional streams for a ReadSession. This
        API can be used to dynamically adjust the parallelism of
        a batch processing task upwards by adding additional
        workers.

        Args:
            request (:class:`~.storage.BatchCreateReadSessionStreamsRequest`):
                The request object. Information needed to request
                additional streams for an established read session.
            session (:class:`~.storage.ReadSession`):
                Required. Must be a non-expired
                session obtained from a call to
                CreateReadSession. Only the name field
                needs to be set.
                This corresponds to the ``session`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            requested_streams (:class:`int`):
                Required. Number of new streams
                requested. Must be positive. Number of
                added streams may be less than this, see
                CreateReadSessionRequest for more
                information.
                This corresponds to the ``requested_streams`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.storage.BatchCreateReadSessionStreamsResponse:
                The response from ``BatchCreateReadSessionStreams``
                returns the stream identifiers for the newly created
                streams.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([session, requested_streams])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.BatchCreateReadSessionStreamsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.BatchCreateReadSessionStreamsRequest):
            request = storage.BatchCreateReadSessionStreamsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if session is not None:
                request.session = session
            if requested_streams is not None:
                request.requested_streams = requested_streams

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.batch_create_read_session_streams
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("session.name", request.session.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def finalize_stream(
        self,
        request: storage.FinalizeStreamRequest = None,
        *,
        stream: storage.Stream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Triggers the graceful termination of a single stream
        in a ReadSession. This API can be used to dynamically
        adjust the parallelism of a batch processing task
        downwards without losing data.

        This API does not delete the stream -- it remains
        visible in the ReadSession, and any data processed by
        the stream is not released to other streams. However, no
        additional data will be assigned to the stream once this
        call completes. Callers must continue reading data on
        the stream until the end of the stream is reached so
        that data which has already been assigned to the stream
        will be processed.

        This method will return an error if there are no other
        live streams in the Session, or if SplitReadStream() has
        been called on the given Stream.

        Args:
            request (:class:`~.storage.FinalizeStreamRequest`):
                The request object. Request information for invoking
                `FinalizeStream`.
            stream (:class:`~.storage.Stream`):
                Required. Stream to finalize.
                This corresponds to the ``stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.FinalizeStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.FinalizeStreamRequest):
            request = storage.FinalizeStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if stream is not None:
                request.stream = stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.finalize_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("stream.name", request.stream.name),)
            ),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def split_read_stream(
        self,
        request: storage.SplitReadStreamRequest = None,
        *,
        original_stream: storage.Stream = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage.SplitReadStreamResponse:
        r"""Splits a given read stream into two Streams. These streams are
        referred to as the primary and the residual of the split. The
        original stream can still be read from in the same manner as
        before. Both of the returned streams can also be read from, and
        the total rows return by both child streams will be the same as
        the rows read from the original stream.

        Moreover, the two child streams will be allocated back to back
        in the original Stream. Concretely, it is guaranteed that for
        streams Original, Primary, and Residual, that Original[0-j] =
        Primary[0-j] and Original[j-n] = Residual[0-m] once the streams
        have been read to completion.

        This method is guaranteed to be idempotent.

        Args:
            request (:class:`~.storage.SplitReadStreamRequest`):
                The request object. Request information for
                `SplitReadStream`.
            original_stream (:class:`~.storage.Stream`):
                Required. Stream to split.
                This corresponds to the ``original_stream`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.storage.SplitReadStreamResponse:
                Response from ``SplitReadStream``.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([original_stream])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a storage.SplitReadStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, storage.SplitReadStreamRequest):
            request = storage.SplitReadStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if original_stream is not None:
                request.original_stream = original_stream

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.split_read_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("original_stream.name", request.original_stream.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-storage",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigQueryStorageClient",)
