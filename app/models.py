from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import secrets

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    observations = db.Column(db.Text, nullable=True)
    conditions = db.Column(db.Text, nullable=False, default="Condiciones de recepción predefinidas.")
    unique_code = db.Column(db.String(8), unique=True, nullable=False, default=lambda: secrets.token_hex(4))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="Recibido")

    def __repr__(self):
        return f"Repair('{self.unique_code}', '{self.client_name}', '{self.status}')"
