import sys
import os
from pathlib import Path

# Añadir el directorio raíz del proyecto al sys.path
# Esto permite importar el core del analizador sin modificar su estructura
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.motor_analisis.services import analyze_code

app = FastAPI(
    title="Static Analysis Skill API",
    version="1.0.0",
    description="Servicio REST independiente para consumir el analizador estático sin levantar el frontend principal."
)

# Configuración CORS basada en variables de entorno (por defecto permitimos todo para la Skill)
CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValidationRequest(BaseModel):
    code: str
    extension: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "static-analysis-skill"}

@app.post("/api/v1/validate")
def validate_code(request: ValidationRequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="El campo 'code' es obligatorio.")
    if not request.extension.startswith("."):
        raise HTTPException(status_code=400, detail="La extensión debe comenzar con un punto (ej. '.java', '.py').")
        
    try:
        # Llamar al motor core puro
        metrics = analyze_code(request.code, request.extension.lower())
        
        # Formatear la respuesta
        return {
            "status": "success",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 4000))
    uvicorn.run(app, host="0.0.0.0", port=port)
