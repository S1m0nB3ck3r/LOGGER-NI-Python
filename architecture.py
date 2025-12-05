"""
Visualisation de l'architecture MVC du Logger NI
Génère un schéma de l'architecture
"""


def print_architecture():
    """Affiche un schéma ASCII de l'architecture MVC"""
    
    schema = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ARCHITECTURE MVC - LOGGER NI                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

                               ┌─────────────┐
                               │   main.py   │
                               │ (Point      │
                               │  d'entrée)  │
                               └──────┬──────┘
                                      │
                                      │ initialise
                                      ▼
                    ┌─────────────────────────────────┐
                    │      CONTROLLER                 │
                    │   main_controller.py            │
                    │                                 │
                    │  • Orchestration MVC            │
                    │  • Gestion événements           │
                    │  • Timer mise à jour UI         │
                    └────┬──────────────────┬─────────┘
                         │                  │
         ┌───────────────┘                  └───────────────┐
         │                                                  │
         │ utilise                                    utilise│
         ▼                                                  ▼
┌─────────────────┐                              ┌──────────────────┐
│     MODEL       │                              │      VIEW        │
├─────────────────┤                              ├──────────────────┤
│                 │                              │                  │
│ daq_model.py    │◄────── données ─────────────►│  main_view.py    │
│                 │                              │                  │
│ • DAQmx API     │                              │ • Tkinter UI     │
│ • Threading     │                              │ • Matplotlib     │
│ • Acquisition   │                              │ • Graphiques     │
│ • Buffers       │                              │ • Boutons        │
│                 │                              │ • Onglets        │
└────────┬────────┘                              └──────────────────┘
         │                                                  ▲
         │ utilise                                          │
         ▼                                           callbacks│
┌─────────────────┐                                         │
│ data_model.py   │                                         │
│                 │                                         │
│ • Sauvegarde    │─────────────────────────────────────────┘
│ • Statistiques  │         notifie succès
│ • Décimation    │
│ • Export CSV    │
└────────┬────────┘
         │
         │ utilise
         ▼
┌─────────────────┐
│  utils/         │
│  config.py      │
│                 │
│ • Paramètres    │
│ • Configuration │
└────────┬────────┘
         │
         │ sauvegarde dans
         ▼
┌─────────────────┐
│   data/         │
│  *.csv          │
│                 │
│ • Fichiers de   │
│   données       │
└─────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                        FLUX DE DONNÉES                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  1. Utilisateur clique "Démarrer" sur VIEW
                      │
                      ▼
  2. VIEW appelle callback → CONTROLLER.start_recording()
                      │
                      ▼
  3. CONTROLLER appelle → MODEL.daq_model.start_recording()
                      │
                      ▼
  4. DAQ Model acquiert données (thread séparé)
                      │
                      ▼
  5. Timer du CONTROLLER (toutes les 100ms)
                      │
                      ▼
  6. CONTROLLER récupère données du MODEL
                      │
                      ▼
  7. CONTROLLER met à jour VIEW avec nouvelles données
                      │
                      ▼
  8. VIEW affiche les graphiques mis à jour
                      │
                      ▼
  9. Utilisateur clique "Arrêter"
                      │
                      ▼
 10. CONTROLLER → MODEL.daq_model.stop_recording()
                      │
                      ▼
 11. CONTROLLER → MODEL.data_model.save_to_csv()
                      │
                      ▼
 12. Fichier CSV sauvegardé dans data/


╔══════════════════════════════════════════════════════════════════════════════╗
║                    COMMUNICATION HARDWARE                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Capteur/Signal → Carte NI → Driver DAQmx → API Python nidaqmx
                                                      │
                                                      ▼
                                              daq_model.py
                                                      │
                                                      ▼
                                         Buffer (numpy array)
                                                      │
                                                      ▼
                                    Affichage Matplotlib


╔══════════════════════════════════════════════════════════════════════════════╗
║                        THREADING                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────┐              ┌─────────────────────┐
│  Thread Principal   │              │  Thread Acquisition │
│  (GUI Tkinter)      │              │  (DAQ)              │
│                     │              │                     │
│ • Interface         │              │ • Lecture continue  │
│ • Événements        │              │ • Bufferisation     │
│ • Affichage         │◄────data─────┤ • Sans bloquer UI   │
│ • Timer update      │              │                     │
└─────────────────────┘              └─────────────────────┘

"""
    
    print(schema)


if __name__ == "__main__":
    print_architecture()
