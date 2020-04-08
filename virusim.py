import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from ui_helper import *

if __name__ == "__main__":
    running = True
    
    app_title = "ViruSim"
    app_dimensions = (1280, 720)

    pygame.font.init()
    UI_TITLE_FONT = pygame.font.SysFont('Consolas', 32)

    # Create the window
    surface = pygame.display.set_mode(size=app_dimensions, flags=pygame.DOUBLEBUF)
    pygame.display.flip()

    # Set window title
    pygame.display.set_caption(app_title)

    clock = pygame.time.Clock()

    # Temporary colors
    GRAY = (100, 100, 100)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    background = GRAY

    # Setup UI panels
    graph_panel = UIPanel(15, 15, 350, 350, (255, 0, 0))
    param_panel = UIPanel(15, 380, 350, 325, (0, 255, 0))
    simul_panel = UIPanel(380, 15, 885, 600, (0, 0, 255))
    stats_panel = UIPanel(380, 630, 885, 75, (0, 255, 255))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    background = RED
                elif event.key == pygame.K_y:
                    background = YELLOW

        surface.fill(background)

        # Sketch out locations of UI elements
        graph_panel.draw(surface)
        graph_panel.render_panel_title_text(surface, "Graph", UI_TITLE_FONT, (0, 0, 0))
        param_panel.draw(surface)
        param_panel.render_panel_title_text(surface, "Parameters", UI_TITLE_FONT, (0, 0, 0))
        simul_panel.draw(surface)
        simul_panel.render_panel_title_text(surface, "Simulation Space", UI_TITLE_FONT, (0, 0, 0))
        stats_panel.draw(surface)
        stats_panel.render_panel_title_text(surface, "Statistics", UI_TITLE_FONT, (0, 0, 0))
        
        # Update the window
        pygame.display.update()
