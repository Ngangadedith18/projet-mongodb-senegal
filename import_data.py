from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["alimentation_senegal"]

# ── On repart de zéro à chaque import ──
db.restaurants.drop()
db.plats.drop()
db.clients.drop()
db.commandes.drop()
db.livreurs.drop()

# ────────────────────────────────────────
# Collection 1 : restaurants
# ────────────────────────────────────────
db.restaurants.insert_many([
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e001"),
    "nom": "Chez Fatou - Thiéboudienne",
    "adresse": {
      "rue": "Rue 10", "ville": "Dakar", "quartier": "Ouakam",
      "code_postal": "10000",
      "coordinates": {"type": "Point", "coordinates": [-17.476, 14.716]}
    },
    "telephone": "77 123 45 01",
    "specialites": ["Thiéboudienne", "Yassa Poulet"],
    "note_moyenne": 4.5,
    "zone_livraison": ["Dakar", "Pikine", "Guédiawaye"],
    "ouvert": True
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e002"),
    "nom": "La Marmite de Mame Diarra",
    "adresse": {
      "ville": "Dakar", "quartier": "Mermoz",
      "coordinates": {"type": "Point", "coordinates": [-17.472, 14.710]}
    },
    "specialites": ["Mafé", "Soupe Kandia", "Thiéboudienne"],
    "note_moyenne": 4.8,
    "zone_livraison": ["Dakar", "Almadies"],
    "ouvert": True
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e003"),
    "nom": "Dibi Star Thiès",
    "adresse": {
      "ville": "Thiès", "quartier": "Centre",
      "coordinates": {"type": "Point", "coordinates": [-16.924, 14.802]}
    },
    "specialites": ["Dibi", "Yassa Poisson"],
    "note_moyenne": 4.2,
    "zone_livraison": ["Thiès", "Tivaouane"],
    "ouvert": True
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e004"),
    "nom": "Saint-Louis Plateau",
    "adresse": {
      "ville": "Saint-Louis", "quartier": "Île",
      "coordinates": {"type": "Point", "coordinates": [-16.503, 16.025]}
    },
    "specialites": ["Caldou", "Soupe Kandia", "Thiéboudienne"],
    "note_moyenne": 4.6,
    "zone_livraison": ["Saint-Louis", "Ndiareme"],
    "ouvert": False
  }
])

# Index géospatial (obligatoire pour la Question 7)
db.restaurants.create_index([("adresse.coordinates", "2dsphere")])

# ────────────────────────────────────────
# Collection 2 : plats
# ────────────────────────────────────────
db.plats.insert_many([
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e101"),
    "nom": "Thiéboudienne Poisson", "categorie": "plat_principal",
    "prix": 3500, "ingredients": ["riz", "poisson", "légumes", "tomate", "oignon"],
    "regime": ["sans lactose"],
    "restaurant_id": ObjectId("67a1c2d3e4f5a6b7c8d9e001"),
    "preparation_minutes": 45, "calories": 850
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e102"),
    "nom": "Yassa Poulet", "categorie": "plat_principal",
    "prix": 3000, "ingredients": ["poulet", "oignon", "citron", "moutarde"],
    "regime": [],
    "restaurant_id": ObjectId("67a1c2d3e4f5a6b7c8d9e001"),
    "preparation_minutes": 30, "calories": 720
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e103"),
    "nom": "Mafé Tofu", "categorie": "plat_principal",
    "prix": 2800, "ingredients": ["tofu", "pâte arachide", "légumes"],
    "regime": ["vegetarien", "vegan"],
    "restaurant_id": ObjectId("67a1c2d3e4f5a6b7c8d9e002"),
    "preparation_minutes": 40, "calories": 680
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e104"),
    "nom": "Dibi Mouton", "categorie": "grillade",
    "prix": 4500, "ingredients": ["mouton", "moutarde", "oignon"],
    "regime": ["sans gluten"],
    "restaurant_id": ObjectId("67a1c2d3e4f5a6b7c8d9e003"),
    "preparation_minutes": 25, "calories": 950
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e105"),
    "nom": "Caldou (Poisson)", "categorie": "plat_principal",
    "prix": 4000, "ingredients": ["poisson", "légumes", "plantain"],
    "regime": [],
    "restaurant_id": ObjectId("67a1c2d3e4f5a6b7c8d9e004"),
    "preparation_minutes": 50, "calories": 800
  }
])

