from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    crm_ticket_id: str | None = None
    customer_id: int
    subject: str
    description: str
    status: str = "Open"
    priority: str = "Medium"


class TicketResponse(BaseModel):
    id: int
    crm_ticket_id: str | None
    customer_id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )