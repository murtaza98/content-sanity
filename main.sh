#!/bin/bash

set -e

# Variables
REPO_URL="https://github.com/your-username/your-repo.git"  # Replace with the actual repo URL
CLONE_DIR="$HOME/$(basename "$REPO_URL" .git)"
VENV_NAME="venv"

echo "Cloning repository..."
# Clone the repository
git clone "$REPO_URL" "$CLONE_DIR"

# Navigate to the cloned directory
cd "$CLONE_DIR"

echo "Creating virtual environment..."
# Create a virtual environment
python3 -m venv "$VENV_NAME"

# Activate the virtual environment
source "$VENV_NAME/bin/activate"

echo "Installing required packages..."
# Install required packages
pip install --upgrade pip
pip install -r requirements.txt

# Find the Python script in the repo
PYTHON_SCRIPT=$(find . -type f -name "*.py" | head -n 1)

if [ -z "$PYTHON_SCRIPT" ]; then
    echo "No Python script found in the repository."
    deactivate
    exit 1
fi

echo "Running the Python script: $PYTHON_SCRIPT"
# Run the Python script
python "$PYTHON_SCRIPT"

# Deactivate the virtual environment
deactivate

echo "Script execution completed."
