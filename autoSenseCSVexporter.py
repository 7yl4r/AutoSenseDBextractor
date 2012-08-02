import sqlite3	#for database access
import datetime	#for converting from unix time to datetime

import struct #for interpreting binary blobs in db

#set up sqlite db stream
FILENAME="./StressInferencePhone_7thApril_Demo_For_Commercial_Appeal.db"
conn = sqlite3.connect(FILENAME)	#connection
c = conn.cursor()	#cursor

# ===================================================================================
# ================================== MODELS =========================================
# ===================================================================================
#models assumed to be of the form:
# _id, start_timestamp, end_timestamp, value
models = ['model1',
	'model2',
	'model4',
	'model5'
	]
modelLabels = ['Physical_Activity_and_Posture(0:sit|1:stand|2:walk)',
	'Stress(0:Not_stressed|1:Stressed|-1:Unknown/Timed)',
	'ECG_Data_Quality(0:Off|-2:Loose|-1:Noisy|1:Good)',	#model4 part 1
	'RIP_Data_Quality(0:Off|-2:Loose|-1:Noisy|1:Good)',	#model4 part 2
	'Conversation_Level(0:Quiet|1:Smoking|2:Speaking)'
	]

#this function reads in the value of a model and the model name and returns a 'mapped to a more vizualization-friendly' value
def modelsValueMap(tableName, valueToConvert):
	if(tableName == 'model1'):
		dictionary = {'0':'0, , , , ',
			'1':'1, , , , ',
			'2':'2, , , , '
		}
	elif(tableName == 'model2'):
		dictionary = {'1':' ,0, , , ',
			'2':' ,1, , , ',
			'3':' ,-1, , , '
		}
	elif(tableName == 'model4'):
		dictionary = {'0':' , ,1,1, ',
			 '1':' , ,-1,1, ',
			 '2':' , ,-2,1, ',
			 '3':' , ,0,1, ',
			'10':' , ,1,-1, ',
			'11':' , ,-1,-1, ',
			'12':' , ,-2,-1, ',
			'13':' , ,0,-1, ',
			'20':' , ,-2,-2, ',
			'21':' , ,-1,-2, ',
			'22':' , ,-2,-2, ',
			'23':' , ,0,-2, ',
			'30':' , ,0,0, ',
			'31':' , ,-1,0, ',
			'32':' , ,-2,0, ',
			'33':' , ,0,0, '
			}
	elif(tableName == 'model5'):	#TODO: perhaps smoking/notsmoking should be segmented into its own column
		dictionary = {'0':' , , , ,0',
			'1':' , , , ,2',
			'2':' , , , ,1'
		}
	else:
		return ' , , , , , , , , , ,'+str(valueToConvert)
	return dictionary[' '.join(str(valueToConvert).split())]

#this function is used to return the text specified in model_metadata from the value passed
def modelsMeta(tableName, valueToConvert):
	if(tableName == 'model1'):
		dictionary = {'0':'Sit, , , , ',
			'1':'Stand, , , , ',
			'2':'Walk, , , , '
		}
	elif(tableName == 'model2'):
		dictionary = {'1':' ,Not_Stressed, , , ',
			'2':' ,Stressed, , , ',
			'3':' ,Unknown/Timed, , , '
		}
	elif(tableName == 'model4'):
		dictionary = {'0':' , ,ECG_good,RIP_Good, ',
			 '1':' , ,ECG_Noisy,RIP_Good, ',
			 '2':' , ,ECG_Loose,RIP_Good, ',
			 '3':' , ,ECG_Off,RIP_Good, ',
			'10':' , ,ECG_Good,RIP_Noisy, ',
			'11':' , ,ECG_Noisy,RIP_Noisy, ',
			'12':' , ,ECG_Loose,RIP_Noisy, ',
			'13':' , ,ECG_Off,RIP_Noisy, ',
			'20':' , ,ECG_Loose,RIP_Loose, ',
			'21':' , ,ECG_Noisy,RIP_Loose, ',
			'22':' , ,ECG_Loose,RIP_Loose, ',
			'23':' , ,ECG_Off,RIP_Loose, ',
			'30':' , ,ECG_Off,RIP_Off, ',
			'31':' , ,ECG_Noisy,RIP_Off, ',
			'32':' , ,ECG_Loose,RIP_Off, ',
			'33':' , ,ECG_Off,RIP_Off, '
			}
	elif(tableName == 'model5'):	#TODO: perhaps smoking/notsmoking should be segmented into its own column
		dictionary = {'0':' , , , ,Quiet',
			'1':' , , , ,Speaking',
			'2':' , , , ,Smoking'
		}
	else:
		return ' , , , , , , , , , ,'+str(valueToConvert)
	return dictionary[' '.join(str(valueToConvert).split())]

