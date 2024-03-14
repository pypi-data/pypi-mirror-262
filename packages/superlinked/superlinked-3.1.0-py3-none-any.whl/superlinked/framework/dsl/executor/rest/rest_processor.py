# Copyright 2024 Superlinked, Inc.
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

from dataclasses import dataclass
from typing import Any

from fastapi import Request, Response, status
from pydantic import Field

from superlinked.framework.common.util.immutable_model import ImmutableBaseModel
from superlinked.framework.dsl.executor.in_memory.in_memory_executor import InMemoryApp
from superlinked.framework.dsl.executor.rest.rest_configuration import RestQuery
from superlinked.framework.dsl.source.rest_source import RestSource


class QueryResponse(ImmutableBaseModel):
    schema_: str = Field(..., alias="schema")
    results: list[dict[str, Any]]


@dataclass
class RestProcessor:
    app: InMemoryApp
    source_path_map: dict[str, RestSource]
    query_path_map: dict[str, RestQuery]

    async def ingest_func(self, request: Request) -> Response:
        payload = await request.json()
        source = self.source_path_map[request.url.path]
        source._online_source.put([payload])
        return Response(status_code=status.HTTP_202_ACCEPTED)

    async def query_func(self, request: Request) -> QueryResponse:
        payload = await request.json()
        query = self.query_path_map[request.url.path].query_obj
        result = self.app.query(query, **payload)
        return QueryResponse(
            schema=result.schema._schema_name,
            results=[
                {
                    "entity": {
                        "id": entry.entity.id_.object_id,
                        "origin": (
                            {
                                "id": entry.entity.origin_id.object_id,
                                "schema": entry.entity.origin_id.schema_id,
                            }
                            if entry.entity.origin_id
                            else {}
                        ),
                    },
                    "obj": entry.stored_object,
                }
                for entry in result.entries
            ],
        )
