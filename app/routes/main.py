from flask import Blueprint, render_template
from app.models import MenuItem, Order
from app import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    total_items = MenuItem.query.count()
    available_items = MenuItem.query.filter_by(is_available=True).count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_items=total_items,
                         available_items=available_items,
                         recent_orders=recent_orders)