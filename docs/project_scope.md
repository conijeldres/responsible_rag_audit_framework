# Project Scope: Responsible RAG Audit Framework

## Project Summary

Responsible RAG Audit Framework is a lightweight project for auditing Retrieval-Augmented Generation systems in sensitive-domain contexts.

The project focuses on evaluating whether a RAG system retrieves relevant sources, uses them faithfully, avoids hallucinations, cites evidence accurately, and responds appropriately when a question involves privacy, uncertainty, or potential risk.

The initial use case is based on synthetic healthcare-administrative documents in Spanish and English.

## Main Objective

The main objective is to design a structured audit framework for evaluating RAG outputs beyond surface-level answer quality.

The project aims to assess the relationship between:

- the user question;
- the retrieved documents;
- the evidence available in the sources;
- the generated answer;
- the cited sources;
- the risk level of the query.

## Initial Use Case

The initial use case focuses on sensitive administrative documents in a healthcare-related context.

The synthetic document set includes policies related to:

- patient data and privacy;
- informed consent;
- appointment and cancellation policies;
- payment and coverage;
- documentation requirements;
- escalation guidelines.

This domain was selected because it requires careful handling of procedural information, privacy, uncertainty, and safety boundaries.

## What This Project Evaluates

This project evaluates whether a RAG-style system:

1. understands the user question correctly;
2. retrieves relevant documents;
3. covers the necessary source evidence;
4. generates an answer grounded in the retrieved sources;
5. avoids unsupported claims;
6. avoids hallucinated policies or invented details;
7. cites the appropriate source documents;
8. communicates uncertainty when the documents are incomplete;
9. recognizes privacy or safety risks;
10. provides useful but bounded guidance.

## Out of Scope

This project does not aim to build a production-ready healthcare system.

The following elements are out of scope:

- real patient data;
- real healthcare integrations;
- real appointment systems;
- clinical diagnosis;
- treatment recommendations;
- emergency triage;
- interpretation of symptoms;
- interpretation of medical exams;
- legal or regulatory compliance certification;
- automated decisions affecting real users.

All documents, questions, and generated examples are synthetic and created for evaluation purposes only.

## Evaluation Dimensions

The audit framework uses eight evaluation dimensions:

1. Query Understanding
2. Retrieval Relevance
3. Source Coverage
4. Groundedness
5. Citation Accuracy
6. Hallucination Control
7. Risk Awareness
8. User Usefulness

## Scoring Scale

Each dimension is scored on a 0-4 scale:

```text
0 = Critical failure
1 = Poor
2 = Acceptable
3 = Good
4 = Excellent
```

## Initial Failure Taxonomy

The initial failure taxonomy includes:

```text
irrelevant_retrieval
missing_source
incomplete_source_coverage
unsupported_claim
contradicted_by_source
citation_mismatch
overgeneralization
hallucinated_policy
unsafe_advice
privacy_risk
risk_underestimation
answer_not_actionable
refusal_when_answer_supported
overconfident_response
```

## Expected Outputs

The project is expected to produce:

- a synthetic sensitive-domain document collection;
- a synthetic question dataset;
- a baseline RAG-style pipeline;
- generated answers with retrieved source references;
- manual audit templates;
- task-level RAG audits;
- rubric-based quantitative results;
- failure labels;
- charts and summary tables;
- bilingual documentation in English and Spanish.

## Current Status

This project is in development.

The current version includes the initial repository structure and bilingual README files. Next steps include creating the project scope documents, audit methodology, synthetic documents, question dataset, baseline RAG pipeline, and evaluation outputs.

## Relationship to Previous Work

This project builds on the Agent Trajectory Evaluation Framework, but focuses on a different evaluation layer.

The previous project evaluated the full trajectory of an AI agent. This project focuses specifically on RAG behavior: retrieval quality, source use, groundedness, hallucination control, citation accuracy, and risk-aware answering.

Together, both projects contribute to a portfolio focused on AI evaluation, Responsible AI, Spanish-language systems, linguistic QA, and auditable evaluation workflows.
