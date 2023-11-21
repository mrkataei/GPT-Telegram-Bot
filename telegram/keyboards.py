from telegram import *
from models.subscribe import Subscribe


def start_keyboard() -> ReplyKeyboardMarkup:
    key_markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    key_contact = KeyboardButton(trans("C_contact"))
    key_help = KeyboardButton(trans("C_Help"))
    key_profile = KeyboardButton(trans("C_profile_status"))
    key_invite = KeyboardButton(trans("C_invite_code"))
    key_transcript = KeyboardButton(trans("C_Transcript"))
    key_translate = KeyboardButton(trans("C_translation"))
    key_buy_token = KeyboardButton(trans("C_buy_token"))
    key_ocr = KeyboardButton(trans("C_OCR"))
    summarize_key = KeyboardButton(trans("C_summarize"))
    tariff_key = KeyboardButton(trans("C_billings"))
    exchange_key = KeyboardButton(trans("C_exchange"))
    picture = KeyboardButton(trans("C_generate_picture"))
    
    key_markup.row(summarize_key, key_translate, key_transcript)
    key_markup.row(key_profile)
    key_markup.row(key_invite, key_buy_token, exchange_key)
    key_markup.row(key_ocr, picture)
    key_markup.row(key_contact, key_help, tariff_key)
    
    return key_markup


def backhome_keyboard() -> ReplyKeyboardMarkup:
    key_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    key_back = KeyboardButton(trans("C_backhome"))

    key_markup.add(key_back)
    return key_markup


def social_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text=trans("S_telegram"),
                                            url='https://t.me/mrkatae'),
                InlineKeyboardButton(text=trans("S_github"),
                                            url='https://github.com/mrkataei/'),
                InlineKeyboardButton(text=trans("S_website"),
                                            url='https://mrkatae.ir'))
    return keyboard


def join_keyboard(channels: List[Subscribe]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=len(channels) % 3)
    for channel in channels:
        channel_id = str(channel.channel_id)[1:]
        keyboard.add(InlineKeyboardButton(text=channel_id,
                                            url=f'https://t.me/{channel_id}'))
    keyboard.add(InlineKeyboardButton(text=trans("M_joined"),
                 url='https://telegram.me/GPT_fa_bot?start=hi'))
    return keyboard


def language_keyboard() -> InlineKeyboardMarkup:
    lang_option = InlineKeyboardMarkup(row_width=3)
    lang_option.add(InlineKeyboardButton("فارسی 🇮🇷", callback_data='summarize_perisan'),
                    InlineKeyboardButton("English 🇺🇸", callback_data='summarize_english'),
                    InlineKeyboardButton("Germany 🇩🇪", callback_data='summarize_germany'),
                    InlineKeyboardButton("Russian 🇷🇺", callback_data='summarize_russian'),
                    InlineKeyboardButton("French 🇫🇷", callback_data='summarize_french'),
                    InlineKeyboardButton("Turkey 🇹🇷", callback_data='summarize_turkey'),
                    InlineKeyboardButton("Spanish 🇪🇸", callback_data='summarize_spanish')
                    )
    
    return lang_option

def pay_keyboard(url: str, amount_rial: int, authority: str, amount_token: int, code: str) -> InlineKeyboardMarkup:
    pay_option = InlineKeyboardMarkup(row_width=1)
    pay_option.add(InlineKeyboardButton(trans("M_pay"), url=url),
                                       InlineKeyboardButton("پرداخت کردم",
                                                            callback_data=f"payed_{amount_rial}_{authority}_{amount_token}_{code}"))
    return pay_option