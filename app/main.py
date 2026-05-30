from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

from app.persistencia.database.database import Base, engine
from app.presentacion.routers.analysis_router import router as analysis_router
from app.presentacion.routers.auth_router import router as auth_router
from app.presentacion.routers.admin_router import router as admin_router

app = FastAPI(title="Analizador Estático de Código")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "default_secret_123"))


app.mount("/static", StaticFiles(directory="app/presentacion/static"), name="static")
app.mount(
    "/examples",
    StaticFiles(directory="app/presentacion/static/examples"),
    name="examples",
)

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app.include_router(analysis_router)
app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("app/presentacion/static/index.html")


@app.get("/dashboard")
async def dashboard() -> FileResponse:
    return FileResponse("app/presentacion/static/dashboard.html")


@app.get("/admin")
async def admin_dashboard() -> FileResponse:
    return FileResponse("app/presentacion/static/admin_dashboard.html")
