import pygame
import sys

# Inicialización de Pygame y el sistema de sonido
pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Pelea")

# Colores y fuentes
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
fuente = pygame.font.SysFont(None, 36)

# Cargar imágenes y sonidos
fondo = pygame.image.load("fondo.png")  # Fondo del juego
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

jugador1 = {
    "x": 100, "y": 300, "vida": 100,
    "ancho": 80, "alto": 100,
    "imagen": pygame.image.load("images1.png"),
}
jugador2 = {
    "x": 650, "y": 300, "vida": 100,
    "ancho": 80, "alto": 100,
    "imagen": pygame.image.load("imagenes2.png"),
}

# Escalar las imágenes
jugador1["imagen"] = pygame.transform.scale(jugador1["imagen"], (jugador1["ancho"], jugador1["alto"]))
jugador2["imagen"] = pygame.transform.scale(jugador2["imagen"], (jugador2["ancho"], jugador2["alto"]))

# Velocidad y control de ataque
velocidad = 5
dano_ataque = 10
ataque_realizado = {"jugador1": False, "jugador2": False}

# Cargar sonidos
sonido_ataque = pygame.mixer.Sound("sonido_ataque.mp3")
musica_fondo = "musica_fondo.mp3"
pygame.mixer.music.load(musica_fondo)

# Variables de juego
jugando = False
tiempo_maximo = 30  # 30 segundos de límite
reloj = pygame.time.Clock()
tiempo_restante = tiempo_maximo

# Función para mostrar la barra de vida
def mostrar_vida():
    barra_j1 = pygame.Rect(10, 10, jugador1["vida"] * 2, 20)
    barra_j2 = pygame.Rect(ANCHO - jugador2["vida"] * 2 - 10, 10, jugador2["vida"] * 2, 20)
    pygame.draw.rect(pantalla, ROJO, (10, 10, 200, 20))  # Barra de fondo
    pygame.draw.rect(pantalla, ROJO, (ANCHO - 210, 10, 200, 20))  # Barra de fondo
    pygame.draw.rect(pantalla, VERDE, barra_j1)  # Barra de vida
    pygame.draw.rect(pantalla, VERDE, barra_j2)

# Función para manejar el combate
def atacar(atacante, receptor):
    if abs(atacante["x"] - receptor["x"]) < 60:
        receptor["vida"] -= dano_ataque
        if receptor["vida"] < 0:
            receptor["vida"] = 0
        sonido_ataque.play()

# Pantalla de inicio
def pantalla_inicio():
    pantalla.fill(BLANCO)
    mensaje = fuente.render("Presiona Enter para Iniciar", True, NEGRO)
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
    pygame.display.flip()

# Pantalla de finalización
def pantalla_fin(ganador):
    pantalla.fill(BLANCO)
    mensaje = fuente.render(f"{ganador} Gana!", True, NEGRO)
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Bucle principal del juego
while True:
    if not jugando:
        pantalla_inicio()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jugando = True
                pygame.mixer.music.play(-1)
                tiempo_restante = tiempo_maximo
                jugador1["vida"] = jugador2["vida"] = 100  # Resetear vida al inicio
    else:
        # Fondo y reloj
        pantalla.blit(fondo, (0, 0))
        tiempo_restante -= 1 / 30  # Reducir tiempo
        if tiempo_restante <= 0:
            ganador = "Jugador 1" if jugador1["vida"] > jugador2["vida"] else "Jugador 2"
            pantalla_fin(ganador)
            jugando = False
            pygame.mixer.music.stop()
            continue

        # Eventos de salida
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Movimiento y ataques
        teclas = pygame.key.get_pressed()
        
        # Movimiento Jugador 1
        if teclas[pygame.K_a] and jugador1["x"] > 0:
            jugador1["x"] -= velocidad
        if teclas[pygame.K_d] and jugador1["x"] < ANCHO - jugador1["ancho"] :
            jugador1["x"] += velocidad
        if teclas[pygame.K_w] and jugador1["y"] > 0:
            jugador1["y"] -= velocidad
        if teclas[pygame.K_s] and jugador1["y"] < ALTO - jugador1["alto"]:
            jugador1["y"] += velocidad

        # Ataque Jugador 1
        if teclas[pygame.K_q]:
            if not ataque_realizado["jugador1"]:
                atacar(jugador1, jugador2)
                ataque_realizado["jugador1"] = True
        else:
            ataque_realizado["jugador1"] = False

        # Movimiento Jugador 2
        if teclas[pygame.K_LEFT] and jugador2["x"] > 0:
            jugador2["x"] -= velocidad
        if teclas[pygame.K_RIGHT] and jugador2["x"] < ANCHO - jugador2["ancho"]:
            jugador2["x"] += velocidad
        if teclas[pygame.K_UP] and jugador2["y"] > 0:
            jugador2["y"] -= velocidad
        if teclas[pygame.K_DOWN] and jugador2["y"] < ALTO - jugador2["alto"]:
            jugador2["y"] += velocidad

        # Ataque Jugador 2 (Ahora usa la tecla 'F')
        if teclas[pygame.K_f]:
            if not ataque_realizado["jugador2"]:
                atacar(jugador2, jugador1)
                ataque_realizado["jugador2"] = True
        else:
            ataque_realizado["jugador2"] = False

        # Dibujar jugadores y vida
        pantalla.blit(jugador1["imagen"], (jugador1["x"], jugador1["y"]))
        pantalla.blit(jugador2["imagen"], (jugador2["x"], jugador2["y"]))
        mostrar_vida()

        # Comprobar si alguien ha ganado
        if jugador1["vida"] <= 0 or jugador2["vida"] <= 0:
            ganador = "Jugador 1" if jugador2["vida"] <= 0 else "Jugador 2"
            pantalla_fin(ganador)
            jugando = False
            pygame.mixer.music.stop()

        # Mostrar temporizador
        tiempo_texto = fuente.render(f"Tiempo: {int(tiempo_restante)}", True, NEGRO)
        pantalla.blit(tiempo_texto, (ANCHO // 2 - tiempo_texto.get_width() // 2, 10))

        # Actualizar pantalla y reloj
        pygame.display.flip()
        reloj.tick(30)

pygame.quit()
