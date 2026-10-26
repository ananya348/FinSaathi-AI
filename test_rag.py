
from src.retriever import retrieve
from src.watsonx_client import generate_answer


question = "How can I stay safe while using digital payments in India?"

print("Searching the financial knowledge base...")
passages = retrieve(question, top_k=3)

print(f"Retrieved {len(passages)} passages.")

for passage in passages:
    print(
        f"- {passage['source_name']}, "
        f"page {passage['page']}, "
        f"score {passage['score']}"
    )

print("\nGenerating a grounded answer with IBM Granite...")
answer, sources = generate_answer(question, passages)

print("\n=== FinSaathi AI Answer ===\n")
print(answer)

print("\n=== Sources ===")
for source in sources:
    print(
        f"[Source {source['number']}] "
        f"{source['source_name']} — page {source['page']}"
    )
    if source["source_url"]:
        print(source["source_url"])
