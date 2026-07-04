import aiosqlite
from config import DATABASE_PATH


async def get_or_create_user(
    user_id: int, username: str | None, first_name: str
) -> dict:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row 
        await db.execute(
            """
            INSERT INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO NOTHING
            """,
            (user_id, username, first_name),
        )
        await db.commit()
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        return dict(await cursor.fetchone())


async def update_daily_goal(user_id: int, goal_ml: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET daily_goal = ? WHERE user_id = ?",
            (goal_ml, user_id),
        )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def add_log(user_id: int, amount_ml: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO water_logs (user_id, amount_ml) VALUES(?, ?)",
            (user_id, amount_ml)
        )
        await db.commit()


async def get_today_total(user_id: int) -> int: 
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT COALESCE(SUM(amount_ml), 0)
            FROM water_logs
            WHERE user_id = ?
              AND date(logged_at) = date('now')
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        return row[0]


async def set_reminder(user_id: int, interval_minutes: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE user set reminder_interval = ? WHERE user_id = ?",
            (interval_minutes, user_id),
        )
        await db.commit()


async def get_users_with_reminders() -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT user_id, first_name, reminder_interval FROM users "
            "WHERE reminder_interval IS NOT NULL"
        )
        return [dict(row) for row in await cursor.fetchall()]