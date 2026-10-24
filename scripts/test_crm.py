from app.crm.mock import MockCRMProvider


crm = MockCRMProvider()


print("\n=== CUSTOMER ===")
print(crm.get_customer(1))


print("\n=== TICKET ===")
print(crm.get_ticket("TKT-001"))


print("\n=== CUSTOMER TICKETS ===")
print(crm.get_customer_tickets(1))


print("\n=== CREATE TICKET ===")
new_ticket = crm.create_ticket(
    customer_id=1,
    subject="Website not loading",
    description="Customer reports that the website is not loading.",
    priority="High"
)

print(new_ticket)