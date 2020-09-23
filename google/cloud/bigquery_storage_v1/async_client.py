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

"""Parent async client for calling the Cloud BigQuery Storage API.

This is the base from which all interactions with the API occur.
"""

from __future__ import absolute_import


from google.cloud.bigquery import storage_v1


_SCOPES = (
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform",
)


class BigQueryReadAsyncClient(storage_v1.BigQueryReadAsyncClient):
    """Async Client for interacting with BigQuery Storage API.

    The BigQuery storage API can be used to read data stored in BigQuery.
    """
