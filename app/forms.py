from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese usuario ya existe. Escoge otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese correo ya está registrado.')

class LoginForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RepairForm(FlaskForm):
    # Datos del cliente
    client_name = StringField('Nombre del Cliente', validators=[DataRequired()])
    phone = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    address = StringField('Dirección', validators=[DataRequired()])
    # Datos del electrodoméstico
    brand = StringField('Marca', validators=[DataRequired()])
    model = StringField('Modelo', validators=[DataRequired()])
    serial_number = StringField('Número de Serie', validators=[DataRequired()])
    # Detalles de la reparación
    description = TextAreaField('Descripción del Problema', validators=[DataRequired()])
    observations = TextAreaField('Observaciones')
    conditions = TextAreaField('Condiciones de Recepción', default="Condiciones de recepción predefinidas.")
    submit = SubmitField('Guardar Reparación')

class QueryForm(FlaskForm):
    unique_code = StringField('Código de Reparación', validators=[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('Consultar')

class FilterForm(FlaskForm):
    status = SelectField('Estado', choices=[('', 'Todos'), ('Recibido', 'Recibido'), ('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')])
    submit = SubmitField('Filtrar')
