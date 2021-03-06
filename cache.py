from streamer import StreamFTP
from threadclient import *
from server import *
from pyftpdlib import ftpserver
import os
import Queue
import random
import csv
import time
from time import gmtime, strftime
import threading
import resource
import sys
from helper import *
import urllib2
import requests #used for handling the cache session (associate this cache with a logged in account to tracker)

import pdb #remove all pdb.set_trace() to make it run continuously

# Debugging MSG
DEBUGGING_MSG = False
DEBUG_FULL = False
# Algorithm DEBUGGING
POSITIVE_CONSTRAINT = True

# Cache Configuration
cache_config_file = '../../config/cache_config.csv'

# Log Configuration
LOG_PERIOD = 1000

INFINITY = 10e10
MAX_CONNS = 10000
MAX_VIDEOS = 1000
BUFFER_LENGTH = 10
path = "."
tracker_address = load_tracker_address() # set in helper.

# CACHE RESOURCE
BANDWIDTH_CAP = 12800 #(Kbps), equal to 12.8 Megabytes
STORAGE_CAP_IN_MB = 1500 #Megabytes, equal to 1.5 Gigabytes
T_rate = .1
T_storage = 1
T_topology = 600
STORAGE_UPDATE_PERIOD_OUTER = 1

# IP Table
class ThreadStreamFTPServer(StreamFTPServer, threading.Thread):
    """
        A threaded server. Requires a Handler.
    """
    def __init__(self, address, handler, spec_rate=0):
        StreamFTPServer.__init__(self, address, handler, spec_rate)
        threading.Thread.__init__(self)

    def run(self):
        self.serve_forever()

    def get_conns(self):
        return self.conns

    def get_handlers(self):
        #print '[cache.py] self.handlers = ', self.handlers
        return self.handlers

