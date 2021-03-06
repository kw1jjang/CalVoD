import web
import ast
import csv
import pdb

# TOPOLOGY_CONFIG
FIXED_TOPOLOGY = False
topology_config_file = 'config/topology_config.csv'

db = web.database(dbn='sqlite', db='tracker.db')

# SERVER
def add_server(input_ip, input_port):
    db.insert('nodes', type_of_node='server', ip=input_ip, port=input_port)

def add_server_for_cache(input_ip, input_port):
    db.insert('nodes', type_of_node='server_for_cache', ip=input_ip, port=input_port)

def remove_server():
    db.delete('nodes', where="type_of_node='server'", vars=locals())

def remove_server_for_cache():
    db.delete('nodes', where="type_of_node='server_for_cache'", vars=locals())

def get_server():
    return db.query("SELECT * FROM nodes WHERE type_of_node='server' ORDER BY RANDOM() LIMIT %d" % 1).list()

def get_server_for_cache():
    return db.select('nodes', where="type_of_node='server_for_cache'", order='id').list()

# VIDEO
def add_video(input_vname, input_n_of_frames, input_code_param_n, input_code_param_k, input_total_size, input_chunk_size, input_last_chunk_size):
    db.insert('videos',
            vname = input_vname,
            n_of_frames = input_n_of_frames,
            code_param_n = input_code_param_n,
            code_param_k = input_code_param_k,
            total_size = input_total_size,
            chunk_size = input_chunk_size,
            last_chunk_size = input_last_chunk_size)

def remove_video(input_vname):
    db.delete('videos', where="vname=$input_vname", vars=locals())

def remove_all_videos():
    db.delete('videos', where="id>=0", vars=locals())

def get_video(input_vname):
    return db.select('videos', where="vname=$input_vname", vars=locals()).list()

def get_all_videos():
    return db.select('videos').list()

def get_num_of_videos():
    results = db.query("SELECT count(*) AS ct FROM videos")
    return results[0].ct

# NODE
def remove_all_nodes():
    db.delete('nodes', where="id>=0", vars=locals())

def get_all_nodes():
    return db.select('nodes').list()

# CACHE
def add_cache(input_ip, input_port):
    db.insert('nodes', type_of_node='cache', ip=input_ip, port=input_port, stored_chunks=str({}))

def add_chunks_for_cache(input_ip, input_port, input_video_name, input_chunks):
    query_result = db.select('nodes', where="type_of_node='cache' AND ip=$input_ip AND port=$input_port", vars=locals()).list()
    chunk_stored = ast.literal_eval(query_result[0].stored_chunks)
    chunk_stored[input_video_name] = input_chunks
    chunk_str_output = str(chunk_stored)
    db.update('nodes', where="ip=$input_ip AND port=$input_port", stored_chunks=chunk_str_output,vars=locals())

def remove_cache(input_ip, input_port):
    db.delete('nodes', where="type_of_node='cache' AND ip=$input_ip AND port=$input_port", vars=locals())

def get_cache(node_id):
    return db.select('nodes', where="type_of_node='cache' AND id=$node_id", order='id', vars=locals()).list()

def get_many_caches(user_name, num_of_caches):
    res = db.query("SELECT * FROM nodes WHERE type_of_node='cache' ORDER BY RANDOM() LIMIT %d" % num_of_caches).list()

    if not FIXED_TOPOLOGY:
        return res
    else:
        f = open(topology_config_file)
        fs = csv.reader(f, delimiter = ' ')
        for row in fs:
            row_user_name = row[0]
            if row_user_name == user_name:
                connectable_caches = map(int, row[1:])
                print '[db_manager.py]', connectable_caches
                break
        res2 = []
        print '[db_manager.py]', res
        for cache in res:
            if int(cache.port) in connectable_caches:
                res2.append(cache)
        return res2

def get_num_of_caches():
    results = db.query("SELECT count(*) AS ct FROM nodes WHERE type_of_node='cache'")
    return results[0].ct

# USER
def add_user(input_ip, input_port, input_watching_video):
    db.insert('nodes', type_of_node='user', ip=input_ip, port=input_port, watching_video=input_watching_video)

