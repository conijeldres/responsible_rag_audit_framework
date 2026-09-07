from pathlib import Path
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt


AUDITS_PATH = Path("evaluations/audits")
RESULTS_PATH = Path("evaluations/results")
CHARTS_PATH = RESULTS_PATH / "charts"

RESULTS_PATH.mkdir(parents=True, exist_ok=True)
CHARTS_PATH.mkdir(parents=True, exist_ok=True)


DIMENSIONS_ES = [
    "Comprensión de la pregunta",
    "Relevancia de la recuperación",
    "Cobertura de fuentes",
    "Fundamentación en evidencia",
    "Precisión de citas",
    "Control de alucinaciones",
    "Conciencia de riesgo",
    "Utilidad para el usuario",
]

DIMENSIONS_EN = [
    "Query Understanding",
    "Retrieval Relevance",
    "Source Coverage",
    "Groundedness",
    "Citation Accuracy",
    "Hallucination Control",
    "Risk Awareness",
    "User Usefulness",
]

JUDGMENT_ES_TO_EN = {
    "Exitosa": "Successful",
    "Parcialmente exitosa": "Partially successful",
    "Fallida": "Failed",
}

JUDGMENT_EN_TO_ES = {
    "Successful": "Exitosa",
    "Partially successful": "Parcialmente exitosa",
    "Failed": "Fallida",
}


def normalize_judgment_en(judgment: str) -> str:
    judgment = judgment.strip()
    return JUDGMENT_ES_TO_EN.get(judgment, judgment)


def normalize_judgment_es(judgment: str) -> str:
    judgment_en = normalize_judgment_en(judgment)
    return JUDGMENT_EN_TO_ES.get(judgment_en, judgment)


def extract_text_value(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return default


def extract_scores(text: str) -> list[int]:
    score_matches = re.findall(r"\*\*Puntaje:\*\*\s*`?(\d)/4`?", text)
    return [int(score) for score in score_matches]


def extract_failure_labels(text: str) -> list[str]:
    section_match = re.search(
        r"## Etiquetas de fallo\s+Etiquetas seleccionadas:\s+```text\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )

    if not section_match:
        return []

    labels_text = section_match.group(1).strip()

    if not labels_text:
        return []

    return [
        label.strip()
        for label in labels_text.splitlines()
        if label.strip()
    ]


def parse_audit_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    question_id = extract_text_value(
        r"ID de la pregunta:\s*(q\d+)",
        text,
        default=path.stem.replace("audit_", "").replace(".es", ""),
    )

    risk_level = extract_text_value(
        r"Nivel de riesgo:\s*(\w+)",
        text,
        default="unknown",
    )

    judgment_raw = extract_text_value(
        r"Juicio global:\s*([^\n]+)",
        text,
        default="Unknown",
    )

    scores = extract_scores(text)

    if len(scores) != len(DIMENSIONS_ES):
        raise ValueError(
            f"{path.name} has {len(scores)} scores, expected {len(DIMENSIONS_ES)}"
        )

    failure_labels = extract_failure_labels(text)

    row = {
        "question_id": question_id,
        "risk_level": risk_level,
        "overall_judgment_en": normalize_judgment_en(judgment_raw),
        "overall_judgment_es": normalize_judgment_es(judgment_raw),
        "failure_labels": "; ".join(failure_labels),
    }

    for dimension_en, score in zip(DIMENSIONS_EN, scores):
        row[dimension_en] = score

    row["average_score"] = round(sum(scores) / len(scores), 2)

    return row


def load_audit_results() -> pd.DataFrame:
    audit_files = sorted(AUDITS_PATH.glob("audit_q*.es.md"))

    if not audit_files:
        raise FileNotFoundError(
            "No Spanish audit files were found in evaluations/audits."
        )

    rows = [parse_audit_file(path) for path in audit_files]

    df = pd.DataFrame(rows)
    df = df.sort_values("question_id")

    return df


def build_english_results(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "question_id",
        "risk_level",
        "overall_judgment_en",
        *DIMENSIONS_EN,
        "average_score",
        "failure_labels",
    ]

    return df[columns].rename(
        columns={
            "question_id": "question_id",
            "risk_level": "risk_level",
            "overall_judgment_en": "overall_judgment",
            "average_score": "average_score",
            "failure_labels": "failure_labels",
        }
    )


def build_spanish_results(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "question_id": "id_pregunta",
        "risk_level": "nivel_riesgo",
        "overall_judgment_es": "juicio_global",
        "average_score": "puntaje_promedio",
        "failure_labels": "etiquetas_de_fallo",
    }

    for dimension_en, dimension_es in zip(DIMENSIONS_EN, DIMENSIONS_ES):
        rename_map[dimension_en] = dimension_es

    columns = [
        "question_id",
        "risk_level",
        "overall_judgment_es",
        *DIMENSIONS_EN,
        "average_score",
        "failure_labels",
    ]

    return df[columns].rename(columns=rename_map)


def save_main_tables(df: pd.DataFrame) -> None:
    english_df = build_english_results(df)
    spanish_df = build_spanish_results(df)

    english_df.to_csv(
        RESULTS_PATH / "rag_audit_results.csv",
        index=False,
        encoding="utf-8",
    )

    english_df.to_markdown(
        RESULTS_PATH / "rag_audit_results.md",
        index=False,
    )

    spanish_df.to_csv(
        RESULTS_PATH / "rag_audit_results.es.csv",
        index=False,
        encoding="utf-8",
    )

    spanish_df.to_markdown(
        RESULTS_PATH / "rag_audit_results.es.md",
        index=False,
    )


def save_dimension_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    dimension_summary_en = (
        df[DIMENSIONS_EN]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"index": "dimension", 0: "average_score"})
    )

    dimension_summary_es = dimension_summary_en.copy()
    dimension_summary_es["dimension"] = DIMENSIONS_ES
    dimension_summary_es = dimension_summary_es.rename(
        columns={
            "dimension": "dimension",
            "average_score": "puntaje_promedio",
        }
    )

    dimension_summary_en.to_csv(
        RESULTS_PATH / "dimension_summary.csv",
        index=False,
        encoding="utf-8",
    )

    dimension_summary_en.to_markdown(
        RESULTS_PATH / "dimension_summary.md",
        index=False,
    )

    dimension_summary_es.to_csv(
        RESULTS_PATH / "dimension_summary.es.csv",
        index=False,
        encoding="utf-8",
    )

    dimension_summary_es.to_markdown(
        RESULTS_PATH / "dimension_summary.es.md",
        index=False,
    )

    return dimension_summary_en, dimension_summary_es


