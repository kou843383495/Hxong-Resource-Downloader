import subprocess
from pathlib import Path

from DirCleaner import nestedDirClean
from setting import SETTING

patool_check = ['patool','test','--password']
patool_extract = ['patool','extract','--password']


def findPassword(archived_file_path:Path):
    for password in SETTING.PASSWORDS:
        checkResult = subprocess.run(patool_check+[password,str(archived_file_path)],capture_output=True,text=True)
        if 'tested ok' in checkResult.stderr:
            return password
    return None

def extractArchivedFile(archivedFile:Path, filePassword:str, targetDir:Path = None):
    fileName = archivedFile.name.split('.')[0]
    newPath = targetDir / fileName if targetDir else archivedFile.parent/fileName
    newPath.mkdir(parents=True,exist_ok=True)
    extractResult=subprocess.run(patool_extract + [filePassword, str(archivedFile),'--outdir',str(newPath)],capture_output=True,text=True)
    if 'ERROR' not in extractResult.stderr:
        archivedFile.unlink(missing_ok=True)
        nestedDirClean(newPath)
        print(f'success deal {fileName}')

def tgDownloadCheck(filePath:Path):
    password = findPassword(filePath)
    if password:
        extractArchivedFile(filePath,password)

