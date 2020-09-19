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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigquery.storage_v1beta1.services.big_query_storage import (
    BigQueryStorageAsyncClient,
)
from google.cloud.bigquery.storage_v1beta1.services.big_query_storage import (
    BigQueryStorageClient,
)
from google.cloud.bigquery.storage_v1beta1.services.big_query_storage import transports
from google.cloud.bigquery.storage_v1beta1.types import arrow
from google.cloud.bigquery.storage_v1beta1.types import avro
from google.cloud.bigquery.storage_v1beta1.types import read_options
from google.cloud.bigquery.storage_v1beta1.types import storage
from google.cloud.bigquery.storage_v1beta1.types import table_reference
from google.cloud.bigquery.storage_v1beta1.types import (
    table_reference as gcbs_table_reference,
)
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert BigQueryStorageClient._get_default_mtls_endpoint(None) is None
    assert (
        BigQueryStorageClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigQueryStorageClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        BigQueryStorageClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigQueryStorageClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        BigQueryStorageClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [BigQueryStorageClient, BigQueryStorageAsyncClient]
)
def test_big_query_storage_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "bigquerystorage.googleapis.com:443"


def test_big_query_storage_client_get_transport_class():
    transport = BigQueryStorageClient.get_transport_class()
    assert transport == transports.BigQueryStorageGrpcTransport

    transport = BigQueryStorageClient.get_transport_class("grpc")
    assert transport == transports.BigQueryStorageGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigQueryStorageClient, transports.BigQueryStorageGrpcTransport, "grpc"),
        (
            BigQueryStorageAsyncClient,
            transports.BigQueryStorageGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    BigQueryStorageClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryStorageClient),
)
@mock.patch.object(
    BigQueryStorageAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryStorageAsyncClient),
)
def test_big_query_storage_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BigQueryStorageClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BigQueryStorageClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            BigQueryStorageClient,
            transports.BigQueryStorageGrpcTransport,
            "grpc",
            "true",
        ),
        (
            BigQueryStorageAsyncClient,
            transports.BigQueryStorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            BigQueryStorageClient,
            transports.BigQueryStorageGrpcTransport,
            "grpc",
            "false",
        ),
        (
            BigQueryStorageAsyncClient,
            transports.BigQueryStorageGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    BigQueryStorageClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryStorageClient),
)
@mock.patch.object(
    BigQueryStorageAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(BigQueryStorageAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_big_query_storage_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigQueryStorageClient, transports.BigQueryStorageGrpcTransport, "grpc"),
        (
            BigQueryStorageAsyncClient,
            transports.BigQueryStorageGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_storage_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (BigQueryStorageClient, transports.BigQueryStorageGrpcTransport, "grpc"),
        (
            BigQueryStorageAsyncClient,
            transports.BigQueryStorageGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_big_query_storage_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_big_query_storage_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.bigquery.storage_v1beta1.services.big_query_storage.transports.BigQueryStorageGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = BigQueryStorageClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_read_session(
    transport: str = "grpc", request_type=storage.CreateReadSessionRequest
):
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ReadSession(
            name="name_value",
            sharding_strategy=storage.ShardingStrategy.LIQUID,
            avro_schema=avro.AvroSchema(schema="schema_value"),
        )

        response = client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.CreateReadSessionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.ReadSession)

    assert response.name == "name_value"

    assert response.sharding_strategy == storage.ShardingStrategy.LIQUID


def test_create_read_session_from_dict():
    test_create_read_session(request_type=dict)


@pytest.mark.asyncio
async def test_create_read_session_async(transport: str = "grpc_asyncio"):
    client = BigQueryStorageAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = storage.CreateReadSessionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.ReadSession(
                name="name_value", sharding_strategy=storage.ShardingStrategy.LIQUID,
            )
        )

        response = await client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.ReadSession)

    assert response.name == "name_value"

    assert response.sharding_strategy == storage.ShardingStrategy.LIQUID


def test_create_read_session_field_headers():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateReadSessionRequest()
    request.table_reference.project_id = "table_reference.project_id/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_read_session), "__call__"
    ) as call:
        call.return_value = storage.ReadSession()

        client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "table_reference.project_id=table_reference.project_id/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_read_session_field_headers_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.CreateReadSessionRequest()
    request.table_reference.project_id = "table_reference.project_id/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_read_session), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.ReadSession())

        await client.create_read_session(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "table_reference.project_id=table_reference.project_id/value",
    ) in kw["metadata"]


