# Commit-msg
- Currently, the script simply Prefixes the commit message with a ticket number
- The ticket number regex pattern should be updated to match your ticket number format
- Simply add it to .git/hooks/commit-msg of your git repo

# keep_master.sh
Deletes all local branches in a git repository except the one you provide (e.g **main** or **master**)
