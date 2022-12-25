import psycopg2
from psycopg2 import errors
from flask import render_template, request, session, redirect, url_for
from flask import flash
from . import app


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    entered_password = request.form.get('password')

    user = None
    is_password_right = None

    if request.method == 'POST':
        if login and entered_password:
            conn = psycopg2.connect(database='training_diary',
                                    user='postgres', password='1234',
                                    host='localhost', port=5432)

            with conn:
                with conn.cursor() as cur:
                    cur.execute(f'''SELECT * FROM users WHERE user_login = '{login}' ''')
                    user = cur.fetchone()

                    if user is None:
                        flash('Такого пользователя не существует')
                        return redirect(url_for('login_page'))

                    cur.execute(f'''SELECT user_password = crypt('{entered_password}', user_password)
                                        FROM users WHERE user_login = '{login}' ''')
                    is_password_right = cur.fetchone()[0]

            if is_password_right:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''UPDATE users SET is_authenticated = true
                                            WHERE user_login = '{login}' ''')
                        cur.execute(f'''SELECT * FROM users WHERE user_login = '{login}' ''')
                        user = cur.fetchone()
                        session['current_user'] = user
                        session['user_password'] = entered_password

                return redirect(url_for('index'))
            else:
                flash('Пожалуйста, введите корректные данные')
                return redirect(url_for('login_page'))
        else:
            flash('Пожалуйста, заполните все поля')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    surname = request.form.get('surname')
    name = request.form.get('name')
    middle_name = request.form.get('middle_name')
    age = request.form.get('age')
    exp = request.form.get('exp')
    email = request.form.get('email')
    role = request.form.get('role')

    values = [login, password, password2, surname, name, middle_name, age,
              exp, email, role]

    if request.method == 'POST':
        if not all(values):
            flash('Пожалуйста, заполните все данные')
            return redirect(url_for('register_page'))

        if (int(age) < 10):
            flash('Возраст не подходит')
            return redirect(url_for('register_page'))

        if (int(exp) < 0):
            flash('Стаж отрицательный')
            return redirect(url_for('register_page'))

        if (int(age) - int(exp) < 10):
            flash('Возраст и стаж неверно')
            return redirect(url_for('register_page'))

        elif password != password2:
            flash('Введенные пароли не равны')
            return redirect(url_for('register_page'))
        else:
            conn = psycopg2.connect(database='training_diary',
                                    user='postgres', password='1234',
                                    host='localhost', port=5432)
            with conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute(f'''CALL create_user('{name}', '{middle_name}', '{surname}', '{exp}',
                                                                '{age}', '{email}', '{role}', '{login}', '{password}')''')
                    except errors.RaiseException:
                        flash('Такой пользователь уже существует')
                        return redirect(url_for('register_page'))

            return redirect(url_for('login_page'))
    else:
        return render_template('auth/register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    login = session.get('current_user', app.secret_key)[1]
    conn = psycopg2.connect(database='training_diary',
                            user='postgres', password='1234',
                            host='localhost', port=5432)
    with conn:
        with conn.cursor() as cur:
            cur.execute(f'''UPDATE users SET is_authenticated = false
                                           WHERE user_login = '{login}' ''')

    session.clear()
    return redirect(url_for('index'))
