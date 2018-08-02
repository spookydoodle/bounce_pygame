
class Camera:

    def __init__(self):
        self.x = 0
        self.y = 0

        # not sure if these parameters should be placed here or inside the adjust_x and adjust_y functions???
        self.margin_left = 0.2
        self.margin_right = 0.5
        self.margin_top = 0.3
        self.margin_bottom = 0.6


    def adjust(self, screen, player):
        self.adjust_x(screen, player)
        self.adjust_y(screen, player)


    def adjust_x(self, screen, player):
        """
        Changes camera x parameteres depending on the location of the player on screen x axis
        """
        if player.rect.x > (screen.get_rect().x + self.margin_right * screen.get_rect().width):
            self.x += 1

        elif player.rect.x < (screen.get_rect().x + self.margin_left * screen.get_rect().width):
            self.x -= 1

        else: 
            self.x = 0


    def adjust_y(self, screen, player):
        """
        Changes camera y parameteres depending on the location of the player on screen y axis
        """
        if player.rect.y > (screen.get_rect().y + self.margin_bottom * screen.get_rect().height):
            self.y += 1

        elif player.rect.y < (screen.get_rect().y + self.margin_top * screen.get_rect().height):
            self.y -= 1

        else: 
            self.y = 0