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

qadd_one = ("INSERT INTO paitweets "
               "(tweet_id, username, geo_lat, geo_long, text, timestamp) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
data_one = (572844984476545024, 'PieMaster', 60.00, 60.00, '@carlsontinashe @DearAngelbert @mafaizer those who admit their hunger shall b given food', '2015-03-03 22:17:56')

cursor.execute(qadd_one, data_one)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()