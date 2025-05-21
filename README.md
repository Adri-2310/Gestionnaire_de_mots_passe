
## Description

Un gestionnaire de mots de passe sécurisé construit avec Python 3.13 et ttkbootstrap pour l'interface graphique. Ce projet permet aux utilisateurs de stocker et de gérer leurs mots de passe de manière sécurisée et efficace.

## Fonctionnalités

- Enregistrement de mots de passe : Ajoutez et stockez vos mots de passe de manière sécurisée.
- Recherche de mots de passe : Recherchez des mots de passe et des utilisateurs selon un critère spécifique.
- Interface Utilisateur Intuitive : Utilisation de ttkbootstrap pour une expérience utilisateur fluide et moderne.
- Sécurité : Chiffrement des mots de passe pour une protection accrue.

## Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Python 3.13
- ttkbootstrap
- pytest
- ruff

## Développement

### Étapes

1. Création du fichier `app.py` : Ce fichier sera le lanceur de l'application.
   - Utilisation du modèle MVC : Pour une simplification de la structure des fichiers.
2. Création du fichier `data.py` : Ce fichier contiendra tout le code lié à la gestion des données (enregistrement, modification, etc.).
3. development du fichier 'data.py' avec sqlite3
4. development du chichier 'test_data.py' avec pytest
5. ...

## Structure des fichiers

- `models` : Ce dossier répertorie tous les fichiers Python utilisés pour la gestion des données.
- `views` : Ce dossier répertorie toutes les vues de l'application, c'est-à-dire les fichiers qui gèrent l'interface graphique.
- `controllers` : Ce dossier répertorie tous les fichiers Python qui font le lien entre le modèle et la vue, permettant de gérer la communication entre la vue et le modèle.


# development
## étape
1)
* création de du fichier app.py : qui va être le lanceur de l'application.
* utilisation du model MVC : pour plus une simplifaction de la structure des fichiers
2)
* création du fichier data.py qui va contenir tout le code qui est lié à la gestion des données (enregistrement, modification, etc)
3)

## Structure des fichiers
*Models : ce dossier va répertorier tous les fichiers python qui sont pour l'utilisation des données
*views : ce dossier va répertorier toutes les vues de mon application donc les fichiers qui gèrent le gui
*controllers : ce dossier va répertorier tous les fichiers python qui vont faire le lien entre le model et la vue, il va permettre de gérer la communication entre la vue et le model

## amélioration
* ajout de l'url ou source dans l'enregistrement du mot de passe et utilisateur
* nouvelle interface en toga
* utilisation de briefcase pour créer un .msi
* utilisation de random pour générer un mot passe aléatoire 
* utilisation des packages
  - beeware
    - briefcase
      - toga
  - random
* exportation des mots de passe et utilisateur dans un pdf selon le choix de l'utilisateur
* importation de mots de passe et utilisateur selon un format via chrome ou explorateur de navigation