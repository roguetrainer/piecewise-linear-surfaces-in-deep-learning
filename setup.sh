#!/bin/bash

# Setup script for Piecewise Linear Neural Networks Demo
# Creates a virtual environment and installs dependencies

echo "=================================================="
echo "  Piecewise Linear Neural Networks Demo Setup"
echo "=================================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment."
    echo "Make sure python3-venv is installed:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-venv"
    echo "  macOS: python3-venv should be included with Python"
    exit 1
fi

echo "✓ Virtual environment created successfully"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment."
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

if [ $? -ne 0 ]; then
    echo "WARNING: Failed to upgrade pip, continuing anyway..."
fi

echo ""

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install required packages."
    exit 1
fi

echo ""
echo "✓ All packages installed successfully"
echo ""

# Setup Jupyter kernel
echo "Setting up Jupyter kernel..."
python -m ipykernel install --user --name=piecewise_linear_demo --display-name="Piecewise Linear Demo"

if [ $? -eq 0 ]; then
    echo "✓ Jupyter kernel installed successfully"
else
    echo "WARNING: Failed to install Jupyter kernel. You may need to do this manually."
fi

echo ""
echo "=================================================="
echo "  Setup Complete!"
echo "=================================================="
echo ""
echo "To get started:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Run the demo scripts:"
echo "     - python piecewise_linear_demo.py"
echo "     - python simple_1d_example.py"
echo "  3. Or launch Jupyter: jupyter notebook piecewise_linear_notebook.ipynb"
echo ""
echo "To deactivate the environment later, simply run: deactivate"
echo ""
