from zfec import filefec
import os, sys
from FLVWrapper import FLVWrapper

"""
Encodes a file into chunks.

Important: chunk_size: specifies size of chunk.
"""

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

if __name__ == "__main__":
    """Encodes files within the movies directory."""

    k = 20
    n = 40
    print 'sys.argv = ', sys.argv
    if len(sys.argv) < 2:
        print "Usage: python encode.py <filename> <chunk> <coded chunks>"
        print "Defaults: <chunk=20> <coded chunks=40>"
    else:
        filestr = sys.argv[1]
        if len(sys.argv) == 4:
            k = int(sys.argv[2])
            n = int(sys.argv[3])
        # movies_path = '/home/ec2-user/movies'
        # os.chdir(movies_path)
        split_and_encode(filestr, k, n)
