# Cafe Order Management System

A production-ready Cafe Order Management System built with Flask, featuring a warm coffee-themed UI and comprehensive order tracking capabilities.

![Coffee Theme](https://img.shields.io/badge/Theme-Coffee%20Latte-brown)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Admin Dashboard** - Overview of cafe performance with statistics
- **Menu Management** - CRUD operations for menu items with category filtering
- **Order Management** - Create orders with multiple items, auto-calculate totals
- **Coffee Theme UI** - Warm, cozy brown color palette inspired by coffees
- **Responsive Design** - Works on desktop and mobile devices
- **PostgreSQL Database** - Production-ready database support

## Tech Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.40
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Render.com

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cafe-order-manager.git
   cd cafe-order-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   Visit http://localhost:5000

### Deployment on Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Blueprint on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Environment Variables** (auto-configured)
   - `DATABASE_URL` - PostgreSQL connection (auto-generated)
   - `SECRET_KEY` - Flask secret key (auto-generated)
   - `FLASK_ENV=production`

4. **Database Migration**
   After deployment, run in Render Shell:
   ```bash
   flask db upgrade
   ```

## Project Structure

```
Cafe-e/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── main.py          # Dashboard routes
│   │   ├── menu.py          # Menu management routes
│   │   └── orders.py        # Order management routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Coffee theme styles
│   │   └── js/
│   │       └── main.js      # JavaScript utilities
│   └── templates/
│       ├── base.html        # Base template
│       ├── dashboard.html   # Dashboard page
│       ├── menu/
│       │   └── index.html   # Menu management
│       └── orders/
│           ├── index.html   # Orders list
│           ├── create.html  # Create order
│           └── view.html    # View order
├── migrations/              # Database migrations
├── config.py               # Configuration classes
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
└── README.md              # This file
```

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Espresso Brown | #3E2723 | Headers, dark backgrounds |
| Coffee Brown | #5D4037 | Primary buttons, text |
| Mocha | #6D4C41 | Secondary elements |
| Caramel | #BF8C63 | Accents, highlights |
| Latte | #D7B19D | Input borders, dividers |
| Cream | #F5E6D3 | Main background |
| Light Cream | #FFF3E8 | Card backgrounds |

## Database Schema

- **MenuItem** - id, name, category, price, is_available
- **Order** - id, order_name, total_amount, created_at
- **OrderItem** - id, order_id, menu_item_id, quantity, subtotal

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard |
| `/menu` | GET | Menu list |
| `/menu/create` | POST | Add menu item |
| `/orders` | GET | Orders list |
| `/orders/create` | GET/POST | Create order |
| `/orders/<id>` | GET | View order |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Coffee-themed color palette inspired by warm cafe aesthetics
- Built with Flask and Bootstrap 5
- Deployed on Render.com
