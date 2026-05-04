"""
db.py — Connexion MongoDB et pipelines d'agrégation.
Base de données : alimentation_senegal
Collections     : restaurants, plats, clients, commandes, livreurs
"""

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["alimentation_senegal"]


def get_db():
    """Retourne l'objet base de données MongoDB."""
    return db


def serialize(data):
    """Convertit les ObjectId en string pour permettre la sérialisation JSON par Flask."""
    for doc in data:
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, list):
                doc[key] = [str(i) if isinstance(i, ObjectId) else i for i in value]
    return data


def q1():
    """
    Retourne les restaurants de Dakar avec leurs plats, triés par note décroissante.
    Utilise $match, $lookup, $project et $sort.
    """
    pipeline = [
        {"$match": {"adresse.ville": "Dakar"}},
        {"$lookup": {
            "from": "plats",
            "localField": "_id",
            "foreignField": "restaurant_id",
            "as": "plats"
        }},
        {"$project": {
            "nom": 1,
            "note_moyenne": 1,
            "plats": {"nom": 1, "prix": 1}
        }},
        {"$sort": {"note_moyenne": -1}}
    ]
    return serialize(list(db.restaurants.aggregate(pipeline)))


def q2():
    """
    Retourne le total dépensé, le nombre de commandes et la moyenne par client.
    Ne prend en compte que les commandes au statut 'livrée'.
    Utilise $match, $group, $lookup, $unwind, $project et $sort.
    """
    pipeline = [
        {"$match": {"statut": "livrée"}},
        {"$group": {
            "_id": "$client_id",
            "total_depense": {"$sum": "$total"},
            "nb_commandes": {"$sum": 1},
            "moyenne_commande": {"$avg": "$total"}
        }},
        {"$lookup": {
            "from": "clients",
            "localField": "_id",
            "foreignField": "_id",
            "as": "client"
        }},
        {"$unwind": "$client"},
        {"$project": {
            "nom_client": {"$concat": ["$client.prenom", " ", "$client.nom"]},
            "total_depense": 1,
            "nb_commandes": 1,
            "moyenne_commande": {"$round": ["$moyenne_commande", 0]}
        }},
        {"$sort": {"total_depense": -1}}
    ]
    return serialize(list(db.commandes.aggregate(pipeline)))


def q3():
    """
    Retourne le top 3 des plats les plus commandés avec quantité totale et prix moyen.
    Utilise $unwind, $group, $sort, $limit et $lookup.
    """
    pipeline = [
        {"$unwind": "$articles"},
        {"$group": {
            "_id": "$articles.plat_id",
            "nom_plat": {"$first": "$articles.nom_plat"},
            "quantite_totale": {"$sum": "$articles.quantite"},
            "prix_moyen": {"$avg": "$articles.prix_unitaire"}
        }},
        {"$sort": {"quantite_totale": -1}},
        {"$limit": 3},
        {"$lookup": {
            "from": "plats",
            "localField": "_id",
            "foreignField": "_id",
            "as": "detail"
        }},
        {"$unwind": {"path": "$detail", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "nom_plat": 1,
            "quantite_totale": 1,
            "prix_moyen": {"$round": ["$prix_moyen", 0]},
            "restaurant_id": "$detail.restaurant_id"
        }}
    ]
    return serialize(list(db.commandes.aggregate(pipeline)))


def q4():
    """
    Retourne le revenu total par mode de paiement avec son pourcentage du CA global.
    Utilise un double $group pour calculer les pourcentages.
    """
    pipeline = [
        {"$match": {"statut": "livrée"}},
        {"$group": {
            "_id": "$mode_paiement",
            "total": {"$sum": "$total"}
        }},
        {"$group": {
            "_id": None,
            "modes": {"$push": {"mode": "$_id", "total": "$total"}},
            "grand_total": {"$sum": "$total"}
        }},
        {"$unwind": "$modes"},
        {"$project": {
            "_id": 0,
            "mode": "$modes.mode",
            "total": "$modes.total",
            "pourcentage": {
                "$round": [
                    {"$multiply": [
                        {"$divide": ["$modes.total", "$grand_total"]}, 100
                    ]}, 1
                ]
            }
        }}
    ]
    return list(db.commandes.aggregate(pipeline))


def q5():
    """
    Retourne les clients ayant commandé un plat avec tofu ET un plat avec poisson
    dans des commandes différentes. Filtrage final effectué en Python.
    """
    pipeline = [
        {"$unwind": "$articles"},
        {"$lookup": {
            "from": "plats",
            "localField": "articles.plat_id",
            "foreignField": "_id",
            "as": "plat_detail"
        }},
        {"$unwind": "$plat_detail"},
        {"$group": {
            "_id": "$client_id",
            "ingredients": {"$addToSet": "$plat_detail.ingredients"}
        }},
        {"$lookup": {
            "from": "clients",
            "localField": "_id",
            "foreignField": "_id",
            "as": "client"
        }},
        {"$unwind": "$client"},
        {"$project": {
            "nom_client": {"$concat": ["$client.prenom", " ", "$client.nom"]},
            "ingredients": 1
        }}
    ]
    results = list(db.commandes.aggregate(pipeline))
    filtered = []
    for doc in results:
        all_ingredients = [i for sublist in doc.get("ingredients", []) for i in sublist]
        has_tofu    = any("tofu"    in ing for ing in all_ingredients)
        has_poisson = any("poisson" in ing for ing in all_ingredients)
        if has_tofu and has_poisson:
            filtered.append({"nom_client": doc["nom_client"]})
    return filtered


