from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.forms import RegistrationForm, LoginForm, RepairForm, QueryForm, FilterForm
from app.models import User, Repair
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# Página pública de consulta de reparaciones
@main.route('/')
def index():
    form = QueryForm()
    return render_template('index.html', form=form)

@main.route('/consulta', methods=['POST'])
def consulta():
    form = QueryForm()
    if form.validate_on_submit():
        code = form.unique_code.data
        repair = Repair.query.filter_by(unique_code=code).first()
        if repair:
            return render_template('repair_detail.html', repair=repair)
        else:
            flash('No se encontró reparación con ese código', 'danger')
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))

# Rutas de autenticación
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Inicio de sesión fallido. Revisa tus credenciales', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Dashboard y gestión de reparaciones (CRUD)
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = FilterForm()
    if form.validate_on_submit():
        status = form.status.data
        if status:
            repairs = Repair.query.filter_by(status=status).all()
        else:
            repairs = Repair.query.all()
    else:
        repairs = Repair.query.all()
    return render_template('dashboard.html', repairs=repairs, form=form)

@main.route('/repair/new', methods=['GET', 'POST'])
@login_required
def new_repair():
    form = RepairForm()
    if form.validate_on_submit():
        repair = Repair(
            client_name=form.client_name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            brand=form.brand.data,
            model=form.model.data,
            serial_number=form.serial_number.data,
            description=form.description.data,
            observations=form.observations.data,
            conditions=form.conditions.data
        )
        db.session.add(repair)
        db.session.commit()
        flash('Reparación registrada con éxito', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('repair_form.html', form=form, legend='Nueva Reparación')

@main.route('/repair/<int:repair_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    form = RepairForm()
    if form.validate_on_submit():
        repair.client_name = form.client_name.data
        repair.phone = form.phone.data
        repair.email = form.email.data
        repair.address = form.address.data
        repair.brand = form.brand.data
        repair.model = form.model.data
        repair.serial_number = form.serial_number.data
        repair.description = form.description.data
        repair.observations = form.observations.data
        repair.conditions = form.conditions.data
        db.session.commit()
        flash('Reparación actualizada', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.client_name.data = repair.client_name
        form.phone.data = repair.phone
        form.email.data = repair.email
        form.address.data = repair.address
        form.brand.data = repair.brand
        form.model.data = repair.model
        form.serial_number.data = repair.serial_number
        form.description.data = repair.description
        form.observations.data = repair.observations
        form.conditions.data = repair.conditions
    return render_template('repair_form.html', form=form, legend='Editar Reparación')

@main.route('/repair/<int:repair_id>/delete', methods=['POST'])
@login_required
def delete_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    db.session.delete(repair)
    db.session.commit()
    flash('Reparación eliminada', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/repair/<int:repair_id>/complete')
@login_required
def complete_repair(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    repair.status = 'Terminado'
    db.session.commit()
    flash('Reparación marcada como completada', 'success')
    return redirect(url_for('main.dashboard'))

# Generación de la Nota de Recepción
@main.route('/repair/<int:repair_id>/nota')
@login_required
def nota_recepcion(repair_id):
    repair = Repair.query.get_or_404(repair_id)
    return render_template('nota_recepcion.html', repair=repair)