class Cache(object):
    """
    Manages the cache as a whole. Has 3 main functions:
    -Opens up an FTP mini-server (CacheServer) in one thread.
    -Opens up a connection to the actual server (ServerDownloader) in a thread.
    -Every <timestep> check to see if cache is properly serving user-needs.
    If not, use ServerDownloader to request different chunks from the server.
    """

    def __init__(self, cache_config):
        """Make the FTP server instance and the Cache Downloader instance.
        Obtain the queue of data from the FTP server."""
        #config = [1, '0.0.0.0', str(60000+int(sys.argv[1])), sys.argv[2], 15000000, session, multiplier]
        self.packet_size = 2504
        session = cache_config[5]
        server_ip_address = get_server_address(tracker_address, session)
        self.server_client = ThreadClient(self, server_ip_address, self.packet_size)
        inst_SENDPORT = 'SENDPORT '
        if DEBUG_FULL:
            pdb.set_trace()
        self.server_client.put_instruction(inst_SENDPORT + cache_config[2] + ' ' + cache_config[3] +' cache')
        self.server_client.set_respond_RETR(True)

        self.cache_id = cache_id = int(cache_config[0])
        self.address = (cache_config[1], int(cache_config[2]))
        self.public_address = cache_config[3]
        register_to_tracker_as_cache(tracker_address, self.public_address, self.address[1], cache_config[6], session)
        stream_rate = int(cache_config[4])

        if True:
            # Variables for algorithms
            average_streaming_rate = 3000 # Kbps
            average_length = 120 # sec

            scale = 3
            self.eps_x = 1 * scale
            self.eps_k = 1 * scale
            self.eps_la = .3 * scale
            self.eps_f = .001 * scale
            self.eps_mu = .0000001 * scale

            print '[cache.py] EPS'
            print '[cache.py] eps_x ', self.eps_x
            print '[cache.py] eps_f ', self.eps_f
            print '[cache.py] eps_k ', self.eps_k
            print '[cache.py] eps_la ', self.eps_la
            print '[cache.py] eps_mu ', self.eps_mu
        else:
            # Variables for algorithms
            eps = .01
            average_streaming_rate = 3000 # Kbps
            average_length = 120 # sec
            self.eps_x = eps * 100
            self.eps_f = eps / 500 / 8
            self.eps_la = eps / 100
            self.eps_mu = eps / pow(average_length, 2) / 10
            self.eps_k = eps

        self.bandwidth_cap = BANDWIDTH_CAP * cache_config[6] # (Kbps)
        self.storage_cap_in_MB = STORAGE_CAP_IN_MB * cache_config[6] # (MB)
        self.storage_cap = self.storage_cap_in_MB * 1000 * 1000 # (Bytes)

        self.dual_la = 0 # dual variable for BW
        self.dual_mu = 0 # dual variable for ST

        self.primal_x = [0] * MAX_CONNS
        self.primal_f = {}
        self.dual_k = [0] * MAX_CONNS

        self.sum_rate = 0
        self.sum_storage = 0

        self.authorizer = ftpserver.DummyAuthorizer()
        self.authorizer.add_anonymous(path, perm='elr') # allow anonymous login.
        handler = CacheHandler
        handler.parentCache = self
        handler.authorizer = self.authorizer
        self.movie_LUT = retrieve_MovieLUT_from_tracker(tracker_address)
        handler.movie_LUT = self.movie_LUT
        handler.passive_ports = range(60000, 65535)

        # set public.
        handler.masquerade_address = self.public_address
        handler.id_to_index = {} # Dictionary from ID to index
        handler.rates = [0] * MAX_CONNS # in chunks per frame
        handler.chunks = {}
        handler.binary_g = [0] * MAX_CONNS # binary: provided chunks sufficient for conn
        handler.watching_video = [''] * MAX_CONNS

        # Create server on this cache.
        self.mini_server = ThreadStreamFTPServer(self.address, handler, stream_rate)
        print "Cache streaming rate set to ", self.mini_server.stream_rate
        handler.set_movies_path(path)

    def start_cache(self):
        """Start the FTP server and the CacheDownloader instance.
        Every <timestamp>, obtain the recorded data from the FTP server queue
        and ask the server for additional chunks if needed."""
        print 'Trying to run a cache...'
        self.mini_server.start()
        self.start_control()
        print 'Cache is running...'

    def get_conns(self):
        return self.mini_server.get_conns()

    def get_handlers(self):
        return self.mini_server.get_handlers()

    def set_conn_rate(self, index, new_rate):
        self.mini_server.get_handlers()[index].set_packet_rate(new_rate)

    def get_conn_rate(self, index):
        return CacheHandler.rates[index]

    def get_chunks(self, video_name):
        if video_name in CacheHandler.chunks.keys():
            return CacheHandler.chunks[video_name]
        else:
            return []

    def set_chunks(self, video_name, new_chunks):
        # print '[cache.py]', new_chunks
        CacheHandler.chunks[video_name] = new_chunks
        # self.mini_server.get_handlers()[index].set_chunks(new_chunks)

    def get_g(self, index):
        return CacheHandler.binary_g[index]

    def get_watching_video(self, index):
        return CacheHandler.watching_video[index]

    def bound(self, h, y, a, b):
       # if (a > b)
       #     Illegal bound specified, a(lower bound) must be less than or equal to b(upper bound
       # end
       if y >= b:
           return min(0, h)
       elif y <= a:
           return max(0, h)
       else:
           return h

    def rate_update(self, T_period):
        self.rate_update_optimal(T_period)
        #self.rate_udpate_greedy(T_period)

    def rate_update_optimal(self, T_period):
        log_ct = 0
        while True:
            log_ct = log_ct + 1
            if log_ct == LOG_PERIOD:
                log_ct = 0
            time.sleep(T_period)
            print '[cache.py -debug] RATE ALLOCATION BEGINS UPDATE =================='
            print '[cache.py -debug] current_time =', strftime("%Y-%m-%d %H:%M:%S")

            handlers = self.get_handlers()
            if len(handlers) == 0:
                print '[cache.py -debug] No user is connected, len(handler) = 0'
            else:
                sum_x = 0
                #if log_ct == 0:
                print '[cache.py -debug] Initialize sum_x = 0'
                print '[cache.py -debug] handler_length', len(handlers)
                print '[cache.py -debug] Initialize debug variables....'
                handler_debug = []
                watching_debug = []
                debug_1 = []
                debug_2 = []
                delta_x_debug = []
                primal_x_debug = []
                sum_x_debug = []
                current_rate_debug = []
                total_rate_debug = []
                delta_k_debug = []
                dual_k_debug = []

                for i in range(len(handlers)):
                    if i not in CacheHandler.id_to_index.values():
                        continue

                    ## 1. UPDATE PRIMAL_X
                    handler = handlers[i]
                    if handler._closed == True:
                        continue
                    #else:
                        #if log_ct == 0:
                        #print '[cache.py -debug] Connection ' + str(i) + ' is open, proceed!'
                    video_name = self.get_watching_video(i)
                    code_param_n = self.movie_LUT.code_param_n_lookup(video_name)
                    code_param_k = self.movie_LUT.code_param_k_lookup(video_name)
                    packet_size = self.movie_LUT.chunk_size_lookup(video_name)
                    if packet_size == 0:
                        continue
                    
                    # First, find the optiaml variables
                    g = self.get_g(i)
                    delta_x = self.bound(g - (self.dual_la + self.dual_k[i]), \
                                        self.primal_x[i], 0, self.bandwidth_cap)
                    self.primal_x[i] += self.eps_x * delta_x
                    if POSITIVE_CONSTRAINT:
                        self.primal_x[i] = max(self.primal_x[i], 0)
                    sum_x += self.primal_x[i]

                    # Apply it if it goes over some rate
                    rate_per_chunk = packet_size / 1000 / BUFFER_LENGTH * 8 # (Kbps)
                    assigned_rate = max(round(self.primal_x[i] / rate_per_chunk), 0)
                    num_of_stored_chunks = len(self.get_chunks(video_name))
                    self.set_conn_rate(i, min(assigned_rate, num_of_stored_chunks))

                    ## 2. UPDATE DUAL_K
                    if video_name not in self.primal_f.keys():
                        self.primal_f[video_name] = 0.0
                    delta_k = self.bound(self.primal_x[i] - self.primal_f[video_name] * rate_per_chunk * code_param_k, self.dual_k[i], 0, INFINITY)
                    self.dual_k[i] += self.eps_k * delta_k
                    if POSITIVE_CONSTRAINT:
                        self.dual_k[i] = max(0, self.dual_k[i])

                    # Log Debug message
                    handler_debug.append(i)
                    watching_debug.append(str(video_name))
                    debug_1.append([handlers[i].index, g, self.primal_x[i]])
                    debug_2.append([g, self.dual_la, self.dual_k[i]])
                    delta_x_debug.append(delta_x)
                    primal_x_debug.append(self.primal_x[i])
                    sum_x_debug.append(sum_x)
                    current_rate_debug.append(self.get_conn_rate(i))
                    total_rate_debug.append((rate_per_chunk * code_param_k))
                    delta_k_debug.append(delta_k)
                    dual_k_debug.append(self.dual_k[i])

                # print debug message
                print '[cache.py -debug] index of active handlers =', handler_debug
                print '[cache.py -debug] watching =', watching_debug
                print '[cache.py -debug] (self.index, g, x) =', debug_1
                print '[cache.py -debug] (self.index, g, x) =', debug_2
                print '[cache.py -debug] delta_x =', delta_x_debug
                print '[cache.py -debug] primal_x =', primal_x_debug
                print '[cache.py -debug -important] sum_x (after updating primal_x) =', sum_x_debug
                print '[cache.py -debug] current_rate =', current_rate_debug
                print '[cache.py -debug] total_rate =', total_rate_debug
                print '[cache.py -debug] delta_k =', delta_k_debug
                print '[cache.py -debug] dual_k =', dual_k_debug
                
                ## 3. UPDATE DUAL_LA
                print '[cache.py -debug -important] sum_x (after updating primal_x and dual_k) =', sum_x
                delta_la = self.bound(sum_x - self.bandwidth_cap, self.dual_la, 0, INFINITY)
                print "[cache.py -debug] delta_la =", delta_la
                self.dual_la += self.eps_la * delta_la
                if POSITIVE_CONSTRAINT:
                    self.dual_la = max(self.dual_la, 0)
                print '[cache.py -debug] dual_la =' + str(self.dual_la)

    def remove_one_chunk(self, video_name, index):
        print '[cache.py] Removing chunk', index , 'of' , video_name
        frame_num = self.movie_LUT.frame_num_lookup(video_name)
        code_param_n = self.movie_LUT.code_param_n_lookup(video_name)
        for i in range(1, frame_num+1):
            f_num = str(index[0])
            if len(f_num) == 1:
                f_num = '0' + f_num
            # example: rm video-test10/test10.1.dir/test10.1.02_40.chunk
            command = 'video-'+video_name+'/'+video_name+'.'+str(i)+'.dir/'+video_name+'.'+str(i)+'.'+f_num+'_'+str(code_param_n)+'.chunk'
            print '[cache.py] removing command:', command
            os.remove(command)
        return True

    def download_one_chunk_from_server(self, video_name, index):
        print '[cache.py] Caching chunk', index , 'of' , video_name
        packet_size = self.movie_LUT.chunk_size_lookup(video_name)
        frame_num = self.movie_LUT.frame_num_lookup(video_name)
        if packet_size == 0: # This must not happen.
            return True

        last_packet_size = self.movie_LUT.last_chunk_size_lookup(video_name)
        if last_packet_size == 0:
            return True
        inst_INTL = 'INTL ' + 'CNKN ' + str(packet_size) # chunk size of typical frame (not last one)
        inst_INTL_LAST = 'INTL ' + 'CNKN ' + str(last_packet_size) # chunk size of last frame

        chosen_chunks = index
        server_request = map(str, chosen_chunks)
        server_request_string = '%'.join(server_request) + '&0' # The last digit '0' means 'I am cache'

        self.server_client.put_instruction(inst_INTL) # set chunk_size to typical frame.
        for i in range(1, frame_num+1):
            if i == frame_num: # This is the last frame, so change chunk_size.
                self.server_client.put_instruction(inst_INTL_LAST)
            filename = 'file-' + video_name + '.' + str(i)
            inst_RETR = 'RETR ' + filename
            self.server_client.put_instruction(inst_RETR + '.' + server_request_string)
            # wait till download is completed
            resp_RETR = self.server_client.get_response()
            parsed_form = parse_chunks(resp_RETR)
            fname, framenum, chunks, user_or_cache = parsed_form
            print '[cache.py] Finished downloading: Frame %s Chunk %s' % (framenum, chunks)
        return True

    def storage_update(self, T_period):
        self.storage_update_optimal(T_period)
        # self.storage_update_greedy(T_period)

    def storage_update_optimal(self, T_period):
        ct = 0
        log_ct = 0
        while True:
            time.sleep(T_period)

            ct += 1
            log_ct += 1
            if log_ct == LOG_PERIOD:
                log_ct = 0

            if DEBUGGING_MSG:
                print '[cache.py] STORAGE ALLOCATION BEGINS'
            handlers = self.get_handlers()
            if len(handlers) == 0:
                if DEBUGGING_MSG:
                    print '[cache.py] No user is connected'
            else:
                sum_storage_virtual = 0
                video_check_list = {}

                ## 1. UPDATE PRIMAL_F
                # print '[cache.py] Update dual_k'
                for i in range(len(handlers)):

                    if i not in CacheHandler.id_to_index.values():
                        # print '[cache.py]', i, 'is not in map values, we skip'
                        continue

                    handler = handlers[i]
                    if handler._closed == True:
                        if DEBUGGING_MSG:
                            print '[cache.py] Connection ' + str(i) + ' is closed'
                        continue
                    else:
                        if DEBUGGING_MSG:
                            print '[cache.py] Connection ' + str(i) + ' is open'
                    #print '[cache.py] ' + str(i) + 'th connection, index = ' + str(handler.index)

                    # Open connection
                    current_rate = self.get_conn_rate(i)
                    video_name = self.get_watching_video(i)
                    if video_name in video_check_list.keys():
                        continue
                    else:
                        video_check_list[video_name] = True
                        if log_ct == 0:
                            print '[cache.py] Updating primal_f for video', video_name
                    code_param_n = self.movie_LUT.code_param_n_lookup(video_name)
                    code_param_k = self.movie_LUT.code_param_k_lookup(video_name)
                    packet_size = self.movie_LUT.chunk_size_lookup(video_name)
                    frame_num = self.movie_LUT.frame_num_lookup(video_name)
                    additional_storage_needed = packet_size * frame_num # Rough
                    if packet_size == 0:
                        continue
                    dual_k_sum = 0

                    for j in range(len(handlers)):
                        handler_j = handlers[j]
                        if handler_j._closed == True:
                            continue
                        try:
                            if self.get_watching_video(j) == video_name:
                                dual_k_sum += self.dual_k[j]
                        except IndexError:
                            sys.stderr.write('IndexError occured. j = %d' % j)
                    print 'Handler %d is watching %s. dual_k = %.1f, dual_k_sum = %.1f' % (i, video_name, self.dual_k[j],  dual_k_sum)
                    if log_ct == 0:
                        print '[cache.py] dual_k_sum = ', dual_k_sum
                        print '[cache.py] dual_mu = ', self.dual_mu
                    if video_name not in self.primal_f.keys():
                        self.primal_f[video_name] = 0.0
                    delta_f = self.bound(dual_k_sum - frame_num * BUFFER_LENGTH * self.dual_mu, self.primal_f[video_name], 0, 1)
                    self.primal_f[video_name] += self.eps_f * delta_f
                    self.primal_f[video_name] = max(self.primal_f[video_name], 0)
                    sum_storage_virtual += self.primal_f[video_name] * self.movie_LUT.size_bytes_lookup(video_name)

                    if log_ct == 0:
                        print '[cache.py] primal_f[' + video_name + '] = ' + str(self.primal_f[video_name])
                    if DEBUGGING_MSG:
                        if log_ct == 0:
                            print '[cache.py] delta_f = %.5f' % delta_f
                            print '[cache.py] self.eps_f = %.5f' % self.eps_f
                            print '[cache.py] self.eps_f * delta_f = %.5f ' % (self.eps_f * delta_f)

                    stored_chunks = self.get_chunks(video_name)
                    if log_ct == 0:
                        print '[cache.py] stored_chunks ', stored_chunks
                    num_stored_chunks = len(stored_chunks)
                    assigned_num_of_chunks = min(max(int(self.primal_f[video_name] * code_param_k), 0), code_param_k) # ceiling
                    if log_ct == 0:
                        print '[cache.py] num_stored_chunks ', num_stored_chunks
                        print '[cache.py] assigned_num_of_chks ', assigned_num_of_chunks
                    if ct % STORAGE_UPDATE_PERIOD_OUTER == 0:
                        if assigned_num_of_chunks > num_stored_chunks:
                            if num_stored_chunks >= code_param_k:
                                if log_ct == 0:
                                    print '[cache.py] Downloading nothing from server'
                                print '[cache.py] Logic error'
                                sys.exit(0)
                            else:
                                chunk_index = random.sample( list(set(range(0,code_param_n)) - set(map(int, stored_chunks))), 1 ) # Sample one out of missing chunks
                                if self.download_one_chunk_from_server(video_name, chunk_index) == True:
                                    new_chunks = list(set(self.get_chunks(video_name)) | set(map(str, chunk_index)))
                                    self.set_chunks(video_name, new_chunks)
                                    update_chunks_for_cache(tracker_address, self.public_address, self.address[1], video_name, new_chunks)
                                    self.sum_storage = self.sum_storage + additional_storage_needed
                                    if log_ct == 0:
                                        print '[cache.py] chunk add done'
                                        print '[cache.py] storage Usage' , int(self.sum_storage/1000/1000) , '(MB) /' , int(self.storage_cap/1000/1000) , '(MB)'
                        elif assigned_num_of_chunks < num_stored_chunks:
                            if len(stored_chunks) == 0:
                                pass
                            else:
                                chunk_index = random.sample( list(set(stored_chunks)), 1 )
                                if self.remove_one_chunk(video_name, chunk_index) == True:
                                    new_chunks = list(set(self.get_chunks(video_name)) - set(map(str, chunk_index)))
                                    self.set_chunks(video_name, new_chunks)
                                    update_chunks_for_cache(tracker_address, self.public_address, self.address[1], video_name, new_chunks)
                                    self.sum_storage = self.sum_storage - additional_storage_needed
                                    if log_ct == 0:
                                        print '[cache.py] chunk ', chunk_index, ' is dropped'
                                        print '[cache.py] storage Usage' , int(self.sum_storage/1000/1000) , '(MB) /' , int(self.storage_cap/1000/1000) , '(MB)'
                        else:
                            if log_ct == 0:
                                print '[cache.py] storage not updated'

                ## 2. UPDATE DUAL_K
                print '[cache.py -debug -storage] Update dual_k ========'
                print '[cache.py -debug -storage] current_time =', strftime("%Y-%m-%d %H:%M:%S")
                handler_storage = []
                debug_storage = []
                delta_k_storage = []
                for i in range(len(handlers)):
                    if i not in CacheHandler.id_to_index.values():
                        # print '[cache.py]', i, 'is not in map values, we skip'
                        continue

                    handler = handlers[i]
                    if handler._closed == True:
                        #if log_ct == 0:
                        #    print '[cache.py] Connection ' + str(i) + ' is closed'
                        continue
                    video_name = self.get_watching_video(i)
                    if video_name not in self.primal_f.keys():
                        self.primal_f[video_name] = 0.0
                    code_param_n = self.movie_LUT.code_param_n_lookup(video_name)
                    code_param_k = self.movie_LUT.code_param_k_lookup(video_name)
                    packet_size = self.movie_LUT.chunk_size_lookup(video_name)
                    if packet_size == 0:
                        continue
                    rate_per_chunk = packet_size / 1000 / BUFFER_LENGTH * 8 # (Kbps)
                    #if log_ct == 0:
                    #    print '[cache.py] self.primal_f', self.primal_f
                    #print '[cache.py] self.primal_f[', video_name, '] = ', self.primal_f[video_name]

                    delta_k = self.bound(self.primal_x[i] - self.primal_f[video_name] * rate_per_chunk * code_param_k, self.dual_k[i], 0, INFINITY)
                    
                    handler_storage.append(i)
                    debug_storage.append([self.primal_x[i], self.primal_f[video_name], rate_per_chunk, code_param_k, self.dual_k[i]])
                    delta_k_storage.append(delta_k)

                    # if log_ct == 0:
                    #     print '[cache.py] User ' + str(i) + ' delta_k ' + str(delta_k)
                    self.dual_k[i] += self.eps_k * delta_k
                    if POSITIVE_CONSTRAINT:
                        self.dual_k[i] = max(0, self.dual_k[i])
                    # if log_ct == 0:
                    #     print '[cache.py] User ' + str(i) + ' dual_k ' + str(self.dual_k[i])
                    # print '[cache.py]DEBUG__ self.dual_k', self.dual_k[:2]

                print '[cache.py -debug -storage] index of active handlers =', handler_storage
                print '[cache.py -debug -storage] (primal_x, primal_f, rate_per_chunk, code_param_k, dual_k) =', debug_storage
                print '[cache.py -debug -storage] delta_k =', delta_k_storage

                # Need to update dual_mu
                if log_ct == 0:
                    print '[cache.py] self.sum_storage ', self.sum_storage
                    print '[cache.py] self.sum_storage_virtual ', sum_storage_virtual
                delta_mu = self.bound(sum_storage_virtual - self.storage_cap, self.dual_mu, 0, INFINITY)
                self.dual_mu += self.eps_mu * delta_mu
                if POSITIVE_CONSTRAINT:
                    self.dual_mu = max(self.dual_mu, 0)
                if log_ct == 0:
                    print '[cache.py] dual_mu ' + str(self.dual_mu)

    def topology_update(self, T_period):
        while True:
            print '[cache.py] topology updating'
            time.sleep(T_period)

    def connection_check(self):
        pass
        # print '[cache.py] connection checking'
        #conns = self.get_conns()

        # Currently assuming 'a single movie'. It needs to be generalized
        #for i in range(len(conns)):
        #CacheHandler.connected[self.index] = True

    def start_control(self):
        th1 = threading.Thread(target=self.rate_update, args=(T_rate,))
        th2 = threading.Thread(target=self.storage_update, args=(T_storage,))
        th3 = threading.Thread(target=self.topology_update, args=(T_topology,))
        threads = [th1, th2, th3]

        for th in threads:
            th.start()

