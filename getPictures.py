import os

def getPictures():

    DIRECTORY = "./Static"

    files = []

    for filename in os.listdir(DIRECTORY):
        f = os.path.join(DIRECTORY, filename)
        if os.path.isfile(f):
            files.append(filename)
            
    return files





