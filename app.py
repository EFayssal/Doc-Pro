from flask import Flask, render_template, request, send_file, after_this_request, make_response, send_from_directory
from docx import Document
from io import BytesIO
import docx.shared
from docx.shared import RGBColor, Pt
from werkzeug.utils import secure_filename
from PIL import Image
import tempfile
import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


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

def generate_pdf_fayssal(buffer, data, photo_path=None):
    """Génère un PDF stylé type 'Fayssal' (header stylé, contenu vertical, pas de table imbriquée)."""
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    elements = []

    # Header: Nom, Titre, Age, Photo (table 2 colonnes)
    header_data = []
    left = []
    left.append(Paragraph(f"<b>{data['nom']}</b> <font size=10 color='#888'>({data['age']} ans)</font>", styles['Title']))
    if data.get('titre'):
        left.append(Paragraph(f"<font color='#0057b7'>{data['titre']}</font>", styles['Heading2']))
    left.append(Spacer(1, 6))
    header_data.append(left)

    right = []
    if photo_path:
        try:
            img = RLImage(photo_path, width=1.2*inch, height=1.2*inch)
            right.append(img)
        except Exception:
            right.append(Spacer(1, 1))
    else:
        right.append(Spacer(1, 1))
    header_data.append(right)

    table = Table([ [header_data[0], header_data[1]] ], colWidths=[4*inch, 2*inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Coordonnées
    coord = []
    if data.get('ville'):
        coord.append(f"📍 {data['ville']}")
    if data.get('email'):
        coord.append(f"📧 {data['email']}")
    if data.get('telephone'):
        coord.append(f"📞 {data['telephone']}")
    coord_str = " &nbsp; | &nbsp; ".join(coord)
    if coord_str:
        elements.append(Paragraph(coord_str, styles['Normal']))
        elements.append(Spacer(1, 8))

    # Sections verticales (plus de table imbriquée)
    def add_section(title, content, bullet=False, sep='\n'):
        if content:
            elements.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
            if bullet:
                for item in filter(None, (x.strip() for x in content.split(sep))):
                    elements.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                elements.append(Paragraph(content, styles['Normal']))
            elements.append(Spacer(1, 8))

    add_section("Profil", data.get('profil'))
    add_section("Compétences", data.get('competences'), bullet=True, sep=',')
    add_section("Langues", data.get('langues'), bullet=True, sep=',')
    add_section("Expériences professionnelles", data.get('experiences'), bullet=True, sep='\n')
    add_section("Formation", data.get('formations'), bullet=True, sep='\n')
    add_section("Centres d'intérêt", data.get('interets'), bullet=True, sep=',')

    doc.build(elements)

def generate_pdf_classique(buffer, data, photo_path=None):
    """Génère un PDF style classique (simple, sobre, une colonne)."""
    # À implémenter : structure simple, titres sobres, pas de couleurs flashy
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    elements = []
    if photo_path:
        try:
            img = RLImage(photo_path, width=1.2*inch, height=1.2*inch)
            elements.append(img)
        except Exception:
            pass
    elements.append(Paragraph(f"<b>{data['nom']}</b> - {data['age']} ans", styles['Title']))
    if data.get('titre'):
        elements.append(Paragraph(data['titre'], styles['Heading2']))
    coord = []
    if data.get('ville'): coord.append(f"📍 {data['ville']}")
    if data.get('email'): coord.append(f"📧 {data['email']}")
    if data.get('telephone'): coord.append(f"📞 {data['telephone']}")
    if coord:
        elements.append(Paragraph(" | ".join(coord), styles['Normal']))
    def add_section(title, content, bullet=False, sep='\n'):
        if content:
            elements.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
            if bullet:
                for item in filter(None, (x.strip() for x in content.split(sep))):
                    elements.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                elements.append(Paragraph(content, styles['Normal']))
            elements.append(Spacer(1, 8))
    add_section("Profil", data.get('profil'))
    add_section("Compétences", data.get('competences'), bullet=True, sep=',')
    add_section("Langues", data.get('langues'), bullet=True, sep=',')
    add_section("Expériences professionnelles", data.get('experiences'), bullet=True, sep='\n')
    add_section("Formation", data.get('formations'), bullet=True, sep='\n')
    add_section("Centres d'intérêt", data.get('interets'), bullet=True, sep=',')
    doc.build(elements)

def generate_pdf_etudiant(buffer, data, photo_path=None):
    """Génère un PDF style étudiant (moderne, coloré, focus sur formation et compétences)."""
    # À implémenter : couleurs, focus formation, compétences, moins d'expérience
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='EtudiantTitle', fontSize=18, textColor='#0057b7', fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='EtudiantSection', fontSize=13, textColor='#00b7ff', fontName='Helvetica-Bold'))
    elements = []
    if photo_path:
        try:
            img = RLImage(photo_path, width=1.2*inch, height=1.2*inch)
            elements.append(img)
        except Exception:
            pass
    elements.append(Paragraph(f"{data['nom']} - {data['age']} ans", styles['EtudiantTitle']))
    if data.get('titre'):
        elements.append(Paragraph(data['titre'], styles['Heading2']))
    coord = []
    if data.get('ville'): coord.append(f"📍 {data['ville']}")
    if data.get('email'): coord.append(f"📧 {data['email']}")
    if data.get('telephone'): coord.append(f"📞 {data['telephone']}")
    if coord:
        elements.append(Paragraph(" | ".join(coord), styles['Normal']))
    def add_section(title, content, bullet=False, sep='\n', style='EtudiantSection'):
        if content:
            elements.append(Paragraph(title, styles[style]))
            if bullet:
                for item in filter(None, (x.strip() for x in content.split(sep))):
                    elements.append(Paragraph(f"• {item}", styles['Normal']))
            else:
                elements.append(Paragraph(content, styles['Normal']))
            elements.append(Spacer(1, 8))
    add_section("Formation", data.get('formations'), bullet=True, sep='\n')
    add_section("Compétences", data.get('competences'), bullet=True, sep=',')
    add_section("Langues", data.get('langues'), bullet=True, sep=',')
    add_section("Profil", data.get('profil'))
    add_section("Expériences", data.get('experiences'), bullet=True, sep='\n')
    add_section("Centres d'intérêt", data.get('interets'), bullet=True, sep=',')
    doc.build(elements)

