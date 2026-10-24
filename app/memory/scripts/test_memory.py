
from app.memory.conversation_memory import ConversationMemory

memory = ConversationMemory(max_messages=4)

session_id = "session_001"

memory.add_message(
    session_id,
    "user",
    "What tickets does customer 1 have?"
)

memory.add_message(
    session_id,
    "assistant",
    "Customer 1 has tickets TKT-001 and TKT-002."
)

memory.add_message(
    session_id,
    "user",
    "What is the priority of the first ticket?"
)

memory.add_message(
    session_id,
    "assistant",
    "TKT-001 has High priority."
)

print("=== CONVERSATION HISTORY ===")

for message in memory.get_history(session_id):
    print(f"{message['role']}: {message['content']}")

print("\n=== CLEAR HISTORY ===")

memory.clear(session_id)

print(memory.get_history(session_id))
