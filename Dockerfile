FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Bot JSON fayllari va data uchun papka
RUN mkdir -p /app/data && chmod 755 /app/data

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Start the bot
CMD ["python", "bot.py"]
