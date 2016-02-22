import ConfigParser
import sys

def main():
	if len(sys.argv) == 2:
		tracker_address = sys.argv[1] + 'req/'
	elif len(sys.argv) == 3:
		tracker_address = 'http://' + sys.argv[1] + ':' + sys.argv[2] + '/req/'
	
	# write tracker_address.txt
	f = open('tracker_address.txt', 'w')
	f.write(tracker_address)
	f.close()

	# write development.ini
	config = ConfigParser.ConfigParser()
	config.read('development.ini')
	config.set('Global','tracker_address', tracker_address)
	with open(r'development.ini', 'wb') as configfile:
	    config.write(configfile)
	print 'tracker address changed to: ' + tracker_address

if __name__ == "__main__":
    main()