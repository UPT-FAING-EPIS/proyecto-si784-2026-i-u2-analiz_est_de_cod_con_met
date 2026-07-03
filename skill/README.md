# Static Analysis Skill

Servicio REST independiente para consumir el validador estático de código desde otros proyectos, extensiones (como VS Code) o CLIs, sin tener que levantar el frontend web completo.

## ¿Qué resuelve?

El proyecto principal cuenta con vistas y controladores para renderizar un dashboard interactivo en HTML. Sin embargo, otras herramientas (como extensiones de IDE o pipelines CI/CD) solo necesitan extraer métricas y code smells puros desde el código. Esta **Skill** actúa como un microservicio que toma el motor core (ubicado en `app/motor_analisis`) y lo expone como una API reutilizable y ligera.

## Arquitectura

- `skill/STATIC_ANALYSIS_SKILL.md`: Definición conceptual de la capacidad reutilizable.
- `skill/service/`: Directorio que contiene la API FastAPI independiente.
- `skill/service/main.py`: Adaptador fino que levanta un servidor e importa el core en `app/motor_analisis/services.py`.

La Skill **no** depende de la base de datos, el enrutamiento de autenticación, ni de los HTML templates del proyecto principal.

## Ejecutar localmente

Desde la raíz del repositorio, entra al directorio y ejecuta:

```bash
cd skill/service
pip install -r requirements.txt
python main.py
```

El servicio escuchará por defecto en:

```text
http://localhost:4000
```

Health check:

```bash
curl http://localhost:4000/health
```

## Swagger (Documentación de API)

FastAPI genera automáticamente la documentación OpenAPI. Puedes abrirla en tu navegador:

```text
http://localhost:4000/docs
```

## Variables de entorno

```env
PORT=4000
CORS_ORIGIN=*
```

## Endpoints

- `GET /health`: Estado del servicio.
- `POST /api/v1/validate`: Endpoint principal para analizar el código.

## Ejemplo de uso con `curl`

```bash
curl -X POST http://localhost:4000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"extension":".py","code":"def sumar(a,b):\n  return a+b"}'
```

## Ejemplo en Python (`requests`)

```python
import requests

response = requests.post(
    "http://localhost:4000/api/v1/validate",
    json={"extension": ".py", "code": "def sumar(a, b, c, d, e, f):\n    pass"}
)

print(response.json())
```

## Formato de Respuesta Exitosa

```json
{
  "status": "success",
  "metrics": {
    "loc": 2,
    "complexity": 0,
    "method_count": 1,
    "nom": 1,
    "npm": 1,
    "noa": 0,
    "cloc": 0,
    "code_smells": [
      "Long Parameter List en método: sumar"
    ]
  }
}
```

## Códigos HTTP
- `200`: Análisis procesado correctamente.
- `400`: Falta `code` o extensión no válida.
- `500`: Error interno en el motor de parseo.
