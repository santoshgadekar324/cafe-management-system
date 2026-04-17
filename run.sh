#!/bin/bash

echo "========================================"
echo "   Cafe Management System"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install requirements
echo "Installing/Updating dependencies..."
pip install -r requirements.txt --quiet
echo ""

# Run the application
echo "Starting Cafe Management System..."
echo ""
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "Admin Login: admin@cafe.com / admin123"
echo ""

python app.py
