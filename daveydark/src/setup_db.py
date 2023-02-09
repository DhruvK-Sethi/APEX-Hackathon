import pandas as pd
import sqlite3

# Load the .xlsx file into a pandas DataFrame
dfSellers = pd.read_excel('daveydark\src\Database.xlsx')
# dfProducts = pd.read_excel('products.xlsx')

# Connect to an SQLite database
conn = sqlite3.connect('instance/db.sqlite3')

# Write the DataFrame to the database
dfSellers.to_sql('sellers', conn, if_exists='replace', index=False)
# dfProducts.to_sql('products', conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
