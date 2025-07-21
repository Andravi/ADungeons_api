from app import db


class ObjetoDeInteracao(db.Model):
    __tablename__ = 'objeto_de_interacao'
    
    id = db.Column(db.Integer, primary_key=True)
    id_mapa = db.Column(db.Integer, db.ForeignKey('mapa.id'))
    nome = db.Column(db.String(20), nullable=False)
    path_modelo = db.Column(db.String(300))
    pos_x = db.Column(db.Float)
    pos_y = db.Column(db.Float)
    pos_z = db.Column(db.Float)