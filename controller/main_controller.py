"""
Contrôleur principal - Orchestre la communication entre Model et View
"""
import tkinter as tk
import time
import numpy as np
from utils.settings_manager import SettingsManager
from utils.daq_utils import list_available_tasks, get_task_channels


class MainController:
    """
    Classe contrôleur pour orchestrer le modèle et la vue
    """
    
    def __init__(self, daq_model, data_model, view):
        """
        Initialise le contrôleur
        
        Args:
            daq_model: Instance du modèle DAQ
            data_model: Instance du modèle de données
            view: Instance de la vue
        """
        self.daq_model = daq_model
        self.data_model = data_model
        self.view = view
        
        # Gestionnaire de paramètres
        self.settings_manager = SettingsManager()
        
        # Connecter les callbacks de la vue
        self.view.on_start_recording = self.start_recording
        self.view.on_stop_recording = self.stop_recording
        self.view.on_task_changed = self.on_task_changed
        self.view.on_period_changed = self.on_period_changed
        self.view.on_quit = self.quit_application
        
        # État de l'application
        self.acquisition_active = False
        self.recording_active = False
        self.selected_task_name = None
        
        # Gestion de l'enregistrement périodique
        self.record_period = 60  # secondes
        self.last_record_time = None
        
        # Timer pour la mise à jour de l'interface
        self.update_timer = None
        
    def initialize(self):
        """
        Initialise l'application
        """
        # Charger les paramètres sauvegardés
        settings = self.settings_manager.load_settings()
        
        # Lister les tâches DAQmx disponibles
        available_tasks = list_available_tasks()
        
        # Mettre à jour la combobox des tâches
        if available_tasks:
            self.view.task_combo['values'] = available_tasks
            
            # Sélectionner la dernière tâche utilisée si disponible
            if settings['task_name'] and settings['task_name'] in available_tasks:
                self.view.selected_task.set(settings['task_name'])
                self.selected_task_name = settings['task_name']
            elif available_tasks:
                # Sinon, sélectionner la première tâche
                self.view.selected_task.set(available_tasks[0])
                self.selected_task_name = available_tasks[0]
        else:
            print("Aucune tâche DAQmx configurée")
        
        # Restaurer les autres paramètres
        self.view.record_period.set(settings['record_period'])
        self.record_period = settings['record_period']
        
        self.view.file_prefix.set(settings.get('file_prefix', 'data'))
        self.view.file_comment.set(settings.get('file_comment', ''))
        self.view.save_directory.set(settings.get('last_save_folder', 'data'))
        
        # Lister les périphériques disponibles
        devices = self.daq_model.list_available_devices()
        if devices:
            print(f"Périphériques DAQ détectés: {', '.join(devices)}")
        else:
            print("Aucun périphérique DAQ détecté (mode simulation)")
        
        # NE PAS démarrer l'acquisition automatiquement - attendre le clic sur Démarrer
        print("ℹ Application en attente - Cliquez sur 'Démarrer' pour lancer l'acquisition")
        
        # Démarrer la mise à jour périodique de l'interface quand même
        self._schedule_update()
    
    def start_recording(self):
        """
        Démarre l'acquisition ET l'enregistrement des données
        """
        # Si l'acquisition n'est pas active, la démarrer avec la tâche sélectionnée
        if not self.acquisition_active:
            task_name = self.view.selected_task.get()
            
            if not task_name:
                tk.messagebox.showerror("Erreur", "Veuillez sélectionner une tâche DAQmx")
                return
            
            print(f"Démarrage de l'acquisition avec la tâche: {task_name}")
            
            # Démarrer l'acquisition avec la tâche NI MAX
            success = self.daq_model.start_acquisition(
                data_callback=self._on_data_received,
                task_name=task_name
            )
            
            if success:
                self.acquisition_active = True
                
                # Désactiver les contrôles de configuration pendant l'acquisition
                self.view.set_config_controls_state(enabled=False)
                
                # Configurer les graphiques avec les canaux détectés
                channel_names = self.daq_model.get_channel_names()
                if channel_names:
                    self.view.setup_plot_channels(channel_names)
                
                print("Acquisition démarrée à 10 Hz")
            else:
                tk.messagebox.showerror(
                    "Erreur",
                    f"Impossible de démarrer la tâche '{task_name}'.\n"
                    "Vérifiez que la tâche existe dans NI MAX et que\n"
                    "la carte DAQ est connectée."
                )
                return
        
        # Démarrer l'enregistrement avec préfixe, commentaire et période
        file_prefix = self.view.file_prefix.get() or "data"
        comment = self.view.file_comment.get() or ""
        record_period = int(self.view.record_period.get())
        save_folder = self.view.save_directory.get() or "data"
        self.daq_model.start_recording(file_prefix=file_prefix, comment=comment, record_period=record_period, save_folder=save_folder)
        self.recording_active = True
        self.last_record_time = time.time()
        print("Enregistrement démarré")
    
    def stop_recording(self):
        """
        Arrête l'enregistrement ET l'acquisition
        """
        if not self.recording_active:
            return
        
        # Arrêter l'enregistrement
        result = self.daq_model.stop_recording()
        self.recording_active = False
        self.last_record_time = None
        
        # Arrêter l'acquisition
        if self.acquisition_active:
            self.daq_model.stop_acquisition()
            self.acquisition_active = False
            
            # Réactiver les contrôles de configuration
            self.view.set_config_controls_state(enabled=True)
            
            print("Acquisition arrêtée")
        
        # Afficher les informations
        if result and result['filepath']:
            tk.messagebox.showinfo(
                "Enregistrement terminé",
                f"Données sauvegardées dans:\n{result['filepath']}\n\n"
                f"{len(result['timestamps'])} échantillons enregistrés"
            )
        else:
            tk.messagebox.showwarning(
                "Attention",
                "Aucune donnée à sauvegarder"
            )
        
        print("Enregistrement arrêté")
    
    def on_task_changed(self, task_name):
        """
        Callback appelé quand la tâche DAQmx est changée
        
        Args:
            task_name: Nom de la nouvelle tâche sélectionnée
        """
        self.selected_task_name = task_name
        print(f"Tâche sélectionnée: {task_name}")
        
        # Sauvegarder la configuration
        self.settings_manager.set('task_name', task_name)
        self.settings_manager.save_settings()
        
        # TODO: Redémarrer l'acquisition avec la nouvelle tâche si nécessaire
    
    def on_period_changed(self, period):
        """
        Callback appelé quand la période d'enregistrement change
        
        Args:
            period: Nouvelle période en secondes
        """
        self.record_period = period
        
        # Si un enregistrement est en cours, mettre à jour la période dynamiquement
        if self.recording_active:
            self.daq_model.set_record_period(period)
        
        print(f"Période d'enregistrement: {period} seconde(s)")
    
    def toggle_waiting(self):
        """
        Méthode obsolète - conservée pour compatibilité
        """
        pass
    
    def quit_application(self):
        """
        Quitte l'application proprement
        """
        # Sauvegarder tous les paramètres
        self.settings_manager.set('task_name', self.selected_task_name)
        self.settings_manager.set('record_period', int(self.view.record_period.get()))
        self.settings_manager.set('file_prefix', self.view.file_prefix.get())
        self.settings_manager.set('file_comment', self.view.file_comment.get())
        self.settings_manager.set('last_save_folder', self.view.save_directory.get())
        self.settings_manager.save_settings()
        
        # Arrêter l'enregistrement si actif
        if self.recording_active:
            self.stop_recording()
        
        # Arrêter l'acquisition
        if self.acquisition_active:
            self.daq_model.stop_acquisition()
            self.acquisition_active = False
        
        # Annuler le timer
        if self.update_timer:
            self.view.root.after_cancel(self.update_timer)
        
        print("Application terminée")
    
    def _on_data_received(self, data):
        """
        Callback appelé lors de la réception de nouvelles données
        
        Args:
            data: Données reçues du DAQ
        """
        # Cette fonction est appelée depuis le thread d'acquisition
        # Les mises à jour de l'interface seront faites dans _update_interface
        pass
    
    def _update_interface(self):
        """
        Met à jour l'interface avec les dernières données
        """
        try:
            # Récupérer les données instantanées
            instant_data = self.daq_model.get_instantane_data()
            instant_timestamps = self.daq_model.get_instantane_timestamps()
            
            # Mettre à jour le graphique instantané
            if instant_data is not None and len(instant_data) > 0:
                self.view.update_instantane_plot(instant_data, instant_timestamps)
            
            # Mettre à jour le nombre de points disponibles dans le buffer
            if self.acquisition_active:
                buffer_available = self.daq_model.get_buffer_available_samples()
                self.view.buffer_available.set(f"{buffer_available} points")
            else:
                self.view.buffer_available.set("0 points")
            
            # Si enregistrement actif
            if self.recording_active:
                # Vérifier si on doit faire un enregistrement périodique (non nécessaire car temps réel)
                # self._check_periodic_save()
                
                # Mettre à jour le graphique longue durée
                long_data_dict = self.daq_model.get_longue_duree_data()
                if long_data_dict and long_data_dict['data'] is not None:
                    if isinstance(long_data_dict['data'], np.ndarray) and long_data_dict['data'].size > 0:
                        self.view.update_longue_duree_plot(
                            long_data_dict['timestamps'],
                            long_data_dict['data']
                        )
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'interface: {e}")
        
        # Planifier la prochaine mise à jour
        self._schedule_update()
    
    def _check_periodic_save(self):
        """
        Vérifie si un enregistrement périodique doit être effectué
        """
        # Si période = 0, pas d'enregistrement automatique
        period = int(self.view.record_period.get())
        if period == 0:
            return
        
        # Vérifier le temps écoulé
        if self.last_record_time is not None:
            elapsed = time.time() - self.last_record_time
            
            if elapsed >= period:
                # Sauvegarder automatiquement
                data = self.daq_model.get_longue_duree_data()
                if data is not None and len(data) > 0:
                    filepath = self.data_model.save_to_csv(data)
                    if filepath:
                        print(f"Enregistrement périodique: {filepath}")
                
                # Réinitialiser le timer
                self.last_record_time = time.time()
    
    def _schedule_update(self):
        """
        Planifie la prochaine mise à jour de l'interface
        """
        # Mise à jour toutes les 100 ms
        self.update_timer = self.view.root.after(100, self._update_interface)
    
    def run(self):
        """
        Lance l'application
        """
        self.initialize()
        self.view.run()