def q6():
    """
    Retourne un dashboard via $facet combinant trois analyses en un seul appel :
    répartition des statuts, CA mensuel et top 3 clients par points de fidélité.
    """
    pipeline = [
        {"$facet": {
            "repartition_statuts": [
                {"$group": {"_id": "$statut", "count": {"$sum": 1}}}
            ],
            "ca_mensuel": [
                {"$match": {"statut": "livrée"}},
                {"$group": {
                    "_id": {
                        "mois": {"$month": "$date_commande"},
                        "annee": {"$year": "$date_commande"}
                    },
                    "montant_total": {"$sum": "$total"}
                }},
                {"$sort": {"_id.annee": 1, "_id.mois": 1}}
            ],
            "top3_clients": [
                {"$lookup": {
                    "from": "clients",
                    "localField": "client_id",
                    "foreignField": "_id",
                    "as": "client"
                }},
                {"$unwind": "$client"},
                {"$sort": {"client.points_fidelite": -1}},
                {"$limit": 3},
                {"$project": {
                    "_id": 0,
                    "nom": {"$concat": ["$client.prenom", " ", "$client.nom"]},
                    "points_fidelite": "$client.points_fidelite"
                }}
            ]
        }}
    ]
    return list(db.commandes.aggregate(pipeline))


def q7():
    """
    Retourne les 2 restaurants les plus proches des coordonnées d'Ousmane Sarr.
    Utilise $geoNear (requiert un index 2dsphere) suivi d'un $limit séparé.
    """
    pipeline = [
        {"$geoNear": {
            "near": {"type": "Point", "coordinates": [-17.480, 14.720]},
            "distanceField": "distance_metres",
            "spherical": True
        }},
        {"$limit": 2},
        {"$project": {
            "nom": 1,
            "distance_metres": {"$round": ["$distance_metres", 0]}
        }}
    ]
    return serialize(list(db.restaurants.aggregate(pipeline)))


def q8():
    """
    Retourne les statistiques par livreur : nombre de livraisons,
    délai moyen et note moyenne. Filtre sur les commandes livrées uniquement.
    """
    pipeline = [
        {"$match": {"statut": "livrée", "livreur_id": {"$ne": None}}},
        {"$group": {
            "_id": "$livreur_id",
            "nb_commandes": {"$sum": 1},
            "delai_moyen": {"$avg": "$delai_livraison_minutes"}
        }},
        {"$lookup": {
            "from": "livreurs",
            "localField": "_id",
            "foreignField": "_id",
            "as": "livreur"
        }},
        {"$unwind": "$livreur"},
        {"$project": {
            "_id": 0,
            "nom_livreur": "$livreur.nom",
            "nb_commandes": 1,
            "delai_moyen": {"$round": ["$delai_moyen", 1]},
            "note_moyenne": "$livreur.note_moyenne"
        }}
    ]
    return list(db.commandes.aggregate(pipeline))


def q9():
    """
    Retourne le nombre de commandes contenant au moins un plat végétarien ou vegan.
    Utilise $lookup, $match sur le champ 'regime', $group pour dédoublonner et $count.
    """
    pipeline = [
        {"$unwind": "$articles"},
        {"$lookup": {
            "from": "plats",
            "localField": "articles.plat_id",
            "foreignField": "_id",
            "as": "plat"
        }},
        {"$unwind": "$plat"},
        {"$match": {
            "plat.regime": {"$in": ["vegetarien", "vegan"]}
        }},
        {"$group": {"_id": "$_id"}},
        {"$count": "nb_commandes_veg"}
    ]
    return list(db.commandes.aggregate(pipeline))


def q10():
    """
    Retourne des recommandations de plats pour Ousmane Sarr basées sur
    le filtrage collaboratif : plats commandés par d'autres clients dakarois
    mais jamais commandés par Ousmane Sarr.
    """
    ousmane_id = ObjectId("67a1c2d3e4f5a6b7c8d9e201")

    pipeline = [
        {"$lookup": {
            "from": "clients",
            "localField": "client_id",
            "foreignField": "_id",
            "as": "client"
        }},
        {"$unwind": "$client"},
        {"$unwind": "$articles"},
        {"$group": {
            "_id": "$client_id",
            "ville": {"$first": "$client.ville"},
            "plats_commandes": {"$addToSet": "$articles.plat_id"}
        }},
        {"$match": {"ville": "Dakar"}}
    ]

    results = list(db.commandes.aggregate(pipeline))

    ousmane_plats = set()
    autres_plats  = set()

    for entry in results:
        plats = set(str(p) for p in entry["plats_commandes"])
        if entry["_id"] == ousmane_id:
            ousmane_plats = plats
        else:
            autres_plats.update(plats)

    recommandations_ids = autres_plats - ousmane_plats
    recommandations = []
    for pid in recommandations_ids:
        plat = db.plats.find_one({"_id": ObjectId(pid)}, {"nom": 1, "prix": 1})
        if plat:
            recommandations.append({"nom": plat["nom"], "prix": plat["prix"]})

    return recommandations
