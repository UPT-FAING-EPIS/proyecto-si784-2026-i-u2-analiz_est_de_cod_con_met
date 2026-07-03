# Static Analysis Skill - Definición

Esta Skill convierte el core del analizador estático (desarrollado en Clean Architecture) en un servicio REST API totalmente independiente y reutilizable.

## Capacidades

Permite a aplicaciones externas analizar código fuente y extraer:
- LOC (Líneas de código reales).
- Métricas estructurales (NOM, NPM, NOA).
- Complejidad ciclomatica/estructural.
- Identificación de Code Smells (Long Method, Long Parameter List).

## Por qué es una Skill (Microservicio)
De la misma manera en que una Skill de Alexa provee una capacidad específica, este microservicio extrae **únicamente** la funcionalidad de validación de código, dejando de lado la autenticación, base de datos y vistas HTML del proyecto principal.

Esto es ideal para:
- Consumir el analizador estático desde la extensión de VS Code que desarrollamos.
- Integrarlo en bots de Slack/Discord.
- Usarlo en integraciones CI/CD.

## Estructura
- `/skill/service`: Contiene la aplicación FastAPI en `main.py`.
- Su inicio es tan simple como `python main.py` en el puerto `4000`.
