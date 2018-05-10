import pymongo
import sys
# To escape the @ in the Mongo URI
import urllib 
from pprint import pprint

def get_mongodb_uri(config_f='../settings/mongodb.txt'):
	try:
		keys_file = open(config_f)
		lines = keys_file.readlines()
	except Exception as e:
		print('Problem found opening the file '+config_f+'.')
		print(e)
		sys.exit(1)
	try:
		username = lines[0].rstrip().split('=')[1]
		password = lines[1].rstrip().split('=')[1]
		cluster = lines[2].rstrip().split('=')[1]
	except Exception as e:
		print('Problem processing the file '+config_f+'.')
		print(e)
		sys.exit(1)

	return {'username':username, 
			'password':password, 
			'cluster':cluster
			}

mongodb_uri = get_mongodb_uri()

#client = pymongo.MongoClient("mongodb+srv://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test")

client = pymongo.MongoClient("mongodb://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test")
db = client.admin

serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)