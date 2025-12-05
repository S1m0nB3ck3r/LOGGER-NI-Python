"""
Modèle DAQ - Gestion de l'acquisition de données avec National Instruments DAQmx
"""
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import numpy as np
import threading
import time
from datetime import datetime
import csv
import os


class DAQModel:
    """
    Classe pour gérer l'acquisition de données avec une carte NI DAQmx
    """
    
    def __init__(self, config):
        """
        Initialise le modèle DAQ
        
        Args:
            config: Objet de configuration contenant les paramètres DAQ
        """
        self.config = config
        self.task = None
        self.is_running = False
        self.is_recording = False
        self.acquisition_thread = None
        self.data_callback = None
        
        # Buffers pour les données
        self.buffer_instantane = []
        self.buffer_instantane_timestamps = []
        self.max_instantane_samples = config.INSTANT_MAX_SAMPLES  # 600 points (1 minute à 10Hz)
        
        # Données enregistrées avec timestamps
        self.recorded_data = []
        self.recorded_timestamps = []
        
        # Compteur de points pour le calcul précis du temps
        self.total_samples_acquired = 0  # Compteur total de points acquis depuis le début de l'enregistrement
        self.sample_rate = config.SAMPLE_RATE  # Fréquence d'échantillonnage (Hz)
        
        # Période d'enregistrement (peut être changée dynamiquement)
        self.record_period = 1  # Par défaut 1 seconde
        
        # Fichier TXT pour enregistrement temps réel
        self.txt_file = None
        self.txt_writer = None
        self.current_filepath = None
        self.recording_start_time = None  # Temps de début d'enregistrement
        self.last_save_time = None  # Dernier temps de sauvegarde
        
        # Informations sur les canaux
        self.channel_names = []
        self.n_channels = len(config.CHANNELS)
        
    def initialize_task(self):
        """
        Initialise la tâche DAQmx avec les canaux configurés
        """
        try:
            # Créer une nouvelle tâche
            self.task = nidaqmx.Task()
            
            # Ajouter les canaux analogiques
            self.channel_names = []
            for channel in self.config.CHANNELS:
                ai_channel = self.task.ai_channels.add_ai_voltage_chan(
                    channel,
                    terminal_config=TerminalConfiguration.RSE,
                    min_val=self.config.MIN_VOLTAGE,
                    max_val=self.config.MAX_VOLTAGE
                )
                # Récupérer le nom du canal
                self.channel_names.append(ai_channel.name)
            
            self.n_channels = len(self.channel_names)
            print(f"✓ {self.n_channels} canal(aux) configuré(s): {', '.join(self.channel_names)}")
            
            # Configurer le timing
            self.task.timing.cfg_samp_clk_timing(
                rate=self.config.SAMPLE_RATE,
                sample_mode=AcquisitionType.CONTINUOUS,
                samps_per_chan=self.config.SAMPLES_PER_CHANNEL
            )
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation DAQ: {e}")
            return False
    
    def initialize_task_from_nimax(self, task_name):
        """
        Charge une tâche existante depuis NI MAX et configure le timing à 10Hz
        
        Args:
            task_name: Nom de la tâche NI MAX
        
        Returns:
            True si succès, False sinon
        """
        try:
            # Charger la tâche sauvegardée depuis NI MAX
            import nidaqmx.system.storage as storage
            
            # Charger la tâche persistée
            persisted_task = storage.PersistedTask(task_name)
            
            # Charger la tâche dans une instance de Task
            self.task = persisted_task.load()
            
            print(f"✓ Tâche '{task_name}' chargée depuis NI MAX")
            
            # Récupérer les noms des canaux (noms personnalisés)
            self.channel_names = []
            for channel in self.task.ai_channels:
                # Utiliser le nom personnalisé du canal (ex: "Tension 1")
                self.channel_names.append(channel.name)
            
            self.n_channels = len(self.channel_names)
            
            # Vérifier qu'il y a au moins un canal AVANT d'afficher
            if self.n_channels == 0:
                print(f"✗ La tâche '{task_name}' ne contient aucun canal d'entrée analogique (AI)")
                raise Exception(f"La tâche '{task_name}' ne contient aucun canal d'entrée analogique (AI).\n"
                              f"Veuillez utiliser une tâche avec des canaux AI configurés dans NI MAX.")
            
            print(f"✓ {self.n_channels} canal(aux): {', '.join(self.channel_names)}")
            
            # Reconfigurer le timing pour 10Hz continu
            self.task.timing.samp_quant_samp_mode = AcquisitionType.CONTINUOUS
            self.task.timing.samp_clk_rate = 10.0
            self.task.timing.samp_quant_samp_per_chan = 1000
            
            print(f"✓ Timing reconfiguré: 10 Hz, échantillonnage continu")
            
            return True
            
        except Exception as e:
            print(f"Erreur lors du chargement de la tâche '{task_name}': {e}")
            if self.task:
                try:
                    self.task.close()
                except:
                    pass
                self.task = None
            return False
    
    def start_acquisition(self, data_callback=None, task_name=None):
        """
        Démarre l'acquisition de données
        
        Args:
            data_callback: Fonction de callback pour recevoir les données
            task_name: Nom de la tâche NI MAX à utiliser (optionnel)
        """
        if self.is_running:
            print("L'acquisition est déjà en cours")
            return False
        
        self.data_callback = data_callback
        
        # Si un nom de tâche est fourni, utiliser la tâche NI MAX
        if task_name:
            if not self.initialize_task_from_nimax(task_name):
                return False
        else:
            # Sinon utiliser la configuration manuelle
            if not self.initialize_task():
                return False
        
        self.is_running = True
        self.acquisition_thread = threading.Thread(target=self._acquisition_loop, daemon=True)
        self.acquisition_thread.start()
        
        return True
    
    def stop_acquisition(self):
        """
        Arrête l'acquisition de données
        """
        self.is_running = False
        
        if self.acquisition_thread:
            self.acquisition_thread.join(timeout=2.0)
        
        if self.task:
            try:
                self.task.stop()
                self.task.close()
            except Exception as e:
                print(f"Erreur lors de l'arrêt de la tâche: {e}")
            finally:
                self.task = None
    
    def start_recording(self, file_prefix="data", comment="", record_period=1, save_folder="data"):
        """
        Démarre l'enregistrement des données en temps réel
        
        Args:
            file_prefix: Préfixe du nom de fichier
            comment: Commentaire à ajouter en en-tête du fichier
            record_period: Période d'enregistrement en secondes
            save_folder: Répertoire où sauvegarder les fichiers
        """
        self.is_recording = True
        self.recorded_data = []
        self.recorded_timestamps = []
        self.total_samples_acquired = 0  # Réinitialiser le compteur de points
        self.recording_start_time = time.time()  # Temps de départ (pour référence)
        self.last_save_sample_count = 0  # Dernier nombre de points lors de la sauvegarde
        self.record_period = record_period  # Stocker la période d'enregistrement
        
        # Créer le fichier TXT avec le préfixe
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{file_prefix}_{timestamp}.txt'
        self.current_filepath = os.path.join(save_folder, filename)
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(save_folder, exist_ok=True)
        
        # Ouvrir le fichier TXT
        self.txt_file = open(self.current_filepath, 'w', newline='', encoding='utf-8')
        self.txt_writer = csv.writer(self.txt_file, delimiter='\t')
        
        # Écrire le commentaire en première ligne (si fourni)
        if comment:
            self.txt_writer.writerow([f'# {comment}'])
        
        # Écrire les en-têtes de colonnes: Temps + noms des canaux
        headers = ['Temps'] + self.channel_names
        self.txt_writer.writerow(headers)
        
        # Forcer l'écriture sur disque
        self.txt_file.flush()
        
        print(f"Enregistrement démarré dans: {self.current_filepath}")
        print(f"Période d'enregistrement: {record_period} seconde(s)")
        if comment:
            print(f"Commentaire: {comment}")
    
    def stop_recording(self):
        """
        Arrête l'enregistrement des données
        """
        self.is_recording = False
        
        # Fermer le fichier TXT
        if self.txt_file:
            self.txt_file.close()
            self.txt_file = None
            self.txt_writer = None
        
        self.recording_start_time = None
        self.last_save_time = None
        
        print(f"Enregistrement arrêté - {len(self.recorded_timestamps)} échantillons")
        
        # Retourner les données enregistrées
        return {
            'timestamps': self.recorded_timestamps.copy(),
            'data': self.recorded_data.copy(),
            'filepath': self.current_filepath
        }
    
    def _acquisition_loop(self):
        """
        Boucle d'acquisition continue (exécutée dans un thread séparé)
        """
        try:
            self.task.start()
            
            while self.is_running:
                try:
                    # Lire les données
                    data = self.task.read(
                        number_of_samples_per_channel=self.config.SAMPLES_PER_READ,
                        timeout=self.config.TIMEOUT
                    )
                    
                    # Convertir en numpy array si nécessaire
                    if not isinstance(data, np.ndarray):
                        data = np.array(data)
                    
                    # Assurer que data est 2D (nombre de canaux x nombre d'échantillons)
                    if len(data.shape) == 1:
                        data = data.reshape(1, -1)
                    
                    # Nombre de nouveaux échantillons acquis
                    num_new_samples = data.shape[1]
                    
                    # Calculer les timestamps précis basés sur le compteur de points
                    # timestamp = nombre_de_points / fréquence_échantillonnage
                    timestamps_for_batch = []
                    for i in range(num_new_samples):
                        sample_time = (self.total_samples_acquired + i) / self.sample_rate
                        timestamps_for_batch.append(sample_time)
                    
                    # Incrémenter le compteur total de points
                    self.total_samples_acquired += num_new_samples
                    
                    # Pour compatibilité avec l'affichage, utiliser le dernier timestamp du batch
                    timestamp = timestamps_for_batch[-1]
                    
                    # Mettre à jour le buffer instantané (fenêtre glissante de 10 secondes)
                    if len(self.buffer_instantane) == 0:
                        self.buffer_instantane = data.copy()
                        self.buffer_instantane_timestamps = timestamps_for_batch
                    else:
                        self.buffer_instantane = np.concatenate(
                            (self.buffer_instantane, data), axis=1
                        )
                        self.buffer_instantane_timestamps.extend(timestamps_for_batch)
                        
                        # Limiter à max_instantane_samples
                        if self.buffer_instantane.shape[1] > self.max_instantane_samples:
                            overflow = self.buffer_instantane.shape[1] - self.max_instantane_samples
                            self.buffer_instantane = self.buffer_instantane[:, overflow:]
                            self.buffer_instantane_timestamps = self.buffer_instantane_timestamps[overflow:]
                    
                    # Si enregistrement actif, vérifier si on doit sauvegarder
                    if self.is_recording and self.txt_writer:
                        # Calculer le nombre de points attendus depuis le dernier enregistrement
                        expected_samples = int(self.record_period * self.sample_rate)
                        samples_since_last_save = self.total_samples_acquired - self.last_save_sample_count
                        
                        if samples_since_last_save >= expected_samples:
                            # Calculer le temps précis basé sur le nombre de points
                            precise_time = self.total_samples_acquired / self.sample_rate
                            
                            # Enregistrer un seul point (le premier de ce batch)
                            row = [precise_time] + data[:, 0].tolist()
                            self.txt_writer.writerow(row)
                            
                            # Flush pour écrire immédiatement
                            self.txt_file.flush()
                            
                            # Ajouter aux buffers de données enregistrées (pour le graphe)
                            if len(self.recorded_data) == 0:
                                self.recorded_data = data[:, 0:1].copy()  # Premier point seulement
                            else:
                                self.recorded_data = np.concatenate(
                                    (self.recorded_data, data[:, 0:1]), axis=1
                                )
                            self.recorded_timestamps.append(precise_time)
                            
                            # Mettre à jour le dernier nombre de points lors de la sauvegarde
                            self.last_save_sample_count = self.total_samples_acquired
                    
                    # Appeler le callback si défini
                    if self.data_callback:
                        self.data_callback(data)
                    
                    # Petite pause pour éviter la surcharge CPU
                    time.sleep(0.01)
                    
                except nidaqmx.errors.DaqError as e:
                    print(f"Erreur DAQ: {e}")
                    break
                    
        except Exception as e:
            print(f"Erreur dans la boucle d'acquisition: {e}")
        finally:
            self.is_running = False
    
    def get_instantane_data(self):
        """
        Retourne les données instantanées (fenêtre glissante de 10 secondes)
        """
        return self.buffer_instantane
    
    def get_instantane_timestamps(self):
        """
        Retourne les timestamps des données instantanées
        """
        return self.buffer_instantane_timestamps
    
    def get_longue_duree_data(self):
        """
        Retourne les données enregistrées avec timestamps
        """
        return {
            'timestamps': self.recorded_timestamps,
            'data': self.recorded_data
        }
    
    def get_channel_names(self):
        """
        Retourne la liste des noms de canaux
        """
        return self.channel_names
    
    def get_channel_count(self):
        """
        Retourne le nombre de canaux
        """
        return self.n_channels
    
    def set_record_period(self, period):
        """
        Met à jour la période d'enregistrement (peut être appelé pendant l'acquisition)
        
        Args:
            period: Nouvelle période d'enregistrement en secondes
        """
        self.record_period = period
        print(f"Période d'enregistrement mise à jour: {period} seconde(s)")
    
    def list_available_devices(self):
        """
        Liste les périphériques DAQ disponibles
        """
        try:
            system = nidaqmx.system.System.local()
            devices = system.devices
            return [device.name for device in devices]
        except Exception as e:
            print(f"Erreur lors de la recherche des périphériques: {e}")
            return []
