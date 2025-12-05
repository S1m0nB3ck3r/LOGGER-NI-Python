# Corrections v2.2 - Logger Cuve Expérimentale

## Problèmes corrigés

### 1. ✅ Fréquence d'acquisition correcte
**Problème** : L'acquisition ne respectait pas le timing de 10Hz (1 point toutes les 100ms)

**Solution** :
```python
# config.py
SAMPLES_PER_READ = 1  # Lire 1 point à la fois à 10Hz (au lieu de 100)
TIMEOUT = 1.0  # Timeout adapté (au lieu de 10.0)
```

### 2. ✅ Fenêtre glissante d'1 minute (600 points)
**Problème** : Le graphique instantané n'affichait que 10 secondes (100 points)

**Solution** :
```python
# config.py
INSTANT_HISTORY_SECONDS = 60  # 1 minute
INSTANT_MAX_SAMPLES = SAMPLE_RATE * INSTANT_HISTORY_SECONDS  # 600 points à 10Hz

# daq_model.py
self.max_instantane_samples = config.INSTANT_MAX_SAMPLES  # 600 points
```

**Résultat** : Le graphique instantané affiche maintenant 1 minute d'historique glissant (600 points maximum)

### 3. ✅ Adaptation dynamique des légendes
**Problème** : Les légendes étaient fixes ("Canal 0", "Canal 1") même si la tâche avait un nombre différent de canaux

**Solution** :

#### a) Détection des canaux dans le modèle DAQ
```python
# daq_model.py
def initialize_task(self):
    self.channel_names = []
    for channel in self.config.CHANNELS:
        ai_channel = self.task.ai_channels.add_ai_voltage_chan(...)
        self.channel_names.append(ai_channel.name)  # Récupère le nom réel
    
    print(f"✓ {self.n_channels} canal(aux) configuré(s): {', '.join(self.channel_names)}")

def get_channel_names(self):
    return self.channel_names
```

#### b) Graphiques dynamiques dans la vue
```python
# view/main_view.py
def _create_plots(self, tab1, tab2):
    # Couleurs pour jusqu'à 8 canaux
    self.plot_colors = [
        self.colors['accent_blue'],
        self.colors['accent_purple'],
        self.colors['accent_green'],
        self.colors['accent_yellow'],
        self.colors['accent_red'],
        '#ff6b9d',  # Rose
        '#00d4ff',  # Cyan
        '#ffaa00',  # Orange
    ]
    
    # Lignes créées dynamiquement (au lieu de lignes fixes)
    self.lines_instant = []
    self.lines_long = []

def setup_plot_channels(self, channel_names):
    """Configure les lignes de graphique selon les noms de canaux"""
    # Supprime les anciennes lignes
    for line in self.lines_instant:
        line.remove()
    
    # Crée les nouvelles lignes
    for i, channel_name in enumerate(channel_names):
        color = self.plot_colors[i % len(self.plot_colors)]
        line, = self.ax_instant.plot([], [], color=color, linewidth=2.5, 
                                     label=channel_name, alpha=0.9)
        self.lines_instant.append(line)
    
    # Met à jour la légende
    legend = self.ax_instant.legend(...)
```

#### c) Mise à jour dynamique dans le contrôleur
```python
# controller/main_controller.py
def initialize(self):
    success = self.daq_model.start_acquisition(...)
    
    if success:
        # Configurer les graphiques avec les canaux détectés
        channel_names = self.daq_model.get_channel_names()
        if channel_names:
            self.view.setup_plot_channels(channel_names)
```

#### d) Méthodes update adaptées
```python
# view/main_view.py
def update_instantane_plot(self, data, timestamps=None):
    # Mettre à jour chaque canal dynamiquement
    for i in range(min(data.shape[0], len(self.lines_instant))):
        self.lines_instant[i].set_data(time_axis, data[i, :])
```

## Résultats

### Console au démarrage
```
✓ 2 canal(aux) configuré(s): Dev3/ai0, Dev3/ai1
✓ 2 canal(aux) configuré(s) dans les graphiques: Dev3/ai0, Dev3/ai1
Acquisition démarrée à 10 Hz
```

### Capacités
- ✅ Jusqu'à **8 canaux** supportés (extensible facilement)
- ✅ Noms de canaux **réels** affichés dans la légende (ex: "Dev3/ai0", "Dev3/ai1")
- ✅ Couleurs **différentes** pour chaque canal
- ✅ **Ajustement automatique** selon le nombre de canaux de la tâche
- ✅ Fenêtre glissante de **60 secondes** (600 points à 10Hz)
- ✅ Acquisition à **10Hz exactement** (1 point toutes les 100ms)

## Fichiers modifiés

### `utils/config.py`
- `SAMPLES_PER_READ = 1` (au lieu de 100)
- `TIMEOUT = 1.0` (au lieu de 10.0)
- Ajout : `INSTANT_HISTORY_SECONDS = 60`
- Ajout : `INSTANT_MAX_SAMPLES = 600`

### `model/daq_model.py`
- `self.max_instantane_samples = config.INSTANT_MAX_SAMPLES`
- `self.channel_names = []` pour stocker les noms
- `self.n_channels` pour le compteur
- `initialize_task()` : Récupère et affiche les noms de canaux
- Ajout : `get_channel_names()` et `get_channel_count()`

### `view/main_view.py`
- `self.plot_colors` : Liste de 8 couleurs
- `self.lines_instant = []` et `self.lines_long = []` (listes dynamiques)
- Ajout : `setup_plot_channels(channel_names)` pour configuration dynamique
- `update_instantane_plot()` : Boucle sur tous les canaux
- `update_longue_duree_plot()` : Boucle sur tous les canaux
- Axe X du graphique instantané : `set_xlim(0, 60)` au lieu de `set_xlim(0, 10)`

### `controller/main_controller.py`
- Appel de `self.view.setup_plot_channels(channel_names)` après démarrage acquisition

## Tests effectués

✅ Démarrage avec 2 canaux (Dev3/ai0, Dev3/ai1)  
✅ Détection automatique des canaux  
✅ Légendes correctes dans les graphiques  
✅ Couleurs différenciées  
✅ Pas d'erreurs au démarrage  

## À tester manuellement

- [ ] Changer la tâche sélectionnée (avec plus ou moins de canaux)
- [ ] Vérifier que les légendes s'adaptent
- [ ] Observer la fenêtre glissante d'1 minute
- [ ] Démarrer un enregistrement et vérifier le CSV
- [ ] Vérifier que chaque canal a bien sa propre couleur

## Prochaines améliorations possibles

1. **Rechargement dynamique lors du changement de tâche**
   - Actuellement, changer la tâche dans le menu déroulant ne redémarre pas l'acquisition
   - Il faudrait arrêter et redémarrer l'acquisition avec la nouvelle tâche

2. **Support de plus de 8 canaux**
   - Actuellement limité à 8 couleurs
   - Possibilité de générer des couleurs automatiquement ou d'utiliser des styles de ligne

3. **Indicateur visuel du buffer**
   - Barre de progression montrant le remplissage du buffer (0 à 600 points)

4. **Zoom et pan sur les graphiques**
   - Permettre à l'utilisateur de zoomer/déplacer les graphiques
