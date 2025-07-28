
from app import db

class Entidade(db.Model):
    __tablename__ = 'entidade'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pos_x = db.Column(db.Float)  # DOUBLE PRECISION no PostgreSQL
    pos_y = db.Column(db.Float)
    pos_z = db.Column(db.Float)
    nome = db.Column(db.String(30), nullable=False)
    path_modelo = db.Column(db.String(300))
    hp = db.Column(db.SmallInteger)
    qnt_deslocamento = db.Column(db.SmallInteger)
    qnt_campo_visao = db.Column(db.SmallInteger)

    # Relação com campanhas (via tabela associativa)
    #campanhas = db.relationship('EntidadeEmCampanha', back_populates='entidade', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Entidade(id={self.id}, nome='{self.nome}', pos=({self.pos_x}, {self.pos_y}, {self.pos_z}))>"
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'last_login_at': self.last_login.isoformat() if self.last_login else None
        }