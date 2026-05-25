from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.vehiculo import Vehiculo

portal_bp = Blueprint('portal', __name__)

# Decorador para restringir acceso a administradores
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash("Acceso denegado: Se requieren permisos de administrador.")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# RUTA 1: El Dashboard (Lobby de opciones)
@portal_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('dashboard.html')

# RUTA 2: El CRUD (Gestión de inventario)
@portal_bp.route('/inventario')
@login_required
@admin_required
def portal_index():
    autos = Vehiculo.query.all()
    return render_template('portal.html', autos=autos)

# RUTA 3: Crear nuevo auto
@portal_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuevo_auto():
    if request.method == 'POST':
        nuevo = Vehiculo(
            marca=request.form['marca'],
            modelo=request.form['modelo'],
            anio=int(request.form['anio']),
            precio=float(request.form['precio']),
            imagen_url=request.form.get('imagen_url', '')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Vehículo registrado con éxito')
        return redirect(url_for('portal.portal_index'))
    return render_template('form.html', auto=None)

# RUTA 4: Editar auto
@portal_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_auto(id):
    auto = Vehiculo.query.get_or_404(id)
    if request.method == 'POST':
        auto.marca = request.form['marca']
        auto.modelo = request.form['modelo']
        auto.anio = int(request.form['anio'])
        auto.precio = float(request.form['precio'])
        auto.imagen_url = request.form.get('imagen_url', auto.imagen_url)
        db.session.commit()
        flash('Vehículo actualizado')
        return redirect(url_for('portal.portal_index'))
    return render_template('form.html', auto=auto)

# RUTA 5: Eliminar auto
@portal_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_auto(id):
    auto = Vehiculo.query.get_or_404(id)
    db.session.delete(auto)
    db.session.commit()
    flash('Vehículo eliminado del catálogo')
    return redirect(url_for('portal.portal_index'))