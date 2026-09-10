# Responsible RAG Audit Framework

A lightweight framework to audit Retrieval-Augmented Generation systems for hallucination, source use, groundedness, and risk in sensitive-domain documents.

## Overview

Retrieval-Augmented Generation systems are often evaluated by looking only at the final answer. However, in sensitive domains, this is not enough.

A response may sound correct while relying on irrelevant sources, omitting important evidence, misrepresenting a document, inventing a policy, or giving advice beyond what the source material supports.

This project proposes a structured audit framework for RAG systems. It evaluates not only the final answer, but also the relationship between the user question, retrieved documents, cited sources, generated response, and potential risk.

## Initial Use Case

The initial use case focuses on sensitive administrative documents in a healthcare-related context.

The project uses synthetic documents and synthetic user questions related to:

- patient data and privacy;
- informed consent;
- appointment and cancellation policies;
- payment and coverage;
- escalation guidelines;
- documentation requirements.

This domain was selected because it combines procedural information, user vulnerability, privacy concerns, and the need for careful source-grounded responses.

## Core Idea

A RAG answer should not only be fluent. It should be grounded.

This project audits whether a generated answer:

- retrieves relevant sources;
- covers the necessary evidence;
- stays faithful to the documents;
- cites sources accurately;
- avoids unsupported claims;
- recognizes risk;
- communicates uncertainty when the sources are incomplete;
- gives useful but bounded guidance.

## Evaluation Dimensions

1. Query Understanding
2. Retrieval Relevance
3. Source Coverage
4. Groundedness
5. Citation Accuracy
6. Hallucination Control
7. Risk Awareness
8. User Usefulness

## Current Implementation

The current version will implement a simple baseline RAG-style system in Python.

The first version is intentionally lightweight. It does not use external LLM APIs, production healthcare systems, or real patient data. The goal is to create transparent and auditable outputs before introducing more complex retrieval or generation architectures.

Future versions may include semantic retrieval, embeddings, vector databases, or comparison between different RAG pipelines.

## Repository Structure

```text
data/
  questions_sensitive_docs.jsonl
  documents/

docs/
  project_scope.md
  project_scope.es.md
  audit_methodology.md
  audit_methodology.es.md

src/
  rag_baseline.py
  retrieval.py
  schemas.py
  run_rag.py

runs/
  rag_run_q001.json
  ...
  rag_run_q012.json

evaluations/
  rag_audit_template.md
  rag_audit_template.es.md
  audits/
    audit_q001.md
    audit_q001.es.md
    ...
    audit_q012.md
    audit_q012.es.md
  results/
    rag_audit_results.md
    rag_audit_results.es.md
    dimension_summary.md
    dimension_summary.es.md
    judgment_summary.md
    judgment_summary.es.md
    failure_label_summary.md
    failure_label_summary.es.md
    rag_audit_results_summary.md
    rag_audit_results_summary.es.md
    charts/

scripts/
  create_audit_tables.py
```

## Results

The baseline was evaluated across 12 Spanish sensitive-domain questions.

```text
Overall average score: 3.36/4
Successful interactions: 5
Partially successful interactions: 6
Failed interactions: 1
```

## Language

This repository is documented in English and Spanish.

- [Spanish README](README.es.md)
- [Project Scope](docs/project_scope.md)
- [Alcance del proyecto](docs/project_scope.es.md)


## Status

Version 1 completed.

The current version includes:

- synthetic bilingual sensitive-domain documents;
- a Spanish evaluation question dataset;
- a lightweight baseline RAG-style pipeline;
- generated RAG runs for 12 questions;
- qualitative audits for each run;
- bilingual audit templates;
- quantitative result tables;
- bilingual charts;
- failure label summaries;
- bilingual result interpretation reports.

The project now provides an end-to-end example of how a RAG system can be audited beyond final-answer quality, including retrieval behavior, source coverage, groundedness, citation accuracy, hallucination control, risk awareness, and user usefulness.