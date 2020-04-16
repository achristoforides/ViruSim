import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import thorpy

from ui_helper import *

if __name__ == "__main__":
    running = True
    
    app_title = "ViruSim"
    app_dimensions = (1280, 720)

    pygame.font.init()
    UI_TITLE_FONT = pygame.font.SysFont('Consolas', 32)
    STATS_FONT = pygame.font.SysFont('Consolas', 18)

    # Create the window
    surface = pygame.display.set_mode(size=app_dimensions, flags=pygame.DOUBLEBUF)
    pygame.display.flip()

    # Set window title
    pygame.display.set_caption(app_title)

    clock = pygame.time.Clock()

    background = (100, 100, 100)

    # Setup UI panels
    graph_panel = UIPanel(15, 15, 350, 350, (255, 0, 0), 'Graph', UI_TITLE_FONT, (0, 0, 0))
    param_panel = UIPanel(15, 380, 350, 325, (0, 255, 0), 'Parameters', UI_TITLE_FONT, (0, 0, 0))
    simul_panel = UIPanel(380, 15, 885, 600, (0, 0, 255), 'Simulation Area', UI_TITLE_FONT, (0, 0, 0))
    stats_panel = UIPanel(380, 630, 885, 75, (0, 255, 255), 'Statistics', UI_TITLE_FONT, (0, 0, 0))

    STATS_PADDING = 30
    susceptible_text = STATS_FONT.render("Susceptible: 0", True, (0, 0, 0))
    infected_text = STATS_FONT.render("Infected: 0", True, (0, 0, 0))
    removed_text = STATS_FONT.render("Removed: 0", True, (0, 0, 0))

    # UI max values
    max_infection_chance = 1.0
    infection_chance_default_value = 0.5
    max_infection_radius = 10
    infection_radius_default_value = 5
    max_population = 10000
    population_default_value = 100
    
    # Setup simulation parameter UI elements
    infection_chance_slider = thorpy.SliderX(100, (0.0, max_infection_chance), 'Infection Chance', initial_value=infection_chance_default_value)
    infection_radius_slider = thorpy.SliderX(100, (0, max_infection_radius), 'Infection Radius', type_=int, initial_value=infection_radius_default_value)
    population_textbox = thorpy.Inserter(name="Population: ", value=str(population_default_value))
    run_sim_button = thorpy.make_button('Run Simulation', func=sys.exit)

    param_box = thorpy.Box(elements=[infection_chance_slider,infection_radius_slider,population_textbox, run_sim_button])
    
    simulation_parameters_menu = thorpy.Menu(param_box)
    for element in simulation_parameters_menu.get_population():
        element.surface = surface

    param_box.set_topleft((15, 380 + param_panel.get_title_height()))
    param_box.blit()
    param_box.update()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            simulation_parameters_menu.react(event)

        surface.fill(background)
        
        # Sketch out locations of UI elements
        graph_panel.draw(surface)
        graph_panel.render_panel_title_text(surface)
        param_panel.draw(surface)
        param_panel.render_panel_title_text(surface)
        simul_panel.draw(surface)
        simul_panel.render_panel_title_text(surface)
        stats_panel.draw(surface)
        stats_panel.render_panel_title_text(surface)

        # Draw stats text
        surface.blit(susceptible_text, (395, 630 + stats_panel.get_title_height()))
        surface.blit(infected_text, (STATS_PADDING + 395 + susceptible_text.get_width(), 630 + stats_panel.get_title_height()))
        surface.blit(removed_text, (STATS_PADDING * 2 + 395 + susceptible_text.get_width() + infected_text.get_width(), 630 + stats_panel.get_title_height()))        
        
        # Draw UI Elements
        param_box.blit()
            
        # Update the window
        pygame.display.update()

        clock.tick(60)
