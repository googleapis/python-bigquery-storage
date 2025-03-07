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

import time

from google.api_core import exceptions
from google.api_core import retry


_CONNECTION_RETRIABLE_REASONS = (
    EOFError,
    exceptions.Aborted,
    exceptions.Cancelled,
    exceptions.DeadlineExceeded,
    exceptions.ServiceUnavailable,
)

_DEFAULT_CONNECTION_RETRY_DEADLINE = 10   # 10 seconds
_DEFAULT_CONNECTION_RETRY_BACKOFF = 0.05  # 50 miliseconds


def _should_retry_connection(exc):
    return isinstance(exc, _CONNECTION_RETRIABLE_REASONS)


_DEFAULT_CONNECTION_RETRY = retry.Retry(
    predicate=_should_retry_connection,
    initial=_DEFAULT_CONNECTION_RETRY_BACKOFF, 
    multiplier=2,
    timeout=_DEFAULT_CONNECTION_RETRY_DEADLINE,
)

def _stateless_retry(func, func_args={}, num_retry=1, backoff=0.05):
    for i in range(num_retry + 1):
        try:
            return func(**func_args)
        except Exception:
            time.sleep(backoff)
            continue
    raise exceptions.Unknown("Max retry for connection is reached.")
