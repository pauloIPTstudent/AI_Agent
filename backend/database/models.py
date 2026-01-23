from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserMessage(Base):
    __tablename__ = "user_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacionamento 1:1 com a mensagem refinada
    refined_version: Mapped["RefinedMessage"] = relationship(
        back_populates="original_message", cascade="all, delete-orphan"
    )

class RefinedMessage(Base):
    __tablename__ = "refined_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_message_id: Mapped[int] = mapped_column(ForeignKey("user_messages.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    model_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacionamentos
    original_message: Mapped["UserMessage"] = relationship(back_populates="refined_version")
    final_response: Mapped["FinalResponse"] = relationship(
        back_populates="refined_version", cascade="all, delete-orphan"
    )

class FinalResponse(Base):
    __tablename__ = "final_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    refined_message_id: Mapped[int] = mapped_column(ForeignKey("refined_messages.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    model_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relacionamento
    refined_version: Mapped["RefinedMessage"] = relationship(back_populates="final_response")