from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.usuario import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está logueado, lo redirigimos a donde corresponde
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        
        # Validar credenciales
        if user and user.password == password:
            login_user(user)
            flash(f'¡Bienvenido de nuevo, {user.username}!', 'success')
            
            # Redirección según rol: 
            # Admin va al Dashboard, Cliente va al index general
            if user.es_admin:
                return redirect(url_for('portal.dashboard'))
            else:
                return redirect(url_for('main.index'))
        
        flash('Credenciales incorrectas. Intenta de nuevo.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Crear nuevo usuario con rol de cliente por defecto
        new_user = Usuario(
            username=request.form.get('username'),
            password=request.form.get('password'),
            es_admin=False 
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cuenta creada exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    # Ajusta 'main.welcome' al nombre de la ruta de tu página de inicio pública
    return redirect(url_for('main.index'))