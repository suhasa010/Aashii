"""Contains Message object."""
from .label import Label


class Message:
    """Message contains text strings that is used in users interaction."""

    ADMIN_CONNECTED = (
        "<a href='tg://user?id={ADMIN_ID}'>{ADMIN_FULL_NAME}</a> "
        "has connected with "
        "<a href='tg://user?id={USER_ID}'>{USER_FULL_NAME}</a>"
    )

    ADMIN_CONNECTED_STATUS = (
        "<b>Voila, an admin has connected with you! 🤝</b>\n\n"
        "You can start talking now."
    )

    ALREADY_IN_GROUP = "You're already there in the request group"

    ANNOUNCEMENT_CANCELLED = (
        "Announcement cancelled in progress.\n"
        " • <b>Sent</b> : <code>{SENT}</code>\n"
        " • <b>Failed</b> : <code>{FAILED}</code>\n"
        " • <b>Progress</b> : <code>{PROGRESS}</code>%."
    )

    ANNOUNCEMENT_DONE = (
        "Announcement done.\n"
        " • <b>Sent</b> : <code>{SENT}</code>\n"
        " • <b>Failed</b> : <code>{FAILED}</code>\n"
        " • <b>Total</b> : <code>{TOTAL}</code>."
    )

    ANNOUNCEMENT_IN_DUE = (
        "There is already an announcement in due. "
        "Please /cancel it before starting new one."
    )

    ANNOUNCEMENT_INIT = (
        "An announcement has been initiated.\n"
        "<b>Audience</b> : <code>{TOTAL}</code> users."
    )

    ANNOUNCEMENT_PULSE = (
        "Announcement in due.\n"
        " • <b>Sent</b> : <code>{SENT}</code>\n"
        " • <b>Failed</b> : <code>{FAILED}</code>\n"
        " • <b>Progress</b> : <code>{PROGRESS}</code>%."
    )

    BLOCKED_USER = "<a href='tg://user?id={USER_ID}'>{FULL_NAME}</a> has been blocked successfully."

    BLOCKED_USER_STATUS = "Dang, you were blocked by an admin 🚫\n\n<b>Goodbye</b>"

    BLOCKED_BY_USER = "<a href='tg://user?id={USER_ID}'>{FULL_NAME}</a> has blocked me from contacting them."

    CANCELLED_ANNOUNCEMENT = (
        "Cancelled announcement at <code>{PROGRESS}</code>% progress."
    )

    CHAT_LINK_INFO = (
        "Clicking on the below link(within the next 2 mins) will allow you to place a request to join "
        "the group. <b>Your answers are auto-moderated and joining requests "
        "are automatically approved if they are deemed fit. If you don't "
        "answer them properly with all the details, don't expect to be "
        "admitted to the group.</b>\n\n"
        "<i>Note: If you're not on the newest version of Telegram, "
        "you won't be able to use the following link.</i>\n\n"
        "{LINK}"
    )

    DELETE_DONE = "Message deleted successfully!"

    DELETE_FAILED = "I can't delete that message …"

    ENTITY_FORWARD_ANONYMOUS = "<b>Forwarded from {SENDER_NAME}</b>\n{FROM}"

    ENTITY_FORWARD_CHAT = (
        "<b>Forwarded from <a href='tg://user?id={FROM_CHAT_ID}'>"
        "{FROM_CHAT_NAME}</a></b>\n"
        "{FROM}"
    )

    ENTITY_FORWARD_USER = "<b>Forwarded from <a href='tg://user?id={FROM_USER_ID}'>{FROM_FULL_NAME}</a></b>\n{FROM}"

    ENTITY_FROM = "<b><a href='tg://user?id={USER_ID}'>{FULL_NAME}</a></b>\n\n"

    ERROR = "Oops ! I faced an error : <code>{ERROR}</code>\n<code>{TRACEBACK}</code>"
    
    EXHAUSTED_INVITE_LINKS = (
        "You've already requested to join the group. "
        "Please be patient until your request is approved."
    )

    FALLBACK_STATUS = "Left"

    HELP_GROUP = (
        "Hey there ! It's <b>Aashii</b> here to help you "
        "in managing communication between members and admins.\n\n"
        "Since you are in <b>admins group</b>, the following commands are your exclusive.\n\n"
        " ⁃ /block - Blocks a user from contacting you.\n"
        " ⁃ /cancel - Cancels an announcement in progress.\n"
        " ⁃ /unblock - Unblocks a blocked user.\n\n"
        "All the above commands should be a reply to a message.\n"
        "For <code>block</code> and <code>unblock</code>, "
        "the replied message should be a forwarded message by me.\n\n"
        "My source code is available at https://github.com/j-arun-mani/Aashii\n"
        "Enjoy !"
    )

    HELP_PRIVATE = (
        "<b>Welcome to A GRoUP Of eBooKz® Support Bot 👋</b>\n\n"
        "Please note, that this bot is for contacting admins "
        "of <b>A GRoUP Of eBooKz®</b> Group\n\n"
        "Click /invite if you want to join the A GRoUP Of eBooKz® Group.\n\n"
        "<b>Do not request books through this bot!</b>\n"
        "press Menu button to find out the list of actions you can "
        "perform using the bot.\n\n"
        "As soon as an admin connects with you, you'll receive a notification."
    )

    INFORM_APPROVAL = (
        "Congratulations, you have been approved and added to "
        "<b>A GRoUP Of eBooKz® group</b>."
    )

    INFORM_DECLINE = (
        "Your request to join the group was declined due to "
        "various reasons. Try again after few months."
    )

    INVALID_COMMAND = "I don't understand what you are talking about …"

    INVALID_REPLY = "I expected this as a reply to a valid message."
    
    INVITE_LINKS_RESET = "You are now allowed to generate /invite links."

    JOIN_REQUEST = (
        "<b>Chat Join Request</b>\n"
        "Name : <a href='tg://user?id={USER_ID}'>{FULL_NAME}</a>\n"
        "Username : {USERNAME}\n"
        "User ID : <code>{USER_ID}</code>\n"
        "Blocked : {BLOCKED}\n\n"
    ) + Label.PENDING_REQUEST

    JOIN_REQUEST_APPROVED = (
        "#Approved by <a href='tg://user?id={USER_ID}'>{FULL_NAME}</a>"
    )

    JOIN_REQUEST_DECLINED = (
        "#Declined by <a href='tg://user?id={USER_ID}'>{FULL_NAME}</a>"
    )
    
    KICKED_IN_GROUP = (
        "You've been banned from the group. "
        "Hence you're not allowed to generate any invite links."
    )

    MUTED_IN_GROUP = (
        "You're already in the group but muted. If you want to get unmuted, "
        "reply to this message with your concern."
    )

    NO_ANNOUNCEMENT = "No announcement is in due to cancel."

    NOT_LINKED = "I don't think that message corresponds to any user."

    NOT_PRIVATE_COMMAND = "Sorry, this command is meant to be used in admins group."
    
    RESET_COUNT = "<a href='tg://user?id={USER_ID}'>{FULL_NAME}</a> invite links count has been reset."

    START_GROUP = "I'm all alive and functioning."

    START_PRIVATE = (
        "<b>Welcome to A GRoUP Of eBooKz® Support Bot 👋</b>\n\n"
        "Please note, that this bot is for contacting admins "
        "of <b>A GRoUP Of eBooKz®</b> Group\n\n"
        "Click /invite if you want to join the A GRoUP Of eBooKz® Group.\n\n"
        "<b>Do not request books through this bot!</b>\n"
        "press Menu button to find out the list of actions you can "
        "perform using the bot.\n\n"
        "As soon as an admin connects with you, you'll receive a notification."
    )

    UNBLOCKED_USER = (
        "<a href='tg://user?id={USER_ID}'>{FULL_NAME}</a> has been unblocked."
    )

    UNBLOCKED_USER_STATUS = "Congratulations! You were unblocked by an admin!"

    USER = (
        "Name : <a href='tg://user?id={USER_ID}'>{FULL_NAME}</a>\n"
        "Username : {USERNAME}\n"
        "User ID : <code>{USER_ID}</code>\n"
        "Membership : {MEMBERSHIP}\n"
        "Blocked : {BLOCKED}"
    )

    USER_CONNECTED = (
        "<a href='tg://user?id={USER_ID}'>{FULL_NAME}</a> has started the bot.\n"
        "Username : {USERNAME}\n"
        "User ID : <code>{USER_ID}</code>\n"
        "Membership : {MEMBERSHIP}\n"
        "Blocked : {BLOCKED}"
    )

    USER_NOT_FOUND = "I can't find the user in my database, something's wrong ..."
