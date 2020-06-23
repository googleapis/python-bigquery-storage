# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.cloud.bigquery_storage_v1beta1.proto import (
    storage_pb2 as google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class BigQueryStorageStub(object):
    """BigQuery storage API.

  The BigQuery storage API can be used to read data stored in BigQuery.
  """

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.CreateReadSession = channel.unary_unary(
            "/google.cloud.bigquery.storage.v1beta1.BigQueryStorage/CreateReadSession",
            request_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.CreateReadSessionRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadSession.FromString,
        )
        self.ReadRows = channel.unary_stream(
            "/google.cloud.bigquery.storage.v1beta1.BigQueryStorage/ReadRows",
            request_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadRowsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadRowsResponse.FromString,
        )
        self.BatchCreateReadSessionStreams = channel.unary_unary(
            "/google.cloud.bigquery.storage.v1beta1.BigQueryStorage/BatchCreateReadSessionStreams",
            request_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.BatchCreateReadSessionStreamsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.BatchCreateReadSessionStreamsResponse.FromString,
        )
        self.FinalizeStream = channel.unary_unary(
            "/google.cloud.bigquery.storage.v1beta1.BigQueryStorage/FinalizeStream",
            request_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.FinalizeStreamRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.SplitReadStream = channel.unary_unary(
            "/google.cloud.bigquery.storage.v1beta1.BigQueryStorage/SplitReadStream",
            request_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.SplitReadStreamRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.SplitReadStreamResponse.FromString,
        )


class BigQueryStorageServicer(object):
    """BigQuery storage API.

  The BigQuery storage API can be used to read data stored in BigQuery.
  """

    def CreateReadSession(self, request, context):
        """Creates a new read session. A read session divides the contents of a
    BigQuery table into one or more streams, which can then be used to read
    data from the table. The read session also specifies properties of the
    data to be read, such as a list of columns or a push-down filter describing
    the rows to be returned.

    A particular row can be read by at most one stream. When the caller has
    reached the end of each stream in the session, then all the data in the
    table has been read.

    Read sessions automatically expire 24 hours after they are created and do
    not require manual clean-up by the caller.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ReadRows(self, request, context):
        """Reads rows from the table in the format prescribed by the read session.
    Each response contains one or more table rows, up to a maximum of 10 MiB
    per response; read requests which attempt to read individual rows larger
    than this will fail.

    Each request also returns a set of stream statistics reflecting the
    estimated total number of rows in the read stream. This number is computed
    based on the total table size and the number of active streams in the read
    session, and may change as other streams continue to read data.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def BatchCreateReadSessionStreams(self, request, context):
        """Creates additional streams for a ReadSession. This API can be used to
    dynamically adjust the parallelism of a batch processing task upwards by
    adding additional workers.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def FinalizeStream(self, request, context):
        """Triggers the graceful termination of a single stream in a ReadSession. This
    API can be used to dynamically adjust the parallelism of a batch processing
    task downwards without losing data.

    This API does not delete the stream -- it remains visible in the
    ReadSession, and any data processed by the stream is not released to other
    streams. However, no additional data will be assigned to the stream once
    this call completes. Callers must continue reading data on the stream until
    the end of the stream is reached so that data which has already been
    assigned to the stream will be processed.

    This method will return an error if there are no other live streams
    in the Session, or if SplitReadStream() has been called on the given
    Stream.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SplitReadStream(self, request, context):
        """Splits a given read stream into two Streams. These streams are referred to
    as the primary and the residual of the split. The original stream can still
    be read from in the same manner as before. Both of the returned streams can
    also be read from, and the total rows return by both child streams will be
    the same as the rows read from the original stream.

    Moreover, the two child streams will be allocated back to back in the
    original Stream. Concretely, it is guaranteed that for streams Original,
    Primary, and Residual, that Original[0-j] = Primary[0-j] and
    Original[j-n] = Residual[0-m] once the streams have been read to
    completion.

    This method is guaranteed to be idempotent.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_BigQueryStorageServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateReadSession": grpc.unary_unary_rpc_method_handler(
            servicer.CreateReadSession,
            request_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.CreateReadSessionRequest.FromString,
            response_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadSession.SerializeToString,
        ),
        "ReadRows": grpc.unary_stream_rpc_method_handler(
            servicer.ReadRows,
            request_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadRowsRequest.FromString,
            response_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.ReadRowsResponse.SerializeToString,
        ),
        "BatchCreateReadSessionStreams": grpc.unary_unary_rpc_method_handler(
            servicer.BatchCreateReadSessionStreams,
            request_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.BatchCreateReadSessionStreamsRequest.FromString,
            response_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.BatchCreateReadSessionStreamsResponse.SerializeToString,
        ),
        "FinalizeStream": grpc.unary_unary_rpc_method_handler(
            servicer.FinalizeStream,
            request_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.FinalizeStreamRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "SplitReadStream": grpc.unary_unary_rpc_method_handler(
            servicer.SplitReadStream,
            request_deserializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.SplitReadStreamRequest.FromString,
            response_serializer=google_dot_cloud_dot_bigquery__storage__v1beta1_dot_proto_dot_storage__pb2.SplitReadStreamResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.bigquery.storage.v1beta1.BigQueryStorage", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
