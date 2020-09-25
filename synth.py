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

templated_files = common.py_library(
    microgenerator=True,
    samples=True,
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

# We want the default client accessible through "google.cloud.bigquery.storage"
# to be the hand-written client that wrap the generated client, as this path is
# the users' main "entry point" into the library.
# HOWEVER - we don't want to expose the async client just yet.
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    r"from google\.cloud\.bigquery\.storage_v1\.services.big_query_read.client import",
    "from google.cloud.bigquery_storage_v1 import"
)
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
    (
        r"from google\.cloud\.bigquery\.storage_v1\.services.big_query_read.async_client "
        r"import BigQueryReadAsyncClient\n"
    ),
    "",
)
s.replace(
    "google/cloud/bigquery/storage/__init__.py",
   r"""["']BigQueryReadAsyncClient["'],\n""",
    "",
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

# Fix redundant library installations in nox sessions (unit and system tests).
s.replace(
    "noxfile.py",
    (
        r'session\.install\("-e", "\."\)\n    '
        r'(?=session\.install\("-e", "\.\[fastavro)'
    ),
    "",
)
s.replace(
    "noxfile.py",
    (
        r'(?<=google-cloud-testutils", \)\n)'
        r'    session\.install\("-e", "\."\)\n'
    ),
    '    session.install("-e", ".[fastavro,pandas,pyarrow]")\n',
)


# Install the library as a non-editable package in test, otherwise the
# "google.cloud.bigquery.*"" namespace does not work correctly (import errors).
s.replace(
    "noxfile.py",
    r'''session\.install\("-e", "\.\[fastavro,pandas,pyarrow\]"\)''',
    'session.install(".[fastavro,pandas,pyarrow]")',
)

# TODO(busunkim): Use latest sphinx after microgenerator transition
s.replace("noxfile.py", """['"]sphinx['"]""", '"sphinx<3.0.0"')

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
