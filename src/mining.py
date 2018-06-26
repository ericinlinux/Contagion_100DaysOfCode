
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import sys
import csv
import json

from twitter_config import get_auth_api
import mongodb_config as mdb


# def fix_text(text):
# 	'''
# 	To correct the problem with: 'ascii' codec can't encode character
# 	'''
# 	return u''.text.encode('utf-8').strip()

def get_queries(queries_f='../settings/queries.txt'):
	'''
	Read the file with the keys for Twitter API and return a dictionary with them.
	'''
	try:
		queries_file = open(queries_f)
		queries = queries_file.readlines()
		# Clean \n
		queries = [query.rstrip() for query in queries]
	except Exception as e:
		print('Problem found opening the file '+config_f+'.')
		print(e)
		sys.exit(1)
	
	return queries

# Create a streamer object
class StdOutListener(StreamListener):
	
	# Define a function that is initialized when the miner is called
	def __init__(self, api = None):
		# That sets the api
		self.api = api
		
		self.connect_db = mdb.connect(local=True)
		self.db = mdb.create_db(self.connect_db,'Tweets_100DaysofCode')

		# Create a file with 'data_' and the current time
		# self.filename = 'data'+'_'+time.strftime('%Y%m%d-%H%M%S')+'.jsonl'
		
		# Here it should be the MongoDB set up...

		
		'''
		csvWriter.writerow(['text',
							'created_at',
							'geo',
							'lang',
							'place',
							'coordinates',
							'user.favourites_count',
							'user.statuses_count',
							'user.description',
							'user.location',
							'user.id',
							'user.created_at',
							'user.verified',
							'user.following',
							'user.url',
							'user.listed_count',
							'user.followers_count',
							'user.default_profile_image',
							'user.utc_offset',
							'user.friends_count',
							'user.default_profile',
							'user.name',
							'user.lang',
							'user.screen_name',
							'user.geo_enabled',
							'user.profile_background_color',
							'user.profile_image_url',
							'user.time_zone',
							'id',
							'favorite_count',
							'retweeted',
							'source',
							'favorited',
							'retweet_count'])
		'''

	def on_data(self, data):
		try:
			#with open('../data/python.json', 'a') as f:
			#	f.write(data)
			data_json = json.loads(data)
			#print(data)
			print(data_json['created_at'])
			collection_name = 'tweets'+'_'+time.strftime('%Y%m%d')
			collection = mdb.create_collection(self.db, collection_name)
			print(mdb.insert_data(collection, data_json))
			return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	# # When a tweet appears
	# def on_status(self, status):
		
	# 	# Open the csv file created previously
	# 	csvFile = open(self.filename, 'a')
		
	# 	# Create a csv writer
	# 	csvWriter = csv.writer(csvFile)
		
	# 	# If the tweet is not a retweet
	# 	if not 'RT @' in status.text:
	# 		# Try to 
	# 		try:
	# 			# Write the tweet's information to the csv file
	# 			csvWriter.writerow([clean_text(status.text),
	# 								status.created_at,
	# 								status.geo,
	# 								status.lang,
	# 								status.place,
	# 								status.coordinates,
	# 								status.user.favourites_count,
	# 								status.user.statuses_count,
	# 								status.user.description,
	# 								status.user.location,
	# 								status.user.id,
	# 								status.user.created_at,
	# 								status.user.verified,
	# 								status.user.following,
	# 								status.user.url,
	# 								status.user.listed_count,
	# 								status.user.followers_count,
	# 								status.user.default_profile_image,
	# 								status.user.utc_offset,
	# 								status.user.friends_count,
	# 								status.user.default_profile,
	# 								status.user.name,
	# 								status.user.lang,
	# 								status.user.screen_name,
	# 								status.user.geo_enabled,
	# 								status.user.profile_background_color,
	# 								status.user.profile_image_url,
	# 								status.user.time_zone,
	# 								status.id,
	# 								status.favorite_count,
	# 								status.retweeted,
	# 								status.source,
	# 								status.favorited,
	# 								status.retweet_count])
	# 		# If some error occurs
	# 		except Exception as e:
	# 			# Print the error
	# 			print(e)
	# 			# and continue
	# 			pass
			
	# 	# Close the csv file
	# 	csvFile.close()

	# 	# Return nothing
	# 	return

	# When an error occurs
	def on_error(self, status_code):
		# Print the error code
		print('Encountered error with status code:', status_code)
		
		# If the error code is 401, which is the error for bad credentials
		if status_code == 401:
			# End the stream
			return False

	# When a deleted tweet appears
	def on_delete(self, status_id, user_id):
		
		# Print message
		print("Delete notice")
		
		# Return nothing
		return

	# When reach the rate limit
	def on_limit(self, track):
		
		# Print rate limiting error
		print("Rate limited, continuing")
		
		# Continue mining tweets
		return True

	# When timed out
	def on_timeout(self):
		
		# Print timeout message
		print(sys.stderr, 'Timeout...')
		
		# Wait 10 seconds
		time.sleep(10)
		
		# Return nothing
		return


# Create a mining function
def start_mining(queries=None):
	'''
	Inputs list of strings. Returns tweets containing those strings.
	'''
	if queries is None:
		queries = get_queries()

	# Create a listener
	l = StdOutListener()
	
	auth = get_auth_api()[0]
	
	# Create a stream object with listener and authorization
	stream = Stream(auth, l)

	# Run the stream object using the user defined queries
	stream.filter(track=queries)


# for test purposes
if __name__ == "__main__":
	#start_mining(['python', '#Python'])
	start_mining()

