# Copyright 2021 Google LLC
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

import unittest

from google.api_core import exceptions


class Test_should_retry_connection(unittest.TestCase):
    def _call_fut(self, exc):
        from google.cloud.bigquery_storage_v1.retry import _should_retry_connection

        return _should_retry_connection(exc)
    
    def test_w_eof_error(self):
        exc = EOFError()
        self.assertTrue(self._call_fut(exc))

    def test_w_aborted_error(self):
        exc = exceptions.Aborted("")
        self.assertTrue(self._call_fut(exc))

    def test_w_cancelled_error(self):
        exc = exceptions.Cancelled("")
        self.assertTrue(self._call_fut(exc))

    def test_w_deadline_exceeded_error(self):
        exc = exceptions.DeadlineExceeded("")
        self.assertTrue(self._call_fut(exc))

    def test_w_service_unavailable_error(self):
        exc = exceptions.ServiceUnavailable("")
        self.assertTrue(self._call_fut(exc))

    def test_w_other_error(self):
        exc = exceptions.InternalServerError("")
        self.assertFalse(self._call_fut(exc))
