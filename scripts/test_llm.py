from app.llm.client import LLMClient


llm = LLMClient()

response = llm.generate(
    "Explain RAG in one short paragraph."
)

print("\n--- Qwen Response ---\n")
print(response)