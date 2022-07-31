import ftplib
import os
from db_operations import *
import time
  
   
def getFtpFilenames(ftpHost, ftpPort, ftpUname, ftpPass, remoteWorkingDirectory):
    # create an FTP client instance, use the timeout(seconds) parameter for slow connections only
    ftp = ftplib.FTP(timeout=30)
    
    # connect to the FTP server
    try:
        ftp.connect(ftpHost, ftpPort)
    except:
        print("Connection Not Fine")
        fnames = []
        fnames.append("ftpconnectionfailure")
        return fnames
        
    # login to the FTP server
    ftp.login(ftpUname, ftpPass)

    # change current working directory if specified
    if not (remoteWorkingDirectory == None or remoteWorkingDirectory.strip() == ""):
        _ = ftp.cwd(remoteWorkingDirectory)
    
    # initialize the filenames as an empty list
    fnames = []
    
    try:
        # use nlst function to get the list of filenames
        fnames = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            fnames = []
        else:
            raise
    
    # send QUIT command to the FTP server and close the connection
    ftp.quit()

    # return the list of filenames
    return fnames


def downloadFilesFromFtp(localfolderPath, targetFilenames, ftpHost, ftpPort, ftpUname, ftpPass, remoteWorkingDirectory):
    # initialize the flag that specifies if download is success
    isDownloadSuccess: bool = False

    # create an FTP client instance, use the timeout parameter for slow connections only
    ftp = ftplib.FTP(timeout=30)

    # connect to the FTP server
    ftp.connect(ftpHost, ftpPort)

    # login to the FTP server
    ftp.login(ftpUname, ftpPass)

    # change current working directory if specified
    if not (remoteWorkingDirectory == None or remoteWorkingDirectory.strip() == ""):
        _ = ftp.cwd(remoteWorkingDirectory)

    # iterate through each remote filename and download
    for fItr in range(len(targetFilenames)):
        targetFilename = targetFilenames[fItr]
        # derive the local file path by appending the local folder path with remote filename
        localFilePath = os.path.join(localfolderPath, targetFilename)
        print("downloading file {0}".format(targetFilename))
        # download FTP file using retrbinary function
        with open(localFilePath, "wb") as file:
            retCode = ftp.retrbinary("RETR " + targetFilename, file.write)

    # send QUIT command to the FTP server and close the connection
    ftp.quit()

    # check if download is success using the return code (retCode)
    if retCode.startswith('226'):
        isDownloadSuccess = True
    return isDownloadSuccess


while(True):
    # connection parameters
    ftpHost = '192.168.29.87'
    ftpPort = 2221
    ftpUname = 'bala'
    ftpPass = '1234567890'
    remoteFolder = "iRecorder"
    fnames = []
    fnames = getFtpFilenames(ftpHost, ftpPort, ftpUname, ftpPass, "iRecorder")
    if(fnames[0] == "ftpconnectionfailure"):
        print("Connection Not Fine")
        print('Waiting for 1 minute')
        time.sleep(60)
        continue
        
    print(fnames)
    print("Listing complete...")

    localFolderPath = "D:\iRecorder_Phone"

    #SQLQuery(Path2DB + "\\SQLite_Python.db")

    for i in range(len(fnames)):
        print(fnames[i])
        remoteFilenames = []
        remoteFilenames.append(fnames[i])
        print(remoteFilenames)
        
        if os.path.exists(localFolderPath + "\\" + fnames[i]) and os.path.getsize(localFolderPath + "\\" + fnames[i]) > 0:
            print("File already exist locally = {0}".format(remoteFilenames))    
        else:
            # run the function to download the files from FTP server
            isDownloadSuccess = downloadFilesFromFtp(
                localFolderPath,remoteFilenames, ftpHost, ftpPort, ftpUname, ftpPass, remoteFolder)
            #print("download File = {0}".format(remoteFilenames))    
            print("download status = {0}".format(isDownloadSuccess))
            if(isDownloadSuccess == 1):
                #CmdShortsCreation = "start /wait cmd /c "
                CmdShortsCreation = "start cmd /c "
                CmdShortsCreation += "python \"D:\GIT\TTS\main.py\" 9 1 " + localFolderPath + "\\" +fnames[i]
                print(CmdShortsCreation)
                os.system(CmdShortsCreation)
                # changeFtpFilenames(ftpHost, ftpPort, ftpUname, ftpPass, "iRecorder")
                # fileRenameSuces= ftp.rename(remoteFilenames, "BackedUp" + remoteFilenames )
                # print("download rename = {0}".format(fileRenameSuces))   
                
    print('Waiting for 1 minute')
    time.sleep(60)

