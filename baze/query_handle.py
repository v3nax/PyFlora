import sqlite3

database_name = 'baze\\pyFlora.db'

def convert_data(file_name):

    with open(file_name, 'rb') as file:
        blobData = file.read()
    return blobData
  
  
def insert_plant(database_name, name, photo, opis, zalijevanje, osvjetljenje, toplina, dohrana):
    # print(database_name,name,photo,opis)
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_blob_query = """ INSERT INTO pybiljke
                                  (naziv_biljke, 
                                  fotografija, 
                                  opis, 
                                  zalijevanje, 
                                  osvjetljenje, 
                                  toplina, 
                                  dohrana ) 
                                  VALUES (?, ?, ?, ?, ?, ? , ?)"""
     

        # empFoto = convert_data(photo)
        # empOpis = convert_data(opis)
          
        # Convert data into tuple format
        data_tuple = (name, photo, opis, zalijevanje, osvjetljenje, toplina, dohrana)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def update_plants(database_name, new_plant, foto, doc, watering, light, climate, boost, plant):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")
        # empFoto = convert_data(foto)
        # empOpis = convert_data(doc)

        data = cur.execute(f""" UPDATE  pybiljke
                                SET     naziv_biljke = '{new_plant}',
                                        fotografija = '{foto}',
                                        opis = '{doc}',
                                        zalijevanje ='{watering}',
                                        osvjetljenje = '{light}',
                                        toplina = '{climate}',
                                        dohrana = '{boost}'
                                WHERE   naziv_biljke = '{plant}'
                                ;""")
                              
        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def update_pots(database_name, new_pot_name, has_plant, plant_name, pot_name):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")

        if has_plant == True or has_plant == 'True':
            data = cur.execute(f""" UPDATE  pyposude
                                SET     naziv_posude = '{new_pot_name}',
                                        sadnica = '{has_plant}',
                                        naziv_biljke = '{plant_name}'
                                WHERE   naziv_posude = '{pot_name}'
                                ;""")
        else:
            data = cur.execute(f""" UPDATE  pyposude
                                SET     naziv_posude = '{new_pot_name}',
                                        sadnica = '{has_plant}',
                                        naziv_biljke = NULL
                                WHERE   naziv_posude = '{pot_name}'
                                ;""")
                    
        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def select_measurements(database_name):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f""" SELECT naziv_posude, naziv_biljke 
                                FROM pyposude
                                JOIN pynjega USING (naziv_posude)
                                WHERE pynjega.naziv_posude = naziv_posude
                                AND pynjega.naziv_biljke = naziv_biljke""")

        sqliteConnection.commit()

        cur.close()
        return data
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_compare(database_name, naziv_posude):

        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f""" SELECT  DISTINCT naziv_posude,
                                        naziv_biljke, 
                                        zalijevanje, 
                                        osvjetljenje, 
                                        toplina, 
                                        dohrana, 
                                        vrijeme_mjerenja, 
                                        vlaznost_postotak, 
                                        intenzitet_osvjetljenja_lx, 
                                        temperatura_celzijus, tlo_ph
                                FROM pybiljke
                                JOIN pynjega USING (naziv_biljke)
                                WHERE pynjega.naziv_posude = '{naziv_posude}'
                                ORDER BY vrijeme_mjerenja DESC
                                LIMIT (SELECT (COUNT(DISTINCT naziv_posude)+1) FROM pynjega);""")
        # data.fetchone()
        # for d in data:
        #     print (d)
        sqliteConnection.commit()

        return data.fetchone()
    

# select_compare(database_name)

