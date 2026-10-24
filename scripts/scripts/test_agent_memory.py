from app.agents.agent import CareCRMAgent

agent = CareCRMAgent()

session_id = "memory_test_001"

print("\n========== QUESTION 1 ==========\n")

question1 = "What tickets does customer 1 have?"
print("USER:", question1)

answer1 = agent.run(question1, session_id)
print("\nAGENT:", answer1)

print("\n========== QUESTION 2 ==========\n")

question2 = "What is the priority of the first ticket?"
print("USER:", question2)

answer2 = agent.run(question2, session_id)
print("\nAGENT:", answer2)

print("\n========== CONVERSATION MEMORY ==========\n")

history = agent.memory.get_history(session_id)

for message in history:
    print(f"{message['role'].upper()}: {message['content']}")

print("\n========== MEMORY TEST COMPLETED ==========\n")