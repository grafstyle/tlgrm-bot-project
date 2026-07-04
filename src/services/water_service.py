from db import models

PROGRESS_BAR_LENGTH = 10

def build_progress_bar(current: int, goal: int) -> str:
    filled = min(int((current / goal) * PROGRESS_BAR_LENGTH), PROGRESS_BAR_LENGTH)
    empty = PROGRESS_BAR_LENGTH - filled
    return f"{'█' * filled}{'░' * empty}"


async def log_water(user_id: int, amount_ml: int) -> dict:
    user = await models.get_user(user_id)
    await models.add_log(user_id=user_id, amount_ml=amount_ml)
    total = await models.get_today_total(user_id)
    goal = user["daily_goal"]

    
    return {
        "total": total,
        "goal": goal,
        "percentage": min(round((total / goal) * 100), 100),
        "goal_reached": total >= goal, 
        "progress_bar": build_progress_bar(total, goal)
    }

async def get_status(user_id: int) -> dict:
    user = await models.get_user(user_id)
    total = await models.get_today_total(user_id)
    goal = user["daily_goal"]

    return {
        "total": total,
        "goal": goal,
        "percentage": min(round((total / goal) * 100), 100),
        "remaining": max(goal - total, 0), 
        "goal_reached": total >= goal,
        "progress_bar": build_progress_bar(total, goal),
    }