def save_judgment_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    judgment_summary_en = (
        df["overall_judgment_en"]
        .value_counts()
        .rename_axis("overall_judgment")
        .reset_index(name="count")
    )

    judgment_summary_es = (
        df["overall_judgment_es"]
        .value_counts()
        .rename_axis("juicio_global")
        .reset_index(name="conteo")
    )

    judgment_summary_en.to_csv(
        RESULTS_PATH / "judgment_summary.csv",
        index=False,
        encoding="utf-8",
    )

    judgment_summary_en.to_markdown(
        RESULTS_PATH / "judgment_summary.md",
        index=False,
    )

    judgment_summary_es.to_csv(
        RESULTS_PATH / "judgment_summary.es.csv",
        index=False,
        encoding="utf-8",
    )

    judgment_summary_es.to_markdown(
        RESULTS_PATH / "judgment_summary.es.md",
        index=False,
    )

    return judgment_summary_en, judgment_summary_es


def save_failure_label_summary(df: pd.DataFrame) -> pd.DataFrame:
    labels = []

    for value in df["failure_labels"].dropna():
        if not value.strip():
            continue

        labels.extend(
            label.strip()
            for label in value.split(";")
            if label.strip()
        )

    counter = Counter(labels)

    failure_summary = pd.DataFrame(
        counter.items(),
        columns=["failure_label", "count"],
    ).sort_values("count", ascending=False)

    failure_summary_es = failure_summary.rename(
        columns={
            "failure_label": "etiqueta_de_fallo",
            "count": "conteo",
        }
    )

    failure_summary.to_csv(
        RESULTS_PATH / "failure_label_summary.csv",
        index=False,
        encoding="utf-8",
    )

    failure_summary.to_markdown(
        RESULTS_PATH / "failure_label_summary.md",
        index=False,
    )

    failure_summary_es.to_csv(
        RESULTS_PATH / "failure_label_summary.es.csv",
        index=False,
        encoding="utf-8",
    )

    failure_summary_es.to_markdown(
        RESULTS_PATH / "failure_label_summary.es.md",
        index=False,
    )

    return failure_summary


def plot_question_averages_en(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    plt.bar(df["question_id"], df["average_score"])
    plt.ylim(0, 4)
    plt.xlabel("Question ID")
    plt.ylabel("Average score")
    plt.title("Average score by question")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "average_score_by_question.png", dpi=200)
    plt.close()


