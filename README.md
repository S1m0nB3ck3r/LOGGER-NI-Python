# Logger NI - Application d'acquisition de données

Application de logging pour cartes National Instruments développée en Python avec architecture MVC.

## 📋 Fonctionnalités

- ✅ Acquisition de données en temps réel avec DAQmx
- ✅ Interface graphique Tkinter moderne
- ✅ Affichage graphique instantané et longue durée
- ✅ Enregistrement des données en CSV
- ✅ Architecture MVC propre et maintenable
- ✅ Support multi-canaux
- ✅ Mode simulation si aucune carte DAQ n'est détectée

## 🏗️ Architecture

```
Logger NI Lent/
├── model/              # Logique métier et acquisition
│   ├── __init__.py
│   ├── daq_model.py    # Gestion DAQmx
│   └── data_model.py   # Gestion des données
├── view/               # Interface graphique
│   ├── __init__.py
│   └── main_view.py    # Interface Tkinter
├── controller/         # Contrôleur
│   ├── __init__.py
│   └── main_controller.py
├── utils/              # Utilitaires
│   ├── __init__.py
│   └── config.py       # Configuration
├── data/               # Dossier de sauvegarde (créé automatiquement)
├── venv/               # Environnement virtuel
├── main.py             # Point d'entrée
└── requirements.txt    # Dépendances
```

## 🚀 Installation

### 1. Cloner le projet ou naviguer dans le dossier

```bash
cd "c:\TRAVAIL\RepositoriesGithub\Logger NI Lent"
```

### 2. Activer l'environnement virtuel

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\venv\Scripts\activate.bat
```

### 3. Vérifier les dépendances (déjà installées)

```bash
pip list
```

## 🎯 Utilisation

### Lancer l'application

```bash
python main.py
```

### Configuration

Modifiez `utils/config.py` pour adapter à votre configuration :

```python
# Nom du périphérique DAQ
DEVICE_NAME = "Dev1"  # Modifiez selon votre carte

# Canaux à acquérir
CHANNELS = [
    "Dev1/ai0",
    "Dev1/ai1"
]

# Fréquence d'échantillonnage (Hz)
SAMPLE_RATE = 1000

# Plage de tension
MIN_VOLTAGE = -10.0
MAX_VOLTAGE = 10.0
```

### Boutons de l'interface

- **▶ Démarrer enregistrement** : Lance l'enregistrement des données
- **◼ Arrêter enregistrement** : Arrête et sauvegarde les données en CSV
- **Attente** : Mode attente (fonctionnalité personnalisable)
- **Quitter [ECHAP]** : Ferme l'application

### Onglets

- **graph instantané** : Affichage en temps réel des dernières données
- **graph longue durée** : Affichage de toutes les données enregistrées

## 📊 Format des données

Les données sont sauvegardées en CSV dans le dossier `data/` :

```
Canal_0,Canal_1
1.234,5.678
1.235,5.679
...
```

## 🛠️ Dépendances

- Python 3.10+
- nidaqmx >= 0.9.0
- matplotlib >= 3.7.0
- numpy >= 1.24.0
- tkinter (inclus avec Python)

## 📝 Notes importantes

### Matériel requis

- Carte d'acquisition National Instruments compatible DAQmx
- Drivers NI-DAQmx installés sur le système

### Mode simulation

Si aucune carte DAQ n'est détectée, l'application affichera un avertissement mais continuera à fonctionner (sans acquisition réelle).

### Raccourcis clavier

- **ECHAP** : Quitter l'application

## 🐛 Dépannage

### Erreur "No module named 'nidaqmx'"

```bash
pip install nidaqmx
```

### Erreur "Cannot find DAQ device"

1. Vérifiez que la carte est connectée
2. Ouvrez NI MAX (Measurement & Automation Explorer)
3. Vérifiez le nom du périphérique
4. Modifiez `DEVICE_NAME` dans `utils/config.py`

### Erreur Tkinter

Sur certains systèmes, Tkinter doit être installé séparément :

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

## 📄 Licence

Projet développé pour usage interne/éducatif.

## 👨‍💻 Auteur

Application développée avec architecture MVC
Python + Tkinter + National Instruments DAQmx
