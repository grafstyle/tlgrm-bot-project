import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram.ext import Application, CommandHandler

from bot.handlers.onboarding import set_goal, start
from bot.handlers.tracking import drink, status
from bot.handlers.reminder import remindme, schedule_reminder
from config import BOT_TOKEN
from db.database import init_db
from db import models


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    await init_db()
    logger.info("Database ready.")

    users = await models.get_users_with_reminders()
    for user in users:
        schedule_reminder(
            application.job_queue,
            user_id=user["user_id"],
            first_name=user["first_name"],
            chat_id=user["user_id"],
            interval_minutes=user["reminder_interval"],
        )
    if users:
        logger.info(f"Restored {len(users)} reminder job(s).")


def main() -> None:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setgoal", set_goal))
    app.add_handler(CommandHandler("drink", drink))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("remindme", remindme))

    logger.info("DrinkWaterNowBot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()