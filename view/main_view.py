"""
Vue principale - Interface graphique Tkinter pour le Logger NI
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class MainView:
    """
    Classe pour l'interface graphique principale
    """
    
    def __init__(self, root, config):
        """
        Initialise la vue principale
        
        Args:
            root: Fenêtre Tkinter racine
            config: Objet de configuration
        """
        self.root = root
        self.config = config
        
        # Configurer la fenêtre principale
        self.root.title("🧪 Logger")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e1e2e')
        
        # Style moderne
        self.colors = {
            'bg_dark': '#1e1e2e',
            'bg_medium': '#2b2b3c',
            'bg_light': '#363654',
            'accent_blue': '#89b4fa',
            'accent_green': '#a6e3a1',
            'accent_red': '#f38ba8',
            'accent_yellow': '#f9e2af',
            'accent_purple': '#cba6f7',
            'text_white': '#cdd6f4',
            'text_gray': '#a6adc8',
        }
        
        # Variables de contrôle
        self.selected_task = tk.StringVar(value="")
        self.record_period = tk.IntVar(value=60)
        self.file_prefix = tk.StringVar(value="data")
        self.save_directory = tk.StringVar(value="data")
        self.file_comment = tk.StringVar(value="")
        self.available_tasks = []  # Liste des tâches DAQmx disponibles
        
        # Variables pour l'échelle des graphiques
        self.auto_scale = tk.BooleanVar(value=True)
        self.y_min = tk.DoubleVar(value=-10.0)
        self.y_max = tk.DoubleVar(value=10.0)
        
        # Créer l'interface
        self._create_widgets()
        
        # Configurer le gestionnaire de fermeture de fenêtre (croix en haut à droite)
        self.root.protocol("WM_DELETE_WINDOW", self._on_quit_clicked)
        
        # Ajouter une trace sur record_period pour détecter les changements (clavier ET boutons)
        self.record_period.trace_add('write', lambda *args: self._on_period_changed())
        
        # Callbacks (à définir par le contrôleur)
        self.on_start_recording = None
        self.on_stop_recording = None
        self.on_quit = None
        self.on_task_changed = None
        self.on_period_changed = None
    
    def _create_widgets(self):
        """
        Crée tous les widgets de l'interface
        """
        # Titre principal avec logo
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            title_frame,
            text="🧪 LOGGER",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue']
        )
        title_label.pack()
        
        # Separator
        separator = tk.Frame(self.root, height=2, bg=self.colors['accent_blue'])
        separator.pack(fill=tk.X, padx=20)
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame principal gauche (boutons de contrôle)
        left_frame = tk.Frame(main_container, bg=self.colors['bg_medium'], width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_frame.pack_propagate(False)
        
        # Titre section contrôles
        control_title = tk.Label(
            left_frame,
            text="⚙️ CONFIGURATION",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_purple'],
            pady=15
        )
        control_title.pack(fill=tk.X)
        
        # Padding intérieur
        config_container = tk.Frame(left_frame, bg=self.colors['bg_medium'])
        config_container.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Cadre configuration
        config_frame = tk.Frame(config_container, bg=self.colors['bg_dark'], relief=tk.FLAT)
        config_frame.pack(fill=tk.X, pady=5)
        
        # Sélection de la tâche DAQmx
        tk.Label(
            config_frame,
            text="📋 Tâche DAQmx",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(10, 2))
        
        self.task_combo = ttk.Combobox(
            config_frame,
            textvariable=self.selected_task,
            values=self.available_tasks,
            state='readonly',
            font=("Segoe UI", 9)
        )
        self.task_combo.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.task_combo.bind('<<ComboboxSelected>>', lambda e: self._on_task_changed())
        
        # Période d'enregistrement
        tk.Label(
            config_frame,
            text="⏱️ Période d'enregistrement (s)",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(5, 2))
        
        period_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        period_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.period_spinbox = tk.Spinbox(
            period_frame,
            from_=0,
            to=3600,
            textvariable=self.record_period,
            font=("Segoe UI", 10),
            width=10,
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            buttonbackground=self.colors['accent_blue'],
            relief=tk.FLAT
        )
        self.period_spinbox.pack(side=tk.LEFT)
        
        tk.Label(
            period_frame,
            text="(0 = pas d'enregistrement)",
            font=("Segoe UI", 8),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_gray']
        ).pack(side=tk.LEFT, padx=10)
        
        # Préfixe nom fichier
        tk.Label(
            config_frame,
            text="📁 Préfixe nom fichier",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(5, 2))
        
        self.prefix_entry = tk.Entry(
            config_frame,
            textvariable=self.file_prefix,
            font=("Segoe UI", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            insertbackground=self.colors['text_white']
        )
        self.prefix_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Répertoire d'enregistrement
        tk.Label(
            config_frame,
            text="📂 Répertoire d'enregistrement",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(5, 2))
        
        dir_frame = tk.Frame(config_frame, bg=self.colors['bg_dark'])
        dir_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.directory_entry = tk.Entry(
            dir_frame,
            textvariable=self.save_directory,
            font=("Segoe UI", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            insertbackground=self.colors['text_white']
        )
        self.directory_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_button = tk.Button(
            dir_frame,
            text="📁",
            font=("Segoe UI", 10),
            bg=self.colors['accent_purple'],
            fg=self.colors['bg_dark'],
            activebackground=self.colors['accent_blue'],
            activeforeground=self.colors['bg_dark'],
            relief=tk.FLAT,
            borderwidth=0,
            command=self._on_browse_directory,
            width=3,
            cursor="hand2"
        )
        self.browse_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Commentaire
        tk.Label(
            config_frame,
            text="💬 Commentaire",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=10, pady=(5, 2))
        
        self.comment_entry = tk.Entry(
            config_frame,
            textvariable=self.file_comment,
            font=("Segoe UI", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            relief=tk.FLAT,
            insertbackground=self.colors['text_white']
        )
        self.comment_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Separator
        tk.Frame(left_frame, height=2, bg=self.colors['accent_purple']).pack(fill=tk.X, padx=15, pady=10)
        
        # Titre section contrôles
        tk.Label(
            left_frame,
            text="🎮 CONTRÔLES",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent_green'],
            pady=10
        ).pack(fill=tk.X)
        
        # Padding intérieur
        button_container = tk.Frame(left_frame, bg=self.colors['bg_medium'])
        button_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Bouton Démarrer
        self.btn_start = tk.Button(
            button_container,
            text="▶  Démarrer",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent_green'],
            fg=self.colors['bg_dark'],
            activebackground='#94d88d',
            activeforeground=self.colors['bg_dark'],
            relief=tk.FLAT,
            borderwidth=0,
            command=self._on_start_clicked,
            height=2,
            cursor="hand2"
        )
        self.btn_start.pack(fill=tk.X, pady=8)
        self.btn_start.bind('<Enter>', lambda e: self.btn_start.config(bg='#94d88d'))
        self.btn_start.bind('<Leave>', lambda e: self.btn_start.config(bg=self.colors['accent_green']))
        
        # Bouton Arrêter enregistrement
        self.btn_stop = tk.Button(
            button_container,
            text="◼  Arrêter enregistrement",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent_red'],
            fg=self.colors['bg_dark'],
            activebackground='#eb6f87',
            activeforeground=self.colors['bg_dark'],
            relief=tk.FLAT,
            borderwidth=0,
            command=self._on_stop_clicked,
            height=2,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.btn_stop.pack(fill=tk.X, pady=8)
        self.btn_stop.bind('<Enter>', lambda e: self.btn_stop.config(bg='#eb6f87') if self.btn_stop['state'] == 'normal' else None)
        self.btn_stop.bind('<Leave>', lambda e: self.btn_stop.config(bg=self.colors['accent_red']) if self.btn_stop['state'] == 'normal' else None)
        
        # Spacer
        tk.Frame(button_container, bg=self.colors['bg_medium'], height=20).pack()
        
        # Bouton Quitter
        self.btn_quit = tk.Button(
            button_container,
            text="✕  Quitter [ECHAP]",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            activebackground='#4a4a68',
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            borderwidth=0,
            command=self._on_quit_clicked,
            height=2,
            cursor="hand2"
        )
        self.btn_quit.pack(fill=tk.X, pady=8)
        self.btn_quit.bind('<Enter>', lambda e: self.btn_quit.config(bg='#4a4a68'))
        self.btn_quit.bind('<Leave>', lambda e: self.btn_quit.config(bg=self.colors['bg_light']))
        
        # Bouton A propos
        self.btn_about = tk.Button(
            button_container,
            text="ℹ  À propos",
            font=("Segoe UI", 10),
            bg=self.colors['bg_light'],
            fg=self.colors['text_gray'],
            activebackground='#4a4a68',
            activeforeground=self.colors['text_white'],
            relief=tk.FLAT,
            borderwidth=0,
            command=self._show_about,
            height=2,
            cursor="hand2"
        )
        self.btn_about.pack(fill=tk.X, pady=8)
        self.btn_about.bind('<Enter>', lambda e: self.btn_about.config(bg='#4a4a68', fg=self.colors['text_white']))
        self.btn_about.bind('<Leave>', lambda e: self.btn_about.config(bg=self.colors['bg_light'], fg=self.colors['text_gray']))
        
        # Info système en bas
        info_frame = tk.Frame(button_container, bg=self.colors['bg_dark'], relief=tk.FLAT)
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        tk.Label(
            info_frame,
            text="🔌 Périphérique",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            pady=5
        ).pack()
        
        tk.Label(
            info_frame,
            text=self.config.DEVICE_NAME,
            font=("Segoe UI", 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white']
        ).pack()
        
        tk.Label(
            info_frame,
            text=f"📡 {self.config.SAMPLE_RATE} Hz",
            font=("Segoe UI", 9),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_gray'],
            pady=2
        ).pack()
        
        # Frame principal droit (graphiques)
        right_frame = tk.Frame(main_container, bg=self.colors['bg_medium'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Barre de statut et contrôles en bas (créer AVANT le notebook)
        bottom_bar = tk.Frame(right_frame, bg=self.colors['bg_light'], height=70)
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        bottom_bar.pack_propagate(False)
        
        # Conteneur pour le notebook
        notebook_frame = tk.Frame(right_frame, bg=self.colors['bg_medium'])
        notebook_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style pour le Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TNotebook', 
                       background=self.colors['bg_medium'],
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['bg_light'],
                       foreground=self.colors['text_gray'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', self.colors['bg_dark'])],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(notebook_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet 1: Graph instantané
        tab1 = tk.Frame(self.notebook, bg=self.colors['bg_medium'])
        self.notebook.add(tab1, text="📈 Graphique Instantané")
        
        # Onglet 2: Graph longue durée
        tab2 = tk.Frame(self.notebook, bg=self.colors['bg_medium'])
        self.notebook.add(tab2, text="📊 Graphique Longue Durée")
        
        # Créer les graphiques
        self._create_plots(tab1, tab2)
        
        # Remplir la barre de statut et contrôles
        self._fill_bottom_bar(bottom_bar)
        
        # Raccourci clavier ECHAP
        self.root.bind('<Escape>', lambda e: self._on_quit_clicked())
    
    def _fill_bottom_bar(self, bottom_bar):
        """
        Remplit la barre de statut et contrôles en bas des graphiques
        """
        # Statut à gauche
        status_frame = tk.Frame(bottom_bar, bg=self.colors['bg_light'])
        status_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(
            status_frame,
            text="⚡ Statut",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['accent_purple']
        ).pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            status_frame,
            text="● Arrêté",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_gray']
        )
        self.status_label.pack(anchor=tk.W)
        
        # Contrôles d'échelle à droite
        scale_frame = tk.Frame(bottom_bar, bg=self.colors['bg_light'])
        scale_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Checkbox échelle auto
        self.auto_scale_check = tk.Checkbutton(
            scale_frame,
            text="Échelle auto",
            variable=self.auto_scale,
            font=("Segoe UI", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white'],
            selectcolor=self.colors['bg_dark'],
            activebackground=self.colors['bg_light'],
            activeforeground=self.colors['text_white'],
            command=self._on_auto_scale_changed
        )
        self.auto_scale_check.pack(side=tk.LEFT, padx=10)
        
        # Min
        tk.Label(
            scale_frame,
            text="Min:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white']
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        self.min_spinbox = tk.Spinbox(
            scale_frame,
            from_=-1000,
            to=1000,
            increment=1,
            textvariable=self.y_min,
            font=("Segoe UI", 9),
            width=8,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            buttonbackground=self.colors['accent_blue'],
            relief=tk.FLAT,
            state=tk.DISABLED  # Désactivé par défaut (échelle auto)
        )
        self.min_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Max
        tk.Label(
            scale_frame,
            text="Max:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text_white']
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        self.max_spinbox = tk.Spinbox(
            scale_frame,
            from_=-1000,
            to=1000,
            increment=1,
            textvariable=self.y_max,
            font=("Segoe UI", 9),
            width=8,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            buttonbackground=self.colors['accent_blue'],
            relief=tk.FLAT,
            state=tk.DISABLED  # Désactivé par défaut (échelle auto)
        )
        self.max_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Ajouter des traces pour les changements
        self.y_min.trace_add('write', lambda *args: self._on_scale_changed())
        self.y_max.trace_add('write', lambda *args: self._on_scale_changed())
    
    def _on_auto_scale_changed(self):
        """Callback pour le changement d'échelle auto"""
        if self.auto_scale.get():
            # Désactiver les spinbox
            self.min_spinbox.config(state=tk.DISABLED)
            self.max_spinbox.config(state=tk.DISABLED)
        else:
            # Activer les spinbox
            self.min_spinbox.config(state=tk.NORMAL)
            self.max_spinbox.config(state=tk.NORMAL)
            # Appliquer l'échelle manuelle
            self._on_scale_changed()
    
    def _on_scale_changed(self):
        """Callback pour le changement d'échelle manuelle"""
        if not self.auto_scale.get():
            try:
                y_min = float(self.y_min.get())
                y_max = float(self.y_max.get())
                if y_min < y_max:
                    self.ax_instant.set_ylim(y_min, y_max)
                    self.ax_long.set_ylim(y_min, y_max)
                    self.canvas_instant.draw()
                    self.canvas_long.draw()
            except (ValueError, tk.TclError):
                pass  # Ignorer les valeurs invalides
    
    def _create_plots(self, tab1, tab2):
        """
        Crée les graphiques matplotlib avec style moderne
        """
        # Couleurs pour les différents canaux
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
        
        # Graphique instantané
        self.fig_instant = Figure(figsize=(10, 6), facecolor=self.colors['bg_medium'])
        self.ax_instant = self.fig_instant.add_subplot(111)
        self.ax_instant.set_facecolor('#1a1a2e')
        self.ax_instant.set_xlabel('Temps (s)', fontsize=11, color=self.colors['text_white'], fontweight='bold')
        self.ax_instant.set_xlim(0, 60)  # 1 minute
        self.ax_instant.set_ylim(-10, 10)
        self.ax_instant.grid(True, alpha=0.15, color=self.colors['text_gray'], linestyle='--')
        self.ax_instant.tick_params(colors=self.colors['text_gray'], labelsize=9)
        
        # Lignes initialement vides (seront créées dynamiquement)
        self.lines_instant = []
        
        self.fig_instant.tight_layout()
        self.canvas_instant = FigureCanvasTkAgg(self.fig_instant, tab1)
        self.canvas_instant.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Graphique longue durée
        self.fig_long = Figure(figsize=(10, 6), facecolor=self.colors['bg_medium'])
        self.ax_long = self.fig_long.add_subplot(111)
        self.ax_long.set_facecolor('#1a1a2e')
        self.ax_long.set_xlabel('Temps (s)', fontsize=11, color=self.colors['text_white'], fontweight='bold')
        self.ax_long.set_xlim(0, 100)
        self.ax_long.set_ylim(-10, 10)
        self.ax_long.grid(True, alpha=0.15, color=self.colors['text_gray'], linestyle='--')
        self.ax_long.tick_params(colors=self.colors['text_gray'], labelsize=9)
        
        # Lignes initialement vides (seront créées dynamiquement)
        self.lines_long = []
        
        self.fig_long.tight_layout()
        self.canvas_long = FigureCanvasTkAgg(self.fig_long, tab2)
        self.canvas_long.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def setup_plot_channels(self, channel_names):
        """
        Configure les lignes de graphique selon les noms de canaux
        
        Args:
            channel_names: Liste des noms de canaux
        """
        # Supprimer les anciennes lignes
        for line in self.lines_instant:
            line.remove()
        for line in self.lines_long:
            line.remove()
        
        self.lines_instant = []
        self.lines_long = []
        
        # Créer les nouvelles lignes
        for i, channel_name in enumerate(channel_names):
            color = self.plot_colors[i % len(self.plot_colors)]
            
            # Ligne instantanée
            line_inst, = self.ax_instant.plot([], [], color=color, linewidth=2.5, 
                                              label=channel_name, alpha=0.9)
            self.lines_instant.append(line_inst)
            
            # Ligne longue durée
            line_long, = self.ax_long.plot([], [], color=color, linewidth=2.5, 
                                           label=channel_name, alpha=0.9)
            self.lines_long.append(line_long)
        
        # Mettre à jour les légendes
        legend_inst = self.ax_instant.legend(loc='upper right', facecolor=self.colors['bg_light'], 
                                             edgecolor=self.colors['text_gray'], fontsize=10)
        for text in legend_inst.get_texts():
            text.set_color(self.colors['text_white'])
        
        legend_long = self.ax_long.legend(loc='upper right', facecolor=self.colors['bg_light'], 
                                          edgecolor=self.colors['text_gray'], fontsize=10)
        for text in legend_long.get_texts():
            text.set_color(self.colors['text_white'])
        
        print(f"✓ {len(channel_names)} canal(aux) configuré(s) dans les graphiques: {', '.join(channel_names)}")
    
    def update_instantane_plot(self, data, timestamps=None):
        """
        Met à jour le graphique instantané avec fenêtre glissante d'1 minute
        
        Args:
            data: Données à afficher (numpy array)
            timestamps: Liste des timestamps (optionnel)
        """
        if data is None or (isinstance(data, np.ndarray) and data.size == 0):
            return
        
        if len(self.lines_instant) == 0:
            return  # Pas encore de lignes configurées
        
        try:
            # Assurer que data est 2D
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            # Créer l'axe temporel
            num_samples = data.shape[1]
            if timestamps and len(timestamps) >= num_samples:
                # Utiliser les timestamps réels, convertis en temps relatif
                time_axis = np.array(timestamps[-num_samples:])
                time_axis = time_axis - time_axis[0]  # Temps relatif à partir du premier point
            else:
                # Fallback : axe temporel calculé
                time_axis = np.linspace(0, num_samples / self.config.SAMPLE_RATE, num_samples)
            
            # Mettre à jour chaque canal
            for i in range(min(data.shape[0], len(self.lines_instant))):
                self.lines_instant[i].set_data(time_axis, data[i, :])
            
            # Ajuster les limites (fenêtre de 60 secondes)
            if len(time_axis) > 0:
                self.ax_instant.set_xlim(0, max(60, time_axis[-1]))
            
            # Calculer les limites y selon le mode (auto ou manuel)
            if self.auto_scale.get():
                all_data = data.flatten()
                if len(all_data) > 0:
                    y_min = np.min(all_data)
                    y_max = np.max(all_data)
                    margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
                    self.ax_instant.set_ylim(y_min - margin, y_max + margin)
            else:
                # Utiliser les limites manuelles
                self.ax_instant.set_ylim(self.y_min.get(), self.y_max.get())
            
            self.canvas_instant.draw()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique instantané: {e}")
    
    def update_longue_duree_plot(self, timestamps, data):
        """
        Met à jour le graphique longue durée avec timestamps réels (graphique XY)
        
        Args:
            timestamps: Liste des timestamps
            data: Données à afficher (numpy array)
        """
        if data is None or (isinstance(data, np.ndarray) and data.size == 0):
            return
        
        if not timestamps or len(timestamps) == 0:
            return
        
        if len(self.lines_long) == 0:
            return  # Pas encore de lignes configurées
        
        try:
            # Assurer que data est 2D
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            # Convertir timestamps en temps relatif (en secondes depuis le début)
            time_array = np.array(timestamps)
            time_axis = time_array - time_array[0]
            
            # Mettre à jour chaque canal
            for i in range(min(data.shape[0], len(self.lines_long))):
                self.lines_long[i].set_data(time_axis, data[i, :])
            
            # Ajuster les limites
            if len(time_axis) > 0:
                self.ax_long.set_xlim(0, time_axis[-1])
            
            # Calculer les limites y selon le mode (auto ou manuel)
            if self.auto_scale.get():
                all_data = data.flatten()
                if len(all_data) > 0:
                    y_min = np.min(all_data)
                    y_max = np.max(all_data)
                    margin = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
                    self.ax_long.set_ylim(y_min - margin, y_max + margin)
            else:
                # Utiliser les limites manuelles
                self.ax_long.set_ylim(self.y_min.get(), self.y_max.get())
            
            self.canvas_long.draw()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique longue durée: {e}")
    
    def _on_start_clicked(self):
        """Callback pour le bouton Démarrer"""
        if self.on_start_recording:
            self.on_start_recording()
        self.btn_start.config(state=tk.DISABLED, bg=self.colors['bg_light'])
        self.btn_stop.config(state=tk.NORMAL, bg=self.colors['accent_red'])
        self.status_label.config(text="● Enregistrement", fg=self.colors['accent_red'])
    
    def _on_stop_clicked(self):
        """Callback pour le bouton Arrêter"""
        if self.on_stop_recording:
            self.on_stop_recording()
        self.btn_start.config(state=tk.NORMAL, bg=self.colors['accent_green'])
        self.btn_stop.config(state=tk.DISABLED, bg=self.colors['bg_light'])
        self.status_label.config(text="● Arrêté", fg=self.colors['text_gray'])
    
    def _on_task_changed(self):
        """Callback pour le changement de tâche DAQmx"""
        if self.on_task_changed:
            self.on_task_changed(self.selected_task.get())
    
    def _on_browse_directory(self):
        """Callback pour le bouton Browse - Sélection du répertoire d'enregistrement"""
        import os
        # Utiliser le répertoire actuel comme point de départ
        initial_dir = self.save_directory.get()
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()
        
        # Ouvrir le dialogue de sélection de répertoire
        directory = filedialog.askdirectory(
            title="Sélectionner le répertoire d'enregistrement",
            initialdir=initial_dir
        )
        
        # Si un répertoire a été sélectionné, mettre à jour la variable
        if directory:
            self.save_directory.set(directory)
    
    def _on_period_changed(self):
        """Callback pour le changement de période d'enregistrement"""
        if self.on_period_changed:
            try:
                period = int(self.record_period.get())
                self.on_period_changed(period)
            except ValueError:
                pass  # Ignorer les valeurs invalides
    
    def _on_quit_clicked(self):
        """Callback pour le bouton Quitter"""
        # Créer une fenêtre de dialogue personnalisée
        dialog = tk.Toplevel(self.root)
        dialog.title("Confirmation")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f'400x200+{x}+{y}')
        
        tk.Label(
            dialog,
            text="⚠️ Confirmation de fermeture",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_yellow'],
            pady=20
        ).pack()
        
        tk.Label(
            dialog,
            text="Voulez-vous vraiment quitter l'application ?",
            font=("Segoe UI", 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            pady=10
        ).pack()
        
        button_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        button_frame.pack(pady=20)
        
        def on_yes():
            if self.on_quit:
                self.on_quit()
            self.root.quit()
            dialog.destroy()
        
        def on_no():
            dialog.destroy()
        
        tk.Button(
            button_frame,
            text="✓ Oui, quitter",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['accent_red'],
            fg=self.colors['text_white'],
            command=on_yes,
            width=15,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="✕ Non, rester",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['accent_green'],
            fg=self.colors['bg_dark'],
            command=on_no,
            width=15,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=10)
    
    def _show_about(self):
        """Affiche la boîte de dialogue A propos"""
        # Créer une fenêtre personnalisée
        about = tk.Toplevel(self.root)
        about.title("À propos")
        about.geometry("500x400")
        about.configure(bg=self.colors['bg_dark'])
        about.transient(self.root)
        about.grab_set()
        
        # Centrer
        about.update_idletasks()
        x = (about.winfo_screenwidth() // 2) - (500 // 2)
        y = (about.winfo_screenheight() // 2) - (400 // 2)
        about.geometry(f'500x400+{x}+{y}')
        
        tk.Label(
            about,
            text="📊 LOGGER NI",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['accent_blue'],
            pady=20
        ).pack()
        
        tk.Label(
            about,
            text="Acquisition de Données National Instruments",
            font=("Segoe UI", 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_gray'],
            pady=5
        ).pack()
        
        tk.Label(
            about,
            text="Version 1.0 • Décembre 2025",
            font=("Segoe UI", 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_gray'],
            pady=5
        ).pack()
        
        separator = tk.Frame(about, height=2, bg=self.colors['accent_blue'])
        separator.pack(fill=tk.X, padx=50, pady=20)
        
        info_frame = tk.Frame(about, bg=self.colors['bg_medium'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        infos = [
            ("🏗️ Architecture", "MVC (Model-View-Controller)"),
            ("🐍 Langage", "Python 3.10"),
            ("🖼️ Interface", "Tkinter + Matplotlib"),
            ("⚙️ API", "National Instruments DAQmx"),
            ("📡 Périphérique", self.config.DEVICE_NAME),
            ("🔊 Fréquence", f"{self.config.SAMPLE_RATE} Hz")
        ]
        
        for label, value in infos:
            row = tk.Frame(info_frame, bg=self.colors['bg_medium'])
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg_medium'],
                fg=self.colors['accent_purple'],
                width=20,
                anchor=tk.W
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Label(
                row,
                text=value,
                font=("Segoe UI", 10),
                bg=self.colors['bg_medium'],
                fg=self.colors['text_white'],
                anchor=tk.W
            ).pack(side=tk.LEFT)
        
        tk.Button(
            about,
            text="✓ Fermer",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['accent_blue'],
            fg=self.colors['bg_dark'],
            command=about.destroy,
            width=15,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(pady=20)
    
    def run(self):
        """Lance la boucle principale de l'interface"""
        self.root.mainloop()
