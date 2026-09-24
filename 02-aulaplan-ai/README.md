# Proyecto 02 — AulaPlan AI

[← Repositorio](../README.md) · [Guía general](../GUIA_DE_NAVEGACION.md) · [Índice](./docs/README.md)

## Propósito

AulaPlan AI genera horarios académicos válidos y optimizados a partir de profesores, materias, grupos, salones, bloques, disponibilidad y restricciones.

## Stack definitivo

| Capa | Tecnología |
| --- | --- |
| Frontend | Nuxt 4 + Vue 3 + TypeScript |
| UI | Tailwind CSS 4 + daisyUI |
| Estado | Pinia |
| Backend | **Python 3.11** |
| HTTP runtime | Cloud Functions for Firebase + Flask |
| Validación | Pydantic |
| Base de datos | Cloud Firestore |
| Autenticación | Firebase Authentication |
| Admin SDK | Firebase Admin Python |
| Scheduler | Backtracking + heurísticas + scoring |
| IA | Gemini API (`google-genai`) |
| Tests backend | pytest |
| Front deploy | Netlify |
| Backend deploy | Firebase Functions |
| Repositorio | GitHub monorepo |

## Forma de trabajo

### Bloque inicial

Instalación → creación del monorepo → Firebase → GitHub → frontend completo.

### Backend

15 sesiones de 1 h 30 min. Cada una contiene:

- teoría;
- comandos;
- estructura inicial;
- archivos a crear;
- **código completo**;
- explicación;
- ejecución;
- pruebas;
- resultado esperado;
- errores frecuentes;
- checklist;
- commit;
- árbol final.

## Código de referencia

Además de los MD, `codigo-referencia/` contiene el estado final completo del proyecto para comparar el avance.

[Continuar → Índice](./docs/README.md)
