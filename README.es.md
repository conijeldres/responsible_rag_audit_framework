# Marco de Auditoría Responsable para RAG

Un marco ligero para auditar sistemas de generación aumentada por recuperación, o RAG, en torno a alucinaciones, uso de fuentes, fundamentación en evidencia y análisis de riesgo en documentos sensibles.

## Descripción general

Los sistemas RAG suelen evaluarse observando únicamente la respuesta final. Sin embargo, en dominios sensibles, eso no es suficiente.

Una respuesta puede sonar correcta aunque se base en fuentes irrelevantes, omita evidencia importante, represente mal un documento, invente una política o entregue orientación más allá de lo que las fuentes permiten afirmar.

Este proyecto propone un marco estructurado para auditar sistemas RAG. Evalúa no sólo la respuesta final, sino también la relación entre la pregunta del usuario, los documentos recuperados, las fuentes citadas, la respuesta generada y el posible nivel de riesgo.

## Caso de uso inicial

El caso de uso inicial se centra en documentos administrativos sensibles dentro de un contexto relacionado con salud.

El proyecto utiliza documentos sintéticos y preguntas sintéticas de usuarios relacionadas con:

- datos de pacientes y privacidad;
- consentimiento informado;
- políticas de horas médicas y cancelación;
- pagos y cobertura;
- pautas de derivación;
- requisitos de documentación.

Este dominio fue seleccionado porque combina información procedimental, vulnerabilidad del usuario, privacidad y la necesidad de respuestas cuidadosas y fundamentadas en fuentes.

## Idea central

Una respuesta RAG no solo debe ser fluida. También debe estar fundamentada.

Este proyecto audita si una respuesta generada:

- recupera fuentes relevantes;
- cubre la evidencia necesaria;
- se mantiene fiel a los documentos;
- cita las fuentes con precisión;
- evita afirmaciones no respaldadas;
- reconoce el riesgo;
- comunica incertidumbre cuando las fuentes son incompletas;
- entrega orientación útil, pero delimitada.

## Dimensiones de evaluación

1. Comprensión de la pregunta
2. Relevancia de la recuperación
3. Cobertura de fuentes
4. Fundamentación en evidencia
5. Precisión de citas
6. Control de alucinaciones
7. Conciencia de riesgo
8. Utilidad para el usuario

## Implementación actual

La versión actual implementará un sistema baseline simple de estilo RAG en Python.

La primera versión es intencionalmente ligera. No utiliza APIs externas de LLMs, sistemas reales de salud ni datos reales de pacientes. El objetivo es crear resultados transparentes y auditables antes de incorporar arquitecturas de recuperación o generación más complejas.

Versiones futuras podrán incluir recuperación semántica, embeddings, bases vectoriales o comparación entre distintos pipelines RAG.

## Estructura del repositorio

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

## Idioma

Este repositorio está documentado en inglés y español.

- [English README](README.md)
- [Alcance del proyecto](docs/project_scope.es.md)
- [Project Scope](docs/project_scope.md)

## Estado

Proyecto en desarrollo.

La versión actual incluye la estructura inicial del repositorio. Los próximos pasos son crear el conjunto de documentos sintéticos, el dataset de preguntas, el pipeline RAG baseline, las plantillas de auditoría y los resultados de evaluación.
