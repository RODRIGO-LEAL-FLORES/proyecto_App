from app import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    __table_args__ = {'extend_existing': True} # <-- Esto evita que truene por duplicados
    
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)