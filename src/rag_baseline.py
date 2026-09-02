from typing import List

from src.schemas import RAGQuestion, RetrievedDocument


def get_retrieved_document_names(
    retrieved_documents: List[RetrievedDocument],
) -> List[str]:
    """
    Return the names of retrieved documents.
    """
    return [
        document.document_name
        for document in retrieved_documents
    ]


def generate_baseline_answer(
    question: RAGQuestion,
    retrieved_documents: List[RetrievedDocument],
) -> str:
    """
    Generate a simple baseline answer using retrieved document names
    and risk level.

    This baseline intentionally uses rule-based response templates.
    It is designed to create auditable outputs for RAG evaluation,
    not to produce production-level answers.
    """
    query = question.user_question.lower()
    retrieved_names = get_retrieved_document_names(retrieved_documents)

    if not retrieved_documents:
        return (
            "No encontré información suficiente en los documentos disponibles "
            "para responder esta pregunta. Te recomiendo confirmar la información "
            "mediante un canal administrativo oficial."
        )

    if question.risk_level == "high":
        risk_sentence = (
            "Como esta consulta puede involucrar información sensible o posible riesgo, "
            "es importante confirmar la información mediante un canal oficial."
        )
    elif question.risk_level == "medium":
        risk_sentence = (
            "Como esta consulta puede depender de condiciones específicas, "
            "la información debería confirmarse mediante un canal oficial."
        )
    else:
        risk_sentence = (
            "Según los documentos disponibles, esta consulta parece ser administrativa "
            "y de bajo riesgo."
        )

    if any(term in query for term in ["whatsapp", "link", "mensaje", "cédula", "cedula"]):
        answer = (
            "No deberías compartir documentos de identificación, datos personales, "
            "información de salud ni datos de pago por canales no verificados. "
            "Si recibiste un mensaje, enlace o número desconocido, lo más seguro es "
            "verificarlo primero mediante un canal oficial del prestador. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["cancelar", "cancelarla", "cobren", "cobro", "multa"]):
        answer = (
            "Las cancelaciones el mismo día pueden estar sujetas a revisión administrativa. "
            "No es posible garantizar si habrá o no un cobro si los documentos no lo confirman "
            "explícitamente. Lo recomendable es contactar al prestador mediante un canal oficial "
            "para confirmar las condiciones aplicables. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["orden", "impresa", "celular", "documentos", "carnet"]):
        answer = (
            "Los requisitos de documentación pueden variar según el tipo de atención, "
            "procedimiento, cobertura y proceso del prestador. Algunos documentos podrían "
            "aceptarse en formato digital, pero no debe asumirse que una foto, captura o PDF "
            "en el teléfono sea suficiente si los documentos no lo indican. "
            "Lo más seguro es confirmar el formato aceptado por un canal oficial. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["fiebre", "síntomas", "sintomas", "urgente", "dolor"]):
        answer = (
            "No puedo evaluar urgencia clínica ni decidir si es seguro esperar una hora médica. "
            "Si hay síntomas preocupantes, fiebre alta, dolor intenso o empeoramiento, "
            "corresponde contactar a un profesional de salud, servicio de urgencia o canal oficial "
            "de atención inmediata. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["fonasa", "cobertura", "seguro", "pagar", "particular", "transferencia"]):
        answer = (
            "La cobertura y los medios de pago pueden depender del prestador, tipo de atención, "
            "especialidad, convenio, elegibilidad y proceso administrativo. No se debe garantizar "
            "cobertura, precios, reembolsos ni aceptación de transferencia si las fuentes no lo "
            "confirman explícitamente. "
            "Lo recomendable es verificarlo mediante un canal oficial. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["consentimiento", "firmar", "hija", "menor"]):
        answer = (
            "El consentimiento informado puede depender del tipo de atención, procedimiento, "
            "edad del paciente y política del prestador. Cuando se trata de menores de edad, "
            "puede requerirse verificación del tutor legal. No debe asumirse que el consentimiento "
            "digital es válido si las fuentes no lo confirman. "
            "Lo recomendable es confirmarlo mediante un canal administrativo oficial. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["tarde", "atraso", "atrasada", "atrasado"]):
        answer = (
            "Las políticas sobre atrasos pueden variar según el prestador, la especialidad "
            "y el tipo de atención. No se debe garantizar que la persona será atendida, "
            "que la hora se cancelará automáticamente o que no habrá cobro si los documentos "
            "no lo especifican. "
            "Lo recomendable es contactar al prestador lo antes posible. "
            f"{risk_sentence}"
        )

    elif any(term in query for term in ["mamá", "mama", "otra persona", "confirmar si tiene"]):
        answer = (
            "La información sobre horas médicas de otra persona es privada y no debería "
            "confirmarse sin verificación de identidad o autorización correspondiente. "
            "Para cambiar o confirmar una hora de otra persona, corresponde usar un canal "
            "administrativo oficial. "
            f"{risk_sentence}"
        )

    else:
        answer = (
            "Según los documentos recuperados, esta consulta requiere una respuesta administrativa "
            "delimitada. No se debe inventar información que no aparezca en las fuentes, y cuando "
            "la información no esté especificada, corresponde recomendar confirmación mediante "
            "un canal oficial. "
            f"{risk_sentence}"
        )

    sources_text = ", ".join(retrieved_names)

    return (
        f"{answer}\n\n"
        f"Fuentes recuperadas: {sources_text}"
    )


def get_cited_sources(
    retrieved_documents: List[RetrievedDocument],
) -> List[str]:
    """
    In this baseline, cited sources are the retrieved documents used
    to generate the answer.
    """
    return get_retrieved_document_names(retrieved_documents)
