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

featureNames = ['feature10921',
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
	'feature12822']

# ===================================================================================
# ================================== MODELS =========================================
# ===================================================================================
#models assumed to be of the form:
# _id, start_timestamp, end_timestamp, value
models = ['model1',
	'model2',
	'model4',
	'model5']
modelNames = ['Physical_Activity_and_Posture',
	'Stress',
	'ECG&RIP_Data_Quality',
	'Conversation_Level']

# ===================================================================================
# ================================== OTHER =========================================
# ===================================================================================

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
