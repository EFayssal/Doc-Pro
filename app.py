from flask import Flask, render_template, request, send_file
from docx import Document
from io import BytesIO
import docx.shared
from docx.shared import RGBColor, Pt
from werkzeug.utils import secure_filename
from PIL import Image
import tempfile
import os

app = Flask(__name__)

def appliquer_style(doc, theme):
    """Applique un style au document en fonction du thème choisi"""
    if theme == "moderne":
        doc.styles['Normal'].font.name = 'Calibri'
        doc.styles['Normal'].font.size = Pt(11)
    elif theme == "couleur":
        doc.styles['Normal'].font.name = 'Arial'
        doc.styles['Normal'].font.size = Pt(11)
        doc.styles['Normal'].font.color.rgb = RGBColor(0, 102, 204)
    else:  # classique (par défaut)
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_cv():
    # Vérification du consentement
    if not request.form.get("consentement"):
        return "Vous devez accepter la politique de traitement des données.", 400

    # Récupération des données
    theme = request.form.get("theme", "classique")
    nom = request.form.get("nom", "").strip()
    age = request.form.get("age", "").strip()
    titre = request.form.get("titre", "").strip()
    ville = request.form.get("ville", "").strip()
    email = request.form.get("email", "").strip()
    telephone = request.form.get("telephone", "").strip()
    profil = request.form.get("profil", "").strip()
    experiences = request.form.get("experiences", "").strip()
    competences = request.form.get("competences", "").strip()
    langues = request.form.get("langues", "").strip()
    formations = request.form.get("formations", "").strip()
    interets = request.form.get("interets", "").strip()


    # Validation des champs obligatoires
    if not nom or not age:
        return "Les champs 'Nom' et 'Âge' sont obligatoires.", 400

    # Création du document
    doc = Document()
    appliquer_style(doc, theme)

    # En-tête du CV
    doc.add_heading(f"{nom} - {age} ans", level=0)
    if titre:
        doc.add_paragraph(titre)
    
    # Coordonnées
    coordonnees = []
    if ville: coordonnees.append(f"📍 {ville}")
    if email: coordonnees.append(f"📧 {email}")
    if telephone: coordonnees.append(f"📞 {telephone}")
    
    if coordonnees:
        doc.add_paragraph("\n".join(coordonnees))

    # Sections du CV
    if profil:
        doc.add_heading("Profil", level=1)
        doc.add_paragraph(profil)

    if experiences:
        doc.add_heading("Expériences professionnelles", level=1)
        for exp in filter(None, (e.strip() for e in experiences.split('\n'))):
            doc.add_paragraph(exp, style='List Bullet')

    if competences:
        doc.add_heading("Compétences", level=1)
        for comp in filter(None, (c.strip() for c in competences.split(','))):
            doc.add_paragraph(f"• {comp}", style='List Bullet')

    if langues:
        doc.add_heading("Langues", level=1)
        for lang in filter(None, (l.strip() for l in langues.split(','))):
            doc.add_paragraph(f"• {lang}", style='List Bullet')

    if formations:
        doc.add_heading("Formation", level=1)
        for form in filter(None, (f.strip() for f in formations.split('\n'))):
            doc.add_paragraph(f"• {form}", style='List Bullet')

    if interets:
        doc.add_heading("Centres d'intérêt", level=1)
        for interest in filter(None, (i.strip() for i in interets.split(','))):
            doc.add_paragraph(f"• {interest}", style='List Bullet')

    # Génération du fichier
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"CV_{nom.replace(' ', '_')}.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    app.run(debug=True)