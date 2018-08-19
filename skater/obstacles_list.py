"""
    Types description:
    1 - platform / rectangular shape
    2 - line
"""

OBSTACLES = {

    'P_01' : {
        'type' : 1,
        'position': {'x': 0, 'y': 600}, 
        'size': {'width': 1200, 'height': 50}
        },

    'P_02' : {
        'type' : 1,
        'position': {'x': 1200, 'y': 700}, 
        'size': {'width': 800, 'height': 50}
        },

    'P_03' : {
        'type' : 1,
        'position': {'x': 500, 'y': 575}, 
        'size': {'width': 300, 'height': 25}
        },

    'P_04' : {
        'type' : 1,
        'position': {'x': 0, 'y': 200}, 
        'size': {'width': 50, 'height': 400}
        },

    #'P_05' : {
    #    'type' : 1,
    #    'position': {'x': 1950, 'y': 350}, 
    #    'size': {'width': 50, 'height': 400}
    #    },

    'L_01' : {
        'type' : 2,
        'start_position' : {'x': 2000, 'y': 600}, 
        'end_position' : {'x': 2200, 'y': 800}, 
        'size': {'width': 50, 'height': 50}
        }

    }
            

        