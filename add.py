from dbconfig import dbconfig
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import aes_encrypt
import random
import string

# Function to compute master key
def calculateMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    # Derive a 32-byte key using PBKDF2 with SHA5127
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

# Function to add an entry to the password manager
def addEntry(mp, ds, name, url, username, email):
    # Loop until a valid password is chosen
    while True:
        password_choice = int(input("Do you want to (1) enter a password manually or (2) generate a random password? Enter 1 or 2: "))
        if password_choice == 1:
            password = getpass("Password:")
        elif password_choice == 2:
            # Generate a random password of length 12
            characters = string.ascii_letters + string.digits + string.punctuation
            password = "".join(random.choices(characters, k = 12))
            print(f"Successfully generated random password: {password}")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    master_key = calculateMasterKey(mp, ds)
    # Encrypt password using master key
    encrypted = aes_encrypt.encrypt(key=master_key, source=password, keyType="bytes")
    # Connect to SQL database and insert data
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("USE pm")
    cursor.execute("INSERT INTO manager (name, url, username, email, password) VALUES(%s, %s, %s, %s, %s)", (name, url, username, email, encrypted))
    db.commit()
    print("Successfully added entry.")




