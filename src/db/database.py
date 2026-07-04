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
        await db.execute("""
            CREATE TABLE IF NOT EXISTS water_logs (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL REFERENCES users(user_id),
                amount_ml INTEGER NOT NULL,
                logged_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        await db.commit()

        cursor = await db.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in await cursor.fetchall()]
        if "reminder_interval" not in columns:
            await db.execute(
                "ALTER TABLE users ADD COLUMN reminder_interval INTEGER"
            )
            await db.commit()

    