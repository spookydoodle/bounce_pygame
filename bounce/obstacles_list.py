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
        'size': {'width': 300, 'height': 50}
        },
    
    'P_02' : {
        'type' : 1,
        'position': {'x': 300, 'y': 700}, 
        'size': {'width': 300, 'height': 50}
        }
    }
            

        