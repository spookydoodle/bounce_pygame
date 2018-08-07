class MockRect:
    """
    A mock replacement of `pygame.sprite.Sprite.rect` for testing purposes
    """
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    @property
    def x(self):
        return self.left

    @property 
    def y(self):
        return self.top

    @property
    def width(self):
        return (self.right - self.left)

    @property
    def height(self):
        return (self.bottom - self.top)

# Utility methods to make tests more readable
def makeMockRect(other_rectangle):
    return MockRect(
        other_rectangle.top,
        other_rectangle.bottom,
        other_rectangle.left,
        other_rectangle.right
    )

def shifted(base_rect, x_shift=0, y_shift=0):
    return MockRect(
        base_rect.top + y_shift,
        base_rect.bottom + y_shift,
        base_rect.left + x_shift,
        base_rect.right + x_shift
    )
