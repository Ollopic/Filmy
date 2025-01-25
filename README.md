<p align="center">
  <img src="https://img.shields.io/github/languages/top/Ollopic/Filmy "Language"" alt=" Language" />
  <img src="https://img.shields.io/github/stars/Ollopic/Filmy "Stars"" alt=" Stars" />
  <img src="https://img.shields.io/github/contributors/Ollopic/Filmy "Contributors"" alt=" Contributors" />
</p>

# Filmy

Bibliothèque de films numériques et physiques

## Auteurs

Maréchal Antoine
Lemont Gaétan

[![Contributors](https://contrib.rocks/image?repo=Ollopic/Filmy)](https://github.com/Ollopic/Filmy/graphs/contributors)

## Prérequis

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git): Téléchargez et installez Git en suivant les instructions de votre OS. Pour vérifier que Git a été installé avec succès, exécutez `git --version`.
- [Docker](https://docs.docker.com/get-docker/): Téléchargez et installez Docker en suivant les instructions de votre OS. Pour vérifier que Docker a été installé avec succès, exécutez `docker --version`.


## Lancer localement

1. Cloner le dépôt Filmy :  
```bash  
git clone https://github.com/Ollopic/Filmy
```
2. Vous pouvez lancer l'app en faisant simplement une de ces deux commandes :  
```bash  
make init
docker compose up -d
```

L'application sera accessible en local via l'adresse http://localhost:8080.


## Accès à la partie Admin
Une partie administrateur est disponible à l'adresse http://localhost:8002/admin. Un compte admin par défaut est créé avec les identifiants suivants :

- **Email** : admin@example.com
- **Mot de passe** : admin

Cela vous permet de tester à la fois l'application principale et la section administrateur. Pour se connecter, rendez-vous sur la page de connexion de l'application (http://localhost:8080/auth/login) et utilisez les identifiants ci-dessus.


## Déploiement global
Pour lancer l'ensemble du projet, y compris l'app et l'API, un fichier Docker Compose est disponible dans le projet. Vous pouvez le retrouver ici : [compose.yml](./docker/compose.yml)
Un compte The Movie Database est nécessaire pour lancer l'API. Afin de pouvoir tester l'app directement, un compte spécial a été fait uniquement pour cette utilisation. Le token est déjà renseigné dans les variables dans le compose.
Vous retrouverez également le Dockerfile ayant servi a build l'image de l'app ici : [Dockerfile](./docker/Dockerfile.prod)
Plus d'informations sont affichées dans le [README](./docker/README.md) de la partie Docker.


## API
Pour voir la partie API, rendez-vous sur le dépôt suivant : [Filmy API](https://github.com/Ollopic/Filmy-api)