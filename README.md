# Gestionnaire de Mots de Passe
    by Adrien Mertens

## Description
Un gestionnaire de mots de passe sécurisé construit avec Python 3.13 et ttkbootstrap pour l'interface graphique. Ce projet permet aux utilisateurs de stocker et de gérer leurs mots de passe de manière sécurisée et efficace.

## Fonctionnalités
- **Enregistrement de mots de passe** : Ajoutez et stockez vos mots de passe de manière sécurisée.
- **Interface Utilisateur Intuitive** : Utilisation de ttkbootstrap pour une expérience utilisateur fluide et moderne.

## Installation

### Prérequis
Avant de commencer, assurez-vous d'avoir installé :
- Python 3.13
- ttkbootstrap
- pytest
- ruff
- pyinstaller

### Étapes
1. **Création du fichier `app.py`** : Ce fichier sera le lanceur de l'application.
   - Utilisation du modèle MVC : Pour une simplification de la structure des fichiers.
2. **Création du fichier `data.py` et du dossier `models`** : Ce fichier contiendra tout le code lié à la gestion des données (enregistrement, modification, etc.) et le dossier contient tous les fichiers Python destinés à la gestion de la base de données.
3. **Développement du fichier `data.py` avec sqlite3**.
4. **Création du dossier `views` et des fichiers** : Ce dossier comprend tous les fichiers qui gèrent la vue ou l'interface graphique.
5. **Développement des fichiers du dossier `views`**.
6. **Création du dossier `controllers` et du fichier `controllerDatas`**.
7. **Développement du fichier `controllerDatas.py`**.
8. **Création du dossier `tests`** : Il comprend tous les tests du projet.
9. **Développement des fichiers qui testent le projet**.
10. **Création d'un exécutable avec PyInstaller** : Commande utilisée :
    ```bash
    pyinstaller --onedir --windowed --name EasyPassword --icon=ico/logo.ico app.py
    ```

## Structure des fichiers
- `models` : Ce dossier répertorie tous les fichiers Python utilisés pour la gestion des données.
- `views` : Ce dossier répertorie toutes les vues de l'application, c'est-à-dire les fichiers qui gèrent l'interface graphique.
- `controllers` : Ce dossier répertorie tous les fichiers Python qui font le lien entre le modèle et la vue, permettant de gérer la communication entre la vue et le modèle.

## Améliorations
- Sécurisation des données en les cryptant.
- Possibilité de rechercher un élément dans toute la liste.
- Nouvelle interface en toga.
- Utilisation de Briefcase pour créer un fichier `.msi`.
- Utilisation de `random` pour générer un mot de passe aléatoire.
- Exportation des mots de passe et utilisateurs dans un PDF selon le choix de l'utilisateur.
- Importation de mots de passe et utilisateurs selon un format via Chrome ou un navigateur de fichiers.
