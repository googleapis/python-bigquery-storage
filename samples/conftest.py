# Copyright 2021 Google LLC
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

import datetime
import os

import pytest

import logging


PYTHONWARNINGS="default"
# import http.client as http_client

# http_client.HTTPConnection.debuglevel = 3

logging.basicConfig()
logging.getLogger("google").setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def project_id():
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def dataset(project_id):
    from google.cloud import bigquery

    client = bigquery.Client()
    dataset_suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    dataset_name = "samples_tests_" + dataset_suffix

    dataset_id = "{}.{}".format(project_id, dataset_name)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "us-east7"
    created_dataset = client.create_dataset(dataset)
    yield created_dataset

    client.delete_dataset(created_dataset, delete_contents=True)
