class CareCRMAgent:

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

        self.available_tools = {
            "get_customer": get_customer,
            "get_ticket": get_ticket,
            "get_customer_tickets": get_customer_tickets,
            "create_ticket": create_ticket,
        }

        self.pending_action = None