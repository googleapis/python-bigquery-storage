
import google.cloud.bigquery_storage_v1
import google.cloud.bigquery_storage_v1.types

readclient = google.cloud.bigquery_storage_v1.BigQueryReadClient()
request = google.cloud.bigquery_storage_v1.types.CreateReadSessionRequest(
    parent="projects/swast-scratch",
    read_session=google.cloud.bigquery_storage_v1.types.ReadSession(
        table="projects/swast-scratch/datasets/my_dataset/tables/all_types",
        data_format=google.cloud.bigquery_storage_v1.types.DataFormat.ARROW,
))

session = readclient.create_read_session(request)
