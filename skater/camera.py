
class Camera:

    def __init__(self):
        self.x = 0
        self.y = 0
        

    def adjust(self, screen, player):
        
        LAG = 0.99

        self.adjust_x(screen, player, LAG)
        self.adjust_y(screen, player, LAG)


    def adjust_x(self, screen, player, lag):
        """
        Changes camera x parameteres depending on the location of the player on screen x axis
        """
        MARGIN_LEFT = 0.2
        MARGIN_RIGHT = 0.5

        # point when camera should move down / up dependent on player's vertical position on the screen
        cam_thresh_left = screen.get_rect().x + MARGIN_LEFT * screen.get_rect().width
        cam_thresh_right = screen.get_rect().x + MARGIN_RIGHT * screen.get_rect().width

        if player.rect.x < cam_thresh_left:

            ##### hey rwa: with this commented code below the game looks a lot less smooth 
            ##### and distances between obstacles are not correct.

            #self.x -= abs(player.rect.x - cam_thresh_left) * lag
            self.x -= 1
            
        elif player.rect.x > cam_thresh_right:
            #self.x += abs(player.rect.x - cam_thresh_right) * lag
            self.x += 1

        else: 
            self.x = 0


    def adjust_y(self, screen, player, lag):
        """
        Changes camera y parameteres depending on the location of the player on screen y axis
        """
        MARGIN_TOP = 0.3
        MARGIN_BOTTOM = 0.6

        # point when camera should move down / up dependent on player's vertical position on the screen
        cam_thresh_up = screen.get_rect().y + MARGIN_TOP * screen.get_rect().height
        cam_thresh_down = screen.get_rect().y + MARGIN_BOTTOM * screen.get_rect().height

        if player.rect.y < cam_thresh_up:
            #self.y -= abs(player.rect.y - cam_thresh_up) * lag
            self.y -= 1

        elif player.rect.y > cam_thresh_down:
            #self.y += abs(player.rect.y - cam_thresh_down)
            self.y += 1

        else: 
            self.y = 0