def generate_pdf_moderne(buffer, data, photo_path=None):
    """Génère un PDF moderne inspiré du HTML/CSS fourni (2 colonnes, header coloré, photo ronde, cadres, couleurs)."""
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, Frame, PageTemplate, FrameBreak, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing, Circle

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ModerneHeader', fontSize=22, textColor='#fff', fontName='Helvetica-Bold', spaceAfter=2, alignment=1))
    styles.add(ParagraphStyle(name='ModerneTitre', fontSize=14, textColor='#eee', fontName='Helvetica', spaceAfter=8, alignment=1))
    styles.add(ParagraphStyle(name='ModerneSection', fontSize=13, textColor='#068ec6', fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle(name='ModerneNormal', fontSize=11, textColor='#555', fontName='Helvetica', leading=14))
    styles.add(ParagraphStyle(name='ModerneBullet', fontSize=11, textColor='#555', fontName='Helvetica', leftIndent=12, bulletIndent=0, leading=14))

    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)

    # Header coloré
    header_elements = []
    # Photo ronde
    if photo_path:
        try:
            d = Drawing(1.5*inch, 1.5*inch)
            circle = Circle(0.75*inch, 0.75*inch, 0.7*inch)
            circle.strokeColor = colors.HexColor('#068ec6')
            circle.strokeWidth = 4
            circle.fillColor = None
            d.add(circle)
            img = RLImage(photo_path, width=1.4*inch, height=1.4*inch)
            img.hAlign = 'CENTER'
            d.add(img)
            header_img = d
        except Exception:
            header_img = Spacer(1, 1)
    else:
        header_img = Spacer(1, 1)

    # Header infos
    header_info = []
    header_info.append(Paragraph(f"{data['nom']}", styles['ModerneHeader']))
    if data.get('titre'):
        header_info.append(Paragraph(data['titre'], styles['ModerneTitre']))
    coord = []
    if data.get('ville'): coord.append(f"📍 {data['ville']}")
    if data.get('email'): coord.append(f"📧 {data['email']}")
    if data.get('telephone'): coord.append(f"📞 {data['telephone']}")
    if coord:
        header_info.append(Paragraph(" | ".join(coord), styles['ModerneNormal']))

    header_table = Table(
        [[header_img, header_info]],
        colWidths=[1.7*inch, 5.5*inch],
        style=[
            ('BACKGROUND', (0,0), (1,0), colors.HexColor('#068ec6')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]
    )

    elements = [header_table, Spacer(1, 18)]

    # Deux colonnes
    frame_width = (letter[0] - 60) / 2
    frame_height = letter[1] - 200
    left_frame = Frame(30, 30, frame_width-10, frame_height, id='left')
    right_frame = Frame(30+frame_width+10, 30, frame_width-10, frame_height, id='right')

    # Colonne gauche (photo déjà en header, compétences, langues, centres d'intérêt)
    left_col = []
    def add_section(title, content, bullet=False, sep='\n'):
        if content:
            left_col.append(Paragraph(title, styles['ModerneSection']))
            if bullet:
                for item in filter(None, (x.strip() for x in content.split(sep))):
                    left_col.append(Paragraph(f"• {item}", styles['ModerneBullet']))
            else:
                left_col.append(Paragraph(content, styles['ModerneNormal']))
            left_col.append(Spacer(1, 8))
    add_section("Compétences", data.get('competences'), bullet=True, sep=',')
    add_section("Langues", data.get('langues'), bullet=True, sep=',')
    add_section("Centres d'intérêt", data.get('interets'), bullet=True, sep=',')

    # Colonne droite (profil, formations, expériences)
    right_col = []
    def add_section_right(title, content, bullet=False, sep='\n'):
        if content:
            right_col.append(Paragraph(title, styles['ModerneSection']))
            if bullet:
                for item in filter(None, (x.strip() for x in content.split(sep))):
                    right_col.append(Paragraph(f"• {item}", styles['ModerneBullet']))
            else:
                right_col.append(Paragraph(content, styles['ModerneNormal']))
            right_col.append(Spacer(1, 8))
    add_section_right("Présentation", data.get('profil'))
    add_section_right("Formations et diplomes", data.get('formations'), bullet=True, sep='\n')
    add_section_right("Expérience", data.get('experiences'), bullet=True, sep='\n')

    doc.addPageTemplates([
        PageTemplate(id='TwoColModerne', frames=[left_frame, right_frame])
    ])

    story = []
    story += elements
    story += left_col
    story.append(FrameBreak())
    story += right_col

    doc.build(story)

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
    format = request.form.get("format", "docx")
    modele = request.form.get("modele", "fayssal")


    # Validation des champs obligatoires
    if not nom or not age:
        return "Les champs 'Nom' et 'Âge' sont obligatoires.", 400

    # Sauvegarde dans la base SQLite
    conn = sqlite3.connect('cv_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            age TEXT,
            titre TEXT,
            ville TEXT,
            email TEXT,
            telephone TEXT,
            profil TEXT,
            experiences TEXT,
            competences TEXT,
            langues TEXT,
            formations TEXT,
            interets TEXT
        )
    ''')
    c.execute('''
        INSERT INTO cvs (nom, age, titre, ville, email, telephone, profil, experiences, competences, langues, formations, interets)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nom, age, titre, ville, email, telephone, profil, experiences, competences, langues, formations, interets))
    conn.commit()
    conn.close()

    # Récupération de la photo
    photo = request.files.get("photo")
    photo_path = None
    if photo:
        try:
            # Sauvegarder temporairement la photo
            temp_dir = tempfile.gettempdir()
            photo_filename = secure_filename(photo.filename)
            photo_path = os.path.join(temp_dir, photo_filename)
            photo.save(photo_path)

            # Convertir l'image en format compatible (JPEG/PNG)
            with Image.open(photo_path) as img:
                if img.format not in ["JPEG", "PNG"]:
                    photo_path_new = os.path.join(temp_dir, f"{os.path.splitext(photo_filename)[0]}.png")
                    img.convert("RGB").save(photo_path_new, "PNG")
                    os.remove(photo_path)
                    photo_path = photo_path_new
        except Exception as e:
            return f"Erreur lors du traitement de la photo : {str(e)}", 500

    # Création du document
    doc = Document()
    appliquer_style(doc, theme)

    # Ajouter la photo au document
    if photo_path:
        try:
            doc.add_picture(photo_path, width=docx.shared.Inches(1.5))
        except Exception as e:
            return f"Erreur lors de l'ajout de la photo au document : {str(e)}", 500

    if format == "pdf":
        buffer = BytesIO()
        if modele == "moderne":
            generate_pdf_moderne(buffer, {
                'nom': nom,
                'age': age,
                'titre': titre,
                'ville': ville,
                'email': email,
                'telephone': telephone,
                'profil': profil,
                'experiences': experiences,
                'competences': competences,
                'langues': langues,
                'formations': formations,
                'interets': interets
            }, photo_path)
        elif modele == "fayssal":
            generate_pdf_fayssal(buffer, {
                'nom': nom,
                'age': age,
                'titre': titre,
                'ville': ville,
                'email': email,
                'telephone': telephone,
                'profil': profil,
                'experiences': experiences,
                'competences': competences,
                'langues': langues,
                'formations': formations,
                'interets': interets
            }, photo_path)
        elif modele == "classique":
            generate_pdf_classique(buffer, {
                'nom': nom,
                'age': age,
                'titre': titre,
                'ville': ville,
                'email': email,
                'telephone': telephone,
                'profil': profil,
                'experiences': experiences,
                'competences': competences,
                'langues': langues,
                'formations': formations,
                'interets': interets
            }, photo_path)
        elif modele == "etudiant":
            generate_pdf_etudiant(buffer, {
                'nom': nom,
                'age': age,
                'titre': titre,
                'ville': ville,
                'email': email,
                'telephone': telephone,
                'profil': profil,
                'experiences': experiences,
                'competences': competences,
                'langues': langues,
                'formations': formations,
                'interets': interets
            }, photo_path)
        else:
            return "Modèle inconnu.", 400

        buffer.seek(0)
        # Supprimer la photo temporaire APRÈS l'envoi du fichier
        if photo_path:
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(photo_path)
                except Exception as e:
                    print(f"Erreur lors de la suppression de la photo temporaire : {e}")
                return response

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"CV_{nom.replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )

    # Génération du fichier
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Supprimer la photo temporaire APRÈS l'envoi du fichier
    if photo_path:
        @after_this_request
        def remove_file(response):
            try:
                os.remove(photo_path)
            except Exception as e:
                print(f"Erreur lors de la suppression de la photo temporaire : {e}")
            return response

    if format == "html" and (modele == "moderne" or modele == "fayssal"):
        # Génère le HTML moderne avec la structure et le CSS fourni
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>CV de {nom} {titre}</title>
    <meta name="author" content="{nom}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/cv_modern.css">
