# First we need to load some libraries
import sys
import json
from ftplib import FTP
import os
import urllib.request
# For Python < 3.0 use import urllib or import urllib2.request
# If you are suing Python 3 or above (most likely case) there is no one urllib module. It has been split into several modules




# check the number of input parameters, we need at least one project accession to query with
if len(sys.argv) < 2:
    print('No input parameter specified. You have to provide at least one project accession')
    sys.exit(-1)

projects = sys.argv;
# get rid of the first argument, as it is the name of the script itself
projects.pop(0)

# project = 'PRD000008'

if not os.path.exists("PRIDE_FTP_downloads"):
    os.mkdir("PRIDE_FTP_downloads")

download_path = os.path.abspath("PRIDE_FTP_downloads")

# for each of the provided project accessions retrieve the record and print some details
for project in projects:
        # Set the request URL
        url = 'http://www.ebi.ac.uk:80/pride/ws/archive/file/list/project/' + project
        # Create the request
        req = urllib.request.Request(url)
        # Send the request and retrieve the data
        resp = urllib.request.urlopen(req).read()
        # Interpret the JSON response
        project = json.loads(resp.decode('utf8'))
        # Get the FTP address for this project
        ftp_dir = project['list'][0]['downloadLink']
        # We need to trim the URL
        ftp_dir = ftp_dir[26:-len(project['list'][0]['fileName'])]
        print("FTP location is: " + ftp_dir)

        for i in range(len(project['list'])):
                print("Downloading file: " + project['list'][i]['fileName'])
                filename = project['list'][i]['fileName']
                ftp = FTP('ftp.pride.ebi.ac.uk')
                ftp.login()
                ftp.cwd(str(ftp_dir))
                # download the file
                local_filename = os.path.join(download_path, filename)
                lf = open(local_filename, "wb")
                ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
                lf.close()