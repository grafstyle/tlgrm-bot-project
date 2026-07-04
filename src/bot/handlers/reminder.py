from telegram import Update
from telegram.ext import ContextTypes

from db import models

MIN_INTERVAL = 30
MAX_INTERVAL = 240


async def _reminder_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = job.data["user_id"]
    first_name = job.data["first_name"]

    status = await models.get_today_total(user_id)
    user = await model.get_user(user_id)
    goal = user["daily_goal"]
    remaining = max(goal - status, 0)

    if remaining == 0:
        await context.bot.send_message(
            chat_id=job.chat_id,
            text=f"You've already hit your goal today {first_name}! Great work!",
        )
    else:
        await context.bot.send_message(
            chat_id=job.chat_id,
            text=(
                f"Time to drink some water, {first_name}!\n"
                f"You still need *{remaining} ml* to reach your daily goal."
            ),
            parse_mode="Markdown",
            )


def schedule_reminder(
    job_queue, user_id: int, first_name: str, chat_id: int, interval_minutes: int
) -> None:
    job_queue.run_repeating(
        _reminder_callback,
        interval=interval_minutes * 60,
        first=interval_minutes * 60,
        chat_id=chat_id,
        name=f"reminder_{user_id}",
        date={"user_id": user_id, "first_name": first_name},
    )


def cancel_reminder(job_queue, user_id: int) -> bool:
    jobs = job_queue.get_jobs_by_name(f"reminder_{user_id}")
    for job in jobs:
        job.schedule_removal()
    return len(jobs) > 0


async def remindme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text(
            "Usage:\n"
            "/remindme <minutes> — set a reminder every N minutes\n"
            "/remindme off — cancel your reminders\n\n"
            f"Interval must be between {MIN_INTERVAL} and {MAX_INTERVAL} minutes."
        )
        return

    if context.args[0].lower() == "off":
        cancelled = cancel_reminder(context.job_queue, user.id)
        await models.clear_reminder(user.id)
        if cancelled:
            await update.message.reply_text("Reminders cancelled.")
        else:
            await update.message.reply_text("You have no active reminder.")
        return

    
    try:
        interval = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            f"Please provide a number between {MIN_INTERVAL} and {MAX_INTERVAL}.\n"
            "Example: /remindme 60"
        )
        return

    if not (MIN_INTERVAL <= interval <= MAX_INTERVAL):
        await update.message.reply_text(
            f"Interval must be between {MIN_INTERVAL} and {MAX_INTERVAL} minutes."
        )
        return

    cancel_reminder(context.job_queue, user.id)
    await models.set_reminder(user.id, interval)
    schedule_reminder(
        context.job_queue,
        user_id=user.id,
        first_name=user.first_name,
        chat_id=chat_id,
        interval_minutes=interval,
    )

    await update.message.reply_text(
        f"Done! I'll remind you to drink water every *{interval} minutes*.",
        parse_mode="Markdown",
    )