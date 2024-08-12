import pygame
import random
import math


pygame.init()


WIDTH, HEIGHT = 800, 600 # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Sand Simulator")


BACKGROUND_COLOR = (30, 30, 30)
OPTIONS_BG_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_BORDER_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 255, 0)  


GRID_SIZE = 4
cols, rows = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE


grid = [[None for _ in range(cols)] for _ in range(rows)]


max_grains = 500
grain_themes = {
    "Rainbow": lambda y: rainbow_color(y),
    "Mountain": lambda y: (int(139 * (1 - y / rows)), int(69 * (1 - y / rows)), int(19 * (1 - y / rows))),
    "Nature": lambda y: (int(34 * (y / rows)), int(139 * (y / rows)), int(34 * (1 - y / rows))),
    "Beach": lambda y: (int(244 * (1 - y / rows)), int(164 * (1 - y / rows)), int(96 * (1 - y / rows))),
    "Desert": lambda y: (int(255 * (1 - y / rows)), int(228 * (1 - y / rows)), int(169 * (1 - y / rows))),
    "Moon": lambda y: moon_color(y)
}
current_theme = "Rainbow"
options_menu = False
gradient_menu = False
font = pygame.font.Font(None, 36)

button_width = 300
button_height = 50
preview_size = 50



def rainbow_color(y):
    hue = (pygame.time.get_ticks() / 5000 + y / rows) % 1.0
    r = int(255 * (0.5 + 0.5 * math.sin(2 * math.pi * hue)))
    g = int(255 * (0.5 + 0.5 * math.sin(2 * math.pi * hue + 2)))
    b = int(255 * (0.5 + 0.5 * math.sin(2 * math.pi * hue + 4)))
    return (r, g, b)


def moon_color(y):
    grey_value = int(255 * (1 - y / rows))
    if random.random() < 0.1:  
        return (grey_value, grey_value, grey_value)
    return (grey_value, grey_value, grey_value)


def add_sand(x, y):
    if 0 <= x < cols and 0 <= y < rows and grid[y][x] is None:
        grid[y][x] = grain_themes[current_theme](y)


def update_sand():
    for y in range(rows - 2, -1, -1):
        for x in range(cols):
            if grid[y][x] is not None:
                if grid[y + 1][x] is None:  
                    grid[y + 1][x] = grid[y][x]
                    grid[y][x] = None
                elif x > 0 and grid[y + 1][x - 1] is None:  
                    grid[y + 1][x - 1] = grid[y][x]
                    grid[y][x] = None
                elif x < cols - 1 and grid[y + 1][x + 1] is None:  
                    grid[y + 1][x + 1] = grid[y][x]
                    grid[y][x] = None


def draw_grid():
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] is not None:
                color = grid[y][x]
                pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_pixel_art(surface, art, position, pixel_size):
    width, height = surface.get_size()
    surface.fill((0, 0, 0))  
    
    for y, row in enumerate(art):
        for x, color in enumerate(row):
            if color:
                pygame.draw.rect(surface, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))



