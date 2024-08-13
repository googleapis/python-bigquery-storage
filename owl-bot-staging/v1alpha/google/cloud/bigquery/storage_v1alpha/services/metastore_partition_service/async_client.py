# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import re
from typing import Dict, Callable, Mapping, MutableMapping, MutableSequence, Optional, AsyncIterable, Awaitable, AsyncIterator, Sequence, Tuple, Type, Union

from google.cloud.bigquery.storage_v1alpha import gapic_version as package_version

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials   # type: ignore
from google.oauth2 import service_account              # type: ignore


try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.cloud.bigquery.storage_v1alpha.types import metastore_partition
from google.cloud.bigquery.storage_v1alpha.types import partition
from .transports.base import MetastorePartitionServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import MetastorePartitionServiceGrpcAsyncIOTransport
from .client import MetastorePartitionServiceClient


class MetastorePartitionServiceAsyncClient:
    """BigQuery Metastore Partition Service API.
    This service is used for managing metastore partitions in
    BigQuery metastore. The service supports only batch operations
    for write.
    """

    _client: MetastorePartitionServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = MetastorePartitionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MetastorePartitionServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = MetastorePartitionServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = MetastorePartitionServiceClient._DEFAULT_UNIVERSE

    read_stream_path = staticmethod(MetastorePartitionServiceClient.read_stream_path)
    parse_read_stream_path = staticmethod(MetastorePartitionServiceClient.parse_read_stream_path)
    table_path = staticmethod(MetastorePartitionServiceClient.table_path)
    parse_table_path = staticmethod(MetastorePartitionServiceClient.parse_table_path)
    common_billing_account_path = staticmethod(MetastorePartitionServiceClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(MetastorePartitionServiceClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(MetastorePartitionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(MetastorePartitionServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(MetastorePartitionServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(MetastorePartitionServiceClient.parse_common_organization_path)
    common_project_path = staticmethod(MetastorePartitionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(MetastorePartitionServiceClient.parse_common_project_path)
    common_location_path = staticmethod(MetastorePartitionServiceClient.common_location_path)
    parse_common_location_path = staticmethod(MetastorePartitionServiceClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            MetastorePartitionServiceAsyncClient: The constructed client.
        """
        return MetastorePartitionServiceClient.from_service_account_info.__func__(MetastorePartitionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MetastorePartitionServiceAsyncClient: The constructed client.
        """
        return MetastorePartitionServiceClient.from_service_account_file.__func__(MetastorePartitionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[ClientOptions] = None):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return MetastorePartitionServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> MetastorePartitionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MetastorePartitionServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = MetastorePartitionServiceClient.get_transport_class

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Optional[Union[str, MetastorePartitionServiceTransport, Callable[..., MetastorePartitionServiceTransport]]] = "grpc_asyncio",
            client_options: Optional[ClientOptions] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the metastore partition service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,MetastorePartitionServiceTransport,Callable[..., MetastorePartitionServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the MetastorePartitionServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = MetastorePartitionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def batch_create_metastore_partitions(self,
            request: Optional[Union[metastore_partition.BatchCreateMetastorePartitionsRequest, dict]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> metastore_partition.BatchCreateMetastorePartitionsResponse:
        r"""Adds metastore partitions to a table.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.bigquery import storage_v1alpha

            async def sample_batch_create_metastore_partitions():
                # Create a client
                client = storage_v1alpha.MetastorePartitionServiceAsyncClient()

                # Initialize request argument(s)
                requests = storage_v1alpha.CreateMetastorePartitionRequest()
                requests.parent = "parent_value"
                requests.metastore_partition.values = ['values_value1', 'values_value2']

                request = storage_v1alpha.BatchCreateMetastorePartitionsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = await client.batch_create_metastore_partitions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.bigquery.storage_v1alpha.types.BatchCreateMetastorePartitionsRequest, dict]]):
                The request object. Request message for
                BatchCreateMetastorePartitions.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery.storage_v1alpha.types.BatchCreateMetastorePartitionsResponse:
                Response message for
                BatchCreateMetastorePartitions.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, metastore_partition.BatchCreateMetastorePartitionsRequest):
            request = metastore_partition.BatchCreateMetastorePartitionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[self._client._transport.batch_create_metastore_partitions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_delete_metastore_partitions(self,
            request: Optional[Union[metastore_partition.BatchDeleteMetastorePartitionsRequest, dict]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> None:
        r"""Deletes metastore partitions from a table.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.bigquery import storage_v1alpha

            async def sample_batch_delete_metastore_partitions():
                # Create a client
                client = storage_v1alpha.MetastorePartitionServiceAsyncClient()

                # Initialize request argument(s)
                partition_values = storage_v1alpha.MetastorePartitionValues()
                partition_values.values = ['values_value1', 'values_value2']

                request = storage_v1alpha.BatchDeleteMetastorePartitionsRequest(
                    parent="parent_value",
                    partition_values=partition_values,
                )

                # Make the request
                await client.batch_delete_metastore_partitions(request=request)

        Args:
            request (Optional[Union[google.cloud.bigquery.storage_v1alpha.types.BatchDeleteMetastorePartitionsRequest, dict]]):
                The request object. Request message for
                BatchDeleteMetastorePartitions. The
                MetastorePartition is uniquely
                identified by values, which is an
                ordered list. Hence, there is no
                separate name or partition id field.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, metastore_partition.BatchDeleteMetastorePartitionsRequest):
            request = metastore_partition.BatchDeleteMetastorePartitionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[self._client._transport.batch_delete_metastore_partitions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def batch_update_metastore_partitions(self,
            request: Optional[Union[metastore_partition.BatchUpdateMetastorePartitionsRequest, dict]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> metastore_partition.BatchUpdateMetastorePartitionsResponse:
        r"""Updates metastore partitions in a table.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.bigquery import storage_v1alpha

            async def sample_batch_update_metastore_partitions():
                # Create a client
                client = storage_v1alpha.MetastorePartitionServiceAsyncClient()

                # Initialize request argument(s)
                requests = storage_v1alpha.UpdateMetastorePartitionRequest()
                requests.metastore_partition.values = ['values_value1', 'values_value2']

                request = storage_v1alpha.BatchUpdateMetastorePartitionsRequest(
                    parent="parent_value",
                    requests=requests,
                )

                # Make the request
                response = await client.batch_update_metastore_partitions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.bigquery.storage_v1alpha.types.BatchUpdateMetastorePartitionsRequest, dict]]):
                The request object. Request message for
                BatchUpdateMetastorePartitions.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery.storage_v1alpha.types.BatchUpdateMetastorePartitionsResponse:
                Response message for
                BatchUpdateMetastorePartitions.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, metastore_partition.BatchUpdateMetastorePartitionsRequest):
            request = metastore_partition.BatchUpdateMetastorePartitionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[self._client._transport.batch_update_metastore_partitions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_metastore_partitions(self,
            request: Optional[Union[metastore_partition.ListMetastorePartitionsRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> metastore_partition.ListMetastorePartitionsResponse:
        r"""Gets metastore partitions from a table.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.bigquery import storage_v1alpha

            async def sample_list_metastore_partitions():
                # Create a client
                client = storage_v1alpha.MetastorePartitionServiceAsyncClient()

                # Initialize request argument(s)
                request = storage_v1alpha.ListMetastorePartitionsRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.list_metastore_partitions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.bigquery.storage_v1alpha.types.ListMetastorePartitionsRequest, dict]]):
                The request object. Request message for
                ListMetastorePartitions.
            parent (:class:`str`):
                Required. Reference to the table to
                which these metastore partitions belong,
                in the format of
                projects/{project}/locations/{location}/datasets/{dataset}/tables/{table}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery.storage_v1alpha.types.ListMetastorePartitionsResponse:
                Response message for
                ListMetastorePartitions.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, metastore_partition.ListMetastorePartitionsRequest):
            request = metastore_partition.ListMetastorePartitionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[self._client._transport.list_metastore_partitions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def stream_metastore_partitions(self,
            requests: Optional[AsyncIterator[metastore_partition.StreamMetastorePartitionsRequest]] = None,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> Awaitable[AsyncIterable[metastore_partition.StreamMetastorePartitionsResponse]]:
        r"""This is a bi-di streaming rpc method that allows the
        client to send a stream of partitions and commit all of
        them atomically at the end. If the commit is successful,
        the server will return a response and close the stream.
        If the commit fails (due to duplicate partitions or
        other reason), the server will close the stream with an
        error. This method is only available via the gRPC API
        (not REST).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud.bigquery import storage_v1alpha

            async def sample_stream_metastore_partitions():
                # Create a client
                client = storage_v1alpha.MetastorePartitionServiceAsyncClient()

                # Initialize request argument(s)
                request = storage_v1alpha.StreamMetastorePartitionsRequest(
                    parent="parent_value",
                )

                # This method expects an iterator which contains
                # 'storage_v1alpha.StreamMetastorePartitionsRequest' objects
                # Here we create a generator that yields a single `request` for
                # demonstrative purposes.
                requests = [request]

                def request_generator():
                    for request in requests:
                        yield request

                # Make the request
                stream = await client.stream_metastore_partitions(requests=request_generator())

                # Handle the response
                async for response in stream:
                    print(response)

        Args:
            requests (AsyncIterator[`google.cloud.bigquery.storage_v1alpha.types.StreamMetastorePartitionsRequest`]):
                The request object AsyncIterator. The top-level message sent by the client to the
                `Partitions.StreamMetastorePartitions <>`__ method.
                Follows the default gRPC streaming maximum size of 4 MB.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.bigquery.storage_v1alpha.types.StreamMetastorePartitionsResponse]:
                This is the response message sent by the server
                   to the client for the
                   [Partitions.StreamMetastorePartitions]() method when
                   the commit is successful. Server will close the
                   stream after sending this message.

        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[self._client._transport.stream_metastore_partitions]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = rpc(
            requests,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "MetastorePartitionServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "MetastorePartitionServiceAsyncClient",
)