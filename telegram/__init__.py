import os
import logging
import random
import openai
from telebot import TeleBot, util, apihelper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from typing import Tuple, List, Dict
from datetime import datetime
from .definitions import trans
from .keyboards import start_keyboard, backhome_keyboard, social_keyboard, join_keyboard, language_keyboard, pay_keyboard

logger = logging.getLogger("chatgpt")

DEBUG = (os.getenv('DEBUG', 'False') == 'True')

TEST_BOT_TOKEN = os.getenv("TEST_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = TEST_BOT_TOKEN if DEBUG else BOT_TOKEN
MODEL = os.getenv("MODEL")

MESSAGE_SIZE_LIMIT = int(os.getenv("MESSAGE_SIZE_LIMIT"))
FILE_SIZE_LIMIT = int(os.getenv("FILE_SIZE_LIMIT"))
PDF_SIZE_LIMIT = int(os.getenv("PDF_SIZE_LIMIT"))
THREAD_MESSAGE_LIMIT = int(os.getenv("THREAD_MESSAGE_LIMIT"))

CHAT_VALUE = int(os.getenv("CHAT_VALUE"))
AUDIO_VALUE = int(os.getenv("AUDIO_VALUE"))
DOC_VALUE = int(os.getenv("DOC_VALUE"))
REPLY_VALUE = int(os.getenv("REPLY_VALUE"))
SUMMARIZE_VALUE = int(os.getenv("SUMMARIZE_VALUE"))
PIC_VALUE = int(os.getenv("PIC_VALUE"))


CHAT_SCORE = int(os.getenv("CHAT_SCORE"))
AUDIO_SCORE = int(os.getenv("AUDIO_SCORE"))
PIC_SCORE = int(os.getenv("PIC_SCORE"))
SUMMARIZE_SCORE = int(os.getenv("SUMMARIZE_SCORE"))
PURCHASE_PER_TOKEN_SCORE = int(os.getenv("PURCHASE_PER_TOKEN_SCORE"))
EXCHANGE_SCORE = int(os.getenv("EXCHANGE_SCORE"))

TOKEN_REWARD = int(os.getenv("TOKEN_REWARD"))

START_KEYBOARD = start_keyboard()
SOCIAL_KEYBOARD = social_keyboard()
BACKHOME_KEYBOARD = backhome_keyboard()
LANGUAGE_KEYBOARD = language_keyboard()


TOKEN_PRICE = int(os.getenv("TOKEN_PRICE"))
PAY_LIMIT = int(os.getenv("PAY_LIMIT"))

BONUS = int(os.getenv("BONUS"))
