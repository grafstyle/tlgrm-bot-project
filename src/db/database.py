import aiosqlite
from pathlib import Path
from config import DATABASE_PATH

async def init_db() -> None:
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            first_name  TEXT NOT NULL,
            daily_goal  INTEGER NOT NULL DEFAULT 2000,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        await db.commit()

        