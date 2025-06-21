import pygame

def draft_intro_scene(save_file):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Draft Manager")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((20, 20, 60))

        title = font.render(f"Draft Starting for {save_file}", True, (255, 255, 255))
        screen.blit(title, (100, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
