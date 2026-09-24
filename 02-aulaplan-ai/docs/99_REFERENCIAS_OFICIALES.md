# 99 — Referencias oficiales

Validado para la arquitectura del curso el **23 de septiembre de 2026**.

## Netlify

- Functions — Getting started: https://docs.netlify.com/build/functions/get-started/
- Functions configuration/routing: https://docs.netlify.com/build/functions/configuration/
- Functions API reference: https://docs.netlify.com/build/functions/api/
- Lambda compatibility / Go deprecation: https://docs.netlify.com/build/functions/lambda-compatibility/?fn-language=go
- Monorepos/build configuration: https://docs.netlify.com/build/configure-builds/monorepos/

## Nuxt

- Nuxt 4 installation: https://nuxt.com/docs/4.x/getting-started/installation
- Deployment: https://nuxt.com/docs/4.x/getting-started/deployment
- Netlify: https://nuxt.com/deploy/netlify

## Firebase

- Admin SDK setup: https://firebase.google.com/docs/admin/setup
- Authentication: https://firebase.google.com/docs/auth
- Firestore: https://firebase.google.com/docs/firestore
- Emulator Suite: https://firebase.google.com/docs/emulator-suite

## Gemini

- Getting started: https://ai.google.dev/gemini-api/docs/get-started
- Google GenAI SDK migration/current SDK: https://ai.google.dev/gemini-api/docs/migrate

## Nota de arquitectura

Aunque Netlify documenta Go Functions mediante compatibilidad AWS Lambda, ese modo está deprecated y Netlify indica que dejará de aceptar deploys en ese modo el **1 de julio de 2027**. Por eso AulaPlan AI usa Netlify Functions modernas en TypeScript.
