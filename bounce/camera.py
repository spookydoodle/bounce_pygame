from silnik.rendering.point import Point

class Camera:
    LAG = 0.02

    def __init__(self, focus_shift=None):
        self.x = 0
        self.y = 0
        self.focus_shift = focus_shift or Point(0, 0)

    def adjust(self, screen, player):
        self.adjust_x(screen.get_rect(), player.rect)
        self.adjust_y(screen.get_rect(), player.rect)

    def focus_point(self, focus_object):
        """
        Computes the point the camera should focus: `focus_object.center` + `self.focus_shift`
        """
        return focus_object.centre() + self.focus_shift

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
        focus_point = self.focus_point(player_rect)
        player_position = focus_point.x
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
            margin_top = 0.1
            margin_bottom = 0.1

            cam_thresh_top = margin_top * screen_rect.height
            cam_thresh_bottom = margin_bottom * screen_rect.height

            focus_point = self.focus_point(player_rect)
            player_position = focus_point.y
            camera_focus = self.y + screen_rect.height / 2

            relative_player_position = player_position - camera_focus

            if relative_player_position < -1 * cam_thresh_bottom or relative_player_position > cam_thresh_top:
                # player is outside of camera's focus -> move camera
                self.y += relative_player_position * self.LAG

            else:
                # player is within camera's focus -> do nothing
                pass
