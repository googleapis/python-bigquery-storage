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


from google.cloud.bigquery.storage_v1beta1.types import arrow
from google.cloud.bigquery.storage_v1beta1.types import avro
from google.cloud.bigquery.storage_v1beta1.types import (
    read_options as gcbs_read_options,
)
from google.cloud.bigquery.storage_v1beta1.types import (
    table_reference as gcbs_table_reference,
)
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1beta1",
    manifest={
        "DataFormat",
        "ShardingStrategy",
        "Stream",
        "StreamPosition",
        "ReadSession",
        "CreateReadSessionRequest",
        "ReadRowsRequest",
        "StreamStatus",
        "Progress",
        "ThrottleStatus",
        "ReadRowsResponse",
        "BatchCreateReadSessionStreamsRequest",
        "BatchCreateReadSessionStreamsResponse",
        "FinalizeStreamRequest",
        "SplitReadStreamRequest",
        "SplitReadStreamResponse",
    },
)


class DataFormat(proto.Enum):
    r"""Data format for input or output data."""
    DATA_FORMAT_UNSPECIFIED = 0
    AVRO = 1
    ARROW = 3


class ShardingStrategy(proto.Enum):
    r"""Strategy for distributing data among multiple streams in a
    read session.
    """
    SHARDING_STRATEGY_UNSPECIFIED = 0
    LIQUID = 1
    BALANCED = 2


class Stream(proto.Message):
    r"""Information about a single data stream within a read session.

    Attributes:
        name (str):
            Name of the stream, in the form
            ``projects/{project_id}/locations/{location}/streams/{stream_id}``.
    """

    name = proto.Field(proto.STRING, number=1)


class StreamPosition(proto.Message):
    r"""Expresses a point within a given stream using an offset
    position.

    Attributes:
        stream (~.storage.Stream):
            Identifier for a given Stream.
        offset (int):
            Position in the stream.
    """

    stream = proto.Field(proto.MESSAGE, number=1, message=Stream,)

    offset = proto.Field(proto.INT64, number=2)


class ReadSession(proto.Message):
    r"""Information returned from a ``CreateReadSession`` request.

    Attributes:
        name (str):
            Unique identifier for the session, in the form
            ``projects/{project_id}/locations/{location}/sessions/{session_id}``.
        expire_time (~.timestamp.Timestamp):
            Time at which the session becomes invalid.
            After this time, subsequent requests to read
            this Session will return errors.
        avro_schema (~.avro.AvroSchema):
            Avro schema.
        arrow_schema (~.arrow.ArrowSchema):
            Arrow schema.
        streams (Sequence[~.storage.Stream]):
            Streams associated with this session.
        table_reference (~.gcbs_table_reference.TableReference):
            Table that this ReadSession is reading from.
        table_modifiers (~.gcbs_table_reference.TableModifiers):
            Any modifiers which are applied when reading
            from the specified table.
        sharding_strategy (~.storage.ShardingStrategy):
            The strategy to use for distributing data
            among the streams.
    """

    name = proto.Field(proto.STRING, number=1)

    expire_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    avro_schema = proto.Field(
        proto.MESSAGE, number=5, oneof="schema", message=avro.AvroSchema,
    )

    arrow_schema = proto.Field(
        proto.MESSAGE, number=6, oneof="schema", message=arrow.ArrowSchema,
    )

    streams = proto.RepeatedField(proto.MESSAGE, number=4, message=Stream,)

    table_reference = proto.Field(
        proto.MESSAGE, number=7, message=gcbs_table_reference.TableReference,
    )

    table_modifiers = proto.Field(
        proto.MESSAGE, number=8, message=gcbs_table_reference.TableModifiers,
    )

    sharding_strategy = proto.Field(proto.ENUM, number=9, enum="ShardingStrategy",)


