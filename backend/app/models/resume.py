from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class Resume(Base, TimestampMixin):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(80), default="application/pdf", nullable=False)
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extracted_skills: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    ats_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True)
    analysis_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="resumes")

    def __repr__(self) -> str:
        return f"<Resume id={self.id} user_id={self.user_id} file='{self.original_filename}'>"
