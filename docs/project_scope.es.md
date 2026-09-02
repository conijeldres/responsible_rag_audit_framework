# Alcance del proyecto: Responsible RAG Audit Framework

## Resumen del proyecto

Responsible RAG Audit Framework es un proyecto ligero para auditar sistemas de generación aumentada por recuperación, o RAG, en contextos de dominio sensible.

El proyecto se centra en evaluar si un sistema RAG recupera fuentes relevantes, las utiliza de manera fiel, evita alucinaciones, cita evidencia con precisión y responde de forma adecuada cuando una pregunta involucra privacidad, incertidumbre o posible riesgo.

El caso de uso inicial se basa en documentos administrativos sintéticos de salud en español e inglés.

## Objetivo principal

El objetivo principal es diseñar un marco estructurado de auditoría para evaluar respuestas RAG más allá de la calidad superficial de la respuesta final.

El proyecto busca evaluar la relación entre:

- la pregunta del usuario;
- los documentos recuperados;
- la evidencia disponible en las fuentes;
- la respuesta generada;
- las fuentes citadas;
- el nivel de riesgo de la consulta.

## Caso de uso inicial

El caso de uso inicial se centra en documentos administrativos sensibles dentro de un contexto relacionado con salud.

El conjunto de documentos sintéticos incluye políticas relacionadas con:

- datos de pacientes y privacidad;
- consentimiento informado;
- políticas de horas médicas y cancelación;
- pagos y cobertura;
- requisitos de documentación;
- pautas de derivación.

Este dominio fue seleccionado porque requiere un manejo cuidadoso de información procedimental, privacidad, incertidumbre y límites de seguridad.

## Qué evalúa este proyecto

Este proyecto evalúa si un sistema de estilo RAG:

1. comprende correctamente la pregunta del usuario;
2. recupera documentos relevantes;
3. cubre la evidencia necesaria de las fuentes;
4. genera una respuesta fundamentada en los documentos recuperados;
5. evita afirmaciones no respaldadas;
6. evita políticas inventadas o detalles inexistentes;
7. cita los documentos fuente adecuados;
8. comunica incertidumbre cuando los documentos son incompletos;
9. reconoce riesgos de privacidad o seguridad;
10. entrega orientación útil, pero delimitada.

## Fuera del alcance

Este proyecto no busca construir un sistema de salud listo para producción.

Los siguientes elementos están fuera del alcance:

- datos reales de pacientes;
- integraciones reales con sistemas de salud;
- sistemas reales de agendamiento;
- diagnóstico clínico;
- recomendaciones de tratamiento;
- triaje de urgencia;
- interpretación de síntomas;
- interpretación de exámenes médicos;
- certificación de cumplimiento legal o regulatorio;
- decisiones automatizadas que afecten a usuarios reales.

Todos los documentos, preguntas y ejemplos generados son sintéticos y fueron creados únicamente con fines de evaluación.

## Dimensiones de evaluación

El marco de auditoría utiliza ocho dimensiones de evaluación:

1. Comprensión de la pregunta
2. Relevancia de la recuperación
3. Cobertura de fuentes
4. Fundamentación en evidencia
5. Precisión de citas
6. Control de alucinaciones
7. Conciencia de riesgo
8. Utilidad para el usuario

## Escala de puntuación

Cada dimensión se evalúa en una escala de 0 a 4:

```text
0 = Fallo crítico
1 = Deficiente
2 = Aceptable
3 = Bueno
4 = Excelente
```

## Taxonomía inicial de fallos

La taxonomía inicial de fallos incluye:

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

## Resultados esperados

Se espera que el proyecto produzca:

- una colección sintética de documentos de dominio sensible;
- un dataset sintético de preguntas;
- un pipeline baseline de estilo RAG;
- respuestas generadas con referencias a fuentes recuperadas;
- plantillas manuales de auditoría;
- auditorías RAG por tarea;
- resultados cuantitativos basados en rúbrica;
- etiquetas de fallo;
- gráficos y tablas de resumen;
- documentación bilingüe en inglés y español.

## Estado actual

El proyecto se encuentra en desarrollo.

La versión actual incluye la estructura inicial del repositorio, los archivos README bilingües y el documento de alcance en inglés. Los próximos pasos incluyen crear la metodología de auditoría, los documentos sintéticos, el dataset de preguntas, el pipeline RAG baseline y los resultados de evaluación.

## Relación con trabajo previo

Este proyecto se construye a partir del Agent Trajectory Evaluation Framework, pero se enfoca en una capa de evaluación distinta.

El proyecto anterior evaluó la trayectoria completa de un agente de IA. Este proyecto se centra específicamente en el comportamiento RAG: calidad de recuperación, uso de fuentes, fundamentación, control de alucinaciones, precisión de citas y respuestas sensibles al riesgo.

En conjunto, ambos proyectos contribuyen a un portafolio centrado en evaluación de IA, IA responsable, sistemas en español, QA lingüístico y flujos de evaluación auditables.
