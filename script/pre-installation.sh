#!/bin/bash

# Define colors for output messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print success messages in green
function print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Function to print error messages in red
function print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Exit immediately if a command exits with a non-zero status
set -e

# Get the script's current directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Navigate to the parent directory
cd "$SCRIPT_DIR/.." || { print_error "Failed to navigate to parent directory"; exit 1; }

# Access the previous directory
REPO_DIR=$(pwd)

# Load environment variables from .env file 
if ! source "$REPO_DIR/.env"; then
    print_error "Failed to load environment variables from .env file"
    exit 1
fi

# Make the run.sh and backup.sh scripts executable
if ! chmod +x "$REPO_DIR/run.sh" "$REPO_DIR/script/backup.sh"; then
    print_error "Failed to make scripts executable"
    exit 1
fi

# Update and upgrade system packages
if ! sudo -- sh -c 'apt-get update; apt-get upgrade -y; apt-get full-upgrade -y; apt-get autoremove -y; apt-get autoclean -y'; then
    print_error "Failed to update system packages"
    exit 1
fi
print_success "System packages updated successfully"

# Install necessary packages
if ! sudo apt-get install -y python3-distutils jq postgresql postgresql-contrib ffmpeg tesseract-ocr; then
    print_error "Failed to install necessary packages"
    exit 1
fi
print_success "Necessary packages installed successfully"

# Add tesseract-ocr to system path
if ! export PATH="/path/to/tesseract:$PATH"; then
    print_error "Failed to add tesseract-ocr to system path"
    exit 1
fi
print_success "tesseract-ocr added to system path successfully"

# Download and install latest version of pip package
if ! wget https://bootstrap.pypa.io/get-pip.py && sudo python3 get-pip.py; then
    print_error "Failed to download or install pip package"
    exit 1
fi
print_success "Pip package downloaded and installed successfully"

# Upgrade PyOpenSSL package
if ! python3 -m pip install pyopenssl --upgrade; then
    print_error "Failed to upgrade PyOpenSSL package"
    exit 1
fi
print_success "PyOpenSSL package upgraded successfully"

# Install python packages from requirements.txt file
if ! python3 -m pip install -r "$REPO_DIR/requirements.txt"; then
    print_error "Failed to install Python packages from requirements.txt file"
    exit 1
fi
print_success "Python packages installed successfully"

# Exit successfully
exit 0
