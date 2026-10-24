from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    crm_id: str | None = None
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None


class CustomerResponse(BaseModel):
    id: int
    crm_id: str | None
    name: str
    email: str
    phone: str | None
    company: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)