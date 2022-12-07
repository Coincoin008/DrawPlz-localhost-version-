import json

def updateLike(picture, more):
    with open("./Data/pictures.json", 'r') as file:
        json_ =  file.read()

    pictures = json.loads(json_)

    if more:
        pictures[picture]['likes'] += 1
        
    
    else:
        pictures[picture]['likes'] -= 1
       
    #print(json.dumps(pictures, sort_keys=True, indent=4))
    with open("./Data/pictures.json", "w") as file:
        file.write(json.dumps(pictures, sort_keys=True, indent=4))

print(bool("False"))
