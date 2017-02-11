import os

def touch():
    """Simply creates an empty file. Only for tests."""
    # print(__file__)
    filename = "lolo.txt"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../files/output', filename)
    # print(path)
    open(path, 'w').close()
    print(os.path.abspath('./files/'))
touch()