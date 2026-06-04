"""Contains the Server object."""

import asyncio
import logging

from telegram.constants import ParseMode
from telegram.ext import Application, Defaults

from Aashii.constants import Scope
from Aashii.utils.database import Database
from Aashii.utils.misc import error_handler


class Server:
    """Server takes care of setting up the bot, handlers and getting updates."""

    def __init__(
        self,
        token: str,
        commands: dict,
        database_url: str,
        handlers: dict,
    ):
        defaults = Defaults(
            parse_mode=ParseMode.HTML,
            allow_sending_without_reply=True,
        )

        self.application = Application.builder().token(token).defaults(defaults).build()

        self.database = Database(database_url)

        self.application.bot_data["database"] = self.database

        self._setup_handlers(handlers)

        self.commands = commands

        self.application.post_init = self._post_init
        self.application.post_shutdown = self._post_shutdown

    async def _post_init(self, application: Application):
        """Run after application startup."""

        admins = self.commands["admins"] + self.commands["all"]
        private = self.commands["private"] + self.commands["all"]

        await application.bot.set_my_commands(
            admins,
            scope=Scope.ADMINS,
        )

        await application.bot.set_my_commands(
            private,
            scope=Scope.PRIVATE,
        )

    async def _post_shutdown(self, application: Application):
        """Clean up resources."""

        try:
            del self.database
        except Exception:
            pass

        logging.info("Got an interruption, bye.")

    def _setup_handlers(self, handlers: dict):

        for handler_type, handles in handlers.items():
            for handle in handles:
                h_kwargs, d_args = handle[0], handle[1:]
                print("REGISTERING", h_kwargs.get("callback"))
                handler = handler_type(**h_kwargs)

                self.application.add_handler(
                    handler,
                    *d_args,
                )

        self.application.add_error_handler(error_handler)

    def listen(
        self,
        listen: str,
        port: int,
        url: str,
        url_path: str,
    ):
        """Listen for incoming webhook updates."""

        self.application.run_webhook(
            listen=listen,
            port=port,
            url_path=url_path,
            webhook_url=f"{url}/{url_path}",
            allowed_updates=[
                "callback_query",
                "chat_join_request",
                "edited_message",
                "message",
            ],
        )

    def poll(self, poll_interval: int = 0):
        """Poll for incoming updates."""

        self.application.run_polling(
            poll_interval=poll_interval,
            allowed_updates=[
                "callback_query",
                "chat_join_request",
                "edited_message",
                "message",
            ],
        )

    def signal_handler(self, *_):
        """Backward compatibility stub."""
        logging.info("Signal received.")
