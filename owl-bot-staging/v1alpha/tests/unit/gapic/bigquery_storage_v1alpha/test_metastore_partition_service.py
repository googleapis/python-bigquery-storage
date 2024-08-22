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
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from google.api_core import api_core_version
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service import MetastorePartitionServiceAsyncClient
from google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service import MetastorePartitionServiceClient
from google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service import transports
from google.cloud.bigquery_storage_v1alpha.types import metastore_partition
from google.cloud.bigquery_storage_v1alpha.types import partition
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"

# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT

# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return "test.{UNIVERSE_DOMAIN}" if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE) else client._DEFAULT_ENDPOINT_TEMPLATE


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(None) is None
    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert MetastorePartitionServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi

def test__read_environment_variables():
    assert MetastorePartitionServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (True, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError) as excinfo:
            MetastorePartitionServiceClient._read_environment_variables()
    assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (False, "never", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (False, "always", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (False, "auto", None)

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            MetastorePartitionServiceClient._read_environment_variables()
    assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert MetastorePartitionServiceClient._read_environment_variables() == (False, "auto", "foo.com")

def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert MetastorePartitionServiceClient._get_client_cert_source(None, False) is None
    assert MetastorePartitionServiceClient._get_client_cert_source(mock_provided_cert_source, False) is None
    assert MetastorePartitionServiceClient._get_client_cert_source(mock_provided_cert_source, True) == mock_provided_cert_source

    with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
        with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_default_cert_source):
            assert MetastorePartitionServiceClient._get_client_cert_source(None, True) is mock_default_cert_source
            assert MetastorePartitionServiceClient._get_client_cert_source(mock_provided_cert_source, "true") is mock_provided_cert_source

@mock.patch.object(MetastorePartitionServiceClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceClient))
@mock.patch.object(MetastorePartitionServiceAsyncClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceAsyncClient))
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = MetastorePartitionServiceClient._DEFAULT_UNIVERSE
    default_endpoint = MetastorePartitionServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=default_universe)
    mock_universe = "bar.com"
    mock_endpoint = MetastorePartitionServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=mock_universe)

    assert MetastorePartitionServiceClient._get_api_endpoint(api_override, mock_client_cert_source, default_universe, "always") == api_override
    assert MetastorePartitionServiceClient._get_api_endpoint(None, mock_client_cert_source, default_universe, "auto") == MetastorePartitionServiceClient.DEFAULT_MTLS_ENDPOINT
    assert MetastorePartitionServiceClient._get_api_endpoint(None, None, default_universe, "auto") == default_endpoint
    assert MetastorePartitionServiceClient._get_api_endpoint(None, None, default_universe, "always") == MetastorePartitionServiceClient.DEFAULT_MTLS_ENDPOINT
    assert MetastorePartitionServiceClient._get_api_endpoint(None, mock_client_cert_source, default_universe, "always") == MetastorePartitionServiceClient.DEFAULT_MTLS_ENDPOINT
    assert MetastorePartitionServiceClient._get_api_endpoint(None, None, mock_universe, "never") == mock_endpoint
    assert MetastorePartitionServiceClient._get_api_endpoint(None, None, default_universe, "never") == default_endpoint

    with pytest.raises(MutualTLSChannelError) as excinfo:
        MetastorePartitionServiceClient._get_api_endpoint(None, mock_client_cert_source, mock_universe, "auto")
    assert str(excinfo.value) == "mTLS is not supported in any universe other than googleapis.com."


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert MetastorePartitionServiceClient._get_universe_domain(client_universe_domain, universe_domain_env) == client_universe_domain
    assert MetastorePartitionServiceClient._get_universe_domain(None, universe_domain_env) == universe_domain_env
    assert MetastorePartitionServiceClient._get_universe_domain(None, None) == MetastorePartitionServiceClient._DEFAULT_UNIVERSE

    with pytest.raises(ValueError) as excinfo:
        MetastorePartitionServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest"),
])
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())
        transport=transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [int(part) for part in google.auth.__version__.split(".")[0:2]]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(
            transport=transport_class(credentials=credentials)
        )
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert str(excinfo.value) == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [int(part) for part in api_core_version.__version__.split(".")[0:2]]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(client_options={"universe_domain": "bar.com"}, transport=transport_class(credentials=ga_credentials.AnonymousCredentials(),))
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert str(excinfo.value) == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize("client_class,transport_name", [
    (MetastorePartitionServiceClient, "grpc"),
    (MetastorePartitionServiceAsyncClient, "grpc_asyncio"),
    (MetastorePartitionServiceClient, "rest"),
])
def test_metastore_partition_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'bigquerystorage.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://bigquerystorage.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.MetastorePartitionServiceGrpcTransport, "grpc"),
    (transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.MetastorePartitionServiceRestTransport, "rest"),
])
def test_metastore_partition_service_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (MetastorePartitionServiceClient, "grpc"),
    (MetastorePartitionServiceAsyncClient, "grpc_asyncio"),
    (MetastorePartitionServiceClient, "rest"),
])
def test_metastore_partition_service_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'bigquerystorage.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://bigquerystorage.googleapis.com'
        )


