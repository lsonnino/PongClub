from game import *

WIN_SIZE = (700, 700)
FPS = 30

FONT = "Arial"
FONT_SIZE = 20
TEXT_COLOR = PLAYER_COLOR

BACKGROUND_COLOR = (77, 77, 77)


def game(name, number_of_ai, first_agent=None, second_agent=None):
    # Engine materials

    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption(name)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT, FONT_SIZE)

    # Game materials

    game = Game(WIN_SIZE, number_of_ai, first_agent, second_agent)

    # Running the game

    running = True
    while running:
        for event in pygame.event.get():
            # Check special events
            if event.type == pygame.QUIT:  # Quit
                running = False
                playing = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
            continue

        window.fill(BACKGROUND_COLOR)

        game.step()

        game.draw(window)

        text_surface = font.render(str(game.score[0]) + " - " + str(game.score[1]), False, TEXT_COLOR)
        window.blit(text_surface, ( (WIN_SIZE[0] - text_surface.get_width()) / 2, 10))

        pygame.display.update()
        clock.tick(FPS)
