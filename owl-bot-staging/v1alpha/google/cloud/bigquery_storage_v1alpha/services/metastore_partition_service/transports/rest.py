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

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.cloud.bigquery_storage_v1alpha.types import metastore_partition
from google.protobuf import empty_pb2  # type: ignore

from .base import MetastorePartitionServiceTransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class MetastorePartitionServiceRestInterceptor:
    """Interceptor for MetastorePartitionService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the MetastorePartitionServiceRestTransport.

    .. code-block:: python
        class MyCustomMetastorePartitionServiceInterceptor(MetastorePartitionServiceRestInterceptor):
            def pre_batch_create_metastore_partitions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_metastore_partitions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_batch_delete_metastore_partitions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_batch_update_metastore_partitions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_update_metastore_partitions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_metastore_partitions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_metastore_partitions(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = MetastorePartitionServiceRestTransport(interceptor=MyCustomMetastorePartitionServiceInterceptor())
        client = MetastorePartitionServiceClient(transport=transport)


    """
    def pre_batch_create_metastore_partitions(self, request: metastore_partition.BatchCreateMetastorePartitionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[metastore_partition.BatchCreateMetastorePartitionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_create_metastore_partitions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastorePartitionService server.
        """
        return request, metadata

    def post_batch_create_metastore_partitions(self, response: metastore_partition.BatchCreateMetastorePartitionsResponse) -> metastore_partition.BatchCreateMetastorePartitionsResponse:
        """Post-rpc interceptor for batch_create_metastore_partitions

        Override in a subclass to manipulate the response
        after it is returned by the MetastorePartitionService server but before
        it is returned to user code.
        """
        return response
    def pre_batch_delete_metastore_partitions(self, request: metastore_partition.BatchDeleteMetastorePartitionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[metastore_partition.BatchDeleteMetastorePartitionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_delete_metastore_partitions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastorePartitionService server.
        """
        return request, metadata

    def pre_batch_update_metastore_partitions(self, request: metastore_partition.BatchUpdateMetastorePartitionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[metastore_partition.BatchUpdateMetastorePartitionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for batch_update_metastore_partitions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastorePartitionService server.
        """
        return request, metadata

    def post_batch_update_metastore_partitions(self, response: metastore_partition.BatchUpdateMetastorePartitionsResponse) -> metastore_partition.BatchUpdateMetastorePartitionsResponse:
        """Post-rpc interceptor for batch_update_metastore_partitions

        Override in a subclass to manipulate the response
        after it is returned by the MetastorePartitionService server but before
        it is returned to user code.
        """
        return response
    def pre_list_metastore_partitions(self, request: metastore_partition.ListMetastorePartitionsRequest, metadata: Sequence[Tuple[str, str]]) -> Tuple[metastore_partition.ListMetastorePartitionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_metastore_partitions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the MetastorePartitionService server.
        """
        return request, metadata

    def post_list_metastore_partitions(self, response: metastore_partition.ListMetastorePartitionsResponse) -> metastore_partition.ListMetastorePartitionsResponse:
        """Post-rpc interceptor for list_metastore_partitions

        Override in a subclass to manipulate the response
        after it is returned by the MetastorePartitionService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class MetastorePartitionServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: MetastorePartitionServiceRestInterceptor


class MetastorePartitionServiceRestTransport(MetastorePartitionServiceTransport):
    """REST backend transport for MetastorePartitionService.

    BigQuery Metastore Partition Service API.
    This service is used for managing metastore partitions in
    BigQuery metastore. The service supports only batch operations
    for write.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(self, *,
            host: str = 'bigquerystorage.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            client_cert_source_for_mtls: Optional[Callable[[
                ], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            url_scheme: str = 'https',
            interceptor: Optional[MetastorePartitionServiceRestInterceptor] = None,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'bigquerystorage.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(f"Unexpected hostname structure: {host}")  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST)
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or MetastorePartitionServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _BatchCreateMetastorePartitions(MetastorePartitionServiceRestStub):
        def __hash__(self):
            return hash("BatchCreateMetastorePartitions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: metastore_partition.BatchCreateMetastorePartitionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> metastore_partition.BatchCreateMetastorePartitionsResponse:
            r"""Call the batch create metastore
        partitions method over HTTP.

            Args:
                request (~.metastore_partition.BatchCreateMetastorePartitionsRequest):
                    The request object. Request message for
                BatchCreateMetastorePartitions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore_partition.BatchCreateMetastorePartitionsResponse:
                    Response message for
                BatchCreateMetastorePartitions.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1alpha/{parent=projects/*/locations/*/datasets/*/tables/*}/partitions:batchCreate',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_create_metastore_partitions(request, metadata)
            pb_request = metastore_partition.BatchCreateMetastorePartitionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = metastore_partition.BatchCreateMetastorePartitionsResponse()
            pb_resp = metastore_partition.BatchCreateMetastorePartitionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_metastore_partitions(resp)
            return resp

    class _BatchDeleteMetastorePartitions(MetastorePartitionServiceRestStub):
        def __hash__(self):
            return hash("BatchDeleteMetastorePartitions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: metastore_partition.BatchDeleteMetastorePartitionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ):
            r"""Call the batch delete metastore
        partitions method over HTTP.

            Args:
                request (~.metastore_partition.BatchDeleteMetastorePartitionsRequest):
                    The request object. Request message for
                BatchDeleteMetastorePartitions. The
                MetastorePartition is uniquely
                identified by values, which is an
                ordered list. Hence, there is no
                separate name or partition id field.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1alpha/{parent=projects/*/locations/*/datasets/*/tables/*}/partitions:batchDelete',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_delete_metastore_partitions(request, metadata)
            pb_request = metastore_partition.BatchDeleteMetastorePartitionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _BatchUpdateMetastorePartitions(MetastorePartitionServiceRestStub):
        def __hash__(self):
            return hash("BatchUpdateMetastorePartitions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: metastore_partition.BatchUpdateMetastorePartitionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> metastore_partition.BatchUpdateMetastorePartitionsResponse:
            r"""Call the batch update metastore
        partitions method over HTTP.

            Args:
                request (~.metastore_partition.BatchUpdateMetastorePartitionsRequest):
                    The request object. Request message for
                BatchUpdateMetastorePartitions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore_partition.BatchUpdateMetastorePartitionsResponse:
                    Response message for
                BatchUpdateMetastorePartitions.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'post',
                'uri': '/v1alpha/{parent=projects/*/locations/*/datasets/*/tables/*}/partitions:batchUpdate',
                'body': '*',
            },
            ]
            request, metadata = self._interceptor.pre_batch_update_metastore_partitions(request, metadata)
            pb_request = metastore_partition.BatchUpdateMetastorePartitionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request['body'],
                use_integers_for_enums=True
            )
            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = metastore_partition.BatchUpdateMetastorePartitionsResponse()
            pb_resp = metastore_partition.BatchUpdateMetastorePartitionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_update_metastore_partitions(resp)
            return resp

    class _ListMetastorePartitions(MetastorePartitionServiceRestStub):
        def __hash__(self):
            return hash("ListMetastorePartitions")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] =  {
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {k: v for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items() if k not in message_dict}

        def __call__(self,
                request: metastore_partition.ListMetastorePartitionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> metastore_partition.ListMetastorePartitionsResponse:
            r"""Call the list metastore partitions method over HTTP.

            Args:
                request (~.metastore_partition.ListMetastorePartitionsRequest):
                    The request object. Request message for
                ListMetastorePartitions.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.metastore_partition.ListMetastorePartitionsResponse:
                    Response message for
                ListMetastorePartitions.

            """

            http_options: List[Dict[str, str]] = [{
                'method': 'get',
                'uri': '/v1alpha/{parent=projects/*/locations/*/datasets/*/tables/*}/partitions:list',
            },
            ]
            request, metadata = self._interceptor.pre_list_metastore_partitions(request, metadata)
            pb_request = metastore_partition.ListMetastorePartitionsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request['uri']
            method = transcoded_request['method']

            # Jsonify the query params
            query_params = json.loads(json_format.MessageToJson(
                transcoded_request['query_params'],
                use_integers_for_enums=True,
            ))
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers['Content-Type'] = 'application/json'
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = metastore_partition.ListMetastorePartitionsResponse()
            pb_resp = metastore_partition.ListMetastorePartitionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_metastore_partitions(resp)
            return resp

    class _StreamMetastorePartitions(MetastorePartitionServiceRestStub):
        def __hash__(self):
            return hash("StreamMetastorePartitions")

        def __call__(self,
                request: metastore_partition.StreamMetastorePartitionsRequest, *,
                retry: OptionalRetry=gapic_v1.method.DEFAULT,
                timeout: Optional[float]=None,
                metadata: Sequence[Tuple[str, str]]=(),
                ) -> rest_streaming.ResponseIterator:
            raise NotImplementedError(
                "Method StreamMetastorePartitions is not available over REST transport"
            )

    @property
    def batch_create_metastore_partitions(self) -> Callable[
            [metastore_partition.BatchCreateMetastorePartitionsRequest],
            metastore_partition.BatchCreateMetastorePartitionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateMetastorePartitions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def batch_delete_metastore_partitions(self) -> Callable[
            [metastore_partition.BatchDeleteMetastorePartitionsRequest],
            empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchDeleteMetastorePartitions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def batch_update_metastore_partitions(self) -> Callable[
            [metastore_partition.BatchUpdateMetastorePartitionsRequest],
            metastore_partition.BatchUpdateMetastorePartitionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchUpdateMetastorePartitions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def list_metastore_partitions(self) -> Callable[
            [metastore_partition.ListMetastorePartitionsRequest],
            metastore_partition.ListMetastorePartitionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMetastorePartitions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def stream_metastore_partitions(self) -> Callable[
            [metastore_partition.StreamMetastorePartitionsRequest],
            metastore_partition.StreamMetastorePartitionsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StreamMetastorePartitions(self._session, self._host, self._interceptor) # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__=(
    'MetastorePartitionServiceRestTransport',
)
