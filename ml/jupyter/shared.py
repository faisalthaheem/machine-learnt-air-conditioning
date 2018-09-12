import pymongo as mongo
import pprint
import time
from pandas import DataFrame
import os

def test():
	mongoClient = mongo.MongoClient(os.environ['mongodbhost'], 27017)
	db = mongoClient.admin
	collection = db.sensors
	composite = collection.find_one({"source":"composite", "day":26, "hour":10})
	pprint.pprint(composite)

def getData(forDays, dropExtraCols=True):

	# subtract forDays in terms of seconds from now
	now = int(time.time()) * 1000
	timeToSubtract = int(forDays * 24 * 60 * 60 * 1000)
	effective_time = now - timeToSubtract
	print("now:", now)
	print("timeToSubtract:",timeToSubtract)
	print("effective_time :", effective_time)
	
	mongoClient = mongo.MongoClient(os.environ['mongodbhost'], 27017)
	db = mongoClient.admin
	sensorDataCollection = db.sensors
	sensorData = sensorDataCollection.find({"source":"composite", "unixtime" : {"$gte":effective_time} }).sort([("timestamp",mongo.DESCENDING)])

	#temporary to hold data
	sensorDataArray = []

	#populate temp 
	for dataRow in sensorData:
		if len(dataRow) is 17:
			sensorDataArray.append(dataRow)
		else:
			print("bad data", dataRow)
	
	#create df
	df = DataFrame.from_dict(sensorDataArray)

	#drop unnecessary cols
	if dropExtraCols:
		df = df.drop(['_id','timestamp','unixtime','source'], axis = 1)

	return df
