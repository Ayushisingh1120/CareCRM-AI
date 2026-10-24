
from app.agents.agent import CareCRMAgent

agent = CareCRMAgent()

question = "Can a support agent promise a refund?"

print("\n========== USER ==========\n")
print(question)

answer = agent.run(question)

print("\n========== FINAL ANSWER ==========\n")
print(answer)
