# 🎯 GUIDE DE DÉMARRAGE RAPIDE - Logger NI

## ✅ Projet créé avec succès !

Votre application de logger National Instruments est prête avec :
- ✅ Architecture MVC complète
- ✅ Interface Tkinter moderne
- ✅ API DAQmx Python configurée
- ✅ Environnement virtuel Python
- ✅ Tous les packages installés

---

## 🚀 LANCEMENT RAPIDE

### Option 1 : Double-clic (le plus simple)
Double-cliquez sur :
- **`run.bat`** (Windows CMD)
- **`run.ps1`** (PowerShell - Recommandé)

### Option 2 : Ligne de commande
```powershell
cd "c:\TRAVAIL\RepositoriesGithub\Logger NI Lent"
.\.venv\Scripts\python.exe main.py
```

---

## 📁 STRUCTURE DU PROJET

```
Logger NI Lent/
│
├── 📂 model/                    # Modèle (Logique métier)
│   ├── daq_model.py            # Acquisition DAQmx
│   └── data_model.py           # Gestion des données
│
├── 📂 view/                     # Vue (Interface graphique)
│   └── main_view.py            # Interface Tkinter
│
├── 📂 controller/               # Contrôleur
│   └── main_controller.py      # Orchestration MVC
│
├── 📂 utils/                    # Utilitaires
│   └── config.py               # ⚙️ CONFIGURATION ICI
│
├── 📂 data/                     # Données sauvegardées (auto-créé)
│
├── 📂 .venv/                    # Environnement virtuel Python
│
├── 📄 main.py                   # 🎯 Point d'entrée
├── 📄 test_installation.py     # Script de test
├── 📄 run.bat                   # Lanceur Windows CMD
├── 📄 run.ps1                   # Lanceur PowerShell
├── 📄 requirements.txt          # Dépendances Python
├── 📄 README.md                 # Documentation complète
├── 📄 CONFIGURATION.md          # Guide de configuration
└── 📄 QUICKSTART.md            # Ce fichier !
```

---

## ⚙️ CONFIGURATION DE BASE

### 1️⃣ Identifier votre périphérique DAQ

```powershell
.\.venv\Scripts\python.exe test_installation.py
```

**Périphériques détectés sur votre système :**
- ✅ Dev3: USB-6421
- TS1, TS1Mod1, TS1Mod2, TS1Mod3, TS1Mod4

### 2️⃣ Configurer le périphérique

Éditez **`utils/config.py`** :

```python
# Ligne 15 environ
DEVICE_NAME = "Dev3"  # 👈 Changez ici selon votre carte

# Les canaux (ligne 19)
CHANNELS = [
    "Dev3/ai0",  # Canal 0
    "Dev3/ai1",  # Canal 1
]

# Fréquence (ligne 24)
SAMPLE_RATE = 1000  # Hz
```

### 3️⃣ Tester

```powershell
.\.venv\Scripts\python.exe test_installation.py
```

Tout doit être vert ✅

### 4️⃣ Lancer !

```powershell
.\.venv\Scripts\python.exe main.py
```

---

## 🎮 UTILISATION DE L'INTERFACE

### Boutons disponibles :

1. **▶ Démarrer enregistrement**
   - Lance l'enregistrement des données
   - Les données s'accumulent dans le buffer

2. **◼ Arrêter enregistrement**
   - Arrête l'enregistrement
   - Sauvegarde automatique en CSV dans `data/`
   - Message de confirmation avec le chemin du fichier

3. **Attente**
   - Mode pause/attente
   - Personnalisable dans le code

4. **Quitter [ECHAP]**
   - Ferme l'application proprement
   - Raccourci : touche ECHAP

### Onglets graphiques :

- **graph instantanné** : Affichage temps réel des dernières données
- **graph longue durée** : Toutes les données enregistrées

### Affichage mesures :

Coin supérieur droit : Valeur moyenne du canal 0 en temps réel

---

## 📊 FICHIERS DE DONNÉES

Les données sont automatiquement sauvegardées dans :

```
Logger NI Lent/data/acquisition_YYYYMMDD_HHMMSS.csv
```

Format CSV compatible Excel :
```csv
Canal_0,Canal_1
1.234,5.678
1.235,5.679
...
```

---

## 🔧 PERSONNALISATION

### Changer les couleurs

Éditez `utils/config.py` :
```python
COLOR_BACKGROUND = '#e8f4f8'  # Fond de l'application
COLOR_PLOT_BG = '#808080'      # Fond des graphiques
```

### Ajouter des canaux

```python
CHANNELS = [
    "Dev3/ai0",
    "Dev3/ai1",
    "Dev3/ai2",  # 👈 Ajoutez ici
    "Dev3/ai3",
]
```

### Changer la fréquence

```python
SAMPLE_RATE = 5000  # 5 kHz au lieu de 1 kHz
```

---

## 🐛 DÉPANNAGE

### Problème : "Device cannot be accessed"
**Solution :** Changez `DEVICE_NAME` dans `utils/config.py`

### Problème : Interface ne s'affiche pas
**Solution :** Vérifiez que Tkinter est installé (normalement inclus)

### Problème : Erreur d'import
**Solution :** Utilisez toujours `.\.venv\Scripts\python.exe` et non `python`

### Problème : Graphique ne se met pas à jour
**Solution :** Vérifiez que la carte DAQ envoie bien des données

---

## 📚 DOCUMENTATION COMPLÈTE

- **README.md** : Documentation générale du projet
- **CONFIGURATION.md** : Guide détaillé de configuration
- **Code source** : Tous les fichiers sont commentés

---

## 🎓 ARCHITECTURE MVC EXPLIQUÉE

### Model (`model/`)
- **daq_model.py** : Communication avec la carte DAQ
  - Acquisition continue
  - Gestion du threading
  - Buffers de données
  
- **data_model.py** : Traitement des données
  - Sauvegarde CSV
  - Statistiques
  - Décimation pour affichage

### View (`view/`)
- **main_view.py** : Interface graphique
  - Tkinter widgets
  - Matplotlib graphiques
  - Onglets et boutons

### Controller (`controller/`)
- **main_controller.py** : Logique de contrôle
  - Liaison Model ↔ View
  - Gestion des événements
  - Mise à jour périodique de l'interface

---

## 🚀 PROCHAINES ÉTAPES

### Fonctionnalités à ajouter (si besoin) :

1. **Export en format TDMS** (format National Instruments)
2. **Déclenchement** (trigger sur seuil)
3. **Filtrage** (passe-bas, passe-haut)
4. **FFT** (analyse fréquentielle)
5. **Alarmes** (seuils min/max)
6. **Calibration** (facteur d'échelle, offset)

### Modifiez le code :

Tous les fichiers sont structurés et commentés pour faciliter les modifications !

---

## 💡 CONSEILS

✅ **Testez toujours** après une modification avec `test_installation.py`
✅ **Sauvegardez régulièrement** votre configuration
✅ **Consultez NI MAX** pour vérifier les périphériques
✅ **Lisez les commentaires** dans le code source

---

## 📞 AIDE

En cas de problème :
1. Vérifiez `test_installation.py`
2. Consultez les messages d'erreur dans le terminal
3. Vérifiez la configuration dans `utils/config.py`
4. Relisez `CONFIGURATION.md`

---

## ✨ PROFITEZ DE VOTRE LOGGER NI !

Votre application est prête à l'emploi avec une architecture professionnelle MVC ! 🎉

**Bon logging ! 📊🔬**
