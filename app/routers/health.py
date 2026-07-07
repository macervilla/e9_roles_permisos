from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/ready")
def ready():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {"status": "ready", "database": "ok"}

    except Exception:
        return {"status": "not ready", "database": "error"}

    finally:
        db.close()
