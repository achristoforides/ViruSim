import pygame

class UIPanel:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect((self.x, self.y), (self.width, self.height)))

    def render_panel_title_text(self, surface, text, font, color):
        rendered_text = font.render(text, True, color)
        rect = rendered_text.get_rect()

        rect.center = (self.x + (self.width / 2), self.y + (font.size(text)[1]) / 2)
        surface.blit(rendered_text, rect)

