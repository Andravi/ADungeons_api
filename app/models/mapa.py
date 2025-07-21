from app import db


class Mapa(db.Model):
    __tablename__ = 'mapa'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    
    objetos = db.relationship('ObjetoDeInteracao', backref='mapa', lazy=True)