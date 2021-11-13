"""Contains handlers for all interactions to the bot."""

from telegram.ext import (
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    TypeHandler,
)
from telegram import Update
from Aashii.base.commands import (
    announce_users,
    block_user_cl,
    cancel_announcement,
    delete,
    invite_user,
    reset,
    send_help,
    send_start,
    static_command,
    unblock_user_cl,
    whois,
)
from Aashii.base.callback_query import (
    answer_join_request,
    block_user_cb,
    connect_admin_cb,
    unblock_user_cb,
)
from Aashii.constants import Literal
from Aashii.bridge.admin import edit_admin_message, forward_to_user
from Aashii.bridge.user import edit_user_message, forward_to_admins
from Aashii.utils.misc import add_user, request_join

handlers = {
    CallbackQueryHandler: [
        ({"callback": answer_join_request, "pattern": r"^approve|decline$"},),
        ({"callback": block_user_cb, "pattern": r"^block$"},),
        ({"callback": connect_admin_cb, "pattern": r"^connect$"},),
        ({"callback": unblock_user_cb, "pattern": r"^unblock$"},),
    ],
    ChatJoinRequestHandler: [({"callback": request_join},)],
    CommandHandler: [
        (
            {
                "command": "announce",
                "callback": announce_users,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "block",
                "callback": block_user_cl,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "cancel",
                "callback": cancel_announcement,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "delete",
                "callback": delete,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "help",
                "callback": send_help,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "invite",
                "callback": invite_user,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "reset",
                "callback": reset,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "start",
                "callback": send_start,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "unblock",
                "callback": unblock_user_cl,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "whois",
                "callback": whois,
                "filters": ~Filters.chat(Literal.CHAT_GROUP_ID),
            },
        ),
    ],
    MessageHandler: [
        (
            {
                "filters": Filters.command & ~Filters.chat(Literal.CHAT_GROUP_ID),
                "callback": static_command,
            },
        ),
        (
            {
                "filters": Filters.chat(Literal.ADMINS_GROUP_ID)
                & Filters.reply
                & Filters.update.edited_message,
                "callback": edit_admin_message,
            },
        ),
        (
            {
                "filters": Filters.chat(Literal.ADMINS_GROUP_ID),
                "callback": forward_to_user,
            },
        ),
        (
            {
                "filters": Filters.chat_type.private & Filters.update.edited_message,
                "callback": edit_user_message,
            },
        ),
        ({"filters": Filters.chat_type.private, "callback": forward_to_admins},),
    ],
    TypeHandler: [
        ({"type": Update, "callback": add_user}, -1),
    ],
}
