# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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
"""System tests for reading rows from tables."""

import os
import uuid

import pytest

_TABLE_FORMAT = "projects/{}/datasets/{}/tables/{}"

_ASSETS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets")


@pytest.fixture(scope="session")
def project_id():
    return os.environ["PROJECT_ID"]


@pytest.fixture(scope="session")
def use_mtls():
    return "always" == os.environ.get("GOOGLE_API_USE_MTLS_ENDPOINT", "never")


@pytest.fixture(scope="session")
def credentials(use_mtls):
    import google.auth
    from google.oauth2 import service_account

    if use_mtls:
        # mTLS test uses user credentials instead of service account credentials
        creds, _ = google.auth.default()
        return creds

    # NOTE: the test config in noxfile checks that the env variable is indeed set
    filename = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    return service_account.Credentials.from_service_account_file(filename)


@pytest.fixture()
def table_reference():
    return _TABLE_FORMAT.format("bigquery-public-data", "usa_names", "usa_1910_2013")


@pytest.fixture()
def small_table_reference():
    return _TABLE_FORMAT.format(
        "bigquery-public-data", "utility_us", "country_code_iso"
    )


@pytest.fixture(scope="session")
def local_shakespeare_table_reference(project_id, use_mtls):
    if use_mtls:
        pytest.skip(
            "Skip it for mTLS testing since the table does not exist for mTLS project"
        )
    return _TABLE_FORMAT.format(project_id, "public_samples_copy", "shakespeare")


@pytest.fixture(scope="session")
def dataset(project_id, bq_client):
    from google.cloud import bigquery

    unique_suffix = str(uuid.uuid4()).replace("-", "_")
    dataset_name = "bq_storage_system_tests_" + unique_suffix

    dataset_id = "{}.{}".format(project_id, dataset_name)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    created_dataset = bq_client.create_dataset(dataset)

    yield created_dataset

    bq_client.delete_dataset(dataset, delete_contents=True)


@pytest.fixture(scope="session")
def table(project_id, dataset, bq_client):
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
    ]

    table_id = "{}.{}.{}".format(project_id, dataset.dataset_id, "users")
    bq_table = bigquery.Table(table_id, schema=schema)
    created_table = bq_client.create_table(bq_table)

    yield created_table

    bq_client.delete_table(created_table)


@pytest.fixture(scope="session")
def bq_client(credentials, use_mtls):
    if use_mtls:
        pytest.skip("Skip it for mTLS testing since bigquery does not support mTLS")
    from google.cloud import bigquery

    return bigquery.Client(credentials=credentials)


@pytest.fixture
def all_types_table_ref(project_id, dataset, bq_client):
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("string_field", "STRING"),
        bigquery.SchemaField("bytes_field", "BYTES"),
        bigquery.SchemaField("int64_field", "INT64"),
        bigquery.SchemaField("float64_field", "FLOAT64"),
        bigquery.SchemaField("numeric_field", "NUMERIC"),
        bigquery.SchemaField("bool_field", "BOOL"),
        bigquery.SchemaField("geography_field", "GEOGRAPHY"),
        bigquery.SchemaField(
            "person_struct_field",
            "STRUCT",
            fields=(
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("age", "INT64"),
            ),
        ),
        bigquery.SchemaField("timestamp_field", "TIMESTAMP"),
        bigquery.SchemaField("date_field", "DATE"),
        bigquery.SchemaField("time_field", "TIME"),
        bigquery.SchemaField("datetime_field", "DATETIME"),
        bigquery.SchemaField("string_array_field", "STRING", mode="REPEATED"),
    ]
    bq_table = bigquery.table.Table(
        table_ref="{}.{}.complex_records".format(project_id, dataset.dataset_id),
        schema=schema,
    )

    created_table = bq_client.create_table(bq_table)

    table_ref = _TABLE_FORMAT.format(
        created_table.project, created_table.dataset_id, created_table.table_id
    )
    yield table_ref

    bq_client.delete_table(created_table)


@pytest.fixture
def ingest_partition_table_ref(project_id, dataset, bq_client):
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("shape", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("altitude", "INT64", mode="NULLABLE"),
    ]
    time_partitioning = bigquery.table.TimePartitioning(
        type_=bigquery.table.TimePartitioningType.DAY,
        field=None,  # use _PARTITIONTIME pseudo column
    )
    bq_table = bigquery.table.Table(
        table_ref="{}.{}.ufo_sightings".format(project_id, dataset.dataset_id),
        schema=schema,
    )
    bq_table.time_partitioning = time_partitioning

    created_table = bq_client.create_table(bq_table)

    table_ref = _TABLE_FORMAT.format(
        created_table.project, created_table.dataset_id, created_table.table_id
    )
    yield table_ref

    bq_client.delete_table(created_table)


@pytest.fixture
def col_partition_table_ref(project_id, dataset, bq_client):
    from google.cloud import bigquery

    schema = [
        bigquery.SchemaField("occurred", "DATE", mode="NULLABLE"),
        bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
    ]
    time_partitioning = bigquery.table.TimePartitioning(
        type_=bigquery.table.TimePartitioningType.DAY, field="occurred"
    )
    bq_table = bigquery.table.Table(
        table_ref="{}.{}.notable_events".format(project_id, dataset.dataset_id),
        schema=schema,
    )
    bq_table.time_partitioning = time_partitioning

    created_table = bq_client.create_table(bq_table)

    table_ref = _TABLE_FORMAT.format(
        created_table.project, created_table.dataset_id, created_table.table_id
    )
    yield table_ref

    bq_client.delete_table(created_table)


@pytest.fixture
def table_with_data_ref(dataset, table, bq_client):
    from google.cloud import bigquery

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.schema = table.schema

    filename = os.path.join(_ASSETS_DIR, "people_data.csv")

    with open(filename, "rb") as source_file:
        job = bq_client.load_table_from_file(source_file, table, job_config=job_config)

    job.result()  # wait for the load to complete

    table_ref = _TABLE_FORMAT.format(table.project, table.dataset_id, table.table_id)
    yield table_ref

    # truncate table data
    query = "DELETE FROM {}.{} WHERE 1 = 1".format(dataset.dataset_id, table.table_id)
    query_job = bq_client.query(query, location="US")
    query_job.result()
