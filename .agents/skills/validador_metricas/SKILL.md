---
name: validador_metricas
description: Capacidad para ejecutar el analizador estático de código del proyecto para Java, Python y C#, evaluar métricas (LOC, NOM, NPM) y detectar Code Smells.
---

# Habilidad del Analizador Estático (Agent Skill)

Esta habilidad documenta la lógica del motor de análisis para que cualquier Agente de IA (como este agente, Copilot Workspace o herramientas locales) pueda entender profundamente cómo funciona la evaluación de código en este repositorio y usarlo directamente en el chat.

## Funcionamiento del Motor Core

La lógica pura de evaluación se encuentra en `app/motor_analisis/services.py`. La función principal es:

```python
from app.motor_analisis.services import analyze_code
analyze_code(code_string: str, extension: str) -> Dict[str, Any]
```

### Lenguajes Soportados y Estrategia
- **Java** (`.java`): Parseo riguroso usando Abstract Syntax Trees (AST) con la librería `javalang`.
- **Python** (`.py`): Parseo riguroso usando el módulo nativo `ast` de Python.
- **C#** (`.cs`) / Genérico: Análisis basado en heurísticas de expresiones regulares.

### Estructura de la Respuesta (Métricas)
El analizador retorna un diccionario con las siguientes llaves:
- `loc`: Líneas de código reales (ignorando líneas vacías).
- `complexity`: Conteo de estructuras de control (if, for, while, switch, catch).
- `nom` (y `method_count`): Number of Methods.
- `npm`: Number of Public Methods.
- `noa`: Number of Attributes.
- `cloc`: Commented Lines of Code.
- `code_smells`: Una lista detallando los problemas detectados.

### Detección de Code Smells (Lógica Heurística)
El motor identifica automáticamente los siguientes antipatrones:
1. **Long Parameter List**: Se activa cuando un método o función recibe **más de 5 parámetros**.
2. **Long Method**: Se activa cuando el cuerpo de un método tiene **más de 50 líneas de código**.

## ¿Cómo puede la IA aprovechar esta Skill?

1. **Simulación en el Chat**: Cuando el usuario pida analizar un fragmento de código, la IA usará los umbrales documentados aquí (>5 parámetros o >50 líneas) para simular el comportamiento del sistema real en el chat.
2. **Uso del Core**: La IA puede crear scripts temporales que importen `analyze_code` y ejecuten análisis reales sobre el código sin necesidad de levantar el servidor web.
3. **Refactorización Pedagógica**: La IA está instruida para no solo mostrar el error, sino ofrecer rediseños arquitectónicos (ej. usar DTOs si hay muchos parámetros, o extraer lógica si el método es muy largo) alineados a Clean Architecture.
