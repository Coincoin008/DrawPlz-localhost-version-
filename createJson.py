import json
from getPictures import *

PICTURES = getPictures()


json_ = json.dumps({n : {} for n in PICTURES})
print(json.dumps({n : {} for n in PICTURES}, sort_keys=True, indent=4))

with open("./Data/pictures.json", "w") as file:
    file.write(json.dumps({n : {"likes":0} for n in PICTURES}, sort_keys=True, indent=4))

