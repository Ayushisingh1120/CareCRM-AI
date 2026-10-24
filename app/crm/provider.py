from abc import ABC, abstractmethod
from typing import Any


class CRMProvider(ABC):

    @abstractmethod
    def get_customer(self, customer_id: int) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def get_ticket(self, ticket_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def get_customer_tickets(self, customer_id: int) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def create_ticket(
        self,
        customer_id: int,
        subject: str,
        description: str,
        priority: str = "Medium"
    ) -> dict[str, Any]:
        pass