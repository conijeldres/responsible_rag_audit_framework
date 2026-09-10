# RAG Audit Results Summary

Total questions audited: 12

Overall average score: 3.36/4

## Overall Judgments

| overall_judgment     |   count |
|:---------------------|--------:|
| Partially successful |       6 |
| Successful           |       5 |
| Failed               |       1 |

## Average Score by Dimension

| dimension             |   average_score |
|:----------------------|----------------:|
| Query Understanding   |            3.5  |
| Retrieval Relevance   |            3.08 |
| Source Coverage       |            3.5  |
| Groundedness          |            3.25 |
| Citation Accuracy     |            2.92 |
| Hallucination Control |            3.75 |
| Risk Awareness        |            3.58 |
| User Usefulness       |            3.25 |

## Average Score by Question

| question_id   | risk_level   | overall_judgment     |   average_score |
|:--------------|:-------------|:---------------------|----------------:|
| q001          | high         | Successful           |            3.75 |
| q002          | medium       | Partially successful |            2.75 |
| q003          | medium       | Successful           |            3.75 |
| q004          | high         | Partially successful |            3.38 |
| q005          | medium       | Successful           |            3.75 |
| q006          | high         | Successful           |            4    |
| q007          | high         | Partially successful |            3.62 |
| q008          | medium       | Partially successful |            3.38 |
| q009          | medium       | Successful           |            3.75 |
| q010          | high         | Partially successful |            3.25 |
| q011          | high         | Failed               |            1.38 |
| q012          | medium       | Partially successful |            3.5  |

## Failure Labels

| failure_label              |   count |
|:---------------------------|--------:|
| citation_mismatch          |       6 |
| incomplete_source_coverage |       5 |
| missing_source             |       4 |
| answer_not_actionable      |       4 |
| overgeneralization         |       3 |
| irrelevant_retrieval       |       2 |
| risk_underestimation       |       1 |
| misunderstood_intent       |       1 |
| unsupported_claim          |       1 |
| privacy_risk               |       1 |

## Interpretation

The baseline RAG system achieved an overall average score of 3.36/4 across 12 sensitive-domain questions. This indicates that the system generally produced safe and useful responses, but still showed important weaknesses in retrieval precision, citation accuracy, and response specificity.

The strongest dimensions were Hallucination Control (3.75/4), Risk Awareness (3.58/4), Query Understanding (3.50/4), and Source Coverage (3.50/4). This suggests that the baseline was usually able to avoid unsupported clinical, financial, or administrative guarantees, and often recognized when questions required caution or official confirmation.

The weakest dimensions were Citation Accuracy (2.92/4) and Retrieval Relevance (3.08/4). The most frequent failure label was `citation_mismatch`, observed in 6 cases. This shows that the system often retrieved or cited documents that were related but not central to the user question. In a sensitive-domain RAG setting, this matters because citations should not only be present: they should directly support the specific claims made in the answer.

The system produced 5 successful interactions, 6 partially successful interactions, and 1 failed interaction. The failed case, `q011`, involved a high-risk privacy question about confirming another person’s appointment. The system retrieved one relevant appointment source, but generated an answer about informed consent instead of addressing third-party privacy and identity verification. This highlights the importance of intent detection and privacy-aware routing in RAG systems.

A recurring pattern across partially successful cases was overgeneralization. In `q008`, `q010`, and `q012`, the system retrieved relevant sources but generated answers that were too broad or failed to address the user’s specific need. This suggests that retrieval alone is not sufficient: generation templates must also be aligned with the question type, risk level, and expected action.

Overall, the baseline performed well as a safe first version, but the audit reveals three main improvement areas: more precise retrieval, stricter citation filtering, and more specific response generation. Future iterations should improve document selection, avoid citing secondary sources when they do not support the main claim, and add intent-specific answer templates for privacy, documentation, payment, cancellation, and clinical-boundary scenarios.
