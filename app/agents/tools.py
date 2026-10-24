from app.crm.mock import MockCRMProvider
from app.rag.service import RAGService


crm = MockCRMProvider()
rag = RAGService()


def get_customer(customer_id: int):
    """
    Get a customer by customer ID.
    """
    return crm.get_customer(customer_id)


def get_ticket(ticket_id: str):
    """
    Get a support ticket by ticket ID.
    """
    return crm.get_ticket(ticket_id)


def get_customer_tickets(customer_id: int):
    """
    Get all support tickets for a customer.
    """
    return crm.get_customer_tickets(customer_id)


def create_ticket(
    customer_id: int,
    subject: str,
    description: str,
    priority: str = "Medium"
):
    """
    Create a new CRM support ticket.
    """
    return crm.create_ticket(
        customer_id=customer_id,
        subject=subject,
        description=description,
        priority=priority
    )


def search_knowledge_base(question: str):
    """
    Search the CareCRM knowledge base for information relevant to a question.
    """
    return rag.retrieve(
        question=question,
        top_k=3
    )