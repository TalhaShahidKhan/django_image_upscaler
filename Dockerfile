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

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations during the build phase
CMD ["sh", "-c", "python manage.py migrate && gunicorn upscale.wsgi"]
