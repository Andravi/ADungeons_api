from app import db


class MapaEmCampanha(db.Model):
    __tablename__ = 'mapa_em_campanha'
    
    id_campanha = db.Column(db.Integer, db.ForeignKey('campanha.id'), primary_key=True)
    id_mapa = db.Column(db.Integer, db.ForeignKey('mapa.id'), primary_key=True)