from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class LectureNote(Base, TimestampMixin):
    __tablename__ = "lecture_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_filename: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="lecture_notes")
    summaries: Mapped[List["NoteSummary"]] = relationship(
        "NoteSummary",
        back_populates="note",
        cascade="all, delete-orphan"
    )
    flashcard_decks: Mapped[List["FlashcardDeck"]] = relationship(
        "FlashcardDeck",
        back_populates="note",
        cascade="all, delete-orphan"
    )
    mcqs: Mapped[List["NoteMCQ"]] = relationship(
        "NoteMCQ",
        back_populates="note",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<LectureNote id={self.id} title='{self.title}' subject='{self.subject}'>"


class NoteSummary(Base):
    __tablename__ = "note_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("lecture_notes.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    summary_type: Mapped[str] = mapped_column(
        String(50),
        default="executive",
        nullable=False
    )  # executive, detailed, key_takeaways
    summary_content: Mapped[str] = mapped_column(Text, nullable=False)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    note: Mapped["LectureNote"] = relationship("LectureNote", back_populates="summaries")


class FlashcardDeck(Base):
    __tablename__ = "flashcard_decks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("lecture_notes.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    card_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    note: Mapped["LectureNote"] = relationship("LectureNote", back_populates="flashcard_decks")
    cards: Mapped[List["Flashcard"]] = relationship(
        "Flashcard",
        back_populates="deck",
        cascade="all, delete-orphan"
    )


class Flashcard(Base):
    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    front_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    back_solution: Mapped[str] = mapped_column(Text, nullable=False)
    mastery_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0 to 5
    last_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    deck: Mapped["FlashcardDeck"] = relationship("FlashcardDeck", back_populates="cards")


class NoteMCQ(Base):
    __tablename__ = "note_mcqs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("lecture_notes.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSON, nullable=False)  # [{'id': 'A', 'text': '...'}]
    correct_option: Mapped[str] = mapped_column(String(10), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    note: Mapped["LectureNote"] = relationship("LectureNote", back_populates="mcqs")
