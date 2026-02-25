from datetime import datetime
from app import db


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', back_populates='menu_item', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': float(self.price),
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(100), nullable=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', back_populates='order', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        total = sum(item.subtotal for item in self.order_items)
        self.total_amount = total
        return total
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_name': self.order_name,
            'total_amount': float(self.total_amount),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'item_count': len(self.order_items)
        }
    
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    order = db.relationship('Order', back_populates='order_items')
    menu_item = db.relationship('MenuItem', back_populates='order_items')
    
    def calculate_subtotal(self):
        if self.menu_item:
            self.subtotal = float(self.menu_item.price) * self.quantity
        return self.subtotal
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'menu_item_name': self.menu_item.name if self.menu_item else None,
            'menu_item_price': float(self.menu_item.price) if self.menu_item else None,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal)
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'