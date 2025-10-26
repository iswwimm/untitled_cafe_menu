#!/usr/bin/env bash
# Build script for Render deployment

echo "Starting build process..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Populate sample data (optional)
echo "Populating sample data..."
python manage.py populate_coffee || echo "Sample data population failed or skipped"

# Initialize ordering
echo "Initializing item ordering..."
python manage.py init_order || echo "Order initialization failed or skipped"

echo "Build process completed successfully!"