def draw_main_menu():
    screen.fill(OPTIONS_BG_COLOR)
    
    title_text = font.render("Pixel Sand Simulator", True, rainbow_color(0))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    grains_text = font.render(f"Max Grains: {max_grains}", True, TEXT_COLOR)
    screen.blit(grains_text, (WIDTH // 2 - grains_text.get_width() // 2, 150))
    
    pygame.draw.rect(screen, TEXT_COLOR, (WIDTH // 2 - 100, 190, 200, 30), 2)
    pygame.draw.rect(screen, TEXT_COLOR, (WIDTH // 2 - 100 + int((max_grains / 1000) * 200), 190, 10, 30))
    
    gradient_text = font.render("Gradient Menu", True, TEXT_COLOR)
    screen.blit(gradient_text, (WIDTH // 2 - gradient_text.get_width() // 2, 250))
    
    exit_text = font.render("Exit", True, TEXT_COLOR)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 350))
    
    pygame.display.flip()


def draw_gradients_menu():
    screen.fill(OPTIONS_BG_COLOR)
    
    gradient_text = font.render("Select Gradient", True, TEXT_COLOR)
    screen.blit(gradient_text, (WIDTH // 2 - gradient_text.get_width() // 2, 50))
    
    y_offset = 150
    button_width = 300
    button_height = 50
    preview_size = 50

    gradients = {
        "Rainbow": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [[rainbow_color(i) for i in range(preview_size)] for _ in range(preview_size)],
                (0, 0),
                1
            )
        ],
        "Mountain": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [
                    [None, None, (139, 69, 19), (139, 69, 19), None],
                    [None, (139, 69, 19), (139, 69, 19), (139, 69, 19), None],
                    [(139, 69, 19), (139, 69, 19), (139, 69, 19), (139, 69, 19), (139, 69, 19)],
                    [(139, 69, 19), (139, 69, 19), (139, 69, 19), (139, 69, 19), None],
                    [None, (139, 69, 19), None, None, None]
                ],
                (0, 0),
                10
            )
        ],
        "Nature": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [
                    [None, (34, 139, 34), None, None, (34, 139, 34)],
                    [(34, 139, 34), (34, 139, 34), None, (34, 139, 34), None],
                    [None, None, (34, 139, 34), None, None],
                    [None, (34, 139, 34), None, (34, 139, 34), None],
                    [None, None, (34, 139, 34), None, None]
                ],
                (0, 0),
                10
            )
        ],
        "Beach": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [
                    [(244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96), None],
                    [(244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96)],
                    [(244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96)],
                    [(244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96), (244, 164, 96)],
                    [None, None, (0, 191, 255), None, None]
                ],
                (0, 0),
                10
            )
        ],
        "Desert": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [
                    [None, None, (255, 228, 169), (255, 228, 169), None],
                    [(255, 228, 169), (255, 228, 169), (255, 228, 169), (255, 228, 169), None],
                    [(255, 228, 169), (255, 228, 169), (255, 228, 169), (255, 228, 169), (0, 128, 0)],
                    [(255, 228, 169), (255, 228, 169), (255, 228, 169), (255, 228, 169), (0, 128, 0)],
                    [None, (0, 128, 0), None, None, None]
                ],
                (0, 0),
                10
            )
        ],
        "Moon": [
            pygame.Surface((preview_size, preview_size)),
            lambda: draw_pixel_art(
                pygame.Surface((preview_size, preview_size)),
                [
                    [(192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192)],
                    [(192, 192, 192), (192, 192, 192), None, (192, 192, 192)],
                    [(192, 192, 192), None, None, (192, 192, 192)],
                    [(192, 192, 192), (192, 192, 192), (192, 192, 192), (192, 192, 192)]
                ],
                (0, 0),
                10
            )
        ]
    }

  


    for theme, (surface, draw_func) in gradients.items():
        draw_func()
        theme_rect = pygame.Rect(WIDTH // 2 - button_width // 2, y_offset, button_width, button_height)
        screen.blit(surface, theme_rect)
        
        theme_option = font.render(theme, True, TEXT_COLOR)
        screen.blit(theme_option, (WIDTH // 2 - theme_option.get_width() // 2, y_offset + (button_height - theme_option.get_height()) // 2))
        
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, theme_rect, 2)
        if theme == current_theme:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, theme_rect, 5)
        
        y_offset += button_height + 10
    
    pygame.display.flip()


def change_background_color():
    if options_menu:
        return (50, 50, 50)
    return BACKGROUND_COLOR


running = True
mouse_down = False

while running:
    screen.fill(change_background_color())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if options_menu:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if gradient_menu:
                    y_offset = 150
                    for theme in grain_themes.keys():
                        if WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2 and y_offset <= mouse_y <= y_offset + button_height:
                            current_theme = theme
                            gradient_menu = False
                            break
                        y_offset += button_height + 10
                else:
                    if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and 190 <= mouse_y <= 220:
                        max_grains = int(((mouse_x - (WIDTH // 2 - 100)) / 200) * 1000)
                    elif WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2 and 250 <= mouse_y <= 250 + button_height:
                        gradient_menu = True
                    elif WIDTH // 2 - 50 <= mouse_x <= WIDTH // 2 + 50 and 350 <= mouse_y <= 380:
                        running = False
            else:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                options_menu = not options_menu
                gradient_menu = False
    
    if not options_menu:
        if mouse_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // GRID_SIZE, mouse_y // GRID_SIZE
            for _ in range(max_grains // 100):
                add_sand(grid_x + random.randint(-1, 1), grid_y + random.randint(-1, 1))
        update_sand()
        draw_grid()
    elif gradient_menu:
        draw_gradients_menu()
    else:
        draw_main_menu()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()