import sqlite3

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('data.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table
# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS news
             (id integer primary key, title text, location text, pubyear text, pubdate text, websource text, loaddate text, content longtext)''')



# Insert a row of data
#cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# to select all column we will use
statement = '''SELECT * FROM news'''

cursor.execute(statement)
print("All the data")
output = cursor.fetchall()
for row in output:
  print(row)
# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()