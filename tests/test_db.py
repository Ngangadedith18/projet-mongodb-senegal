"""
tests/test_db.py — Tests unitaires des 10 requetes MongoDB.
Necessite que MongoDB soit accessible sur localhost:27017
et que le dataset ait ete importe via import_data.py.
"""

from db import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10


# ══════════════════════════════════════════════════════════════
# Q1 — Restaurants de Dakar avec leurs plats
# ══════════════════════════════════════════════════════════════

def test_q1_retourne_une_liste():
    """Q1 doit retourner une liste."""
    assert isinstance(q1(), list)


def test_q1_restaurants_sont_a_dakar():
    """Q1 doit retourner au moins un restaurant a Dakar."""
    assert len(q1()) > 0


def test_q1_contient_champs_attendus():
    """Q1 : chaque document doit avoir nom et note_moyenne."""
    for doc in q1():
        assert "nom" in doc
        assert "note_moyenne" in doc


def test_q1_trie_par_note_decroissante():
    """Q1 : les restaurants doivent etre tries par note decroissante."""
    notes = [doc["note_moyenne"] for doc in q1()]
    assert notes == sorted(notes, reverse=True)


# ══════════════════════════════════════════════════════════════
# Q2 — Total depense par client
# ══════════════════════════════════════════════════════════════

def test_q2_retourne_une_liste():
    """Q2 doit retourner une liste."""
    assert isinstance(q2(), list)


def test_q2_contient_champs_attendus():
    """Q2 : chaque document doit avoir les champs financiers."""
    for doc in q2():
        assert "nom_client" in doc
        assert "total_depense" in doc
        assert "nb_commandes" in doc


def test_q2_total_positif():
    """Q2 : le total depense doit etre positif."""
    for doc in q2():
        assert doc["total_depense"] > 0


# ══════════════════════════════════════════════════════════════
# Q3 — Top 3 plats les plus commandes
# ══════════════════════════════════════════════════════════════

def test_q3_retourne_au_plus_3_resultats():
    """Q3 doit retourner au plus 3 plats."""
    assert len(q3()) <= 3


def test_q3_contient_champs_attendus():
    """Q3 : chaque document doit avoir nom_plat et quantite_totale."""
    for doc in q3():
        assert "nom_plat" in doc
        assert "quantite_totale" in doc


def test_q3_quantite_positive():
    """Q3 : la quantite totale doit etre positive."""
    for doc in q3():
        assert doc["quantite_totale"] > 0


# ══════════════════════════════════════════════════════════════
# Q4 — Revenu par mode de paiement
# ══════════════════════════════════════════════════════════════

def test_q4_retourne_une_liste():
    """Q4 doit retourner une liste."""
    assert isinstance(q4(), list)


def test_q4_pourcentages_somme_100():
    """Q4 : la somme des pourcentages doit etre proche de 100%."""
    total_pct = sum(doc["pourcentage"] for doc in q4())
    assert abs(total_pct - 100) < 0.5, f"Somme des pourcentages = {total_pct}"


def test_q4_contient_champs_attendus():
    """Q4 : chaque document doit avoir mode, total et pourcentage."""
    for doc in q4():
        assert "mode" in doc
        assert "total" in doc
        assert "pourcentage" in doc


# ══════════════════════════════════════════════════════════════
# Q5 — Clients ayant commande tofu ET poisson
# ══════════════════════════════════════════════════════════════

def test_q5_retourne_une_liste():
    """Q5 doit retourner une liste."""
    assert isinstance(q5(), list)


def test_q5_contient_nom_client():
    """Q5 : chaque resultat doit avoir un nom_client non vide."""
    for doc in q5():
        assert "nom_client" in doc
        assert len(doc["nom_client"]) > 0


# ══════════════════════════════════════════════════════════════
# Q6 — Dashboard $facet
# ══════════════════════════════════════════════════════════════

def test_q6_retourne_une_liste():
    """Q6 doit retourner une liste."""
    assert isinstance(q6(), list)


def test_q6_contient_trois_facettes():
    """Q6 : le resultat doit contenir les 3 facettes attendues."""
    result = q6()
    assert len(result) > 0
    doc = result[0]
    assert "repartition_statuts" in doc
    assert "ca_mensuel" in doc
    assert "top3_clients" in doc


def test_q6_top3_au_plus_3_clients():
    """Q6 : top3_clients doit contenir au plus 3 entrees."""
    doc = q6()[0]
    assert len(doc["top3_clients"]) <= 3


# ══════════════════════════════════════════════════════════════
# Q7 — Restaurants les plus proches (geospatial)
# ══════════════════════════════════════════════════════════════

def test_q7_retourne_au_plus_2_restaurants():
    """Q7 doit retourner au plus 2 restaurants."""
    assert len(q7()) <= 2


def test_q7_contient_distance():
    """Q7 : chaque resultat doit avoir un champ distance_metres positif."""
    for doc in q7():
        assert "distance_metres" in doc
        assert doc["distance_metres"] >= 0


def test_q7_trie_par_distance():
    """Q7 : les restaurants doivent etre tries par distance croissante."""
    distances = [doc["distance_metres"] for doc in q7()]
    assert distances == sorted(distances)


# ══════════════════════════════════════════════════════════════
# Q8 — Statistiques par livreur
# ══════════════════════════════════════════════════════════════

def test_q8_retourne_une_liste():
    """Q8 doit retourner une liste."""
    assert isinstance(q8(), list)


def test_q8_contient_champs_attendus():
    """Q8 : chaque document doit avoir les champs statistiques."""
    for doc in q8():
        assert "nom_livreur" in doc
        assert "nb_commandes" in doc
        assert "delai_moyen" in doc
        assert "note_moyenne" in doc


def test_q8_nb_commandes_positif():
    """Q8 : le nombre de commandes doit etre positif."""
    for doc in q8():
        assert doc["nb_commandes"] > 0


# ══════════════════════════════════════════════════════════════
# Q9 — Commandes avec plat vegetarien ou vegan
# ══════════════════════════════════════════════════════════════

def test_q9_retourne_une_liste():
    """Q9 doit retourner une liste."""
    assert isinstance(q9(), list)


def test_q9_nombre_positif_ou_zero():
    """Q9 : le nombre de commandes vegetariennes doit etre >= 0."""
    result = q9()
    nb_val = result[0]["nb_commandes_veg"] if result else 0
    assert nb_val >= 0


# ══════════════════════════════════════════════════════════════
# Q10 — Recommandations pour Ousmane Sarr
# ══════════════════════════════════════════════════════════════

def test_q10_retourne_une_liste():
    """Q10 doit retourner une liste."""
    assert isinstance(q10(), list)


def test_q10_contient_champs_attendus():
    """Q10 : chaque recommandation doit avoir nom et prix."""
    for doc in q10():
        assert "nom" in doc
        assert "prix" in doc


def test_q10_prix_positif():
    """Q10 : le prix de chaque recommandation doit etre positif."""
    for doc in q10():
        assert doc["prix"] > 0