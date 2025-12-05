# ðŸŽ¯ GUIDE DE DÃ‰MARRAGE RAPIDE - Logger NI

## âœ… Projet crÃ©Ã© avec succÃ¨s !

Votre application de logger National Instruments est prÃªte avec :
- âœ… Architecture MVC complÃ¨te
- âœ… Interface Tkinter moderne
- âœ… API DAQmx Python configurÃ©e
- âœ… Environnement virtuel Python
- âœ… Tous les packages installÃ©s

---

## ðŸš€ LANCEMENT RAPIDE

### Option 1 : Double-clic (le plus simple)
Double-cliquez sur :
- **`run.bat`** (Windows CMD)
- **`run.ps1`** (PowerShell - RecommandÃ©)

### Option 2 : Ligne de commande
```powershell
cd "c:\TRAVAIL\RepositoriesGithub\Logger NI"
.\.venv\Scripts\python.exe main_logger.py
```

---

## ðŸ“ STRUCTURE DU PROJET

```
Logger NI/
â”‚
â”œâ”€â”€ ðŸ“‚ model/                    # ModÃ¨le (Logique mÃ©tier)
â”‚   â”œâ”€â”€ daq_model.py            # Acquisition DAQmx
â”‚   â””â”€â”€ data_model.py           # Gestion des donnÃ©es
â”‚
â”œâ”€â”€ ðŸ“‚ view/                     # Vue (Interface graphique)
â”‚   â””â”€â”€ main_view.py            # Interface Tkinter
â”‚
â”œâ”€â”€ ðŸ“‚ controller/               # ContrÃ´leur
â”‚   â””â”€â”€ main_controller.py      # Orchestration MVC
â”‚
â”œâ”€â”€ ðŸ“‚ utils/                    # Utilitaires
â”‚   â””â”€â”€ config.py               # âš™ï¸ CONFIGURATION ICI
â”‚
â”œâ”€â”€ ðŸ“‚ data/                     # DonnÃ©es sauvegardÃ©es (auto-crÃ©Ã©)
â”‚
â”œâ”€â”€ ðŸ“‚ .venv/                    # Environnement virtuel Python
â”‚
â”œâ”€â”€ ðŸ“„ main_logger.py                   # ðŸŽ¯ Point d'entrÃ©e
â”œâ”€â”€ ðŸ“„ test_installation.py     # Script de test
â”œâ”€â”€ ðŸ“„ run.bat                   # Lanceur Windows CMD
â”œâ”€â”€ ðŸ“„ run.ps1                   # Lanceur PowerShell
â”œâ”€â”€ ðŸ“„ requirements.txt          # DÃ©pendances Python
â”œâ”€â”€ ðŸ“„ README.md                 # Documentation complÃ¨te
â”œâ”€â”€ ðŸ“„ CONFIGURATION.md          # Guide de configuration
â””â”€â”€ ðŸ“„ QUICKSTART.md            # Ce fichier !
```

---

## âš™ï¸ CONFIGURATION DE BASE

### 1ï¸âƒ£ Identifier votre pÃ©riphÃ©rique DAQ

```powershell
.\.venv\Scripts\python.exe test_installation.py
```

**PÃ©riphÃ©riques dÃ©tectÃ©s sur votre systÃ¨me :**
- âœ… Dev3: USB-6421
- TS1, TS1Mod1, TS1Mod2, TS1Mod3, TS1Mod4

### 2ï¸âƒ£ Configurer le pÃ©riphÃ©rique

Ã‰ditez **`utils/config.py`** :

```python
# Ligne 15 environ
DEVICE_NAME = "Dev3"  # ðŸ‘ˆ Changez ici selon votre carte

# Les canaux (ligne 19)
CHANNELS = [
    "Dev3/ai0",  # Canal 0
    "Dev3/ai1",  # Canal 1
]

# FrÃ©quence (ligne 24)
SAMPLE_RATE = 1000  # Hz
```

### 3ï¸âƒ£ Tester

```powershell
.\.venv\Scripts\python.exe test_installation.py
```

Tout doit Ãªtre vert âœ…

### 4ï¸âƒ£ Lancer !

```powershell
.\.venv\Scripts\python.exe main_logger.py
```

---

## ðŸŽ® UTILISATION DE L'INTERFACE

### Boutons disponibles :

1. **â–¶ DÃ©marrer enregistrement**
   - Lance l'enregistrement des donnÃ©es
   - Les donnÃ©es s'accumulent dans le buffer

2. **â—¼ ArrÃªter enregistrement**
   - ArrÃªte l'enregistrement
   - Sauvegarde automatique en CSV dans `data/`
   - Message de confirmation avec le chemin du fichier

3. **Attente**
   - Mode pause/attente
   - Personnalisable dans le code