def test_metastore_partition_service_client_get_transport_class():
    transport = MetastorePartitionServiceClient.get_transport_class()
    available_transports = [
        transports.MetastorePartitionServiceGrpcTransport,
        transports.MetastorePartitionServiceRestTransport,
    ]
    assert transport in available_transports

    transport = MetastorePartitionServiceClient.get_transport_class("grpc")
    assert transport == transports.MetastorePartitionServiceGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc"),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest"),
])
@mock.patch.object(MetastorePartitionServiceClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceClient))
@mock.patch.object(MetastorePartitionServiceAsyncClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceAsyncClient))
def test_metastore_partition_service_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(MetastorePartitionServiceClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(MetastorePartitionServiceClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc", "true"),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc", "false"),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest", "true"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest", "false"),
])
@mock.patch.object(MetastorePartitionServiceClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceClient))
@mock.patch.object(MetastorePartitionServiceAsyncClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_metastore_partition_service_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE)
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE)
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    MetastorePartitionServiceClient, MetastorePartitionServiceAsyncClient
])
@mock.patch.object(MetastorePartitionServiceClient, "DEFAULT_ENDPOINT", modify_default_endpoint(MetastorePartitionServiceClient))
@mock.patch.object(MetastorePartitionServiceAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(MetastorePartitionServiceAsyncClient))
def test_metastore_partition_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert str(excinfo.value) == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"

@pytest.mark.parametrize("client_class", [
    MetastorePartitionServiceClient, MetastorePartitionServiceAsyncClient
])
@mock.patch.object(MetastorePartitionServiceClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceClient))
@mock.patch.object(MetastorePartitionServiceAsyncClient, "_DEFAULT_ENDPOINT_TEMPLATE", modify_default_endpoint_template(MetastorePartitionServiceAsyncClient))
def test_metastore_partition_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = MetastorePartitionServiceClient._DEFAULT_UNIVERSE
    default_endpoint = MetastorePartitionServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=default_universe)
    mock_universe = "bar.com"
    mock_endpoint = MetastorePartitionServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=mock_universe)

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"):
            options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=api_override)
            client = client_class(client_options=options, credentials=ga_credentials.AnonymousCredentials())
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(client_options=options, credentials=ga_credentials.AnonymousCredentials())
    else:
        client = client_class(client_options=options, credentials=ga_credentials.AnonymousCredentials())
    assert client.api_endpoint == (mock_endpoint if universe_exists else default_endpoint)
    assert client.universe_domain == (mock_universe if universe_exists else default_universe)

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(client_options=options, credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc"),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest"),
])
def test_metastore_partition_service_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc", grpc_helpers),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceRestTransport, "rest", None),
])
def test_metastore_partition_service_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_metastore_partition_service_client_client_options_from_dict():
    with mock.patch('google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.transports.MetastorePartitionServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = MetastorePartitionServiceClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport, "grpc", grpc_helpers),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_metastore_partition_service_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "bigquerystorage.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/bigquery',
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="bigquerystorage.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  metastore_partition.BatchCreateMetastorePartitionsRequest,
  dict,
])
def test_batch_create_metastore_partitions(request_type, transport: str = 'grpc'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore_partition.BatchCreateMetastorePartitionsResponse(
        )
        response = client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchCreateMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchCreateMetastorePartitionsResponse)


