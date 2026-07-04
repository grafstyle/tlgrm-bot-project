from telegram import Update
from telegram.ext import ContextTypes

from services import water_service


async def drink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    if not context.args:
        await update.message.reply_text(
            "Tell me how much you drank.\n"
            "Example: /drink 250" 
        )
        return

    try:
        amount_ml = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "That doesn't look like a number. Example: /drink 250"
        )
        return

    if amount_ml <= 0:
        await update.message.reply_text("Amount must be greater than 0.")
        return

    if amount_ml > 2000:
        await update.message.reply_text(
            "That's over 2000 ml in one go — are you sure? Log smaller amounts at a time."
        )
        return

    result = await water_service.log_water(user_id=user.id, amount_ml=amount_ml)

    if result["goal_reached"] and result["total"] - amount_ml < result["goal"]:
        await update.message.reply_text(
            f"You logged *{amount_ml} ml*.\n\n"
            f"GOAL REACHED! Congratulations {user.first_name}!\n"
            f"You hit your daily target of *{result['goal']} ml*!\n\n"
            f"{result['progress_bar']} {result['percentage']}%\n"
            f"Total today: *{result['total']} ml*",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"Logged *{amount_ml} ml*.\n\n"
            f"{result['progress_bar']} {result['percentage']}%\n"
            f"Total today: *{result['total']} ml* / {result['goal']} ml",
            parse_mode="Markdown",
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    result = await water_service.get_status(user_id=user.id)

    if result["goal_reached"]:
        await update.message.reply_text(
            f"Daily goal complete!\n\n"
            f"{result['progress_bar']} {result['percentage']}%\n"
            f"Total today: *{result['total']} ml* / {result['goal']} ml",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"Here's your progress for today:\n\n"
            f"{result['progress_bar']} {result['percentage']}%\n"
            f"Total today: *{result['total']} ml* / {result['goal']} ml\n"
            f"Remaining: *{result['remaining']} ml*",
            parse_mode="Markdown",
            )

