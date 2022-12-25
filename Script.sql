CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS folders CASCADE;
DROP TABLE IF EXISTS notes CASCADE;
DROP TABLE IF EXISTS deleted_notes CASCADE;
DROP TABLE IF EXISTS persons_info CASCADE;
DROP TABLE IF EXISTS beginners CASCADE;
DROP TABLE IF EXISTS person_types CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS article_types CASCADE;

CREATE TABLE person_types (
	person_type_id SERIAL PRIMARY KEY,
	person_type_name VARCHAR(30)
);

CREATE TABLE persons_info (
	person_id SERIAL PRIMARY KEY,
	person_name VARCHAR(50) NOT NULL,
	person_middle_name VARCHAR(50),
	person_surname VARCHAR(50) NOT NULL,
	train_experience SMALLINT NOT NULL,
	person_age SMALLINT NOT NULL,
	person_email VARCHAR(80) NOT NULL,
	person_type SERIAL NOT NULL REFERENCES person_types (person_type_id) 
);

CREATE TABLE beginners (
	beginner_id SERIAL PRIMARY KEY,
	person_id SERIAL NOT NULL REFERENCES persons_info (person_id),
	trainer INTEGER REFERENCES persons_info (person_id)
);

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	user_login VARCHAR(50) NOT NULL,
	user_password VARCHAR(50) NOT NULL,
	is_authenticated BOOLEAN NOT NULL,
	person_id SERIAL NOT NULL REFERENCES persons_info (person_id)
);

CREATE TABLE folders (
	folder_id SERIAL PRIMARY KEY,
	folder_name VARCHAR(50) NOT NULL,
	creation_date TIMESTAMP NOT NULL,
	author_id SERIAL NOT NULL REFERENCES persons_info (person_id)
);

CREATE TABLE notes (
	note_id SERIAL PRIMARY KEY,
	note_name VARCHAR(50) NOT NULL,
	note_description VARCHAR,
	creation_date TIMESTAMP NOT NULL,
	author_id SERIAL NOT NULL REFERENCES persons_info (person_id),
	folder_id INTEGER REFERENCES folders (folder_id) ON DELETE CASCADE
); 

CREATE TABLE deleted_notes (
	deleted_note_id SERIAL PRIMARY KEY,
	note_name VARCHAR(50) NOT NULL,
	note_description VARCHAR,
	creation_date TIMESTAMP NOT NULL,
	author_id SERIAL NOT NULL REFERENCES persons_info (person_id),
	folder_id INTEGER REFERENCES folders (folder_id) ON DELETE CASCADE,
	deletion_date TIMESTAMP NOT NULL
);

CREATE TABLE article_types (
	article_type_id SERIAL PRIMARY KEY,
	article_type_name VARCHAR(50),
	article_type_description VARCHAR NOT NULL
);

CREATE TABLE articles (
	article_id SERIAL PRIMARY KEY,
	article_name VARCHAR(50) NOT NULL,
	article_description VARCHAR NOT NULL,
	creation_date DATE NOT NULL,
	author_id SERIAL NOT NULL REFERENCES persons_info (person_id),
	article_type SERIAL NOT NULL REFERENCES article_types (article_type_id)
);

INSERT INTO person_types(person_type_name) VALUES
	('Новичок'),
	('Тренер');

INSERT INTO persons_info(person_name, person_middle_name, person_surname, 
					train_experience, person_age, person_email, person_type) VALUES 
	('Данил', 'Даниилович', 'Земляков', 1, 20, 'zemlya@mail.ru', 1),
	('Саня', 'Михалыч', 'Шварценегер', 5, 20, 'sanya@mail.ru', 2),
	('Андрей', 'Сергеевич', 'Успенский', 38, 48, 'trener@mail.ru', 2),
	('Комар', 'Даниилович', 'Комариков', 1, 20, 'komarik@mail.ru', 1),
	('Дениска', 'Юренкович', 'Боецович', 1, 20, 'liska@mail.ru', 1),
	('Рони', 'Коулманович', 'Колуман', 35, 51, 'lightweightbaby@mail.ru', 2);

INSERT INTO beginners(person_id, trainer) VALUES
	(1, 2),
	(4, 2),
	(5, 6);

