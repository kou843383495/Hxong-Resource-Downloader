import re
import time
from pathlib import Path


def nested_dir_clean(currentDir:Path):
    if not currentDir.is_dir():
        return
    children = sorted(currentDir.glob('*'))
    if len(children) == 1 and children[0].is_dir() and children[0].name == currentDir.name:
        newDir = children[0].replace(currentDir.parent/f'{currentDir.name}-temp-{time.time()}')
        if currentDir.exists():
            currentDir.rmdir()
        newDir = newDir.replace(currentDir)
        nested_dir_clean(newDir)
    else:
        for child in children:
            nested_dir_clean(child)


def add_ignore_to_dir(currentDir:Path, targetDir:str):
    if not currentDir.is_dir():
        return

    if re.fullmatch(targetDir,currentDir.name):
        (currentDir/'.ignore').touch(exist_ok=True)

    children = sorted(currentDir.glob('*'))
    for child in children:
        add_ignore_to_dir(child, targetDir)