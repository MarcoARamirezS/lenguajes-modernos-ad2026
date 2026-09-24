[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Proyecto](../README.md) · [Arquitectura →](./01_ARQUITECTURA.md)

# 00 — Inicio aquí

AulaPlan AI se construye desde cero. No se presupone que el alumno tenga creado el proyecto.

## Resultado final

```text
Usuario
  ↓
Nuxt 4
  ↓ /api/*
Netlify proxy
  ↓
Firebase HTTP Function
  ↓
Python + Flask
  ↓
Services / Repositories
  ↓
Firestore

Generar horario
  ↓
Cargar contexto
  ↓
Construir candidatos
  ↓
Hard constraints
  ↓
Backtracking
  ↓
Scoring
  ↓
Guardar versión
```

## Orden obligatorio

1. Preparar equipo.
2. Crear monorepo.
3. Configurar Firebase.
4. Subir a GitHub.
5. Construir frontend completo.
6. Empezar backend por sesiones.
7. Desplegar al terminar.

## Qué NO haremos

- No generaremos horarios directamente con Gemini.
- No accederemos a Firestore administrativamente desde el navegador.
- No pondremos secretos en Nuxt.
- No fingiremos que Python corre dentro de Netlify Functions.

---

[Repositorio](../../README.md) · [Proyecto](../README.md) · [Índice](./README.md) · [← Proyecto](../README.md) · [Arquitectura →](./01_ARQUITECTURA.md)
