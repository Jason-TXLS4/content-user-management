import sqlite3

con = sqlite3.connect('player_services.db')  # You can create a new database by changing the name within the quotes
c = con.cursor() # The database will be saved in the location where your 'py' file is saved

# c.execute('''
# INSERT INTO players (title) values ("Clark");
# ''')

# c.execute('''
# INSERT INTO players (title) values ("Bruce");
# ''')

# c.execute('''
# INSERT INTO players (title) values ("Hal");
# ''')


c.execute('''
INSERT INTO characters_attributes (character_id, attr_title, attr_value) values ("1", "HP", "100");
''')

c.execute('''
INSERT INTO characters_attributes (character_id, attr_title, attr_value) values ("2", "HP", "120");''')

c.execute('''
INSERT INTO characters_attributes (character_id, attr_title, attr_value) values ("3", "HP", "140");''')

con.commit()
c.close()
con.close()