def update_sensors(database_name):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f"""UPDATE pynjega 
                                SET price=(SELECT price FROM table2 WHERE table1.id=table2.id);""")

        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def update_pot_new_name(database_name, novi_naziv, posuda):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f"""UPDATE pynjega 
                                SET naziv_posude='{novi_naziv}'
                                WHERE naziv_posude='{posuda}';""")

        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def delete_old_plant_data(database_name, novi_naziv, posuda):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f"""DELETE pynjega 
                                SET naziv_posude='{novi_naziv}'
                                WHERE naziv_posude='{posuda}';""")

        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def insert_posuda(database_name, pot_name, has_plant, plant_name):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")


        sqlite_insert_query = """ INSERT INTO pyposude (
                                naziv_posude, 
                                sadnica,
                                naziv_biljke)
                                VALUES (?, ?, ?)"""

          
        # Convert data into tuple format
        data_tuple = (pot_name, has_plant, plant_name)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_image(naziv_biljke):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")


        data = cur.execute(f""" SELECT fotografija
                                FROM pybiljke
                                WHERE naziv_biljke = '{naziv_biljke}';""")
        for d in data:
            # print ('Uspjesno!')
            name = d[0]
        sqliteConnection.commit()

        cur.close()
        return name
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def insert_measuring(database_name, naziv_posude, naziv_biljke, datetime, humidity, lumination, temperature, soil_ph):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        data = cursor.execute('SELECT naziv_posude FROM pyposude ORDER BY naziv_posude DESC LIMIT 1;')
        for d in data:
            # print(d[0])
            data_tuple = (naziv_posude, naziv_biljke, datetime, humidity, lumination, temperature, soil_ph)
            # print(data_tuple)


        sqlite_insert_query = """ INSERT INTO pynjega(
                                naziv_posude,
                                naziv_biljke,
                                vrijeme_mjerenja,
                                vlaznost_postotak,
                                intenzitet_osvjetljenja_lx,
                                temperatura_celzijus,
                                tlo_ph) 
                                VALUES ( ?, ?, ?, ?, ?, ?, ?);"""
         
        # Convert data into tuple format
        
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def sync_measurements(database_name, naziv_posude, naziv_biljke, datetime, humidity, lumination, temperature, soil_ph):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_query = """ INSERT INTO pynjega(
                                naziv_posude,
                                naziv_biljke,
                                vrijeme_mjerenja,
                                vlaznost_postotak,
                                intenzitet_osvjetljenja_lx,
                                temperatura_celzijus,
                                tlo_ph) 
                                VALUES ( ?, ?, ?, ?, ?, ?, ?);"""
         
        # Convert data into tuple format
        data_tuple = (naziv_posude, naziv_biljke, datetime, humidity, lumination, temperature, soil_ph)

          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def insert_connection(database_name, naziv_posude, naziv_biljke):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")


        sqlite_insert_query = """ INSERT INTO konekcija (
                                naziv_posude, 
                                naziv_biljke) 
                                VALUES (?, ?)"""

          
        # Convert data into tuple format
        data_tuple = (naziv_posude, naziv_biljke)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def delete_sensors(database_name, name, naziv_biljke):

    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()

        cur.execute(f'''DELETE
                        FROM pynjega
                        WHERE naziv_posude = "{name}"
                        AND   naziv_biljke = "{naziv_biljke}";''')

        conn.commit()
        cur.close()
        print(f'Uspjesno obrisani senzori biljke {naziv_biljke} za posudu {name}.')
  
    except sqlite3.Error as error:
        print("Failed to delete data.", error)
      
    finally:
        if conn:
            conn.close()
    
def delete_row(database_name, table, column_name, name):

    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()

        cur.execute(f'''DELETE
                        FROM {table}
                        WHERE {column_name}="{name}";''')
        conn.commit()
        cur.close()
  
    except sqlite3.Error as error:
        print("Failed to delete data.", error)
      
    finally:
        if conn:
            conn.close()

def delete_one_value(database_name, table, column_name, name):
    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        """UPDATE naziv_posude SET n=null where n=0"""

        cur.execute(f'''DELETE naziv_posude
                        FROM {table}
                        WHERE {column_name}="{name}";''')


        conn.commit()
        cur.close()
  
    except sqlite3.Error as error:
        print("Failed to delete data.", error)
      
    finally:
        if conn:
            conn.close()


def select_all(database_name, table_name, column): 
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} ORDER BY {column} ASC")
    rows = cur.fetchall()
    return rows

def select_one_by_name(database_name,  naziv_posude):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM pyposude WHERE naziv_posude='{naziv_posude}'")
    rows = cur.fetchall()
    return rows

def select_pl_by_name(database_name,  naziv_biljke):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM pybiljke WHERE naziv_biljke='{naziv_biljke}'")
    rows = cur.fetchall()
    return rows

def select_all_full(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM pyposude WHERE sadnica=1 OR sadnica='True'")
    rows = cur.fetchall()
    return rows

def select_by_name(database_name, table1_name, table2_name): 
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f"""SELECT naziv_posude
                    FROM {table1_name} 
                    JOIN {table2_name} 
                    WHERE {table1_name}.naziv_posude = naziv_posude""")
    rows = cur.fetchone()

# select_by_id('baze\\pybiljke.db', 'pyposude', 'pynjega', 'naziv_posude', 10)

def get_last_row(database_name, table_name, table2_name, name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f'''SELECT      *
                    FROM        {table_name}
                    JOIN        {table2_name}
                    WHERE       {table2_name}.naziv_posude = "{name}"
                    ORDER BY    vrijeme_mjerenja DESC
                    LIMIT       1;''')
    rows = cur.fetchall()
    return rows

def get_biljke(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(f'''SELECT  *
                    FROM    pybiljke
                    WHERE   pybiljke.naziv_biljke = naziv_biljke;''')
    rows = cur.fetchall()
    return rows



#get_last_id('baze\\pybiljke.db', 'pyposude', 'naziv_posude',)

def cursor_close(database_name):
    conn = sqlite3.connect(database_name)
    if conn:
            conn.close()

def n_estimate(database_name, table):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    e = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    return e

