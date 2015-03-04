# basic libraries
import json

# date time manipulation
import dateutil.parser
from pytz import timezone
import pytz

# tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# flask framework, flask sqlalchemy
import flask

# mysql connector
import mysql.connector

# from flask.ext.sqlalchemy import SQLAlchemy
application = flask.Flask(__name__)

# ------------------------End of Library Imports-----------------------------------------
# setting time for insertion timestamp
sgtz = timezone('US/Eastern')
utc = pytz.timezone('UTC')

# Twitter consumer/ accesss key and secret
accessKey = '3064523805-j1pUg9xKiL6GG4aOLrMrCNbq6rFGNk7auVprzm4'
accessToken = 'sIufLPBNv8WiQ1zzcp6jmOgkOkZ5csk79GJ9L46H3lh7K'
consumerKey = 'f2gQNjXOIwXNnzaNVboNLB7zy'
consumerSecret = 'DlPdIXIkwgCGZLp0IUjU5418a9txJrp27qKsGovZh9iumcXyYy'



# db configuration
# application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{piemaster}:{piemaster123}@{piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com:3306}/{PieDB}'
# db = SQLAlchemy(application)

# DB = {
#         'default': {
#             'ENGINE': 'MySQL 5.6.19b ',
#             'NAME': 'PieDB',
#             'USER': 'piemaster',
#             'PASSWORD': 'piemaster123',
#             'HOST': 'piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com',
#             'PORT': '3306',
#         }
#     }
config = {
  'user': 'piemaster',
  'password': 'piemaster123',
  'host': 'piedb.chhtgdmxqekc.us-east-1.rds.amazonaws.com',
  'database': 'PieDB',
  'raise_on_warnings': True,
}




#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
application.debug=True

@application.route('/')

# enc = lambda x: x.encode('latin1', errors='ignore')

class StdOutListener(StreamListener):

	def on_data(self, data):

		# getting connection with DB
		try:
			cnx = mysql.connector.connect(**config)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		else:
			cnx.close()

		# loading each tweet
		tweet = json.loads(data)

		# validate that user id not null
		if not tweet.has_key('user'):
			print 'No user data - ignoring tweet.'
			return True

		# getting username, tweet content, and geo location for each tweet
		user = tweet['user']['name'].encode('UTF-8')
		text = tweet['text'].encode('UTF-8')
		tweetId = tweet['id_str'].encode('UTF-8')
		location = ''
		if tweet['geo'] != None:
			location = tweet['geo']['coordinates']

		d = dateutil.parser.parse(tweet['created_at'].encode('UTF-8'))

		# localize time
		d_tz = utc.normalize(d)
		localtime = d.astimezone(sgtz)
		tmstr = localtime.strftime("%Y-%m-%d %H:%M:%S")

		# print summary of tweet
		print('%s\n%s\n%s\n%s\n%s\n\n ----------------\n' % (user, tweetId, tmstr, location, text))

		return True

	def on_error(self, status):
		print('status: %s' % status)

 
if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessToken)

	stream = Stream(auth, l, timeout=60)

	print("Listening to filter stream...")

	stream.filter(locations=[-179.99,-89.99,179.99,89.99])
