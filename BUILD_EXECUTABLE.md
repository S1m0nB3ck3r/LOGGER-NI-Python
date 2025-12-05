# Guide de création d'exécutable pour Logger NI

## 📦 Créer un exécutable Windows (.exe)

Ce guide explique comment créer un fichier exécutable autonome de Logger NI qui peut être distribué et exécuté sur n'importe quel PC Windows **sans avoir besoin d'installer Python**.

---

## 🚀 Méthode rapide

### Option 1 : Script Batch (Windows)
```batch
build_exe.bat
```

### Option 2 : Script PowerShell
```powershell
.\build_exe.ps1
```

Ces scripts :
1. Installent PyInstaller si nécessaire
2. Nettoient les anciens builds
3. Créent l'exécutable dans le dossier `dist/`

---

## 📋 Méthode manuelle

### 1. Installer PyInstaller

```bash
pip install pyinstaller
```

### 2. Créer l'exécutable

```bash
pyinstaller logger_ni.spec --clean
```

### 3. Localiser l'exécutable

L'exécutable se trouve dans : `dist\LoggerNI.exe`

---

## ⚙️ Configuration avancée

### Modifier le fichier `logger_ni.spec`

Vous pouvez personnaliser :

#### 🎨 Ajouter une icône
```python
exe = EXE(
    ...
    icon='path/to/icon.ico',  # Remplacer None par le chemin de votre icône
)
```

#### 🖥️ Cacher la console
```python
exe = EXE(
    ...
    console=False,  # Mettre False pour une application GUI pure
)
```

#### 📁 Inclure des fichiers supplémentaires
```python
a = Analysis(
    ...
    datas=[
        ('logger_config.json', '.'),
        ('data/', 'data/'),  # Inclure le dossier data
        ('docs/', 'docs/'),  # Inclure la documentation
    ],
)
```

---

## 📦 Distribution

### Fichier unique
L'exécutable créé est **autonome** et contient :
- ✅ Python et toutes les bibliothèques
- ✅ Le code de votre application
- ✅ Les fichiers de configuration
- ✅ Toutes les dépendances

### Taille
L'exécutable sera d'environ **50-100 MB** car il inclut :
- Python embedded
- numpy, matplotlib, tkinter
- NIDAQmx drivers (si inclus)

### ⚠️ Important - Drivers NI
L'exécutable **NE CONTIENT PAS** les drivers National Instruments DAQmx.
Les utilisateurs doivent avoir installé :
- **NI-DAQmx Runtime** (disponible gratuitement sur ni.com)

---

## 🧪 Test de l'exécutable

1. Copiez `dist\LoggerNI.exe` vers un autre emplacement
2. Double-cliquez dessus pour l'exécuter
3. Vérifiez que l'application fonctionne correctement

---

## 🔧 Dépannage

### Erreur "Module not found"
Ajoutez le module manquant dans `hiddenimports` :
```python
hiddenimports=[
    'nidaqmx',
    'matplotlib',
    'numpy',
    'votre_module_manquant',
],
```

### L'exécutable est trop gros
Utilisez UPX (déjà activé dans le .spec) ou excluez des modules inutiles :
```python
excludes=['PIL', 'pandas', 'scipy'],  # Modules non utilisés
```

### Erreur au lancement
Activez la console pour voir les erreurs :
```python
console=True,
```

---

## 📝 Notes

### Avantages
- ✅ Distribution facile (1 seul fichier)
- ✅ Pas besoin d'installer Python
- ✅ Protection du code source
- ✅ Fonctionne sur tous les Windows (7/8/10/11)

### Limitations
- ⚠️ Taille du fichier importante
- ⚠️ Les drivers NI-DAQmx doivent être installés séparément
- ⚠️ Temps de démarrage légèrement plus long

---

## 🔄 Mise à jour

Pour recréer l'exécutable après modification du code :

```bash
pyinstaller logger_ni.spec --clean
```

Ou utilisez les scripts `build_exe.bat` / `build_exe.ps1`

---

## 📧 Support

Pour toute question, consultez :
- [Documentation PyInstaller](https://pyinstaller.org/)
- Le fichier `README.md` du projet
