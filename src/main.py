import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram.ext import Application, CommandHandler

from bot.handlers.onboarding import set_goal, start
from config import BOT_TOKEN
from db.database import init_db

logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    await init_db()
    logger.info("Database ready.")


def main() -> None:
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setgoal", set_goal))

    logger.info("DrinkWaterNowBot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()