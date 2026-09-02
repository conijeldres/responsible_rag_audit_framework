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
  generated_answers.jsonl
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
  rag_run_*.json

evaluations/
  rag_audit_template.md
  rag_audit_template.es.md
  audits/
  results/

scripts/
  create_audit_tables.py
```
## Language

This repository is documented in English and Spanish.

- [Spanish README](README.es.md)
- [Project Scope](docs/project_scope.md)
- [Alcance del proyecto](docs/project_scope.es.md)


## Status

Work in progress.
Current version includes the initial repository structure. Upcoming steps include creating the synthetic document set, question dataset, baseline RAG pipeline, audit templates, and evaluation results.
