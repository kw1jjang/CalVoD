import os
import pdb

def get_user_logs():
	path_name = os.getcwd()
	print 'path_name is ' + path_name
	path_name = path_name + '/server/user_log/'
	vl = os.listdir(path_name)
	h = path_name.join(vl)
	print vl
	pdb.set_trace()
	return h

	
