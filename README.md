# 🎬 YouTube Downloader Pro

Application Desktop moderne pour télécharger des vidéos YouTube avec une interface graphique élégante.

## 🚀 Fonctionnalités

- ✅ Interface graphique moderne avec design sombre
- ✅ Téléchargement de vidéos YouTube en plusieurs formats (MP4, MP3, WEBM)
- ✅ Choix de la qualité (1080p, 720p, 480p, Audio uniquement)
- ✅ Barre de progression en temps réel
- ✅ Affichage de la vitesse de téléchargement
- ✅ Sélection du dossier de destination
- ✅ Validation des URLs YouTube
- ✅ Gestion des erreurs
- ✅ Boutons Pause, Annuler, Effacer

## 📋 Prérequis

- Python 3.7 ou supérieur
- Windows (testé sur Windows 10/11)

## 🔧 Installation

1. Clonez ou téléchargez ce projet

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. (Optionnel) Pour la conversion MP3, installez FFmpeg :
   - Téléchargez FFmpeg depuis https://ffmpeg.org/download.html
   - Ajoutez FFmpeg au PATH de Windows

## 🎮 Utilisation

1. Lancez l'application :
```bash
python youtube_downloader_pro.py
```

2. Cliquez sur "Dossier" pour sélectionner où sauvegarder les vidéos

3. Collez l'URL YouTube dans le champ "Lien YouTube"

4. Choisissez le format (MP4, MP3, WEBM) et la qualité

5. Cliquez sur "Télécharger"

6. Suivez la progression en temps réel

## 🎨 Interface

L'interface comprend :
- **Bouton Dossier** : Sélection du dossier de destination
- **Champ URL** : Pour coller le lien YouTube
- **Menus déroulants** : Choix du format et de la qualité
- **Bouton Télécharger** : Lance le téléchargement
- **Barre de progression** : Affiche l'avancement en %
- **Boutons de contrôle** : Pause, Annuler, Effacer
- **Zone d'informations** : Vitesse, taille, temps restant

## ⚠️ Notes

- La fonction Pause/Reprise est en développement
- Pour télécharger en MP3, FFmpeg doit être installé
- Assurez-vous d'avoir une connexion internet stable
- Respectez les droits d'auteur lors du téléchargement

## 🛠️ Technologies utilisées

- **Python** : Langage de programmation
- **tkinter** : Interface graphique
- **yt-dlp** : Téléchargement YouTube
- **threading** : Téléchargement asynchrone

## 📝 Licence

Ce projet est à usage éducatif uniquement.
