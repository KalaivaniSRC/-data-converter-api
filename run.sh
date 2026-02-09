#!/bin/bash

echo ""
echo "======================================"
echo " Data Converter API - Linux/Mac Start"
echo "======================================"
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting API on http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo "Press CTRL+C to stop"
echo ""

python main.py
