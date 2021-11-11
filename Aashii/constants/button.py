"""Contains Button object."""

from telegram import InlineKeyboardButton
from .label import Label


class Button:
    """Button contains inline keyboard buttons used in reply markup."""

    APPROVE = InlineKeyboardButton(Label.APPROVE, callback_data="approve")

    BLOCK = InlineKeyboardButton(text=Label.BLOCK, callback_data="block")

    CONNECT = InlineKeyboardButton(text=Label.CONNECT, callback_data="connect")

    DECLINE = InlineKeyboardButton(Label.DECLINE, callback_data="decline")

    UNBLOCK = InlineKeyboardButton(text=Label.UNBLOCK, callback_data="unblock")