def test_create_read_session_flattened():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ReadSession()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_read_session(
            table_reference=gcbs_table_reference.TableReference(
                project_id="project_id_value"
            ),
            parent="parent_value",
            requested_streams=1840,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].table_reference == gcbs_table_reference.TableReference(
            project_id="project_id_value"
        )

        assert args[0].parent == "parent_value"

        assert args[0].requested_streams == 1840


def test_create_read_session_flattened_error():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_read_session(
            storage.CreateReadSessionRequest(),
            table_reference=gcbs_table_reference.TableReference(
                project_id="project_id_value"
            ),
            parent="parent_value",
            requested_streams=1840,
        )


@pytest.mark.asyncio
async def test_create_read_session_flattened_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_read_session), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.ReadSession()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(storage.ReadSession())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_read_session(
            table_reference=gcbs_table_reference.TableReference(
                project_id="project_id_value"
            ),
            parent="parent_value",
            requested_streams=1840,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].table_reference == gcbs_table_reference.TableReference(
            project_id="project_id_value"
        )

        assert args[0].parent == "parent_value"

        assert args[0].requested_streams == 1840


@pytest.mark.asyncio
async def test_create_read_session_flattened_error_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_read_session(
            storage.CreateReadSessionRequest(),
            table_reference=gcbs_table_reference.TableReference(
                project_id="project_id_value"
            ),
            parent="parent_value",
            requested_streams=1840,
        )


def test_read_rows(transport: str = "grpc", request_type=storage.ReadRowsRequest):
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        response = client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.ReadRowsRequest()

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, storage.ReadRowsResponse)


def test_read_rows_from_dict():
    test_read_rows(request_type=dict)


@pytest.mark.asyncio
async def test_read_rows_async(transport: str = "grpc_asyncio"):
    client = BigQueryStorageAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = storage.ReadRowsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.read_rows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.ReadRowsResponse()]
        )

        response = await client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, storage.ReadRowsResponse)


def test_read_rows_field_headers():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ReadRowsRequest()
    request.read_position.stream.name = "read_position.stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.read_rows), "__call__") as call:
        call.return_value = iter([storage.ReadRowsResponse()])

        client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "read_position.stream.name=read_position.stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_read_rows_field_headers_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.ReadRowsRequest()
    request.read_position.stream.name = "read_position.stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.read_rows), "__call__"
    ) as call:
        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(
            side_effect=[storage.ReadRowsResponse()]
        )

        await client.read_rows(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "read_position.stream.name=read_position.stream.name/value",
    ) in kw["metadata"]


def test_read_rows_flattened():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.read_rows), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.read_rows(
            read_position=storage.StreamPosition(
                stream=storage.Stream(name="name_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].read_position == storage.StreamPosition(
            stream=storage.Stream(name="name_value")
        )


def test_read_rows_flattened_error():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.read_rows(
            storage.ReadRowsRequest(),
            read_position=storage.StreamPosition(
                stream=storage.Stream(name="name_value")
            ),
        )


@pytest.mark.asyncio
async def test_read_rows_flattened_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.read_rows), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([storage.ReadRowsResponse()])

        call.return_value = mock.Mock(aio.UnaryStreamCall, autospec=True)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.read_rows(
            read_position=storage.StreamPosition(
                stream=storage.Stream(name="name_value")
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].read_position == storage.StreamPosition(
            stream=storage.Stream(name="name_value")
        )


@pytest.mark.asyncio
async def test_read_rows_flattened_error_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.read_rows(
            storage.ReadRowsRequest(),
            read_position=storage.StreamPosition(
                stream=storage.Stream(name="name_value")
            ),
        )


def test_batch_create_read_session_streams(
    transport: str = "grpc", request_type=storage.BatchCreateReadSessionStreamsRequest
):
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCreateReadSessionStreamsResponse()

        response = client.batch_create_read_session_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.BatchCreateReadSessionStreamsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.BatchCreateReadSessionStreamsResponse)


def test_batch_create_read_session_streams_from_dict():
    test_batch_create_read_session_streams(request_type=dict)


@pytest.mark.asyncio
async def test_batch_create_read_session_streams_async(transport: str = "grpc_asyncio"):
    client = BigQueryStorageAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = storage.BatchCreateReadSessionStreamsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCreateReadSessionStreamsResponse()
        )

        response = await client.batch_create_read_session_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.BatchCreateReadSessionStreamsResponse)