</head>
<body>
    <header>
        <ul class="container">
            <li>
                <h1>
                    <span id="prenom">{nom.split(' ')[0]}</span>
                    <span id="nom">{' '.join(nom.split(' ')[1:])}</span>
                </h1>
            </li>
            <li>
                <strong>Adresse</strong>
                {ville if ville else ''}
            </li>
            <li>
                <strong>Téléphone</strong>
                {telephone}
            </li>
            <li>
                <strong>Mail</strong>
                {email}
            </li>
        </ul>
    </header>
    <main class="container">
        <aside>
            {"<img src='/static/photo.jpg' alt='Photo du cv'>" if photo_path else ""}
            <article>
                <h2>Compétences</h2>
                <p>
                    {"<br>".join([c.strip() for c in competences.split(',') if c.strip()])}
                </p>
            </article>
            <article>
                <h2>Langues</h2>
                <p>
                    {"<br>".join([l.strip() for l in langues.split(',') if l.strip()])}
                </p>
            </article>
            <article>
                <h2>Centre d'intérêt</h2>
                <p class="noBorder">
                    {"<br>".join([i.strip() for i in interets.split(',') if i.strip()])}
                </p>
            </article>
        </aside>
        <section>
            <div class="container">
                <article>
                    <h2>Présentation</h2>
                    <p>{profil}</p>
                </article>
                <article>
                    <h2>Formations et diplomes</h2>
                    <ul>
                        {''.join(f'<li class="exp"><span class="periode"></span><span class="desc">{f.strip()}</span></li>' for f in formations.split('\n') if f.strip())}
                    </ul>
                </article>
                <article>
                    <h2>Expérience</h2>
                    <ul class="top10">
                        {''.join(f'<li class="exp"><span class="periode"></span><span class="desc">{e.strip()}</span></li>' for e in experiences.split('\n') if e.strip())}
                    </ul>
                </article>
            </div>
        </section>
    </main>
    <footer>
        <ul class="container">
            <li></li>
            <li>
                <img src="/static/logoface.png" alt="logo Facebook">
                <a href="#">{nom}</a>
            </li>
        </ul>
    </footer>
