import subprocess
from pathlib import Path

from patoolib import is_archive

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
        test_result = subprocess.run(['7z', 't', f'-p{password}', archived_file_path], capture_output=True, text=True)
        if 'Everything is Ok' in test_result.stdout:
            print(password + ' it is password')
            return password
        else:
            continue
    raise NoFindSuitablePasswordError

# Extract the file to the target folder
def extract_archived_file(archived_file:Path) -> Path:
    fileName = archived_file.stem
    newPath = archived_file.parent / fileName
    newPath.mkdir(parents=True,exist_ok=True)
    password = find_password(str(archived_file))
    extract_result = subprocess.run(['7z', 'x', f'-p{password}',f'-o{str(newPath)}', archived_file], capture_output=True, text=True)
    if 'Everything is Ok' in extract_result.stdout:
        pass
    archived_file.unlink(missing_ok=True)
    return newPath


