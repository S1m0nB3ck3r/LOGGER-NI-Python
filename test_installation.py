"""
Script de test pour vérifier l'installation et la configuration
"""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test des imports de modules"""
    print("Test des imports...")
    
    try:
        import tkinter as tk
        print("  ✓ Tkinter disponible")
    except ImportError as e:
        print(f"  ✗ Erreur Tkinter: {e}")
        return False
    
    try:
        import numpy as np
        print(f"  ✓ NumPy {np.__version__} disponible")
    except ImportError as e:
        print(f"  ✗ Erreur NumPy: {e}")
        return False
    
    try:
        import matplotlib
        print(f"  ✓ Matplotlib {matplotlib.__version__} disponible")
    except ImportError as e:
        print(f"  ✗ Erreur Matplotlib: {e}")
        return False
    
    try:
        import nidaqmx
        print(f"  ✓ NI-DAQmx Python disponible")
    except ImportError as e:
        print(f"  ✗ Erreur NI-DAQmx: {e}")
        return False
    
    return True


def test_modules():
    """Test des modules de l'application"""
    print("\nTest des modules de l'application...")
    
    try:
        from model.daq_model import DAQModel
        print("  ✓ DAQModel importé")
    except ImportError as e:
        print(f"  ✗ Erreur DAQModel: {e}")
        return False
    
    try:
        from model.data_model import DataModel
        print("  ✓ DataModel importé")
    except ImportError as e:
        print(f"  ✗ Erreur DataModel: {e}")
        return False
    
    try:
        from view.main_view import MainView
        print("  ✓ MainView importé")
    except ImportError as e:
        print(f"  ✗ Erreur MainView: {e}")
        return False
    
    try:
        from controller.main_controller import MainController
        print("  ✓ MainController importé")
    except ImportError as e:
        print(f"  ✗ Erreur MainController: {e}")
        return False
    
    try:
        from utils.config import config
        print("  ✓ Config importé")
    except ImportError as e:
        print(f"  ✗ Erreur Config: {e}")
        return False
    
    return True


def test_daq_devices():
    """Test de détection des périphériques DAQ"""
    print("\nTest de détection des périphériques DAQ...")
    
    try:
        import nidaqmx
        from nidaqmx.system import System
        
        system = System.local()
        devices = system.devices
        
        if len(devices) > 0:
            print(f"  ✓ {len(devices)} périphérique(s) détecté(s):")
            for device in devices:
                print(f"    - {device.name}: {device.product_type}")
        else:
            print("  ⚠ Aucun périphérique DAQ détecté")
            print("    L'application fonctionnera en mode simulation")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur lors de la détection: {e}")
        return False


def test_config():
    """Test de la configuration"""
    print("\nTest de la configuration...")
    
    try:
        from utils.config import config
        
        print(f"  ✓ Périphérique: {config.DEVICE_NAME}")
        print(f"  ✓ Canaux: {config.CHANNELS}")
        print(f"  ✓ Fréquence d'échantillonnage: {config.SAMPLE_RATE} Hz")
        print(f"  ✓ Plage de tension: {config.MIN_VOLTAGE}V à {config.MAX_VOLTAGE}V")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur de configuration: {e}")
        return False


def main():
    """Fonction principale de test"""
    print("=" * 70)
    print("Test de l'installation Logger NI")
    print("=" * 70)
    
    all_tests_passed = True
    
    # Test des imports
    if not test_imports():
        all_tests_passed = False
    
    # Test des modules
    if not test_modules():
        all_tests_passed = False
    
    # Test des périphériques DAQ
    if not test_daq_devices():
        all_tests_passed = False
    
    # Test de la configuration
    if not test_config():
        all_tests_passed = False
    
    # Résumé
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("✓ Tous les tests sont passés avec succès!")
        print("\nVous pouvez lancer l'application avec:")
        print("  python main.py")
    else:
        print("✗ Certains tests ont échoué")
        print("\nVérifiez les erreurs ci-dessus avant de lancer l'application")
    print("=" * 70)
    
    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
