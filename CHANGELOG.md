# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery-storage/#history

## [2.8.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.7.0...v2.8.0) (2021-09-10)


### Features

* add `AppendRowsStream` helper to append rows with a `BigQueryWriteClient` ([#284](https://www.github.com/googleapis/python-bigquery-storage/issues/284)) ([2461f63](https://www.github.com/googleapis/python-bigquery-storage/commit/2461f63d37f707c2d634a95d87b8ffc3e4af3686))

## [2.7.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.3...v2.7.0) (2021-09-02)


### Features

* **v1beta2:** Align ReadRows timeout with other versions of the API ([#293](https://www.github.com/googleapis/python-bigquery-storage/issues/293)) ([43e36a1](https://www.github.com/googleapis/python-bigquery-storage/commit/43e36a13ece8d876763d88bad0252a1b2421c52a))


### Documentation

* **v1beta2:** Align session length with public documentation ([43e36a1](https://www.github.com/googleapis/python-bigquery-storage/commit/43e36a13ece8d876763d88bad0252a1b2421c52a))

### [2.6.3](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.2...v2.6.3) (2021-08-06)


### Bug Fixes

* resume read stream on `Unknown` transport-layer exception ([#263](https://www.github.com/googleapis/python-bigquery-storage/issues/263)) ([127caa0](https://www.github.com/googleapis/python-bigquery-storage/commit/127caa06144b9cec04b23914b561be6a264bcb36))

### [2.6.2](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.1...v2.6.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#249](https://www.github.com/googleapis/python-bigquery-storage/issues/249)) ([a7e8d91](https://www.github.com/googleapis/python-bigquery-storage/commit/a7e8d913fc3de67a3f38ecbd35af2f9d1a33aa8d))


### Documentation

* remove duplicate code samples ([#246](https://www.github.com/googleapis/python-bigquery-storage/issues/246)) ([303f273](https://www.github.com/googleapis/python-bigquery-storage/commit/303f2732ced38e491df92e965dd37bac24a61d2f))
* add Samples section to CONTRIBUTING.rst ([#241](https://www.github.com/googleapis/python-bigquery-storage/issues/241)) ([5d02358](https://www.github.com/googleapis/python-bigquery-storage/commit/5d02358fbd397cafcc1169d829859fe2dd568645))


### [2.6.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.6.0...v2.6.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#240](https://www.github.com/googleapis/python-bigquery-storage/issues/240)) ([8f848e1](https://www.github.com/googleapis/python-bigquery-storage/commit/8f848e18379085160492cdd2d12dc8de50a46c8e))


### Documentation

* pandas DataFrame samples are more standalone ([#224](https://www.github.com/googleapis/python-bigquery-storage/issues/224)) ([4026997](https://www.github.com/googleapis/python-bigquery-storage/commit/4026997d7a286b63ed2b969c0bd49de59635326d))

## [2.6.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.5.0...v2.6.0) (2021-07-09)


### Features

* `read_session` optional to `ReadRowsStream.rows()` ([#228](https://www.github.com/googleapis/python-bigquery-storage/issues/228)) ([4f56029](https://www.github.com/googleapis/python-bigquery-storage/commit/4f5602950a0c1959e332aa2964245b9caf4828c8))
* add always_use_jwt_access ([#223](https://www.github.com/googleapis/python-bigquery-storage/issues/223)) ([fd82417](https://www.github.com/googleapis/python-bigquery-storage/commit/fd824174fb044fbacc83c647f619fda556333e26))

## [2.5.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.4.0...v2.5.0) (2021-06-29)


### ⚠ BREAKING CHANGES

* remove default deadline for AppendRows API (#205)

### Features

* Add ZSTD compression as an option for Arrow ([#197](https://www.github.com/googleapis/python-bigquery-storage/issues/197)) ([f941446](https://www.github.com/googleapis/python-bigquery-storage/commit/f9414469fac37bf05db28230a1a6c1e3f7342e8d))
* new JSON type through BigQuery Write ([#178](https://www.github.com/googleapis/python-bigquery-storage/issues/178)) ([a6d6afa](https://www.github.com/googleapis/python-bigquery-storage/commit/a6d6afa8654907701aab2724f940be8f63edd0ea))


### Bug Fixes

* **deps:** add packaging requirement ([#200](https://www.github.com/googleapis/python-bigquery-storage/issues/200)) ([f2203fe](https://www.github.com/googleapis/python-bigquery-storage/commit/f2203fefe36dd043a258adb85e970fef14cf6ebc))
* remove default deadline for AppendRows API ([#205](https://www.github.com/googleapis/python-bigquery-storage/issues/205)) ([cd4e637](https://www.github.com/googleapis/python-bigquery-storage/commit/cd4e637c4c74f21be50c3b0ebdfeebb1dfb88cbb))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-bigquery-storage/issues/1127)) ([#212](https://www.github.com/googleapis/python-bigquery-storage/issues/212)) ([8bcc4cd](https://www.github.com/googleapis/python-bigquery-storage/commit/8bcc4cd298eb0f5da03ecf66670982ab41e35c88))


### Miscellaneous Chores

* release 2.5.0 ([#220](https://www.github.com/googleapis/python-bigquery-storage/issues/220)) ([946c8a9](https://www.github.com/googleapis/python-bigquery-storage/commit/946c8a91c2d74c6bf37b333a4d0483f4483dcbce))

## [2.4.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.3.0...v2.4.0) (2021-04-07)


### Features

* add a Arrow compression options (Only LZ4 for now) ([#166](https://www.github.com/googleapis/python-bigquery-storage/issues/166)) ([1c91a27](https://www.github.com/googleapis/python-bigquery-storage/commit/1c91a276289a0e319f93b136836f81ee943f661c))
* updates for v1beta2 storage API - Updated comments on BatchCommitWriteStreams - Added new support Bigquery types BIGNUMERIC and INTERVAL to TableSchema - Added read rows schema in ReadRowsResponse - Misc comment updates ([#172](https://www.github.com/googleapis/python-bigquery-storage/issues/172)) ([bef63fb](https://www.github.com/googleapis/python-bigquery-storage/commit/bef63fbb3b7e41e1c0d73f91a2c86d4d24e42151))


### Dependencies

* update minimum pandas to 0.21.1 ([#165](https://www.github.com/googleapis/python-bigquery-storage/issues/165)) ([8a97763](https://www.github.com/googleapis/python-bigquery-storage/commit/8a977633a81d080f03f6922752adbf4284199dd4))

## [2.3.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.2.1...v2.3.0) (2021-02-18)


### Features

* add `client_cert_source_for_mtls` argument to transports ([#135](https://www.github.com/googleapis/python-bigquery-storage/issues/135)) ([072850d](https://www.github.com/googleapis/python-bigquery-storage/commit/072850dd341909fdc22f330117a17e48da12fdd1))


### Documentation

* update python contributing guide ([#140](https://www.github.com/googleapis/python-bigquery-storage/issues/140)) ([1671056](https://www.github.com/googleapis/python-bigquery-storage/commit/1671056bfe181660440b1bf4415005e3eed01eb2))

### [2.2.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.2.0...v2.2.1) (2021-01-25)


### Documentation

* remove required session variable to fix publish ([#124](https://www.github.com/googleapis/python-bigquery-storage/issues/124)) ([19a105c](https://www.github.com/googleapis/python-bigquery-storage/commit/19a105cb9c868bb1a9e63966609a2488876f511b))

## [2.2.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.1.0...v2.2.0) (2021-01-22)


### Features

* add clients for v1beta2 endpoint ([#113](https://www.github.com/googleapis/python-bigquery-storage/issues/113)) ([e5f6198](https://www.github.com/googleapis/python-bigquery-storage/commit/e5f6198262cf9a593c62219cf5f6632c5a2a811e))
* add manual wrapper for v1beta2 read client ([#117](https://www.github.com/googleapis/python-bigquery-storage/issues/117)) ([798cd34](https://www.github.com/googleapis/python-bigquery-storage/commit/798cd341fbe0734f99b9c2ac3c50ae09886d1c90))


### Bug Fixes

* skip some system tests for mtls testing ([#106](https://www.github.com/googleapis/python-bigquery-storage/issues/106)) ([89ba292](https://www.github.com/googleapis/python-bigquery-storage/commit/89ba292281970cbdee5bb43b45a9dac69e29ff0a))


### Documentation

* add note about Arrow blocks to README ([#73](https://www.github.com/googleapis/python-bigquery-storage/issues/73)) ([d9691f1](https://www.github.com/googleapis/python-bigquery-storage/commit/d9691f1714bf34b3119d4e457293a723c2fb9120))
* request only a single stream in dataframe example ([#114](https://www.github.com/googleapis/python-bigquery-storage/issues/114)) ([3518624](https://www.github.com/googleapis/python-bigquery-storage/commit/35186247018b0c93a4af1fcde52fa739efa803c4))

## [2.1.0](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.0.1...v2.1.0) (2020-11-04)


### Features

* add public transport property and path formatting methods to client ([#80](https://www.github.com/googleapis/python-bigquery-storage/issues/80)) ([fbbb439](https://www.github.com/googleapis/python-bigquery-storage/commit/fbbb439b8c77fa9367a4b5bea725dd0b0f26b769))


### Documentation

* add intersphinx to proto-plus library ([#86](https://www.github.com/googleapis/python-bigquery-storage/issues/86)) ([4cd35d2](https://www.github.com/googleapis/python-bigquery-storage/commit/4cd35d21de4486f659b7efc4ff4dcb9b4eee6c9e))
* show inheritance in types reference ([#91](https://www.github.com/googleapis/python-bigquery-storage/issues/91)) ([e5fd4e6](https://www.github.com/googleapis/python-bigquery-storage/commit/e5fd4e62de2768a49d633dc3a81e03d64df9fe1f))

### [2.0.1](https://www.github.com/googleapis/python-bigquery-storage/compare/v2.0.0...v2.0.1) (2020-10-21)


### Bug Fixes

* don't fail with 429 when downloading wide tables ([#79](https://www.github.com/googleapis/python-bigquery-storage/issues/79)) ([45faf97](https://www.github.com/googleapis/python-bigquery-storage/commit/45faf9712b25bd63d962ca7e5afc8b8d3a0d8353))


### Documentation

* update to_dataframe sample to latest dependencies ([#72](https://www.github.com/googleapis/python-bigquery-storage/issues/72)) ([a7fe762](https://www.github.com/googleapis/python-bigquery-storage/commit/a7fe7626312a5b9fe1e7bd0e0fe5601ae97605c7))

## 2.0.0

09-24-2020 08:21 PDT

### Implementation Changes

- Transition the library to microgenerator. ([#62](https://github.com/googleapis/python-bigquery-storage/pull/62))
  This is a **breaking change** that introduces several **method signature changes** and **drops support
  for Python 2.7 and 3.5**. See [migration guide](https://googleapis.dev/python/bigquerystorage/latest/UPGRADING.html)
  for more info.

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

- Update CODEOWNERS for samples and library code. ([#56](https://github.com/googleapis/python-bigquery-storage/pull/56))
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
