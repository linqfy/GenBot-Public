from colorama import Fore
import sqlite3
print("[TUTORIAL] ! Create a file called import.txt, and then specify category in importer.\nBefore this, you have to have some modules installed like\nColorama and mysql.connection, discord, datetime or numpy! so keep that in mind.\nFor the Stock.db to have the categories run the following command in python terminal")
print("[TUTORIAL] [CMD] 1. 'import sqlite3' ")
print("[TUTORIAL] [CMD] 2. 'con = sqlite3.connect('Stock.db')' ")
print("[TUTORIAL] [CMD] 3. 'cur = con.cursor()' ")
print("[TUTORIAL] [CMD] 4. 'cur.execute('''CREATE TABLE Stock (data TEXT, category TEXT)''')' ")
print("[TUTORIAL] ! ONLY DO THIS IF YOU KNOW WHAT YOU ARE DOING !")
print("[TUTORIAL] ! IGNORE IF ALREADY DONE !\n")

try:
    print(Fore.YELLOW + "Trying to connect to database")
    conn = sqlite3.connect('Stock.db')
    cur = conn.cursor()
except Exception as e:
    print(Fore.RED + "Error connecting to database | " + e)
    exit()

print(Fore.GREEN + "Database Connection established")
print(Fore.YELLOW + "Importing entries to Database")

count = 0
try:
    category = input("Enter category: ")
    with open('import.txt', 'r', encoding='utf-8') as f:
        print(Fore.GREEN + category)
        #count_max = len(f.readlines())
        for line in f.readlines():
            print(Fore.GREEN + str(count))  # + str(count_max))
            conn.execute(
                'INSERT INTO stock (data, category) VALUES (?, ?)', (line, category))
            conn.commit()
            print(
                Fore.YELLOW + "[SERVICE_WORKER] Processing line: " + line + ' Into Database')
            count += 1
        print(Fore.YELLOW + "DONE.")
        f.close()
except Exception as e:
    print(e)
cur.close()
conn.close()
