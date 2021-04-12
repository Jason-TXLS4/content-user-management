import sqlite3

con = sqlite3.connect('player_services.db')  # You can create a new database by changing the name within the quotes
c = con.cursor() # The database will be saved in the location where your 'py' file is saved

c.execute('''
INSERT INTO players (title) values ("Clark");
''')

c.execute('''
INSERT INTO players (title) values ("Bruce");
''')

c.execute('''
INSERT INTO players (title) values ("Hal");
''')

con.commit()
c.close()
con.close()