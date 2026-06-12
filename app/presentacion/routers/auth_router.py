import bcrypt
import os
import uuid
from typing import Any

from fastapi import APIRouter, Depends, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.persistencia.database.dependencies import get_db
from app.persistencia.repositories import UserRepository
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

router = APIRouter(prefix="/api/auth", tags=["auth"])

from dotenv import load_dotenv
load_dotenv(override=True)

config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth.register(
    name='github',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    client_kwargs={'scope': 'user:email'},
)



@router.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("developer"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Registra un nuevo usuario en el sistema.

    - username: Nombre de usuario único.
    - password: Contraseña en texto plano.
    - db: Sesión de base de datos inyectada.

    Retorna los datos del usuario creado o un error si ya existe.
    """
    repository = UserRepository(db)

    # Verificar si el usuario ya existe
    existing_user = repository.get_user_by_username(username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe",
        )

    try:
        user = repository.create_user(username=username, password=password, role=role)
        repository.log_action(user.id, "Registro de usuario")
        return {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "active_status": user.active_status,
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario. El nombre de usuario podría estar duplicado.",
        )


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    repository = UserRepository(db)
    user = repository.get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    is_valid_password = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    )
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    repository.update_login_status(user.id, True)
    repository.log_action(user.id, "Inicio de sesión")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_logged_in": True,
    }


@router.post("/logout")
async def logout(
    user_id: int = Form(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    repository = UserRepository(db)
    repository.update_login_status(user_id, False)
    repository.log_action(user_id, "Cierre de sesión")
    return {"message": "Sesión cerrada correctamente"}


@router.get("/login/google")
async def login_google(request: Request):
    """Redirige al usuario al inicio de sesión con Google."""
    redirect_uri = request.url_for('callback_google')
    response = await oauth.google.authorize_redirect(request, str(redirect_uri), prompt='select_account')
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


@router.get("/callback/google")
async def callback_google(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="No user info returned from Google")
            
        username = user_info.get('email', '').split('@')[0] or "google_user"
        
        repository = UserRepository(db)
        user = repository.get_user_by_username(username)
        if not user:
            random_password = str(uuid.uuid4())
            user = repository.create_user(username=username, password=random_password, role="developer")
            repository.log_action(user.id, "Registro de usuario via Google")
        
        repository.update_login_status(user.id, True)
        repository.log_action(user.id, "Inicio de sesión via Google")
        
        return RedirectResponse(url=f"/static/oauth_success.html?id={user.id}&username={user.username}&role={user.role}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {str(e)}")


@router.get("/login/github")
async def login_github(request: Request):
    """Redirige al usuario al inicio de sesión con GitHub."""
    redirect_uri = request.url_for('callback_github')
    response = await oauth.github.authorize_redirect(request, str(redirect_uri), prompt='consent')
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


@router.get("/callback/github")
async def callback_github(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.github.authorize_access_token(request)
        resp = await oauth.github.get('user', token=token)
        profile = resp.json()
        
        username = profile.get('login')
        if not username:
            raise HTTPException(status_code=400, detail="No username returned from GitHub")
            
        repository = UserRepository(db)
        user = repository.get_user_by_username(username)
        if not user:
            random_password = str(uuid.uuid4())
            user = repository.create_user(username=username, password=random_password, role="developer")
            repository.log_action(user.id, "Registro de usuario via GitHub")
        
        repository.update_login_status(user.id, True)
        
        access_token = token.get('access_token')
        if access_token:
            repository.update_github_token(user.id, access_token)
            
        repository.log_action(user.id, "Inicio de sesión via GitHub")
        
        return RedirectResponse(url=f"/static/oauth_success.html?id={user.id}&username={user.username}&role={user.role}&provider=github")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"GitHub OAuth error: {str(e)}")
