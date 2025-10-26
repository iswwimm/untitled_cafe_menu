# ☕ Cafe Menu – Django Web Application

A comprehensive Django-based web application for managing a coffee shop menu, designed for real-world usage in a café.  
The system provides both customer-facing menu display and staff management interface with advanced features for menu customization, allergen management, and responsive design.

## 🚀 Key Features

### 👥 Customer Interface
- **Responsive Menu Display** - Mobile-first design with beautiful UI
- **Coffee Menu** - Organized by groups (Basic, Alternative, Other, Add-ons)
- **Toast & Sweets Menu** - Complete food offerings with allergen information
- **Interactive Modals** - Detailed item information and image galleries
- **Allergen Information** - Comprehensive allergen tracking and display
- **Text Wrapping** - Smart text wrapping for long item names

### 🛠️ Staff Management Dashboard
- **CRUD Operations** - Add, edit, delete, and archive menu items
- **Drag & Drop Ordering** - AJAX-powered item reordering
- **Image Management** - Upload and manage item photos
- **Allergen Management** - Checkbox-based allergen selection
- **Archive System** - Soft delete with restore functionality
- **Group Management** - Organize coffee by categories
- **Price Management** - Support for dual pricing (e.g., small/large)

### 📊 Advanced Features
- **Order Management** - Custom ordering for all menu items
- **Active/Inactive Status** - Control item visibility
- **Temperature Options** - Hot, Cold, or Both for beverages
- **Description System** - Rich descriptions for modal displays
- **Management Commands** - Automated data population and initialization

## 🛠️ Tech Stack
- **Backend:** Django 5.2, Python 3.12
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Styling:** Custom CSS with responsive design
- **Image Processing:** Pillow for image handling
- **Testing:** Comprehensive test suite (54 tests)
- **Deployment:** Docker-ready with production configurations

## 📁 Project Structure
```
cafe_menu/
├── menu/                    # Main menu application
│   ├── models.py           # Coffee, Toast, Sweet models
│   ├── views.py            # Customer-facing views
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   └── management/          # Custom Django commands
├── modifiers/               # Staff management app
│   ├── views.py            # Admin dashboard views
│   ├── forms.py            # Django forms for CRUD
│   └── templates/           # Admin interface templates
├── tests.py                # Comprehensive test suite
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Installation
```bash
# Clone the repository
git clone https://github.com/iswwimm/untitled_cafe_menu.git
cd cafe_menu

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Populate sample data (optional)
python manage.py populate_coffee

# Initialize item ordering (optional)
python manage.py init_order

# Start development server
python manage.py runserver
```

### Access the Application
- **Customer Menu:** http://127.0.0.1:8000/
- **Staff Dashboard:** http://127.0.0.1:8000/modifiers/

## 🧪 Testing

The project includes a comprehensive test suite covering all functionality:

```bash
# Run all tests
python manage.py test tests -v 2

# Run specific test categories
python manage.py test tests.ModelTests -v 2
python manage.py test tests.ViewTests -v 2
python manage.py test tests.ModifierViewTests -v 2
```

### Test Coverage
- **54 total tests** covering:
  - Model functionality and properties
  - View rendering and AJAX endpoints
  - Form validation and processing
  - URL routing and resolution
  - Integration workflows
  - Edge cases and error handling
  - Performance with large datasets

## 📋 Management Commands

### Populate Sample Data
```bash
python manage.py populate_coffee
```
Creates sample coffee items with proper grouping and pricing.

### Initialize Ordering
```bash
python manage.py init_order
```
Sets up proper ordering for existing menu items.

## 🎨 Customization

### Adding New Menu Items
1. Access the staff dashboard at `/modifiers/`
2. Select the appropriate category (Coffee, Toast, Sweet)
3. Click "Add New Item"
4. Fill in the form with item details
5. Upload images and set allergens as needed

### Managing Allergens
The system supports 6 allergen categories:
- 1 - Gluten
- 2 - Dairy  
- 3 - Nuts
- 4 - Eggs
- 5 - Soy
- 6 - Sesame

### Coffee Groups
Coffee items are organized into 4 groups:
- **Basic Drinks** - Espresso, Cappuccino, Latte, etc.
- **Alternative** - Pour-over methods, Chemex, AeroPress
- **Other Drinks** - Cold brew, Matcha, Tea varieties
- **Add-ons** - Syrups, extra shots, etc.

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

## 📱 Responsive Design

The application is fully responsive with:
- **Mobile-first approach** - Optimized for smartphones
- **Tablet support** - Enhanced layouts for tablets
- **Desktop optimization** - Full-featured desktop experience
- **Touch-friendly** - Optimized for touch interactions

## 🚀 Deployment

### Docker Deployment

#### Quick Start with Docker Compose
```bash
# Clone and setup
git clone https://github.com/iswwimm/untitled_cafe_menu.git
cd cafe_menu

# Run setup script (Linux/Mac)
chmod +x docker-setup.sh
./docker-setup.sh

# Or run setup script (Windows)
docker-setup.bat

# Or manual setup
docker-compose up --build -d
```

> 📖 **Detailed Docker instructions:** See [DOCKER.md](DOCKER.md) for comprehensive Docker setup, troubleshooting, and production deployment guide.

#### Manual Docker Setup
```bash
# Build and start containers
docker-compose up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Populate sample data
docker-compose exec web python manage.py populate_coffee

# Initialize ordering
docker-compose exec web python manage.py init_order

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

#### Docker Commands
```bash
# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test tests
```

#### Single Container Deployment
```bash
# Build Docker image
docker build -t cafe-menu .

# Run with SQLite (development)
docker run -p 8000:8000 cafe-menu

# Run with PostgreSQL (production)
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:port/db \
  cafe-menu
```

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure media file storage
- [ ] Set up SSL/HTTPS
- [ ] Configure logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- 📖 **Troubleshooting Guide:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions
- 🐳 **Docker Guide:** See [DOCKER.md](DOCKER.md) for Docker setup and deployment
- 🚀 **Render Deployment:** See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for production deployment guide
- Create an issue on GitHub
- Check the test suite for usage examples
- Review the management commands for data setup

---

**Built with ❤️ for coffee lovers everywhere**