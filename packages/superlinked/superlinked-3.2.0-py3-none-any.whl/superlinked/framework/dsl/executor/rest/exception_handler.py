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

from json import JSONDecodeError

from fastapi import Request, status
from fastapi.responses import JSONResponse

from superlinked.framework.common.exception import QueryException
from superlinked.framework.common.parser.exception import MissingIdException
from superlinked.framework.online.dag.exception import ValueNotProvidedException


class ExceptionHandler:
    @staticmethod
    def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"exception": str(exc.__class__.__name__), "detail": str(exc)},
        )

    @staticmethod
    def handle_bad_request(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"exception": str(exc.__class__.__name__), "detail": str(exc)},
        )

    handler_mapping = {
        ValueNotProvidedException: handle_bad_request,
        MissingIdException: handle_bad_request,
        JSONDecodeError: handle_bad_request,
        TypeError: generic_exception_handler,
        ValueError: generic_exception_handler,
        QueryException: generic_exception_handler,
    }
