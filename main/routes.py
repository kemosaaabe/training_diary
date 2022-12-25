import psycopg2
import requests
from flask import render_template, session, redirect, url_for
from flask import request, flash
from datetime import datetime
from random import randint, shuffle

from . import app


@app.route('/')
def index():
    user = {'is_authenticated': False}
    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]

    conn = psycopg2.connect(database='training_diary',
                            user='postgres', password='1234',
                            host='localhost', port=5432)

    articles = None
    article_types = None

    with conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM articles')
            articles = [[item[0], item[1], item[2], item[3], item[4], item[5]] for item in cur.fetchall()]

            cur.execute('SELECT * FROM article_types')
            article_types = [item[1] for item in cur.fetchall()]

    for article in articles:
        article[5] = article_types[article[5] - 1]

    return render_template('index.html', articles=articles, user=user)


@app.route('/user_account/<int:user_id>')
def show_user_acc(user_id):
    user = {'is_authenticated': False}
    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]

        person_types = None
        person_id = session.get('current_user', app.secret_key)[4]
        user['person_id'] = person_id

        conn = psycopg2.connect(database='training_diary',
                                user=f'''{session.get('current_user', app.secret_key)[1]}''',
                                password=f'''{session.get('user_password', app.secret_key)}''',
                                host='localhost', port=5432)

        with conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM persons_info WHERE person_id = {person_id}')
                user['info'] = list(cur.fetchone())

                if user['info'][7] == 1:
                    cur.execute(f'''SELECT * FROM persons_info WHERE person_id = (
                                    SELECT trainer FROM beginners WHERE person_id = {person_id})''')
                    user['trainer'] = cur.fetchone()

                    print(user['trainer'])

                cur.execute(f'SELECT * FROM person_types')
                person_types = [item[1] for item in cur.fetchall()]

                user['info'][7] = person_types[user['info'][7] - 1]

        return render_template('user_account.html', user=user)
    else:
        return redirect(url_for('index'))


@app.route('/article/<int:article_id>')
def show_article(article_id):
    user = {'is_authenticated': False}
    article = None

    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        user['person_id'] = session.get('current_user', app.secret_key)[4]

    conn = psycopg2.connect(database='training_diary',
                            user='postgres', password='1234',
                            host='localhost', port=5432)

    with conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT * FROM articles WHERE article_id = {article_id}')
            article = list(cur.fetchone())

            cur.execute(f'SELECT * FROM persons_info WHERE person_id = {article[4]}')
            author = list(cur.fetchone())

            user['author'] = article[4]

            article[4] = author[1] + ' ' + author[3]

    return render_template('articles/article.html', user=user, article=article, author=author)


@app.route('/my_articles')
def show_author_articles():
    user = {'is_authenticated': False}
    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        conn = psycopg2.connect(database='training_diary',
                                user=f'{username}', password=f'{user_pass}',
                                host='localhost', port=5432)

        articles = None
        article_types = None

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM articles')
                articles = [[item[0], item[1], item[2], item[3], item[4], item[5]] for item in cur.fetchall()]

                cur.execute('SELECT * FROM article_types')
                article_types = [item[1] for item in cur.fetchall()]

        for article in articles:
            article[5] = article_types[article[5] - 1]

        return render_template('articles/my_articles.html', articles=articles, user=user)

    else:
        return redirect(url_for('index'))


@app.route('/change_article/<int:article_id>', methods=['GET', 'POST'])
def change_article(article_id):
    user = {'is_authenticated': False}
    article = None

    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        user['person_id'] = session.get('current_user', app.secret_key)[4]

        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        conn = psycopg2.connect(database='training_diary',
                                user=f'{username}', password=f'{user_pass}',
                                host='localhost', port=5432)

        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f'''UPDATE articles SET article_name='{title}', article_description='{description}'
                                    WHERE article_id = {article_id}''')

            return redirect(url_for('show_article', article_id=article_id))

        else:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f'SELECT * FROM articles WHERE article_id = {article_id}')
                    try:
                        article = list(cur.fetchone())
                    except TypeError:
                        return redirect(url_for('index'))

                    cur.execute(f'SELECT * FROM persons_info WHERE person_id = {article[4]}')
                    author = list(cur.fetchone())

                    user['author'] = article[4]

                    article[4] = author[1] + ' ' + author[3]

            return render_template('articles/change_article.html', user=user, article=article)

    else:
        return redirect(url_for('index'))


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    user = {'is_authenticated': False}

    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]

        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        conn = psycopg2.connect(database='training_diary',
                                user=f'{username}', password=f'{user_pass}',
                                host='localhost', port=5432)

        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            article_type = request.form.get('article-type')

            if description == '' or title == '':
                flash('Пожалуйста, заполните все поля')
                return render_template('articles/add_article.html', user=user)

            with conn:
                with conn.cursor() as cur:
                    cur.execute(f'''CALL create_article('{title}', '{description}', {article_type})''')

            return redirect(url_for('show_author_articles'))

        else:
            return render_template('articles/add_article.html', user=user)

    else:
        return redirect(url_for('index'))


