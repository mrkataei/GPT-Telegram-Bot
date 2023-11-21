# ChatGPT

An Iranian telegram bot for ChatGPT

## Services that we provide

- Chat bot OpenAI API
- Transcript music and voices {mp3, mp4, mpeg, mpga, m4a, wav, or webm, ogg}
- Translation to English music and voices {mp3, mp4, mpeg, mpga, m4a, wav, or webm, ogg}
- PDF to Word (.docx) with OCR
- Buy token(In-App purchases unit coin)
- User account provide with panel
- Invite link with bonus

### Install

On your server run

`bash pre-installation.sh`

Wait until the update and postgress installation.

### Alembic

If you do not have any backup of your database start migrations and create tables with this comands

#### First step

change sqlalchemy link in alelbic.ini

sqlalchemy.url = postgresql://USER:PASSWORD@HOST/DATABASE

#### Second step

(create migration folder and initial it if you not found any folder like this in your Rep)
` alembic init migrations`

```alembic
alembic revision --autogenerate -m "create usermodel"
alembic upgrade heads
```

### Backup Store and Restore

sign in your postgres user and create daatabase

```
sudo su postgres
psql
createdb chatgpt
\q
```

#### Restore database

`psql -U postgres chatgpt < backup_file.sql`

#### Store and backup database

This will backup database and store it in /backup/ and push it to the git

`sudo ./scripts/backup.sh`

#### Changing postgres password

```
sudo su postgres
psql
\password postgres
```

### Run

Remember you need change global variables in .env(like: Telegram Token, OpenAI token)

`bash sudo run.sh`

#### Some commands I needed

```
ps ax | grep main
nohup python3 main.py > output.log &
celery -A tasks worker --loglevel=INFO
update "user" set token = "limit" - "requests";
ALTER USER user_name WITH PASSWORD 'new_password';
select \* from "user" ORDER BY signup_date DESC;
update "user" set token = "limit" - "requests";
truncate alembic_version

```
