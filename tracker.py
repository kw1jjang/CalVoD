import ast
import sys
import web
import db_manager
import helper #now importing the helper. The helper is storing the ip address of the tracker. we set the value of this
from time import gmtime, strftime
import data_visualization as dv
import json
import urllib2
import pdb
web.config.debug = False
urls = (
    '/', 'overview',
    '/test', 'test',
    '/req/(.*)', 'request',
    '/signup', 'signup',
    '/login', 'login',
    '/logout', 'logout',
    '/user_overview', 'overview',
    '/help', 'help',
)
app = web.application(urls,globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': False,'user_name': None})

#import site
#site.getsitepackages() to find where your site packages are stored
#all of app.run does the following: return wsgi.runwsgi(self.wsgifunc(*middleware))
#wsgifunc takes the *middleware input and makes it readable for runwsgi. aka dont touch this.
#ultimately, app.run() will run:
#return httpserver.runsimple(func, validip(listget(sys.argv, 1, '')))
#So long as fcgi or scgi are not in the command line.

#validip checks if what you entered was a valid ip address (i.e. 1.2.3.4 or 0.0.0.0), and returns a tuple
#with its second value automatically set to 8080. An example of what validip returns is:
#('1.2.3.4', 8080)
#validip will think that 'localhost' is not a valid ip.
#listget takes a list, and index, and a default value.
#for example with (listget(sys.argv,1,'')), it checks if list sys.argv exists,
#if it does, it returns the first index. if it does not, it returns ''.
#runsimple is by default this: def runsimple(func, server_address=("0.0.0.0", 8080)):
#inside of httpserver.py. This is what actually runs our stuff.


render = web.template.render('templates/')
user_population = {}

def log_load():
    # Open log files
    f_log = open('log/user_population.txt', 'a')
    current_time = strftime("%Y-%m-%d %H:%M:%S")
    output_str1 = ' '.join(map(str, user_population.keys()))
    output_str = ' '.join(map(str, user_population.values()))
    f_log.write(current_time + ' ' + output_str1 + ' ' + output_str + '\n')
    f_log.close()

def time_from_timestamp(timestamp):
    (h, m, s) = timestamp.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def get_server_load():
    try:
        f_user = open('server/server_load_user.txt', 'r')
        f_cache = open('server/server_load_cache.txt', 'r')
        f = [f_user, f_cache]
        base_time_stamp = 0
        server_load_user = [0] * 3600 * 24 # 1 Day
        server_load_cache = [0] * 3600 * 24 # 1 Day
        max_time = 0
        ## Server load for users
        while True:
            input_line = f_user.readline()
            if len(input_line) ==0:
                break # EOF
            parsed_str = input_line.split(' ')
            time = time_from_timestamp(parsed_str[1])
            if base_time_stamp == 0:
                base_time_stamp = time
            time -= base_time_stamp
            if time > max_time:
                max_time = time
            server_load_user[time] += int(parsed_str[2])

        ## Server load for caches
        while True:
            input_line = f_cache.readline()
            if len(input_line) ==0:
                break # EOF
            parsed_str = input_line.split(' ')
            time = time_from_timestamp(parsed_str[1])
            if base_time_stamp == 0:
                base_time_stamp = time
            time -= base_time_stamp
            if time > max_time:
                max_time = time
            server_load_cache[time] += int(parsed_str[2])
        f_user.close()
        f_cache.close()
        print '[tracker.py] server_load_user:', server_load_user
        print '[tracker.py] server_load_cache:', server_load_cache
        if False:
            f2 = open('server/server_load_manipulated.txt', 'w')
            for i in range(3600 * 24):
                f2.write(str(i) + ' ' + str(server_load[i])+ '\n')
            f2.close()

        for i in range(max_time + 1):
            server_load_user[i] = float(server_load_user[i]) * 8 / 1000 / 1000
        for i in range(max_time + 1):
            server_load_cache[i] = float(server_load_cache[i]) * 8 / 1000 / 1000

        return [server_load_user[:max_time+1], server_load_cache[:max_time+1]]
    except:
        return [[0], [0]]

class test:
    def GET(self):
        return render.test(server_load_read())

class overview:
    def GET(self):
        #pdb.set_trace()
        if session.get('login', False):
            print 'SUCCESSFULLY DETECTS LOGIN'
            nodes_info = db_manager.get_all_nodes()
            videos_info = db_manager.get_all_videos()
            points = db_manager.get_all_points()
            accounts = db_manager.get_all_accounts()
            account_caches = db_manager.get_all_account_cache()
            nodes_info2 = []
            videos_info2 = []
            points2 = []
            accounts2 = []
            account_cache2 = []

            if session.user_name == 'admin': #admin
                #pdb.set_trace()
                n_nodes = [0, 0, 0] # Server / cache / user

                # Convert 'chunk indexes' to ints
                for each in nodes_info:
                    each.stored_chunks = ast.literal_eval(str(each.stored_chunks))
                    if each.stored_chunks is not None:
                        if len(each.stored_chunks.keys()) == 0:
                            continue
                        for key, val in each.stored_chunks.items():
                            stored_chunk_str = str(val)
                            stored_chunk_list = map(int, ast.literal_eval(stored_chunk_str))
                            val = stored_chunk_list.sort()
                            each.stored_chunks[key] = stored_chunk_list

                # Convert storages to lists
                for each in nodes_info:
                    nodes_info2.append([each.id, str(each.type_of_node), str(each.ip), str(each.port), str(each.watching_video), each.stored_chunks])
                    if str(each.type_of_node) == 'server':
                        n_nodes[0] = n_nodes[0] + 1
                    elif str(each.type_of_node) == 'cache':
                        n_nodes[1] = n_nodes[1] + 1
                    elif str(each.type_of_node) == 'user':
                        n_nodes[2] = n_nodes[2] + 1
                for each in videos_info:
                    videos_info2.append([each.id, str(each.vname), each.n_of_frames, each.code_param_n, each.code_param_k, each.total_size, each.chunk_size, each.last_chunk_size])
                for each in points:
                    points2.append([each.id, str(each.user_name), each.bytes_uploaded, each.points])
                for each in accounts:
                    accounts2.append([each.id, str(each.user_name), str(each.password), str(each.email_address)])
                for each in account_caches:
                    account_cache2.append([each.id, str(each.user_name), str(each.ip), str(each.port)])
                    
                    
                print '[tracker.py] nodes_info ', nodes_info2
                print '[tracker.py] n_nodes ', n_nodes
                print '[tracker.py] videos_info ', videos_info2
                print '[tracker.py] points_info ', points2
                print '[tracker.py] accounts', accounts2
                print '[tracker.py] account_cache', account_cache2
                server_load = get_server_load()
                #pdb.set_trace()
                average_server_load = [sum(server_load[0])/len(server_load[0]), sum(server_load[1])/len(server_load[1])]
                return render.overview(nodes_info2, n_nodes, videos_info2, server_load, average_server_load, points2, accounts2, account_cache2)
            else: #normal user
                num_cache = 0
                for each in points:
                    if each.user_name == session.user_name:
                        points2 = [each.id, str(each.user_name), each.bytes_uploaded, each.points]
                for each in accounts:
                    if each.user_name == session.user_name:
                        accounts2 = [each.id, str(each.user_name), str(each.password), str(each.email_address)]
                for each in account_caches:
                    if each.user_name == session.user_name:
                        num_cache = num_cache + 1
                        account_cache2.append([each.id, str(each.user_name), str(each.ip), str(each.port)])
                return render.user_overview(session.user_name, points2, accounts2, account_cache2, num_cache)
        else:
            raise web.seeother('/login')

class user_overview:
    def GET(self):
        if session.get('login', False):
            nodes_info = db_manager.get_all_nodes()
            points = db_manager.get_all_points()
            accounts = db_manager.get_all_accounts()
            account_caches = db_manager.get_all_account_cache()
            nodes_info2 = []
            points2 = []
            accounts2 = []
            account_cache2 = []
            num_cache = 0
            for each in points:
                if each.user_name == session.user_name:
                    points2 = [each.id, str(each.user_name), each.bytes_uploaded, each.points]
            for each in accounts:
                if each.user_name == session.user_name:
                    accounts2 = [each.id, str(each.user_name), str(each.password), str(each.email_address)]
            for each in account_caches:
                if each.user_name == session.user_name:
                    num_cache = num_cache + 1
                    account_cache2.append([each.id, str(each.user_name), str(each.ip), str(each.port)])
            return render.user_overview(session.user_name, points2, accounts2, account_cache2, num_cache)
        else:
            raise web.seeother('/login')
    
class request:
    def parse_request(self, request_str):
        # REQUEST_COMMAND & ARGUMENT
        valid_req_strings = ['RESET',
                            'GET_SERVER_ADDRESS',
                            'GET_SERVER_ADDRESS_FOR_CACHE',
                            'GET_CACHES_ADDRESS',
                            'GET_ALL_VIDEOS',
                            'UPDATE_CHUNKS_FOR_CACHE',
                            'REGISTER_SERVER',
                            'REGISTER_SERVER_FOR_CACHE',
                            'REGISTER_VIDEO',
                            'REGISTER_USER',
                            'REGISTER_CACHE',
                            'REMOVE_SERVER',
                            'REMOVE_SERVER_FOR_CACHE',
                            'REMOVE_USER',
                            'REMOVE_CACHE',
                            'UPDATE_SERVER_LOAD',
                            'CACHE_DATA_VIS',
                            'CACHE_TO_USER_DATA',
                            'GET_CACHE_DATA',
                            'GET_CACHE_DATA2',
                            'POST_CACHE_DATA']
        req_type = request_str.split('&')[0]
        if len(request_str.split('&')) > 1:
            req_arg = request_str.split('&')[1]
        else:
            req_arg = 0
        req_valid = req_type in valid_req_strings
        return req_valid, req_type, req_arg
    
    def POST(self, request_str):
        req_valid, req_type, req_arg = self.parse_request(request_str)
        if req_type == 'POST_CACHE_DATA':
            data = web.data()
            data = json.loads(data) #data holds a list of all the caches, and the metadata about what they sent
            for cache_metadata in data:
                cache_dict = cache_metadata['data']
                full_address = cache_dict['full_address']
                ip_address = cache_dict['ip_address']
                port = int(cache_dict['port'])
                bytes_uploaded = int(cache_dict['bytes_downloaded'])
                #pdb.set_trace()
                #TODO check what account is associated with this cache
                #check if this account (before accounts added, if this cache) is in the db
                account_name = db_manager.get_account_from_cache(ip_address,str(port))
                account_name = account_name[0].user_name
                if db_manager.get_account_from_points_table(account_name) == []:
                    db_manager.add_account_to_points_table(account_name)
                    db_manager.update_points_for_account(account_name, bytes_uploaded)
                else:
                    db_manager.update_points_for_account(account_name, bytes_uploaded)
            #pdb.set_trace()
            print data
    
    def GET(self, request_str):
        req_valid, req_type, req_arg = self.parse_request(request_str)
        if req_valid == False:
            return 'Invalid request'
        else:
            # REQUEST NODE INFO
            if req_type == 'RESET':
                db_manager.remove_server()
                db_manager.remove_server_for_cache()
                db_manager.remove_all_videos()
                db_manager.remove_all_nodes()
                db_manager.remove_all_caches_from_account_cache()
            elif req_type == 'GET_SERVER_ADDRESS':
                if session.get('login', False):
                    res = db_manager.get_server()
                    return str(res[0].ip) + ' ' + str(res[0].port)
                else:
                    raise web.seeother('/login')
            elif req_type == 'GET_SERVER_ADDRESS_FOR_CACHE':
                if session.get('login', False):
                    print 'get_server_address_for_cache'
                    res = db_manager.get_server_for_cache()
                    return str(res[0].ip) + ' ' + str(res[0].port)
                else:
                    raise web.seeother('/login')
            elif req_type == 'GET_CACHES_ADDRESS':
                if session.get('login', False):
                    # req = "user-hyunah-1 & 10"
                    arg_user_name = req_arg.split('_')[0]
                    arg_num_of_caches = req_arg.split('_')[1]
                    n_of_current_caches = db_manager.get_num_of_caches()
                    n_of_returned_caches = min(n_of_current_caches, int(arg_num_of_caches))
                    print '[tracker.py] n_of_returned_caches', n_of_returned_caches
                    caches = db_manager.get_many_caches(arg_user_name, n_of_returned_caches)
                    ret_str = ''
                    for cache in caches:
                        ret_str = ret_str + str(cache.ip) + ' ' + str(cache.port) + '\n'
                    return ret_str
                else:
                    raise web.seeother('/login')
            # NODE REGISTER
            elif req_type == 'REGISTER_USER':
                if session.get('login', False):
                    # req_arg = "143.243.23.13_324"
                    arg_ip = req_arg.split('_')[0]
                    arg_port = req_arg.split('_')[1]
                    arg_watching_video = req_arg.split('_')[2]
                    db_manager.add_user(arg_ip, arg_port, arg_watching_video)

                    print '[tracker.py] Accessing...'
                    print '[tracker.py] user_pop', user_population
                    user_population[str(arg_watching_video)] += 1
                    log_load()
                    return 'User is registered'
                else:
                    raise web.seeother('/login')
            elif req_type == 'REGISTER_CACHE':
                if session.get('login', False):
                    #pdb.set_trace()
                    arg_ip = req_arg.split('_')[0]
                    arg_port = req_arg.split('_')[1]
                    db_manager.add_cache(arg_ip, arg_port)
                    un = session.user_name
                    db_manager.add_cache_to_account_cache(un, arg_ip, arg_port)
                    return 'Cache is registered'
                else:
                    raise web.seeother('/login')
            elif req_type == 'REGISTER_SERVER':
                #CURRENTLY NO SERVER ACCOUNT BUT WE SHOULD HAVE ONE
                arg_ip = req_arg.split('_')[0]
                arg_port = req_arg.split('_')[1]
                # remove existing server & videos
                db_manager.add_server(arg_ip, arg_port)
                return 'Server is registered'
            elif req_type == 'REGISTER_SERVER_FOR_CACHE':
                #CURRENTLY NO SERVER ACCOUNT BUT WE SHOULD HAVE ONE
                arg_ip = req_arg.split('_')[0]
                arg_port = req_arg.split('_')[1]
                # remove existing server & videos
                db_manager.add_server_for_cache(arg_ip, arg_port)
                return 'Server is registered'
            # VIDEO REGISTER
            elif req_type == 'REGISTER_VIDEO':
                #CURRENTLY NO SERVER ACCOUNT BUT WE SHOULD HAVE ONE
                print 'add video'
                split_arg = req_arg.split('_')
                arg_vname = split_arg[0]
                arg_n_of_frames = split_arg[1]
                arg_code_param_n = split_arg[2]
                arg_code_param_k = split_arg[3]
                arg_total_size = split_arg[4]
                arg_chunk_size = split_arg[5]
                arg_last_chunk_size = split_arg[6]
                db_manager.add_video(arg_vname, arg_n_of_frames, arg_code_param_n, arg_code_param_k, arg_total_size, arg_chunk_size, arg_last_chunk_size)

                if str(arg_vname) not in user_population.keys():
                    user_population[str(arg_vname)] = 0
                    print '[tracker.py] arg_vname', str(arg_vname)
                    print '[tracker.py] user_pop', user_population

                return 'Video is registered'
            elif req_type == 'GET_ALL_VIDEOS':
                #users can still get all videos
                videos = db_manager.get_all_videos()
                ret_str = ''
                for video in videos:
                    ret_str = ret_str + str(video.id) + ' ' + str(video.vname) + ' ' + str(video.n_of_frames) + ' ' + str(video.code_param_n) + ' ' + str(video.code_param_k) + ' ' + str(video.total_size) + ' ' + str(video.chunk_size) + ' ' + str(video.last_chunk_size) + '\n'
                return ret_str
            elif req_type == 'REMOVE_SERVER':
                db_manager.remove_server()
                return 'Server is removed'
            elif req_type == 'REMOVE_SERVER_FOR_CACHE':
                db_manager.remove_server_for_cache()
                return 'Server for cache is removed'
            elif req_type == 'REMOVE_USER':
                arg_ip = req_arg.split('_')[0]
                arg_port = req_arg.split('_')[1]
                arg_watching_video = req_arg.split('_')[2]
                db_manager.remove_user(arg_ip, arg_port, arg_watching_video)

                user_population[str(arg_watching_video)] -= 1
                log_load()

                return 'User is removed'
            elif req_type == 'REMOVE_CACHE':
                arg_ip = req_arg.split('_')[0]
                arg_port = req_arg.split('_')[1]
                db_manager.remove_cache(arg_ip, arg_port)
                #pdb.set_trace()
                un = session.user_name
                #Right now not using username as input, because the server can remove any user it wants.
                #Need to have server logged in as admin for its extra priverlages
                db_manager.remove_cache_from_account_cache(ip=arg_ip, port=arg_port)
                return 'Cache is removed'
            elif req_type == 'UPDATE_CHUNKS_FOR_CACHE':
                arg_ip = req_arg.split('_')[0]
                arg_port = req_arg.split('_')[1]
                arg_vname = req_arg.split('_')[2]
                arg_chunk_str = req_arg.split('_')[3]
                db_manager.add_chunks_for_cache(arg_ip, arg_port, arg_vname, arg_chunk_str)
            elif req_type == 'UPDATE_SERVER_LOAD':
                arg_vname = req_arg.split('_')[0]
                arg_n_of_chks = req_arg.split('_')[1]
                db_manager.add_server_load(arg_vname, arg_n_of_chks)
                
            elif req_type == 'CACHE_DATA_VIS':
                return render.index()
            
            elif req_type == 'CACHE_TO_USER_DATA':
                return render.cache_to_user_data()
            
            elif req_type =='GET_CACHE_DATA':
                web.header('Content-Type', 'application/json')
                user_data = dv.get_user_logs_as_json()
                return json.dumps(user_data)
                #currently reading from file. must later have post request to store data into db
            
            elif req_type =='GET_CACHE_DATA2':
                web.header('Content-Type', 'application/json')
                user_data = dv.get_user_logs_as_json()
                user_data = dv.rearrange_data_for_caches(user_data)
                return json.dumps(user_data)
                #currently reading from file. must later have post request to store data into db

class signup:
    def GET(self):
        return render.signup()

    def POST(self):
        data = web.input() #when not setting ('Content-Type', application/json')
        #data = web.data() from urllib2 sending as json
        user_name = data.inputUserName
        password = data.inputPassword
        email_address = data.inputEmail
        if len(db_manager.get_account(user_name)) == 0:
            db_manager.add_account(user_name, password, email_address)
            session.login = True
            session.user_name= user_name
            raise web.seeother('/user_overview')
        else:
            #raise web.seeother('/signup')
            session.login = False
            return "User name already exist! Login or register with another user name!"

class login: 
    #http://stackoverflow.com/questions/923296/keeping-a-session-in-python-while-making-http-requests
    #http://docs.python-requests.org/en/latest/user/advanced/#session-objects
    #import requests
    #s = requests.Session()
    #r = s.get('http://localhost:8080') will return login page
    #r = s.post('http://localhost:8080/login', data='inputUserName=ryan&inputPassword=11111')
    #s will save the logged in session
    def GET(self):
        #pdb.set_trace()
        return render.login()
    def POST(self):
        #pdb.set_trace()
        #if web.data() != {}:
         #   pdb.set_trace()
        #    data = web.data()
        #    data = json.loads(data)
        #    user_name = data['inputUserName']
        #    password = data['inputPassword']
            #This if statement must be before the web.input() statement.
        if web.input() != {}:
            data = web.input()
            user_name = data.inputUserName
            password = data.inputPassword
        if len(db_manager.get_account(user_name)) == 0:
            session.login = False
            #return "user does not exist!"
            raise web.seeother('/login')
        elif db_manager.get_account(user_name)[0].password == password:
            session.login = True
            session.user_name= user_name
            
            if session.user_name == 'admin':
                raise web.seeother('/')
            else:
                raise web.seeother('/user_overview')
        elif db_manager.get_account(user_name)[0].password != password:
            session.login = False
            #return "wrong username/password combination!"
            raise web.seeother('/login')

class logout:
    def GET(self):
        session.login = False
        raise web.seeother('/login')

class help:
    def GET(self):
        if session.get('login', False):
            return render.help()
        else:
            raise web.seeother('/login')


if __name__ == "__main__":
    print(len(sys.argv))
    print('above was the length')
    if(len(sys.argv) == 1):
        helper.change_tracker_address('0.0.0.0','8080')
    if(len(sys.argv) == 2):
        server_port = sys.argv[1]
        server_address = '0.0.0.0'
        helper.change_tracker_address(server_address, server_port)
        sys.argv[1] = server_address + ':' + server_port
    if(len(sys.argv) == 3):
        if(sys.argv[1] == 'public'):
            sys.argv[1] = urllib2.urlopen('http://icanhazip.com').read().strip('\n')
        server_port = sys.argv[2]
        server_address = sys.argv[1]
        if(web.net.validip6addr(server_address)):
            server_address = '[' + server_address + ']'
        sys.argv[1] = server_address + ':' + server_port
        helper.change_tracker_address(server_address, server_port)
        print sys.argv[1]
    app.run() #takes commandline input of ip_address:port. i.e. 0.0.0.0:8080 on sys.argv[1].
    #tracker.py takes an input of port ip_address. i.e.
    #tracker.py 8080 0.0.0.0 for localhost:8080
