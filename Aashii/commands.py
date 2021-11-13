"""Contains commands used by the bot."""

from telegram import BotCommand
from Aashii.utils.misc import dehtml


def _command(fname):
    cmd = fname
    with open(f"data/static/{fname}", "r") as staticfp:
        dsc = dehtml(staticfp.read(80)) + "…"
    return BotCommand(cmd, dsc)


commands = {
    "admins": [
        BotCommand("announce", "Announce all users"),
        BotCommand("block", "Block the user"),
        BotCommand("cancel", "Cancel the announcement"),
        BotCommand("delete", "Delete the message of admin"),
        BotCommand("reset", "Reset the invite links count"),
        BotCommand("unblock", "Unblock the user"),
        BotCommand("whois", "Get the details of replied user"),
    ],
    "all": [
        BotCommand("help", "Help on usage"),
        BotCommand("start", "Start the adventure"),
    ],
    "private": [
        ("invite", "Request to join A GRoUP Of eBooKz®"),
        ("query", "General queries, appeals etc"),
    ],  # FIXME: Keep it hardcoded? [_command(fname) for fname in os.listdir("data/static")],
}
