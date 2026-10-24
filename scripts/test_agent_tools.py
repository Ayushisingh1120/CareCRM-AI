from app.agents.tools import (
    get_customer,
    get_ticket,
    get_customer_tickets,
    create_ticket,
    search_knowledge_base,
)


print("\n=== GET CUSTOMER ===")

customer = get_customer(1)

print(customer)


print("\n=== GET TICKET ===")

ticket = get_ticket("TKT-001")

print(ticket)


print("\n=== CUSTOMER TICKETS ===")

tickets = get_customer_tickets(1)

print(tickets)


print("\n=== CREATE TICKET ===")

created_ticket = create_ticket(
    customer_id=1,
    subject="Payment failed",
    description="Customer reports that payment is failing.",
    priority="High"
)

print(created_ticket)


print("\n=== SEARCH KNOWLEDGE BASE ===")

knowledge = search_knowledge_base(
    "Can a support agent promise a refund?"
)

print(knowledge)