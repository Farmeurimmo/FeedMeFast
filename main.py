import sys
import pygame

pygame.init()
info = pygame.display.Info()
SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
mainsurface = pygame.display.set_mode(SIZE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("FeedMeFast")
print("Starting game with resolution: {}x{}".format(WIDTH, HEIGHT))
screen.fill((0, 255, 0))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

max_fps = 60

mainsurface.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))

player = pygame.Rect(0, 0, 60, 60)


def exit_window():
    pygame.quit()
    sys.exit()


def render_fps(fps):
    fps_text = font.render(str(fps), False, (255, 0, 0))
    screen.blit(fps_text, (0, 0))


def render_player():
    pygame.draw.rect(screen, (255, 0, 0), player)


def move_x(modifier):
    if WIDTH >= player.x + modifier + player.width >= player.width:
        player.x += modifier


def move_y(modifier):
    if HEIGHT >= player.y + modifier + player.height >= player.height:
        player.y += modifier


while True:
    clock.tick(max_fps)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit_window()

    key = pygame.key.get_pressed()
    if key[pygame.K_z]:
        move_y(-5)
    if key[pygame.K_q]:
        move_x(-5)
    if key[pygame.K_s]:
        move_y(5)
    if key[pygame.K_d]:
        move_x(5)

    render_player()
    render_fps(int(clock.get_fps()))
    pygame.display.update()
