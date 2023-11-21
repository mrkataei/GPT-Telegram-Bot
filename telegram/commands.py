from telegram import *

from time import sleep
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session

from crud.message import message as crudMessage
from crud.user import user as crudUser
from schema.message import MessageCreate
from models.message import Message
from models.openai import StatusEnum
from .utils import send_waiting_action, ocr, read_docx, convert_ogg_to_mp3, delete_extra_file, change_api_status

pool = ThreadPoolExecutor(4)
bot = TeleBot(BOT_TOKEN)


def is_over_size(file_size: int, limit: int, chat_id: str) -> bool:
    MB = 1000000
    if file_size > limit:
        bot.send_message(chat_id, trans("M_out_of_size").format(size=limit/MB))
        return True
    else:
        return False


def chat_handler(message: dict, db: Session, user_messages: List[Message] = None) -> bool:
    try:
        content = message.text
        if len(str(content).split()) > MESSAGE_SIZE_LIMIT:
            bot.send_message(message.chat.id,
                             trans("M_out_of_size_message"),
                             reply_markup=START_KEYBOARD)
            return False
        value = REPLY_VALUE if user_messages else CHAT_VALUE
        bot.send_message(message.chat.id, trans("M_waiting").format(token=value,
                                                                    score=CHAT_SCORE),
                         parse_mode="MarkdownV2")
        bot.send_chat_action(chat_id=message.chat.id, action="typing")
        sleep(3)

        if user_messages is None:
            try:
                completion = openai.ChatCompletion.create(
                    model=MODEL, messages=[{"role": "user", "content": content}])

            except openai.OpenAIError as e:
                if "Rate limit" in str(e):
                    logger.warning(
                    f"{datetime.now()}: chat handler single message {message.chat.id}. error is : API rate limit exceeded.")
                    change_api_status(db=db, api=openai.api_key, status=StatusEnum.PENDING)
                
                elif "billing" in str(e) or "exceeded" in str(e):
                    logger.info(
                        f"{datetime.now()}: chat handler single message {message.chat.id}. error is :Billing hard limit has been reached")
                    change_api_status(db=db, api=openai.api_key, status=StatusEnum.INACTIVE) 
                
                return False
            
            message_id = message.message_id
        else:
            if len(user_messages) > THREAD_MESSAGE_LIMIT :
                bot.send_message(message.chat.id, trans("M_out_of_thread_message_number"),
                                 reply_markup=START_KEYBOARD)
                return False

            final_message = []
            for ms in user_messages:
                final_message.append({"role": ms.role, "content": ms.text})
                message_id = ms.message_id
            final_message.append({"role": "user", "content": content})
            try:
                completion = openai.ChatCompletion.create(
                    model=MODEL, messages=final_message)

            except openai.OpenAIError as e:
                
                if "Rate limit" in str(e):
                    logger.warning(
                        f"{datetime.now()}: chat handler multiple messages {message.chat.id}. error is : API rate limit exceeded.")
                    change_api_status(db=db, api=openai.api_key, status=StatusEnum.PENDING)
                    
                elif "billing" in str(e) or "exceeded" in str(e):
                    logger.info(
                        f"{datetime.now()}: chat handler single message {message.chat.id}. error is :Billing hard limit has been reached")
                    change_api_status(db=db, api=openai.api_key, status=StatusEnum.INACTIVE) 
                
                return False

        assistance_text = completion.choices[0].message.content
        splitted_text = pool.submit(util.split_string,
                                    assistance_text,
                                    2000).result()

        messages = [
            MessageCreate(chat_id=str(message.chat.id),
                          message_id=message_id, text=content, role='user'),
            MessageCreate(chat_id=str(message.chat.id),
                          message_id=message_id, text=assistance_text, role='assistant')
        ]
        crudMessage.create_multi(db=db, obj_in=messages)

        reply_option = InlineKeyboardMarkup(row_width=1)
        reply_option.add(InlineKeyboardButton("پاسخ",
                                              callback_data=f'reply_{message_id}'))

        for text in splitted_text:
            try:
                bot.send_message(message.chat.id,
                                 text, reply_to_message_id=message_id,
                                 reply_markup=reply_option)
            except Exception as f:
                logger.warning(
                    f"{datetime.now()}: chat handler send response for user {message.chat.id}, warning is :\n{e}")
                bot.send_message(message.chat.id, text,
                                 reply_markup=reply_option)

    except Exception as e:
        error_message = f"""
        {datetime.now()}: chat handler for user {message.chat.id},
        and message {content}. error is :\n{e}
        """
        logger.error(error_message)
        return False
    return True


