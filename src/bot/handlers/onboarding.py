from telegram import Update
from telegram.ext import ContextTypes


from config import DEFAULT_DAILY_GOAL_ML, MIN_GOAL_ML, MAX_GOAL_ML
from db import models


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = await models.get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )
    await update.message.reply_text(
        f"Hi {user.first_name}! Welcome to Drink Water Now Bot. \n \n"
        f"I will help you track your daily water intake and remind you to stay hydrated.\n\n"
        f"Your current daily goal is *{db_user['daily_goal']} ml*.\n"
        f"You can change it anytime with /setgoal <amount>\n\n"
        f"Commands:\n"
        f"/setgoal <ml> — set your daily water goal\n"
        f"/drink <ml> — log water intake (coming soon)\n"
        f"/status — see today's progress (comming soon)",
        parse_mode="Markdown",
    )


    async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user

        if not context.args:
            await update.message.reply_text(
                "Please provide your goal in ml. \n"
                "Example: /setgoal 2500"
            )
            return
        
        try:
            goal_ml = int(context.args[0])
        except ValueError:
            await update.message.reply_text(
                "That doesn't look like a number. Example: /setgoal 2500"
            )
            return

        if not (MIN_GOAL_ML <= goal_ml <= MAX_GOAL_ML):
            await update.message.reply_text(
                f"Please set a goal between {MIN_GOAL_ML} ml and {MAX_GOAL_ML} ml."
            )
            return

        await models.update_daily_goal(user_id=user.id, goal_ml=goal_ml)
        await update.message.reply_text(
            f"Done! Your new daily goal *{goal_ml} ml*.",
            parse_mode="Markdown",
        )

        