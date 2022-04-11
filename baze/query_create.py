import sqlite3


select_query = "SELECT sqlite_version();"
database_name = 'baze\\pyFlora.db'
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

    table_query1 = f'''CREATE TABLE IF NOT EXISTS pybiljke (
                    naziv_biljke    TEXT NOT NULL UNIQUE,
                    fotografija     TEXT NOT NULL UNIQUE,
                    opis            TEXT NOT NULL UNIQUE,
                    zalijevanje     TEXT NOT NULL,
                    osvjetljenje    TEXT NOT NULL,
                    toplina         TEXT NOT NULL,
                    dohrana         BOOLEAN NOT NULL);'''

    print(table_query1)


    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(table_query1)

    conn.commit()
    print(f"Nova tabela je uspjesno kreirana")

    cur.close()

    ### tablica PYposude ##


    table_query2 = f'''CREATE TABLE IF NOT EXISTS pyposude (
                    naziv_posude        TEXT NOT NULL UNIQUE,
                    sadnica             BOOLEAN NOT NULL,
                    naziv_biljke        TEXT,
                    FOREIGN KEY             (naziv_biljke) 
                    REFERENCES pybiljke     (naziv_biljke)
                    );'''
                    
    print(table_query2)
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(table_query2)
    conn.commit()
    print(f"Nova tabela je uspjesno kreirana")
    cur.close()

    table_query3 = f'''CREATE TABLE IF NOT EXISTS pynjega (
                    naziv_posude                INTEGER NOT NULL,
                    naziv_biljke                TEXT NOT NULL,
                    vrijeme_mjerenja            TEXT NOT NULL,
                    vlaznost_postotak           INTEGER NOT NULL,
                    intenzitet_osvjetljenja_lx  INTEGER NOT NULL,
                    temperatura_celzijus        REAL NOT NULL,
                    tlo_ph                      REAL NOT NULL,
                    FOREIGN KEY                 (naziv_posude) 
                    REFERENCES pyosuda          (naziv_posude),
                    FOREIGN KEY                 (naziv_biljke) 
                    REFERENCES pyosuda          (naziv_biljke)
                    );'''
    print(table_query3)
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(table_query3)
    conn.commit()
    print(f"Nova tabela je uspjesno kreirana")
    cur.close()
 
 
          ### Spajanje posuda po kljucu  ##
 
    table_query4 = f'''CREATE TABLE IF NOT EXISTS konekcija (
                    naziv_posude                   INTEGER NOT NULL,
                    naziv_biljke                   INTEGER NOT NULL,
                    PRIMARY KEY                 (naziv_posude, naziv_biljke),
                    FOREIGN KEY                 (naziv_posude) 
                    REFERENCES pyosuda          (naziv_posude) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION,
                    FOREIGN KEY                 (naziv_biljke) 
                    REFERENCES pybiljke         (naziv_biljke) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION );'''
    print(table_query4)
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(table_query4)

    conn.commit()
    print(f"Nova tabela je uspjesno kreirana")
    cur.close()

create_table(database_name)

# create_table(database_name)

# dbCon = sqlite3.connect("pybiljke.db")

 

# # Obtain a Cursor object to execute SQL statements

# cur   = dbCon.cursor()

# cur.execute('DROP TABLE sqlite_sequence')

# dbCon.commit()
# print(f"Nova tabela je uspjesno kreirana")

# cur.close()

# # ADD a new COLUMN to table

# addColumn = "ALTER TABLE pybiljke ADD COLUMN opis BLOB NOT NULL"

# cur.execute(addColumn)

# # DELETE an existing COLUMN from table
# # dropColumn = "ALTER TABLE pybiljke DROP COLUMN opis;"
# # cur.execute(dropColumn)

