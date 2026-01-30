#!/bin/bash

# CPR Pose Detection Model - Setup Script
# Professional deployment script for hackathon evaluation

echo "=========================================="
echo "CPR Pose Detection Model Setup"
echo "=========================================="

# Check if Node.js is installed
if command -v node &> /dev/null; then
    echo "✓ Node.js found: $(node --version)"
    
    # Install serve if not present
    if ! command -v npx &> /dev/null; then
        echo "Installing npx..."
        npm install -g npx
    fi
    
    echo "Starting model server..."
    echo "Model will be available at: http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    npx serve . -p 8000
    
elif command -v python3 &> /dev/null; then
    echo "✓ Python 3 found: $(python3 --version)"
    echo "Starting Python server..."
    echo "Model will be available at: http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    python3 -m http.server 8000
    
elif command -v python &> /dev/null; then
    echo "✓ Python found: $(python --version)"
    echo "Starting Python server..."
    echo "Model will be available at: http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    python -m http.server 8000
    
else
    echo "❌ No suitable server found."
    echo "Please install Node.js or Python to run the model."
    echo ""
    echo "Installation options:"
    echo "- Node.js: https://nodejs.org/"
    echo "- Python: https://python.org/"
    echo ""
    echo "Alternative: Open index.html directly in browser"
    echo "(Note: Camera may not work without proper server)"
fi