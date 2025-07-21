from app import db
import datetime

class Campanha(db.Model):
    __tablename__ = 'campanha'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(300))
    nome = db.Column(db.String(20), nullable=False)
    id_mestre = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_criacao = db.Column(db.Date, default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relações
    mapas = db.relationship('MapaEmCampanha', backref='campanha', lazy=True)

# Tabela de associação muitos-para-muitos
usuario_campanha = db.Table('usuario_em_campanha',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('id_campanha', db.Integer, db.ForeignKey('campanha.id'), primary_key=True)
)