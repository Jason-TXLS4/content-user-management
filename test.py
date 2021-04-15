import sqlite3

#con = sqlite3.connect('player_services.db')
con = sqlite3.connect('content_services.db')
c = con.cursor() 
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
INSERT INTO items (game_id, title, description) values (123,'shortsword','Short sword. Sharp.');
''')

c.execute('''
INSERT INTO items (game_id, title, description) values (123,'Laser Blaster','Pew Pew');
''')

c.execute('''
INSERT INTO items (game_id, title, description) values (456,'Sais',"Raph's weapons of choice.");
''')



con.commit()
c.close()
con.close()