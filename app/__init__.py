from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize production config if needed
    config[config_name].init_app(app) if hasattr(config[config_name], 'init_app') else None
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes.main import main_bp
    from app.routes.menu import menu_bp
    from app.routes.orders import orders_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    
    return app