from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    age = db.Column(db.String(10))
    titre = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    profil = db.Column(db.Text)
    experiences = db.Column(db.Text)
    competences = db.Column(db.Text)
    langues = db.Column(db.Text)
    formations = db.Column(db.Text)
    interets = db.Column(db.Text)
