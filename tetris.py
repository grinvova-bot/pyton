import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
CELL_SIZE = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Цвета фигур
SHAPE_COLORS = [CYAN, MAGENTA, YELLOW, GREEN, RED, BLUE, ORANGE]

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Тетрис')

# Игровое поле
grid = [[0] * (SCREEN_WIDTH // CELL_SIZE) for _ in range(SCREEN_HEIGHT // CELL_SIZE)]

# Класс фигуры
class Shape:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = SCREEN_WIDTH // CELL_SIZE // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE + x * CELL_SIZE, self.y * CELL_SIZE + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# Создание новой фигуры
def create_shape():
    shape = random.choice(SHAPES)
    color = SHAPE_COLORS[SHAPES.index(shape)]
    return Shape(shape, color)

# Проверка столкновений
def check_collision(shape, dx, dy):
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = shape.x + x + dx
                new_y = shape.y + y + dy
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid) or grid[new_y][new_x]:
                    return True
    return False

# Добавление фигуры на игровое поле
def add_shape_to_grid(shape):
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[shape.y + y][shape.x + x] = shape.color

# Удаление заполненных строк
def clear_rows():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    rows_cleared = len(grid) - len(new_grid)
    grid = [[0] * len(grid[0]) for _ in range(rows_cleared)] + new_grid
    return rows_cleared

# Моментальное падение фигуры
def drop_shape(shape):
    while not check_collision(shape, 0, 1):
        shape.move(0, 1)

# Экран выбора уровня
def level_selection_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    title_text = font.render('Select Level', True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 100))

    level = 1
    font = pygame.font.SysFont(None, 36)
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2))

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    level = min(10, level + 1)
                elif event.key == pygame.K_DOWN:
                    level = max(1, level - 1)
                elif event.key == pygame.K_RETURN:
                    return level

        screen.fill(BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 100))
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_text.get_height() // 2))
        pygame.display.flip()

    pygame.quit()
    return 1

# Функция для сброса состояния игры
def reset_game():
    global grid
    grid = [[0] * (SCREEN_WIDTH // CELL_SIZE) for _ in range(SCREEN_HEIGHT // CELL_SIZE)]

# Основной игровой цикл
def main(start_level=1):
    reset_game()  # Сброс состояния игры
    clock = pygame.time.Clock()
    current_shape = create_shape()
    next_shape = create_shape()
    fall_time = 0
    fall_speed = 500 // 3  # Увеличиваем начальную скорость падения в 3 раза
    score = 0
    level = start_level
    lines_cleared = (start_level - 1) * 10

    running = True
    while running:
        screen.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(current_shape, -1, 0):
                    current_shape.move(-1, 0)
                elif event.key == pygame.K_RIGHT and not check_collision(current_shape, 1, 0):
                    current_shape.move(1, 0)
                elif event.key == pygame.K_DOWN and not check_collision(current_shape, 0, 1):
                    current_shape.move(0, 1)
                elif event.key == pygame.K_UP:
                    current_shape.rotate()
                    if check_collision(current_shape, 0, 0):
                        current_shape.rotate()
                        current_shape.rotate()
                        current_shape.rotate()
                elif event.key == pygame.K_SPACE:
                    drop_shape(current_shape)
                    add_shape_to_grid(current_shape)
                    rows_cleared = clear_rows()
                    score += rows_cleared * 100
                    lines_cleared += rows_cleared
                    level = lines_cleared // 10 + 1
                    fall_speed = max(100, 500 // 3 - (level - 1) * 50)
                    current_shape = next_shape
                    next_shape = create_shape()
                    if check_collision(current_shape, 0, 0):
                        running = False

        # Падение фигуры
        fall_time += clock.get_rawtime()
        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(current_shape, 0, 1):
                current_shape.move(0, 1)
            else:
                add_shape_to_grid(current_shape)
                rows_cleared = clear_rows()
                score += rows_cleared * 100
                lines_cleared += rows_cleared
                level = lines_cleared // 10 + 1
                fall_speed = max(100, 500 // 3 - (level - 1) * 50)
                current_shape = next_shape
                next_shape = create_shape()
                if check_collision(current_shape, 0, 0):
                    running = False

        # Отрисовка игрового поля
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Отрисовка текущей фигуры
        current_shape.draw()

        # Отрисовка очков и уровня
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    # Предложение играть еще раз
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 36)  # Уменьшенный размер шрифта
    game_over_text = font.render('Game Over', True, WHITE)
    play_again_text = font.render('Press R to play again', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 - play_again_text.get_height() // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_level = level_selection_screen()
                    main(start_level)
                    waiting = False

    pygame.quit()

if __name__ == '__main__':
    start_level = level_selection_screen()
    main(start_level)