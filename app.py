from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # поменяй на свой секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caseblitz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    balance = db.Column(db.Integer, default=0)
    drops = db.relationship('Drop', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Drop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', user=user)
    return render_template('index.html', user=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Имя уже занято')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Войдите в аккаунт.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Вы успешно вошли')
            return redirect(url_for('index'))
        flash('Неверные данные')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('index'))

@app.route('/topup', methods=['POST'])
def topup():
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизованы'}), 401
    amount = int(request.json.get('amount', 0))
    if amount <= 0:
        return jsonify({'error': 'Некорректная сумма'}), 400
    user = User.query.get(session['user_id'])
    user.balance += amount
    db.session.commit()
    return jsonify({'balance': user.balance})

@app.route('/open_case', methods=['POST'])
def open_case():
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизованы'}), 401

    case_price = int(request.json.get('price', 0))
    case_type = request.json.get('type', '')

    user = User.query.get(session['user_id'])
    if user.balance < case_price:
        return jsonify({'error': 'Недостаточно средств'}), 400

    drops = {
        'starter': [
            ('🔫 Pistol', 50, 50),
            ('🔪 Knife', 30, 150),
            ('💎 Rare Gem', 15, 300),
            ('👑 Legend', 5, 1000)
        ],
        'epic': [
            ('💣 Epic Bomb', 50, 200),
            ('🧤 Gloves', 30, 400),
            ('💎 Crystal', 15, 700),
            ('👑 Godlike', 5, 1500)
        ],
        'legendary': [
            ('🔮 Orb', 50, 400),
            ('💎 Sapphire', 30, 900),
            ('👑 Ancient Relic', 15, 1600),
            ('🔥 Dragon Lore', 5, 3000)
        ],
        'ultra': [
            ('🚀 Rocket', 50, 800),
            ('🛡 Titan Shield', 30, 1500),
            ('👑 Divine Crown', 15, 2500),
            ('🌌 Galaxy Core', 5, 5000)
        ],
    }
    roll = random.uniform(0, 100)
    cumulative = 0
    won_item = None
    for name, chance, price in drops.get(case_type, []):
        cumulative += chance
        if roll <= cumulative:
            won_item = (name, price)
            break

    if not won_item:
        return jsonify({'error': 'Ошибка выпадения предмета'}), 500

    user.balance -= case_price
    drop = Drop(item_name=won_item[0], price=won_item[1], user_id=user.id)
    db.session.add(drop)
    db.session.commit()

    return jsonify({'drop': won_item[0], 'price': won_item[1], 'balance': user.balance})

@app.route('/sell_drop', methods=['POST'])
def sell_drop():
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизованы'}), 401
    drop_id = request.json.get('drop_id')
    drop = Drop.query.filter_by(id=drop_id, user_id=session['user_id']).first()
    if not drop:
        return jsonify({'error': 'Предмет не найден'}), 404

    user = User.query.get(session['user_id'])
    user.balance += drop.price
    db.session.delete(drop)
    db.session.commit()

    return jsonify({'balance': user.balance})

NOWPAYMENTS_API_KEY = os.getenv('NOWPAYMENTS_API_KEY')
NOWPAYMENTS_API_URL = 'https://api.nowpayments.io/v1/invoice'

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизованы'}), 401
    amount = float(request.json.get('amount', 0))
    if amount <= 0:
        return jsonify({'error': 'Некорректная сумма'}), 400

    headers = {
        'x-api-key': NOWPAYMENTS_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'price_amount': amount,
        'price_currency': 'rub',
        'pay_currency': 'rub',
        'order_id': f'user_{session["user_id"]}_{int(random.random()*100000)}',
        'ipn_callback_url': url_for('payment_callback', _external=True),
        'success_url': url_for('index', _external=True),
        'cancel_url': url_for('index', _external=True),
    }
    r = requests.post(NOWPAYMENTS_API_URL, json=data, headers=headers)
    if r.status_code != 200:
        return jsonify({'error': 'Ошибка создания счета'}), 500
    return jsonify(r.json())

@app.route('/payment_callback', methods=['POST'])
def payment_callback():
    # Здесь нужно обрабатывать уведомления NOWPayments о статусе оплаты
    # и зачислять баланс пользователю, например:
    data = request.json
    # TODO: проверить подпись, проверить статус
    # Найти пользователя по order_id и обновить баланс
    return 'OK', 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
