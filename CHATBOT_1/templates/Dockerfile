# Start from the official Ollama image
FROM ollama/ollama

# Set up a work directory
WORKDIR /app

# Install Python and Pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy our application files
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Pre-pull the model we want to use (optional, but speeds up first launch)
RUN ollama pull phi3:mini

# Expose the port our Flask app will run on
EXPOSE 8080

# Set the startup command
CMD ["/app/start.sh"]