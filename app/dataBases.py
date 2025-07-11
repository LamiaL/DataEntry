from app.auth import login_required,admin_required
from app.config import DB_PATH, DB_PATH_M,DB_PATH_FIN,DB_PATH_RH,DB_PATH_USERS,DB_PATH_LISTES
import sqlite3
from werkzeug.security import generate_password_hash

# ------------------ database for users ------------------  
def create_users_table():
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    # Insert default admin user
    hashed_password = generate_password_hash("admin")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("admin", hashed_password, "admin"))

    conn.commit()
    conn.close()

# ------------------ database for inventaire ------------------
# Database setup
def setup_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameAgent TEXT,
            boxNum INTEGER,
            strc TEXT,
            exr TEXT,
            intl TEXT,
            addTopo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP             
        )
    """)
    conn.commit()
    conn.close()
setup_db()

# ------------------ database for inventaire FIN ------------------
# Database setup
def setup_db_fin():
    conn = sqlite3.connect(DB_PATH_FIN)
    cursor = conn.cursor()
    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entriesfin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameAgent TEXT,
            typedoc TEXT,
            de INTEGER,
            au INTEGER,
            boxNum INTEGER,
            manque TEXT,
            rmq TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """) 
    conn.commit()
    conn.close()
setup_db_fin()

# ------------------ database for inventaire RH ------------------
# Database setup
def setup_db_rh():
    conn = sqlite3.connect(DB_PATH_RH)
    cursor = conn.cursor()
    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entriesrh (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameAgent TEXT,
            mtl INTEGER,
            name TEXT,
            fname TEXT,
            bday DATE,
            fonction TEXT,
            dent DATE,
            dsor DATE,
            motifdepart TEXT,
            boxNum INTEGER,
            addTopo TEXT,
            rmq TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
setup_db_rh()

# ------------------ database for inventaire Madjid ------------------
# Database setup
def setup_db_envm():
    conn = sqlite3.connect(DB_PATH_M)
    cursor = conn.cursor()
    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entriesenvm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nameAgent TEXT,
            boxCote INTEGER,
            boxNum TEXT,
            strc TEXT,
            intl TEXT,
            mois DATE,
            anne TEXT,
            typeDoc TEXT,
            cond TEXT,
            comtr TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
setup_db_envm()

# ------------------ database for listes ------------------ 
def setup_db_lst():
    conn = sqlite3.connect(DB_PATH_LISTES)
    cursor = conn.cursor()

    # Create parameters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_name TEXT NOT NULL,
            value TEXT NOT NULL,
            UNIQUE(list_name, value)  -- Prevent duplicate values in the same list
        )
    """)

    # Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM parameters")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert default values only once
        default_data = [
            ('structures', 'RH'),
            ('structures', 'FIN'),
            ('type_doc', 'Bon de commande'),
            ('type_doc', 'Contrat'),
            ('type_doc', 'Avenant'),
            ('motif_depart', 'Essai non concluant'),
            ('motif_depart', 'Licenciement'),
            ('motif_depart', 'Abandon de poste'),
            ('motif_depart', 'départ volontaire'),
            ('motif_depart', 'Retraite'),
            ('motif_depart', 'Fin contract'),
            ('motif_depart', 'Décès'),
            ('motif_depart', 'Service militaire'),
            ('motif_depart', 'Contentieux'),
            ('structures2', 'APCO'),
            ('structures2', 'DRH'),
            ('structures2', 'FORAGE'),
            ('structures2', 'SIE'),
            ('structures2', 'FORMATION'),
            ('structures2', 'DFC'),
            ('structures2', 'LOG'),
            ('structures2', 'QHSE'),
            ('conditionnement', 'Chrono'),
            ('conditionnement', 'Boite'),
            ('conditionnement', 'Envloppe'),
            ('conditionnement', 'Chemise'),
            ('conditionnement', 'Dossier'),
            ('conditionnement', 'CD-ROM'),
            # Add more default values here
        ]

        cursor.executemany("INSERT INTO parameters (list_name, value) VALUES (?, ?)", default_data)

    conn.commit()
    conn.close()

# Call the function
setup_db_lst()
