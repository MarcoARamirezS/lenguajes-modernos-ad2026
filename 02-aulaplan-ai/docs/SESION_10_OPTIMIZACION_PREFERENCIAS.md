# Sesión 10 — Optimización y preferencias

**Duración:** 1 hora 30 minutos  
**Proyecto:** AulaPlan AI

## Objetivo

Convertir el solver de factibilidad en un optimizador que considere preferencias sin convertirlas en reglas obligatorias.

## Resultado esperado

El solver devuelve `score`, penalizaciones y una solución que mantiene todos los hard constraints.

## Distribución de tiempo

| Tiempo | Actividad |
| --- | --- |
| 00–15 | Factibilidad vs optimalidad |
| 15–30 | Pesos |
| 30–50 | Variables de penalización |
| 50–65 | Función objetivo |
| 65–80 | Explicabilidad |
| 80–90 | Comparar soluciones |

## Regla principal

Nunca convertir una preferencia en hard constraint por comodidad.

## Ejemplo de pesos

| Preferencia | Penalización |
| --- | ---: |
| Clase después de hora preferida | 10 |
| Hueco de grupo | 15 |
| Hueco de profesor | 10 |
| Último bloque del día | 5 |
| Exceso de bloques consecutivos | 20 |

## Objetivo

```text
minimize(total_penalty)
```

En CP-SAT:

```python
model.minimize(sum(penalties))
```

## Resultado explicable

La API no devuelve únicamente un número:

```json
{
  "solverStatus": "OPTIMAL",
  "score": 920,
  "penalty": 80,
  "violations": [
    {
      "constraint": "TEACHER_PREFERRED_END",
      "targetId": "teacher-3",
      "penalty": 10
    }
  ]
}
```

## Prueba didáctica

Ejecutar el mismo dataset:

1. Sin soft constraints.
2. Con preferencias.
3. Comparar distribución, no solo score.

El objetivo es demostrar que un modelo matemático válido puede tener múltiples soluciones y que la función objetivo expresa qué significa "mejor" para el sistema.


## Cierre de sesión

```bash
git status
git add .
git commit -m "feat: optimize schedule preferences"
```

## Checklist

- [ ] La funcionalidad principal de la sesión funciona.
- [ ] No existen secretos versionados.
- [ ] Los endpoints nuevos aparecen en `/docs` cuando aplica.
- [ ] La documentación coincide con el código.
- [ ] Se realizó el commit de cierre.

## Navegación

- [Índice de documentación](./README.md)
