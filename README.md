# Alimentation & Gastronomie Sénégal — MongoDB

Application web d'analyse de données de restauration et de livraison de plats traditionnels sénégalais, développée avec **Python**, **Flask**, **PyMongo** et **MongoDB**.

---

## Présentation

Ce projet répond à 10 requêtes d'agrégation MongoDB sur une base de données composée de 5 collections :

| Collection | Description |
|------------|-------------|
| `restaurants` | Établissements de restauration avec coordonnées GPS |
| `plats` | Plats proposés avec prix, ingrédients et régimes |
| `clients` | Clients avec points de fidélité et localisation |
| `commandes` | Commandes avec statut, articles et mode de paiement |
| `livreurs` | Livreurs avec zone, note et disponibilité |

---

## Technologies utilisées

- **Python 3.10+**
- **Flask** — serveur web
- **PyMongo** — connexion et requêtes MongoDB
- **MongoDB** — base de données NoSQL
- **Chart.js** — visualisations graphiques
- **Font Awesome** — icônes
- **HTML / CSS / JavaScript** — interface frontend

---

## Structure du projet

```
projet-mongodb/
├── app.py               # Serveur Flask (routes API)
├── db.py                # Connexion MongoDB + 10 pipelines d'agrégation
├── import_data.py       # Script d'import du dataset dans MongoDB
├── requirements.txt     # Dépendances Python
├── templates/
│   └── index.html       # Interface web principale
└── static/
    └── style.css        # Feuille de styles
```

---

## Installation et exécution

### 1. Prérequis

- Python 3.10 ou supérieur
- MongoDB installé et démarré localement sur le port `27017`

### 2. Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/projet-mongodb-senegal.git
cd projet-mongodb-senegal
```

### 3. Créer et activer l'environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Importer le dataset dans MongoDB

```bash
python import_data.py
```

Résultat attendu :
```
✅ Dataset importé avec succès dans 'alimentation_senegal' !
   - Restaurants : 4
   - Plats       : 5
   - Clients     : 4
   - Commandes   : 4
   - Livreurs    : 3
```

### 6. Lancer l'application

```bash
python app.py
```

Ouvrir dans le navigateur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Les 10 requêtes MongoDB

| # | Description | Opérateurs utilisés |
|---|-------------|---------------------|
| Q1 | Restaurants de Dakar avec leurs plats, triés par note | `$match`, `$lookup`, `$sort` |
| Q2 | Total dépensé par client (commandes livrées) | `$match`, `$group`, `$lookup` |
| Q3 | Top 3 plats les plus commandés | `$unwind`, `$group`, `$limit` |
| Q4 | Revenu par mode de paiement avec pourcentage | `$group` double, `$project` |
| Q5 | Clients ayant commandé tofu ET poisson | `$lookup`, filtrage Python |
| Q6 | Dashboard : statuts + CA mensuel + top clients | `$facet` |
| Q7 | 2 restaurants les plus proches (géospatial) | `$geoNear`, index `2dsphere` |
| Q8 | Statistiques par livreur | `$match`, `$group`, `$lookup` |
| Q9 | Commandes avec plat végétarien ou vegan | `$lookup`, `$match`, `$count` |
| Q10 | Recommandations pour Ousmane Sarr | Filtrage collaboratif Python |

---

## Qualité du code

Le code a été analysé avec **pylint** :

| Fichier | Note |
|---------|------|
| `app.py` | ✅ 10/10 |
| `db.py` | ✅ 10/10 |

---

## Auteur

Projet réalisé par D'edith NGANGA dans le cadre d'un TP MongoDB.