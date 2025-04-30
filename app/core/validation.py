from starlette import status
from pydantic import BaseModel
from typing import Set, Any, List, override, Dict, Union

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi import Request


class ValidationErrorParser(BaseModel):
    type: str
    loc: Set[Union[str, int]]
    msg: str
    input: Any

    @override
    def model_dump(self):
        return {
            "type": self.type,
            "loc": list(self.loc),
            "msg": self.msg,
            "input": self.input,
        }


async def validation_error_handler(
    request: Request, error: RequestValidationError
) -> JSONResponse:
    print(error.errors())
    errors_list: List[ValidationErrorParser] = [
        ValidationErrorParser.model_validate(e) for e in error.errors()
    ]
    for e in errors_list:
        if "header" in e.loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Bad Request",
                        "details": [
                            {"reason": "Invalid header"},
                            {"details": [e.model_dump() for e in errors_list]},
                        ],
                    }
                },
            )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
                "details": [e.model_dump() for e in errors_list],
            }
        },
        headers={"X-Error-Count": f"{len(errors_list)}"},
    )