def test_batch_create_metastore_partitions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_create_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchCreateMetastorePartitionsRequest()


def test_batch_create_metastore_partitions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = metastore_partition.BatchCreateMetastorePartitionsRequest(
        parent='parent_value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_create_metastore_partitions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchCreateMetastorePartitionsRequest(
            parent='parent_value',
        )

def test_batch_create_metastore_partitions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_create_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_create_metastore_partitions] = mock_rpc
        request = {}
        client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_create_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_create_metastore_partitions_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchCreateMetastorePartitionsResponse(
        ))
        response = await client.batch_create_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchCreateMetastorePartitionsRequest()

@pytest.mark.asyncio
async def test_batch_create_metastore_partitions_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._client._transport.batch_create_metastore_partitions in client._client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[client._client._transport.batch_create_metastore_partitions] = mock_rpc

        request = {}
        await client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.batch_create_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_create_metastore_partitions_async(transport: str = 'grpc_asyncio', request_type=metastore_partition.BatchCreateMetastorePartitionsRequest):
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchCreateMetastorePartitionsResponse(
        ))
        response = await client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchCreateMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchCreateMetastorePartitionsResponse)


@pytest.mark.asyncio
async def test_batch_create_metastore_partitions_async_from_dict():
    await test_batch_create_metastore_partitions_async(request_type=dict)


def test_batch_create_metastore_partitions_field_headers():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchCreateMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        call.return_value = metastore_partition.BatchCreateMetastorePartitionsResponse()
        client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_batch_create_metastore_partitions_field_headers_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchCreateMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_create_metastore_partitions),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchCreateMetastorePartitionsResponse())
        await client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  metastore_partition.BatchDeleteMetastorePartitionsRequest,
  dict,
])
def test_batch_delete_metastore_partitions(request_type, transport: str = 'grpc'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchDeleteMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_batch_delete_metastore_partitions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_delete_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchDeleteMetastorePartitionsRequest()


def test_batch_delete_metastore_partitions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = metastore_partition.BatchDeleteMetastorePartitionsRequest(
        parent='parent_value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_delete_metastore_partitions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchDeleteMetastorePartitionsRequest(
            parent='parent_value',
        )

def test_batch_delete_metastore_partitions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_delete_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_delete_metastore_partitions] = mock_rpc
        request = {}
        client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_delete_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_delete_metastore_partitions_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.batch_delete_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchDeleteMetastorePartitionsRequest()

@pytest.mark.asyncio
async def test_batch_delete_metastore_partitions_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._client._transport.batch_delete_metastore_partitions in client._client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[client._client._transport.batch_delete_metastore_partitions] = mock_rpc

        request = {}
        await client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.batch_delete_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_delete_metastore_partitions_async(transport: str = 'grpc_asyncio', request_type=metastore_partition.BatchDeleteMetastorePartitionsRequest):
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchDeleteMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_batch_delete_metastore_partitions_async_from_dict():
    await test_batch_delete_metastore_partitions_async(request_type=dict)


def test_batch_delete_metastore_partitions_field_headers():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchDeleteMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        call.return_value = None
        client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_batch_delete_metastore_partitions_field_headers_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchDeleteMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_delete_metastore_partitions),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  metastore_partition.BatchUpdateMetastorePartitionsRequest,
  dict,
])
def test_batch_update_metastore_partitions(request_type, transport: str = 'grpc'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse(
        )
        response = client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchUpdateMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchUpdateMetastorePartitionsResponse)


