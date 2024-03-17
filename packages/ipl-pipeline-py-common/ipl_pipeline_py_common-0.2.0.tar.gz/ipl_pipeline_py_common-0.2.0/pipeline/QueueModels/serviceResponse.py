from pydantic import BaseModel, Field
from typing import Optional


class ServiceResponse(BaseModel):
    response_node_id: str = Field("unknown")
    response_node_version: str = Field("unknown")
    request_error: bool = Field(False, description="Error in request")
    request_error_message: Optional[str] = Field(None, description="Error Message")
    response_data: Optional[dict] = Field(None, description="Response Data")
