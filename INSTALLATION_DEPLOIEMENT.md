# 📦 Guide d'installation et de déploiement - Logger NI

## ✅ CONFIRMATION : Installation simple en 2 étapes

Oui, c'est **exactement ça** ! Vous n'avez besoin que de :

1. ✅ **Installer NI-DAQmx** sur le PC cible
2. ✅ **Copier l'exécutable** `LoggerNI.exe`

C'est tout ! 🎉

---

## 📋 Installation détaillée

### Étape 1️⃣ : Installer NI-DAQmx Runtime

#### Sur le PC cible (où vous voulez utiliser Logger NI) :

1. **Télécharger NI-DAQmx Runtime** depuis :
   - Site officiel : https://www.ni.com/fr-fr/support/downloads/drivers/download.ni-daqmx.html
   - Chercher : "NI-DAQmx Runtime" (GRATUIT)

2. **Installer** :
   - Version recommandée : **NI-DAQmx 2023 Q3** ou plus récent
   - Suivre l'assistant d'installation
   - Redémarrer si demandé

3. **Vérifier l'installation** :
   - Lancer **NI MAX** (National Instruments Measurement & Automation Explorer)
   - Vérifier que vos périphériques DAQ apparaissent
   - Vérifier que vos tâches configurées sont présentes

#### ⚠️ Note importante :
- Le **Runtime** est suffisant (pas besoin du SDK complet)
- Le Runtime est **GRATUIT** et redistribuable
- Taille : environ 500 MB - 1 GB

---

### Étape 2️⃣ : Copier l'exécutable

#### Fichier à copier :

```
dist\LoggerNI.exe
```

#### Où le copier ?

N'importe où sur le PC cible ! Par exemple :
- `C:\Program Files\LoggerNI\LoggerNI.exe`
- `C:\Applications\LoggerNI.exe`
- Sur le Bureau
- Sur une clé USB

#### ✅ L'exécutable est **100% autonome** et contient :
- ✅ Python 3.10.9 embedded
- ✅ numpy, matplotlib, tkinter
- ✅ nidaqmx (bibliothèque Python)
- ✅ Toutes les dépendances
- ✅ Votre code de l'application

---

## 🚀 Utilisation

### Lancement

1. **Double-cliquer** sur `LoggerNI.exe`
2. L'application démarre immédiatement
3. Sélectionner votre tâche DAQmx dans la liste
4. Cliquer sur **Démarrer**

### Première utilisation

Au premier lancement, l'application crée automatiquement :
- `logger_config.json` (configuration)
- Dossier `data/` (par défaut pour l'enregistrement)

---

## 📂 Structure de déploiement recommandée

```
MonDossierApplication/
├── LoggerNI.exe              ← L'exécutable
├── logger_config.json        ← Créé automatiquement au 1er lancement
├── data/                     ← Dossier de données par défaut
│   └── *.txt                 ← Fichiers de mesures
└── README.txt                ← Documentation utilisateur (optionnel)
```

---

## 🔧 Configuration requise sur le PC cible

### Système d'exploitation
- ✅ Windows 7 / 8 / 10 / 11 (64 bits)
- ✅ Pas besoin de Python installé
- ✅ Pas besoin de Visual Studio
- ✅ Pas besoin d'autres outils de développement

### Matériel
- ✅ Carte d'acquisition NI-DAQmx compatible
- ✅ 4 GB RAM minimum (8 GB recommandé)
- ✅ 100 MB d'espace disque (+ espace pour les données)

### Logiciels
- ✅ **NI-DAQmx Runtime** (seul prérequis)
- ✅ Tâches DAQmx configurées dans NI MAX

---

## 🎯 Fonctionnalités incluses dans l'exécutable

### Version actuelle : **2.3**

✅ **Acquisition de données**
- Échantillonnage à 10 Hz
- Support multi-canaux
- Affichage temps réel

✅ **Enregistrement**
- Fichiers TXT avec timestamp précis
- Période d'enregistrement configurable
- Choix du répertoire de sauvegarde

✅ **Timestamps ultra-précis**
- Basés sur le compteur de points
- Précision : nanosecondes
- Stable sur plusieurs mois

✅ **Interface graphique**
- Sélection de tâche DAQmx
- Configuration de la période
- Graphiques temps réel
- Préfixe et commentaire personnalisables

✅ **Configuration**
- Sauvegarde automatique des paramètres
- Répertoire d'enregistrement personnalisable
- Restauration des derniers paramètres

---

## 📝 Distribution à plusieurs utilisateurs

### Pour distribuer à d'autres personnes :

1. **Créer un dossier** :
   ```
   LoggerNI_v2.3/
   ├── LoggerNI.exe
   └── INSTALL.txt  (ce fichier)
   ```

2. **Compresser** en .zip

3. **Partager** par email, clé USB, réseau, etc.

4. **Instructions pour l'utilisateur final** :
   ```
   1. Installer NI-DAQmx Runtime (lien fourni)
   2. Extraire le .zip
   3. Double-cliquer sur LoggerNI.exe
   ```

---

## ❓ Dépannage

### L'exécutable ne démarre pas
- ✅ Vérifier que NI-DAQmx Runtime est installé
- ✅ Vérifier les droits d'administrateur (si nécessaire)
- ✅ Vérifier l'antivirus (ajouter une exception)

### "Aucune tâche DAQmx configurée"
- ✅ Ouvrir NI MAX
- ✅ Créer ou importer vos tâches DAQmx
- ✅ Vérifier que les tâches sont bien enregistrées

### Erreur au démarrage de l'acquisition
- ✅ Vérifier que la carte DAQ est connectée
- ✅ Vérifier dans NI MAX que la carte est détectée
- ✅ Tester la tâche dans NI MAX avant

---

## 🔄 Mise à jour

Pour mettre à jour l'application :
1. Remplacer `LoggerNI.exe` par la nouvelle version
2. Conserver `logger_config.json` (paramètres)
3. Conserver le dossier `data/` (données)

---

## 📊 Taille du fichier

- **LoggerNI.exe** : ~50-60 MB
- Compact pour un exécutable Python complet !

---

## ✅ Checklist avant déploiement

- [ ] NI-DAQmx Runtime installé sur le PC cible
- [ ] Carte DAQ connectée et détectée
- [ ] Tâches DAQmx configurées dans NI MAX
- [ ] LoggerNI.exe copié sur le PC
- [ ] Test de lancement : OK
- [ ] Test d'acquisition : OK
- [ ] Test d'enregistrement : OK

---

## 🎉 Résumé

**OUI, vous confirmez bien :**

> Je n'ai qu'à installer DAQmx sur le PC et copier l'exécutable

**C'est exactement ça !** 👍

- ✅ Pas de Python à installer
- ✅ Pas de dépendances supplémentaires
- ✅ Pas de fichiers .py à distribuer
- ✅ Pas de configuration complexe
- ✅ Juste DAQmx + EXE = ✨ Ça marche !

---

**Version de ce guide** : 2.3  
**Date** : 5 décembre 2024  
**Emplacement de l'exécutable** : `C:\TRAVAIL\RepositoriesGithub\Logger NI\dist\LoggerNI.exe`