###### HANDLER FOR EACH CONNECTION TO THIS CACHE######

class CacheHandler(StreamHandler):
    """
    The mini-server handler that serves users on this address.

    The mini-server only stores a particular set of chunks per frame,
    and that set will be what it sends to the user per frame requested.
    """
    chunks = []
    rates = []
    watching_video = []
    connected = []
    stream_rate = 10*1024 # Default is 10 Kbps
    def __init__(self, conn, server, index=0, spec_rate=0):
        print '[cache.py]', index
        StreamHandler.__init__(self, conn, server, index, spec_rate)

    def close(self): # Callback function on a connection close
        print '[cache.py] connection is closed'
        StreamHandler.close(self)

    def set_chunks(self, new_chunks):
        """
        Adjusts the set of chunks that this cache holds across all frames.
        """
        CacheHandler.chunks[self.index] = new_chunks

    def set_binary_g(self, new_g):
        """
        Adjusts the binary value of the user's satisfaction with this connection.
        """
        CacheHandler.binary_g[self.index] = new_g

    def set_packet_rate(self, new_rate):
        CacheHandler.rates[self.index] = new_rate
#        print "Packet rate has been set within CacheHandler for: %d conn to rate %d" % (self.index, new_rate)

    def ftp_CNKS(self, arg):
        """
        FTP command: Returns this cache's chunk number set.
        """
        # print "index:", self.index
        # print '[cache.py] CacheHandler.chunks', CacheHandler.chunks
        # print '[cache.py] line', arg
        video_name = arg.split('file-')[-1].split('.')[0]
        # print '[cache.py] video_name ', video_name
        if video_name in CacheHandler.chunks.keys():
            data = '%'.join(map(str, CacheHandler.chunks[video_name]))
        else:
            data = '%'.join(map(str, ''))
        try:
            data = data + '&' + str(int(CacheHandler.rates[self.index]))
        except IndexError:
            sys.stderr.write('IndexError occured')
            data = data + '&'
        # print "Sending CNKS: ", data
        #CacheHandler.connected[self.index] = True
        self.push_dtp_data(data, isproducer=False, cmd="CNKS")

    def ftp_UPDG(self, line):
        """
        FTP command: Update g(satisfaction signal) from users.
        """
        # Update G for this user
        CacheHandler.binary_g[self.index] = int(line)
        self.respond("200 I successfully updated g=" + line + " for the user" + str(self.index))

    def ftp_ID(self, line):
        """
        FTP command: Update ID from users.
        """
        # line = ID
        # print "[cache.py] CacheHandler.id_to_index =", CacheHandler.id_to_index
        if line not in CacheHandler.id_to_index.keys():
            CacheHandler.id_to_index[line] = self.index # Data transfer conection
            # print "[cache.py] Successfully added (ID, index) = (" + line + ", " + str(self.index) + ")"
            self.respond("200 I successfully added (ID, index) = (" + line + ", " + str(self.index) + ")")
        else:
            self.index = CacheHandler.id_to_index[line] # Info transfer conection
            # print "[cache.py] Successfully matched a connection for (ID, index) = (" + line + ", " + str(self.index) + ")"
            self.respond("200 I successfully matched a connection for (ID, index) = (" + line + ", " + str(self.index) + ")")

    def ftp_RETR(self, file):
        """Retrieve the specified file (transfer from the server to the
        client).

        Accepts filestrings of the form:
            chunk-<filename>.<ext>&<framenum>/<chunknum>
            file-<filename>
        """
        if DEBUGGING_MSG:
            pass
            # print file
        parsedform = parse_chunks(file)
        if parsedform:
            filename, framenum, chunks, user_or_cache = parsedform
            try:
                # filename should be prefixed by "file-" in order to be valid.
                # frame number is expected to exist for this cache.
                chunksdir = 'video-' + filename
                framedir = filename + '.' + framenum + '.dir'
                path = self.movies_path + '/' + chunksdir + '/' + framedir
                # get chunks list and open up all files
                files = self.get_chunk_files(path, chunks)
                # return CacheHandler.chunks[index]

                if DEBUGGING_MSG:
                    print "chunks requested:", chunks
                    print 'chunksdir', chunksdir
                    print 'framedir', framedir
                    print 'path', path
            except OSError, err:
                why = ftpserver._strerror(err)
                self.respond('550 %s.' % why)
                sys.stderr.write('ERROR: %s\n' % str(why))
                sys.stderr.write('@: %s\n' % str(self.address))

            parentCache = self.parentCache
            # print '[cache.py] primal_x to this link was', parentCache.primal_x[self.index]
            packet_size = parentCache.movie_LUT.chunk_size_lookup(filename)
            rate_per_chunk = packet_size / 1000 / BUFFER_LENGTH * 8 # (Kbps)
            parentCache.primal_x[self.index] = rate_per_chunk * len(chunks)
            # print '[cache.py] primal_x is forced down to', parentCache.primal_x[self.index]

            #CacheHandler.connected[self.index] = True
            CacheHandler.watching_video[self.index] = filename
            producer = self.chunkproducer(files, self._current_type)
            self.push_dtp_data(producer, isproducer=True, file=None, cmd="RETR")
            return
        
    

    def on_connect(self):
        print '[cache.py] CONNECTION is ESTABLISHED!!'

    def get_chunk_files(self, path, chunks=None):
        """For the specified path, open up all files for reading. and return
        an array of file objects opened for read.

        Only return the file objects specified by chunk numbers argument."""
        files = Queue.Queue()
        if not chunks:
            return files
        file_list_iterator = self.run_as_current_user(self.fs.get_list_dir, path)
        file_list = list(file_list_iterator)

        # print "[cache.py]", chunks
        for x in range(len(file_list)):
            each_file = file_list[x]
            # print "[cache.py]", x, "th file", each_file
            filename = ((each_file.split(' ')[-1]).split('\r'))[0]
            chunk_num = (each_file.split('_')[0]).split('.')[-1]
            if chunk_num.isdigit() and int(chunk_num) in chunks:
                filepath = path + '/' + filename
                # print "filepath ", filepath
                fd = self.run_as_current_user(self.fs.open, filepath, 'rb')
                files.put(fd)
                if (DEBUGGING_MSG):
                    print "Sending chunk", filename

        return files

