# basic libraries
import json
import errno
from mysql.connector import errorcode
import urllib3
from datetime import datetime

# date time manipulation
import dateutil.parser
from pytz import timezone
import pytz

# tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# mysql connector
import mysql.connector

# Alchemy API Key
# 752f1ed251b75b7800b23a7cb73c4d9a0c0f9cfd
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()


# ------------------------End of Library Imports-----------------------------------------

# Twitter consumer/ accesss key and secret
accessKey = '3064523805-j1pUg9xKiL6GG4aOLrMrCNbq6rFGNk7auVprzm4'
accessToken = 'sIufLPBNv8WiQ1zzcp6jmOgkOkZ5csk79GJ9L46H3lh7K'
consumerKey = 'f2gQNjXOIwXNnzaNVboNLB7zy'
consumerSecret = 'DlPdIXIkwgCGZLp0IUjU5418a9txJrp27qKsGovZh9iumcXyYy'

# DB credentials
config = {
  'user': 'piemaster',
  'password': 'piemaster123',
  'host': 'piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com',
  'database': 'PieDB',
  'raise_on_warnings': True,
}

# ------------------------End of DB credientials-----------------------------------------

def analyzeSentiment(text):
	myText = text
	response = alchemyapi.sentiment("text", myText)
	if response["docSentiment"]:
		sentScore = response["docSentiment"]["type"]
		print "text: ", text
		print "Sentiment: ", sentScore
		return sentScore
	else:
		return 0


class StdOutListener(StreamListener):

	def on_status(self, status):
		
		# creating cursor for the operation of this tweet
		cursor = cnx.cursor()

		tweet = status

		# validate that user id not null
		if tweet.user == None:
			print 'No user data - ignoring tweet.'
			return True

		# getting username, tweet content, and geo location for each tweet
		user = tweet.user.name.encode('ascii','ignore')
		text = tweet.text.encode('ascii','ignore')
		tweetId = tweet.id_str.encode('ascii')
		location = ''
		if tweet.geo != None:
			location = tweet.geo['coordinates']

		d = datetime.now()

		tmstr = d.strftime("%Y-%m-%d %H:%M:%S")

		# only insert into pitweets table if none of the 6 fields is null
		if user == '' or tweetId == '' or tmstr == '' or text == '' or location == '':
			# print summary of tweet
			print "X---------------------------------INVALID---------------------------------X"
			print('%s\n%s\n%s\n%s\n%s\n\n ----------------\n' % (user, tweetId, tmstr, location, text))
		else:		

			# sentiment analysis through alchemy API
			score = analyzeSentiment(text)

			# only insert into DB if exist sentiment score
			if score == 0:
				print "No sentiment score ;_;"
			else:


				# insertion work to table pitweets
				tweetId = int(tweetId)
				geoLat = location[0]
				geoLong = location[1]

				# building query and query data
				qadd_one = ("INSERT INTO lemonpie "
	               "(tweet_id, username, geo_lat, geo_long, text, timestamp) "
	               "VALUES (%s, %s, %s, %s, %s, %s)")
				data_one = (tweetId, user, geoLat, geoLong, text, tmstr)

				# executing query
				cursor.execute(qadd_one, data_one)

				# Make sure data is committed to the database
				cnx.commit()
				
				print "<3--------------------------------SUCCESS--------------------------------<3"
		
		# closing the cursor for this operation
		cursor.close()
		return True

	def on_error(self, status):
		print 'Error on status', status

	def on_limit(self, status):
		print 'Limit threshold exceeded', status

	def on_timeout(self, status):
		print 'Stream disconnected; continuing...'

try:
	cnx = mysql.connector.connect(**config)
	print "connection established"

	# connect to twitter API for twitter stream
	l = StdOutListener()
	auth = OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessToken)

	stream = Stream(auth, l)

	print("Listening to filter stream...")

	# put steam function in a while loop to suppress incompleteread error
	for i in range(1000):
		try:
			# check out -180, -90, 180, 90
			stream.filter(track=["weather"], locations=[-179.9,-89.9,179.9,89.9])
		except RuntimeError:
			print "OHNOOOOO"
			quit()

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Something is wrong with your user name or password" 
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exist" 
	else:
		print err 
else:
	cnx.close()



