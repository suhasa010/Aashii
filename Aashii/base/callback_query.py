"""Functions to handle callback query."""

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from Aashii.constants import Button, Label, Literal, Message
from Aashii.utils.misc import (
    block_user,
    get_membership,
    get_user_src_message,
    unblock_user,
)
from Aashii.utils.wrappers import check_is_blocked_by_user


def answer_join_request(update: Update, context: CallbackContext):
    """Approve or decline user to join the group."""
    update.callback_query.answer()
    admin_id = update.callback_query.from_user.id
    user_id, _ = get_user_src_message(update, context)
    full_name = update.callback_query.from_user.full_name
    status = ""

    if update.callback_query.data == "approve":
        status = f"{Message.JOIN_REQUEST_APPROVED}"
        context.bot.approve_chat_join_request(Literal.CHAT_GROUP_ID, user_id)
        context.bot.send_message(user_id, Message.INFORM_APPROVAL)
    else:
        status = f"{Message.JOIN_REQUEST_DECLINED}"
        context.bot.decline_chat_join_request(Literal.CHAT_GROUP_ID, user_id)
        context.bot.send_message(user_id, Message.INFORM_DECLINE)

    text = update.callback_query.message.text_html_urled.replace(
        Label.PENDING_REQUEST, ""
    )
    text = text + status.format(USER_ID=admin_id, FULL_NAME=full_name)
    update.callback_query.message.edit_text(text)


def block_user_cb(update: Update, context: CallbackContext):
    """Block the user for the incoming callback query."""
    update.callback_query.answer()
    database = context.bot_data["database"]
    message = update.callback_query.message
    user_id, _ = database.get_user_message_id_from_users(message.message_id)
    msg_id = block_user(user_id, context)
    membership = get_membership(user_id, context.bot)
    username, full_name, blocked = database.get_user(user_id)
    edit_text = Message.USER_CONNECTED.format(
        FULL_NAME=full_name,
        USER_ID=user_id,
        USERNAME=username,
        MEMBERSHIP=membership,
        BLOCKED=blocked,
    )
    text = Message.BLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    markup = InlineKeyboardMarkup.from_row([Button.UNBLOCK, Button.CONNECT])
    message.edit_text(text=edit_text, reply_markup=markup)
    message = message.reply_html(text)
    database.add_admin_message(0, user_id, msg_id)
    database.add_user_message(1, user_id, message.message_id)
    context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID


@check_is_blocked_by_user
def connect_admin_cb(update: Update, context: CallbackContext):
    """Connect the admin with the user."""
    update.callback_query.answer()
    database = context.bot_data["database"]
    message = update.callback_query.message
    admin_id = update.callback_query.from_user.id
    admin_name = update.callback_query.from_user.full_name
    user_id, _ = database.get_user_message_id_from_users(message.message_id)
    full_name = database.get_user_full_name(user_id)
    text = Message.ADMIN_CONNECTED.format(
        ADMIN_ID=admin_id,
        ADMIN_FULL_NAME=admin_name,
        USER_ID=user_id,
        USER_FULL_NAME=full_name,
    )
    msg = context.bot.send_photo(
        photo="https://telegra.ph/file/70dc7aec0bb44b85f7c62.jpg",
        chat_id=user_id,
        caption=Message.ADMIN_CONNECTED_STATUS,
    )
    update.callback_query.answer()
    message = message.reply_html(text)
    database.add_admin_message(0, user_id, msg.message_id)
    database.add_user_message(1, user_id, message.message_id)


def unblock_user_cb(update: Update, context: CallbackContext):
    """Unblocks the user for the incoming callback query."""
    update.callback_query.answer()
    database = context.bot_data["database"]
    message = update.callback_query.message
    user_id, _ = database.get_user_message_id_from_users(message.message_id)
    msg_id = unblock_user(user_id, context)
    membership = get_membership(user_id, context.bot)
    username, full_name, blocked = database.get_user(user_id)
    edit_text = Message.USER_CONNECTED.format(
        FULL_NAME=full_name,
        USER_ID=user_id,
        USERNAME=username,
        MEMBERSHIP=membership,
        BLOCKED=blocked,
    )
    text = Message.UNBLOCKED_USER.format(USER_ID=user_id, FULL_NAME=full_name)
    markup = InlineKeyboardMarkup.from_row([Button.BLOCK, Button.CONNECT])
    message.edit_text(text=edit_text, reply_markup=markup)
    message = message.reply_html(text)
    database.add_admin_message(0, user_id, msg_id)
    database.add_user_message(1, user_id, message.message_id)
    context.bot_data["lastUserId"] = Literal.ADMINS_GROUP_ID
