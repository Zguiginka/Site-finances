from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Gastos(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.Date)
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)
    cat1 = db.Column(db.String(50))
    cat2 = db.Column(db.String(50))
    metodo = db.Column(db.String(25))
    idparc = db.Column(db.Integer)
    numparcela = db.Column(db.Integer)