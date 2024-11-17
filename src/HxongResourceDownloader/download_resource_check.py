import subprocess
from pathlib import Path

from patoolib import is_archive, test_archive, extract_archive
from patoolib.util import PatoolError

from .Excepation.FileExcepation import NoFindSuitablePasswordError
from .dir_cleaner import nested_dir_clean
from .setting import SETTING


# Check the file is an archived file or not, if it archived then extract it to a new fold in target folder
def check_file(filePath:Path):
    newFilePath = filePath
    if is_archive(str(filePath)):
        newFilePath = extract_archived_file(filePath)

    nested_dir_clean(newFilePath)

# Find the password of the archived, the password is in the setting file
def find_password(archived_file_path:str):
    for password in SETTING.PASSWORDS:
        try:
            test_archive(archive=str(archived_file_path),verbosity=-1,password=password,show_err=False)
            return password
        except PatoolError:
            tmp_path = Path(archived_file_path)
            tmp_path = tmp_path.parent/tmp_path.stem
            if tmp_path.exists() and tmp_path.is_dir():
                tmp_path.rmdir()
            pass
    raise NoFindSuitablePasswordError

# Extract the file to the target folder
def extract_archived_file(archived_file:Path) -> Path:
    fileName = archived_file.stem
    newPath = archived_file.parent / fileName
    newPath.mkdir(parents=True,exist_ok=True)
    password = find_password(str(archived_file))
    extract_archive(archive=str(archived_file),verbosity=-1,password=password,outdir=str(newPath))
    archived_file.unlink(missing_ok=True)
    return newPath


