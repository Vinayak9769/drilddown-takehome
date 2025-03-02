import pandas as pd
import sqlite3
df1 = pd.read_csv('file1.csv')
df2 = pd.read_csv('file2.csv')
combined_df = pd.concat([df1, df2], ignore_index=True)
conn = sqlite3.connect('database.db')
combined_df.to_sql('combined_table', conn, if_exists='replace', index=False)
conn.close()
print("CSV files have been successfully merged into a single SQLite table.")
