from app.rag.service import RAGService


rag = RAGService()

question = "Can a support agent promise a refund?"

result = rag.answer(question)

print("\n========== ANSWER ==========\n")
print(result["answer"])

print("\n========== SOURCES ==========\n")

for source in result["sources"]:
    print(source)