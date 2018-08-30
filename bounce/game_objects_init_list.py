GAME_OBJECT_TYPES = {
    1 : "walls",
    2 : "collectables",
    3 : "obstacles"
    }

GAME_OBJECTS = {

    # floor, type 1
    'F_01' : {
        'type' : 1,
        'position': {'x': 0, 'y': 0}, 
        'size': {'width': 800, 'height': 50}
        },

    # walls, type 1
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
        },

    # collectables, type 2
    'C_01' : {
        'type' : 2,
        'position': {'x': 170, 'y': -400}, 
        'size': {'width': 50, 'height': 50}
        },
    
    'C_02' : {
        'type' : 2,
        'position': {'x': 430, 'y': -1000}, 
        'size': {'width': 50, 'height': 50}
        },

    # obstacles, type 3


    }
