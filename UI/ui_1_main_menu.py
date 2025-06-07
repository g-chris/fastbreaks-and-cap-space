import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FANTASY FANTASY BASKETBALL")

# Fonts and colors
font_title = pygame.font.SysFont("Arial", 48)
font_button = pygame.font.SysFont("Arial", 32)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Button data
buttons = [
    {"label": "Save File 1", "rect": pygame.Rect(200, 120, 200, 50), "db_name": "league01.db"},
    {"label": "Save File 2", "rect": pygame.Rect(200, 190, 200, 50), "db_name": "league02.db"},
    {"label": "Save File 3", "rect": pygame.Rect(200, 260, 200, 50), "db_name": "league03.db"},
]

selected_db = None

def draw_menu():
    screen.fill(BLACK)

    # Draw title
    title_surface = font_title.render("FF BBALL", True, WHITE)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 40))

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        rect = button["rect"]
        color = GRAY if rect.collidepoint(mouse_pos) else DARK_GRAY
        pygame.draw.rect(screen, color, rect)
        text_surface = font_button.render(button["label"], True, WHITE)
        screen.blit(
            text_surface,
            (rect.x + rect.width // 2 - text_surface.get_width() // 2,
             rect.y + rect.height // 2 - text_surface.get_height() // 2)
        )

    pygame.display.flip()

def main_menu():
    global selected_db
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        selected_db = button["db_name"]
                        print(f"Selected: {selected_db}")
                        return selected_db  # Use this to start the next step

# Run the menu
if __name__ == "__main__":
    db_name = main_menu()
    # Proceed to rest of your game logic using db_name
    pygame.quit()
    print(f"Starting game with save file: {db_name}")