def test_batch_create_read_session_streams_field_headers():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.BatchCreateReadSessionStreamsRequest()
    request.session.name = "session.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        call.return_value = storage.BatchCreateReadSessionStreamsResponse()

        client.batch_create_read_session_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session.name=session.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_batch_create_read_session_streams_field_headers_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.BatchCreateReadSessionStreamsRequest()
    request.session.name = "session.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCreateReadSessionStreamsResponse()
        )

        await client.batch_create_read_session_streams(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "session.name=session.name/value",) in kw[
        "metadata"
    ]


def test_batch_create_read_session_streams_flattened():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCreateReadSessionStreamsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_read_session_streams(
            session=storage.ReadSession(name="name_value"), requested_streams=1840,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].session == storage.ReadSession(name="name_value")

        assert args[0].requested_streams == 1840


def test_batch_create_read_session_streams_flattened_error():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_read_session_streams(
            storage.BatchCreateReadSessionStreamsRequest(),
            session=storage.ReadSession(name="name_value"),
            requested_streams=1840,
        )


@pytest.mark.asyncio
async def test_batch_create_read_session_streams_flattened_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_read_session_streams), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.BatchCreateReadSessionStreamsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.BatchCreateReadSessionStreamsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_read_session_streams(
            session=storage.ReadSession(name="name_value"), requested_streams=1840,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].session == storage.ReadSession(name="name_value")

        assert args[0].requested_streams == 1840


@pytest.mark.asyncio
async def test_batch_create_read_session_streams_flattened_error_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_read_session_streams(
            storage.BatchCreateReadSessionStreamsRequest(),
            session=storage.ReadSession(name="name_value"),
            requested_streams=1840,
        )


def test_finalize_stream(
    transport: str = "grpc", request_type=storage.FinalizeStreamRequest
):
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.finalize_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.finalize_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.FinalizeStreamRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_finalize_stream_from_dict():
    test_finalize_stream(request_type=dict)


@pytest.mark.asyncio
async def test_finalize_stream_async(transport: str = "grpc_asyncio"):
    client = BigQueryStorageAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = storage.FinalizeStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.finalize_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.finalize_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_finalize_stream_field_headers():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FinalizeStreamRequest()
    request.stream.name = "stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.finalize_stream), "__call__") as call:
        call.return_value = None

        client.finalize_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "stream.name=stream.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_finalize_stream_field_headers_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.FinalizeStreamRequest()
    request.stream.name = "stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.finalize_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.finalize_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "stream.name=stream.name/value",) in kw["metadata"]


def test_finalize_stream_flattened():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.finalize_stream), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.finalize_stream(stream=storage.Stream(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].stream == storage.Stream(name="name_value")


def test_finalize_stream_flattened_error():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.finalize_stream(
            storage.FinalizeStreamRequest(), stream=storage.Stream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_finalize_stream_flattened_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.finalize_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.finalize_stream(
            stream=storage.Stream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].stream == storage.Stream(name="name_value")


@pytest.mark.asyncio
async def test_finalize_stream_flattened_error_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.finalize_stream(
            storage.FinalizeStreamRequest(), stream=storage.Stream(name="name_value"),
        )


def test_split_read_stream(
    transport: str = "grpc", request_type=storage.SplitReadStreamRequest
):
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.SplitReadStreamResponse()

        response = client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == storage.SplitReadStreamRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.SplitReadStreamResponse)


def test_split_read_stream_from_dict():
    test_split_read_stream(request_type=dict)


@pytest.mark.asyncio
async def test_split_read_stream_async(transport: str = "grpc_asyncio"):
    client = BigQueryStorageAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = storage.SplitReadStreamRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.SplitReadStreamResponse()
        )

        response = await client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, storage.SplitReadStreamResponse)


