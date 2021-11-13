"""Miscellaneous functions."""

import logging
import traceback
import re
from telegram import InlineKeyboardMarkup, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext
from Aashii.constants import Button, Literal, Message

_p = re.compile("<[^>]*>")


def add_user(update: Update, context: CallbackContext):
    """Add or update the user to database."""
    if not update.effective_message:
        return

    database = context.bot_data["database"]
    user = update.effective_message.from_user
    user_id = user.id
    full_name = user.full_name
    username = f"@{user.username}" if user.username else None
    database.add_user(user_id, username, full_name)


def block_user(user_id: int, context: CallbackContext):
    """Blocks the user from contacting admins and informs the user."""
    database = context.bot_data["database"]
    database.set_user_blocked(user_id, True)
    try:
        msg = context.bot.send_photo(
            photo="https://telegra.ph/file/68aa3d09729058f1883f5.jpg",
            chat_id=user_id,
            caption=Message.BLOCKED_USER_STATUS,
        )
    except Unauthorized:
        return 0
    else:
        return msg.message_id


def dehtml(text: str):
    """Return deHTMLed string from given text."""
    return _p.sub("", text)


def error_handler(_: object, context: CallbackContext):
    """Handle the known errors and exceptions."""
    error = str(context.error)
    tb = "".join(
        traceback.format_tb(context.error.__traceback__, Literal.TRACEBACK_VALUE)
    )
    logging.error(context.error)
    return
    error_text = Message.ERROR.format(ERROR=error, TRACEBACK=tb)
    if Literal.INFORM_ERROR:
        try:
            context.bot.send_message(
                chat_id=Literal.ADMINS_GROUP_ID,
                text=error_text,
            )
        except:
            logging.error("%s\n%s", error, tb)
    else:
        logging.error("%s\n%s", error, tb)


def get_membership(user_id: int, context: CallbackContext):
    """Return membership of user."""
    try:
        mem = context.get_chat_member(Literal.CHAT_GROUP_ID, user_id)
    except Exception as e:
        print(e)
        membership = Message.FALLBACK_STATUS
    else:
        membership = mem.status.title()

    return membership


def get_user_src_message(update: Update, context: CallbackContext):
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


def request_join(update: Update, context: CallbackContext):
    """Send a message in admins group to request addition in chat group."""
    database = context.bot_data["database"]
    user_id = update.chat_join_request.from_user.id
    username = update.chat_join_request.from_user.username
    username = f"@{username}" if username else None
    blocked = database.get_user_blocked(user_id)

    if blocked:
        context.bot.decline_chat_join_request(Literal.CHAT_GROUP_ID, user_id)
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

    dest = context.bot.send_message(
        chat_id=Literal.ADMINS_GROUP_ID,
        text=text,
        reply_markup=markup,
        reply_to_message_id=last_message_id,
    )
    database.add_user_message(last_message_id, user_id, dest.message_id)


def unblock_user(user_id: int, context: CallbackContext):
    """Unblock the user from contacting admins and informs the user."""
    database = context.bot_data["database"]
    database.set_user_blocked(user_id, False)
    try:
        msg = context.bot.send_message(
            chat_id=user_id,
            text=Message.UNBLOCKED_USER_STATUS,
        )
    except Unauthorized:
        return 0
    else:
        return msg.message_id
