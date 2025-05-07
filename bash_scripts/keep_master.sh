#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <master-branch-name>"
  exit 1
fi

MASTER_BRANCH_NAME=$1

if ! git show-ref --verify --quiet "refs/heads/$MASTER_BRANCH_NAME"; then
  echo "Error: Branch '$MASTER_BRANCH_NAME' does not exist."
  exit 1
fi

git branch | grep -v "$MASTER_BRANCH_NAME" | xargs git branch -d
