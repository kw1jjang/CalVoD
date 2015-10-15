from zfec import filefec
import os, sys, shutil
from FLVWrapper import FLVWrapper
import csv

try:
    from pymediainfo import MediaInfo #used to get the bitrate of the video file.
except:
    print 'Must install new dependencies.'
    print 'First download Mediainfo from here: https://mediaarea.net/en/MediaInfo/Download'
    print 'If using ubuntu, download with sudo apt-get mediainfo'
    print 'This is a command line interface for reading different media formats.'
    print 'Then, install the python wrapper for it: easy_install pymediainfo'
    print 'With this, we can gather metadata from more file formats than just FLV'
    print 'FLVWrapper is no longer required or used, however is imported anyways'
#install this from doing:
#easy_install pymediainfo
#requires Mediainfo from here:
#https://mediaarea.net/en/MediaInfo/Download

"""
Encodes a file into chunks.

Important: chunk_size: specifies size of chunk.
"""

def get_media_info(media_info):
    #Depending on the file type, the metadata for encoding is slightly different.
    #The python wrapper can retrieve the metadata of any video format.
    #For now, this function only will work for .flv and for .mkv. It is trivial to add others,
    #However I do not know the exact way how the object will handle the data, thus I did not add.
    print 'Type = ' + media_info.tracks[0].codec
    if media_info.tracks[0].codec == 'Flash Video':
        for track in media_info.tracks:
            if track.track_type == 'Video':
                video_bit_rate = track.bit_rate
            if track.track_type == 'Audio':
                audio_bit_rate = track.bit_rate
        average_bit_rate = video_bit_rate + audio_bit_rate
        return average_bit_rate
    if media_info.tracks[0].codec == 'Matroska':
        average_bit_rate = media_info.tracks[0].overall_bit_rate
        return average_bit_rate


def split_and_encode(filestr, k, n):
    # 2/25/2013 : KW Lee
    # Now, it reads 'average bitrate' from the FLV metadata, it automatically decides the size of chunk.
    buffer_size = 10 # (secs)
    filestr_old = filestr
    filestr = filestr.split('file-')[1]
    #flv_input = FLVWrapper(filestr, 'r+b') # FLV wrapper of the input file
    media_info = MediaInfo.parse(filestr); #takes video file as input, returns metadata
    filestr_ryan = filestr
    filestr = filestr_old
    
    #average_bit_rate = video_bit_rate / 1000 + audio_bit_rate / 1000
    #average_bit_rate = flv_input.get_Bitrate() # (Kbps)
    average_bit_rate = get_media_info(media_info) #returns in bps
    #chunk_size = int(buffer_size * average_bit_rate * 1000 / 8) # size of each frame
    #Because average_bit_rate is now in bps, we no longer have to convert from Kbps to bps
    chunk_size = int(buffer_size * average_bit_rate / 8) # size of each frame 
    chunk_num = 1

    filename = ''
    # Remove "file-" prefix and extension.
    try:
        filename=(((filestr.split('.'))[0]).split('file-'))[1]
    except:
        print "input in wrong format. Must be 'file-<filename>.ext."
        return

    server_dir = 'server'
    dirname = server_dir + '/video-' + filename
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        print "Encoded videos for " + (filestr.split('.'))[0] + ".flv already exist"
        print "Deleted existing files and re-encoding..."
    os.mkdir(dirname)
    filestr = filestr_ryan
    forig = open(filestr, 'rb')
    filestr = filestr_old
    data = forig.read(chunk_size)
    while data:
        subfilestr = filename.replace('_', '-') + '.' + str(chunk_num)
        subfile = open(dirname + '/' + subfilestr, 'wb')
        subfile.write(data)
        subfile.close()
        code(subfilestr, subfilestr, k, n, dirname)
        data = forig.read(chunk_size)
        chunk_num += 1
    forig.close()

def code(filestr, prefix, k, n, dirname=''):
    """Makes a directory for the specified file portion to code and stores
    encoded packets into that directory."""

    print "filestr", filestr, "prefix", prefix, "dirname", dirname
    current_dir = os.getcwd()
    os.chdir(dirname)
    os.mkdir(filestr + '.dir')

    f = open(filestr, 'rb')
    f.seek(0,2) # Seek to 0th bit from the end of the file (second param = 2)
    file_size = f.tell() # See what's the index of the last bit, or the filesize
    f.seek(0,0) # Seek to 0th bit of the file (second param = 0)

    # Call filefec's encode_to_files
    # parameters : File / File Size / Target Directory / File Name / k / n / File Extension
    filefec.encode_to_files(f, file_size, filestr + '.dir', prefix, k, n, '.chunk')

    os.chdir(current_dir)

def write_csv(filestr, k, n):
    # automatically update config/video_info.csv with new encoded video
    #template: file_name dir_num n k file_size first_chunk_size last_chunk_size bandwidth
    server_dir = 'server'
    filestr_old = filestr
    filestr = filestr.split('file-')[1]
    file_name = (((filestr_old.split('.'))[0]).split('file-'))[1]
    dir_name = server_dir + '/video-' + file_name
    dir_num = str(len(os.listdir(dir_name))/2)
    #file_size = str(os.path.getsize(filestr))
    print file_name
    print filestr
    print dir_name
    print dir_num
    file_size = str(os.path.getsize(filestr))
    #example: server/video-ryan/ryan.1.dir/ryan.1.00_40.chunk
    first_chunk_dir = dir_name + "/" + file_name + ".1.dir/" \
        + file_name + ".1.00_" + str(n) + ".chunk"
    last_chunk_dir =  dir_name+"/"+file_name+"."+dir_num+".dir/" \
        + file_name + "." + dir_num + ".00_" + str(n) + ".chunk"
    print first_chunk_dir
    print last_chunk_dir
    first_chunk_size = str(os.path.getsize(first_chunk_dir))
    last_chunk_size = str(os.path.getsize(last_chunk_dir))
    bandwidth = "3.2Mbps"
    s = " "
    info = file_name + s + dir_num + s + str(n) + s + str(k) \
        + s + file_size + s + first_chunk_size + s + last_chunk_size + s + bandwidth

    #write info to video_info.csv
    reader = csv.reader(open('config/video_info.csv', 'r'))
    writer = csv.writer(open('config/video_info.csv', 'a'))
    #find out if entry already exists
    for row in reader:
        if str(row[0]).find(info) != -1:
            print "csv entry already exist"
            return
    writer.writerow([info])
    print "wrote new csv entry"

if __name__ == "__main__":
    """Encodes files within the movies directory."""

    k = 20
    n = 40
    #create ./server directory
    if os.path.exists("server") == 0:
        os.mkdir("server")
    print 'sys.argv = ', sys.argv
    if len(sys.argv) < 2:
        print "Usage: python encode.py <file-filename> <chunk> <coded chunks>"
        print "Defaults: <chunk=20> <coded chunks=40>"
    else:
        filestr = sys.argv[1]
        if len(sys.argv) == 4:
            k = int(sys.argv[2])
            n = int(sys.argv[3])

        # movies_path = '/home/ec2-user/movies'
        # os.chdir(movies_path)
        split_and_encode(filestr, k, n)
        write_csv(filestr, k, n)
