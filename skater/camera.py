
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0        

    def adjust(self, screen, player):
        
        LAG = 0.01

        self.adjust_x(screen, player, LAG)
        self.adjust_y(screen, player, LAG)


    def adjust_x(self, screen, player, lag):
        """
        Computes the required camera adjustment depending on player's location and camera's current x shift
        """
        margin_left = 0.2
        margin_right = 0.3

        # point when camera should move down / up dependent on player's vertical position on the screen
        cam_thresh_left = margin_left * screen.get_rect().width
        cam_thresh_right = margin_right * screen.get_rect().width

        # compute camera / player coordinates on the screen
        player_position = player.rect.x + player.rect.width / 2
        camera_focus = self.x + screen.get_rect().width / 2

        relative_player_position = player_position - camera_focus

        if relative_player_position > cam_thresh_right or relative_player_position < -1 * cam_thresh_left:
            # player is outside of camera's focus -> move camera
            self.x += relative_player_position * lag

        else:
            # player is within camera's focus -> do nothing
            pass

    def adjust_y(self, screen, player, lag):
            """
            see `adjust_x`
            """
            margin_top = 0.3
            margin_bottom = 0.5

            cam_thresh_top = margin_top * screen.get_rect().height
            cam_thresh_bottom = margin_bottom * screen.get_rect().height

            player_position = player.rect.y + player.rect.height / 2
            camera_focus = self.y + screen.get_rect().height / 2

            relative_player_position = player_position - camera_focus

            if relative_player_position < -1 * cam_thresh_bottom or relative_player_position > cam_thresh_top:
                # player is outside of camera's focus -> move camera
                self.y += relative_player_position * lag

            else:
                # player is within camera's focus -> do nothing
                pass
