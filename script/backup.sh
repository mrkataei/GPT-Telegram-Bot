#!/bin/bash

# Set the colors for error and success messages
ERROR_COLOR="\033[31m"
SUCCESS_COLOR="\033[32m"
RESET_COLOR="\033[0m"
INFO_COLOR="\033[36m"

# Get the script's current directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Navigate to the parent directory
cd "$SCRIPT_DIR/.."

# Access the previous directory
REPO_DIR=$(pwd)
BACKUP_DIR="$REPO_DIR/backup"
GIT_DIR=$REPO_DIR

# Load environment variables from .env file 
source "$REPO_DIR/.env"

# Check required variables are set
if [[ -z $DB_NAME || -z $DB_USERNAME || -z $DB_PASSWORD || -z $DB_HOST ]]; then
  echo -e "${ERROR_COLOR}Error: Required database credentials not set in .env file.${RESET_COLOR}"
  exit 1
fi

# Set the PGPASSWORD environment variable
export PGPASSWORD="$DB_PASSWORD"

# Define backup file name with timestamp
BACKUP_FILENAME="$REPO_DIR/backup/backup_$(date '+%Y%m').sql"

# Run pg_dump command to create backup
if ! pg_dump -U $DB_USERNAME -d $DB_NAME -h "$DB_HOST" -f $BACKUP_FILENAME; then
  echo -e "${ERROR_COLOR}Error creating PostgreSQL backup. Exiting...${RESET_COLOR}"
  exit 1
fi

# Check if the pg_dump command was successful
if [ $? -eq 0 ]; then
  echo -e "${SUCCESS_COLOR}PostgreSQL backup created successfully: $BACKUP_FILENAME${RESET_COLOR}"
else
  echo -e "${ERROR_COLOR}Error creating PostgreSQL backup. Exiting...${RESET_COLOR}"
  exit 1
fi

# initialize the git repository if it doesn't exist
if [ ! -d $GIT_DIR/.git ]; then
    git init $GIT_DIR
    if ! git -C $GIT_DIR remote add origin $GIT_REPO; then
    echo -e "${ERROR_COLOR}Error adding Git remote repository. Exiting...${RESET_COLOR}"
    exit 1
  fi
fi

# add the backup file to the git repository
if ! git -C $GIT_DIR add $BACKUP_FILENAME; then
  echo -e "${ERROR_COLOR}Error adding backup file to Git repository. Exiting...${RESET_COLOR}"
  exit 1
fi

# commit the backup file
if ! git -C $GIT_DIR commit -m "Backup for $(date +%Y%m%d)"; then
  echo -e "${ERROR_COLOR}Error committing backup file to Git repository. Exiting...${RESET_COLOR}"
  exit 1
else
  echo -e "${INFO_COLOR}committing backup file to Git repository..."
fi

# push the changes to the remote repository
if ! git -C $GIT_DIR push origin $GIT_BRANCH; then
  echo -e "${ERROR_COLOR}Error pushing backup file to Git remote repository. Exiting...${RESET_COLOR}"
  exit 1
else
  echo -e "${SUCCESS_COLOR}Backup pushed to Git remote repository successfully."
fi
