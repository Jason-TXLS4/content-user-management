import os
import psycopg2


#players_db = os.environ['DATABASE_URL']

conn = psycopg2.connect(players_db, sslmode='require')
c = conn.cursor()

c.execute('''
    CREATE TABLE players
(
    players_id SERIAL PRIMARY KEY,
    title varchar(120)
);
''')

c.execute('''
    CREATE TABLE  players_attributes
(
    players_attributes_id SERIAL PRIMARY KEY,
    player_id INTEGER,
    attr_title varchar(100),
    attr_value varchar(100),
    CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
);
''')

c.execute('''
    CREATE TABLE characters
    (
        characters_id SERIAL PRIMARY KEY,
        game_id INTEGER,
        player_id INTEGER,
        title varchar(100),
        CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
    );
''')

c.execute('''
    CREATE TABLE items
    (
        items_id SERIAL PRIMARY KEY,
        character_id INTEGER,
        item_id INTEGER,
        CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id)
    );
''')

c.execute('''
    CREATE TABLE characters_attributes
    (
        characters_attributes_id SERIAL PRIMARY KEY,
        character_id INTEGER,
        attr_title varchar(100),
        attr_value varchar(100),
        CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id) 
    );
''')

conn.commit()
c.close()
conn.close()
