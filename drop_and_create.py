import sqlite3

con = sqlite3.connect('player_services.db')  # You can create a new database by changing the name within the quotes
c = con.cursor() # The database will be saved in the location where your 'py' file is saved

c.execute('''
DROP TABLE characters
''')

c.execute('''
CREATE TABLE characters
(
	characters_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player_id INTEGER,
    title varchar,
    CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
);
''')



con.commit()
c.close()
con.close()