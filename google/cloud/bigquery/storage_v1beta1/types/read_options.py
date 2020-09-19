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


__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1beta1", manifest={"TableReadOptions",},
)


class TableReadOptions(proto.Message):
    r"""Options dictating how we read a table.

    Attributes:
        selected_fields (Sequence[str]):
            Optional. Names of the fields in the table that should be
            read. If empty, all fields will be read. If the specified
            field is a nested field, all the sub-fields in the field
            will be selected. The output field order is unrelated to the
            order of fields in selected_fields.
        row_restriction (str):
            Optional. SQL text filtering statement, similar to a WHERE
            clause in a query. Aggregates are not supported.

            Examples: "int_field > 5" "date_field = CAST('2014-9-27' as
            DATE)" "nullable_field is not NULL" "st_equals(geo_field,
            st_geofromtext("POINT(2, 2)"))" "numeric_field BETWEEN 1.0
            AND 5.0".
    """

    selected_fields = proto.RepeatedField(proto.STRING, number=1)

    row_restriction = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
