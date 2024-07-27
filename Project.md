
# Projet de Scraping d'Annonces Immobilières sur Leboncoin.fr

## Contexte et Objectifs

Ce projet vise à développer un module de scraping pour récupérer des annonces de ventes immobilières sur le site leboncoin.fr. L'objectif est de vérifier quotidiennement si de nouvelles annonces ont été postées dans des villes spécifiques et de conserver un historique des annonces pour permettre des comparaisons ultérieures. À terme, ce module pourrait être étendu pour scrapper d'autres sites.

### Fonctionnalités Principales

1. **Scraping des Annonces :**
   - Récupération des annonces de ventes immobilières à partir d'un lien spécifique.
   - Extraction des informations clés : Titre, Date de publication, Prix, Lien.

2. **Comparaison des Annonces :**
   - Comparaison des nouvelles annonces avec l'historique pour détecter les nouvelles annonces ou les changements de prix.

3. **Stockage des Données :**
   - Stockage des annonces sous format JSON, un fichier par ville (basé sur le code postal).

4. **Gestion des Proxies et Captchas :**
   - Intégration du service Web Unlocker de brightdata.fr pour gérer les proxies et les captchas.

### Fréquence et Exécution

- Le script sera exécuté quotidiennement pour vérifier les nouvelles annonces.
- Initialement, les tests seront réalisés en local sur Windows, avec une migration prévue vers une VM Linux pour l'exécution à terme.

### Structure du Projet

1. **Modules de Scraping :**
   - **scraper.py :** Contient les fonctions pour récupérer les annonces depuis un lien donné.
   - **parsing.py :** Contient les fonctions pour extraire les données pertinentes des pages HTML.

2. **Modules de Gestion des Données :**
   - **storage.py :** Gère le stockage et la récupération des données JSON.
   - **comparison.py :** Gère la comparaison entre les nouvelles annonces et l'historique.

3. **Modules de Configuration et Utilitaires :**
   - **config.py :** Contient les configurations globales, y compris les paramètres du proxy.
   - **utils.py :** Contient des fonctions utilitaires pour des tâches diverses (ex : gestion des dates).

4. **Modules de Notification (à implémenter plus tard) :**
   - **notification.py :** Enverra des notifications en cas de nouvelles annonces ou de changements de prix.

### Détails Techniques

1. **Scraping :**
   - Utilisation des bibliothèques BeautifulSoup et Selectolax pour le parsing HTML.
   - Utilisation de Playwright pour automatiser la navigation et contourner les protections anti-bot.
   - Configuration des headers HTTP pour simuler une navigation humaine.

2. **Stockage des Données :**
   - Stockage des annonces sous format JSON, avec un fichier par ville. Exemple de structure :

     ```json
     {
         "annonces": [
             {
                 "titre": "Appartement T3",
                 "date_publication": "2024-07-26",
                 "prix": "250000",
                 "lien": "https://www.leboncoin.fr/ventes_immobilieres/1234567890"
             },
         ]
     }
     ```

3. **Gestion des Proxies :**
   - Intégration du service Web Unlocker de brightdata.fr pour gérer les proxies et les captchas.
   - Configuration des proxies directement dans les requêtes HTTP.

4. **Comparaison des Annonces :**
   - Comparaison basée sur le titre et le lien de l'annonce pour identifier les nouvelles annonces.
   - Stockage des annonces mises à jour dans le même fichier JSON, avec une logique pour ajouter de nouvelles annonces ou mettre à jour les prix.

### Structure des Dossiers et Fichiers

project_root/
│
├── leboncoin/
│   ├── **init**.py
│   ├── scraper.py
│   ├── parsing.py
│   ├── config.py
│   └── utils.py
│
├── storage.py
├── comparison.py
└── notification.py

## Conclusion

En structurant ainsi le projet, nous séparons les éléments spécifiques à leboncoin.fr des éléments généraux, ce qui permet une meilleure modularité et facilité d'extension vers d'autres sites à l'avenir. Le code est organisé de manière à être clair, maintenable et évolutif.
