# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery-storage/#history

## 1.1.0

09-14-2020 08:51 PDT


### Implementation Changes

- Change default retry policies timeouts (via synth). ([#53](https://github.com/googleapis/python-bigquery-storage/pull/53))


### New Features

- Add resource path helper methods. ([#40](https://github.com/googleapis/python-bigquery-storage/pull/40))


### Documentation

- Move code samples from the common [samples repo](https://github.com/GoogleCloudPlatform/python-docs-samples/) to this library. ([#50](https://github.com/googleapis/python-bigquery-storage/pull/50))
- Fix `read_rows()` docstring sample. ([#44](https://github.com/googleapis/python-bigquery-storage/pull/44))


### Internal / Testing Changes

- Update language of py2 admonition, add 3.8 unit tests. ([#45](https://github.com/googleapis/python-bigquery-storage/pull/45))
- Install google-cloud-testutils (via synth). ([#26](https://github.com/googleapis/python-bigquery-storage/pull/26))

## [1.0.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v0.8.0...v1.0.0) (2020-06-04)


### Bug Fixes

* handle consuming streams with no data ([#29](https://www.github.com/googleapis/python-bigquery-storage/issues/29)) ([56d1b1f](https://www.github.com/googleapis/python-bigquery-storage/commit/56d1b1fd75965669f5a4d10e5b00671c276eda88))
* update pyarrow references that are warning ([#31](https://www.github.com/googleapis/python-bigquery-storage/issues/31)) ([5302481](https://www.github.com/googleapis/python-bigquery-storage/commit/5302481d9f0ee07630ae62ed7268e510bcaa5d84))

## [0.8.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v0.7.0...v0.8.0) (2020-03-03)


### Features

* add manual layer for v1 endpoint ([#16](https://www.github.com/googleapis/python-bigquery-storage/issues/16)) ([a0fc0af](https://www.github.com/googleapis/python-bigquery-storage/commit/a0fc0af5b4447ce8b50c365d4d081b9443b8490e))
* update synth to generate v1beta2, v1 endpoints for bigquerystorage ([#10](https://www.github.com/googleapis/python-bigquery-storage/issues/10)) ([2ea5ac4](https://www.github.com/googleapis/python-bigquery-storage/commit/2ea5ac46035f38bdacf2976541a0af2dc0880660))


### Bug Fixes

* **bigquerystorage:** resume reader connection on `EOS` internal error ([#9994](https://www.github.com/googleapis/python-bigquery-storage/issues/9994)) ([acbd57f](https://www.github.com/googleapis/python-bigquery-storage/commit/acbd57f01cc8b338d9264aeedba117f7f1e48369))
* **bigquerystorage:** to_dataframe on an arrow stream uses 2x faster to_arrow + to_pandas, internally ([#9997](https://www.github.com/googleapis/python-bigquery-storage/issues/9997)) ([fdfb21e](https://www.github.com/googleapis/python-bigquery-storage/commit/fdfb21ec82278dbc5e6e9f7f16e4a22eb812b1be))
* pass snapshot_millis to the main function ([#8](https://www.github.com/googleapis/python-bigquery-storage/issues/8)) ([e522bf8](https://www.github.com/googleapis/python-bigquery-storage/commit/e522bf8327420d852352180ebfc0f816f269f22e))

## 0.7.0

07-31-2019 17:48 PDT


### New Features
- Support faster Arrow data format in `to_dataframe` and `to_arrow` when using BigQuery Storage API. ([#8551](https://github.com/googleapis/google-cloud-python/pull/8551))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pins of 'googleapis-common-protos. ([#8688](https://github.com/googleapis/google-cloud-python/pull/8688))

### Documentation
- Update quickstart sample with data format and sharding options. ([#8665](https://github.com/googleapis/google-cloud-python/pull/8665))
- Fix links to bigquery storage documentation. ([#8859](https://github.com/googleapis/google-cloud-python/pull/8859))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version. (via synth). ([#8672](https://github.com/googleapis/google-cloud-python/pull/8672))

## 0.6.0

07-11-2019 13:15 PDT

### New Features

- Add `to_arrow` with support for Arrow data format. ([#8644](https://github.com/googleapis/google-cloud-python/pull/8644))
- Add 'client_options' support (via synth). ([#8536](https://github.com/googleapis/google-cloud-python/pull/8536))
- Add sharding strategy, stream splitting, Arrow support (via synth). ([#8477](https://github.com/googleapis/google-cloud-python/pull/8477))

### Documentation

- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

### Internal / Testing Changes

- Allow kwargs to be passed to create_channel (via synth). ([#8441](https://github.com/googleapis/google-cloud-python/pull/8441))
- Add encoding declaration to protoc-generated files (via synth). ([#8345](https://github.com/googleapis/google-cloud-python/pull/8345))
- Refactor `reader.ReadRowsPage` to use `_StreamParser`. ([#8262](https://github.com/googleapis/google-cloud-python/pull/8262))
- Fix coverage in 'types.py' (via synth). ([#8148](https://github.com/googleapis/google-cloud-python/pull/8148))
- Add empty lines, remove coverage exclusions (via synth). ([#8051](https://github.com/googleapis/google-cloud-python/pull/8051))

## 0.5.0

05-20-2019 09:23 PDT

### Implementation Changes

- Increase default deadline on ReadRows. ([#8030](https://github.com/googleapis/google-cloud-python/pull/8030))
- Respect timeout on `client.read_rows`. Don't resume on `DEADLINE_EXCEEDED` errors. ([#8025](https://github.com/googleapis/google-cloud-python/pull/8025))

### Documentation

- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

## 0.4.0

04-16-2019 13:46 PDT

### Implementation Changes

- Remove gRPC size limit in the transport options ([#7664](https://github.com/googleapis/google-cloud-python/pull/7664))
- Add retry params for create_read_session (via synth). ([#7658](https://github.com/googleapis/google-cloud-python/pull/7658))

### New Features

- Add page iterator to ReadRowsStream ([#7680](https://github.com/googleapis/google-cloud-python/pull/7680))

### Internal / Testing Changes

- Remove system test for split rows ([#7673](https://github.com/googleapis/google-cloud-python/pull/7673))

## 0.3.0

04-02-2019 15:22 PDT

### Dependencies

- Add dependency for resource proto. ([#7585](https://github.com/googleapis/google-cloud-python/pull/7585))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### Documentation

- Fix links to BigQuery Storage API docs ([#7647](https://github.com/googleapis/google-cloud-python/pull/7647))
- Update proto / docstrings (via synth). ([#7461](https://github.com/googleapis/google-cloud-python/pull/7461))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Blacken new quickstart snippet. ([#7242](https://github.com/googleapis/google-cloud-python/pull/7242))
- Add quickstart demonstrating most BQ Storage API read features ([#7223](https://github.com/googleapis/google-cloud-python/pull/7223))
- Add bigquery_storage to docs ([#7222](https://github.com/googleapis/google-cloud-python/pull/7222))

### Internal / Testing Changes

- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Copy lintified proto files (via synth). ([#7475](https://github.com/googleapis/google-cloud-python/pull/7475))
- Add annotations to protocol buffers indicating request parameters (via synth). ([#7550](https://github.com/googleapis/google-cloud-python/pull/7550))

## 0.2.0

01-25-2019 13:54 PST

### New Features

- Add option to choose dtypes by column in to_dataframe. ([#7126](https://github.com/googleapis/google-cloud-python/pull/7126))

### Internal / Testing Changes

- Update copyright headers
- Protoc-generated serialization update. ([#7076](https://github.com/googleapis/google-cloud-python/pull/7076))
- BigQuery Storage: run 'blacken' during synth ([#7047](https://github.com/googleapis/google-cloud-python/pull/7047))

## 0.1.1

12-17-2018 18:03 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes in GAPIC generator. ([#6708](https://github.com/googleapis/google-cloud-python/pull/6708))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Correct release_status for bigquery_storage ([#6767](https://github.com/googleapis/google-cloud-python/pull/6767))

## 0.1.0

11-29-2018 13:45 PST

- Initial release of BigQuery Storage API client.