def send_message_to_all(message: str, db: Session) -> None:
    users = crudUser.get_multi(db=db, limit=-1)
    for user in users:
        try:
            bot.send_message(chat_id=user.chat_id, text=message)
        except Exception as e:
            # logger.warning(f'send message to all -> {e}')
            pass


def generate_picture(db: Session, prompt: str, chat_id: int) -> bool:
    try:
        response_text = pool.submit(openai.Image.create,
                                    prompt=prompt, n=1,
                                    size="256x256").result()
        url = response_text['data'][0]['url']
        bot.send_photo(chat_id=chat_id, photo=url)
        return True
    except openai.OpenAIError as e:
        if "Rate limit" in str(e):
            error_message = f"""
                {datetime.now()}: generate_picture {chat_id}. error is : API rate limit exceeded.
                """
            logger.warning(error_message)
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.PENDING)
            
        elif "billing" in str(e) or "exceeded" in str(e):
            logger.info(
                        f"{datetime.now()}: generate_picture {chat_id}. error is :Billing hard limit has been reached")
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.INACTIVE)        
        
        return False

    except Exception as e:
        logger.error(f"{datetime.now()}:  send photo {chat_id}. error is :{e}")
        return False


def submit_prompt(db: Session, prompt: str, chat_id: str) -> bool:
    try:
        completion = openai.ChatCompletion.create(model=MODEL,
                                                  messages=[{"role": "user", "content": prompt}])
        assistance_text = completion.choices[0].message.content
        bot.send_message(chat_id, assistance_text, reply_markup=START_KEYBOARD)
        return True

    except openai.OpenAIError as e:
        if "Rate limit" in str(e):
            logger.warning(
                f"{datetime.now()}: submit_prompt {chat_id}. error is : API rate limit exceeded.")
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.PENDING)
            
        elif "billing" in str(e) or "exceeded" in str(e):
            logger.info(
                        f"{datetime.now()}: submit_prompt {chat_id}. error is :Billing hard limit has been reached")
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.INACTIVE) 
        
        return False


def PDF_to_word(message: Dict, doc_path: str) -> bool:
    chat_id = str(message.chat.id)
    content = message.content_type

    if content == 'document':
        fileID = message.document.file_id
        file_name = message.document.file_name

        if is_over_size(file_size=message.document.file_size, limit=PDF_SIZE_LIMIT, chat_id=chat_id):
            return False

        if not str(file_name).endswith(".pdf"):
            bot.send_message(chat_id, trans("M_invalid_format"),
                             reply_markup=START_KEYBOARD)
            return False
    else:
        bot.send_message(chat_id, trans("M_invalid_format"),
                         reply_markup=START_KEYBOARD)
        return False

    send_waiting_action(chat_id=chat_id, token_usage=DOC_VALUE,
                        score=0, action='upload_document')
    file_path = f'{doc_path}{chat_id}-{file_name}'
    file_info = bot.get_file(fileID)
    pdf_file = bot.download_file(file_info.file_path)
    try:
        with open(file_path, 'wb') as f:
            f.write(pdf_file)
    except Exception as e:
        logger.error(
            f"{datetime.now()}: opening file for pdf to word error is {e}")
        return False

    return True if ocr(file_path=file_path, chat_id=chat_id) else False


