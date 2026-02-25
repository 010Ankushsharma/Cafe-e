from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import MenuItem
from app import db

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/')
def index():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = MenuItem.query
    
    if search:
        query = query.filter(MenuItem.name.ilike(f'%{search}%'))
    
    if category:
        query = query.filter_by(category=category)
    
    menu_items = query.order_by(MenuItem.created_at.desc()).all()
    categories = db.session.query(MenuItem.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('menu/index.html', 
                         menu_items=menu_items, 
                         categories=categories,
                         search=search,
                         selected_category=category)


@menu_bp.route('/create', methods=['POST'])
def create():
    try:
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', '').strip()
        
        if not name or not category or not price:
            flash('All fields are required.', 'error')
            return redirect(url_for('menu.index'))
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be greater than 0.', 'error')
                return redirect(url_for('menu.index'))
        except ValueError:
            flash('Invalid price format.', 'error')
            return redirect(url_for('menu.index'))
        
        menu_item = MenuItem(
            name=name,
            category=category,
            price=price
        )
        
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item created successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while creating the menu item.', 'error')
    
    return redirect(url_for('menu.index'))


@menu_bp.route('/<int:id>/edit', methods=['POST'])
def edit(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    try:
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', '').strip()
        
        if not name or not category or not price:
            flash('All fields are required.', 'error')
            return redirect(url_for('menu.index'))
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be greater than 0.', 'error')
                return redirect(url_for('menu.index'))
        except ValueError:
            flash('Invalid price format.', 'error')
            return redirect(url_for('menu.index'))
        
        menu_item.name = name
        menu_item.category = category
        menu_item.price = price
        
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the menu item.', 'error')
    
    return redirect(url_for('menu.index'))


@menu_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    try:
        db.session.delete(menu_item)
        db.session.commit()
        flash('Menu item deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete menu item. It may be referenced by existing orders.', 'error')
    
    return redirect(url_for('menu.index'))


@menu_bp.route('/<int:id>/toggle', methods=['POST'])
def toggle_availability(id):
    menu_item = MenuItem.query.get_or_404(id)
    
    try:
        menu_item.is_available = not menu_item.is_available
        db.session.commit()
        status = 'available' if menu_item.is_available else 'out of stock'
        flash(f'Menu item marked as {status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating availability.', 'error')
    
    return redirect(url_for('menu.index'))


@menu_bp.route('/api/items')
def api_items():
    available_only = request.args.get('available', 'false').lower() == 'true'
    query = MenuItem.query
    
    if available_only:
        query = query.filter_by(is_available=True)
    
    items = query.all()
    return jsonify([item.to_dict() for item in items])