#!/bin/bash

current_branch=$(git rev-parse --abbrev-ref HEAD)
ticket_number_pattern='S[0-9]+-[0-9]+'
ticket_number=$(echo "$current_branch" | grep -oE "$ticket_number_pattern")

if [[ -n "$ticket_number" ]]; then
  commit_message=$(cat "$1")

  if [[ "$commit_message" != "$ticket_number"* ]]; then
    new_commit_message="$ticket_number: $commit_message"

    echo "$new_commit_message" > "$1"
    echo "* Added ticket number '$ticket_number' as a prefix to the commit message."
  else
    echo "* Commit message already contains the ticket number '$ticket_number'."
  fi
else
  echo "!!! No ticket number found in the branch name '$current_branch'. Commit message will not be modified."
fi

exit 0
