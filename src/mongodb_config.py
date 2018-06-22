import pymongo
import sys
# To escape the @ in the Mongo URI
import urllib 
from pprint import pprint
import json

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

def get_mongodb_local_url(config_f='../settings/mongodb_local.txt'):
    try:
        with open(config_f) as f:
            keys_file = json.load(f)
    except  Exception as e:
        print('Problem found opening the file '+config_f+'.')
        print(e)
        sys.exit(1)

    return keys_file

def connect(local=False):
    if not local:
        # Connection to Mongo DB
        mongodb_uri = get_mongodb_uri()
        try:
            #conn = pymongo.MongoClient("mongodb://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test")

            # mongodb+srv://<USERNAME>:<PASSWORD>@contagion100daysofcode-igtzu.mongodb.net/test?retryWrites=true
            atlas_uri = "mongodb+srv://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test?retryWrites=true"
            
            conn = pymongo.MongoClient(atlas_uri)
            
            print("Mongodb connected successfully!!!")
        except pymongo.errors.ConnectionFailure as e:
           print("Could not connect to MongoDB: %s", e)
    else:
        try:
            # MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
            mongodb_dict = get_mongodb_local_url()
            mongodb_url_str = 'mongodb://%s:%s@127.0.0.1'.format(mongodb_dict['user'], mongodb_dict['pwd'])
            conn = pymongo.MongoClient(mongodb_url_str)
            print("Mongodb locally connected successfully!!!")
            print(conn)
        except pymongo.errors.ConnectionFailure as e:
           print("Could not connect to MongoDB: %s", e)
    return conn


def create_db(conn, dbname):
    '''
    Mongodb creates databases and collections automatically for you if they don't exist already.
    A single instance of MongoDB can support multiple independent databases.
    '''
    db = conn[dbname]
    return db


def create_collection(db, collname):
    '''
    A collection is a group of documents stored in MongoDB, and can be thought of as
    roughly the equivalent of a table in a relational database.
    '''
    collection = db[collname]
    return collection


def insert_data(collname, data):
    '''
    To insert some data into MongoDB, all we need to do is create a dict and call .insert() on the collection object:
    '''
    objID = collname.insert(data)
    return objID


# for test purposes
if __name__ == "__main__":

    print(get_mongodb_local_url())


    connect = connect(local=True)
    print(connect)

    db_test = create_db(connect,'test_db')
    print(db_test)

    coll_test = create_collection(db_test, 'coll_test')
    print(coll_test)

    data_json = json.loads('{"test":123}')
    doc = {"name": "Alberto", "surname": "Negron", "twitter": "@Altons"}
    objID = insert_data(coll_test, data_json)
    print(objID)

    all_data = db_test.coll_test.find()
    for data in all_data:
        print(data)


    print('Current databases active: ', connect.database_names())
    print('Current collections active: ', db_test.collection_names())

    #mongodb_uri = get_mongodb_uri()

    #client = pymongo.MongoClient("mongodb+srv://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test")

    # client = pymongo.MongoClient("mongodb://" + urllib.parse.quote(mongodb_uri['username']) + ":" + urllib.parse.quote(mongodb_uri['password']) + "@" + urllib.parse.quote(mongodb_uri['cluster']) + ".mongodb.net/test")
    # db = client.admin
    # serverStatusResult=db.command("serverStatus")
    # pprint(serverStatusResult)
    
