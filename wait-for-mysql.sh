#!/bin/bash

# Database params
host=$1
port=$2
user=$3
password=$4

timeout=20
start_time=$(date +%s)

# Wait until the database is ready
while :
do
  if mysql -h"$host" -P"$port" -u"$user" -p"$password" &> /dev/null
  then
    break
  fi

  # If timeout is reached, exit and execute the command anyway
  current_time=$(date +%s)
  if [ $(($current_time - $start_time)) -ge $timeout ]
  then
    echo "Timeout reached, executing command anyway..."
    break
  fi

  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Executing command"
exec $5