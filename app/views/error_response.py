from typing import Dict, Any, Optional, List, Union
from http import HTTPStatus
from pydantic import BaseModel, model_validator


class ErrorModel(BaseModel):
    """Define base error model for the response."""

    code: int
    message: str
    details: Optional[List[Dict[str, Any]]] = (
        None  # Rendi esplicito che il valore di default è None
    )

    @model_validator(mode="before")
    def _set_status(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Set the status field value based on the code attribute value."""
        values["status"] = HTTPStatus(values["code"]).name
        return values

    class ConfigDict:
        """Config sub-class needed to extend/override the generated JSON schema."""

        @staticmethod
        def json_schema_extra(schema: Dict[str, Any]) -> None:
            schema["description"] = "Error model."
            schema["properties"].update(
                {"status": {"title": "Status", "type": "string"}}
            )
            schema["required"].append("status")


class ErrorResponse(BaseModel):
    """Define error response model."""

    error: ErrorModel

    def __init__(self, **kwargs: Union[int, str, List[Dict[str, Any]]]):
        """Initialize ErrorResponse class object instance."""
        # Assegna 'details' solo se è presente nei kwargs
        details = kwargs.get("details", None)
        super().__init__(
            error=ErrorModel(
                code=kwargs.get("code"), message=kwargs.get("message"), details=details
            )
        )

    class ConfigDict:
        """Config sub-class needed to extend/override the generated JSON schema."""

        @staticmethod
        def json_schema_extra(schema: Dict[str, Any]) -> None:
            schema["description"] = "Error response model."
