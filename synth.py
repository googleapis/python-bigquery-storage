# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import re

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
versions = ["v1"]

for version in versions:
    library = gapic.py_library(
        service="bigquery_storage",
        version=version,
        bazel_target=f"//google/cloud/bigquery/storage/{version}:bigquery-storage-{version}-py",
        include_protos=True,
    )

    s.move(
        library,
        excludes=[
            "docs/conf.py",
            "docs/index.rst",
            f"google/cloud/bigquery_storage_{version}/__init__.py",
            "README.rst",
            "nox*.py",
            "setup.py",
            "setup.cfg",
        ],
    )

    # We need to parameterize aspects of the client as it varies in different versions.
    #
    # In the future once the read and write client are colocated in the same version,
    # we'll need to loop through through multiple clients.  Perhaps by the time that
    # happens we'll be on a generator that needs less post-generation modifications.
    clientinfo = {
        "file": "big_query_storage_client.py",
        "type": "storage",
        "name": "BigQueryStorageClient",
        "badpkg": "google-cloud-bigquerystorage",
        "goodpkg": "google-cloud-bigquery-storage",
    }
    if version in {"v1"}:
        clientinfo = {
            "file": "big_query_read_client.py",
            "type": "read",
            "name": "BigQueryReadClient",
            "badpkg": "google-cloud-bigquerystorage",
            "goodpkg": "google-cloud-bigquery-storage",
        }

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
optional_deps = [".[fastavro,pandas,pyarrow]"]
system_test_deps = optional_deps

templated_files = common.py_library(
    microgenerator=True,
    samples=True,
    system_test_external_dependencies=system_test_deps,
    unit_test_dependencies=optional_deps,
    cov_level=95,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file


# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------

python.py_samples(skip_readmes=True)


# install bigquery as a (non-editable) package
s.replace(
    "noxfile.py",
    r'session\.install\("--pre", "grpcio"\)',
    '\g<0>\n\n    session.install("google-cloud-bigquery")',
)

# Make the async client available to import from storage_v1/
s.replace(
    "google/cloud/bigquery/storage_v1/__init__.py",
    r"from \.services\.big_query_read import BigQueryReadClient",
    "from .services.big_query_read import BigQueryReadAsyncClient\n\g<0>",
)
s.replace(
    "google/cloud/bigquery/storage_v1/__init__.py",
    r"""["']BigQueryReadClient["']""",
    '"BigQueryReadAsyncClient",\n    \g<0>',
)

# We want the default clients accessible through "google.cloud.bigquery.storage"
# to be the hand-written clients that wrap the generated clients, as this path is
# the users' main "entry point" into the library.
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    r"from google\.cloud\.bigquery\.storage_v1\.services.big_query_read.client import",
    "from google.cloud.bigquery_storage_v1 import"
)
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    r"from google\.cloud\.bigquery\.storage_v1\.services.big_query_read.async_client import",
    "from google.cloud.bigquery_storage_v1 import"
)

# Ditto for types and __version__, make them accessible through the consolidated
# entry point.
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    r"from google\.cloud\.bigquery\.storage_v1\.types\.arrow import ArrowRecordBatch",
    (
        "from google.cloud.bigquery_storage_v1 import types\n"
        "from google.cloud.bigquery_storage_v1 import __version__\n"
        "\g<0>"
    ),
)
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    r"""["']ArrowRecordBatch["']""",
    (
        '"__version__",\n'
        '    "types",\n'
        "    \g<0>"
    ),
)


# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
