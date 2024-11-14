import re
import time
from pathlib import Path


def nestedDirClean(currentDir:Path):
    if not currentDir.is_dir():
        return
    children = sorted(currentDir.glob('*'))
    if len(children) == 1 and children[0].is_dir() and children[0].name == currentDir.name:
        print(children[0],currentDir)
        newDir = children[0].replace(currentDir.parent/f'{currentDir.name}-temp-{time.time()}')
        newDir = newDir.replace(currentDir)
        nestedDirClean(newDir)
    else:
        for child in children:
            nestedDirClean(child)


def addIgnoreToDir(currentDir:Path,targetDir:str):
    if not currentDir.is_dir():
        return

    if re.fullmatch(targetDir,currentDir.name):
        (currentDir/'.ignore').touch(exist_ok=True)

    children = sorted(currentDir.glob('*'))
    for child in children:
        addIgnoreToDir(child,targetDir)