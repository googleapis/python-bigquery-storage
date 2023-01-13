# Copyright 2022 Google LLC
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

import os
from google.cloud import bigquery_storage_v1

BUILD_SPECIFIC_GCLOUD_PROJECT = "BUILD_SPECIFIC_GCLOUD_PROJECT"


class Base:
    """Stores common parameters and options for API calls."""

    def __init__(self):
        self.client = bigquery_storage_v1.BigQueryWriteClient()
        self.project = (
            None
            if not os.getenv(BUILD_SPECIFIC_GCLOUD_PROJECT)
            else os.getenv(BUILD_SPECIFIC_GCLOUD_PROJECT)
        )


# global base class to store commonly accessed variables
global_base = Base()