class ServerDownloader(threadclient.ThreadClient, threading.Thread):
    """
    Requests new chunks from the server. Is always connected to the server.

    Since the chunk size is always fixed, fix the expected packet_size.
    """
    def __init__(self, address, packet_size):
        threading.Thread.__init__(self)
        StreamFTP.__init__(self, address, chunk_size=packet_size)
        self.client.set_callback(self.chunkcallback)

    def put_instruction(self, cmd_string):
        """Something or other"""
        pass

    def chunkcallback(self, chunk_size, fname):
        # directory name by convention is filename itself.
        def helper(data):
            file_to_write = open(fname, 'a+b')
            datastring = data + chunk_num_and_data[1]
            curr_bytes = sys.getsizeof(datastring)
            outputStr = "%s: Received %d bytes. Current Total: %d bytes.\n" % \
                (filestr, sys.getsizeof(data), curr_bytes)
            sys.stdout.write(outputStr)
            sys.stdout.flush()
            if DEBUGGING_MSG:
                outputStr = "Writing %d bytes to %s.\n" %  (curr_bytes, filestr)
            sys.stdout.write(outputStr)
            sys.stdout.flush()
            file_to_write.write(datastring)
            file_to_write.close()
        return helper

def load_cache_config(cache_id):
    f = open(cache_config_file)
    fs = csv.reader(f, delimiter = ' ')
    for row in fs:
        if int(row[0]) == cache_id:
            if (DEBUGGING_MSG): print '[cache.py] Cache configuration : ', row
            return row
    # If not found
    return None

