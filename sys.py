"""
UQAM - Winter 2018 - INF5017 - Group 20 - q4.py

Program used to launch the blender script "q4-blenderscript.py",
which is used to generate an animation of the solar system
specified in a json file. The produced video file format is OGG. 

    $ python q4.py [INPUT_FILE] [OUTPUT_FILE]

    INPUT_FILE      The json file containing the information on the solar system
                    to render.
    OUTPUT_FILE     The filename for the rendered animation.

author : Alexis Chretien (CHRA25049209)
date : March 1st, 2018
"""
import subprocess
import sys

command = ["blender"]
params = ["--background", "--python", "sys-blenderscript.py", "--"]

if (len(sys.argv) > 1):
    params.extend( sys.argv[1:] )

command.extend( params )
subprocess.call( command )
