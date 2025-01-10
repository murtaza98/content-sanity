#!/bin/bash
set -e

# Description: This is the entrypoint for sanity checks.
#     Broadly, this script performs 2 checks:
#     1. UI based tests using Playwright. This is to simulate the end candidate experience.
#            Description:
#            - For UI tests, we download the test script from a repository.
#            - We then run the test script using Playwright.
#     2. Scoring tests. This ensures that the scoring module is working as expected.
# Input:
#   $1: Base64 encoded install command (optional)
#   $2: Base64 encoded score command
#   Note: We've encoded the commands to avoid any special character issues.
#   Example:
#       if the command has special chars like python3 -c 'print("hello world")'
#       then passing it as an argument will cause issues.
# Output:
#   - The output will be:
#       - The output of the UI tests (????)
#       - The output of the scoring tests (stdout or files)

PROJECT_DIRECTORY=$(pwd)

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 [install_command] score_command ide_url"
    echo "install_command is optional, but score_command and ide_url is mandatory."
    exit 1
fi

INSTALL_COMMAND=""
SCORE_COMMAND=""
IDE_URL=""

if [ "$#" -eq 3 ]; then
    INSTALL_COMMAND="$1"
    SCORE_COMMAND="$2"
    IDE_URL="$3"
else
    SCORE_COMMAND="$1"
    IDE_URL="$2"
fi

# base64 decode the command
INSTALL_COMMAND=$(echo $INSTALL_COMMAND | base64 -d)
SCORE_COMMAND=$(echo $SCORE_COMMAND | base64 -d)
IDE_URL=$(echo $IDE_URL | base64 -d)

##### START of UI tests #####
REPO_URL="https://github.com/murtaza98/content-sanity.git"  # Replace with the actual repo URL
CLONE_DIR="$HOME/$(basename "$REPO_URL" .git)"
VENV_NAME="venv"

git clone "$REPO_URL" "$CLONE_DIR"

cd "$CLONE_DIR"

python3 -m venv "$VENV_NAME"
source "$VENV_NAME/bin/activate"

pip install --upgrade pip
pip install -r requirements.txt
chmod +x post_setup.sh && ./post_setup.sh

# Save output to a file
python sanity_check.py "$IDE_URL" > /tmp/ui_output.txt

# Deactivate the virtual environment
deactivate

##### END of UI tests #####


##### START of Scoring tests #####

cd "$PROJECT_DIRECTORY"
if [ -n "$INSTALL_COMMAND" ]; then
    eval $INSTALL_COMMAND
fi
eval $SCORE_COMMAND

##### END of Scoring tests #####