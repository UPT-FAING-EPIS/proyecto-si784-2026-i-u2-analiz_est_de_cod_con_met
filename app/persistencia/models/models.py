from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    github_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=True)
    google_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    active_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_logged_in: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    analysis_reports: Mapped[list["AnalysisReport"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    actions: Mapped[list["UserActionLog"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    analysis_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    loc: Mapped[int] = mapped_column(Integer, nullable=False)
    complexity: Mapped[int] = mapped_column(Integer, nullable=False)
    code_smells: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    user: Mapped[User] = relationship(back_populates="analysis_reports")


class UserActionLog(Base):
    __tablename__ = "user_action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="actions")
