# Sesión 11 — Gemini API para interpretar restricciones

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Usar IA generativa para convertir instrucciones en lenguaje natural a un contrato estructurado validado por Pydantic, sin permitir que el LLM decida el horario.

## Resultado esperado

`POST /ai/constraints/parse` recibe texto, devuelve restricciones estructuradas y rechaza resultados que no cumplan el schema.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Responsabilidad de IA |
| 15–30 | API key y SDK |
| 30–50 | Schema de salida |
| 50–65 | Prompt |
| 65–80 | Validación y resolución de IDs |
| 80–90 | Casos ambiguos |

## Instalar SDK

```bash
pip install google-genai
```

## Variable

```env
GEMINI_API_KEY=...
GEMINI_MODEL=...
```

El nombre del modelo queda configurable para poder utilizar un modelo disponible en el nivel gratuito sin cambiar código.

## Regla de seguridad

```text
Texto usuario
   ↓
Gemini
   ↓
JSON
   ↓
Pydantic
   ↓
Resolver nombres → IDs existentes
   ↓
Confirmación en UI
   ↓
Firestore
```

Nunca:

```text
Gemini → escritura directa en Firestore
```

## Schema de salida

```python
from pydantic import BaseModel

class ParsedConstraint(BaseModel):
    type: str
    severity: str
    target_name: str | None = None
    parameters: dict

class ConstraintParseResult(BaseModel):
    constraints: list[ParsedConstraint]
    warnings: list[str] = []
```

## Prompt de sistema

El prompt debe limitar los `type` al catálogo existente y pedir advertencias cuando falte información.

Ejemplo de entrada:

```text
Marco no puede los martes y prefiere terminar antes de las 13:00.
```

El backend debe buscar al profesor por un identificador inequívoco. Si hay dos "Marco", no elegir uno arbitrariamente: devolver una advertencia de ambigüedad.

## Privacidad

Para prácticas con nivel gratuito utilizar datos académicos ficticios. No enviar información personal real sensible ni expedientes estudiantiles.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: integrate Gemini constraint parser"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
