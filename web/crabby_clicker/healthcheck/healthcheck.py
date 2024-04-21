#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

import socket

s = socket.socket()
s.connect(("localhost", 1337))
for i in range(101):
    s.send(b"GET /click HTTP/1.1\r\nHost: localhost\r\n\r\n")
    print(s.recv(256))
s.send(b"GET /flag HTTP/1.1\r\nHost: localhost\r\n\r\n")

resp = s.recv(8196).decode("utf-8")
print(resp)
if "UMASS{" in resp:
    exit(0)

exit(1)
