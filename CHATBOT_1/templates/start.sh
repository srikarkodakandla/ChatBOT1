#!/bin/sh
# Start Ollama serve in the background
/bin/ollama serve &
# Wait for Ollama to be ready
sleep 5
# Start the Flask app
exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 app:app