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


def extract_value(pattern, text, default=""):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def extract_scores(text):
    return [int(score) for score in re.findall(r"\*\*Puntaje:\*\*\s*`?(\d)/4`?", text)]


def extract_failure_labels(text):
    match = re.search(
        r"## Etiquetas de fallo\s+Etiquetas seleccionadas:\s+```text\s*(.*?)\s*```",
        text,
        re.DOTALL,
    )
    if not match:
        return []

    labels_text = match.group(1).strip()
    if not labels_text:
        return []

    return [line.strip() for line in labels_text.splitlines() if line.strip()]


def parse_audit(path):
    text = path.read_text(encoding="utf-8")

    question_id = extract_value(
        r"ID de la pregunta:\s*(q\d+)",
        text,
        path.stem.replace("audit_", "").replace(".es", ""),
    )

    risk_level = extract_value(r"Nivel de riesgo:\s*(\w+)", text, "unknown")
    judgment_es = extract_value(r"Juicio global:\s*([^\n]+)", text, "Unknown")
    judgment_en = JUDGMENT_ES_TO_EN.get(judgment_es, judgment_es)

    scores = extract_scores(text)

    if len(scores) != 8:
        raise ValueError(f"{path.name} has {len(scores)} scores, expected 8")

    labels = extract_failure_labels(text)

    row = {
        "question_id": question_id,
        "risk_level": risk_level,
        "overall_judgment_en": judgment_en,
        "overall_judgment_es": JUDGMENT_EN_TO_ES.get(judgment_en, judgment_es),
        "failure_labels": "; ".join(labels),
        "average_score": round(sum(scores) / len(scores), 2),
    }

    for dimension, score in zip(DIMENSIONS_EN, scores):
        row[dimension] = score

    return row


def load_results():
    audit_files = sorted(AUDITS_PATH.glob("audit_q*.es.md"))

    if not audit_files:
        raise FileNotFoundError("No Spanish audit files found in evaluations/audits.")

    rows = [parse_audit(path) for path in audit_files]
    return pd.DataFrame(rows).sort_values("question_id")


def build_results_en(df):
    return df[
        [
            "question_id",
            "risk_level",
            "overall_judgment_en",
            *DIMENSIONS_EN,
            "average_score",
            "failure_labels",
        ]
    ].rename(columns={"overall_judgment_en": "overall_judgment"})


def build_results_es(df):
    rename_map = {
        "question_id": "id_pregunta",
        "risk_level": "nivel_riesgo",
        "overall_judgment_es": "juicio_global",
        "average_score": "puntaje_promedio",
        "failure_labels": "etiquetas_de_fallo",
    }

    for en, es in zip(DIMENSIONS_EN, DIMENSIONS_ES):
        rename_map[en] = es

    return df[
        [
            "question_id",
            "risk_level",
            "overall_judgment_es",
            *DIMENSIONS_EN,
            "average_score",
            "failure_labels",
        ]
    ].rename(columns=rename_map)


def save_tables(df):
    results_en = build_results_en(df)
    results_es = build_results_es(df)

    results_en.to_csv(RESULTS_PATH / "rag_audit_results.csv", index=False)
    results_en.to_markdown(RESULTS_PATH / "rag_audit_results.md", index=False)

    results_es.to_csv(RESULTS_PATH / "rag_audit_results.es.csv", index=False)
    results_es.to_markdown(RESULTS_PATH / "rag_audit_results.es.md", index=False)

    dimension_en = (
        df[DIMENSIONS_EN]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"index": "dimension", 0: "average_score"})
    )

    dimension_es = pd.DataFrame(
        {
            "dimension": DIMENSIONS_ES,
            "puntaje_promedio": dimension_en["average_score"],
        }
    )

    dimension_en.to_csv(RESULTS_PATH / "dimension_summary.csv", index=False)
    dimension_en.to_markdown(RESULTS_PATH / "dimension_summary.md", index=False)

    dimension_es.to_csv(RESULTS_PATH / "dimension_summary.es.csv", index=False)
    dimension_es.to_markdown(RESULTS_PATH / "dimension_summary.es.md", index=False)

    judgment_en = (
        df["overall_judgment_en"]
        .value_counts()
        .rename_axis("overall_judgment")
        .reset_index(name="count")
    )

    judgment_es = (
        df["overall_judgment_es"]
        .value_counts()
        .rename_axis("juicio_global")
        .reset_index(name="conteo")
    )

    judgment_en.to_csv(RESULTS_PATH / "judgment_summary.csv", index=False)
    judgment_en.to_markdown(RESULTS_PATH / "judgment_summary.md", index=False)

    judgment_es.to_csv(RESULTS_PATH / "judgment_summary.es.csv", index=False)
    judgment_es.to_markdown(RESULTS_PATH / "judgment_summary.es.md", index=False)

    labels = []
    for value in df["failure_labels"].dropna():
        labels.extend([label.strip() for label in value.split(";") if label.strip()])

    failure_en = (
        pd.DataFrame(Counter(labels).items(), columns=["failure_label", "count"])
        .sort_values("count", ascending=False)
    )

    failure_es = failure_en.rename(
        columns={"failure_label": "etiqueta_de_fallo", "count": "conteo"}
    )

    failure_en.to_csv(RESULTS_PATH / "failure_label_summary.csv", index=False)
    failure_en.to_markdown(RESULTS_PATH / "failure_label_summary.md", index=False)

    failure_es.to_csv(RESULTS_PATH / "failure_label_summary.es.csv", index=False)
    failure_es.to_markdown(RESULTS_PATH / "failure_label_summary.es.md", index=False)

    return dimension_en, dimension_es, judgment_en, judgment_es, failure_en


