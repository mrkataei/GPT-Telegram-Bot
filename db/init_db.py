from sqlalchemy.exc import OperationalError
from crud.user import user as curdUser
from crud.subscribe import subscribe as crudSubscribe
from schema.user import UserCreate
from schema.subscribe import SubscribeCreate
from dotenv import load_dotenv
import os
from db.session import SessionLocal

load_dotenv()

FIRST_SUPERUSER_CHAT_ID = str(os.getenv("FIRST_SUPERUSER_CHAT_ID"))
FIRST_SUPERUSER_USERNAME = str(os.getenv("FIRST_SUPERUSER_USERNAME"))
FIRST_SUPERUSER_FIRST_NAME = str(os.getenv("FIRST_SUPERUSER_FIRST_NAME"))
FIRST_SUPERUSER_LIMIT = 20
CHANNELS = ['@Gpt4Persian']  # @mrkataei for example


def init_db() -> None:
    try:
        session = SessionLocal()
        user = curdUser.get_by_chat_id(
            db=session, chat_id=FIRST_SUPERUSER_CHAT_ID)
        if not user:
            user_in = UserCreate(
                chat_id=FIRST_SUPERUSER_CHAT_ID,
                first_name=FIRST_SUPERUSER_FIRST_NAME,
                username=FIRST_SUPERUSER_USERNAME,
                limit=FIRST_SUPERUSER_LIMIT

            )

            user = curdUser.create(session, obj_in=user_in)

        channel_create_list = []
        for channel in CHANNELS:
            if not crudSubscribe.get(db=session, channel_id=channel):
                channel_create_list.append(SubscribeCreate(channel_id=channel))
        crudSubscribe.create_multi(db=session, obj_in=channel_create_list)
    except OperationalError as e:
        pass
