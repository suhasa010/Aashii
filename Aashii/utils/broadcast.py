"""Functions related to broadcasting a message to users."""

import logging

from telegram.ext import CallbackContext

from Aashii.constants import Message


async def __announcement_done(context: CallbackContext):
    del context.bot_data["announcement"]
    del context.bot_data["log_message"]
    del context.bot_data["users"]
    del context.bot_data["sent"]
    del context.bot_data["failed"]
    del context.bot_data["total"]
    del context.bot_data["steps"]
    context.job.schedule_removal()


async def __announcement_progress(user_id: int, context: CallbackContext):
    announcement = context.bot_data["announcement"]
    database = context.bot_data["database"]

    try:
        msg = await announcement.copy(user_id)
    except Exception as e:
        logging.error(str(e))
        context.bot_data["failed"] += 1
    else:
        context.bot_data["sent"] += 1
        database.add_admin_message(announcement.message_id, user_id, msg.message_id)


async def __announcement_pulse(sent, failed, total, steps):
    count = sent + failed + 1
    percent = int((count / total) * 100)

    if count in steps:
        text = Message.ANNOUNCEMENT_PULSE.format(
            SENT=sent, FAILED=failed, PROGRESS=percent
        )
    else:
        text = None

    return text


async def announce(context):
    """Announce the message to all users one by one."""
    log_message = context.bot_data["log_message"]
    sent = context.bot_data["sent"]
    failed = context.bot_data["failed"]
    total = context.bot_data["total"]
    steps = context.bot_data["steps"]

    try:
        user_id = context.bot_data["users"].pop(0)
    except IndexError:
        text = Message.ANNOUNCEMENT_DONE.format(
            SENT=sent,
            FAILED=failed,
            TOTAL=total,
        )
        await __announcement_done(context)
    else:
        await __announcement_progress(user_id, context)
        text = await __announcement_pulse(sent, failed, total, steps)

    if text:
        await log_message.edit_text(text)