def test_batch_update_metastore_partitions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_update_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchUpdateMetastorePartitionsRequest()


def test_batch_update_metastore_partitions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = metastore_partition.BatchUpdateMetastorePartitionsRequest(
        parent='parent_value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.batch_update_metastore_partitions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchUpdateMetastorePartitionsRequest(
            parent='parent_value',
        )

def test_batch_update_metastore_partitions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_update_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_update_metastore_partitions] = mock_rpc
        request = {}
        client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_update_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_update_metastore_partitions_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchUpdateMetastorePartitionsResponse(
        ))
        response = await client.batch_update_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.BatchUpdateMetastorePartitionsRequest()

@pytest.mark.asyncio
async def test_batch_update_metastore_partitions_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._client._transport.batch_update_metastore_partitions in client._client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[client._client._transport.batch_update_metastore_partitions] = mock_rpc

        request = {}
        await client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.batch_update_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_batch_update_metastore_partitions_async(transport: str = 'grpc_asyncio', request_type=metastore_partition.BatchUpdateMetastorePartitionsRequest):
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchUpdateMetastorePartitionsResponse(
        ))
        response = await client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.BatchUpdateMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchUpdateMetastorePartitionsResponse)


@pytest.mark.asyncio
async def test_batch_update_metastore_partitions_async_from_dict():
    await test_batch_update_metastore_partitions_async(request_type=dict)


def test_batch_update_metastore_partitions_field_headers():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchUpdateMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        call.return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse()
        client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_batch_update_metastore_partitions_field_headers_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.BatchUpdateMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.batch_update_metastore_partitions),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.BatchUpdateMetastorePartitionsResponse())
        await client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.parametrize("request_type", [
  metastore_partition.ListMetastorePartitionsRequest,
  dict,
])
def test_list_metastore_partitions(request_type, transport: str = 'grpc'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore_partition.ListMetastorePartitionsResponse(
        )
        response = client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.ListMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.ListMetastorePartitionsResponse)


def test_list_metastore_partitions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.list_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.ListMetastorePartitionsRequest()


def test_list_metastore_partitions_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = metastore_partition.ListMetastorePartitionsRequest(
        parent='parent_value',
        filter='filter_value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        call.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client.list_metastore_partitions(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.ListMetastorePartitionsRequest(
            parent='parent_value',
            filter='filter_value',
        )

def test_list_metastore_partitions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.list_metastore_partitions] = mock_rpc
        request = {}
        client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_list_metastore_partitions_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.ListMetastorePartitionsResponse(
        ))
        response = await client.list_metastore_partitions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == metastore_partition.ListMetastorePartitionsRequest()

@pytest.mark.asyncio
async def test_list_metastore_partitions_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._client._transport.list_metastore_partitions in client._client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[client._client._transport.list_metastore_partitions] = mock_rpc

        request = {}
        await client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.list_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_list_metastore_partitions_async(transport: str = 'grpc_asyncio', request_type=metastore_partition.ListMetastorePartitionsRequest):
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.ListMetastorePartitionsResponse(
        ))
        response = await client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = metastore_partition.ListMetastorePartitionsRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.ListMetastorePartitionsResponse)


@pytest.mark.asyncio
async def test_list_metastore_partitions_async_from_dict():
    await test_list_metastore_partitions_async(request_type=dict)