</body>
</html>
"""
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=CV_{nom.replace(" ", "_")}.html'
        return response

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"CV_{nom.replace(' ', '_')}.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@app.route('/cvs')
def liste_cvs():
    conn = sqlite3.connect('cv_data.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            age TEXT,
            titre TEXT,
            ville TEXT,
            email TEXT,
            telephone TEXT,
            profil TEXT,
            experiences TEXT,
            competences TEXT,
            langues TEXT,
            formations TEXT,
            interets TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute("SELECT * FROM cvs ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("liste_cvs.html", cvs=rows)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_cv(id):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cvs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return "CV supprimé avec succès.", 200

@app.route('/admin')
def admin():
    conn = sqlite3.connect("cv_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            age TEXT,
            titre TEXT,
            ville TEXT,
            email TEXT,
            telephone TEXT,
            profil TEXT,
            experiences TEXT,
            competences TEXT,
            langues TEXT,
            formations TEXT,
            interets TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("SELECT * FROM cvs ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template("admin.html", rows=rows)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_cv(id):
    conn = sqlite3.connect("cv_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update the CV entry
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

        cursor.execute('''
            UPDATE cvs
            SET nom = ?, age = ?, titre = ?, ville = ?, email = ?, telephone = ?, profil = ?, experiences = ?, competences = ?, langues = ?, formations = ?, interets = ?
            WHERE id = ?
        ''', (nom, age, titre, ville, email, telephone, profil, experiences, competences, langues, formations, interets, id))
        conn.commit()
        conn.close()
        return "CV mis à jour avec succès.", 200

    # Fetch the CV entry for editing
    cursor.execute("SELECT * FROM cvs WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    return render_template("edit.html", cv=row)

def generate_professional_cv(doc, data):
    """Generate a professional CV using a predefined template."""
    # Add header with name and title
    header = doc.add_section().header
    header_paragraph = header.paragraphs[0]
    header_paragraph.text = f"{data['nom']} – {data['titre']}"
    header_paragraph.style = doc.styles['Heading 1']

    # Add contact information
    contact_table = doc.add_table(rows=1, cols=3)
    contact_table.style = 'Table Grid'
    contact_row = contact_table.rows[0].cells
    contact_row[0].text = f"📍 {data['ville']}" if data['ville'] else ""
    contact_row[1].text = f"📧 {data['email']}" if data['email'] else ""
    contact_row[2].text = f"📞 {data['telephone']}" if data['telephone'] else ""

    # Add sections
    def add_section(title, content):
        if content:
            doc.add_heading(title, level=2)
            doc.add_paragraph(content)

    add_section("Profil", data['profil'])
    add_section("Expériences professionnelles", data['experiences'])
    add_section("Compétences", data['competences'])
    add_section("Langues", data['langues'])
    add_section("Formation", data['formations'])
    add_section("Centres d'intérêt", data['interets'])

def generate_cv_fayssal_structure(doc, data):
    """Generate a CV using the 'cv_fayssal' structure."""
    # Add header with name, title, and photo
    header_table = doc.add_table(rows=1, cols=2)
    header_table.style = 'Table Grid'
    header_cells = header_table.rows[0].cells

    # Left cell: Name, title, and age
    header_cells[0].paragraphs[0].add_run(f"{data['nom']} {data['age']} ans").bold = True
    header_cells[0].paragraphs[0].add_run(f"\n{data['titre']}").italic = True

    # Right cell: Contact information
    contact_info = f"📧 {data['email']}\n📞 {data['telephone']}\n📍 {data['ville']}"
    header_cells[1].paragraphs[0].add_run(contact_info)

    # Add photo if available
    if 'photo_path' in data and data['photo_path']:
        try:
            header_cells[0].add_picture(data['photo_path'], width=docx.shared.Inches(1.5))
        except Exception as e:
            print(f"Erreur lors de l'ajout de la photo : {e}")

    # Add sections in two columns
    section_table = doc.add_table(rows=1, cols=2)
    section_table.style = 'Table Grid'
    left_column = section_table.rows[0].cells[0]
    right_column = section_table.rows[0].cells[1]

    # Left column: Profil, Compétences, Langues
    def add_section_to_column(column, title, content):
        if content:
            column.add_paragraph(title, style='Heading 2')
            column.add_paragraph(content)

    add_section_to_column(left_column, "Profil", data['profil'])
    add_section_to_column(left_column, "Compétences", data['competences'])
    add_section_to_column(left_column, "Langues", data['langues'])

    # Right column: Expériences professionnelles, Formation, Centres d'intérêt
    add_section_to_column(right_column, "Expériences professionnelles", data['experiences'])
    add_section_to_column(right_column, "Formation", data['formations'])
    add_section_to_column(right_column, "Centres d'intérêt", data['interets'])

@app.route('/download/<int:id>', methods=['GET'])
def download_cv(id):
    conn = sqlite3.connect("cv_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cvs WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    # Generate the updated CV document
    doc = Document()
    generate_cv_fayssal_structure(doc, row)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"CV_{row['nom'].replace(' ', '_')}.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    app.run(debug=True)