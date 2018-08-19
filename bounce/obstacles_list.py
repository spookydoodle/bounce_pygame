"""
    Types description:
    1 - platform / rectangular shape
    2 - line
"""

OBSTACLES = {
    # Outer left wall
    'W_01' : {
        'type' : 1,
        'position': {'x': 0, 'y': 0}, 
        'size': {'width': 50, 'height': 800}
        },

    # Outer right wall
    'W_02' : {
        'type' : 1,
        'position': {'x': 550, 'y': 0}, 
        'size': {'width': 50, 'height': 800}
        },

    # floor
    'P_01' : {
        'type' : 1,
        'position': {'x': 0, 'y': 700}, 
        'size': {'width': 600, 'height': 50}
        },
    
    
    'W_03' : {
        'type' : 1,
        'position': {'x': 150, 'y': 75}, 
        'size': {'width': 50, 'height': 250}
        },

    'W_04' : {
        'type' : 1,
        'position': {'x': 450, 'y': 275}, 
        'size': {'width': 50, 'height': 250}
        },

    'W_05' : {
        'type' : 1,
        'position': {'x': 150, 'y': 475}, 
        'size': {'width': 50, 'height': 250}
        }

    }
            

        