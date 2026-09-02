import json
from pathlib import Path
from typing import List

from src.rag_baseline import generate_baseline_answer, get_cited_sources
from src.retrieval import keyword_retrieval, load_documents
from src.schemas import RAGQuestion, RAGRun


QUESTIONS_PATH = Path("data/questions_sensitive_docs.jsonl")
RUNS_PATH = Path("runs")


def load_questions(path: Path = QUESTIONS_PATH) -> List[RAGQuestion]:
    """
    Load RAG audit questions from a JSONL file.

    Each line in the file must be a valid JSON object.
    """
    questions = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            data = json.loads(line)

            questions.append(
                RAGQuestion(
                    question_id=data["question_id"],
                    language=data["language"],
                    domain=data["domain"],
                    user_question=data["user_question"],
                    risk_level=data["risk_level"],
                    expected_sources=data["expected_sources"],
                    expected_behavior=data["expected_behavior"],
                    failure_modes_to_watch=data["failure_modes_to_watch"],
                )
            )

    return questions


def run_single_question(question: RAGQuestion) -> RAGRun:
    """
    Run the baseline RAG pipeline for a single question.
    """
    documents = load_documents(language=question.language)

    retrieved_documents = keyword_retrieval(
        query=question.user_question,
        documents=documents,
        top_k=3,
    )

    generated_answer = generate_baseline_answer(
        question=question,
        retrieved_documents=retrieved_documents,
    )

    cited_sources = get_cited_sources(retrieved_documents)

    return RAGRun(
        question_id=question.question_id,
        user_question=question.user_question,
        risk_level=question.risk_level,
        expected_sources=question.expected_sources,
        retrieved_documents=retrieved_documents,
        generated_answer=generated_answer,
        cited_sources=cited_sources,
    )


def save_run(run: RAGRun) -> None:
    """
    Save a RAG run as a JSON file.
    """
    RUNS_PATH.mkdir(parents=True, exist_ok=True)

    output_path = RUNS_PATH / f"rag_run_{run.question_id}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            run.to_dict(),
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    """
    Run the baseline RAG pipeline for all questions.
    """
    questions = load_questions()

    for question in questions:
        run = run_single_question(question)
        save_run(run)

        print(
            f"Saved run for {question.question_id}: "
            f"{len(run.retrieved_documents)} documents retrieved"
        )


if __name__ == "__main__":
    main()
