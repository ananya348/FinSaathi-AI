
import json
import re
from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "chunks.json"

SOURCE_URL = (
    "https://www.rbi.org.in/commonman/images/"
    "FAME%20Booklet%20second%20edition/"
    "FAME%20Booklet%20English/FAME30072020.pdf"
)

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split extracted text into overlapping character chunks."""
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def build_knowledge_base():
    """Extract text from every PDF in data/raw and save chunks."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {PDF_DIR}"
        )

    all_chunks = []

    for pdf_path in pdf_files:
        print(f"\nReading: {pdf_path.name}")

        reader = PdfReader(str(pdf_path))
        document_chunk_count = 0

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            for chunk_number, chunk in enumerate(
                split_text(text), start=1
            ):
                all_chunks.append({
                    "id": (
                        f"{pdf_path.stem}_p{page_number}_"
                        f"c{chunk_number}"
                    ),
                    "text": chunk,
                    "source_name": pdf_path.name,
                    "source_url": SOURCE_URL,
                    "page": page_number,
                })
                document_chunk_count += 1

        print(f"Passages created: {document_chunk_count}")

    if not all_chunks:
        raise ValueError(
            "No text was extracted. The PDF may be scanned or image-only."
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_chunks, file, ensure_ascii=False, indent=2)

    print("\nKnowledge base created successfully!")
    print(f"Total passages: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


def retrieve(question, top_k=3):
    """Return the most relevant passages for a question."""
    if not question.strip():
        return []

    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(
            "Knowledge base not found. Run build_knowledge.py first."
        )

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    documents = [item["text"] for item in chunks]

    # Fit a local TF-IDF search index on the document passages.
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    document_matrix = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    scores = cosine_similarity(
        question_vector, document_matrix
    ).flatten()

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        score = float(scores[index])

        # Ignore passages that have no meaningful word overlap.
        if score <= 0:
            continue

        result = dict(chunks[index])
        result["score"] = round(score, 4)
        results.append(result)

    return results


if __name__ == "__main__":
    build_knowledge_base()
