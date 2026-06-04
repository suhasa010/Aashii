"""Contains handlers for all interactions to the bot."""

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    CommandHandler,
    MessageHandler,
    TypeHandler,
    filters,
)

from Aashii.base.callback_query import (
    answer_join_request,
    block_user_cb,
    connect_admin_cb,
    unblock_user_cb,
)
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
from Aashii.bridge.admin import edit_admin_message, forward_to_user
from Aashii.bridge.user import edit_user_message, forward_to_admins
from Aashii.constants import Literal
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
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "block",
                "callback": block_user_cl,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "cancel",
                "callback": cancel_announcement,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "delete",
                "callback": delete,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "help",
                "callback": send_help,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "invite",
                "callback": invite_user,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "reset",
                "callback": reset,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "start",
                "callback": send_start,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "unblock",
                "callback": unblock_user_cl,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
        (
            {
                "command": "whois",
                "callback": whois,
                "filters": ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
            },
        ),
    ],
    MessageHandler: [
        (
            {
                "filters": filters.COMMAND
                & ~filters.Chat(chat_id=Literal.CHAT_GROUP_ID),
                "callback": static_command,
            },
        ),
        (
            {
                "filters": filters.Chat(chat_id=Literal.ADMINS_GROUP_ID)
                & filters.REPLY
                & filters.UpdateType.EDITED_MESSAGE,
                "callback": edit_admin_message,
            },
        ),
        (
            {
                "filters": filters.Chat(chat_id=Literal.ADMINS_GROUP_ID),
                "callback": forward_to_user,
            },
        ),
        (
            {
                "filters": filters.ChatType.PRIVATE & filters.UpdateType.EDITED_MESSAGE,
                "callback": edit_user_message,
            },
        ),
        ({"filters": filters.ChatType.PRIVATE, "callback": forward_to_admins},),
    ],
    TypeHandler: [
        ({"type": Update, "callback": add_user}, -1),
    ],
}
