from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def welcome():
    # Esta es la página de bienvenida general
    return render_template('welcome.html')

@main_bp.route('/catalogo')
def index():
    # Aquí puedes mostrar los autos para todos
    from app.models.vehiculo import Vehiculo
    autos = Vehiculo.query.all()
    return render_template('index.html', autos=autos)