import os
import pdb
import json
from time import strptime, strftime
from datetime import datetime


def remove_old_users(user_data_jsoned):
	#Currently, users are not being removed from tracker.db.
	#We only want to look at video data given to users from the caches in the past 5 minutes (later just 10 seconds)
	FMT = "%Y-%m-%d %H:%M:%S"
	current_time = strftime("%Y-%m-%d %H:%M:%S")
	new_json_list = []
	
	for user_data in user_data_jsoned:
		single_cache_data = user_data[0]
		old_time = single_cache_data['data']['time']
		
		#returns difference in seconds
		tdelta = datetime.strptime(current_time, FMT) - datetime.strptime(old_time, FMT)
		
		if(tdelta.seconds < 300):
			new_json_list.append(user_data)
	
	return new_json_list
		
	
	
	

def get_user_logs_as_json():
	path_name = os.getcwd()
	print 'path_name is ' + path_name
	path_name = path_name + '/server/user_log/'
	vl = os.listdir(path_name)
	print vl
	data_list = []
	for name in vl:
		path = path_name + name
		print path
		f = open(path,'r')
		user_data_jsoned = json.loads(f.read())
		f.close()
		data_list.append(user_data_jsoned)
	
	user_data = data_list #for testing purposes
	#user_data = remove_old_users(data_list)
	return user_data


#see 
#http://stackoverflow.com/questions/3096953/difference-between-two-time-intervals-in-python
#for how to compare times
#FMT = "%Y-%m-%d %H:%M:%S"
#datetime.strptime(t, FMT)
#current_time = strftime("%Y-%m-%d %H:%M:%S")
#tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT) <-- must be the more recent one first