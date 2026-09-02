from pathlib import Path
from typing import Dict, List

from src.schemas import RetrievedDocument


DOCUMENTS_PATH = Path("data/documents")


def load_documents(language: str = "es") -> Dict[str, str]:
    """
    Load documents from the synthetic document collection.

    By default, this function loads Spanish documents ending in .es.md.
    For English, it loads .md files that do not end in .es.md.
    """
    documents = {}

    if language == "es":
        files = DOCUMENTS_PATH.glob("*.es.md")
    else:
        files = [
            file
            for file in DOCUMENTS_PATH.glob("*.md")
            if not file.name.endswith(".es.md")
        ]

    for file in files:
        documents[file.name] = file.read_text(encoding="utf-8")

    return documents


def normalize_text(text: str) -> str:
    """
    Normalize text for simple keyword matching.
    """
    replacements = {
        "¿": "",
        "?": "",
        "¡": "",
        "!": "",
        ".": "",
        ",": "",
        ";": "",
        ":": "",
        "(": "",
        ")": "",
        "\n": " ",
    }

    text = text.lower()

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def keyword_retrieval(
    query: str,
    documents: Dict[str, str],
    top_k: int = 3,
) -> List[RetrievedDocument]:
    """
    Retrieve documents using a simple keyword overlap score.

    This baseline is intentionally simple and transparent.
    It is designed for auditability, not for production retrieval quality.
    """
    normalized_query = normalize_text(query)
    query_terms = set(normalized_query.split())

    results = []

    for document_name, content in documents.items():
        normalized_content = normalize_text(content)

        score = sum(
            1
            for term in query_terms
            if term in normalized_content
        )

        if score > 0:
            results.append(
                RetrievedDocument(
                    document_name=document_name,
                    score=score,
                    content_preview=content[:1200],
                )
            )

    results = sorted(
        results,
        key=lambda document: document.score,
        reverse=True,
    )

    return results[:top_k]
