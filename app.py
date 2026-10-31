import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

BASE = Path(__file__).resolve().parent

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-only-change-this'), DATABASE=str(BASE / 'soprogest.db'))
    if test_config:
        app.config.update(test_config)

    def connect():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        return db

    def init_db():
        with connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS animais (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, especie TEXT NOT NULL, idade INTEGER NOT NULL CHECK(idade >= 0), saude TEXT NOT NULL, status TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL UNIQUE, senha_hash TEXT NOT NULL)')
            if not db.execute('SELECT id FROM usuarios LIMIT 1').fetchone():
                db.execute('INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)', ('admin', generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'TroqueEstaSenha123!'))))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            with connect() as db:
                user = db.execute('SELECT * FROM usuarios WHERE usuario = ?', (request.form.get('usuario', ''),)).fetchone()
            if user and check_password_hash(user['senha_hash'], request.form.get('senha', '')):
                session.clear()
                session['usuario'] = user['usuario']
                return redirect(url_for('animais'))
            flash('Usuário ou senha inválidos.', 'erro')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    @app.route('/animais')
    def animais():
        if 'usuario' not in session:
            return redirect(url_for('login'))
        with connect() as db:
            rows = db.execute('SELECT * FROM animais ORDER BY id DESC').fetchall()
        return render_template('animais.html', animais=rows)

    @app.route('/animais/novo', methods=['GET', 'POST'])
    def novo_animal():
        if 'usuario' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            especie = request.form.get('especie', '').strip()
            saude = request.form.get('saude', '').strip()
            status = request.form.get('status', '').strip()
            try:
                idade = int(request.form.get('idade', ''))
            except ValueError:
                idade = -1
            if not nome or especie not in ('Cão', 'Gato', 'Outro') or idade < 0 or not saude or status not in ('Disponível', 'Em tratamento', 'Adotado'):
                flash('Confira os dados obrigatórios do animal.', 'erro')
            else:
                with connect() as db:
                    db.execute('INSERT INTO animais (nome, especie, idade, saude, status) VALUES (?, ?, ?, ?, ?)', (nome, especie, idade, saude, status))
                flash('Animal cadastrado com sucesso!', 'sucesso')
                return redirect(url_for('animais'))
        return render_template('novo.html')

    with app.app_context():
        init_db()
    return app

if __name__ == '__main__':
    create_app().run(debug=False)
