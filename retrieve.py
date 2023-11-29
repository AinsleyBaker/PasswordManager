from dbconfig import dbconfig
from prettytable import PrettyTable
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import pyperclip
import aes_encrypt

# Function to compute master key
def calculateMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    # Derive a 32-byte key using PBKDF2 with SHA5127
    key = PBKDF2(password, salt, 32, count = 1000000, hmac_hash_module=SHA512)
    return key

# Function to query database for entries
def retrieveEntries(mp, ds, search, decryptPassword = False):
    # Create a Prettytable object
    table = PrettyTable()
    # Connect to SQL database
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("USE pm")

    # Build SQL query from provided search values
    query = ""
    if len(search) == 0:
        query = "SELECT * FROM manager"
    else:
        query = "SELECT * FROM manager WHERE "
        for i in search:
            query += f"{i} = '{search[i]}' AND "
        query = query[:-5]
    # Run query and fetch results
    cursor.execute(query)
    results = cursor.fetchall()
    # If there are no results
    if not results:
        print("No results for the search.")
        return
    # If user decides to search multiple entries or does not want to copy password
    if (decryptPassword and len(results) > 1) or (not decryptPassword):
        table.field_names = ["Site Name", "URL", "Username", "Email", "Password"]
        for i in results:
            table.add_row([i[0], i[1], i[2], i[3], "{hidden}"])
        print(table)
        return
    # If user decides to search for specific record and selects to copy password
    if len(results) == 1 and decryptPassword:
        master_key = calculateMasterKey(mp, ds)
        decrypted = aes_encrypt.decrypt(key=master_key, source=results[0][4], keyType="bytes")
        # copy to clipboard
        pyperclip.copy(decrypted.decode())
        print("Password copied to clipboard.")
