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
		
		if(tdelta.seconds < 60):
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
		#print path
		f = open(path,'r')
		user_data_jsoned = json.loads(f.read())
		f.close()
		data_list.append(user_data_jsoned)
	
	#user_data = data_list #for static testing purposes when only wanting to run the tracker
	user_data = remove_old_users(data_list)
	return user_data

def rearrange_data_for_caches(user_data):
	cache_name_list = [];
	cache_name_dict = [];
	for user in user_data:
		for cache in user:
			if cache['data']['full_address'] not in cache_name_list:
				#If we have never seen this cache before, add it to a list of caches
				#Initialize the dictionary of its information for below
				cache_name_list.append(cache['data']['full_address'])
				temp_dict = {}
				temp_dict['cache'] = {}
				cache_name_dict.append(temp_dict)
				index_of_dict = cache_name_list.index(cache['data']['full_address'])
				#pdb.set_trace()
				cache_name_dict[index_of_dict]['cache']['full_address'] = cache['data']['full_address']
				cache_name_dict[index_of_dict]['cache']['contents'] = []
			i = cache_name_list.index(cache['data']['full_address'])
			info_dict = {}
			info_dict['data'] = {}
			info_dict['data']['full_address'] = cache['data']['full_address']
			info_dict['data']['user_name'] = cache['data']['user_name']
			info_dict['data']['bytes_sent'] = cache['data']['bytes_downloaded']
			info_dict['data']['number_of_chunks'] = cache['data']['number_of_chunks']
			info_dict['data']['chunks'] = cache['data']['chunks']
			#Store only video name. Not video name + chunk number
			info_dict['data']['video_name'] = cache['data']['video_name'].split('.')[0]
			cache_name_dict[i]['cache']['contents'].append(info_dict)
	
	return cache_name_dict



#see 
#http://stackoverflow.com/questions/3096953/difference-between-two-time-intervals-in-python
#for how to compare times
#FMT = "%Y-%m-%d %H:%M:%S"
#datetime.strptime(t, FMT)
#current_time = strftime("%Y-%m-%d %H:%M:%S")
#tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT) <-- must be the more recent one first