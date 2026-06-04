"""Functions related to transfering messages and their edits."""

from telegram import (
    Bot,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)
from telegram import Message as TMessage
from telegram.constants import MessageLimit

from Aashii.constants import Message
from Aashii.utils.misc import dehtml


def _get_from_tag(message: TMessage, quote: bool):
    if quote:
        entity_from = Message.ENTITY_FROM.format(
            USER_ID=message.from_user.id,
            FULL_NAME=message.from_user.full_name,
        )
    else:
        entity_from = "\n"

    forward_sender_name = getattr(message, "forward_sender_name", None)
    forward_from_chat = getattr(message, "forward_from_chat", None)
    forward_from = getattr(message, "forward_from", None)
    forward_from_message_id = getattr(message, "forward_from_message_id", None)

    if forward_sender_name:
        return Message.ENTITY_FORWARD_ANONYMOUS.format(
            SENDER_NAME=forward_sender_name,
            FROM=entity_from,
        )

    elif forward_from_chat:
        chat_id = int(str(forward_from_chat.id).replace("-100", ""))
        name = forward_from_chat.title

        return Message.ENTITY_FORWARD_CHAT.format(
            FROM_CHAT_ID=chat_id,
            FROM_CHAT_NAME=name,
            MESSAGE_ID=forward_from_message_id,
            FROM=entity_from,
        )

    elif forward_from:
        return Message.ENTITY_FORWARD_USER.format(
            FROM_USER_ID=forward_from.id,
            FROM_FULL_NAME=forward_from.full_name,
            FROM=entity_from,
        )

    return entity_from


def _get_media(message: TMessage, caption: str):
    if message.animation:
        return InputMediaAnimation(media=message.animation, caption=caption)
    if message.audio:
        return InputMediaAudio(media=message.audio, caption=caption)
    if message.document:
        return InputMediaDocument(media=message.document, caption=caption)
    if message.photo:
        return InputMediaPhoto(media=message.photo[-1], caption=caption)
    if message.video:
        return InputMediaVideo(media=message.video, caption=caption)


def _get_quotable(message: TMessage, from_tag: str):
    caption, captionable = _validate_caption(message)
    text, send_from = message.text_html_urled, True
    tag_len = len(dehtml(from_tag))

    if not from_tag.strip():
        return text, caption, False

    if message.text and (tag_len + len(message.text) < MessageLimit.MAX_TEXT_LENGTH):
        text = f"{from_tag}{text}"
        send_from = False
    elif captionable and (tag_len + len(message.caption) < MessageLimit.CAPTION_LENGTH):
        caption = f"{from_tag}{caption}"
        send_from = False

    return text, caption, send_from


def _validate_caption(message: TMessage):
    if (
        message.animation
        or message.audio
        or message.document
        or message.photo
        or message.video
        or message.voice
    ):
        caption = message.caption_html_urled if message.caption else ""
        return caption, True

    return "", False


async def send_edited_message(
    bot: Bot, message: TMessage, dest_message_id: int, chat_id: int, quote: bool
):
    """Edit the message at destination message ID of given chat."""
    from_tag = (
        Message.ENTITY_FROM.format(
            USER_ID=message.from_user.id,
            FULL_NAME=message.from_user.full_name,
        )
        if quote
        else ""
    )
    text, caption, send_from = _get_quotable(message, from_tag)
    media = _get_media(message, caption)

    if caption:
        try:
            await bot.edit_message_caption(
                chat_id=chat_id, message_id=dest_message_id, caption=caption
            )
        except:
            pass

    if message.location:
        try:
            await bot.edit_message_live_location(
                chat_id=chat_id, message_id=dest_message_id, location=message.location
            )
        except:
            pass

    if media:
        try:
            await bot.edit_message_media(
                chat_id=chat_id, message_id=dest_message_id, media=media
            )
        except:
            pass

    if text:
        try:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=dest_message_id, text=text
            )
        except:
            pass

    if send_from:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=from_tag,
            reply_to_message_id=dest_message_id,
        )
        return msg.message_id


async def send_message(
    bot: Bot,
    message: TMessage,
    to_user: int,
    reply_to: int,
    anonymous: bool,
    quote: bool,
):
    """Send message to given user after proper quotation."""
    from_tag = _get_from_tag(message, quote) if not anonymous else ""
    text, caption, send_from = _get_quotable(message, from_tag)
    msg: TMessage = None
    msgs = []

    if text:
        msg = await bot.send_message(
            chat_id=to_user,
            text=text,
            reply_to_message_id=reply_to,
        )
    elif caption:
        msg = await message.copy(
            chat_id=to_user,
            caption=caption,
            reply_to_message_id=reply_to,
        )
    else:
        msg = await message.copy(
            chat_id=to_user,
            reply_to_message_id=reply_to,
        )

    msgs.append(msg.message_id)

    if send_from and not anonymous:
        omsg = await bot.send_message(
            chat_id=to_user,
            text=from_tag,
            reply_to_message_id=msg.message_id,
        )
        msgs.append(omsg.message_id)

    return msgs
