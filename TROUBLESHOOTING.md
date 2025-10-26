# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. ModuleNotFoundError: No module named 'dj_database_url'

**Problem:** Django не може знайти модуль `dj_database_url` при запуску сервера.

**Solution:**
```bash
# Встановити модуль в віртуальне середовище
pip install dj-database-url==2.1.0

# Перевірити встановлення
python -c "import dj_database_url; print('Success')"

# Запустити сервер
python manage.py runserver
```

**Prevention:**
- Завжди встановлюйте залежності з `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Database Connection Issues

**Problem:** Помилки підключення до бази даних.

**Solutions:**

#### For Local Development (SQLite):
```bash
# Переконайтеся, що DATABASE_URL не встановлена
# або встановлена як SQLite
python manage.py migrate
python manage.py runserver
```

#### For Docker (PostgreSQL):
```bash
# Перевірити статус контейнерів
docker-compose ps

# Переглянути логи
docker-compose logs web
docker-compose logs db

# Перезапустити контейнери
docker-compose restart
```

### 3. Static Files Not Loading

**Problem:** CSS/JS файли не завантажуються.

**Solution:**
```bash
# Зібрати статичні файли
python manage.py collectstatic --noinput

# Перевірити STATIC_ROOT в settings.py
# Переконайтеся, що STATIC_URL правильно налаштований
```

### 4. Port Already in Use

**Problem:** Порт 8000 вже використовується.

**Solutions:**
```bash
# Знайти процес, що використовує порт
netstat -an | findstr :8000

# Зупинити процес
taskkill /F /IM python.exe

# Або використати інший порт
python manage.py runserver 8001
```

### 5. Virtual Environment Issues

**Problem:** Пакети встановлені глобально, а не в venv.

**Solution:**
```bash
# Переконайтеся, що venv активований
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Перевірити активне середовище
where python
pip list
```

### 6. Migration Issues

**Problem:** Помилки при виконанні міграцій.

**Solutions:**
```bash
# Перевірити статус міграцій
python manage.py showmigrations

# Застосувати міграції
python manage.py migrate

# Якщо є конфлікти, створити нові міграції
python manage.py makemigrations
python manage.py migrate
```

### 7. Docker Issues

**Problem:** Контейнери не запускаються або не працюють.

**Solutions:**
```bash
# Перевірити статус
docker-compose ps

# Переглянути логи
docker-compose logs -f

# Перезапустити з нуля
docker-compose down -v
docker-compose up --build -d

# Перевірити зображення
docker images
docker ps -a
```

## Quick Fixes

### Reset Everything (Local Development)
```bash
# Зупинити сервер
Ctrl+C

# Очистити кеш
python manage.py clear_cache

# Перезапустити
python manage.py runserver
```

### Reset Everything (Docker)
```bash
# Зупинити та видалити все
docker-compose down -v

# Видалити зображення
docker rmi cafe_menu-web

# Перезапустити
docker-compose up --build -d
```

### Check System Requirements
```bash
# Python версія
python --version

# Django версія
python -m django --version

# Встановлені пакети
pip list

# Статус міграцій
python manage.py showmigrations
```

## Environment Variables

### Local Development
```bash
# Не встановлюйте DATABASE_URL для SQLite
# DEBUG=True (за замовчуванням)
# ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker Development
```bash
# DATABASE_URL=postgresql://postgres:postgres@db:5432/cafe_menu
# DEBUG=1
# ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production
```bash
# DATABASE_URL=postgresql://user:pass@host:port/db
# DEBUG=False
# ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# SECRET_KEY=your-secret-key
```

## Getting Help

1. **Check logs** - Django та Docker логи містять детальну інформацію
2. **Verify environment** - Переконайтеся, що всі залежності встановлені
3. **Test components** - Перевірте кожен компонент окремо
4. **Check documentation** - Django та Docker документація
5. **Community support** - Stack Overflow, Django форуми

## Prevention Tips

1. **Always use virtual environments** - Ізолюйте залежності проекту
2. **Keep requirements.txt updated** - Відстежуйте всі залежності
3. **Test regularly** - Запускайте тести перед деплоєм
4. **Use version control** - Зберігайте зміни в Git
5. **Document changes** - Ведіть журнал змін
