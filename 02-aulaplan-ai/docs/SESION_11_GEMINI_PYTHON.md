[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 10](./SESION_10_SCHEDULER_HEURISTICS_SCORING.md) · [Sesión 12 →](./SESION_12_GENERACION_VERSIONADO.md)

# Sesión 11 — Gemini con Python

**Duración:** 1 hora 30 minutos.

## Objetivo

Convertir restricciones escritas en lenguaje natural a estructuras validadas.

## Distribución de tiempo

```text
00–15  role of AI
15–30  google-genai
30–55  structured prompt
55–70  Pydantic validation
70–85  API endpoint
85–90  commit
```


## Instalación

```bash
pip install google-genai
pip freeze > requirements.txt
```

## Entrada

```text
Marco no puede dar clases el martes y prefiere terminar antes de las 13:00.
```

## Salida esperada

```json
{
  "constraints": [
    {
      "type": "TEACHER_UNAVAILABLE_DAY",
      "target": "Marco",
      "params": {
        "day": "TUESDAY"
      }
    }
  ]
}
```

## Flujo seguro

```text
texto
 ↓
Gemini
 ↓
JSON
 ↓
Pydantic
 ↓
resolución de IDs
 ↓
confirmación humana
 ↓
Firestore
```

Gemini no escribe Firestore y no genera directamente el horario.


## Cierre verificable

- [ ] GEMINI_API_KEY fuera del repo.
- [ ] salida validada.
- [ ] respuesta inválida controlada.
- [ ] usuario confirma antes de guardar.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Sesión 10](./SESION_10_SCHEDULER_HEURISTICS_SCORING.md) · [Sesión 12 →](./SESION_12_GENERACION_VERSIONADO.md)
