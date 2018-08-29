"""
    Types description:
    1 - platform / rectangular shape
    2 - line
"""

OBSTACLES = {

    # floor
    'P_01' : {
        'type' : 1,
        'position': {'x': 0, 'y': 0}, 
        'size': {'width': 400, 'height': 50}
        },
    
    'P_02' : {
        'type' : 1,
        'position': {'x': 400, 'y': 0}, 
        'size': {'width': 400, 'height': 50}
        },

    'W_01' : {
        'type' : 1,
        'position': {'x': 100, 'y': -420}, 
        'size': {'width': 50, 'height': 420}
        },
    
    'W_02' : {
        'type' : 1,
        'position': {'x': 300, 'y': -500}, 
        'size': {'width': 50, 'height': 500}
        },
    
    'W_03' : {
        'type' : 1,
        'position': {'x': 500, 'y': -390}, 
        'size': {'width': 50, 'height': 390}
        }
    }
            

        