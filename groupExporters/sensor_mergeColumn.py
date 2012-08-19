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
def exportMergedSensors(c, fname):
	sensorsF = open(fname, 'w')	#output File for sensors
	#write the header:
	sensorsF.write('timestamp,\
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
	print 'loading in data from:\n'
	dataList = []
	timeList = []
	for table in sensors:
		tableData = []
		tableTime = []
		for row in c.execute("SELECT * FROM " + table + " ORDER BY start_timestamp"):
			d = []
			t = []
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
				dd = int(hexd, 16)
				tt = long(hext, 16)
				d.append(dd)
				t.append(tt)
			tableData.extend(d)
			tableTime.extend(t)
		dataList.append(tableData)
		timeList.append(tableTime)
		print '=== ' + str(table) + ' ==='
		for column in c.description:
			print str(column[0])
	print '\nmerging data at:'
	#TODO: these should be chosen more cleverly:
	currentTime = timeList[0][0]-1000	#start time is time of first in list
	endTime = timeList[0][len(timeList[0])-1]+1000	#end time is last in list + 1k
	deltaTime = 5*100	#amount of time between points (.5s)
	i = 0	#start going through times at begginning (assume sorted)
	startI = [0]*15	#array of last looked at times
	while(currentTime < endTime):	#iterate between earliest and latest times
		print '\ttime: ' + str(currentTime)
		#get values for all vars at/near current time
		value = [-1]*15
		for var in range(0,15):		#iterate over all the sensors
			endI = len(timeList[var])
			for i in range(startI[var],endI):		#iterate through all samples in the sensor
				dTime = abs(timeList[var][i] - currentTime)
				if dTime < abs(timeList[var][i+1] - currentTime):	#if this time is closer to the window than the next time
					#then this the closest time
					if dTime < deltaTime/2:		#check if the time is within the window					
						value[var] = dataList[var][i]
					else: 	#point is not close enough, value should be...??? (maybe write dTimes to another file?)
						value[var] = dataList[var][i]
					startI[var] = i-1
					break	#skip to next sensor
			if value[var] == -1:	#if no acceptable time for the sensor was found
				value[var] = dataList[var][0]		#set this to the first time???
		#write values & time to file
		sensorsF.write(str(currentTime)+',')
		for val in value:	#write values
			sensorsF.write(str(val) + ',')
		sensorsF.seek(sensorsF.tell()-1,0);	#go back one to overwrite the last comma
		sensorsF.write('\n');	

		#move to next time window
		currentTime = currentTime + deltaTime	#move to next time

	sensorsF.close()

#newyorkyankeescaptainthurmanmunson15