def test_split_read_stream_field_headers():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.SplitReadStreamRequest()
    request.original_stream.name = "original_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.split_read_stream), "__call__"
    ) as call:
        call.return_value = storage.SplitReadStreamResponse()

        client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "original_stream.name=original_stream.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_split_read_stream_field_headers_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = storage.SplitReadStreamRequest()
    request.original_stream.name = "original_stream.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.split_read_stream), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.SplitReadStreamResponse()
        )

        await client.split_read_stream(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "original_stream.name=original_stream.name/value",
    ) in kw["metadata"]


def test_split_read_stream_flattened():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.SplitReadStreamResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.split_read_stream(original_stream=storage.Stream(name="name_value"),)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].original_stream == storage.Stream(name="name_value")


def test_split_read_stream_flattened_error():
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.split_read_stream(
            storage.SplitReadStreamRequest(),
            original_stream=storage.Stream(name="name_value"),
        )


@pytest.mark.asyncio
async def test_split_read_stream_flattened_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.split_read_stream), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = storage.SplitReadStreamResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            storage.SplitReadStreamResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.split_read_stream(
            original_stream=storage.Stream(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].original_stream == storage.Stream(name="name_value")


@pytest.mark.asyncio
async def test_split_read_stream_flattened_error_async():
    client = BigQueryStorageAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.split_read_stream(
            storage.SplitReadStreamRequest(),
            original_stream=storage.Stream(name="name_value"),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BigQueryStorageGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryStorageClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BigQueryStorageGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryStorageClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BigQueryStorageGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BigQueryStorageClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryStorageGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = BigQueryStorageClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BigQueryStorageGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BigQueryStorageGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryStorageGrpcTransport,
        transports.BigQueryStorageGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BigQueryStorageClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.BigQueryStorageGrpcTransport,)


def test_big_query_storage_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.BigQueryStorageTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_big_query_storage_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.bigquery.storage_v1beta1.services.big_query_storage.transports.BigQueryStorageTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.BigQueryStorageTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_read_session",
        "read_rows",
        "batch_create_read_session_streams",
        "finalize_stream",
        "split_read_stream",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_big_query_storage_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.bigquery.storage_v1beta1.services.big_query_storage.transports.BigQueryStorageTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryStorageTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_storage_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.bigquery.storage_v1beta1.services.big_query_storage.transports.BigQueryStorageTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.BigQueryStorageTransport()
        adc.assert_called_once()


def test_big_query_storage_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        BigQueryStorageClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_big_query_storage_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.BigQueryStorageGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/bigquery.readonly",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_big_query_storage_host_no_port():
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com"
        ),
    )
    assert client._transport._host == "bigquerystorage.googleapis.com:443"


def test_big_query_storage_host_with_port():
    client = BigQueryStorageClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="bigquerystorage.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "bigquerystorage.googleapis.com:8000"


def test_big_query_storage_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.BigQueryStorageGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


def test_big_query_storage_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.BigQueryStorageGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryStorageGrpcTransport,
        transports.BigQueryStorageGrpcAsyncIOTransport,
    ],
)
def test_big_query_storage_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.readonly",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BigQueryStorageGrpcTransport,
        transports.BigQueryStorageGrpcAsyncIOTransport,
    ],
)
def test_big_query_storage_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/bigquery",
                    "https://www.googleapis.com/auth/bigquery.readonly",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_read_session_path():
    project = "squid"
    location = "clam"
    session = "whelk"

    expected = "projects/{project}/locations/{location}/sessions/{session}".format(
        project=project, location=location, session=session,
    )
    actual = BigQueryStorageClient.read_session_path(project, location, session)
    assert expected == actual


def test_parse_read_session_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "session": "nudibranch",
    }
    path = BigQueryStorageClient.read_session_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryStorageClient.parse_read_session_path(path)
    assert expected == actual


def test_stream_path():
    project = "squid"
    location = "clam"
    stream = "whelk"

    expected = "projects/{project}/locations/{location}/streams/{stream}".format(
        project=project, location=location, stream=stream,
    )
    actual = BigQueryStorageClient.stream_path(project, location, stream)
    assert expected == actual


def test_parse_stream_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "stream": "nudibranch",
    }
    path = BigQueryStorageClient.stream_path(**expected)

    # Check that the path construction is reversible.
    actual = BigQueryStorageClient.parse_stream_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.BigQueryStorageTransport, "_prep_wrapped_messages"
    ) as prep:
        client = BigQueryStorageClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.BigQueryStorageTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = BigQueryStorageClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
