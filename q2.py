import json
import os
import sys

class Scene(object):

    def __init__(self, jsonData):
        self.width = jsonData.get('width')
        self.height = jsonData.get('height')
        self.objects = []

        for o in jsonData.get('objects'):
            type = o.get('type')

            if type == "circle":
                self.objects.append(Circle(o))
            elif type == "box":
                self.objects.append(Box(o))

    def __repr__(self):
        s = "Scene of dimensions {} x {}\n".format(self.width, self.height) \
            + "Containing {} objects:".format(len(self.objects))

        for o in self.objects:
            s += "\n- " + o.__repr__()
            
        return s
        
class Circle(object):

    def __init__(self, jsonData):
        self.center = jsonData.get('center')
        self.radius = jsonData.get('radius')

    def __repr__(self):
        return "A circle of radius {}, centered in ({},{})" \
            .format(self.radius, self.center[0], self.center[1])

class Box(object):
    
    def __init__(self, jsonData):
        self.center = jsonData.get('center')
        self.width = jsonData.get('width')
        self.height = jsonData.get('height')
    
    def __repr__(self):
        return "A box of width {} and height {}, centered in ({},{})" \
            .format(self.width, self.height, self.center[0], self.center[1])

if (len(sys.argv) == 1):
    print("Missing argument : relative path to file required")
else:
    cwd = os.path.dirname(os.path.realpath(__file__))
    sceneFile = cwd + "/" + sys.argv[1]

    try:
        jsonData = json.loads(open(sceneFile).read())
        try:
            scene = Scene(jsonData)
            print scene
        except:
            print("Error : invalid object(s) in json file. The scene " \
                + "only allows circles and boxes")
    except:
        print("Error : invalid filename")