INSERT INTO users(user_login, user_password, is_authenticated, person_id) VALUES
	('zemlya_warface119', crypt('kiaolk19sma13', gen_salt('md5')), false, 1),
	('kemosaaabe', crypt('oielas184nakl135', gen_salt('md5')), false, 2),
	('box_master', crypt('gaijds13gjia0', gen_salt('md5')), false, 3),
	('komar_warface_chix11', crypt('vaoimo10lok', gen_salt('md5')), false, 4),
	('boets228', crypt('kitaloyani01lok1sa', gen_salt('md5')), false, 5),
	('lightweight', crypt('yeaahbaby12ksandra616', gen_salt('md5')), false, 6);

INSERT INTO folders(folder_name, creation_date, author_id) VALUES 
	('Тренировки', '2022-02-12', 1),
	('Как правильно тренировать?', '2022-02-12', 2),
	('Заметки', '2022-02-12', 2),
	('Заметки', '2022-02-12', 4),
	('Заметки', '2022-02-12', 5);

INSERT INTO notes(note_name, note_description, creation_date, author_id, folder_id) VALUES
	('Дневник тренировок', 'Описание', '2022-12-02', 1, 1),
	('Неудачная заметка', 'Описание', '2022-12-02', 1, 1),
	('Заметка комарика', '	Описание', '2022-12-02', 4, 4),
	('Как я пожал 500кг', 'Описание', '2022-12-02', 2, 3),
	('Заметка про варфейс', 'Описание', '2022-12-02', 5, 5);
	
INSERT INTO article_types(article_type_name, article_type_description) VALUES
	('Питание', 'О питании'),
	('Тренировки', 'О тренировках'),
	('Полезное', 'Полезная информация');

INSERT INTO articles(article_name, article_description, creation_date, author_id, article_type) VALUES
	('Как правильно спать?', 'Описание', '2022-12-02', 2, 3),
	('Как правильно тренироваться?', 'Описание', '2022-12-02', 3, 2),
	('Как правильно есть?', 'Повседневная практика показывает, что начало повседневной работы по формированию позиции в значительной степени обуславливает создание новых предложений. Разнообразный и богатый опыт дальнейшее развитие различных форм деятельности требуют определения и уточнения системы обучения кадров, соответствует насущным потребностям.', '2022-12-02', 3, 2);
	
-- Создание ролей и пользователей

 CREATE ROLE trainer;
 CREATE ROLE beginner;

 CREATE USER zemlya_warface119 WITH PASSWORD 'kiaolk19sma13';
 CREATE USER kemosaaabe WITH PASSWORD 'oielas184nakl135';
 CREATE USER box_master WITH PASSWORD 'gaijds13gjia0';
 CREATE USER komar_warface_chix11 WITH PASSWORD 'vaoimo10lok';
 CREATE USER boets228 WITH PASSWORD 'kitaloyani01lok1sa';
 CREATE USER lightweight WITH PASSWORD 'yeaahbaby12ksandra616';

 GRANT beginner TO zemlya_warface119;
 GRANT beginner TO boets228;
 GRANT beginner TO komar_warface_chix11;
 GRANT trainer TO kemosaaabe;
 GRANT trainer TO lightweight;
 GRANT trainer TO box_master;

-- Создание политик и привилегий

ALTER TABLE folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE deleted_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;


GRANT SELECT ON person_types TO trainer, beginner;
GRANT SELECT ON beginners TO trainer, beginner;
GRANT SELECT ON persons_info TO trainer, beginner;
GRANT SELECT ON users TO trainer, beginner;
GRANT SELECT ON article_types TO trainer;
GRANT CONNECT ON DATABASE training_diary TO trainer, beginner;

CREATE POLICY show_user ON users
FOR SELECT
TO trainer, beginner
USING (
	user_login = CURRENT_USER
);


GRANT ALL ON folders, notes TO trainer, beginner;
GRANT ALL ON deleted_notes TO trainer, beginner;
GRANT UPDATE ON folders_folder_id_seq, notes_note_id_seq TO trainer, beginner;
GRANT UPDATE ON deleted_notes_deleted_note_id_seq TO trainer, beginner;

