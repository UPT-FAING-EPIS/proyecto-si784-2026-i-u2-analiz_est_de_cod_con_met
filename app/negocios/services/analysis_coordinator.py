import os
import tempfile
import urllib.request
import zipfile
from typing import Any, Dict

from app.motor_analisis.services import analyze_code
from app.persistencia.models.models import AnalysisReport
from app.persistencia.repositories import AnalysisRepository


class AnalysisCoordinator:
    def __init__(self, repository: AnalysisRepository) -> None:
        self.repository = repository

    def process_and_save_code(
        self,
        user_id: int,
        project_name: str,
        code_string: str,
        file_extension: str,
    ) -> AnalysisReport:
        """Procesa código fuente, guarda el resultado y devuelve el reporte creado.

        - Analiza el código usando `analyze_code`.
        - Crea y persiste el `AnalysisReport` mediante el repositorio.
        """
        analysis = analyze_code(code_string, extension=file_extension)

        loc = int(analysis.get("loc", 0))
        complexity = int(analysis.get("complexity", 0))
        code_smells = analysis.get("code_smells", [])

        # nuevas métricas estructurales devueltas por analyze_code
        nom = int(analysis.get("nom", 0))
        npm = int(analysis.get("npm", 0))
        noa = int(analysis.get("noa", 0))
        cloc = int(analysis.get("cloc", 0))

        # Empaquetar smells y métricas en el payload JSON esperado por el repositorio
        code_smells_payload: Dict[str, Any] = {
            "smells": code_smells,
            "metrics": {"nom": nom, "npm": npm, "noa": noa, "cloc": cloc},
        }

        report = self.repository.create_report(
            user_id=user_id,
            project_name=project_name,
            loc=loc,
            complexity=complexity,
            code_smells=code_smells_payload,
        )

        return report

    def _analyze_github_repo_core(self, repo_url: str) -> dict[str, Any]:
        """Descarga y analiza un repositorio de GitHub, devolviendo el diccionario con los resultados brutos."""
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("URL de repositorio inválida")
        owner, repo = parts[-2], parts[-1]
        if repo.endswith(".git"):
            repo = repo[:-4]
            
        zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"
        
        loc = 0
        complexity = 0
        nom = 0
        npm = 0
        noa = 0
        cloc = 0
        code_smells = []
        files_data = []
        
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "repo.zip")
            
            req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in [".java", ".cs", ".py", ".php", ".js", ".ts", ".jsx", ".tsx", ".c", ".cpp", ".h", ".go", ".rb", ".rs"]:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                code_string = f.read()
                        except UnicodeDecodeError:
                            continue
                            
                        rel_path = os.path.relpath(file_path, temp_dir)
                        path_parts = rel_path.split(os.sep)
                        if len(path_parts) > 1:
                            rel_path = os.path.join(*path_parts[1:])
                            
                        analysis = analyze_code(code_string, extension=ext)
                        
                        file_loc = int(analysis.get("loc", 0))
                        file_complexity = int(analysis.get("complexity", 0))
                        file_nom = int(analysis.get("nom", 0))
                        file_npm = int(analysis.get("npm", 0))
                        file_noa = int(analysis.get("noa", 0))
                        file_cloc = int(analysis.get("cloc", 0))
                        file_smells = analysis.get("code_smells", [])

                        loc += file_loc
                        complexity += file_complexity
                        nom += file_nom
                        npm += file_npm
                        noa += file_noa
                        cloc += file_cloc
                        
                        files_data.append({
                            "file_path": rel_path,
                            "loc": file_loc,
                            "complexity": file_complexity,
                            "metrics": {"nom": file_nom, "npm": file_npm, "noa": file_noa, "cloc": file_cloc},
                            "smells": file_smells
                        })
                        
                        for smell in file_smells:
                            code_smells.append(f"[{rel_path}] {smell}")
                            
        code_smells_payload: Dict[str, Any] = {
            "smells": code_smells,
            "metrics": {"nom": nom, "npm": npm, "noa": noa, "cloc": cloc},
            "files": files_data,
        }

        return {
            "project_name": f"{owner}/{repo}",
            "loc": loc,
            "complexity": complexity,
            "code_smells": code_smells_payload,
        }

    def process_and_save_github_repo(
        self,
        user_id: int,
        repo_url: str,
    ) -> AnalysisReport:
        """Descarga un repositorio, lo analiza y guarda el reporte consolidado."""
        data = self._analyze_github_repo_core(repo_url)
        report = self.repository.create_report(
            user_id=user_id,
            project_name=data["project_name"],
            loc=data["loc"],
            complexity=data["complexity"],
            code_smells=data["code_smells"],
        )
        return report

    def process_github_repo_stateless(self, repo_url: str) -> dict[str, Any]:
        """Descarga un repositorio, lo analiza y devuelve el reporte sin guardar en BD."""
        return self._analyze_github_repo_core(repo_url)
