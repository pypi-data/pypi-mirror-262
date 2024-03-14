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

from __future__ import annotations

from typing import Callable, Mapping, Sequence, TypeVar

from fastapi import FastAPI
from furl import furl
from pydantic.alias_generators import to_snake

from superlinked.framework.common.dag.context import ContextValue
from superlinked.framework.dsl.executor.exception import DuplicateEndpointException
from superlinked.framework.dsl.executor.executor import App, Executor
from superlinked.framework.dsl.executor.in_memory.in_memory_executor import (
    InMemoryApp,
    InMemoryExecutor,
)
from superlinked.framework.dsl.executor.rest.exception_handler import ExceptionHandler
from superlinked.framework.dsl.executor.rest.rest_configuration import (
    RestEndpointConfiguration,
    RestQuery,
)
from superlinked.framework.dsl.executor.rest.rest_processor import RestProcessor
from superlinked.framework.dsl.index.index import Index
from superlinked.framework.dsl.source.rest_source import RestSource

REST = TypeVar("REST", RestSource, RestQuery)


class RestExecutor(Executor[RestSource]):
    """
    The RestExecutor is a subclass of the Executor base class. It encapsulates all the parameters required for
    the REST application. It also instantiates an InMemoryExecutor for data storage purposes.

    Attributes:
        sources (list[RestSource]): List of Rest sources that has information about the schema.
        indices (list[Index]): List indices.
        queries (list[RestQuery]): List of executable queries.
        endpoint_configuration (RestEndpointConfiguration): Optional configuration for REST endpoints.
    """

    def __init__(
        self,
        sources: list[RestSource],
        indices: list[Index],
        queries: list[RestQuery],
        endpoint_configuration: RestEndpointConfiguration | None = None,
        context_data: Mapping[str, Mapping[str, ContextValue]] | None = None,
    ):
        """
        Initialize the RestExecutor.

        Attributes:
            sources (list[RestSource]): List of Rest sources that has information about the schema.
            indices (list[Index]): List indices.
            queries (list[RestQuery]): List of executable queries.
            endpoint_configuration (RestEndpointConfiguration): Optional configuration for REST endpoints.
        """
        online_sources = [source._online_source for source in sources]
        self._online_executor = InMemoryExecutor(online_sources, indices, context_data)
        super().__init__(sources, indices, self._online_executor.context)

        self._queries = queries

        self._endpoint_configuration = (
            endpoint_configuration or RestEndpointConfiguration()
        )

    def run(self) -> RestApp:
        """
        Run the RestExecutor. It returns an app that will create rest endpoints.

        Returns:
            RestApp: An instance of RestApp.
        """
        return RestApp(self)


class RestApp(App):
    """
    Rest implementation of the App class.

    Attributes:
        executor (RestExecutor): An instance of RestExecutor.
    """

    def __init__(self, executor: RestExecutor):
        """
        Initialize the RestApp from an RestExecutor.

        Args:
            executor (RestExecutor): An instance of RestExecutor.
        """
        self.__online_app = executor._online_executor.run()
        super().__init__(
            executor, self.__online_app._entity_store, self.__online_app._object_store
        )

        self.__rest_app = self.__create_app(
            self.__online_app,
            executor._sources,
            executor._queries,
            executor._endpoint_configuration,
        )

    def __create_app(
        self,
        app_: InMemoryApp,
        sources: Sequence[RestSource],
        queries: Sequence[RestQuery],
        endpoint_config: RestEndpointConfiguration,
    ) -> FastAPI:
        path_to_source: dict[str, RestSource] = {}
        path_to_query: dict[str, RestQuery] = {}
        processor = RestProcessor(app_, path_to_source, path_to_query)
        fast_api_app = FastAPI(exception_handlers=ExceptionHandler.handler_mapping)  # type: ignore

        path_to_source.update(
            self.__create_path_to_resource_mapping(
                sources,
                processor.ingest_func,
                endpoint_config.api_root_path,
                endpoint_config.ingest_path_prefix,
                fast_api_app,
            )
        )
        path_to_query.update(
            self.__create_path_to_resource_mapping(
                queries,
                processor.query_func,
                endpoint_config.api_root_path,
                endpoint_config.query_path_prefix,
                fast_api_app,
            )
        )

        return fast_api_app

    def __create_path_to_resource_mapping(
        self,
        resources: Sequence[REST],
        endpoint_function: Callable,
        api_root_path: str,
        path_prefix: str,
        fast_api_app: FastAPI,
    ) -> dict[str, REST]:
        path_to_resource = {}
        for resource in resources:
            path_string = str(
                furl(path=api_root_path)
                .path.add(path_prefix)
                .add(to_snake(resource.path))  # type: ignore[arg-type]
            )
            if path_string in path_to_resource:
                raise DuplicateEndpointException(
                    f"Endpoint duplication detected. The path: {path_string} has been previously added."
                )
            fast_api_app.add_api_route(
                path=path_string, endpoint=endpoint_function, methods=["POST"]
            )
            path_to_resource[path_string] = resource
        return path_to_resource

    @property
    def rest_app(self) -> FastAPI:
        """
        Property that returns the REST application instance.

        This property is used to get the instance of the REST application that has been created
        with the defined sources and queries. The application instance is of type FastAPI and
        it is used to handle the REST API requests.

        Returns:
            FastAPI: The instance of the REST application.
        """
        return self.__rest_app
