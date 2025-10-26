#!/bin/bash

# Docker setup script for Cafe Menu Django application

echo "🐳 Setting up Cafe Menu with Docker..."

# Build and start containers
echo "📦 Building Docker containers..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️ Running database migrations..."
docker-compose exec web python manage.py migrate

# Populate sample data
echo "☕ Populating sample coffee data..."
docker-compose exec web python manage.py populate_coffee

# Initialize ordering
echo "📋 Initializing item ordering..."
docker-compose exec web python manage.py init_order

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🌐 Application is now running at:"
echo "   Customer Menu: http://localhost:8000/"
echo "   Staff Dashboard: http://localhost:8000/modifiers/"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