def test_list_metastore_partitions_field_headers():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.ListMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        call.return_value = metastore_partition.ListMetastorePartitionsResponse()
        client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_metastore_partitions_field_headers_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = metastore_partition.ListMetastorePartitionsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.ListMetastorePartitionsResponse())
        await client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_metastore_partitions_flattened():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore_partition.ListMetastorePartitionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_metastore_partitions(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_metastore_partitions_flattened_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_metastore_partitions(
            metastore_partition.ListMetastorePartitionsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_metastore_partitions_flattened_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = metastore_partition.ListMetastorePartitionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(metastore_partition.ListMetastorePartitionsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_metastore_partitions(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_metastore_partitions_flattened_error_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_metastore_partitions(
            metastore_partition.ListMetastorePartitionsRequest(),
            parent='parent_value',
        )


@pytest.mark.parametrize("request_type", [
  metastore_partition.StreamMetastorePartitionsRequest,
  dict,
])
def test_stream_metastore_partitions(request_type, transport: str = 'grpc'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.stream_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([metastore_partition.StreamMetastorePartitionsResponse()])
        response = client.stream_metastore_partitions(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, metastore_partition.StreamMetastorePartitionsResponse)


def test_stream_metastore_partitions_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.stream_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.stream_metastore_partitions] = mock_rpc
        request = [{}]
        client.stream_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.stream_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_stream_metastore_partitions_async_use_cached_wrapped_rpc(transport: str = "grpc_asyncio"):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._client._transport.stream_metastore_partitions in client._client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.AsyncMock()
        mock_rpc.return_value = mock.Mock()
        client._client._transport._wrapped_methods[client._client._transport.stream_metastore_partitions] = mock_rpc

        request = [{}]
        await client.stream_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        await client.stream_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2

@pytest.mark.asyncio
async def test_stream_metastore_partitions_async(transport: str = 'grpc_asyncio', request_type=metastore_partition.StreamMetastorePartitionsRequest):
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()
    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.stream_metastore_partitions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = mock.Mock(aio.StreamStreamCall, autospec=True)
        call.return_value.read = mock.AsyncMock(side_effect=[metastore_partition.StreamMetastorePartitionsResponse()])
        response = await client.stream_metastore_partitions(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    message = await response.read()
    assert isinstance(message, metastore_partition.StreamMetastorePartitionsResponse)


@pytest.mark.asyncio
async def test_stream_metastore_partitions_async_from_dict():
    await test_stream_metastore_partitions_async(request_type=dict)


@pytest.mark.parametrize("request_type", [
    metastore_partition.BatchCreateMetastorePartitionsRequest,
    dict,
])
def test_batch_create_metastore_partitions_rest(request_type):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore_partition.BatchCreateMetastorePartitionsResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = metastore_partition.BatchCreateMetastorePartitionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_create_metastore_partitions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchCreateMetastorePartitionsResponse)

def test_batch_create_metastore_partitions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_create_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_create_metastore_partitions] = mock_rpc

        request = {}
        client.batch_create_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_create_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_batch_create_metastore_partitions_rest_required_fields(request_type=metastore_partition.BatchCreateMetastorePartitionsRequest):
    transport_class = transports.MetastorePartitionServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_create_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore_partition.BatchCreateMetastorePartitionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = metastore_partition.BatchCreateMetastorePartitionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_create_metastore_partitions(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_create_metastore_partitions_rest_unset_required_fields():
    transport = transports.MetastorePartitionServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_create_metastore_partitions._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "requests", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_create_metastore_partitions_rest_interceptors(null_interceptor):
    transport = transports.MetastorePartitionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.MetastorePartitionServiceRestInterceptor(),
        )
    client = MetastorePartitionServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "post_batch_create_metastore_partitions") as post, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "pre_batch_create_metastore_partitions") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore_partition.BatchCreateMetastorePartitionsRequest.pb(metastore_partition.BatchCreateMetastorePartitionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore_partition.BatchCreateMetastorePartitionsResponse.to_json(metastore_partition.BatchCreateMetastorePartitionsResponse())

        request = metastore_partition.BatchCreateMetastorePartitionsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore_partition.BatchCreateMetastorePartitionsResponse()

        client.batch_create_metastore_partitions(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_create_metastore_partitions_rest_bad_request(transport: str = 'rest', request_type=metastore_partition.BatchCreateMetastorePartitionsRequest):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_create_metastore_partitions(request)


def test_batch_create_metastore_partitions_rest_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    metastore_partition.BatchDeleteMetastorePartitionsRequest,
    dict,
])
def test_batch_delete_metastore_partitions_rest(request_type):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ''

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_delete_metastore_partitions(request)

    # Establish that the response is the type that we expect.
    assert response is None

def test_batch_delete_metastore_partitions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_delete_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_delete_metastore_partitions] = mock_rpc

        request = {}
        client.batch_delete_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_delete_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_batch_delete_metastore_partitions_rest_required_fields(request_type=metastore_partition.BatchDeleteMetastorePartitionsRequest):
    transport_class = transports.MetastorePartitionServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_delete_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_delete_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ''

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_delete_metastore_partitions(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_delete_metastore_partitions_rest_unset_required_fields():
    transport = transports.MetastorePartitionServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_delete_metastore_partitions._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "partitionValues", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_delete_metastore_partitions_rest_interceptors(null_interceptor):
    transport = transports.MetastorePartitionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.MetastorePartitionServiceRestInterceptor(),
        )
    client = MetastorePartitionServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "pre_batch_delete_metastore_partitions") as pre:
        pre.assert_not_called()
        pb_message = metastore_partition.BatchDeleteMetastorePartitionsRequest.pb(metastore_partition.BatchDeleteMetastorePartitionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = metastore_partition.BatchDeleteMetastorePartitionsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.batch_delete_metastore_partitions(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()


def test_batch_delete_metastore_partitions_rest_bad_request(transport: str = 'rest', request_type=metastore_partition.BatchDeleteMetastorePartitionsRequest):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_delete_metastore_partitions(request)


def test_batch_delete_metastore_partitions_rest_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    metastore_partition.BatchUpdateMetastorePartitionsRequest,
    dict,
])
def test_batch_update_metastore_partitions_rest(request_type):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.batch_update_metastore_partitions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.BatchUpdateMetastorePartitionsResponse)