def get_server_address(tracker_address, session=None):
    return retrieve_server_address_from_tracker(tracker_address, session)

def main():
    #default username and password
    username = 'ryan'
    password = '11111'
    multiplier = 1
    
    # python ../../cache.py 1
    # python ../../cache.py multiplier username password
    if len(sys.argv) == 2:
        config = load_cache_config(int(sys.argv[1])) # Look up configuration of the given cache ID
        if config == None:                           # This is kept here for backwards compatibality
            print '[cache.py] cache_id not found'
            sys.exit()
            
    #DO NOT EVER USE THIS ONE HERE.
    elif len(sys.argv) == 4:
        config = load_cache_config(1)
        multiplier = float(sys.argv[1])
        username = sys.argv[2]
        password = sys.argv[3]
    
    # python ../../cache.py 1 public
    # python ../../cache.py multiplier public username password
    # THE ABOVE DOES NOT SPECIFY THE PORT. IT IS USING THE MULTIPLIER AS THE PORT WHICH IS WRONG.
    # DO NOT EVER USE THE ONE ABOVE HERE
    
    #../../cache.py port_number public
    elif len(sys.argv) == 3:
        if(sys.argv[2] == 'public'):
            sys.argv[2] = urllib2.urlopen('http://icanhazip.com').read().strip('\n')
        config = [sys.argv[1], '0.0.0.0', str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
        #config = [sys.argv[1], sys.argv[2], str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
        multiplier = float(1)
        username = 'ryan'
        password = '11111'
        #Originally it was the one on the bottem. I have it here for reference in case the on on top
        #Does not work for some reason.
        
    #../../cache.py port_number public username password
    elif len(sys.argv) == 5:
        #WAS ORIGINALLY MAKING THE PORT NUMBER THE MULTIPLIER WHICH IS WRONG. SETTING MULTIPLIER TO 1
            if(sys.argv[2] == 'public'):
                sys.argv[2] = urllib2.urlopen('http://icanhazip.com').read().strip('\n')
            config = [1, sys.argv[2], str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
            #config = [sys.argv[1], sys.argv[2], str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
            multiplier = float(sys.argv[1])
            multiplier = float(1)
            username = sys.argv[3]
            password = sys.argv[4]
            
    #../../cache.py port_number public username password multiplier
    elif len(sys.argv) == 6:
            if(sys.argv[2] == 'public'):
                sys.argv[2] = urllib2.urlopen('http://icanhazip.com').read().strip('\n')
            #config = [1, sys.argv[2], str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
            #config = [sys.argv[1], '0.0.0.0', str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
            config = [sys.argv[1], sys.argv[2], str(60000+int(sys.argv[1])), sys.argv[2], 15000000]
            multiplier = float(sys.argv[5])
            #multiplier = float(1)
            username = sys.argv[3]
            password = sys.argv[4]
    
    else:
        print 'Please enter x, where cache port = 60000 + x '
        base_port = raw_input()
        cache_id = base_port
        base_port = str(60000 + int(base_port))
        cache_public_address = urllib2.urlopen('http://icanhazip.com').read().strip('\n')
        print 'Enter the cache\'s ip address (press enter to let system determine the address automatically)' #later we need to have it automatically get the user's ip
        ip_address_input = raw_input()
        if len(ip_address_input) == 0:
            ip_address_input = cache_public_address
        print 'Enter the cache\'s ip address again (press enter to let system determine the address automatically)'
        public_address_input = raw_input()
        if len(public_address_input) == 0:
            public_address_input = cache_public_address
        print 'Enter cache size (press enter to use default size 15000000)'
        cache_size_input = raw_input()
        if len(cache_size_input) == 0:
            cache_size_input = 15000000
        print 'Make sure that the correct tracker address is stored in tracker_address.txt'
        print 'Enter any key to continue'
        raw_input()
        config = [cache_id, ip_address_input, base_port, public_address_input, cache_size_input]
    #resource.setrlimit(resource.RLIMIT_NOFILE, (5000,-1))
    
    session = requests.Session()
    log_in_to_tracker(session, tracker_address, username, password)
    config.append(session)
    config.append(multiplier)
    print '[config] ' + str(config)
    cache = Cache(config)
    cache.start_cache()

if __name__ == "__main__":
    main()
