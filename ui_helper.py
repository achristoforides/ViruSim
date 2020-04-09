import pygame

class UIPanel:
    def __init__(self, x, y, width, height, color, text, font, textcolor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = font
        self.textcolor = textcolor

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect((self.x, self.y), (self.width, self.height)))

    def render_panel_title_text(self, surface):
        rendered_text = self.font.render(self.text, True, self.textcolor)
        rect = rendered_text.get_rect()

        rect.center = (self.x + (self.width / 2), self.y + (self.font.size(self.text)[1]) / 2)
        surface.blit(rendered_text, rect)

    def get_title_height(self):
        return self.font.size(self.text)[1]
