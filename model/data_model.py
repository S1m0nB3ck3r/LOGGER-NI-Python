"""
Modèle de données - Gestion du stockage et de l'export des données
"""
import numpy as np
from datetime import datetime
import csv
import os


class DataModel:
    """
    Classe pour gérer le stockage, l'export et le traitement des données
    """
    
    def __init__(self, config):
        """
        Initialise le modèle de données
        
        Args:
            config: Objet de configuration
        """
        self.config = config
        self.recording_start_time = None
        self.current_file_path = None
        
    def save_to_csv(self, data, filename=None):
        """
        Sauvegarde les données dans un fichier CSV
        
        Args:
            data: Données à sauvegarder (numpy array)
            filename: Nom du fichier (optionnel)
        
        Returns:
            str: Chemin du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"acquisition_{timestamp}.csv"
        
        # Créer le dossier data s'il n'existe pas
        data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_folder, exist_ok=True)
        
        filepath = os.path.join(data_folder, filename)
        
        try:
            # Si data est vide
            if data is None or (isinstance(data, np.ndarray) and data.size == 0):
                print("Aucune donnée à sauvegarder")
                return None
            
            # Convertir en numpy array si nécessaire
            if not isinstance(data, np.ndarray):
                data = np.array(data)
            
            # Assurer que data est 2D
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            # Transposer pour avoir les échantillons en lignes
            data_transposed = data.T
            
            # Sauvegarder en CSV
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # En-tête
                header = [f"Canal_{i}" for i in range(data.shape[0])]
                writer.writerow(header)
                
                # Données
                writer.writerows(data_transposed)
            
            print(f"Données sauvegardées dans: {filepath}")
            self.current_file_path = filepath
            return filepath
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return None
    
    def get_statistics(self, data, channel_index=0):
        """
        Calcule les statistiques sur un canal de données
        
        Args:
            data: Données (numpy array)
            channel_index: Index du canal
        
        Returns:
            dict: Dictionnaire avec les statistiques
        """
        if data is None or (isinstance(data, np.ndarray) and data.size == 0):
            return {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'rms': 0.0
            }
        
        try:
            # Convertir en numpy array si nécessaire
            if not isinstance(data, np.ndarray):
                data = np.array(data)
            
            # Assurer que data est 2D
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            # Extraire le canal
            if channel_index >= data.shape[0]:
                channel_index = 0
            
            channel_data = data[channel_index, :]
            
            # Calculer les statistiques
            stats = {
                'mean': float(np.mean(channel_data)),
                'std': float(np.std(channel_data)),
                'min': float(np.min(channel_data)),
                'max': float(np.max(channel_data)),
                'rms': float(np.sqrt(np.mean(channel_data**2)))
            }
            
            return stats
            
        except Exception as e:
            print(f"Erreur lors du calcul des statistiques: {e}")
            return {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'rms': 0.0
            }
    
    def decimate_data(self, data, factor=10):
        """
        Décime les données pour l'affichage (réduit le nombre de points)
        
        Args:
            data: Données à décimer
            factor: Facteur de décimation
        
        Returns:
            numpy.ndarray: Données décimées
        """
        if data is None or (isinstance(data, np.ndarray) and data.size == 0):
            return np.array([])
        
        try:
            # Convertir en numpy array si nécessaire
            if not isinstance(data, np.ndarray):
                data = np.array(data)
            
            # Décimer
            if len(data.shape) == 1:
                return data[::factor]
            else:
                return data[:, ::factor]
                
        except Exception as e:
            print(f"Erreur lors de la décimation: {e}")
            return data
