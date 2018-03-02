"""
UQAM - Winter 2018 - INF5017 - Group 20 - q4-blenderscript.py

Program called by q4.py to generate an OGG format video of
a rendered blender animation of a solar system.

    $ blender --background --python q4-blenderscript.py -- [INPUT_FILE] [OUTPUT_FILE]

    INPUT_FILE      The json file containing the information on the
                    solar system to render
    OUTPUT_FILE     The filename for the rendered animation
"""
import json
import sys
import os
import bpy
import re
from math import pi

ERR_NB_PARAMS = "Error : 2 arguments required, {} provided."
ERR_INV_FILE = "Error : file \"{}\" does not exist."
ERR_INV_JSON_FILE = "Error : invalid JSON file."
ERR_GCD = "Error : called gcd with param a or b == 0."
 
class SolarSystem(object):
    """ Class containing the informations on a solar system.

    Attributes:
        star (Star): The solar system's star.
        planets (list of Planets): The solar system's planets.
    """
    def __init__(self, star, planets):
        """ Creates an instance of solar system.
        """
        self.star = star
        self.planets = planets   
 
class Star(object):
    """ Class containing the informations on a star.

    Attributes:
        radius (float): The star's radius.
        color (int, int, int): The star's RGB colors.
        location (float, float, float): The star's xyz location.
    """    
    def __init__(self, radius, color):
        """ Creates an instance of star. 
        """
        self.radius = radius
        self.color = color
        self.location = (0.0, 0.0, 0.0)

class Planet(object):
    """ Class containing the information on a planet.

    Attributes:
        radius (float): The planet's radius
        color (int, int, int): The planet's RGB colors.
        distance (float): The planet's distance to the star.
        period (int): The number of frames required for the planet to
                      complete an orbit around the star.
        location (float, float, float): The planet's xyz location.
    """ 
    def __init__(self, radius, color, distance, period):
        """ Creates an instance of planet.
        """
        self.radius = radius
        self.color = color
        self.distance = distance
        self.period = period
        self.location = (distance, 0, 0)
   
def loadSolarSystem(params):
    """ Parses the argv parameters and returns the solar system
    specified in file params[0] if the parameters are valid.
    
    Args:
        params (list of string): The argv parameters.
    """
    nbParams = len(params)

    # Verifying param count
    if (nbParams != 2):
        print(ERR_NB_PARAMS.format(nbParams))
        sys.exit(0)
    
    file = params[0]
    cwd = os.path.dirname(os.path.realpath(__file__))
    solarSystemFile = cwd + "/" + file

    # Fetching json data from file
    try:
        jsonData = json.loads(open(solarSystemFile).read())
    except:
        print(ERR_INV_FILE.format(file))
        sys.exit(0)

    # Parsing json file data
    try:
        starData = jsonData.get('star')
        planetsData = jsonData.get('planets')       
        radius = starData.get('radius')
        color = starData.get('color')
        star = Star( radius, color )
        planets = []

        for p in planetsData:
            radius = p.get('radius')
            color = p.get('color')
            distance = p.get('distance-from-star')         
            period = p.get('period')
            planets.append( Planet(radius, color, distance, period) )
    except:
        print(ERR_INV_JSON_FILE)     
        sys.exit(0)
    
    return SolarSystem( star, planets )
    
""" Main
"""
params = sys.argv[sys.argv.index("--")+1:]
solarSystem = loadSolarSystem(params)

# Default scene clean-up
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Camera'].select = True
bpy.data.objects['Cube'].select = True
bpy.data.objects['Lamp'].select = True
bpy.ops.object.delete()
        
# Creating a black background
bpy.context.scene.world.horizon_color = (0, 0, 0)

# Creating camera
d_max = max( [p.distance for p in solarSystem.planets] )
bpy.ops.object.camera_add(view_align=False, location=(0, 0, 3*d_max ), rotation=(0, 0, 0))
bpy.context.active_object.name = 'Camera'

# creating hemi light source
bpy.ops.object.lamp_add(type='HEMI', location=(0, 0, 1.5*d_max), rotation=(0,0,0))
bpy.context.active_object.name = 'Hemi'
bpy.data.lamps['Hemi'].color = solarSystem.star.color
bpy.data.lamps['Hemi'].energy = 0.1

# creating point light source
bpy.ops.object.lamp_add(type='POINT', location=(0, 0, 0))
bpy.context.active_object.name= 'Point'
    
# Creating mesh, texture for star.
starMaterial = bpy.data.materials.new('starMaterial')
starMaterial.emit = 100
starMaterial.diffuse_color = solarSystem.star.color
bpy.ops.mesh.primitive_uv_sphere_add(size=solarSystem.star.radius, location=(0,0,0))
bpy.ops.object.shade_smooth()
bpy.context.active_object.name = 'Star'
bpy.context.active_object.data.materials.append(starMaterial)
        
for i, p in enumerate(solarSystem.planets):

    # Creating meshes and textures for planets
    planetMaterial = bpy.data.materials.new('planetMaterial{}'.format(i))
    planetMaterial.diffuse_color = p.color
    bpy.ops.mesh.primitive_uv_sphere_add(size=p.radius,location=p.location)
    bpy.ops.object.shade_smooth()
    bpy.context.active_object.name = 'Planet{}'.format(i)
    bpy.context.active_object.data.materials.append(planetMaterial)

    # Creating rotating arrows. Defining parenthood relationships
    bpy.ops.object.empty_add(type='SINGLE_ARROW')
    bpy.context.active_object.name = 'Arrow{}'.format(i)

    planet = bpy.data.objects['Planet{}'.format(i)]
    arrow = bpy.data.objects['Arrow{}'.format(i)]
    planet.parent = arrow        
    bpy.context.scene.objects.active = bpy.data.objects['Arrow{}'.format(i)]

    # Creating keyframes.
    bpy.context.scene.frame_set(0)
    bpy.context.active_object.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.active_object.keyframe_insert(data_path="rotation_euler")

    bpy.context.scene.frame_set(p.period)
    bpy.context.active_object.rotation_euler = (0.0, 0.0, 2*pi)
    bpy.context.active_object.keyframe_insert(data_path="rotation_euler")
    bpy.context.active_object.animation_data.action.fcurves[2] \
        .keyframe_points[0].interpolation = 'LINEAR'
    bpy.context.active_object.animation_data.action.fcurves[2] \
        .modifiers.new(type="CYCLES")
        
# Setting up start en end noFrame for a 10 seconds animation 
# at 24 frames per seconds
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 240

# Rendering and saving animation
bpy.context.scene.render.filepath = params[1]
bpy.context.scene.render.use_file_extension = False
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'OGG'
bpy.context.scene.render.ffmpeg.gopsize = 0
bpy.context.scene.render.ffmpeg.constant_rate_factor = 'LOSSLESS'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.camera = bpy.data.objects['Camera']
bpy.ops.render.render(animation=True)
