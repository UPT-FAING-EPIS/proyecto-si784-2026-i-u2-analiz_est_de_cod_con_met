from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.persistencia.database.dependencies import get_db
from app.persistencia.repositories import UserRepository

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    repository = UserRepository(db)
    users = repository.get_all_users()
    
    return [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "active_status": u.active_status,
            "is_logged_in": u.is_logged_in,
        }
        for u in users
    ]

@router.get("/actions")
async def get_all_actions(
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    repository = UserRepository(db)
    actions = repository.get_user_actions(limit=limit)
    
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "username": a.user.username if a.user else "Desconocido",
            "action": a.action,
            "timestamp": a.timestamp.isoformat(),
        }
        for a in actions
    ]
