'''
RecBin v20140709 - John Moran (john@jtmoran.com)

Parses all $I recycle bin artifacts from Windows Vista+ from a given directory
and displays date/time deleted, original file path and original file size.

Syntax: recbin.py -d <directory>
'''

import getopt
import sys
import glob
import os
import datetime
import re

def readDir (dir):
    if not os.path.exists(dir):
        print("\nDirectory '" + dir + "' does not exist!")
        return
    os.chdir(dir)
    fileList = []
    #Get list of $I files in dir
    for file in glob.glob("$I*"):
        fileList.append(dir + "/" + file)
    #If 1+ $I files found continue
    if(len(fileList) < 1):
        print("\nNo $I files found in '" + dir + "'")
        return
    else:
        print("\n(" + str(len(fileList)) + ") $I files found in '" + dir + "'\n")
        print("File                Date\\Time Deleted           Original Path  (Original Size)")
        print("----                -----------------           -----------------------------")
    #Read each file
    for f in fileList:
        readI(f)

def readI(fname):
    #Open file and read into 'data'
    I = open(fname, "rb")
    data = I.read()
    #Read Windows FILETIME obj at bytes 16-23
    date = datetime.datetime.utcfromtimestamp(((int.from_bytes(data[16:24], byteorder='little') - 116444736000000000) / 10000000)).strftime('%H:%M:%S %m/%d/%Y')
    #Read original file name at bytes 24+
    filename = data[24:]
    filename = filename.decode("utf16").rstrip('\0')
    #Read original file size at bytes 8-15
    filesize = int.from_bytes(data[8:16], byteorder='little')
    basename = os.path.basename(fname)
    date = date  + " GMT"
    print(basename.ljust(20) + date.ljust(28) + filename + "  (" + str(filesize) + " bytes)")
		
def main (argv):
	#Get command line options
    try:
	    opts, args = getopt.getopt(argv, "d:h", ["directory=", "help"])
    except getopt.GetoptError:
        print("\nInvalid options!")
        print(__doc__)
        sys.exit(2)
	#Check that only one command line option is specified	
    if len(opts) != 1:
        print("\nInvalid options!")
        print(__doc__)
        sys.exit(2)	
		
    for opt, arg in opts:
	    #Help
        if opt in ("-h", "--help"):
            print(__doc__)
            sys.exit(2)	
    	#Directory
        if opt in ("-d", "--directory"):
            readDir(arg)

		
if __name__ == "__main__":
    main(sys.argv[1:])