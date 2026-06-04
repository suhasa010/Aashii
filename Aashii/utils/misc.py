"""Miscellaneous functions."""

import logging
import re
import traceback

from telegram import InlineKeyboardMarkup, Update
from telegram.error import Forbidden
from telegram.ext import CallbackContext

from Aashii.constants import Button, Literal, Message

_p = re.compile("<[^>]*>")


async def add_user(update: Update, context: CallbackContext):
    """Add or update the user to database."""
    if not update.effective_message:
        return

    database = context.bot_data["database"]
    user = update.effective_message.from_user
    user_id = user.id
    full_name = user.full_name
    username = f"@{user.username}" if user.username else None
    await database.add_user(user_id, username, full_name)


async def block_user(user_id: int, context: CallbackContext):
    """Blocks the user from contacting admins and informs the user."""
    database = context.bot_data["database"]
    database.set_user_blocked(user_id, True)
    try:
        msg = await context.bot.send_photo(
            photo="https://telegra.ph/file/68aa3d09729058f1883f5.jpg",
            chat_id=user_id,
            caption=Message.BLOCKED_USER_STATUS,
        )
    except Forbidden:
        return 0
    else:
        return msg.message_id


def dehtml(text: str):
    """Return deHTMLed string from given text."""
    return _p.sub("", text)


async def error_handler(update, context):
    import traceback

    logging.error("ERROR TYPE: %s", type(context.error))
    logging.error("ERROR VALUE: %s", context.error)

    if getattr(context.error, "__traceback__", None):
        logging.error(
            "".join(
                traceback.format_exception(
                    type(context.error),
                    context.error,
                    context.error.__traceback__,
                )
            )
        )


async def get_membership(user_id: int, context: CallbackContext):
    """Return membership of user."""
    try:
        mem = await context.get_chat_member(Literal.CHAT_GROUP_ID, user_id)
    except Exception as e:
        print(e)
        membership = Message.FALLBACK_STATUS
    else:
        membership = mem.status.title()

    return membership


async def get_user_src_message(update: Update, context: CallbackContext):
    """Return user ID and source message ID if the message is a reply to user's message."""
    database = context.bot_data["database"]
    message = update.effective_message
    reply = message.reply_to_message
    user_id, src_msg_id = None, None

    if not reply:
        user_id, src_msg_id = database.get_user_message_id_from_users(
            message.message_id
        )
    elif reply.from_user.id == context.bot.id:
        user_id, src_msg_id = database.get_user_message_id_from_users(reply.message_id)
    else:
        user_id, src_msg_id = database.get_user_dest_message_id_from_admins(
            reply.message_id
        )
    return (user_id, src_msg_id)


async def request_join(update: Update, context: CallbackContext):
    """Send a message in admins group to request addition in chat group."""
    database = context.bot_data["database"]
    user_id = update.chat_join_request.from_user.id
    username = update.chat_join_request.from_user.username
    username = f"@{username}" if username else None
    blocked = database.get_user_blocked(user_id)

    if blocked:
        await context.bot.decline_chat_join_request(Literal.CHAT_GROUP_ID, user_id)
        return

    context.bot_data.pop("lastUserId", None)
    full_name = update.chat_join_request.from_user.full_name
    last_message_id = database.get_last_user_message_id(user_id)
    text = Message.JOIN_REQUEST.format(
        FULL_NAME=full_name,
        USER_ID=user_id,
        USERNAME=username,
        BLOCKED=blocked,
    )
    markup = InlineKeyboardMarkup([[Button.APPROVE, Button.DECLINE]])

    dest = await context.bot.send_message(
        chat_id=Literal.ADMINS_GROUP_ID,
        text=text,
        reply_markup=markup,
        reply_to_message_id=last_message_id,
    )
    database.set_invite_pending(user_id, True)
    database.add_user_message(last_message_id, user_id, dest.message_id)


async def unblock_user(user_id: int, context: CallbackContext):
    """Unblock the user from contacting admins and informs the user."""
    database = context.bot_data["database"]
    database.set_user_blocked(user_id, False)
    try:
        msg = await context.bot.send_message(
            chat_id=user_id,
            text=Message.UNBLOCKED_USER_STATUS,
        )
    except Forbidden:
        return 0
    else:
        return msg.message_id
