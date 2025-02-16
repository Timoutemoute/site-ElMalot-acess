from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import json
import os
import sqlite3
from functools import wraps

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

# Décorateur pour vérifier si l'utilisateur est admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('role') == 'admin':
            flash("Accès refusé. Veuillez vous connecter en tant qu'admin.", "error")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Page d'accueil
@app.route('/')
def index():
    properties = load_properties()
    return render_template('index.html', properties=properties)

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
            flash("Connexion réussie !", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")
    return render_template('admin_login.html')

# Tableau de bord admin
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    properties = load_properties()
    return render_template('admin_dashboard.html', properties=properties)

# Ajouter une propriété
@app.route('/admin/add_property', methods=['POST'])
@admin_required
def add_property():
    new_property = {
        'id': len(load_properties()) + 1,
        'title': request.form['title'],
        'description': request.form['description'],
        'price': float(request.form['price'])
    }
    properties = load_properties()
    properties.append(new_property)
    save_properties(properties)
    flash("Propriété ajoutée avec succès !", "success")
    return redirect(url_for('admin_dashboard'))

# Modifier une propriété
@app.route('/admin/edit_property/<int:property_id>', methods=['GET', 'POST'])
@admin_required
def edit_property(property_id):
    properties = load_properties()
    property_to_edit = next((p for p in properties if p['id'] == property_id), None)
    if not property_to_edit:
        flash("Propriété non trouvée", "error")
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        property_to_edit['title'] = request.form['title']
        property_to_edit['description'] = request.form['description']
        property_to_edit['price'] = float(request.form['price'])
        save_properties(properties)
        flash("Propriété modifiée avec succès !", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_property.html', property=property_to_edit)

# Supprimer une propriété
@app.route('/admin/delete_property/<int:property_id>', methods=['POST'])
@admin_required
def delete_property(property_id):
    properties = load_properties()
    properties = [p for p in properties if p['id'] != property_id]
    save_properties(properties)
    flash("Propriété supprimée avec succès !", "success")
    return redirect(url_for('admin_dashboard'))

# Gestion des utilisateurs
@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('admin_users.html', users=users)

# Créer un nouvel utilisateur admin
@app.route('/admin/create_user', methods=['POST'])
@admin_required
def create_user():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                 (username, password, 'admin'))
    conn.commit()
    conn.close()
    flash("Utilisateur créé avec succès !", "success")
    return redirect(url_for('admin_users'))

# Déconnexion admin
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash("Déconnexion réussie !", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)