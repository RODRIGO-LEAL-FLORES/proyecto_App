import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'rsmotors_secret_key_123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Ruta a la que redirige si no está logueado

    # Loader de usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    # Registro de Blueprints
    from app.routes.main import main_bp
    from app.routes.portal import portal_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(portal_bp, url_prefix='/portal')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Creación de tablas
    with app.app_context():
        # Importamos modelos para que db.create_all los detecte
        from app.models.vehiculo import Vehiculo
        from app.models.usuario import Usuario
        db.create_all()

    return app