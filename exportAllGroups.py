#	This script exports all vars to a csv file of for their group (sensors/features/models)
#
#

import sqlite3	#for database access

import groupExporters

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

groupExporters.exportSensors(c,"output/sensorsOut.csv")
groupExporters.exportModels(c,"output/modelsOut.csv")
groupExporters.exportFeatures(c,"output/featuresOut.csv")