def save_chart(path, title, xlabel, ylabel, x, y, ylim=None, horizontal=False):
    plt.figure(figsize=(10, 6))

    if horizontal:
        plt.barh(x, y)
    else:
        plt.bar(x, y)

    if ylim:
        plt.ylim(*ylim)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def save_charts(df, dimension_en, dimension_es, judgment_en, judgment_es, failure_en):
    save_chart(
        CHARTS_PATH / "average_score_by_question.png",
        "Average score by question",
        "Question ID",
        "Average score",
        df["question_id"],
        df["average_score"],
        ylim=(0, 4),
    )

    save_chart(
        CHARTS_PATH / "puntaje_promedio_por_pregunta.png",
        "Puntaje promedio por pregunta",
        "ID de pregunta",
        "Puntaje promedio",
        df["question_id"],
        df["average_score"],
        ylim=(0, 4),
    )

    dimension_en_sorted = dimension_en.sort_values("average_score")
    save_chart(
        CHARTS_PATH / "average_score_by_dimension.png",
        "Average score by evaluation dimension",
        "Average score",
        "Evaluation dimension",
        dimension_en_sorted["dimension"],
        dimension_en_sorted["average_score"],
        horizontal=True,
    )

    dimension_es_sorted = dimension_es.sort_values("puntaje_promedio")
    save_chart(
        CHARTS_PATH / "puntaje_promedio_por_dimension.png",
        "Puntaje promedio por dimensión de evaluación",
        "Puntaje promedio",
        "Dimensión de evaluación",
        dimension_es_sorted["dimension"],
        dimension_es_sorted["puntaje_promedio"],
        horizontal=True,
    )

    save_chart(
        CHARTS_PATH / "overall_audit_judgments.png",
        "Overall audit judgments",
        "Overall judgment",
        "Count",
        judgment_en["overall_judgment"],
        judgment_en["count"],
    )

    save_chart(
        CHARTS_PATH / "juicios_globales_de_auditoria.png",
        "Juicios globales de auditoría",
        "Juicio global",
        "Conteo",
        judgment_es["juicio_global"],
        judgment_es["conteo"],
    )

    if not failure_en.empty:
        failure_sorted = failure_en.sort_values("count")
        save_chart(
            CHARTS_PATH / "failure_labels_observed.png",
            "Failure labels observed",
            "Count",
            "Failure label",
            failure_sorted["failure_label"],
            failure_sorted["count"],
            horizontal=True,
        )

        save_chart(
            CHARTS_PATH / "etiquetas_de_fallo_observadas.png",
            "Etiquetas de fallo observadas",
            "Conteo",
            "Etiqueta de fallo",
            failure_sorted["failure_label"],
            failure_sorted["count"],
            horizontal=True,
        )


def save_reports(df, dimension_en, dimension_es, judgment_en, judgment_es, failure_en):
    overall_average = round(df["average_score"].mean(), 2)

    report_en = (
        "# RAG Audit Results Summary\n\n"
        f"Total questions audited: {len(df)}\n\n"
        f"Overall average score: {overall_average}/4\n\n"
        "## Overall Judgments\n\n"
        f"{judgment_en.to_markdown(index=False)}\n\n"
        "## Average Score by Dimension\n\n"
        f"{dimension_en.to_markdown(index=False)}\n\n"
        "## Average Score by Question\n\n"
        f"{build_results_en(df)[['question_id', 'risk_level', 'overall_judgment', 'average_score']].to_markdown(index=False)}\n\n"
        "## Failure Labels\n\n"
        f"{failure_en.to_markdown(index=False)}\n\n"
        "## Interpretation\n\n"
        "The baseline RAG system showed strong safety behavior, but weaker performance in retrieval precision, citation precision, and generation specificity.\n"
    )

    failure_es = failure_en.rename(
        columns={"failure_label": "etiqueta_de_fallo", "count": "conteo"}
    )

    report_es = (
        "# Resumen de resultados de auditoría RAG\n\n"
        f"Total de preguntas auditadas: {len(df)}\n\n"
        f"Puntaje promedio general: {overall_average}/4\n\n"
        "## Juicios globales\n\n"
        f"{judgment_es.to_markdown(index=False)}\n\n"
        "## Puntaje promedio por dimensión\n\n"
        f"{dimension_es.to_markdown(index=False)}\n\n"
        "## Puntaje promedio por pregunta\n\n"
        f"{build_results_es(df)[['id_pregunta', 'nivel_riesgo', 'juicio_global', 'puntaje_promedio']].to_markdown(index=False)}\n\n"
        "## Etiquetas de fallo\n\n"
        f"{failure_es.to_markdown(index=False)}\n\n"
        "## Interpretación\n\n"
        "El sistema RAG baseline mostró buen comportamiento de seguridad, pero menor desempeño en precisión de recuperación, precisión de citas y especificidad de generación.\n"
    )

    (RESULTS_PATH / "rag_audit_results_summary.md").write_text(report_en, encoding="utf-8")
    (RESULTS_PATH / "rag_audit_results_summary.es.md").write_text(report_es, encoding="utf-8")


def main():
    df = load_results()
    dimension_en, dimension_es, judgment_en, judgment_es, failure_en = save_tables(df)
    save_charts(df, dimension_en, dimension_es, judgment_en, judgment_es, failure_en)
    save_reports(df, dimension_en, dimension_es, judgment_en, judgment_es, failure_en)

    print("RAG audit result tables and charts created successfully.")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
