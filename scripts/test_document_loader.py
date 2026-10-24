from pathlib import Path

from app.rag.document_loader import load_markdown


BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "knowledge_base" / "support_policy.md"

content = load_markdown(str(file_path))

print("Document loaded successfully!")
print(f"File: {file_path}")
print(f"Characters: {len(content)}")

print("\n--- Document Preview ---\n")
print(content[:1000])