modelsF = open(FILENAME+"_models.csv", 'w')	#output File for models
#the following header is correct for data mapped using the defined modelsValueMap() function and IS NOT consistent with metaData tables
modelsF.write('_id,\
start_timestamp,\
end_timestamp,\
midTime,')
for label in modelLabels:	#write headers
	modelsF.write(str(label) + ',')
modelsF.seek(modelsF.tell()-1,0);	#go back one to overwrite the last comma
modelsF.write('\n');
#Physical_Activity_and_Posture(0:sit|1:stand|2:walk),\
#Stress(0:Not_stressed|1:Stressed|-1:Unknown/Timed),\
#ECG_Data_Quality(0:Off|-2:Loose|-1:Noisy|1:Good),\
#RIP_Data_Quality(0:Off|-2:Loose|-1:Noisy|1:Good),\
#Conversation_Level(0:Quiet|1:Smoking|2:Speaking)\n')
for table in models:
	for row in c.execute("SELECT * FROM " + table): # + " ORDER BY start_timestamp):
		midTime= datetime.datetime.fromtimestamp(int((row[1]+(row[1]-row[2])/2)/1000.0)).strftime('%m/%d/%Y %H:%M:%S')	#calculate time for point (middle of read time) ((divide by 1000.0 to convert from ms to s))
		#value = row[3]				#use this for unmapped (matching metadata tables) outputs
		#value = modelsMeta(table,row[3])	#use this for text outputs
		value = modelsValueMap(table,row[3])	#use this for Mapped numerical outputs
		#modelsF.write(str(row)+'\n')
		modelsF.write(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',')
		modelsF.write(str(midTime)+','+str(value)+'\n')
		#print str(row.keys())
	print '=== ' + str(table) + ' ==='
	for column in c.description:
		print str(column[0])
modelsF.close()

