import os
import json

if not os.path.exists("config.json"):
    result = {
        "width": 1230,
        "height": 800,
    }
            
    with open("config.json", "w") as outfile:
        json.dump(result, outfile)
        
    outfile.close()


def read():
    with open("config.json", "r") as openfile:
        config = json.load(openfile)

    openfile.close()

    return config

def write(configuration):
    with open("config.json", "w") as outfile:
        json.dump(configuration, outfile)
        
    outfile.close()

    return 1