# 🚀 Guide : Créer un repository Git et pousser Logger NI sur GitHub

## 📋 Méthode 1 : Via l'interface GitHub (RECOMMANDÉ pour débutants)

### Étape 1 : Créer le repository sur GitHub

1. **Aller sur GitHub** : https://github.com
2. **Se connecter** à votre compte
3. Cliquer sur le **bouton "+" en haut à droite** → "New repository"
4. **Remplir les informations** :
   - Repository name : `Logger-NI` (ou `logger-ni`)
   - Description : "Application d'acquisition de données National Instruments avec interface Tkinter"
   - **Public** ou **Private** (votre choix)
   - ❌ **NE PAS cocher** "Initialize this repository with a README" (on a déjà des fichiers)
   - ❌ **NE PAS ajouter** .gitignore pour l'instant
   - ❌ **NE PAS ajouter** de licence pour l'instant
5. Cliquer sur **"Create repository"**

### Étape 2 : Initialiser Git localement

Ouvrir PowerShell dans le dossier du projet et exécuter :

```powershell
cd "C:\TRAVAIL\RepositoriesGithub\Logger NI"

# Initialiser Git (si pas déjà fait)
git init

# Configurer votre identité (si première fois)
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"
```

### Étape 3 : Créer un fichier .gitignore

```powershell
# Créer le fichier .gitignore pour exclure les fichiers inutiles
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
build/
dist/
*.spec

# Jupyter Notebook
.ipynb_checkpoints

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Fichiers de données (optionnel - à vous de décider)
data/*.txt
!data/.gitkeep

# Logs
*.log

# Configuration locale (si vous voulez garder logger_config.json privé)
# logger_config.json
"@ | Out-File -FilePath .gitignore -Encoding utf8
```

### Étape 4 : Ajouter tous les fichiers

```powershell
# Ajouter tous les fichiers au staging
git add .

# Vérifier ce qui va être commité
git status

# Faire le premier commit
git commit -m "Initial commit: Logger NI v2.3 - Application d'acquisition DAQmx"
```

### Étape 5 : Connecter au repository GitHub

GitHub vous donne les commandes après création du repo. Ce sera quelque chose comme :

```powershell
# Remplacer VOTRE-USERNAME et Logger-NI par vos valeurs
git remote add origin https://github.com/VOTRE-USERNAME/Logger-NI.git

# Renommer la branche en main (si nécessaire)
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

### Étape 6 : Entrer vos identifiants

- **Username** : votre nom d'utilisateur GitHub
- **Password** : **Personal Access Token** (PAS votre mot de passe !)

#### Comment créer un Personal Access Token :

1. Sur GitHub → **Settings** (votre profil) → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **Generate new token** → **Generate new token (classic)**
4. Cocher : `repo` (accès complet aux repos)
5. **Generate token**
6. **COPIER LE TOKEN** (vous ne pourrez plus le revoir !)
7. Utiliser ce token comme "password" lors du push

---

## 📋 Méthode 2 : Commandes complètes (tout en une fois)

```powershell
# Naviguer vers le projet
cd "C:\TRAVAIL\RepositoriesGithub\Logger NI"

# Initialiser Git
git init

# Configurer l'utilisateur (première fois seulement)
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"

# Créer .gitignore (voir contenu ci-dessus)
# ... créer le fichier .gitignore ...

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Logger NI v2.3"

# Connecter à GitHub (REMPLACER par votre URL)
git remote add origin https://github.com/VOTRE-USERNAME/Logger-NI.git

# Renommer la branche
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

---

## 📋 Méthode 3 : Utiliser GitHub Desktop (PLUS FACILE)

### Étape 1 : Installer GitHub Desktop

1. Télécharger : https://desktop.github.com/
2. Installer et se connecter avec votre compte GitHub

### Étape 2 : Ajouter le projet

1. **File** → **Add local repository**
2. Sélectionner : `C:\TRAVAIL\RepositoriesGithub\Logger NI`
3. Cliquer sur **"create a repository"** si Git n'est pas initialisé
4. Remplir les informations

### Étape 3 : Publier

1. Créer le fichier `.gitignore` (voir contenu ci-dessus)
2. Cliquer sur **"Publish repository"**
3. Choisir **Public** ou **Private**
4. Cliquer sur **"Publish Repository"**

✅ C'est fait ! Tout est sur GitHub !

---

## 📁 Structure recommandée du repository

