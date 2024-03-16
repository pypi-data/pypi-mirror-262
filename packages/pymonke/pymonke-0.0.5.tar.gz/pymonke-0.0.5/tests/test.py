import json
import os
file = open("../data.json")
data: dict = json.load(file)
file.close()
print(data)
