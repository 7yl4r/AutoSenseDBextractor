#	This script exports all vars to their own csv file
#
#

import sqlite3	#for database access

import exporters

#set up sqlite db stream
FILENAME="db/StressInferencePhone_7thApril_Demo_For_Commercial_Appeal.db"
conn = sqlite3.connect(FILENAME)	#connection
c = conn.cursor()	#cursor

# ================================== OTHER =========================================

#unused tables:
otherTables = ['EMA_metadata',
	'android_metadata',
	'feature_metadata',
	'incentives_metadata',
	'model_metadata',
	'sensor_metadata',
	'ema',
	'incentives'
	]

exporters.exportSensors(c,"output/sensorsOut.csv")
exporters.exportModels(c,"output/modelsOut.csv")
exporters.exportFeatures(c,"output/featuresOut.csv")
