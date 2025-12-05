"""
Logger NI - Application d'acquisition de données National Instruments
Point d'entrée principal de l'application
"""
import tkinter as tk
import sys
import os

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.daq_model import DAQModel
from model.data_model import DataModel
from view.main_view import MainView
from controller.main_controller import MainController
from utils.config import config


def main():
    """
    Fonction principale de l'application
    """
    print("=" * 60)
    print("Logger NI - Application d'acquisition de données")
    print("Architecture MVC - Python + Tkinter + DAQmx")
    print("=" * 60)
    
    # Créer la fenêtre principale Tkinter
    root = tk.Tk()
    
    try:
        # Créer les composants MVC
        print("\nInitialisation des composants...")
        
        # Modèles
        daq_model = DAQModel(config)
        data_model = DataModel(config)
        print("✓ Modèles créés")
        
        # Vue
        view = MainView(root, config)
        print("✓ Vue créée")
        
        # Contrôleur
        controller = MainController(daq_model, data_model, view)
        print("✓ Contrôleur créé")
        
        print("\nDémarrage de l'application...")
        print("-" * 60)
        
        # Lancer l'application
        controller.run()
        
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage de l'application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Nettoyer avant de quitter
        print("\nFermeture de l'application...")
        root.destroy()


if __name__ == "__main__":
    main()
