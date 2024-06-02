#!/bin/bash

commands=(
  #"who",
  "echo \"hello world\" > example.txt"
  "touch file.txt"
  "ls"
  "rm file.txt"
  "chmod 755 ~/example.txt"
  "mkdir ~/newdir"
  "rmdir ~/newdir"
  "cp ~/example.txt ~/ex2.txt"
  "mv ~/example.txt ~/example-moved.txt"
  "cat ~/example-moved.txt"
  "ln -s ~/example-moved.txt ~/example-symlink.txt"
  "sudo chown professor ~/example-moved.txt"
  "find . -wholename ./ex2.txt"
  "tar -czvf archive.tar.gz example-moved.txt"
  "tar -xvzf archive.tar.gz"
  "grep \"hello\" ~/example-moved.txt"
  # Add more commands as needed
)

REMOTE_USER="professor"
REMOTE_HOST="34.168.21.229"
LOG_FILE="command_log.txt"
PRIVATE_KEY="id_rsa_professor"

execute_remote_command() {
  local command=$1
  ssh -i ~/.ssh/${PRIVATE_KEY} ${REMOTE_USER}@${REMOTE_HOST} "${command}"
}

log_command() {
  local command=$3
  local return_value=$2
  echo "Command: ${command}" >>${LOG_FILE}
  echo "Return Value: ${return_value}" >>${LOG_FILE}
  echo "----------------------" >>${LOG_FILE}
}

for cmd in "${commands[@]}"; do
  echo "Executing: $cmd"
  time sleep 30
  execute_remote_command "$cmd"
  time sleep 45

  #  python_return_value=$(python genai_agent.py --time-range 5)
  #  log_command "python genai_agent.py --time-range 5" "${python_return_value}"

  python_return_value=$(python genai_agent.py --time-range 75)
  log_command "python ../llm-agent/genai_agent.py --time-range 75" "${python_return_value}" "${cmd}"

  # time sleep 30 
done
