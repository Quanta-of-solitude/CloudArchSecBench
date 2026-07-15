from pydantic import BaseModel
from typing import List, Optional


class Resource(BaseModel):
    id: Optional[str] = None
    name: str
    type: str

    public: Optional[bool] = False
    encrypted: Optional[bool] = None
    backup_enabled: Optional[bool] = None
    availability_zones: Optional[int] = None

    has_logging: Optional[bool] = None
    has_monitoring: Optional[bool] = None
    uses_iam_role: Optional[bool] = None
    has_waf: Optional[bool] = None
    subnet: Optional[str] = None
    connections: Optional[List[str]] = []


class Architecture(BaseModel):
    provider: str
    resources: List[Resource]