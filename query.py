import datetime
import mysql.connector

# DB credentials
config = {
  'user': 'piemaster',
  'password': 'piemaster123',
  'host': 'piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com',
  'database': 'PieDB',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

# ------------------Display all rows from table paitweets----------------------
# cursor = cnx.cursor()

# query = ("SELECT id, tweet_id, username, geo_lat, geo_long, text, timestamp FROM pietweets")

# cursor.execute(query)

# for (id, tweet_id, username, geo_lat, geo_long, text, timestamp) in cursor:
# 	print('----------------\n')
# 	print ("ID: {}\ntweetId: {}\nuser name: {}\nlocation: [{},{}]\nkeywords: {}\ntimestamp: {}\n".format(id, tweet_id, username, geo_lat, geo_long, text, timestamp))

# cursor.close()
# ------------------check the size of all tables in database----------------------
cursor = cnx.cursor()

query2 = ("SELECT TABLE_NAME, table_rows, data_length, index_length, round(((data_length + index_length) / 1024 / 1024),2) as MB FROM information_schema.TABLES WHERE table_schema = 'PieDB'") 

cursor.execute(query2)

for (TABLE_NAME, table_rows, data_length, index_length, MB) in cursor:
	print('================\n')
	print ("Table Name: {}\nNum rows: {}\nData length: {}\nIndex length: {}\nTable size in MB: {}\n".format(TABLE_NAME, table_rows, data_length, index_length, MB))
	
cursor.close()

cnx.close()