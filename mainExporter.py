import sqlite3	#for database access

import sensor_exporter
import model_exporter
import feature_exporter

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

sensor_exporter.exportSensors(c,"output/sensorsOut.csv")
model_exporter.exportModels(c,"output/modelsOut.csv")
feature_exporter.exportFeatures(c,"output/featuresOut.csv")
