#!/bin/bash
set -e

echo "Building Hospital AI Backend..."

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Build completed successfully!"