@app.route('/delete_article/<int:article_id>')
def delete_article(article_id):
    user = {'is_authenticated': False}
    article = None

    if 'current_user' in session:
        user['is_authenticated'] = True
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        user['person_id'] = session.get('current_user', app.secret_key)[4]

        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        conn = psycopg2.connect(database='training_diary',
                                user=f'{username}', password=f'{user_pass}',
                                host='localhost', port=5432)
        with conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM articles WHERE article_id={article_id}')

        return redirect(url_for('show_author_articles'))

    else:
        return redirect(url_for('index'))


@app.route('/trainers')
def show_trainers():
    user = {'is_authenticated': False}

    if 'current_user' in session:
        trainers = []
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        user['is_authenticated'] = True

        conn = psycopg2.connect(database='training_diary',
                                user='postgres', password='1234',
                                host='localhost', port=5432)

        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM trainers_view')
                trainers = cur.fetchall()
                print(trainers)

        return render_template('trainers/trainers.html', user=user, trainers=trainers)

    else:
        return redirect(url_for('index'))


@app.route('/trainer/<int:trainer_id>', methods=['GET', 'POST'])
def show_trainer(trainer_id):
    user = {'is_authenticated': False}

    if 'current_user' in session:
        user['user_id'] = session.get('current_user', app.secret_key)[0]
        user_id = session.get('current_user', app.secret_key)[0]
        user['is_authenticated'] = True
        person_id = session.get('current_user', app.secret_key)[4]
        trainer = []

        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        if request.method == 'POST':
            post_conn = psycopg2.connect(database='training_diary',
                                         user='postgres', password='1234',
                                         host='localhost', port=5432)

            with post_conn:
                with post_conn.cursor() as cur:
                    cur.execute(f'CALL choose_trainer({user_id}, {trainer_id})')

            return redirect(url_for('show_user_acc', user_id=user_id))

        else:
            conn = psycopg2.connect(database='training_diary',
                                    user=f'{username}', password=f'{user_pass}',
                                    host='localhost', port=5432)

            with conn:
                with conn.cursor() as cur:
                    cur.execute(f'SELECT * FROM persons_info WHERE person_id = {person_id}')
                    user['info'] = list(cur.fetchone())

                    cur.execute(f'SELECT * FROM persons_info WHERE person_id={trainer_id}')
                    trainer = cur.fetchone()
                    print(trainer)

            return render_template('trainers/trainer_info.html', user=user, trainer=trainer)
    else:
        return redirect(url_for('index'))


