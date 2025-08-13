# Projet de Reconnaissance Faciale – Stage Majal Berkane

## À propos
Ce dépôt regroupe les scripts principaux utilisés dans le projet de reconnaissance faciale réalisé durant mon stage chez Majal Berkane pour l’Innovation et l’Intelligence Territoriale.

## Confidentialité
Pour des raisons de confidentialité, certains fichiers ne sont pas inclus dans ce dépôt, notamment ceux contenant des données ou images d’employés.  
**Seuls les fichiers essentiels au fonctionnement et à la compréhension du projet sont publiés**.

## Contenu du dépôt
- **Scripts Python** (reconnaissance faciale, utilitaires, administration)
- **Code web utilisateur** (HTML/CSS/JS) — partiellement publié
- Configuration et exemples — **sans données sensibles**

## Scripts principaux

### `face_encoder.py`
Transforme les **images existantes** (jeu de données déjà collecté) en **vecteurs (embeddings)** pour entraîner/mettre à jour la base de visages connue.

### `face_recognizer.py`
Convertit les **nouvelles images** capturées par la caméra en **vecteurs**, puis **compare** ces vecteurs à ceux déjà enregistrés pour **identifier** les personnes.

### `detection_utils.py`
Gère le **cycle de vie des détections** dans la base de données :
- Vérification de la validité des données
- Chargement des dernières détections
- Calcul de **statistiques** (total, % reconnus, alertes)
- Vérification d’existence d’une détection
- **Enregistrement** de nouvelles détections

### `utils_admin.py`
Outils d’**administration** et de **suivi** du système :
- Lecture des utilisateurs (hors administrateur)
- Calcul du **nombre d’utilisateurs** et du **total des salaires**
- Analyse des **logs** (taux de reconnaissance, alertes)
- Aide à la **gestion** globale de la base et des indicateurs

## Site utilisateur (HTML)
Le dépôt contient également les pages HTML du site utilisateur permettant la consultation et la gestion des informations personnelles :
- `Accueil.html` — Page d’accueil de l’utilisateur
- `ProfilePage.html` — Consultation du profil utilisateur
- `ChangePassword.html` — Modification du mot de passe
- `EditProfileInfo.html` — Modification des informations du profil
- `Reclamation.html` — Formulaire de réclamation

## Contact
Pour toute question : *hamzabouj10@gmail.com*
