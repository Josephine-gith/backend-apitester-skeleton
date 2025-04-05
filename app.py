import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / "data"

# Charger les données CSV
associations_df = pd.read_csv(data / "associations_etudiantes.csv")
evenements_df = pd.read_csv(data / "evenements_associations.csv")


## Vous devez ajouter les routes ici :
@app.route("/api/alive", methods=["GET"])
def alive():
    return jsonify({"message": "Alive"}), 200


@app.route("/api/associations", methods=["GET"])
def associations():
    return associations_df["id"].to_list(), 200


@app.route("/api/association/<int:id>", methods=["GET"])
def details_association(id):
    if id in associations_df["id"].values:
        return associations_df[["nom", "type", "description"]][
            associations_df["id"] == id
        ].to_dict(), 200
    else:
        return jsonify({"error": "Association not found"}), 404


@app.route("/api/evenements", methods=["GET"])
def evenements():
    return evenements_df["id"].to_list(), 200


@app.route("/api/evenement/<int:id>", methods=["GET"])
def details_evenement(id):
    if id in evenements_df["id"].values:
        return evenements_df[["nom", "date", "lieu", "description"]][
            evenements_df["id"] == id
        ].to_dict(), 200
    else:
        return jsonify({"error": "Event not found"}), 404


@app.route("/api/association/<int:id>/evenements", methods=["GET"])
def evenements_par_asso(id):
    return evenements_df[["nom", "date", "lieu", "description"]][
        evenements_df["association_id"] == id
    ].to_dict(), 200


@app.route("/api/associations/type/<type>", methods=["GET"])
def associations_par_type(type):
    return associations_df[["nom", "description"]][
        associations_df["type"] == type
    ].to_dict(), 200


if __name__ == "__main__":
    app.run(debug=False)