CREATE POLICY actions_with_folders ON folders
FOR ALL
TO trainer, beginner
USING (
	(SELECT user_login FROM users
	WHERE person_id = folders.author_id) = CURRENT_USER
);


CREATE POLICY actions_with_notes ON notes
FOR ALL
TO trainer, beginner
USING (
	(SELECT user_login FROM users
	WHERE person_id = notes.author_id) = CURRENT_USER
);

CREATE POLICY actions_with_deleted_notes ON deleted_notes
FOR ALL
TO trainer, beginner
USING (
	(SELECT user_login FROM users
	WHERE person_id = author_id) = CURRENT_USER
);

CREATE POLICY show_notes ON notes
FOR SELECT
TO trainer, beginner
USING (
	(SELECT user_login FROM users
	WHERE person_id = notes.author_id) = CURRENT_USER
);

CREATE POLICY show_notes_by_trainer ON notes
FOR SELECT
TO trainer
USING (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT trainer FROM beginners
		WHERE person_id = author_id
	)) = CURRENT_USER
);

CREATE POLICY action_with_notes_by_beginner ON notes
FOR ALL
TO beginner
USING (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT author_id FROM folders
		WHERE folder_id = notes.folder_id 
	)) = CURRENT_USER
);

CREATE POLICY action_with_deleted_notes_by_beginner ON deleted_notes
FOR INSERT
TO beginner
WITH CHECK (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT person_id FROM beginners
		WHERE trainer = author_id
	)) = CURRENT_USER
);

CREATE POLICY actions_with_deleted_notes_by_trainer ON deleted_notes
FOR ALL
TO trainer
USING (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT trainer FROM beginners
		WHERE person_id = author_id
	)) = CURRENT_USER
);

CREATE POLICY show_folders_by_trainer ON folders
FOR SELECT
TO trainer
USING (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT trainer FROM beginners
		WHERE person_id = author_id
	)) = CURRENT_USER
);

CREATE POLICY change_notes_by_trainer ON notes
FOR UPDATE
TO trainer
USING (true)
WITH CHECK (
	(SELECT user_login FROM users
	WHERE person_id = (
		SELECT trainer FROM beginners
		WHERE person_id = author_id
	)) = CURRENT_USER	
);

GRANT ALL ON articles TO trainer;
GRANT UPDATE ON articles_article_id_seq TO trainer;

CREATE POLICY actions_with_articles ON articles
FOR ALL
TO trainer
USING (
	(SELECT user_login FROM users
	WHERE person_id = articles.author_id) = CURRENT_USER
);


-- Автоматизация
-- Создание пользователя

CREATE OR REPLACE PROCEDURE create_user(user_name varchar, user_middle_name varchar, user_surname varchar,
									  user_experience integer, user_age integer, user_email varchar,
									  user_role varchar, user_login varchar, user_pass varchar) AS $$
DECLARE
	user_type int4;
	user_id int4;
BEGIN
	IF (SELECT COUNT(*) FROM pg_roles WHERE rolname = user_login) THEN
		RAISE EXCEPTION 'Такой пользователь уже существует.';
	ELSE
		IF (user_role = 'beginner') THEN
			user_type := 1;
			ELSE IF (user_role = 'trainer') THEN
				user_type := 2;
			END IF;
		END IF;
		
		EXECUTE format('INSERT INTO persons_info(person_name, person_middle_name, person_surname, 
					   	train_experience, person_age, person_email, person_type)
					    VALUES (%L, %L, %L, %L, %L, %L, %L)',
					  	user_name, user_middle_name, user_surname, user_experience, 
					   	user_age, user_email, user_type);
		
		SELECT MAX(person_id) INTO user_id FROM persons_info;
		
		EXECUTE format('INSERT INTO users(user_login, user_password, is_authenticated, person_id)
					    VALUES (%L, crypt(%L, gen_salt(''md5'')), %L, %L)',
					  	user_login, user_pass, false, user_id);
						
		EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', user_login, user_pass);
		EXECUTE format('GRANT %I TO %I', user_role, user_login);
		EXECUTE format('GRANT CONNECT ON DATABASE training_diary TO %I', user_login);
	END IF;
END;
$$ LANGUAGE plpgsql;


-- Создание заметки

