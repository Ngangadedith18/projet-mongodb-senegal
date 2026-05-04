"""
app.py — Serveur Flask exposant les 10 requêtes MongoDB via une API REST.
Projet : Analyse de données de restauration sénégalaise.
"""

from flask import Flask, render_template, jsonify
from bson import json_util
from db import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10

app = Flask(__name__)


@app.route('/')
def index():
    """Affiche la page principale de l'application."""
    return render_template('index.html')


@app.route('/api/q1')
def route_q1():
    """Retourne les restaurants de Dakar avec leurs plats, triés par note décroissante."""
    return jsonify(q1())


@app.route('/api/q2')
def route_q2():
    """Retourne le total dépensé par client sur les commandes livrées."""
    return jsonify(q2())


@app.route('/api/q3')
def route_q3():
    """Retourne le top 3 des plats les plus commandés."""
    return jsonify(q3())


@app.route('/api/q4')
def route_q4():
    """Retourne le revenu par mode de paiement avec pourcentage du CA."""
    return jsonify(q4())


@app.route('/api/q5')
def route_q5():
    """Retourne les clients ayant commandé un plat avec tofu ET un plat avec poisson."""
    return jsonify(q5())


@app.route('/api/q6')
def route_q6():
    """Retourne le dashboard $facet : statuts, CA mensuel et top 3 clients fidèles."""
    return app.response_class(
        response=json_util.dumps(q6()),
        mimetype='application/json'
    )


@app.route('/api/q7')
def route_q7():
    """Retourne les 2 restaurants les plus proches d'Ousmane Sarr."""
    return jsonify(q7())


@app.route('/api/q8')
def route_q8():
    """Retourne les statistiques par livreur sur les commandes livrées."""
    return jsonify(q8())


@app.route('/api/q9')
def route_q9():
    """Retourne le nombre de commandes contenant au moins un plat végétarien ou vegan."""
    return jsonify(q9())


@app.route('/api/q10')
def route_q10():
    """Retourne les recommandations de plats pour Ousmane Sarr."""
    return jsonify(q10())


if __name__ == '__main__':
    app.run(debug=True)