# ===================================================================================
# ================================== SENSORS ========================================
# ===================================================================================
def sensorsMap(tableName, valueToConvert):
	if(tableName == 'sensor11'):
		return '' + str(valueToConvert) + ', , , , , , , , , , , , , , '
	elif(tableName == 'sensor12'):
		return ' ,' + str(valueToConvert) + ', , , , , , , , , , , , , '
	elif(tableName == 'sensor13'):
		return ' , ,' + str(valueToConvert) + ', , , , , , , , , , , , '
	elif(tableName == 'sensor18'):
		return ' , , ,' + str(valueToConvert) + ', , , , , , , , , , , '
	elif(tableName == 'sensor19'):
		return ' , , , ,' + str(valueToConvert) + ', , , , , , , , , , '
	elif(tableName == 'sensor20'):
		return ' , , , , ,' + str(valueToConvert) + ', , , , , , , , , '
	elif(tableName == 'sensor21'):
		return ' , , , , , ,' + str(valueToConvert) + ', , , , , , , , '
	elif(tableName == 'sensor22'):
		return ' , , , , , , ,' + str(valueToConvert) + ', , , , , , , '
	elif(tableName == 'sensor23'):
		return ' , , , , , , , ,' + str(valueToConvert) + ', , , , , , '
	elif(tableName == 'sensor24'):
		return ' , , , , , , , , ,' + str(valueToConvert) + ', , , , , '
	elif(tableName == 'sensor25'):
		return ' , , , , , , , , , ,' + str(valueToConvert) + ', , , , '
	elif(tableName == 'sensor95'):
		return ' , , , , , , , , , , ,' + str(valueToConvert) + ', , , '
	elif(tableName == 'sensor96'):
		return ' , , , , , , , , , , , ,' + str(valueToConvert) + ', , '
	elif(tableName == 'sensor97'):
		return ' , , , , , , , , , , , , ,' + str(valueToConvert) + ', '
	elif(tableName == 'sensor98'):
		return ' , , , , , , , , , , , , , ,' + str(valueToConvert) + ''
	else:
		return ' , , , , , , , , , , , , , , ,!!,' + str(valueToConvert)


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
sensorsF = open(FILENAME+"_sensors.csv", 'w')	#output File for sensors
#write the header:
sensorsF.write('sampleGroupID,\
sampleID/samplesInGroup,\
timestamp,\
GSR,\
ECG,\
Body_temp,\
accelX,\
accelY,\
accelZ,\
Respiration,\
RRintervals,\
Latitude,\
Longitude,\
Speed,\
Inhalation,\
Exhalation,\
IE_ratio,\
UNKNOWN_SENSOR\n')
for table in sensors:
	for row in c.execute("SELECT * FROM " + table): # + " ORDER BY start_timestamp):
		#startTime = row[1]/1000
		#endTime = row[2]/1000
		#midTime= datetime.datetime.fromtimestamp(int((startTime+(startTime-endTime)/2)/1000.0)).strftime('%m/%d/%Y %H:%M:%S')	#calculate time for point (middle of read time) ((divide by 1000.0 to convert from ms to s))
		groupID = row[0]
		nOfSamples = row[3]

		# raw data
		dat = str(row[5])
		data = dat.encode('hex')		#row[5] is BLOB of samples
		tim = str(row[4])
		timestamp = tim.encode('hex')		#row[4] is BLOB of timestamps
		

		for i in range(0,nOfSamples):#range(0,len(timestamp)/16):
		#NOTE: len(timestamp)/16 == nOfSamples
			dsize = 8	#int d;
			tsize = 16	#long t;
			hexd = data[dsize*i:dsize*(i+1)]
			hext = timestamp[tsize*i:tsize*(i+1)]
			d = int(hexd, 16)
			t = long(hext, 16)
		#	print tim[16*i:16*(i+1)] + '=' + str(hext) + '=' + str(t) + '\n'
		#	print dat[8*i:8*(i+1)] + '=' + str(hexd) + '=' + str(d) + '\n'
					
			# "unix time,sample"
			if (d != 4626):		#TODO: why is this the default value???
				sensorsF.write(str(groupID) + ',' + str(i+1) + '/' + str(nOfSamples) + ',')
				sensorsF.write(str(t) + ',' + sensorsMap(table, d) + '\n')
			#else don't write it

	print '=== ' + str(table) + ' ==='
	for column in c.description:
		print str(column[0])
sensorsF.close()

# ===================================================================================
# ================================== FEATURES =======================================
# ===================================================================================
#features assumed to be of the form:
# _id, start_timestamp, end_timestamp, value
features = ['feature10921',
	'feature11012',
	'feature11018',
	'feature11019',
	'feature11021',
	'feature11023',
	'feature11024',
	'feature11025',
	'feature11098',
	'feature11111',
	'feature11113',
	'feature11120',
	'feature11211',
	'feature11212',
	'feature11213',
	'feature11222',
	'feature11295',
	'feature11296',
	'feature11297',
	'feature11411',
	'feature11413',
	'feature11422',
	'feature11520',
	'feature11711',
	'feature11713',
	'feature11722',
	'feature11795',
	'feature11796',
	'feature11797',
	'feature11895',
	'feature11896',
	'feature11897',
	'feature11921',
	'feature12122',
	'feature12222',
	'feature12422',
	'feature12522',
	'feature12622',
	'feature12722',
	'feature12822'
	]

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

