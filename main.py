# CONWAY'S GAME OF LIFE

# LIBRERÍAS NECESARIAS
import numpy as np
import pygame
import time

# INICIALIZAR PYGAME
pygame.init()

# PONER TÍTULO
pygame.display.set_caption('Conway\'s Game of Life')

# DIMENSIONES DE LA PANTALLA, SE PUEDEN MODIFICAR
width, height = 1280, 720

# CREAR PANTALLA Y PONER FUENTE POR DEFECTO
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont("Consolas", 15)
title_font = pygame.font.SysFont("Consolas", 40)

# COLOR DE FONDO
bg = 25, 25, 25

# LLENAR LA PANTALLA CON EL COLOR DE FONDO
screen.fill(bg)

# NÚMERO DE CELDAS
ncX, ncY = int(width / 20), int(height / 20)

# TAMAÑO DE CELDAS
dimCW = width / ncX
dimCH = height / ncY

# COLORES QUE SE USAN
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 255, 65

# ARRAY DE CEROS
gameState = np.zeros((ncX, ncY))

# VARIABLES NECESITADAS
gen_counter = 0
cell_counter = 0
aux_cell = 0

# TEXTOS
title_text = title_font.render("Conway's Game of Life", True, GREEN, BLACK)
rule_1 = font.render("1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.", True, GREEN, BLACK)
rule_2 = font.render("2. Any live cell with two or three live neighbours lives on to the next generation.", True, GREEN, BLACK)
rule_3 = font.render("3. Any live cell with more than three live neighbours dies, as if by overpopulation.", True, GREEN, BLACK)
rule_4 = font.render("4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.", True, GREEN, BLACK)

start_switch = True

# ESTADO DE PAUSA
pauseState = True

while True:
    screen.fill(BLACK)

    time.sleep(0.1)
    
    start_switch = not start_switch

    # TEXTOS DE TÍTULO Y REGLAS
    screen.blit(title_text, (400, 70))
    screen.blit(font.render("Rules:", True, GREEN, BLACK), (250, 170))
    screen.blit(rule_1, (250, 200))
    screen.blit(rule_2, (250, 220))
    screen.blit(rule_3, (250, 240))
    screen.blit(rule_4, (250, 260))

    # MOSTRAR INSTRUCCIONES
    screen.blit(font.render("Controls:", True, GREEN, BLACK), (250, 350))
    screen.blit(font.render("Paint cell    --->  Left click", True, GREEN, BLACK), (250, 380))
    screen.blit(font.render("Unpaint cell  --->  Right click", True, GREEN, BLACK), (250, 400))
    screen.blit(font.render("Pause/Resume  --->  Escape", True, GREEN, BLACK), (250, 420))

    screen.blit(font.render("Press \"Space\" to start", True, GREEN, BLACK), ((width / 2) - 100, 510))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    # ROMPER EL BUCLE Y PASAR AL JUEGO
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        break

    pygame.display.flip()


while True:
    # MATRIZ AUXILIAR
    newGameState = np.copy(gameState)

    # GENERAR TEXTOS
    gen_text = font.render(f"Gen: {gen_counter}", True, GREEN, BLACK)
    cell_text = font.render(f"Cells alive: {aux_cell}", True, GREEN, BLACK)
    pause_text = font.render(f"PAUSED", True, GREEN, BLACK)

    screen.fill(bg)
    time.sleep(0.1)

    cell_counter = 0

    # CAPTURA LOS EVENTOS DEL MOUSE
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pauseState = not pauseState

        # PARA SALIR DE LA APLICACIÓN
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        mouseC = pygame.mouse.get_pressed()

        if sum(mouseC) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseC[2]

    for i in range(ncX):
        for j in range(ncY):
            if not pauseState:
                # BUSCA LOS VECINOS VIVOS
                neigh_num = gameState[(i - 1) % ncX, (j - 1) % ncY] + \
                            gameState[(i) % ncX, (j - 1) % ncY] + \
                            gameState[(i + 1) % ncX, (j - 1) % ncY] + \
                            gameState[(i - 1) % ncX, (j) % ncY] + \
                            gameState[(i + 1) % ncX, (j) % ncY] + \
                            gameState[(i - 1) % ncX, (j + 1) % ncY] + \
                            gameState[(i) % ncX, (j + 1) % ncY] + \
                            gameState[(i + 1) % ncX, (j + 1) % ncY]

                # APLICA LAS REGLAS
                if gameState[i, j] == 0 and neigh_num == 3:
                    newGameState[i, j] = 1
                
                elif gameState[i, j] == 1 and (neigh_num < 2 or neigh_num > 3):
                    newGameState[i, j] = 0
                
                if gameState[i, j] == 1:
                    cell_counter += 1
                    aux_cell = cell_counter
            
            # MATRIZ DE LA CELDA
            matrix = [((i) * dimCW, (j) * dimCH),
                      ((i + 1) * dimCW, (j) * dimCW),
                      ((i + 1) * dimCW, (j + 1) * dimCH),
                      ((i) * dimCW, (j + 1) * dimCH)]

            # PINTA LA CELDA DEL COLOR CONTRARIO
            if newGameState[i, j] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), matrix, 1)
            
            else:
                pygame.draw.polygon(screen, WHITE, matrix, 0)

    # IMPRIME LOS TEXTOS
    screen.blit(gen_text, (10, 12))
    screen.blit(cell_text, (width - 130, 12))

    if pauseState:
        screen.blit(pause_text, ((width / 2) - 24, 12))

    if not pauseState:
        gen_counter += 1

    # COPIA LA MATRIZ MODIFICADA
    gameState = np.copy(newGameState)

    # ACTUALIZA LA PANTALLA
    pygame.display.flip()
