import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]

DATABASE_PATH: str = os.getenv(
    "DATABASE_PATH",
    str(Path(__file__).parent.parent / "drinkwaternow.db"),
)

DEFAULT_DAILY_GOAL_ML: int = 2000
MIN_GOAL_ML: int = 500 
MAX_GOAL_ML: int = 10_000

HOURS_IN_A_DAY: int = 24
MILLILITERS_IN_A_LITER: int = 1000
MILLILITERS_IN_A_CUP: int = 250
MILLILITERS_IN_A_GLASS: int = 200
MILLILITERS_IN_A_BOTTLE: int = 500
MILLILITERS_IN_A_BOTTLE: int = 500

