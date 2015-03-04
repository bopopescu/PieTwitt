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
cursor = cnx.cursor()

query = ("DELETE FROM pitweets")
cursor.execute(query)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()