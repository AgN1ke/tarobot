# telegram_wrapper.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.update import Update


class TelegramWrapper:
    def __init__(self, token: str, message_callback=None):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.message_callback = message_callback
        self.setup_handlers()

    def setup_handlers(self):
        # Command handler for start command
        self.dispatcher.add_handler(CommandHandler('start', self.start))

        # Message handler for text messages
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id, "Hello, welcome to the TaroBot!")

    def handle_message(self, update: Update, context: CallbackContext):
        # Delegate the handling of the message to the provided callback
        if self.message_callback:
            chat_id = update.effective_chat.id
            message_text = update.message.text
            self.message_callback(chat_id, message_text)

    def send_message(self, chat_id: str, message: str):
        self.updater.bot.send_message(chat_id, message)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

