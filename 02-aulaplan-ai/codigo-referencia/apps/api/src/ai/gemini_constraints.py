import json
import os

from google import genai
from google.genai import types

from src.core.errors import ApiError
from src.schemas.scheduling import ParsedConstraintBatch

SYSTEM_INSTRUCTION = """
Convierte restricciones académicas escritas en español en JSON estructurado.
No inventes IDs. Conserva nombres de profesores o grupos en el campo target.
Usa HARD para reglas obligatorias y SOFT para preferencias.
Devuelve únicamente restricciones representables por el schema solicitado.
""".strip()


def parse_constraints(text: str) -> ParsedConstraintBatch:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ApiError("GEMINI_API_KEY is not configured", 503, "AI_NOT_CONFIGURED")

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    response = client.models.generate_content(
        model=model,
        contents=f"{SYSTEM_INSTRUCTION}\n\nTexto del usuario:\n{text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ParsedConstraintBatch,
            temperature=0.1,
        ),
    )

    if response.parsed:
        return response.parsed
    if response.text:
        return ParsedConstraintBatch.model_validate(json.loads(response.text))
    raise ApiError("Gemini returned an empty response", 502, "AI_EMPTY_RESPONSE")
