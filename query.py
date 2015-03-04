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

query = ("SELECT tweet_id, username, geo_lat, geo_long, text, timestamp FROM paitweets")

cursor.execute(query)

for (tweet_id, username, geo_lat, geo_long, text, timestamp) in cursor:
	print('----------------\n')
	print ("tweetId: {}\nuser name: {}\nlocation: [{},{}]\nkeywords: {}\ntimestamp: {}\n".format(tweet_id, username, geo_lat, geo_long, text, timestamp))


cursor.close()
cnx.close()