def test_batch_update_metastore_partitions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.batch_update_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.batch_update_metastore_partitions] = mock_rpc

        request = {}
        client.batch_update_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.batch_update_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_batch_update_metastore_partitions_rest_required_fields(request_type=metastore_partition.BatchUpdateMetastorePartitionsRequest):
    transport_class = transports.MetastorePartitionServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_update_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).batch_update_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.batch_update_metastore_partitions(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_batch_update_metastore_partitions_rest_unset_required_fields():
    transport = transports.MetastorePartitionServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.batch_update_metastore_partitions._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("parent", "requests", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_batch_update_metastore_partitions_rest_interceptors(null_interceptor):
    transport = transports.MetastorePartitionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.MetastorePartitionServiceRestInterceptor(),
        )
    client = MetastorePartitionServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "post_batch_update_metastore_partitions") as post, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "pre_batch_update_metastore_partitions") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore_partition.BatchUpdateMetastorePartitionsRequest.pb(metastore_partition.BatchUpdateMetastorePartitionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore_partition.BatchUpdateMetastorePartitionsResponse.to_json(metastore_partition.BatchUpdateMetastorePartitionsResponse())

        request = metastore_partition.BatchUpdateMetastorePartitionsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore_partition.BatchUpdateMetastorePartitionsResponse()

        client.batch_update_metastore_partitions(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_batch_update_metastore_partitions_rest_bad_request(transport: str = 'rest', request_type=metastore_partition.BatchUpdateMetastorePartitionsRequest):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.batch_update_metastore_partitions(request)


def test_batch_update_metastore_partitions_rest_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    metastore_partition.ListMetastorePartitionsRequest,
    dict,
])
def test_list_metastore_partitions_rest(request_type):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore_partition.ListMetastorePartitionsResponse(
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = metastore_partition.ListMetastorePartitionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_metastore_partitions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, metastore_partition.ListMetastorePartitionsResponse)