def remove_user(input_ip, input_port, input_watching_video):
    db.delete('nodes', where="type_of_node='user' AND ip=$input_ip AND port=$input_port AND watching_video=$input_watching_video", vars=locals())

def get_user(node_id):
    return db.select('nodes', where="type_of_node='user' AND id=$node_id", order='id').list()

def get_num_of_users():
    results = db.query("SELECT count(*) AS ct FROM nodes WHERE type_of_node='user'")
    return results[0].ct

# POINTS
def add_account_to_points_table(user_name):
    #give 100 free points to each new account, for testing & incentive
    db.insert('points', user_name=user_name, bytes_uploaded = 0, points = 100, owned_videos='')
def remove_account_from_points_table(user_name):
    db.delete('points', where="user_name=$user_name", vars=locals())
def get_account_from_points_table(user_name):
    return db.select('points', where="user_name=$user_name", vars=locals()).list()
def update_points_for_account(user_name, bytes_uploaded):
    query_result = db.select('points',where="user_name=$user_name", vars=locals()).list()
    updated_bytes = query_result[0].bytes_uploaded + bytes_uploaded
    float_bytes = float(bytes_uploaded)
    additional_points = float_bytes / 1000000000
    updated_points = query_result[0].points + additional_points
    ##
    db.update('points', where="user_name=$user_name", bytes_uploaded=updated_bytes, points=updated_points, vars=locals())
def get_owned_videos(user_name):
    query_result = db.select('points',where="user_name=$user_name", vars=locals()).list()
    video_list = query_result[0].owned_videos
    ov = video_list.split('_')
    if len(ov) == 1:
        return ''
    else:
        del(ov[0])
        return ov
def update_owned_videos(user_name, video):
    query_result = db.select('points',where="user_name=$user_name", vars=locals()).list()
    owned_videos = query_result[0].owned_videos
    points = query_result[0].points
    if points >= 5:
        points = points - 5
        owned_videos = owned_videos + '_' + video
        db.update('points',where="user_name=$user_name", owned_videos=owned_videos, points=points, vars=locals())
        return points
    else:
        return 'Not enough points'
def remove_all_accounts_from_points_table():
    db.delete('points', where="id>=0", vars=locals())
def get_all_points():
    return db.select('points').list()

#ACCOUNT_CACHE
def add_cache_to_account_cache(user_name, ip, port, multiplier):
    db.insert('account_cache',user_name=user_name, ip=ip, port=port, bytes_uploaded=0, multiplier=multiplier)
def remove_cache_from_account_cache(ip, port, user_name=None):
    db.delete('account_cache', where="ip=$ip AND port=$port", vars=locals())
def get_caches_for_account(user_name):
    return db.select('account_cache', where="user_name=$user_name", order='id', vars=locals()).list()
def get_account_from_cache(ip, port):
    return db.select('account_cache', where="ip=$ip AND port=$port", vars=locals()).list()
def remove_all_caches_from_account_cache():
    db.delete('account_cache', where="id>=0", vars=locals())
def get_all_account_cache():
    return db.select('account_cache', order='id').list()
def update_bytes_for_cache(user_name, ip, port, bytes_uploaded):
    query_result = db.select('account_cache', where="user_name=$user_name AND ip=$ip AND port=$port", vars=locals()).list()
    updated_bytes = query_result[0].bytes_uploaded + bytes_uploaded
    db.update('account_cache', where="user_name=$user_name AND ip=$ip AND port=$port", bytes_uploaded=updated_bytes, vars=locals())

# ACCOUNTS
def add_account(user_name, password, email_address):
    db.insert('accounts', user_name=user_name, password=password, email_address=email_address)
def remove_account(user_name):
    db.delete('accounts', where='user_name=$user_name', vars=locals())
def get_account(user_name):
    return db.select('accounts', where="user_name=$user_name", vars=locals()).list()
def clear_account():
    db.delete('accounts', where="id>=0", vars=locals())
def get_all_accounts():
    return db.select('accounts', order='id').list()
def verify_account(user_name, password):
    return db.select('accounts', where="user_name=$user_name AND password=$password", vars=locals()).list()

# SERVER_LOAD
def add_server_load(input_vname, input_n):
    db.insert('stat', vname=input_vname, n_of_chks=input_n)
