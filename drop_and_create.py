import sqlite3

#con = sqlite3.connect('player_services.db')  
con = sqlite3.connect('content_services.db')  
c = con.cursor() 

# c.execute('''
# DROP TABLE characters
# ''')

# c.execute('''
# CREATE TABLE characters
# (
# 	characters_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     game_id INTEGER,
#     player_id INTEGER,
#     title varchar,
#     CONSTRAINT FK FOREIGN KEY(player_id) REFERENCES players(players_id)
# );
# ''')

c.execute('''
DROP TABLE items
''')

c.execute('''
CREATE TABLE items
(
  items_id INTEGER PRIMARY KEY AUTOINCREMENT,
  game_id INTEGER,
  title varchar,
  description varchar
);
''')

con.commit()
c.close()
con.close()