@app.route('/notes/<int:user_id>', methods=['GET', 'POST'])
def show_my_notes(user_id):
    user = {'is_authenticated': False}

    if 'current_user' in session:
        current_user_id = session.get('current_user', app.secret_key)[0]
        user['user_id'] = current_user_id
        user['is_authenticated'] = True
        person_id = session.get('current_user', app.secret_key)[4]

        username = session.get('current_user', app.secret_key)[1]
        user_pass = session.get('user_password', app.secret_key)

        conn = psycopg2.connect(database='training_diary',
                                user=f'{username}', password=f'{user_pass}',
                                host='localhost', port=5432)

        folders = None
        notes = None

        with conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM persons_info WHERE person_id={person_id}')
                user['info'] = cur.fetchone()

                cur.execute(f'SELECT * FROM folders')
                folders = [[item[0], item[1], item[2], item[3]] for item in cur.fetchall()]

                cur.execute('SELECT * FROM persons_info')
                authors = [item[1] + ' ' + item[3] for item in cur.fetchall()]

                for folder in folders:
                    folder[3] = authors[folder[3] - 1]

                cur.execute(f'SELECT * FROM notes ORDER BY creation_date DESC')
                notes = [[item[0], item[1], item[2], item[3],
                          item[4], item[5]] for item in cur.fetchall()]

                for note in notes:
                    note[4] = authors[note[4] - 1]

        if request.method == "POST":
            folder_id = request.form.get('folder_id')
            note_id = request.form.get('note_id')
            edit_note_id = request.form.get('editNoteId')
            delete_note_id = request.form.get('deleteNoteId')
            new_note_in_folder_id = request.form.get('addNewNoteId')

            add_new_folder_id = request.form.get('addNewFolder')
            delete_folder_id = request.form.get('deleteFolderId')
            edit_folder_id = request.form.get('editFolder')

            basket = request.form.get('basket')
            restore_id = request.form.get('restoreId')
            destroy_id = request.form.get('destroyId')

            if folder_id:
                new_notes = None
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'SELECT * FROM notes WHERE folder_id={folder_id}')
                        new_notes = [[item[0], item[1], item[2], item[3],
                                      item[4], item[5]] for item in cur.fetchall()]

                        cur.execute('SELECT * FROM persons_info')
                        authors = [item[1] + ' ' + item[3] for item in cur.fetchall()]

                        for note in new_notes:
                            note[4] = authors[note[4] - 1]
                        print(new_notes)

                return new_notes

            elif note_id:
                note = None
                folder_id = request.form.get('folderOfNote')
                with conn:
                    with conn.cursor() as cur:
                        if folder_id == 'null':
                            cur.execute(f'SELECT * FROM deleted_notes WHERE deleted_note_id={note_id}')
                            note = cur.fetchall()
                        else:
                            cur.execute(f'SELECT * FROM notes WHERE note_id={note_id}')
                            note = cur.fetchall()
                return note

            elif edit_note_id:
                note_title = request.form.get('editNoteTitle')
                note_description = request.form.get('editNoteDesc')
                current_date = datetime.now()

                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''UPDATE notes SET note_name='{note_title}',
                                        note_description='{note_description}',
                                        creation_date='{current_date}'
                                        WHERE note_id={edit_note_id}''')

            elif delete_note_id:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'DELETE FROM notes WHERE note_id={delete_note_id}')

            elif new_note_in_folder_id:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''CALL create_note('Новая заметка', '', {new_note_in_folder_id})''')

            elif add_new_folder_id:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''CALL create_folder('Новая папка')''')

            elif delete_folder_id:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''DELETE FROM folders WHERE folder_id={delete_folder_id}''')

            elif edit_folder_id:
                folder_name = request.form.get('newFolderName')
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''UPDATE folders SET folder_name='{folder_name}' 
                                        WHERE folder_id={edit_folder_id}''')

            elif basket:
                notes = None
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''SELECT * FROM deleted_notes''')
                        notes = [[item[0], item[1], item[2], item[3], item[4],
                                  item[5], item[6]] for item in cur.fetchall()]

                        cur.execute('SELECT * FROM persons_info')
                        authors = [item[1] + ' ' + item[3] for item in cur.fetchall()]

                        for note in notes:
                            note[4] = authors[note[4] - 1]

                return notes

            elif restore_id:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(f'''DELETE FROM deleted_notes WHERE deleted_note_id={restore_id}''')

            elif destroy_id:
                admin_conn = psycopg2.connect(database='training_diary',
                                              user='postgres', password='1234',
                                              host='localhost', port=5432)

                with admin_conn:
                    with admin_conn.cursor() as cur:
                        cur.execute(f'''BEGIN;
                                        ALTER TABLE deleted_notes
                                        DISABLE TRIGGER on_recover_from_trash;
                                        DELETE FROM deleted_notes WHERE deleted_note_id={destroy_id};
                                        ALTER TABLE deleted_notes
                                        ENABLE TRIGGER on_recover_from_trash;
                                        COMMIT;''')

        return render_template('notes/notes.html', user=user, notes=notes, folders=folders)

    else:
        return redirect(url_for('index'))


# @app.route('/generate')
# def generate_values():
#     folder_names_lst = ['Тренировки', 'Дневник', 'Рецепты', 'Привычки', 'Цели', 'Планы',
#                         'Финансы', 'Хронометраж', 'Книги', 'Фильмы', 'Просто папка', 'БД',
#                         'Тудуист', 'Питон', 'JS']
#
#     shuffle(folder_names_lst)
#     random_folder_names = []
#     n = 9
#     for i in range(0, n):
#         value = folder_names_lst[i]
#         random_folder_names.append(value)
#
#     admin_conn = psycopg2.connect(database='training_diary',
#                                   user='postgres', password='1234',
#                                   host='localhost', port=5432)
    # with admin_conn:
    #     with admin_conn.cursor() as cur:
    #         for j in range(1, 7):
    #             for i in range(0, 9):
    #                 current_date = datetime.now()
    #                 cur.execute(f'''INSERT INTO folders(folder_name, creation_date, author_id) VALUES
    #                                 ('{random_folder_names[i]}', '{current_date}', {j})''')

    # with admin_conn:
    #     with admin_conn.cursor() as cur:
    #         for j in range (15, 24):
    #             titles = requests.get('https://fish-text.ru/get?format=json&type=title&number=15')
    #             note_names_lst = titles.json()['text'].split('\\n\\n')
    #
    #             descriptions = requests.get('https://fish-text.ru/get?format=json&type=paragraph&number=15')
    #             descriptions_lst = descriptions.json()['text'].split('\\n\\n')
    #
    #             for i in range(0, 15):
    #                 current_date = datetime.now()
    #                 cur.execute(f'''INSERT INTO notes(note_name, note_description, creation_date,
    #                                 author_id, folder_id) VALUES
    #                                 ('{note_names_lst[i][:49]}',
    #                                  '{descriptions_lst[i]}',
    #                                  '{current_date}',
    #                                  2,
    #                                  {j})''')
    #
    # return "<h1>харош</h1>"
