from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Buscamos al usuario por su nombre de usuario
        user = Usuario.query.filter_by(username=request.form['username']).first()
        
        # Verificamos contraseña (Nota: En un entorno real, usa hash de contraseñas)
        if user and user.password == request.form['password']:
            login_user(user)
            # Redirigimos según el rol
            return redirect(url_for('portal.portal_index') if user.es_admin else url_for('main.index'))
        
        flash('Credenciales incorrectas')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))