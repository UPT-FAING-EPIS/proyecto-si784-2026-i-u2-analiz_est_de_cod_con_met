import os
from typing import Any

from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
import requests

from app.negocios.services.analysis_coordinator import AnalysisCoordinator
from app.persistencia.database.dependencies import get_db
from app.persistencia.repositories import AnalysisRepository, UserRepository
from app.persistencia.models.models import User

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/upload")
async def upload_code_analysis(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Recibe un archivo Java, lo analiza y guarda el reporte en la BD.

    - file: Archivo con código Java.
    - user_id: ID del usuario que sube el análisis (simulado con Form).
    - db: Sesión de base de datos inyectada.

    Retorna el reporte creado en formato JSON.
    """
    # Leer el contenido del archivo
    content = await file.read()
    code_string = content.decode("utf-8")

    # Instanciar repositorio y coordinador
    repository = AnalysisRepository(db)
    user_repo = UserRepository(db)
    coordinator = AnalysisCoordinator(repository)

    # Procesar y guardar el análisis
    # El nombre del proyecto es el nombre del archivo sin extensión
    filename = file.filename or "unnamed_project"
    project_name, file_extension = os.path.splitext(filename)
    project_name = project_name or "unnamed_project"
    file_extension = file_extension.lower()

    report = coordinator.process_and_save_code(
        user_id=user_id,
        project_name=project_name,
        code_string=code_string,
        file_extension=file_extension,
    )

    user_repo.log_action(user_id, f"Análisis de código subido: {project_name}")

    # Convertir el reporte a dict para la respuesta JSON
    return {
        "id": report.id,
        "user_id": report.user_id,
        "project_name": report.project_name,
        "analysis_date": report.analysis_date.isoformat(),
        "loc": report.loc,
        "complexity": report.complexity,
        "code_smells": report.code_smells,
    }


@router.post("/github")
async def analyze_github_repo(
    repo_url: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Analiza un repositorio de GitHub y guarda el reporte en la BD."""
    repository = AnalysisRepository(db)
    user_repo = UserRepository(db)
    coordinator = AnalysisCoordinator(repository)

    report = coordinator.process_and_save_github_repo(
        user_id=user_id,
        repo_url=repo_url,
    )
    user_repo.log_action(user_id, f"Análisis de repositorio GitHub: {repo_url}")

    return {
        "id": report.id,
        "user_id": report.user_id,
        "project_name": report.project_name,
        "analysis_date": report.analysis_date.isoformat(),
        "loc": report.loc,
        "complexity": report.complexity,
        "code_smells": report.code_smells,
    }


@router.post("/external/github")
async def analyze_external_github_repo(
    repo_url: str = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Analiza un repositorio de GitHub de forma externa sin guardar estado.
    Perfecto para integraciones con otros microservicios (como el Analizador de Vulnerabilidades).
    """
    user_repo = UserRepository(db)
    
    # Registrar la acción bajo un usuario especial "API_Externa" para que salga en el panel Admin
    ext_user = user_repo.get_user_by_username("API_Externa")
    if not ext_user:
        ext_user = user_repo.create_user(username="API_Externa", password="no_login_allowed", role="system")
        
    user_repo.log_action(ext_user.id, f"Análisis externo consumido para: {repo_url}")

    coordinator = AnalysisCoordinator(None)
    report_dict = coordinator.process_github_repo_stateless(repo_url=repo_url)
    
    return {
        "status": "success",
        "project_name": report_dict["project_name"],
        "loc": report_dict["loc"],
        "complexity": report_dict["complexity"],
        "code_smells": report_dict["code_smells"],
    }


@router.post("/upload_folder")
async def upload_folder_analysis(
    files: list[UploadFile] = File(...),
    user_id: int = Form(...),
    project_name: str = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Analiza múltiples archivos de una carpeta local subida."""
    repository = AnalysisRepository(db)
    user_repo = UserRepository(db)
    coordinator = AnalysisCoordinator(repository)

    files_data = []
    for file in files:
        content = await file.read()
        try:
            code_string = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        
        filename = file.filename or "unknown"
        ext = os.path.splitext(filename)[1].lower()
        
        # Filtramos internamente extensiones válidas por si acaso
        if ext in [".java", ".cs", ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".go", ".rb", ".rs"]:
            files_data.append((filename, code_string, ext))

    report = coordinator.process_and_save_folder(
        user_id=user_id,
        project_name=project_name,
        files_data=files_data,
    )

    user_repo.log_action(user_id, f"Análisis de carpeta subida: {project_name}")

    return {
        "id": report.id,
        "user_id": report.user_id,
        "project_name": report.project_name,
        "analysis_date": report.analysis_date.isoformat(),
        "loc": report.loc,
        "complexity": report.complexity,
        "code_smells": report.code_smells,
    }



@router.get("/history/{user_id}")
async def get_analysis_history(
    user_id: int,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """Obtiene el historial de reportes de un usuario en formato lista JSON."""
    repository = AnalysisRepository(db)
    reports = repository.get_reports_by_user(user_id)

    return [
        {
            "id": report.id,
            "user_id": report.user_id,
            "project_name": report.project_name,
            "analysis_date": report.analysis_date.isoformat(),
            "loc": report.loc,
            "complexity": report.complexity,
            "code_smells": report.code_smells,
        }
        for report in reports
    ]

@router.get("/github/repos/{user_id}")
async def get_github_repos(
    user_id: int,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    """Obtiene la lista de repositorios de GitHub del usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.github_token:
        raise HTTPException(status_code=400, detail="Usuario no encontrado o no ha iniciado sesión con GitHub.")
    
    headers = {"Authorization": f"token {user.github_token}"}
    response = requests.get("https://api.github.com/user/repos?per_page=100", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching repositories from GitHub")
    
    repos = response.json()
    return [{"name": repo["name"], "full_name": repo["full_name"], "url": repo["html_url"], "clone_url": repo["clone_url"]} for repo in repos]
