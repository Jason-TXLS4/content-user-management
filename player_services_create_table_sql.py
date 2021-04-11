import sqlite3

conn = sqlite3.connect('player_services.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved


c.execute('''

CREATE TABLE players
(
  players_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title varchar
);
''')

c.execute('''
CREATE TABLE  players_attributes
(
	players_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
);
''')

c.execute('''
CREATE TABLE characters
(
	characters_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    title varchar
);
''')

c.execute('''
CREATE TABLE items
(
    items INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    item_id INTEGER,
    CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id)
);
''')

c.execute('''
CREATE TABLE characters_attributes
(
    characters_attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER,
    attr_title varchar,
    attr_value varchar,
    CONSTRAINT FK FOREIGN KEY(character_id) REFERENCES characters(characters_id) 
 );
''')

conn.commit()

