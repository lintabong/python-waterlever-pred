import os
import json

if not os.path.exists("config.json"):
    result = {
        "width": 900,
        "height": 500,
        "rectangle": {
            "x": 10,
            "y": 10,
            "w": 80,
            "h": 240
        },
        "camFrame": {
            "width": 880,
            "height": 400
        },
        "video": {
            "scale": 0.8
        }
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