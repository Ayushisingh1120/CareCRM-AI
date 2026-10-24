from typing import Any

from app.crm.provider import CRMProvider


class MockCRMProvider(CRMProvider):

    def __init__(self):
        self.customers = {
            1: {
                "id": 1,
                "name": "Rahul Sharma",
                "email": "rahul@example.com",
                "company": "Example Corp"
            },
            2: {
                "id": 2,
                "name": "Priya Singh",
                "email": "priya@example.com",
                "company": "Demo Technologies"
            }
        }

        self.tickets = {
            "TKT-001": {
                "id": "TKT-001",
                "customer_id": 1,
                "subject": "Unable to access account",
                "description": "Customer cannot log into the account.",
                "status": "Open",
                "priority": "High"
            },
            "TKT-002": {
                "id": "TKT-002",
                "customer_id": 1,
                "subject": "Refund request",
                "description": "Customer requested a refund.",
                "status": "Pending",
                "priority": "Medium"
            },
            "TKT-003": {
                "id": "TKT-003",
                "customer_id": 2,
                "subject": "Password reset",
                "description": "Customer needs help resetting password.",
                "status": "Resolved",
                "priority": "Low"
            }
        }

    def get_customer(
        self,
        customer_id: int
    ) -> dict[str, Any] | None:

        return self.customers.get(customer_id)

    def get_ticket(
        self,
        ticket_id: str
    ) -> dict[str, Any] | None:

        return self.tickets.get(ticket_id)

    def get_customer_tickets(
        self,
        customer_id: int
    ) -> list[dict[str, Any]]:

        return [
            ticket
            for ticket in self.tickets.values()
            if ticket["customer_id"] == customer_id
        ]

    def create_ticket(
        self,
        customer_id: int,
        subject: str,
        description: str,
        priority: str = "Medium"
    ) -> dict[str, Any]:

        ticket_number = len(self.tickets) + 1
        ticket_id = f"TKT-{ticket_number:03d}"

        ticket = {
            "id": ticket_id,
            "customer_id": customer_id,
            "subject": subject,
            "description": description,
            "status": "Open",
            "priority": priority
        }

        self.tickets[ticket_id] = ticket

        return ticket