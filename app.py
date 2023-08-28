from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# Configuration MongoDB
client = MongoClient('mongodb://root:example@localhost:27017/')
db = client.eleves


# Route pour la page d'accueil (liste des élèves)


@app.route('/')
def index():
    eleves = db.eleves.find()
    return render_template('index.html', eleves=eleves)

# Route pour la page d'ajout d'élève


@app.route('/ajouter_eleve', methods=['GET', 'POST'])
def ajouter_eleve():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')

        # Ajouter l'élève à la collection MongoDB
        db.eleves.insert_one({'nom': nom, 'prenom': prenom})

        # Rediriger vers la liste des élèves après l'ajout
        return redirect(url_for('index'))

    return render_template('add_eleve.html')


# Chargement des données depuis le fichier JSON
def load_data_from_json(json_filename):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
    return data

# Route pour insérer les données depuis le fichier JSON


@app.route('/inserer_donnees', methods=['GET'])
def inserer_donnees():
    # Remplacez le nom de fichier par le vôtre
    data = load_data_from_json('exercice_flask/mongol_yann/data.json')
    db.eleves.insert_many(data)
    return jsonify(message="Données insérées avec succès")


if __name__ == '__main__':
    app.run(debug=True)
