#!/bin/bash

commands=(
  "who"
  # Add more commands as needed
)

REMOTE_USER="student"
REMOTE_HOST="35.247.20.4"
LOG_FILE="command_log.txt"
PRIVATE_KEY="id_rsa_student"

execute_remote_command() {
  local command=$1
  ssh -i ~/.ssh/${PRIVATE_KEY} ${REMOTE_USER}@${REMOTE_HOST} "${command}"
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
  log_command "python ../llm-agent/openai_agent.py --time-range 5" "${python_return_value}"

  time sleep 30 # Set enough time
done
