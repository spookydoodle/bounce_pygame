def draw_text(screen, text, font, color, side, side_px, top_px):

    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    if side == "R": text_screen_rect.right = side_px
    if side == "L": text_screen_rect.left = side_px

    screen.blit(text_screen, text_screen_rect)


def draw_rect(screen, camera, rect, image = None):

    rendering_position = (rect.x - camera.x, rect.y - camera.y)
    screen.blit(image.raw_image, rendering_position)


def draw_line(screen, camera, start_pos, end_pos, color):

    start_rendering_position = (start_pos.x - camera.x, start_pos.y - camera.y)
    end_rendering_position = (start_pos.x - camera.x, start_pos.y - camera.y)

    pygame.draw.line(screen, color, start_rendering_position, end_rendering_position, width=1)