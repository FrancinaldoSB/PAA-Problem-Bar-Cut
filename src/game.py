import pygame
import sys
import time
import random

# Inicializar o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Quiz - Vitória")

# Cores pastel
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PASTEL_BLUE  = (173, 216, 230)
PASTEL_RED   = (255, 182, 193)
PASTEL_GREEN = (144, 238, 144)
PASTEL_YELLOW= (255, 255, 224)
PASTEL_ORANGE= (255, 204, 153)
PASTEL_PURPLE= (216, 191, 216)
PASTEL_CYAN  = (224, 255, 255)

# Fonte
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 48)

# Configurações
block_size = 30
points = 0

# Bloco do jogador
block_x = WIDTH // 2 - block_size // 1 + block_size  # Deslocar um bloco para a direita
block_y = 0

# Velocidade de queda
fall_speed = 5

# Pergunta
question = "Qual algoritmo que usou memoization?"
correct_answer = "Recursivo"
input_text = ''

# Estado do jogo
game_over = False
victory = False
block_falling = False
exploding = False
particles = []

# Definindo formatos das peças
tetris_shapes = {
    "O": [(0,0), (1,0), (0,1), (1,1)],
    "I": [(0,0), (0,1), (0,2), (0,3)],
    "L": [(0,0), (0,1), (0,2), (1,2)],
    "J": [(1,0), (1,1), (1,2), (0,2)],
    "T": [(0,0), (1,0), (2,0), (1,1)],
    "S": [(1,0), (2,0), (0,1), (1,1)],
    "Z": [(0,0), (1,0), (1,1), (2,1)]
}

shape_colors = {
    "O": PASTEL_YELLOW,
    "I": PASTEL_CYAN,
    "L": PASTEL_ORANGE,
    "J": PASTEL_BLUE,
    "T": PASTEL_PURPLE,
    "S": PASTEL_GREEN,
    "Z": PASTEL_RED
}

# Montar o chão já com peças
stacked_blocks = []

def add_piece(shape, offset_x, offset_y):
    blocks = []
    for dx, dy in tetris_shapes[shape]:
        x = offset_x + dx
        y = offset_y + dy
        color = shape_colors[shape]
        blocks.append((x * block_size, y * block_size, color))
    return blocks

# Adiciona várias peças fixas para criar um chão mais cheio
floor_pieces = [
    ("L", 0, 18),
    ("T", 2, 18),
    ("O", 4, 18),
    ("S", 6, 18),
    ("Z", 8, 18),
    ("J", 10, 18),
    
    ("O", 1, 20),
    ("T", 3, 20),
    ("L", 5, 20),
    ("S", 7, 20),
    ("Z", 9, 20),
    
    ("I", 0, 22),
    ("I", 2, 22),
    ("I", 4, 22),
    ("I", 6, 22),
    ("I", 8, 22),
]

for shape, ox, oy in floor_pieces:
    stacked_blocks.extend(add_piece(shape, ox, oy))

# Deixar um espaço livre em (5, 17)
stacked_blocks = [b for b in stacked_blocks if not (b[0] == 5*block_size and b[1] == 17*block_size)]

# Funções
def draw_block(x, y, color=PASTEL_BLUE):
    pygame.draw.rect(screen, color, (x, y, block_size, block_size))
    pygame.draw.rect(screen, BLACK, (x, y, block_size, block_size), 2)

def draw_question(text, color=WHITE):
    question_surface = font.render(text, True, color)
    rect = question_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(question_surface, rect)

def draw_input(text):
    input_surface = font.render(text, True, PASTEL_GREEN)
    rect = input_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
    screen.blit(input_surface, rect)

def draw_stacked_blocks():
    for x, y, color in stacked_blocks:
        draw_block(x, y, color)

def show_victory():
    screen.fill(BLACK)
    victory_surface = big_font.render("RESPOSTA CORRETA!", True, PASTEL_GREEN)
    rect = victory_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(victory_surface, rect)
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    sys.exit()

def create_explosion(x, y, color):
    for _ in range(30):
        particles.append({
            "x": x + block_size // 2,
            "y": y + block_size // 2,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-4, 4),
            "size": random.randint(2, 5),
            "color": color  # Usar a cor do bloco
        })

def create_explosion_for_stacked_blocks():
    for x, y, color in stacked_blocks:
        create_explosion(x, y, color)

def update_particles():
    for p in particles:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.2

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])

clock = pygame.time.Clock()

# Controlar o tempo de explosão
explosion_start_time = 0
explosion_delay = 2  # Atraso de 2 segundos para começar a explosão dos blocos do chão
explosion_interval = 1  # Intervalo de 1 segundo entre explosões

explosion_index = 0  # Controlar qual bloco irá explodir a cada intervalo

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and not exploding:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip().lower() == correct_answer.lower():
                        print("Resposta correta!")
                        block_falling = True
                        game_over = True
                    else:
                        print("Resposta errada!")
                        block_falling = True
                        game_over = True
                        create_explosion(block_x, block_y, PASTEL_RED)  # Usando uma cor de exemplo (vermelho)
                        exploding = True
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if block_falling:
        block_y += fall_speed
        if block_y >= (17 * block_size):
            block_falling = False
            if not exploding:
                victory = True
            else:
                stacked_blocks.clear()

    # Iniciar explosão dos blocos do chão após 2 segundos
    if game_over and exploding and explosion_start_time == 0:
        explosion_start_time = time.time()

    if explosion_start_time > 0:
        elapsed_time = time.time() - explosion_start_time
        if elapsed_time > explosion_delay:
            create_explosion_for_stacked_blocks()  # Explode com as cores dos blocos
            stacked_blocks.clear()

    draw_stacked_blocks()

    if not victory:
        if not exploding:
            draw_block(block_x, block_y)
            draw_question(question)
            draw_input(input_text)
        else:
            update_particles()
            draw_particles()
            draw_question("RESPOSTA ERRADA!", color=PASTEL_RED)
            if len(particles) == 0 and explosion_index >= len(stacked_blocks):
                exploding = False
                block_y = 0
    else:
        show_victory()

    pygame.display.flip()
    clock.tick(30)