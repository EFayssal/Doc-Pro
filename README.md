# Doc PRO 5.6 Version stable (Free)

Doc Pro 5.6 est une application web qui permet de créer, gérer et personnaliser des CV et des lettres de motivation facilement.

## Nouveautés
- **👉 CV Moderne 100% personnalisable / changez les couleurs, déplacez les blocs, modifiez chaque texte à votre guise, puis téléchargez-le en PDF format A4, prêt à impressionner et convaincre votre futur employeur** 

- **👉 CV Classique optimisé ATS / spécialement conçu pour passer les robots de tri (ATS) sans être rejeté. Toujours mis à jour selon les dernières exigences, testé et approuvé pour que votre CV arrive directement chez l’employeur.Vous pouvez changer la police et les couleurs, personnaliser chaque détail, puis le télécharger en PDF format A4** 

- **Maj des interfaces utilisateurs L'integration du JS Le Cv_Moderne est entièrement personalisable , infos, Couleurs, position, barre de compétences réglable**
- **Génération d’une lettre de motivation** 


## À quoi sert l’application ?

Cette application a pour objectif de vous aider à concevoir un ou plusieurs CV professionnels en ligne, ainsi que des lettres de motivation personnalisées. Vous pouvez ajouter vos informations personnelles, vos expériences, vos formations, vos compétences, puis générer et gérer vos documents.

## Comment utiliser l’application ?

1. **Installation**
   - Clonez le dépôt :
     ```bash
     git clone https://github.com/EFayssal/cv_app.git
     cd cv_app
     ```
   - Installez les dépendances pour demarer Doc Pro sur votre local host  :
   - Python + 
     ```bash
     python install flask
     # ou
     pip install flask
     pip install python-docx
     pip install pillow
     pip install gunicorn
     pip install reportlab
     pip install weasyprint
        installer MSYS2 (env de py)
        Install GTK4 and its dependencies. 
        Open a MSYS2 shell, and run:
        pacman -S mingw-w64-ucrt-x86_64-gtk4
        If you want to develop with GTK3, run:
        pacman -S mingw-w64-ucrt-x86_64-gtk3
        Info : GTK runtimes (64bit si la version python 64 sinon 32bit)
     
    ```
   - (Facultatif) Configurez le fichier `.env` selon vos besoins.

2. **Lancement**
   - Lancez le serveur en mode développement :
     ```bash
     pip app.py
     ```
   - Ouvrez votre navigateur et accédez à l’adresse indiquée dans le terminal (généralement [http://localhost:5000](http://localhost:5000)).

3. **Utilisation**
   - Choisisez un modèl en Moderne, Classique, Créatif
   - Ajoutez vos informations dans le CV et votre lettre de motivation.
   - Modifiez, supprimez, téléchargez vos CV et lettres à tout moment.

## Pour qui ?

- Étudiants, jeunes diplômés, professionnels, ou toute personne souhaitant créer un CV ou une lettre de motivation simplement et rapidement.

## Remarques

- L’application évolue, n’hésitez pas à proposer des améliorations via une issue ou une pull request.
- Pensez à ne pas partager d’informations sensibles dans vos documents.

# Image

Voici une image illustrative :
CV Moderne :
![Image](https://github.com/user-attachments/assets/d363a247-ba8c-4b82-9323-2dbed8454d62)
CV Classique !
![Image](https://github.com/user-attachments/assets/6de7c746-b32a-4eea-b5ae-e6b141537fa5)
CV Créatif :
![Image](https://github.com/user-attachments/assets/bb8eae18-2ca5-41e6-bde3-1d26b8f0e02f)

Home (Focus sur le Cv créatif)
![Image2](https://github.com/user-attachments/assets/414d1092-ec83-4119-9f03-63e9d8aa7d19)

Merci d’utiliser Doc Pro 5.6
