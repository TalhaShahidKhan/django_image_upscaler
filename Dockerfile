FROM python:3.11.7-slim

WORKDIR /app

# Install Node.js for Tailwind
RUN apt-get update && apt-get install -y nodejs npm

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Build Tailwind CSS
RUN npm run build

# Expose the port
EXPOSE 8000

# Create a startup script
RUN echo '#!/bin/bash\n\
sleep 5\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
gunicorn upscale.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120' > /app/start.sh

RUN chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]
