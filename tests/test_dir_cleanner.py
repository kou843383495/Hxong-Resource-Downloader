from pathlib import Path

from HxongResourceDownloader.dir_cleaner import nested_dir_clean


def create_nested_dir(path:Path):
    (path/'test_nested'/'test_nested').mkdir(parents=True)
    (path/'test_normal_folder'/'different_name').mkdir(parents=True)


class TestDirCleaner:

    def test_nested_dir_cleaner(self,tmp_path):
        create_nested_dir(tmp_path)
        nested_dir_clean(tmp_path)
        assert not (tmp_path/'test_nested'/'test_nested').exists(), 'Nested dir not clean'
        assert (tmp_path/'test_nested').exists(), 'The top nested dir missing'
        assert (tmp_path/'test_normal_folder'/'different_name').exists(), 'The normal dir missing'