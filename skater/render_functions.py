def draw_text(screen, text, font, color, side, side_px, top_px):
    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    if side == "R": text_screen_rect.right = side_px
    if side == "L": text_screen_rect.left = side_px

    screen.blit(text_screen, text_screen_rect)


def draw_sprite(screen, sprite):

    screen.blit(sprite.image, sprite.rect)