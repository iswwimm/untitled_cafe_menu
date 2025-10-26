# 🐳 Docker Setup Instructions

## Quick Start

### Option 1: Automated Setup Scripts
```bash
# Linux/Mac
chmod +x docker-setup.sh
./docker-setup.sh

# Windows
docker-setup.bat
```

### Option 2: Manual Setup
```bash
# Build and start containers
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Access the Application

- **Customer Menu:** http://localhost:8000/
- **Staff Dashboard:** http://localhost:8000/modifiers/

## Docker Commands

### Basic Operations
```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f web
docker-compose logs -f db
```

### Development Commands
```bash
# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test tests

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Database Operations
```bash
# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d cafe_menu

# Backup database
docker-compose exec db pg_dump -U postgres cafe_menu > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres cafe_menu < backup.sql
```

## Configuration

### Environment Variables
The application uses these environment variables:

- `DEBUG` - Django debug mode (default: True)
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### Volumes
- `postgres_data` - PostgreSQL data persistence
- `static_volume` - Static files
- `media_volume` - Media files (images)

## Troubleshooting

### Common Issues

1. **Database connection refused**
   ```bash
   # Check if database is healthy
   docker-compose ps
   
   # Restart containers
   docker-compose restart
   ```

2. **Port already in use**
   ```bash
   # Stop containers
   docker-compose down
   
   # Check what's using the port
   netstat -an | findstr :8000
   ```

3. **Static files not loading**
   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **Permission issues**
   ```bash
   # Rebuild containers
   docker-compose down
   docker-compose up --build -d
   ```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker rmi cafe_menu-web

# Start fresh
docker-compose up --build -d
```

## Production Deployment

### Using Docker Compose
```bash
# Set production environment
export DEBUG=False
export DATABASE_URL=postgresql://user:pass@host:port/db

# Start production containers
docker-compose up -d
```

### Using Single Container
```bash
# Build image
docker build -t cafe-menu .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DEBUG=False \
  -e DATABASE_URL=postgresql://user:pass@host:port/db \
  cafe-menu
```

## File Structure
```
cafe_menu/
├── Dockerfile                 # Main Docker configuration
├── docker-compose.yml         # Multi-container setup
├── docker-compose.override.yml # Development overrides
├── .dockerignore             # Files to exclude from build
├── docker-setup.sh           # Linux/Mac setup script
├── docker-setup.bat          # Windows setup script
└── requirements.txt          # Python dependencies
```

## Performance Tips

1. **Use volumes for development** - Mount source code for hot reloading
2. **Optimize build** - Use .dockerignore to exclude unnecessary files
3. **Health checks** - Database health check ensures proper startup order
4. **Resource limits** - Add memory/CPU limits for production

## Security Notes

1. **Change default passwords** - Update PostgreSQL credentials
2. **Use secrets** - Store sensitive data in Docker secrets
3. **Network isolation** - Use custom networks for container communication
4. **Regular updates** - Keep base images updated
