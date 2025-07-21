from app.models.entidade import Entidade
from app import db


class Inimigo(Entidade):
    __tablename__ = 'inimigo'
    
    id = db.Column(db.Integer, db.ForeignKey('entidade.id'), primary_key=True)
    dano = db.Column(db.SmallInteger)
    
    __mapper_args__ = {
        'polymorphic_identity': 'inimigo',
    }