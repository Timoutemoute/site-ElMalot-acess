from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Chemin vers le fichier JSON
DATA_FILE = os.path.join('data', 'properties.json')

# Charger les propriétés depuis le fichier JSON
def load_properties():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Sauvegarder les propriétés dans le fichier JSON
def save_properties(properties):
    with open(DATA_FILE, 'w') as file:
        json.dump(properties, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    properties = load_properties()
    return jsonify(properties)

@app.route('/api/properties', methods=['POST'])
def add_property():
    new_property = request.json
    properties = load_properties()
    properties.append(new_property)
    save_properties(properties)
    return jsonify(new_property), 201

if __name__ == '__main__':
    app.run(debug=True)