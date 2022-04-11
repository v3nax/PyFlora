import sqlite3

select_query = "SELECT sqlite_version();"
database_name = 'baze\\administracija.db'
def create_table(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        print("Baza je USPJESNO kreirana te je aplikacija spojena na SQLite")
        cur.execute(select_query)
        rec = cur.fetchall()
        print("SQLite verzija je: ", rec)
        cur.close()
        print("Resursi SQLite cur objekta su uspješno otpušteni")
    except sqlite3.Error as error:
        print("ERROR - Dogodila se greska prilikom pokusaja spajanja na SQLite:", error)
    finally:
        if conn:
            conn.close()
            print("SQLite konekcija je uspješno zatvorena")
            
    ### tablica PYbiljke ##

    table_query1 = f'''CREATE TABLE IF NOT EXISTS administracija (
                    korisnicko_ime  TEXT NOT NULL UNIQUE,
                    lozinka         TEXT NOT NULL,
                    ime             TEXT NOT NULL,
                    prezime         TEXT NOT NULL);'''

    print(table_query1)


    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(table_query1)

    conn.commit()
    print(f"Nova tabela je uspjesno kreirana")

    cur.close()

# create_table(database_name)

def insert_posuda(database_name, korisnik, lozinka, ime, prezime):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")


        sqlite_insert_query = """INSERT INTO administracija (
                                    korisnicko_ime, 
                                    lozinka,
                                    ime,
                                    prezime)
                                 VALUES 
                                    (?, ?, ?, ?)"""

          
        # Convert data into tuple format
        data_tuple = (korisnik, lozinka, ime, prezime)
          
        # using cursor object executing our query
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
  
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()

# insert_posuda(database_name, 'Venax', 'n3tko', 'Natalia', 'Veceric')

def update_korisnik(database_name, unq, korisnik, lozinka, ime, prezime):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cur = sqliteConnection.cursor()
        # print("Connected to SQLite")

        data = cur.execute(f""" UPDATE  
                                    administracija
                                SET
                                    korisnicko_ime='{korisnik}', 
                                    lozinka='{lozinka}',
                                    ime='{ime}',
                                    prezime='{prezime}'
                                WHERE   
                                    korisnicko_ime='{unq}';""")
                              
        for d in data:
            print (d)
        sqliteConnection.commit()

        cur.close()
  
    except sqlite3.Error as error:
        print("Nista ", error)
      
    finally:
        if sqliteConnection:
            sqliteConnection.close()
