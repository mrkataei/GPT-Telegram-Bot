# ChatGPT

GPT and AI Telegram bot 

## Services that we provide

- Chat bot OpenAI API
- Transcript music and voices {mp3, mp4, mpeg, mpga, m4a, wav, or webm, ogg}
- Translation to English music and voices {mp3, mp4, mpeg, mpga, m4a, wav, or webm, ogg}
- PDF to Word (.docx) with OCR
- Prompt to Image with OpenAI
- Buy token(In-App purchases unit coin)
- User account provide with panel
- Invite link with bonus
- Score System for buying tokens

## Install

On your server run

`bash pre-installation.sh`

Wait until the update and postgress installation.

### Alembic

If you do not have any backup of your database start migrations and create tables with this comands

#### First step

Fill all requirement variables  in .env 

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

#### Auto backup system 

Just add this line in your crontab file
 
Open your schedule file with 

```
crontab -e

```
Add this line with you desire time to automate your backup script

```
15 3 * * * /bin/bash /root/ChatGPT/script/backup.sh
```


## Telegram BOt

### Definitions 
we have big dicotionary for able to multilanguage bot 

### Admin Guide 

we have some command for administrator 

- /addapi "for add openai api"(you can provide many APIs thats usefull when some api break down another one working)
- /getapi "show all api with status" ***green(active) - red(deactivate) - yellow(pending)***

- /addoffer "add offer code for discount system" ***need duration days and discount persent***

- /charge "charge user token manually" ***needs user id(chat_id) and tokens needs***

- /message "send global message to all users" ***needs your message and you sign to send***


## Supprt me

[buy me a coffee](https://www.buymeacoffee.com/mrkataei)

