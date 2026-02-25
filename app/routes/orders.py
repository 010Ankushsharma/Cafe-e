from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, date
from app.models import Order, OrderItem, MenuItem
from app import db

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/')
def index():
    date_filter = request.args.get('date', '')
    
    query = Order.query
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(
                db.func.date(Order.created_at) == filter_date
            )
        except ValueError:
            pass
    
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('orders/index.html', orders=orders, date_filter=date_filter)


@orders_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            items_data = request.form.getlist('items[]')
            quantities_data = request.form.getlist('quantities[]')
            order_name = request.form.get('order_name', '').strip()
            
            if not items_data:
                flash('Please select at least one menu item.', 'error')
                return redirect(url_for('orders.create'))
            
            order = Order(order_name=order_name if order_name else None)
            db.session.add(order)
            db.session.flush()
            
            total_amount = 0
            
            for item_id, quantity in zip(items_data, quantities_data):
                menu_item = MenuItem.query.get(int(item_id))
                if menu_item and menu_item.is_available:
                    qty = int(quantity)
                    if qty > 0:
                        subtotal = float(menu_item.price) * qty
                        order_item = OrderItem(
                            order_id=order.id,
                            menu_item_id=menu_item.id,
                            quantity=qty,
                            subtotal=subtotal
                        )
                        db.session.add(order_item)
                        total_amount += subtotal
            
            if total_amount == 0:
                db.session.rollback()
                flash('Please select at least one available item.', 'error')
                return redirect(url_for('orders.create'))
            
            order.total_amount = total_amount
            db.session.commit()
            flash('Order created successfully!', 'success')
            return redirect(url_for('orders.view', id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the order.', 'error')
            return redirect(url_for('orders.create'))
    
    menu_items = MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category, MenuItem.name).all()
    
    # Get unique categories and counts
    categories = db.session.query(MenuItem.category).filter_by(is_available=True).distinct().order_by(MenuItem.category).all()
    categories = [c[0] for c in categories]
    
    category_counts = {}
    for category in categories:
        count = MenuItem.query.filter_by(category=category, is_available=True).count()
        category_counts[category] = count
    
    return render_template('orders/create.html', menu_items=menu_items, categories=categories, category_counts=category_counts)


@orders_bp.route('/<int:id>')
def view(id):
    order = Order.query.get_or_404(id)
    return render_template('orders/view.html', order=order)


@orders_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    order = Order.query.get_or_404(id)
    
    try:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the order.', 'error')
    
    return redirect(url_for('orders.index'))


@orders_bp.route('/api/menu-items')
def api_menu_items():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([item.to_dict() for item in items])