class CreateReadSessionRequest(proto.Message):
    r"""Creates a new read session, which may include additional
    options such as requested parallelism, projection filters and
    constraints.

    Attributes:
        table_reference (~.gcbs_table_reference.TableReference):
            Required. Reference to the table to read.
        parent (str):
            Required. String of the form ``projects/{project_id}``
            indicating the project this ReadSession is associated with.
            This is the project that will be billed for usage.
        table_modifiers (~.gcbs_table_reference.TableModifiers):
            Any modifiers to the Table (e.g. snapshot
            timestamp).
        requested_streams (int):
            Initial number of streams. If unset or 0, we
            will provide a value of streams so as to produce
            reasonable throughput. Must be non-negative. The
            number of streams may be lower than the
            requested number, depending on the amount
            parallelism that is reasonable for the table and
            the maximum amount of parallelism allowed by the
            system.
            Streams must be read starting from offset 0.
        read_options (~.gcbs_read_options.TableReadOptions):
            Read options for this session (e.g. column
            selection, filters).
        format (~.storage.DataFormat):
            Data output format. Currently default to
            Avro.
        sharding_strategy (~.storage.ShardingStrategy):
            The strategy to use for distributing data
            among multiple streams. Currently defaults to
            liquid sharding.
    """

    table_reference = proto.Field(
        proto.MESSAGE, number=1, message=gcbs_table_reference.TableReference,
    )

    parent = proto.Field(proto.STRING, number=6)

    table_modifiers = proto.Field(
        proto.MESSAGE, number=2, message=gcbs_table_reference.TableModifiers,
    )

    requested_streams = proto.Field(proto.INT32, number=3)

    read_options = proto.Field(
        proto.MESSAGE, number=4, message=gcbs_read_options.TableReadOptions,
    )

    format = proto.Field(proto.ENUM, number=5, enum="DataFormat",)

    sharding_strategy = proto.Field(proto.ENUM, number=7, enum="ShardingStrategy",)


class ReadRowsRequest(proto.Message):
    r"""Requesting row data via ``ReadRows`` must provide Stream position
    information.

    Attributes:
        read_position (~.storage.StreamPosition):
            Required. Identifier of the position in the
            stream to start reading from. The offset
            requested must be less than the last row read
            from ReadRows. Requesting a larger offset is
            undefined.
    """

    read_position = proto.Field(proto.MESSAGE, number=1, message=StreamPosition,)


class StreamStatus(proto.Message):
    r"""Progress information for a given Stream.

    Attributes:
        estimated_row_count (int):
            Number of estimated rows in the current
            stream. May change over time as different
            readers in the stream progress at rates which
            are relatively fast or slow.
        fraction_consumed (float):
            A value in the range [0.0, 1.0] that represents the fraction
            of rows assigned to this stream that have been processed by
            the server. In the presence of read filters, the server may
            process more rows than it returns, so this value reflects
            progress through the pre-filtering rows.

            This value is only populated for sessions created through
            the BALANCED sharding strategy.
        progress (~.storage.Progress):
            Represents the progress of the current
            stream.
        is_splittable (bool):
            Whether this stream can be split. For
            sessions that use the LIQUID sharding strategy,
            this value is always false. For BALANCED
            sessions, this value is false when enough data
            have been read such that no more splits are
            possible at that point or beyond. For small
            tables or streams that are the result of a chain
            of splits, this value may never be true.
    """

    estimated_row_count = proto.Field(proto.INT64, number=1)

    fraction_consumed = proto.Field(proto.FLOAT, number=2)

    progress = proto.Field(proto.MESSAGE, number=4, message="Progress",)

    is_splittable = proto.Field(proto.BOOL, number=3)


class Progress(proto.Message):
    r"""

    Attributes:
        at_response_start (float):
            The fraction of rows assigned to the stream that have been
            processed by the server so far, not including the rows in
            the current response message.

            This value, along with ``at_response_end``, can be used to
            interpolate the progress made as the rows in the message are
            being processed using the following formula:
            ``at_response_start + (at_response_end - at_response_start) * rows_processed_from_response / rows_in_response``.

            Note that if a filter is provided, the ``at_response_end``
            value of the previous response may not necessarily be equal
            to the ``at_response_start`` value of the current response.
        at_response_end (float):
            Similar to ``at_response_start``, except that this value
            includes the rows in the current response.
    """

    at_response_start = proto.Field(proto.FLOAT, number=1)

    at_response_end = proto.Field(proto.FLOAT, number=2)


