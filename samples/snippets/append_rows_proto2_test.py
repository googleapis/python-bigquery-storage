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

import pathlib
import random

from google.cloud import bigquery
import pytest

from . import append_rows_proto2


DIR = pathlib.Path(__file__).parent


# TODO: Fixture that write to table in non-default location.


@pytest.fixture()
def sample_data_table(
    bigquery_client: bigquery.Client, project_id: str, dataset_id: str
) -> str:
    schema = bigquery_client.schema_from_json(str(DIR / "sample_data_schema.json"))
    table_id = f"append_rows_proto2_{random.randrange(10000)}"
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id}", schema=schema)
    table = bigquery_client.create_table(table, exists_ok=True)
    yield table_id
    bigquery_client.delete_table(table, not_found_ok=True)


def test_append_rows_proto2(
    capsys: pytest.CaptureFixture,
    bigquery_client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    sample_data_table: str,
):
    append_rows_proto2.append_rows_proto2(
        project_id=project_id, dataset_id=dataset_id, table_id=sample_data_table
    )
    out, _ = capsys.readouterr()
    assert "have been committed" in out

    # TODO: Assert that the data actually shows up as expected.
    assert False
