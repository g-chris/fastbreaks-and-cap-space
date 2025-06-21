import pygame
from UI.ui_2_draft_intro import draft_intro_scene

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Fastbreaks and Cap Space")
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    save_slots = ["Save File 1", "Save File 2", "Save File 3"]
    buttons = []
    for i, label in enumerate(save_slots):
        rect = pygame.Rect(300, 150 + i * 100, 200, 50)
        buttons.append((rect, label))

    running = True
    while running:
        screen.fill((30, 30, 30))

        title = font.render("FASTBREAKS AND CAP SPACE", True, (255, 255, 255))
        screen.blit(title, (120, 50))

        for rect, label in buttons:
            pygame.draw.rect(screen, (70, 70, 200), rect)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.x + 10, rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (rect, label) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        # Launch next scene with selected save file
                        save_file = f"league0{i+1}.db"
                        draft_intro_scene(save_file)  # Pass selected file
                        return  # Exit main_menu

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