CREATE OR REPLACE PROCEDURE create_note(note_name varchar, note_description varchar,
									folder_id integer) AS $$
DECLARE
	creation_date TIMESTAMP := now()::TIMESTAMP WITHOUT TIME ZONE;
	author_id integer;
BEGIN
	SELECT person_id INTO author_id FROM users
	WHERE user_login = CURRENT_USER;

	
	EXECUTE format('INSERT INTO notes(note_name, note_description, creation_date, author_id, folder_id)
				   	VALUES (%L, %L, %L, %L, %L)',
				  	note_name, note_description, creation_date, author_id, folder_id);
END;
$$ LANGUAGE plpgsql;


-- Создание папки

CREATE OR REPLACE PROCEDURE create_folder(folder_name varchar) AS $$
DECLARE
	creation_date TIMESTAMP := now()::TIMESTAMP WITHOUT TIME ZONE;
	author_id integer;
BEGIN
	SELECT person_id INTO author_id FROM users
	WHERE user_login = CURRENT_USER;

	EXECUTE format('INSERT INTO folders(folder_name, creation_date, author_id)
				   	VALUES (%L, %L, %L)',
				  	folder_name, creation_date, author_id);
END;
$$ LANGUAGE plpgsql;


-- Создание статьи

CREATE OR REPLACE PROCEDURE create_article(article_name varchar, article_description varchar, 
										   article_type integer) AS $$
DECLARE
	creation_date DATE := CURRENT_DATE;
	author_id integer;
BEGIN
	SELECT person_id INTO author_id FROM users
	WHERE user_login = CURRENT_USER;

	EXECUTE format('INSERT INTO articles(article_name, article_description, creation_date, author_id,
				  	article_type)
				   	VALUES (%L, %L, %L, %L, %L)',
				  	article_name, article_description, creation_date, author_id, article_type);
END;
$$ LANGUAGE plpgsql;

GRANT EXECUTE ON PROCEDURE create_note TO beginner, trainer;
GRANT EXECUTE ON PROCEDURE create_folder TO beginner, trainer;
GRANT EXECUTE ON PROCEDURE create_article TO trainer;


-- Перемещаем заметку в корзину

CREATE OR REPLACE FUNCTION move_to_trash() RETURNS trigger AS $$
DECLARE
	deletion_date TIMESTAMP := now()::TIMESTAMP WITHOUT TIME ZONE;
BEGIN
	EXECUTE format('INSERT INTO deleted_notes(note_name, note_description, creation_date,
				  	author_id, folder_id, deletion_date)
				  	VALUES (%L, %L, %L, %L, %L, %L)',
				  	OLD.note_name, OLD.note_description, OLD.creation_date, OLD.author_id,
				  	null, deletion_date);
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_delete_note
AFTER DELETE ON notes
FOR EACH ROW
EXECUTE FUNCTION move_to_trash();

-- Восстановить заметку

CREATE OR REPLACE FUNCTION recover_note() RETURNS trigger AS $$
DECLARE
BEGIN
	EXECUTE format('INSERT INTO notes(note_name, note_description, creation_date,
				  	author_id, folder_id)
				  	VALUES (%L, %L, %L, %L, %L)',
				  	OLD.note_name, OLD.note_description, OLD.creation_date, OLD.author_id,
				  	NULL);
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE choose_trainer(beginner integer, trainer_id integer) AS $$
DECLARE 
BEGIN 
	IF (SELECT COUNT(*) FROM beginners WHERE person_id = beginner) THEN 
		EXECUTE format('UPDATE beginners SET trainer=%L WHERE person_id=%L', trainer_id, beginner);
	ELSE
		EXECUTE format('INSERT INTO beginners(person_id, trainer)
						VALUES (%L, %L)', beginner, trainer_id);
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_recover_from_trash
AFTER DELETE ON deleted_notes
FOR EACH ROW
EXECUTE FUNCTION recover_note();

-- Создание представлений

-- Тренеры
CREATE VIEW trainers_view AS
SELECT * FROM persons_info
WHERE person_type = 2;

-- Новички
CREATE VIEW beginners_view AS
SELECT * FROM persons_info
WHERE person_type = 1;

-- Создание индексов

CREATE INDEX note_id_idx ON notes (note_id);


