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

from unittest import mock

import pytest

from google.cloud.bigquery_storage_v1beta2.services import big_query_write
from google.cloud.bigquery_storage_v1beta2 import types as gapic_types


@pytest.fixture(scope="module")
def module_under_test():
    from google.cloud.bigquery_storage_v1beta2 import writer

    return writer


def test_constructor_and_default_state(module_under_test):
    mock_client = mock.create_autospec(big_query_write.BigQueryWriteClient)
    manager = module_under_test.AppendRowsStream(mock_client)

    # Public state
    assert manager.is_active is False

    # Private state
    assert manager._client is mock_client


@mock.patch("google.api_core.bidi.BidiRpc", autospec=True)
@mock.patch("google.api_core.bidi.BackgroundConsumer", autospec=True)
def test_open(background_consumer, bidi_rpc, module_under_test):
    mock_client = mock.create_autospec(big_query_write.BigQueryWriteClient)
    manager = module_under_test.AppendRowsStream(mock_client)
    type(bidi_rpc.return_value).is_active = mock.PropertyMock(
        return_value=(False, True)
    )
    initial_request = gapic_types.AppendRowsRequest(
        write_stream="this-is-a-stream-resource-path"
    )

    future = manager.open(initial_request)

    assert isinstance(future, module_under_test.AppendRowsFuture)
    background_consumer.assert_called_once_with(manager._rpc, manager._on_response)
    background_consumer.return_value.start.assert_called_once()
    assert manager._consumer == background_consumer.return_value

    bidi_rpc.assert_called_once_with(
        start_rpc=mock_client.append_rows,
        initial_request=initial_request,
        # Extra header is required to route requests to the correct location.
        metadata=(
            ("x-goog-request-params", "write_stream=this-is-a-stream-resource-path"),
        ),
    )

    bidi_rpc.return_value.add_done_callback.assert_called_once_with(
        manager._on_rpc_done
    )
    assert manager._rpc == bidi_rpc.return_value

    manager._consumer.is_active = True
    assert manager.is_active is True


# TODO: test that rpc is started after open()
# TODO: test for timeout
