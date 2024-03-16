from pydantic import BaseModel


class ServiceRequest(BaseModel):
    request_node_id: str
    request_node_version: str
