

from app.models.entidade import Entidade
from app import db


class Jogador(Entidade):
    __tablename__ = 'jogador'
    
    id = db.Column(db.Integer, db.ForeignKey('entidade.id'), primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    __mapper_args__ = {
        'polymorphic_identity': 'jogador',
    }