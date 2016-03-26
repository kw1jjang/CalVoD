import urllib2
from helper import *
import os

#first change tracker address
tracker_address = load_tracker_address()
print '========================================='
print 'Welcome to Scalable VoD!'

#login
logged_in = False;
while(logged_in == False):
  print ''
  username = raw_input('Enter username: ')
  password = raw_input('Enter password: ')
  req_str = 'VERIFY_ACCOUNT&' + username + '_' + password
  print 'request sent to tracker: ' + tracker_address + req_str
  ret_str = urllib2.urlopen(tracker_address + req_str).read()
  if ret_str == 'True':
    print 'user logged in!'
    logged_in = True
  else:
    print 'wrong combiniation of username/password, try again!'
print ''
print '========================================='
print 'login successful!'

#select number of caches
print 'please select the amount of resources you are willing to contribute'
print '1 - none (slowest streaming speed)'
print '2 - small (slowest streaming speed)'
print '3 - medium (slowest streaming speed)'
print '4 - large (slowest streaming speed)'
while True:
  selection = raw_input('selection: ')
  if selection == '1' or selection == '2' or selection == '3' or selection == '4':
    break
  else:
    print 'invalid selection!'

cache_options = ['0', '3', '5', '10']
num_caches = cache_options[int(selection) - 1]
os.system('./populate_caches_local_ui.sh ' + num_caches + ' ' + username + ' ' + password)

#run user
print '========================================='
print 'starting the user client...'
os.system('./populate_single_user.sh')
