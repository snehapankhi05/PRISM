from sqlalchemy import text

from backend.app.db.session import engine


def check_database_connection() -> bool:
    if engine is None:
        print("Database engine is not configured.")
        return False

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as exc:
        print(f"Database connection error: {type(exc).__name__}: {exc}")
        return False