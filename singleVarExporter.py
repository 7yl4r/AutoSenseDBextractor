import os.path	#for dir checking & creation

# ===================================================================================
# ================================== SENSORS ========================================
# ===================================================================================

#sensors assumed to be of the form:
# _id, start_timestamp, end_timestamp, num_samples, timestamps, samples
sensors = ['sensor11',	#Galvanic Skin Response
	'sensor12',	#Electocardiogram
	'sensor13',	#Body Temperature
	'sensor18',	#Chestband Accelerometer X
	'sensor19',	#Chestband Accelerometer Y
	'sensor20',	#Chestband Accelerometer Z
	'sensor21',	#Respiration
	'sensor22',	#RR intervals from Heart Rate Signal
	'sensor23',	#Latitude from GPS
	'sensor24',	#Longitude from GPS
	'sensor25',	#Speed from GPS
	'sensor95',	#Inhalation (virtual)
	'sensor96',	#Exhalation (virtual)
	'sensor97',	#IE ratio (virtual)
	'sensor98'	#???
	]
sensorNames = ['GSR',
'ECG',
'Body_temp',
'accelX',
'accelY',
'accelZ',
'Respiration',
'RRintervals',
'Latitude',
'Longitude',
'Speed',
'Inhalation',
'Exhalation',
'IE_ratio',
'UNKNOWN_SENSOR']

#params: c = cursor for db; var = variable to output 
def export(c, var):
	varGroup = 'UNKOWN_DATA_GROUP'	#default folder name
	name = var	#default file name
	if (var in sensors):
		varGroup = 'sensors'
		name = sensorNames[sensors.index(var)]
	#TODO: add other elifs
	outDir = 'output/'+varGroup+'/'		#output directory
	if not os.path.exists(outDir):		#ensure output directory exists
		os.makedirs(outDir)
	outF = open(outDir+name+'.csv', 'w')	#output File for var
	#write the header:
	outF.write('timestamp,value\n')

	print 'loading in data for '+var+'\n'

	for row in c.execute("SELECT * FROM " + var + " ORDER BY start_timestamp"):
		nOfSamples = row[3]
		data = str(row[5]).encode('hex')		#row[5] is BLOB of samples
		timestamp = str(row[4]).encode('hex')		#row[4] is BLOB of timestamps
		for i in range(0,nOfSamples):#range(0,len(timestamp)/16):
		#NOTE: len(timestamp)/16 == nOfSamples
			dsize = 8	#int d;
			tsize = 16	#long t;
			dd = int(data[dsize*i:dsize*(i+1)],16)
			tt = long(timestamp[tsize*i:tsize*(i+1)],16)
			outF.write(str(tt) + ',' + str(dd) + '\n')

	outF.close()

import sqlite3	#for database access
#set up sqlite db stream
FILENAME="db/StressInferencePhone_7thApril_Demo_For_Commercial_Appeal.db"
conn = sqlite3.connect(FILENAME)	#connection
c = conn.cursor()	#cursor
export(c,'sensor98')
