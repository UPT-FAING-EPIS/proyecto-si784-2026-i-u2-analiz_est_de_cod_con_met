import bcrypt
from sqlalchemy.orm import Session

from app.persistencia.models.models import User, UserActionLog


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, username: str, password: str, role: str) -> User:
        """Crea un nuevo usuario con contraseña hasheada.

        - username: Nombre de usuario único.
        - password: Contraseña en texto plano (será hasheada).
        - role: Rol del usuario en el sistema (ej: 'developer', 'admin').

        Retorna el usuario creado.
        """
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            active_status=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User | None:
        """Busca un usuario por su nombre de usuario.

        Retorna el usuario si existe, de lo contrario None.
        """
        return self.db.query(User).filter(User.username == username).first()

    def update_login_status(self, user_id: int, is_logged_in: bool) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_logged_in = is_logged_in
            self.db.commit()

    def log_action(self, user_id: int, action: str) -> None:
        log = UserActionLog(user_id=user_id, action=action)
        self.db.add(log)
        self.db.commit()

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def get_user_actions(self, limit: int = 100) -> list[UserActionLog]:
        return self.db.query(UserActionLog).order_by(UserActionLog.timestamp.desc()).limit(limit).all()
