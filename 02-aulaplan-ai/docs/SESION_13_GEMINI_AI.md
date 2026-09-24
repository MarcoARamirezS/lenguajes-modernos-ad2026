[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 12](./SESION_12_HEURISTICS_SCORING.md) · [Sesión 14 →](./SESION_14_SCHEDULE_WORKFLOW_VERSIONING.md)

# Sesión 13 — Gemini: restricciones desde lenguaje natural

**Duración:** 1 h 30 min  
**Objetivo:** integrar IA sin delegarle la generación matemática del horario.

## Distribución

```text
00–15  Responsabilidad de IA
15–30  SDK google-genai
30–50  schema estructurado
50–68  parser
68–80  endpoint
80–90  prueba y seguridad
```

## 1. Regla de arquitectura

```text
Texto humano
 ↓
Gemini
 ↓
JSON estructurado
 ↓
Pydantic
 ↓
confirmación humana / resolución de IDs
 ↓
constraint persistida
 ↓
Scheduler Python
```

Gemini **no** escribe directamente en Firestore ni decide el horario.

## 2. Schemas de scheduling e IA

### `apps/api/src/schemas/scheduling.py`

```python
from typing import Any, Literal
from pydantic import BaseModel, Field


class GenerateScheduleRequest(BaseModel):
    academic_period_id: str = Field(min_length=1)
    max_nodes: int = Field(default=50000, ge=100, le=500000)


class ParseConstraintRequest(BaseModel):
    text: str = Field(min_length=5, max_length=3000)


class ParsedConstraint(BaseModel):
    type: Literal[
        "TEACHER_UNAVAILABLE",
        "TEACHER_PREFERRED",
        "GROUP_UNAVAILABLE",
        "GROUP_AVOID_LAST_BLOCK",
        "MAX_CONSECUTIVE",
    ]
    priority: Literal["HARD", "SOFT"]
    target_type: Literal["TEACHER", "GROUP"]
    target: str
    weight: int = Field(default=0, ge=-1000, le=1000)
    params: dict[str, Any] = Field(default_factory=dict)


class ParsedConstraintBatch(BaseModel):
    constraints: list[ParsedConstraint]
```


## 3. Parser

### `apps/api/src/ai/gemini_constraints.py`

```python
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
```


## 4. Endpoint

### `apps/api/src/http/routes_ai.py`

```python
from flask import Blueprint, jsonify, request

from src.ai.gemini_constraints import parse_constraints
from src.auth.security import require_roles
from src.schemas.scheduling import ParseConstraintRequest

ai_bp = Blueprint("ai", __name__)


@ai_bp.post("/ai/constraints/parse")
@require_roles("ADMIN", "COORDINATOR")
def parse_constraint_text():
    payload = ParseConstraintRequest.model_validate(request.get_json(silent=True) or {})
    result = parse_constraints(payload.text)
    return jsonify(result.model_dump())
```


## 5. Registrar Blueprint

Agrega en `src/http/app.py`:

```python
from src.http.routes_ai import ai_bp
```

y:

```python
app.register_blueprint(ai_bp)
```

## 5.1 Actualizar la Function para enlazar el secreto

### `apps/api/main.py`

```python
from firebase_admin import get_app, initialize_app
from firebase_functions import https_fn

from src.http.app import create_app

try:
    get_app()
except ValueError:
    initialize_app()

flask_app = create_app()


@https_fn.on_request(
    region="us-central1",
    cors=True,
    secrets=["GEMINI_API_KEY"],
)
def api(req: https_fn.Request) -> https_fn.Response:
    with flask_app.request_context(req.environ):
        return flask_app.full_dispatch_request()
```

## 6. Secreto local

Crea:

```text
apps/api/.secret.local
```

Contenido:

```env
GEMINI_API_KEY=TU_API_KEY
```

No hagas commit. La guía incluye `.secret.local` en `.gitignore`.

## 7. Producción

Desde la raíz:

```bash
firebase functions:secrets:set GEMINI_API_KEY
```

Pega la llave cuando CLI la solicite.

`main.py` ya enlaza el secreto con:

```python
secrets=["GEMINI_API_KEY"]
```

## 8. Probar endpoint

Con usuario ADMIN/COORDINATOR autenticado:

```bash
curl -X POST http://127.0.0.1:5001/PROJECT_ID/us-central1/api/ai/constraints/parse   -H "Authorization: Bearer ID_TOKEN"   -H "Content-Type: application/json"   -d '{
    "text":"Ana no puede dar clases el martes y prefiere el lunes a primera hora."
  }'
```

## Resultado conceptual

```json
{
  "constraints": [
    {
      "type": "TEACHER_UNAVAILABLE",
      "priority": "HARD",
      "target_type": "TEACHER",
      "target": "Ana",
      "weight": 0,
      "params": {}
    }
  ]
}
```

La respuesta conserva `target: "Ana"` porque Gemini no debe inventar un ID. La UI o el backend resuelve después el profesor correcto y el usuario confirma.

## Checklist

- [ ] SDK instalado.
- [ ] API key fuera de Git.
- [ ] structured output.
- [ ] Pydantic valida.
- [ ] no se guarda automáticamente.
- [ ] scheduler continúa siendo determinista respecto a sus entradas.

## Commit

```bash
git add .
git commit -m "feat: parse scheduling constraints with Gemini"
```

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 12](./SESION_12_HEURISTICS_SCORING.md) · [Sesión 14 →](./SESION_14_SCHEDULE_WORKFLOW_VERSIONING.md)
