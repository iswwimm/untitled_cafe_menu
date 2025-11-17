# Café Menu — full-stack Django app for running a coffee shop menu

Guests explore a polished digital menu while staff manage offerings, assets, pricing, and ordering via a password-protected dashboard.

## Highlights
- **For guests** – responsive menu grouped by coffee, toasts, and sweets; allergen tags; optional media galleries.  
- **For staff** – session-based dashboard with CRUD, dual pricing, drag-and-drop ordering (desktop & touch), archive/restore, and bulk image uploads.  
- **For developers** – automated management commands (`populate_coffee`, `init_order`), rich Django test suite, `.env`-driven config, and container-ready deployment assets.

## Tech Stack
- **Core:** Python 3.12, Django 5.2.6, Django Admin
- **Data/storage:** SQLite (default), PostgreSQL via `dj-database-url`, Cloudinary-ready media, Pillow
- **Static & performance:** WhiteNoise, `django-cloudinary-storage`
- **Forms & utilities:** `django-multiselectfield`, `python-dotenv`, `requests`, `typing_extensions`
- **Deployment:** Gunicorn, Docker, Docker Compose
- **Frontend:** HTML5 templates, custom CSS (`menu/static`, `modifiers/static`), vanilla ES6 modules

## Project Structure
```
cafe_menu/
├── manage.py                # Django entry point
├── cafe_menu/               # Global settings, URLs, ASGI/WSGI
├── menu/                    # Guest-facing app (models, views, templates, static)
│   ├── management/commands/ # Sample-data & ordering scripts
│   └── static/menu/         # Public CSS/JS/assets
├── modifiers/               # Staff dashboard app (forms, views, templates)
│   └── static/modifiers/    # Dashboard styling & interactivity
├── media/                   # Uploaded images (development samples)
├── staticfiles/             # Collected static output (generated)
├── data.json                # Optional fixture with demo users and menu items
├── requirements.txt         # Python dependencies
├── docker-compose*.yml      # Local/override Compose configs
├── Dockerfile               # Production container recipe
└── tests.py                 # Comprehensive Django test suite
```

## Getting Started
### Prerequisites
- Python 3.12+ with `pip`
- Optional: Docker Desktop 4.x+

### Local Setup
```bash
git clone https://github.com/iswwimm/untitled_cafe_menu.git
cd cafe_menu

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py populate_coffee   # optional sample data
python manage.py init_order        # optional ordering seed
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` (guest menu) and `http://127.0.0.1:8000/modifiers/` (staff dashboard).

### Docker Workflow
```bash
docker-compose up --build
# web service runs migrations, collectstatic, then the dev server

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate_coffee
docker-compose exec web python manage.py init_order
docker-compose exec web python manage.py test
```
`docker-compose.override.yml` preloads demo content for local previews. The production `Dockerfile` installs system deps and serves the app via Gunicorn (`cafe_menu.wsgi`).

## Environment Variables
Add a `.env` file (or exported variables) for configuration:
```env
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=localhost,127.0.0.1,untitled-cafe-menu.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/cafe_menu   # optional
STAFF_PAGE_PASSWORD=set-a-strong-password
CLOUDINARY_URL=cloudinary://<key>:<secret>@<cloud>        # optional
```
- Leaving `DATABASE_URL` unset defaults to SQLite (`db.sqlite3`).  
- `STAFF_PAGE_PASSWORD` guards the dashboard (`modifiers` app).  
- Configure production deployments with `DEBUG=False` and secure secrets.

## Usage Notes
- **Menu URLs:** `/`, `/coffee/`, `/toasts/`, `/sweets/`
- **Staff access:** `/modifiers/enter-password/` prompts for `STAFF_PAGE_PASSWORD`; successful entry stores a session flag.
- **Ordering:** Drag items within their group to persist order via AJAX (`/update-order/<model>/` endpoint).
- **Data seeding:** `python manage.py loaddata data.json` loads demo users/menu items; adjust credentials before production use.
- **Static/media:** WhiteNoise serves collected static; media roots default to `media/menu/images`.

## Running Tests
```bash
python manage.py test
python manage.py test tests.ModelTests
python manage.py test tests.ViewTests
python manage.py test tests.ModifierViewTests
```
The suite covers models, forms, staff flows, AJAX ordering, and URL resolution.

## Docker & Compose Commands
```bash
docker-compose up --build              # start services
docker-compose down                    # stop and remove services
docker-compose restart                 # restart containers
docker-compose logs -f web             # tail web logs
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py shell
```
For single-container builds: `docker build -t cafe-menu .` then `docker run -p 8000:8000 cafe-menu` (configure environment variables as needed).

## License
The repository does not include a project-wide LICENSE file. Unless you add one, all rights remain reserved to the author.