from flask import Flask, render_template, request, redirect
from create_db import db, create_database, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Подключение к базе данных
db.init_app(app)

# Создание базы данных, если она еще не существует
with app.app_context():
    create_database()  # Вызываем функцию без передачи аргумента

# Модель пользователя уже определена в create_db.py, поэтому ее не нужно определять здесь.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
