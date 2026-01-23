"""
Database module for the Maestro AI Agent system.

This module provides database initialization, session management,
and interaction logging for the AI agent's conversation flow.
"""

from .database import (
    DATABASE_URL,
    SessionLocal,
    engine,
    init_db,
    log_interaction,
)
from .models import (
    Base,
    UserMessage,
    RefinedMessage,
    FinalResponse,
)

__all__ = [
    # Database functions
    "DATABASE_URL",
    "SessionLocal",
    "engine",
    "init_db",
    "log_interaction",
    # Models
    "Base",
    "UserMessage",
    "RefinedMessage",
    "FinalResponse",
]
