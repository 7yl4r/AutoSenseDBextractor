import sqlite3	#for database access

def midTime(res, i):	#retuns midTime in res for row i, assuming start_time in 2nd column, end_time in 3rd
	return (res[1][i]+res[2][i])/2

#set up sqlite db stream
FILENAME="db/StressInferencePhone_7thApril_Demo_For_Commercial_Appeal.db"
conn = sqlite3.connect(FILENAME)	#connection
c = conn.cursor()	#cursor

table = "model1"
result = c.execute("SELECT * FROM model1 ORDER BY start_timestamp")

#get start time
currentTime = midTime(result,0)	#1st time is midTime of first in list

#get values for all vars at/near current time
i = 0
while(1){
	if abs(midTime(result,i) - currentTime) < abs(midTime(result,i+1) - currentTime):	#if this time is closer to the window than the next time
		value = result[3][i]
		break
	else i = i + 1
}

#write values & time to file


#move to next time window