def test_list_metastore_partitions_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert client._transport.list_metastore_partitions in client._transport._wrapped_methods

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = "foo" # operation_request.operation in compute client(s) expect a string.
        client._transport._wrapped_methods[client._transport.list_metastore_partitions] = mock_rpc

        request = {}
        client.list_metastore_partitions(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_metastore_partitions(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_metastore_partitions_rest_required_fields(request_type=metastore_partition.ListMetastorePartitionsRequest):
    transport_class = transports.MetastorePartitionServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_metastore_partitions._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_metastore_partitions._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = metastore_partition.ListMetastorePartitionsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = metastore_partition.ListMetastorePartitionsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_metastore_partitions(request)

            expected_params = [
                ('$alt', 'json;enum-encoding=int')
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_metastore_partitions_rest_unset_required_fields():
    transport = transports.MetastorePartitionServiceRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_metastore_partitions._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_metastore_partitions_rest_interceptors(null_interceptor):
    transport = transports.MetastorePartitionServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.MetastorePartitionServiceRestInterceptor(),
        )
    client = MetastorePartitionServiceClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "post_list_metastore_partitions") as post, \
         mock.patch.object(transports.MetastorePartitionServiceRestInterceptor, "pre_list_metastore_partitions") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = metastore_partition.ListMetastorePartitionsRequest.pb(metastore_partition.ListMetastorePartitionsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = metastore_partition.ListMetastorePartitionsResponse.to_json(metastore_partition.ListMetastorePartitionsResponse())

        request = metastore_partition.ListMetastorePartitionsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = metastore_partition.ListMetastorePartitionsResponse()

        client.list_metastore_partitions(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_metastore_partitions_rest_bad_request(transport: str = 'rest', request_type=metastore_partition.ListMetastorePartitionsRequest):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_metastore_partitions(request)


def test_list_metastore_partitions_rest_flattened():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = metastore_partition.ListMetastorePartitionsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/datasets/sample3/tables/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = metastore_partition.ListMetastorePartitionsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_metastore_partitions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1alpha/{parent=projects/*/locations/*/datasets/*/tables/*}/partitions:list" % client.transport._host, args[1])


def test_list_metastore_partitions_rest_flattened_error(transport: str = 'rest'):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_metastore_partitions(
            metastore_partition.ListMetastorePartitionsRequest(),
            parent='parent_value',
        )


def test_list_metastore_partitions_rest_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_stream_metastore_partitions_rest_no_http_options():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = metastore_partition.StreamMetastorePartitionsRequest()
    requests = [request]
    with pytest.raises(RuntimeError):
        client.stream_metastore_partitions(requests)


def test_stream_metastore_partitions_rest_error():
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )
    # Since a `google.api.http` annotation is required for using a rest transport
    # method, this should error.
    with pytest.raises(NotImplementedError) as not_implemented_error:
        client.stream_metastore_partitions({})
    assert (
        "Method StreamMetastorePartitions is not available over REST transport"
        in str(not_implemented_error.value)
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastorePartitionServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MetastorePartitionServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = MetastorePartitionServiceClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetastorePartitionServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = MetastorePartitionServiceClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MetastorePartitionServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.MetastorePartitionServiceGrpcTransport,
    transports.MetastorePartitionServiceGrpcAsyncIOTransport,
    transports.MetastorePartitionServiceRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = MetastorePartitionServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.MetastorePartitionServiceGrpcTransport,
    )

def test_metastore_partition_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.MetastorePartitionServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_metastore_partition_service_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.transports.MetastorePartitionServiceTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.MetastorePartitionServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'batch_create_metastore_partitions',
        'batch_delete_metastore_partitions',
        'batch_update_metastore_partitions',
        'list_metastore_partitions',
        'stream_metastore_partitions',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_metastore_partition_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.transports.MetastorePartitionServiceTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MetastorePartitionServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/bigquery',
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_metastore_partition_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.bigquery_storage_v1alpha.services.metastore_partition_service.transports.MetastorePartitionServiceTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.MetastorePartitionServiceTransport()
        adc.assert_called_once()


def test_metastore_partition_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        MetastorePartitionServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/bigquery',
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastorePartitionServiceGrpcTransport,
        transports.MetastorePartitionServiceGrpcAsyncIOTransport,
    ],
)
def test_metastore_partition_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/bigquery',                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetastorePartitionServiceGrpcTransport,
        transports.MetastorePartitionServiceGrpcAsyncIOTransport,
        transports.MetastorePartitionServiceRestTransport,
    ],
)
def test_metastore_partition_service_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.MetastorePartitionServiceGrpcTransport, grpc_helpers),
        (transports.MetastorePartitionServiceGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_metastore_partition_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "bigquerystorage.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/bigquery',
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="bigquerystorage.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.MetastorePartitionServiceGrpcTransport, transports.MetastorePartitionServiceGrpcAsyncIOTransport])
def test_metastore_partition_service_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_metastore_partition_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.MetastorePartitionServiceRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_metastore_partition_service_host_no_port(transport_name):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='bigquerystorage.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'bigquerystorage.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://bigquerystorage.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_metastore_partition_service_host_with_port(transport_name):
    client = MetastorePartitionServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='bigquerystorage.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'bigquerystorage.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://bigquerystorage.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_metastore_partition_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = MetastorePartitionServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = MetastorePartitionServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.batch_create_metastore_partitions._session
    session2 = client2.transport.batch_create_metastore_partitions._session
    assert session1 != session2
    session1 = client1.transport.batch_delete_metastore_partitions._session
    session2 = client2.transport.batch_delete_metastore_partitions._session
    assert session1 != session2
    session1 = client1.transport.batch_update_metastore_partitions._session
    session2 = client2.transport.batch_update_metastore_partitions._session
    assert session1 != session2
    session1 = client1.transport.list_metastore_partitions._session
    session2 = client2.transport.list_metastore_partitions._session
    assert session1 != session2
    session1 = client1.transport.stream_metastore_partitions._session
    session2 = client2.transport.stream_metastore_partitions._session
    assert session1 != session2
def test_metastore_partition_service_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetastorePartitionServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_metastore_partition_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetastorePartitionServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.MetastorePartitionServiceGrpcTransport, transports.MetastorePartitionServiceGrpcAsyncIOTransport])
def test_metastore_partition_service_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
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
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.MetastorePartitionServiceGrpcTransport, transports.MetastorePartitionServiceGrpcAsyncIOTransport])
def test_metastore_partition_service_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
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
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_read_stream_path():
    project = "squid"
    location = "clam"
    session = "whelk"
    stream = "octopus"
    expected = "projects/{project}/locations/{location}/sessions/{session}/streams/{stream}".format(project=project, location=location, session=session, stream=stream, )
    actual = MetastorePartitionServiceClient.read_stream_path(project, location, session, stream)
    assert expected == actual


def test_parse_read_stream_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "session": "cuttlefish",
        "stream": "mussel",
    }
    path = MetastorePartitionServiceClient.read_stream_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_read_stream_path(path)
    assert expected == actual

def test_table_path():
    project = "winkle"
    dataset = "nautilus"
    table = "scallop"
    expected = "projects/{project}/datasets/{dataset}/tables/{table}".format(project=project, dataset=dataset, table=table, )
    actual = MetastorePartitionServiceClient.table_path(project, dataset, table)
    assert expected == actual


def test_parse_table_path():
    expected = {
        "project": "abalone",
        "dataset": "squid",
        "table": "clam",
    }
    path = MetastorePartitionServiceClient.table_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_table_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = MetastorePartitionServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = MetastorePartitionServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder, )
    actual = MetastorePartitionServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = MetastorePartitionServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = MetastorePartitionServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = MetastorePartitionServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project, )
    actual = MetastorePartitionServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = MetastorePartitionServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = MetastorePartitionServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = MetastorePartitionServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MetastorePartitionServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.MetastorePartitionServiceTransport, '_prep_wrapped_messages') as prep:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.MetastorePartitionServiceTransport, '_prep_wrapped_messages') as prep:
        transport_class = MetastorePartitionServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = MetastorePartitionServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = MetastorePartitionServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (MetastorePartitionServiceClient, transports.MetastorePartitionServiceGrpcTransport),
    (MetastorePartitionServiceAsyncClient, transports.MetastorePartitionServiceGrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
