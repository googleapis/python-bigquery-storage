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

import logging
import queue

from append_rows_benchmark import constants


def main(response_queue: queue.Queue, num_workers: int):
    num_done = 0

    while True:
        print(f"{num_done} workers completed")
        if num_done >= num_workers:
            break

        try:
            print("waiting for queue")
            response_future = response_queue.get()
            if response_future is constants.DONE:
                num_done += 1
            else:
                print("waiting for result")
                response_future.result()
        except Exception as exc:
            logging.error(f"error with response: {exc}")
