from pathlib import Path

from app.rag.document_loader import load_markdown
from app.rag.chunker import chunk_text



BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "knowledge_base" / "support_policy.md"

content = load_markdown(str(file_path))

chunks = chunk_text(
    content,
    chunk_size=500,
    chunk_overlap=100
)

print(f"Original characters: {len(content)}")
print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk)
    print(f"Characters: {len(chunk)}")