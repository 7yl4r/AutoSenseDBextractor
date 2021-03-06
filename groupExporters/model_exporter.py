import datetime	#for converting from unix time to datetime

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


def exportModels(c, fname):
	modelsF = open(fname, 'w')	#output File for models
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

