#!/bin/bash

# Set the process name
process="main.py"

# Colors for logging
green="\033[32m"
red="\033[31m"
yellow="\033[33m"
reset="\033[0m"

# Get the PID of the process if it's running
pid=$(pgrep -f "$process")

if [ -z "$pid" ]; then
  echo -e "${yellow}Process not running: $process${reset}"
else
  # Terminate the process
  echo -e "${red}Terminating process: $process (PID: $pid)${reset}"
  kill "$pid"
fi

# Launch the process
echo -e "${green}Starting process: $process${reset}"
nohup python3 $process > output.log &