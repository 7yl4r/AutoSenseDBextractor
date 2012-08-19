#	This script exports all vars to their own csv file
#
#

import sqlite3	#for database access

import varList
import singleVarExporter

#set up sqlite db stream
FILENAME="db/StressInferencePhone_7thApril_Demo_For_Commercial_Appeal.db"
conn = sqlite3.connect(FILENAME)	#connection
c = conn.cursor()	#cursor

for sensor in varList.sensors:
	singleVarExporter.export(c,sensor)
