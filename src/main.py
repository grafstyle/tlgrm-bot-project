from telegram.ext._updater import Updater
from telegram._update import Update
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext._handlers.commandhandler import CommandHandler
from telegram.ext._handlers.messagehandler import MessageHandler
from dotenv import load_dotenv
import os

load_dotenv()
bottoken = os.getenv("BOT_TOKEN")

updater = Updater(bottoken, use_context=True)
print(bottoken)