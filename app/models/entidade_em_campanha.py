from app import db


class EntidadeEmCampanha(db.Model):
    __tablename__ = 'entidade_em_campanha'
    
    id_campanha = db.Column(db.Integer, db.ForeignKey('campanha.id'), primary_key=True)
    id_entidade = db.Column(db.Integer, db.ForeignKey('entidade.id'), primary_key=True)
    tipo_entidade = db.Column(db.String(15), nullable=False)  # "inimigo" ou "jogador"
    
    # Relações
    campanha = db.relationship('Campanha', back_populates='entidades')
    entidade = db.relationship('Entidade', back_populates='campanhas')