def plot_question_averages_es(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    plt.bar(df["question_id"], df["average_score"])
    plt.ylim(0, 4)
    plt.xlabel("ID de pregunta")
    plt.ylabel("Puntaje promedio")
    plt.title("Puntaje promedio por pregunta")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "puntaje_promedio_por_pregunta.png", dpi=200)
    plt.close()


def plot_dimension_averages_en(dimension_summary_en: pd.DataFrame) -> None:
    sorted_summary = dimension_summary_en.sort_values("average_score")

    plt.figure(figsize=(10, 6))
    plt.barh(sorted_summary["dimension"], sorted_summary["average_score"])
    plt.xlim(0, 4)
    plt.xlabel("Average score")
    plt.ylabel("Evaluation dimension")
    plt.title("Average score by evaluation dimension")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "average_score_by_dimension.png", dpi=200)
    plt.close()


def plot_dimension_averages_es(dimension_summary_es: pd.DataFrame) -> None:
    sorted_summary = dimension_summary_es.sort_values("puntaje_promedio")

    plt.figure(figsize=(10, 6))
    plt.barh(sorted_summary["dimension"], sorted_summary["puntaje_promedio"])
    plt.xlim(0, 4)
    plt.xlabel("Puntaje promedio")
    plt.ylabel("Dimensión de evaluación")
    plt.title("Puntaje promedio por dimensión de evaluación")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "puntaje_promedio_por_dimension.png", dpi=200)
    plt.close()


def plot_judgment_summary_en(judgment_summary_en: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(
        judgment_summary_en["overall_judgment"],
        judgment_summary_en["count"],
    )
    plt.xlabel("Overall judgment")
    plt.ylabel("Count")
    plt.title("Overall audit judgments")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "overall_audit_judgments.png", dpi=200)
    plt.close()


def plot_judgment_summary_es(judgment_summary_es: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    plt.bar(
        judgment_summary_es["juicio_global"],
        judgment_summary_es["conteo"],
    )
    plt.xlabel("Juicio global")
    plt.ylabel("Conteo")
    plt.title("Juicios globales de auditoría")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "juicios_globales_de_auditoria.png", dpi=200)
    plt.close()


def plot_failure_labels_en(failure_summary: pd.DataFrame) -> None:
    if failure_summary.empty:
        return

    plt.figure(figsize=(10, 6))
    plt.barh(
        failure_summary["failure_label"],
        failure_summary["count"],
    )
    plt.xlabel("Count")
    plt.ylabel("Failure label")
    plt.title("Failure labels observed")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "failure_labels_observed.png", dpi=200)
    plt.close()


def plot_failure_labels_es(failure_summary: pd.DataFrame) -> None:
    if failure_summary.empty:
        return

    plt.figure(figsize=(10, 6))
    plt.barh(
        failure_summary["failure_label"],
        failure_summary["count"],
    )
    plt.xlabel("Conteo")
    plt.ylabel("Etiqueta de fallo")
    plt.title("Etiquetas de fallo observadas")
    plt.tight_layout()
    plt.savefig(CHARTS_PATH / "etiquetas_de_fallo_observadas.png", dpi=200)
    plt.close()


def save_reports(
    df: pd.DataFrame,
    dimension_summary_en: pd.DataFrame,
    dimension_summary_es: pd.DataFrame,
    judgment_summary_en: pd.DataFrame,
    judgment_summary_es: pd.DataFrame,
    failure_summary: pd.DataFrame,
) -> None:
    total_questions = len(df)
    overall_average = round(df["average_score"].mean(), 2)

    best_dimension_en = dimension_summary_en.sort_values(
        "average_score",
        ascending=False,
    ).iloc[0]

    weakest_dimension_en = dimension_summary_en.sort_values(
        "average_score",
        ascending=True,
    ).iloc[0]

    best_dimension_es = dimension_summary_es.sort_values(
        "puntaje_promedio",
        ascending=False,
    ).iloc[0]

    weakest_dimension_es = dimension_summary_es.sort_values(
        "puntaje_promedio",
        ascending=True,
    ).iloc[0]

    report_en = f"""# RAG Audit Results Summary

## Overview

This report summarizes the audit results for the Responsible RAG Audit Framework.

```text
Total questions audited: {total_questions}
Overall average score: {overall_average}/4
Best-performing dimension: {best_dimension_en["dimension"]} ({best_dimension_en["average_score"]}/4)
Weakest dimension: {weakest_dimension_en["dimension"]} ({weakest_dimension_en["average_score"]}/4)
