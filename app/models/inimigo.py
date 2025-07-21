from app.models.entidade import Entidade
from app import db


class Inimigo(Entidade):
    __tablename__ = 'inimigo'
    
    id = db.Column(db.Integer, primary_key=True)
    dano = db.Column(db.SmallInteger)
    
    __mapper_args__ = {
        'polymorphic_identity': 'inimigo',
        'inherit_condition': (id == Entidade.id)
    }