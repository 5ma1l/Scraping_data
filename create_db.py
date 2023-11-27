import sqlite3
from util import *


conn = sqlite3.connect('databse.db')

cursor = conn.cursor()



create_table_hospitals = '''
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    type TEXT NOT NULL,
    ville TEXT NOT NULL,
    media_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media(id)
);
'''
create_table_user='''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    isAdmin INTERGER,
    location TEXT,
    ville TEXT,
    date_inscription DATE NOT NULL,
    media_id INTEGER NOT NULL,
    FOREIGN KEY (media_id) REFERENCES media(id)
);
'''
create_table_media='''
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    fichier TEXT NOT NULL
);
'''

create_table_service='''
CREATE TABLE IF NOT EXISTS services(
    id INTEGER PRIMARY KEY,
    hospital_id INTEGER,
    pharmacie_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id),
    FOREIGN KEY (pharmacie_id) REFERENCES pharmacie(id)
);
'''

create_table_discussion='''
CREATE TABLE IF NOT EXISTS discussion (
    id INTEGER PRIMARY KEY,
    contenu TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
'''


create_table_urgence='''
CREATE TABLE IF NOT EXISTS urgence (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    user_id INTEGER,
    service_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
'''

cursor.execute(create_table_hospitals)
cursor.execute(create_table_user)
cursor.execute(create_table_media)
cursor.execute(create_table_service)
cursor.execute(create_table_discussion)
cursor.execute(create_table_urgence)

conn.commit()
i=1
for data in db:
        insert_query="INSERT INTO hospitals (id,name,location,type,ville,media_id) values(?,?,?,?,?,?)"
        cursor.execute(insert_query,(i,data[0],str(data[2]),"public",data[1],"1"))
        i+=1

cursor.execute("INSERT INTO media(id,type,fichier) values(?,?,?)",("1","hospital","hospital_media.png"))
cursor.execute("INSERT INTO media(id,type,fichier) values(?,?,?)",("2","pharmacie","pharmacie_media.png"))
cursor.execute("INSERT INTO media(id,type,fichier) values(?,?,?)",("3","user","user_media.png"))
conn.commit()

cursor.close()
conn.close()



