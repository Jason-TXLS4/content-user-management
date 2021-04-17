import psycopg2


players_db = ""
content_db = ""
con = psycopg2.connect(content_db, sslmode='require')
c = con.cursor() 



# c.execute('''
# INSERT INTO players (title) values ('Clark');
# ''')

# c.execute('''
# INSERT INTO players (title) values ('Bruce');
# ''')

# c.execute('''
# INSERT INTO players (title) values ('Hal');
# ''')


c.execute('''
INSERT INTO items (game_id, title, description) values (123,'shortsword','Short sword. Sharp.');
''')

c.execute('''
INSERT INTO items (game_id, title, description) values (123,'Laser Blaster','Pew Pew');
''')

c.execute('''
INSERT INTO items (game_id, title, description) values (456,'Sais','weapon of choice for a certain ninja turle');
''')



con.commit()
c.close()
con.close()