```
Logger-NI/
├── .gitignore                    ← Fichiers à ignorer
├── README.md                     ← Description du projet
├── requirements.txt              ← Dépendances Python
├── main_logger.py                ← Point d'entrée
├── logger_config.json            ← Configuration (optionnel)
├── architecture.py               ← Documentation architecture
├── BUILD_EXECUTABLE.md           ← Guide de build
├── INSTALLATION_DEPLOIEMENT.md   ← Guide d'installation
├── TIMESTAMP_IMPROVEMENT.md      ← Documentation timestamps
├── QUICKSTART.md                 ← Guide rapide
├── controller/                   ← Contrôleurs MVC
│   ├── __init__.py
│   └── main_controller.py
├── model/                        ← Modèles MVC
│   ├── __init__.py
│   ├── daq_model.py
│   └── data_model.py
├── view/                         ← Vues MVC
│   ├── __init__.py
│   └── main_view.py
├── utils/                        ← Utilitaires
│   ├── __init__.py
│   ├── config.py
│   ├── daq_utils.py
│   └── settings_manager.py
├── data/                         ← Données (peut être ignoré)
│   └── .gitkeep
└── logger_ni.spec                ← Configuration PyInstaller (optionnel)
```

---

## ✅ Fichiers à INCLURE dans Git

- ✅ Tous les fichiers `.py`
- ✅ `requirements.txt`
- ✅ Documentation `.md`
- ✅ `logger_config.json` (optionnel - contient config par défaut)
- ✅ `.gitignore`
- ✅ `README.md`

## ❌ Fichiers à EXCLURE de Git (.gitignore)

- ❌ `__pycache__/` - Fichiers compilés Python
- ❌ `.venv/` - Environnement virtuel
- ❌ `build/` et `dist/` - Fichiers de build PyInstaller
- ❌ `data/*.txt` - Fichiers de données (sauf si vous voulez les partager)
- ❌ `.pyc` - Bytecode Python

---

## 📝 Créer un bon README.md

```markdown
# 🧪 Logger NI

Application d'acquisition de données pour cartes National Instruments DAQmx avec interface graphique Tkinter.

## ✨ Fonctionnalités

- 📊 Acquisition temps réel à 10 Hz
- 💾 Enregistrement continu en fichiers TXT
- 📈 Graphiques en temps réel (instantané et long terme)
- ⏱️ Timestamps ultra-précis (basés sur compteur de points)
- 🎯 Support multi-canaux
- 🔧 Configuration via NI MAX
- 💻 Interface graphique moderne

## 🚀 Installation rapide

### Prérequis

- Python 3.10+
- NI-DAQmx Runtime ou SDK

### Installation

\`\`\`bash
# Cloner le repository
git clone https://github.com/VOTRE-USERNAME/Logger-NI.git
cd Logger-NI

# Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main_logger.py
\`\`\`

## 📦 Créer un exécutable

\`\`\`bash
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
build_exe.bat
\`\`\`

L'exécutable se trouve dans `dist/LoggerNI.exe`

## 📚 Documentation

- [Guide rapide](QUICKSTART.md)
- [Installation et déploiement](INSTALLATION_DEPLOIEMENT.md)
- [Créer un exécutable](BUILD_EXECUTABLE.md)
- [Architecture du projet](architecture.py)
- [Amélioration des timestamps](TIMESTAMP_IMPROVEMENT.md)

## 🛠️ Architecture

Architecture MVC (Model-View-Controller) :
- **Model** : Gestion DAQ et données
- **View** : Interface Tkinter
- **Controller** : Logique métier

## 📄 Licence

[Votre licence - ex: MIT, GPL, etc.]

## 👤 Auteur

Votre Nom
\`\`\`

---

## 🔄 Commandes Git utiles pour la suite

```powershell
# Voir l'état des fichiers
git status

# Ajouter des modifications
git add .
git commit -m "Description des changements"

# Pousser vers GitHub
git push

# Récupérer les changements
git pull

# Créer une branche
git checkout -b nouvelle-fonctionnalite

# Revenir à main
git checkout main

# Fusionner une branche
git merge nouvelle-fonctionnalite

# Voir l'historique
git log --oneline --graph
```

---

## 🎯 Checklist avant le premier push

- [ ] Créer le repository sur GitHub
- [ ] Initialiser Git localement (`git init`)
- [ ] Créer `.gitignore`
- [ ] Créer `README.md`
- [ ] Vérifier que les fichiers sensibles sont exclus
- [ ] Faire le premier commit
- [ ] Connecter au remote GitHub
- [ ] Pousser vers GitHub
- [ ] Vérifier sur GitHub que tout est là

---

## ❓ Problèmes courants

### "Permission denied" lors du push
→ Utiliser un **Personal Access Token** au lieu du mot de passe

### Trop de fichiers à commiter
→ Vérifier le `.gitignore`

### "fatal: not a git repository"
→ Faire `git init` d'abord

### Le dossier `.venv` est inclus
→ Ajouter `.venv/` dans `.gitignore` et faire `git rm -r --cached .venv`

---

**Bonne chance avec votre repository GitHub ! 🚀**
