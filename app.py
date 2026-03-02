import os
from app import create_app, db
from app.models import MenuItem, Order, OrderItem

# Set environment for production
os.environ.setdefault('FLASK_ENV', 'production')

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'MenuItem': MenuItem,
        'Order': Order,
        'OrderItem': OrderItem
    }


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')


@app.cli.command('seed-db')
def seed_db():
    """Seed the database with sample data."""
    from decimal import Decimal
    
    # Sample menu items
    sample_items = [
        MenuItem(name='Espresso', category='Coffee', price=Decimal('3.50')),
        MenuItem(name='Cappuccino', category='Coffee', price=Decimal('4.50')),
        MenuItem(name='Latte', category='Coffee', price=Decimal('4.75')),
        MenuItem(name='Americano', category='Coffee', price=Decimal('3.75')),
        MenuItem(name='Mocha', category='Coffee', price=Decimal('5.00')),
        MenuItem(name='Croissant', category='Pastry', price=Decimal('3.25')),
        MenuItem(name='Muffin', category='Pastry', price=Decimal('2.75')),
        MenuItem(name='Bagel', category='Pastry', price=Decimal('2.50')),
        MenuItem(name='Sandwich', category='Food', price=Decimal('7.50')),
        MenuItem(name='Salad', category='Food', price=Decimal('8.00')),
        MenuItem(name='Cheesecake', category='Dessert', price=Decimal('5.50')),
        MenuItem(name='Tiramisu', category='Dessert', price=Decimal('6.00')),
    ]
    
    for item in sample_items:
        db.session.add(item)
    
    db.session.commit()
    print('Database seeded with sample data.')


if __name__ == '__main__':
    app.run(debug=True, port=5000)