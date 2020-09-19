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

import proto  # type: ignore


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1beta1",
    manifest={"TableReference", "TableModifiers",},
)


class TableReference(proto.Message):
    r"""Table reference that includes just the 3 strings needed to
    identify a table.

    Attributes:
        project_id (str):
            The assigned project ID of the project.
        dataset_id (str):
            The ID of the dataset in the above project.
        table_id (str):
            The ID of the table in the above dataset.
    """

    project_id = proto.Field(proto.STRING, number=1)

    dataset_id = proto.Field(proto.STRING, number=2)

    table_id = proto.Field(proto.STRING, number=3)


class TableModifiers(proto.Message):
    r"""All fields in this message optional.

    Attributes:
        snapshot_time (~.timestamp.Timestamp):
            The snapshot time of the table. If not set,
            interpreted as now.
    """

    snapshot_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
