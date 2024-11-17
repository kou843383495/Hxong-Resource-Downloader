from pathlib import Path
from random import choice

from patoolib import create_archive

from HxongResourceDownloader.Excepation.FileExcepation import NoFindSuitablePasswordError
from HxongResourceDownloader.download_resource_check import find_password, extract_archived_file, check_file
from HxongResourceDownloader.setting import SETTING


def create_archived_file(path:Path):
    files = [path /f"file{i}.text" for i in range(3)]
    for file in files:
        file.touch(exist_ok=True)
        with open(file,'w') as f:
            f.write(file.stem)
        create_archive(archive=str(file.parent/(file.stem+'.7z')),filenames=[str(file)],password=choice(SETTING.PASSWORDS))
        file.unlink(missing_ok=True)


def create_archived_file_unknown_password(path:Path):
    files = [path /f"file_unknown_password{i}.text" for i in range(1)]
    for file in files:
        file.touch(exist_ok=True)
        with open(file,'w') as f:
            f.write(file.stem)
        create_archive(archive=str(file.parent/(file.stem+'.7z')),filenames=[str(file)],password='unknown_password')
        file.unlink(missing_ok=True)

def create_unarchived_file(path:Path):
    files = [path / f"file_unarchived{i}.text" for i in range(1)]
    for file in files:
        file.touch(exist_ok=True)
        with open(file, 'w') as f:
            f.write(file.stem)





class TestDownloadResourceCheck:



    def test_check_file(self,tmp_path):
        create_archived_file(tmp_path)
        create_unarchived_file(tmp_path)
        for file in tmp_path.iterdir():
            check_file(file)
        file_count = 0
        dir_count = 0
        for file in tmp_path.iterdir():
            print(str(file))
            if file.is_dir():
                dir_count += 1
            elif file.suffix == '.text':
                file_count += 1
        assert dir_count == 3 and file_count == 1, 'the check file result is not right'

    def test_find_password_success(self, tmp_path):
        create_archived_file(tmp_path)
        for file in tmp_path.iterdir():
            find_password(str(file))

    def test_find_password_fail(self,tmp_path):
        create_archived_file_unknown_password(tmp_path)
        count = 0
        for file in tmp_path.iterdir():
            try:
                find_password(str(file))
            except NoFindSuitablePasswordError as e:
                count += 1
        assert count == 1, 'unknown password count not right'


    def test_extract_archived_file(self,tmp_path):
        create_archived_file(tmp_path)
        create_archived_file_unknown_password(tmp_path)
        success_count = 0
        fail_count = 0

        for file in tmp_path.iterdir():
            try:
                extract_archived_file(file)
                success_count += 1
            except NoFindSuitablePasswordError as e:
                fail_count += 1

        assert success_count == 3 and fail_count == 1, 'success and fail count not right'
