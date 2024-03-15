# Copyright The OpenTelemetry Authors
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

OTEL_SERVICE_NAME = "OTEL_SERVICE_NAME"
"""
.. envvar:: OTEL_SERVICE_NAME
"""

OTEL_EXPORTER_OTLP_TRACES_ENDPOINT = "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"
"""
.. envvar:: OTEL_EXPORTER_OTLP_TRACES_ENDPOINT

The :envvar:`OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` target to which the span exporter is going to send spans.
The endpoint MUST be a valid URL host, and MAY contain a scheme (http or https), port and path.
A scheme of https indicates a secure connection and takes precedence over this configuration setting.
"""

OTEL_EXPORTER_OTLP_TRACES_HEADERS = "OTEL_EXPORTER_OTLP_TRACES_HEADERS"
"""
.. envvar:: OTEL_EXPORTER_OTLP_TRACES_HEADERS

The :envvar:`OTEL_EXPORTER_OTLP_TRACES_HEADERS` contains the key-value pairs to be used as headers
associated with gRPC or HTTP requests.
"""

OTEL_EXPORTER_OTLP_LOGS_ENDPOINT = "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"
"""
.. envvar:: OTEL_EXPORTER_OTLP_LOGS_ENDPOINT

The :envvar:`OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` target to which the log exporter is going to send logs.
The endpoint MUST be a valid URL host, and MAY contain a scheme (http or https), port and path.
A scheme of https indicates a secure connection and takes precedence over this configuration setting.
"""

OTEL_EXPORTER_OTLP_LOGS_HEADERS = "OTEL_EXPORTER_OTLP_LOGS_HEADERS"
"""
.. envvar:: OTEL_EXPORTER_OTLP_LOGS_HEADERS

The :envvar:`OTEL_EXPORTER_OTLP_LOGS_HEADERS` contains the key-value pairs to be used as headers for logs
associated with gRPC or HTTP requests.
"""
