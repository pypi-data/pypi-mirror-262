import os

def test_mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)