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

#params: c = cursor for db; fname = output filename 
def exportSensors(c, fname):
	sensorsF = open(fname, 'w')	#output File for sensors
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
