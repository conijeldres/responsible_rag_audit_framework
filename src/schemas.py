from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class RAGQuestion:
    question_id: str
    language: str
    domain: str
    user_question: str
    risk_level: str
    expected_sources: List[str]
    expected_behavior: str
    failure_modes_to_watch: List[str]


@dataclass
class RetrievedDocument:
    document_name: str
    score: int
    content_preview: str


@dataclass
class RAGRun:
    question_id: str
    user_question: str
    risk_level: str
    expected_sources: List[str]
    retrieved_documents: List[RetrievedDocument]
    generated_answer: str
    cited_sources: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "user_question": self.user_question,
            "risk_level": self.risk_level,
            "expected_sources": self.expected_sources,
            "retrieved_documents": [
                asdict(document) for document in self.retrieved_documents
            ],
            "generated_answer": self.generated_answer,
            "cited_sources": self.cited_sources,
        }