def transcript_translate(db:Session, message: Dict, doc_path: str, transcript: bool = True) -> bool:
    chat_id = str(message.chat.id)
    content = message.content_type

    if content == 'audio':
        fileID = message.audio.file_id
        file_name = message.audio.file_name
        file_size = message.audio.file_size

    elif content == 'voice':
        fileID = message.voice.file_id
        file_name = f"voice_{chat_id}.ogg"
        file_size = message.voice.file_size

    else:
        bot.send_message(chat_id, trans("M_invalid_format"),
                         reply_markup=START_KEYBOARD)
        return False

    if is_over_size(file_size=file_size, limit=FILE_SIZE_LIMIT, chat_id=chat_id):
        return False

    file_path = f'{doc_path}{chat_id}-{file_name}'
    file_info = bot.get_file(fileID)
    audio_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as f:
        f.write(audio_file)

    if str(file_name).endswith(".ogg"):
        file_path = convert_ogg_to_mp3(path_ogg=file_path)
        if file_path is None:
            bot.send_message(chat_id, trans("M_something_wrong"),
                             reply_markup=START_KEYBOARD)
            return False

    try:
        audio_file = open(file_path, "rb")
        send_waiting_action(
            chat_id=chat_id, token_usage=AUDIO_VALUE, score=AUDIO_SCORE)
        response = openai.Audio.transcribe("whisper-1",
                                           audio_file) if transcript else openai.Audio.translate("whisper-1",
                                                                                                 audio_file)
        splitted_text = util.split_string(response.text, 2000)
        for text in splitted_text:
            bot.send_message(
                chat_id, text, reply_to_message_id=message.message_id)
            delete_extra_file(path=file_path)
        return True

    except openai.OpenAIError as e:
        if "Rate limit" in str(e):
            error_message = f"""
            {datetime.now()}: Create_transcription_step_1, is as transcript {transcript} for user {chat_id},
            and file name is {file_name}. error is :\n{e}"""
            logger.warning(error_message)
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.PENDING)
            
        elif "billing" in str(e) or "exceeded" in str(e):
            logger.info(
                        f"{datetime.now()}: Create_transcription_step_1 {chat_id}. error is :Billing hard limit has been reached")
            change_api_status(db=db, api=openai.api_key, status=StatusEnum.INACTIVE) 
        
        bot.send_message(chat_id, trans("M_bot_to_busy"),
                            reply_markup=START_KEYBOARD)
        delete_extra_file(path=file_path)
        return False
    
    except Exception as e:
        logger.error(
            f"{datetime.now()}: transcript or translate error chat_id is {chat_id} and error is {e}")
        return False


def docx_translate(db: Session, message: Dict, doc_path: str) -> bool:

    chat_id = str(message.chat.id)
    fileID = message.document.file_id
    file_name = message.document.file_name

    if message.document.file_size > PDF_SIZE_LIMIT:
        bot.send_message(chat_id, trans("M_out_of_size").format(
            size=PDF_SIZE_LIMIT/1000000))
        return False

    if not str(file_name).endswith(".docx"):
        bot.send_message(chat_id, trans("M_invalid_format"),
                         reply_markup=START_KEYBOARD)
        return False

    bot.send_message(chat_id, trans("M_waiting").format(
        token=AUDIO_VALUE, score=AUDIO_SCORE), parse_mode="MarkdownV2")
    file_path = f'{doc_path}{chat_id}-{file_name}'
    file_info = bot.get_file(fileID)
    docx_file = bot.download_file(file_info.file_path)

    try:
        with open(file_path, 'wb') as f:
            f.write(docx_file)
    except Exception as e:
        logger.error(
            f"{datetime.now()}: opening file for translate docx error is {e}")
        return False

    return pool.submit(read_docx, db=db, file_path=file_path, chat_id=chat_id).result()
