
class Camera:
    LAG = 0.01

    def __init__(self):
        self.x = 0
        self.y = 0        

    def adjust(self, screen, player):
        self.adjust_x(screen.get_rect(), player.rect)
        self.adjust_y(screen.get_rect(), player.rect)


    def adjust_x(self, screen_rect, player_rect):
        """
        Computes the required camera adjustment depending on player's location and camera's current x shift
        """
        margin_left = 0.7
        margin_right = 0.7

        # point when camera should move down / up dependent on player's vertical position on the screen
        cam_thresh_left = margin_left * screen_rect.width
        cam_thresh_right = margin_right * screen_rect.width

        # compute camera / player coordinates on the screen
        player_position = player_rect.x + player_rect.width / 2
        camera_focus = self.x + screen_rect.width / 2

        relative_player_position = player_position - camera_focus

        if relative_player_position > cam_thresh_right or relative_player_position < -1 * cam_thresh_left:
            # player is outside of camera's focus -> move camera
            self.x += relative_player_position * self.LAG

        else:
            # player is within camera's focus -> do nothing
            pass

    def adjust_y(self, screen_rect, player_rect):
            """
            see `adjust_x`
            """
            margin_top = 0.3
            margin_bottom = 0.3

            cam_thresh_top = margin_top * screen_rect.height
            cam_thresh_bottom = margin_bottom * screen_rect.height

            player_position = player_rect.y + player_rect.height / 2
            camera_focus = self.y + screen_rect.height

            relative_player_position = player_position - camera_focus

            if relative_player_position < -1 * cam_thresh_bottom or relative_player_position > cam_thresh_top:
                # player is outside of camera's focus -> move camera
                self.y += relative_player_position * self.LAG

            else:
                # player is within camera's focus -> do nothing
                pass
