#!/bin/bash
set -e

echo "Installing Python dependencies..."
python -m pip install --user --upgrade pip
python -m pip install --user -r requirements.txt

echo "Build completed successfully!"