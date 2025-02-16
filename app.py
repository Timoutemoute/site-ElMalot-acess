from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Clé secrète pour gérer les sessions

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

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('immobilier.db')
    conn.row_factory = sqlite3.Row
    return conn

# Vérifier si l'utilisateur est connecté en tant qu'admin
def is_admin():
    return session.get('role') == 'admin'

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page de connexion admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and user['password'] == password:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('admin_dashboard'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 401
    return render_template('admin_login.html')

# Tableau de bord admin
@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('admin_login'))
    properties = load_properties()
    return render_template('admin_dashboard.html', properties=properties)

# Ajouter une propriété
@app.route('/admin/add_property', methods=['POST'])
def add_property():
    if not is_admin():
        return redirect(url_for('admin_login'))
    new_property = {
        'id': len(load_properties()) + 1,
        'title': request.form['title'],
        'description': request.form['description'],
        'price': float(request.form['price'])
    }
    properties = load_properties()
    properties.append(new_property)
    save_properties(properties)
    return redirect(url_for('admin_dashboard'))

# Supprimer une propriété
@app.route('/admin/delete_property/<int:property_id>', methods=['POST'])
def delete_property(property_id):
    if not is_admin():
        return redirect(url_for('admin_login'))
    properties = load_properties()
    properties = [p for p in properties if p['id'] != property_id]
    save_properties(properties)
    return redirect(url_for('admin_dashboard'))

# Créer un nouvel utilisateur admin
@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if not is_admin():
        return redirect(url_for('admin_login'))
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                 (username, password, 'admin'))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

# Déconnexion admin
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)