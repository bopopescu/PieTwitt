import flask
import json
import dateutil.parser
from pytz import timezone
import pytz

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
application = flask.Flask(__name__)

#Set application.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
application.debug=True
 
consumerKey = 'f2gQNjXOIwXNnzaNVboNLB7zy'
consumerSecret = 'DlPdIXIkwgCGZLp0IUjU5418a9txJrp27qKsGovZh9iumcXyYy'
accessKey = '3064523805-j1pUg9xKiL6GG4aOLrMrCNbq6rFGNk7auVprzm4'
accessToken = 'sIufLPBNv8WiQ1zzcp6jmOgkOkZ5csk79GJ9L46H3lh7K'

sgtz = timezone('US/Eastern')
utc = pytz.timezone('UTC')

@application.route('/')

# enc = lambda x: x.encode('latin1', errors='ignore')

class StdOutListener(StreamListener):

	def on_data(self, data):

		tweet = json.loads(data)

		if not tweet.has_key('user'):
			print 'No user data - ignoring tweet.'
			return True

		# getting username, tweet content, and geo location for each tweet
		user = tweet['user']['name'].encode('UTF-8')
		text = tweet['text'].encode('UTF-8')
		location = ''
		if tweet['geo'] != None:
			location = tweet['geo']['coordinates']

		d = dateutil.parser.parse(tweet['created_at'].encode('UTF-8'))

		# localize time
		d_tz = utc.normalize(d)
		localtime = d.astimezone(sgtz)
		tmstr = localtime.strftime("%Y%m%d-%H:%M:%S")

		print('%s\n%s\n%s\n%s\n\n ----------------\n' % (user, location, tmstr, text))




		return True

	def on_error(self, status):
		print(status)	

 
if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessToken)

	stream = Stream(auth, l)
	stream.filter(locations=[-180,-90,180,90])
