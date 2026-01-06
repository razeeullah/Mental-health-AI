import sqlite3
import hashlib
import secrets

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Updated schema to include salt
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password_hash TEXT, salt TEXT, email TEXT)''')
    conn.commit()
    conn.close()

def hash_pass(password, salt):
    """Hashes the password with a salt using SHA-256."""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def register_user(username, password, email=""):
    """Registers a new user with a salted password hash."""
    try:
        salt = secrets.token_hex(16)
        password_hash = hash_pass(password, salt)
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password_hash, salt, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Registration Error: {e}")
        return False

def login_user(username, password):
    """Verifies user credentials by hashing the input with the stored salt."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash, salt FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        stored_hash, salt = user
        return hash_pass(password, salt) == stored_hash
    return False