4. **Quitter [ECHAP]**
   - Ferme l'application proprement
   - Raccourci : touche ECHAP

### Onglets graphiques :

- **graph instantannÃ©** : Affichage temps rÃ©el des derniÃ¨res donnÃ©es
- **graph longue durÃ©e** : Toutes les donnÃ©es enregistrÃ©es

### Affichage mesures :

Coin supÃ©rieur droit : Valeur moyenne du canal 0 en temps rÃ©el

---

## ðŸ“Š FICHIERS DE DONNÃ‰ES

Les donnÃ©es sont automatiquement sauvegardÃ©es dans :

```
Logger NI/data/acquisition_YYYYMMDD_HHMMSS.csv
```

Format CSV compatible Excel :
```csv
Canal_0,Canal_1
1.234,5.678
1.235,5.679
...
```

---

## ðŸ”§ PERSONNALISATION

### Changer les couleurs

Ã‰ditez `utils/config.py` :
```python
COLOR_BACKGROUND = '#e8f4f8'  # Fond de l'application
COLOR_PLOT_BG = '#808080'      # Fond des graphiques
```

### Ajouter des canaux

```python
CHANNELS = [
    "Dev3/ai0",
    "Dev3/ai1",
    "Dev3/ai2",  # ðŸ‘ˆ Ajoutez ici
    "Dev3/ai3",
]
```

### Changer la frÃ©quence

```python
SAMPLE_RATE = 5000  # 5 kHz au lieu de 1 kHz
```

---

## ðŸ› DÃ‰PANNAGE

### ProblÃ¨me : "Device cannot be accessed"
**Solution :** Changez `DEVICE_NAME` dans `utils/config.py`

### ProblÃ¨me : Interface ne s'affiche pas
**Solution :** VÃ©rifiez que Tkinter est installÃ© (normalement inclus)

### ProblÃ¨me : Erreur d'import
**Solution :** Utilisez toujours `.\.venv\Scripts\python.exe` et non `python`

### ProblÃ¨me : Graphique ne se met pas Ã  jour
**Solution :** VÃ©rifiez que la carte DAQ envoie bien des donnÃ©es

---

## ðŸ“š DOCUMENTATION COMPLÃˆTE

- **README.md** : Documentation gÃ©nÃ©rale du projet
- **CONFIGURATION.md** : Guide dÃ©taillÃ© de configuration
- **Code source** : Tous les fichiers sont commentÃ©s

---

## ðŸŽ“ ARCHITECTURE MVC EXPLIQUÃ‰E

### Model (`model/`)
- **daq_model.py** : Communication avec la carte DAQ
  - Acquisition continue
  - Gestion du threading
  - Buffers de donnÃ©es
  
- **data_model.py** : Traitement des donnÃ©es
  - Sauvegarde CSV
  - Statistiques
  - DÃ©cimation pour affichage

### View (`view/`)
- **main_view.py** : Interface graphique
  - Tkinter widgets
  - Matplotlib graphiques
  - Onglets et boutons

### Controller (`controller/`)
- **main_controller.py** : Logique de contrÃ´le
  - Liaison Model â†” View
  - Gestion des Ã©vÃ©nements
  - Mise Ã  jour pÃ©riodique de l'interface

---

## ðŸš€ PROCHAINES Ã‰TAPES

### FonctionnalitÃ©s Ã  ajouter (si besoin) :

1. **Export en format TDMS** (format National Instruments)
2. **DÃ©clenchement** (trigger sur seuil)
3. **Filtrage** (passe-bas, passe-haut)
4. **FFT** (analyse frÃ©quentielle)
5. **Alarmes** (seuils min/max)
6. **Calibration** (facteur d'Ã©chelle, offset)

### Modifiez le code :

Tous les fichiers sont structurÃ©s et commentÃ©s pour faciliter les modifications !

---

## ðŸ’¡ CONSEILS

âœ… **Testez toujours** aprÃ¨s une modification avec `test_installation.py`
âœ… **Sauvegardez rÃ©guliÃ¨rement** votre configuration
âœ… **Consultez NI MAX** pour vÃ©rifier les pÃ©riphÃ©riques
âœ… **Lisez les commentaires** dans le code source

---

## ðŸ“ž AIDE

En cas de problÃ¨me :
1. VÃ©rifiez `test_installation.py`
2. Consultez les messages d'erreur dans le terminal
3. VÃ©rifiez la configuration dans `utils/config.py`
4. Relisez `CONFIGURATION.md`

---

## âœ¨ PROFITEZ DE VOTRE LOGGER NI !

Votre application est prÃªte Ã  l'emploi avec une architecture professionnelle MVC ! ðŸŽ‰

**Bon logging ! ðŸ“ŠðŸ”¬**