# ────────────────────────────────────────
# Collection 3 : clients
# ────────────────────────────────────────
db.clients.insert_many([
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e201"),
    "prenom": "Ousmane", "nom": "Sarr",
    "email": "ousmane.sarr@example.sn", "telephone": "77 111 22 33",
    "ville": "Dakar",
    "adresse_coord": {"type": "Point", "coordinates": [-17.480, 14.720]},
    "points_fidelite": 150,
    "date_inscription": datetime(2024, 1, 15, tzinfo=timezone.utc)
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e202"),
    "prenom": "Aïssatou", "nom": "Ndiaye",
    "email": "aissatou.ndiaye@example.sn", "telephone": "78 222 33 44",
    "ville": "Dakar",
    "adresse_coord": {"type": "Point", "coordinates": [-17.465, 14.708]},
    "points_fidelite": 320,
    "date_inscription": datetime(2023, 9, 10, tzinfo=timezone.utc)
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e203"),
    "prenom": "Ibrahima", "nom": "Fall",
    "telephone": "70 333 44 55", "ville": "Thiès",
    "adresse_coord": {"type": "Point", "coordinates": [-16.924, 14.802]},
    "points_fidelite": 45,
    "date_inscription": datetime(2024, 6, 20, tzinfo=timezone.utc)
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e204"),
    "prenom": "Fatou", "nom": "Diop",
    "ville": "Saint-Louis",
    "adresse_coord": {"type": "Point", "coordinates": [-16.503, 16.025]},
    "points_fidelite": 210,
    "date_inscription": datetime(2023, 12, 1, tzinfo=timezone.utc)
  }
])

# ────────────────────────────────────────
# Collection 4 : commandes
# ────────────────────────────────────────
db.commandes.insert_many([
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e301"),
    "client_id": ObjectId("67a1c2d3e4f5a6b7c8d9e201"),
    "date_commande": datetime(2025, 6, 10, 12, 30, tzinfo=timezone.utc),
    "statut": "livrée", "mode_paiement": "Mobile Money", "total": 6500,
    "articles": [
      {"plat_id": ObjectId("67a1c2d3e4f5a6b7c8d9e101"), "quantite": 1, "prix_unitaire": 3500, "nom_plat": "Thiéboudienne Poisson"},
      {"plat_id": ObjectId("67a1c2d3e4f5a6b7c8d9e102"), "quantite": 1, "prix_unitaire": 3000, "nom_plat": "Yassa Poulet"}
    ],
    "livreur_id": ObjectId("67a1c2d3e4f5a6b7c8d9e401"),
    "delai_livraison_minutes": 35
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e302"),
    "client_id": ObjectId("67a1c2d3e4f5a6b7c8d9e202"),
    "date_commande": datetime(2025, 6, 11, 19, 15, tzinfo=timezone.utc),
    "statut": "en_cours", "mode_paiement": "Carte", "total": 2800,
    "articles": [
      {"plat_id": ObjectId("67a1c2d3e4f5a6b7c8d9e103"), "quantite": 1, "prix_unitaire": 2800, "nom_plat": "Mafé Tofu"}
    ],
    "livreur_id": ObjectId("67a1c2d3e4f5a6b7c8d9e402"),
    "delai_livraison_minutes": None
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e303"),
    "client_id": ObjectId("67a1c2d3e4f5a6b7c8d9e202"),
    "date_commande": datetime(2025, 6, 5, 13, 0, tzinfo=timezone.utc),
    "statut": "livrée", "mode_paiement": "Mobile Money", "total": 4500,
    "articles": [
      {"plat_id": ObjectId("67a1c2d3e4f5a6b7c8d9e104"), "quantite": 1, "prix_unitaire": 4500, "nom_plat": "Dibi Mouton"}
    ],
    "livreur_id": ObjectId("67a1c2d3e4f5a6b7c8d9e401"),
    "delai_livraison_minutes": 28
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e304"),
    "client_id": ObjectId("67a1c2d3e4f5a6b7c8d9e203"),
    "date_commande": datetime(2025, 6, 12, 20, 0, tzinfo=timezone.utc),
    "statut": "annulée", "mode_paiement": "Espèces", "total": 4000,
    "articles": [
      {"plat_id": ObjectId("67a1c2d3e4f5a6b7c8d9e105"), "quantite": 1, "prix_unitaire": 4000, "nom_plat": "Caldou"}
    ],
    "livreur_id": None,
    "delai_livraison_minutes": None
  }
])

# ────────────────────────────────────────
# Collection 5 : livreurs
# ────────────────────────────────────────
db.livreurs.insert_many([
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e401"),
    "nom": "Moussa Diagne", "telephone": "70 111 22 33",
    "zone": "Dakar", "nb_livraisons": 128,
    "note_moyenne": 4.9, "disponible": True
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e402"),
    "nom": "Ndeye Diallo", "telephone": "78 222 33 44",
    "zone": "Dakar", "nb_livraisons": 94,
    "note_moyenne": 4.7, "disponible": True
  },
  {
    "_id": ObjectId("67a1c2d3e4f5a6b7c8d9e403"),
    "nom": "Aliou Sene", "telephone": "76 333 44 55",
    "zone": "Thiès", "nb_livraisons": 45,
    "note_moyenne": 4.5, "disponible": False
  }
])

print("✅ Dataset importé avec succès dans 'alimentation_senegal' !")
print(f"   - Restaurants : {db.restaurants.count_documents({})}")
print(f"   - Plats       : {db.plats.count_documents({})}")
print(f"   - Clients     : {db.clients.count_documents({})}")
print(f"   - Commandes   : {db.commandes.count_documents({})}")
print(f"   - Livreurs    : {db.livreurs.count_documents({})}")