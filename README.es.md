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
## Resultados

El baseline fue evaluado en 12 preguntas en español de dominio sensible.

```text
Puntaje promedio general: 3.36/4
Interacciones exitosas: 5
Interacciones parcialmente exitosas: 6
Interacciones fallidas: 1
```

Las dimensiones con mejor desempeño fueron:

- Control de alucinaciones: 3.75/4
- Conciencia de riesgo: 3.58/4
- Comprensión de la pregunta: 3.50/4
- Cobertura de fuentes: 3.50/4

Las dimensiones más débiles fueron:

- Precisión de citas: 2.92/4
- Relevancia de la recuperación: 3.08/4

La etiqueta de fallo más frecuente fue `citation_mismatch`, observada en 6 casos.

Estos resultados sugieren que el baseline generalmente preservó la seguridad y evitó inventar garantías clínicas, financieras o administrativas. Sin embargo, la auditoría también reveló debilidades en precisión de recuperación, filtrado de citas y especificidad de generación.

Ver resultados completos:

- [Resultados de auditoría RAG](evaluations/results/rag_audit_results.es.md)
- [Resumen por dimensión](evaluations/results/dimension_summary.es.md)
- [Resumen de etiquetas de fallo](evaluations/results/failure_label_summary.es.md)
- [Resumen interpretativo de resultados](evaluations/results/rag_audit_results_summary.es.md)

```
```
## Idioma

Este repositorio está documentado en inglés y español.

- [English README](README.md)
- [Alcance del proyecto](docs/project_scope.es.md)
- [Project Scope](docs/project_scope.md)

## Estado

Versión 1 completada. [Reporte final](docs/final_report.es.md)

La versión actual incluye:

- documentos sintéticos bilingües de dominio sensible;
- un dataset de preguntas de evaluación en español;
- un pipeline baseline ligero de estilo RAG;
- corridas RAG generadas para 12 preguntas;
- auditorías cualitativas para cada corrida;
- plantillas de auditoría bilingües;
- tablas cuantitativas de resultados;
- gráficos bilingües;
- resúmenes de etiquetas de fallo;
- reportes bilingües de interpretación de resultados.

El proyecto entrega un ejemplo end-to-end de cómo auditar un sistema RAG más allá de la calidad de la respuesta final, considerando comportamiento de recuperación, cobertura de fuentes, fundamentación en evidencia, precisión de citas, control de alucinaciones, conciencia de riesgo y utilidad para el usuario.
