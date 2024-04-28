import pygame
import sys
import itertools

# Cài đặt kích thước cửa sổ và các thông số liên quan
CELL_SIZE = 26  # Kích thước mỗi ô vuông nhỏ
GRID_SIZE = 20  # Số lượng ô vuông trên mỗi chiều
WIN_SIZE = CELL_SIZE * GRID_SIZE  # Kích thước cửa sổ

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Khởi tạo Pygame và tạo cửa sổ
pygame.init()
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Ultimate Tic Tac Toe - 20x20")
screen.fill(WHITE)

# Vẽ lưới
for x in range(0, WIN_SIZE, CELL_SIZE):
    pygame.draw.line(screen, BLACK, (x, 0), (x, WIN_SIZE))
for y in range(0, WIN_SIZE, CELL_SIZE):
    pygame.draw.line(screen, BLACK, (0, y), (WIN_SIZE, y))

pygame.display.update()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()