#!/bin/bash

commands=(
  "vim ~/example.txt"
  # Add more commands as needed
)

REMOTE_USER="username"
REMOTE_HOST="server_ip_or_hostname"
LOG_FILE="command_log.txt"

execute_remote_command() {
  local command=$1
  ssh ${REMOTE_USER}@${REMOTE_HOST} "${command}"
}

log_command() {
  local command=$1
  local return_value=$2
  echo "Command: ${command}" >>${LOG_FILE}
  echo "Return Value: ${return_value}" >>${LOG_FILE}
  echo "----------------------" >>${LOG_FILE}
}

for cmd in "${commands[@]}"; do
  echo "Executing: $cmd"
  execute_remote_command "$cmd"
  time sleep 5

  #  python_return_value=$(python genai_agent.py --time-range 5)
  #  log_command "python genai_agent.py --time-range 5" "${python_return_value}"

  python_return_value=$(python openai_agent.py --time-range 5)
  log_command "python openai_agent.py --time-range 5" "${python_return_value}"

  time sleep 30 # Set enough time
done