class ThrottleStatus(proto.Message):
    r"""Information on if the current connection is being throttled.

    Attributes:
        throttle_percent (int):
            How much this connection is being throttled.
            0 is no throttling, 100 is completely throttled.
    """

    throttle_percent = proto.Field(proto.INT32, number=1)


class ReadRowsResponse(proto.Message):
    r"""Response from calling ``ReadRows`` may include row data, progress
    and throttling information.

    Attributes:
        avro_rows (~.avro.AvroRows):
            Serialized row data in AVRO format.
        arrow_record_batch (~.arrow.ArrowRecordBatch):
            Serialized row data in Arrow RecordBatch
            format.
        row_count (int):
            Number of serialized rows in the rows block. This value is
            recorded here, in addition to the row_count values in the
            output-specific messages in ``rows``, so that code which
            needs to record progress through the stream can do so in an
            output format-independent way.
        status (~.storage.StreamStatus):
            Estimated stream statistics.
        throttle_status (~.storage.ThrottleStatus):
            Throttling status. If unset, the latest
            response still describes the current throttling
            status.
    """

    avro_rows = proto.Field(
        proto.MESSAGE, number=3, oneof="rows", message=avro.AvroRows,
    )

    arrow_record_batch = proto.Field(
        proto.MESSAGE, number=4, oneof="rows", message=arrow.ArrowRecordBatch,
    )

    row_count = proto.Field(proto.INT64, number=6)

    status = proto.Field(proto.MESSAGE, number=2, message=StreamStatus,)

    throttle_status = proto.Field(proto.MESSAGE, number=5, message=ThrottleStatus,)


class BatchCreateReadSessionStreamsRequest(proto.Message):
    r"""Information needed to request additional streams for an
    established read session.

    Attributes:
        session (~.storage.ReadSession):
            Required. Must be a non-expired session
            obtained from a call to CreateReadSession. Only
            the name field needs to be set.
        requested_streams (int):
            Required. Number of new streams requested.
            Must be positive. Number of added streams may be
            less than this, see CreateReadSessionRequest for
            more information.
    """

    session = proto.Field(proto.MESSAGE, number=1, message=ReadSession,)

    requested_streams = proto.Field(proto.INT32, number=2)


class BatchCreateReadSessionStreamsResponse(proto.Message):
    r"""The response from ``BatchCreateReadSessionStreams`` returns the
    stream identifiers for the newly created streams.

    Attributes:
        streams (Sequence[~.storage.Stream]):
            Newly added streams.
    """

    streams = proto.RepeatedField(proto.MESSAGE, number=1, message=Stream,)


class FinalizeStreamRequest(proto.Message):
    r"""Request information for invoking ``FinalizeStream``.

    Attributes:
        stream (~.storage.Stream):
            Required. Stream to finalize.
    """

    stream = proto.Field(proto.MESSAGE, number=2, message=Stream,)


class SplitReadStreamRequest(proto.Message):
    r"""Request information for ``SplitReadStream``.

    Attributes:
        original_stream (~.storage.Stream):
            Required. Stream to split.
        fraction (float):
            A value in the range (0.0, 1.0) that
            specifies the fractional point at which the
            original stream should be split. The actual
            split point is evaluated on pre-filtered rows,
            so if a filter is provided, then there is no
            guarantee that the division of the rows between
            the new child streams will be proportional to
            this fractional value. Additionally, because the
            server-side unit for assigning data is
            collections of rows, this fraction will always
            map to to a data storage boundary on the server
            side.
    """

    original_stream = proto.Field(proto.MESSAGE, number=1, message=Stream,)

    fraction = proto.Field(proto.FLOAT, number=2)


class SplitReadStreamResponse(proto.Message):
    r"""Response from ``SplitReadStream``.

    Attributes:
        primary_stream (~.storage.Stream):
            Primary stream, which contains the beginning portion of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
        remainder_stream (~.storage.Stream):
            Remainder stream, which contains the tail of
            \|original_stream|. An empty value indicates that the
            original stream can no longer be split.
    """

    primary_stream = proto.Field(proto.MESSAGE, number=1, message=Stream,)

    remainder_stream = proto.Field(proto.MESSAGE, number=2, message=Stream,)


__all__ = tuple(sorted(__protobuf__.manifest))
