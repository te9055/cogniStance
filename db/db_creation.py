import sqlite3

# Connect to an SQLite database (or create it if it doesn't exist)
#conn = sqlite3.connect('data.db')
conn = sqlite3.connect('datasets.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table
# Create table
#cursor.execute('''CREATE TABLE IF NOT EXISTS news
#             (id integer primary key, title text, location text, pubyear text, pubdate text, websource text, loaddate text, content longtext)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS datasets (id INTEGER PRIMARY KEY AUTOINCREMENT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, dataset_id INTEGER, filename TEXT, date TEXT, content TEXT, FOREIGN KEY(dataset_id) REFERENCES datasets(id))''')
# Insert a row of data
#cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# to select all column we will use
statement = '''SELECT * FROM datasets'''

cursor.execute(statement)
print("All the data")
output = cursor.fetchall()
for row in output:
  print(row)
# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()