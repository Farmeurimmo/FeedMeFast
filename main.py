import random
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
font2 = pygame.font.SysFont("Arial", 75)

max_fps = 60

mainsurface.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))


def exit_window():
    pygame.quit()
    sys.exit()


def render_text1(text_a, x, y):
    text_rendered = font.render(str(text_a), False, (255, 0, 0))
    screen.blit(text_rendered, (x, y))


def render_text2(text_a, x, y, bo):
    if bo:
        text_rendered = font2.render(str(text_a), False, (255, 127, 0))
        screen.blit(text_rendered, (x, y))
    else:
        text_rendered = font2.render(str(text_a), False, (0, 255, 0))
        screen.blit(text_rendered, (x, y))


def render_player(player):
    pygame.draw.rect(screen, (255, 0, 0), player)


def move_x(modifier, player):
    if WIDTH >= player.x + modifier + player.width >= player.width:
        player.x += modifier


def move_y(modifier, player):
    if HEIGHT >= player.y + modifier + player.height >= player.height:
        player.y += modifier


def spawn_food_random(food):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    food.append((x, y))


def is_food_in_radius(player, food, size_player):
    check_rad = int(size_player)
    for e in food:
        x = e[0]
        y = e[1]
        if player.centerx - check_rad <= x <= player.centerx + check_rad:
            if player.centery - check_rad <= y <= player.centery + check_rad:
                food.remove(e)
                return True


def game_panel():
    selected = 0
    max_options = 2
    while True:
        clock.tick(max_fps)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_window()
                if event.key == pygame.K_s:
                    if selected < max_options:
                        selected += 1
                if event.key == pygame.K_z:
                    if selected > 0:
                        selected -= 1
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        game()
                    if selected == 1:
                        pass
                    if selected == 2:
                        exit_window()

        render_text1(int(clock.get_fps()), 0, 0)
        if selected == 0:
            render_text2(">>>> FeedMeFast", 100, 100, True)
        else:
            render_text2("FeedMeFast", 100, 100, False)
        if selected == 1:
            render_text2(">>>> Crédits", 100, 200, True)
        else:
            render_text2("Crédits", 100, 200, False)
        if selected == 2:
            render_text2(">>>> Quitter", 100, 300, True)
        else:
            render_text2("Quitter", 100, 300, False)

        pygame.display.update()


def game():
    food_eated = 0
    speed = 7
    size_player = 10
    player = pygame.Rect(0, 0, size_player, size_player)
    food = []
    last_spawn = 0
    while True:
        clock.tick(max_fps)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_panel()

        key = pygame.key.get_pressed()
        if key[pygame.K_z]:
            move_y(-speed, player)
        if key[pygame.K_q]:
            move_x(-speed, player)
        if key[pygame.K_s]:
            move_y(speed, player)
        if key[pygame.K_d]:
            move_x(speed, player)

        if is_food_in_radius(player, food, size_player):
            food_eated += 1
            size_player += 1
            player.width += 1
            player.height += 1
            if food.__sizeof__().__int__() <= 1:
                spawn_food_random(food)
                last_spawn = 0

        render_player(player)
        render_text1(int(clock.get_fps()), 0, 0)
        render_text1(food_eated, 25, 0)

        for e in food:
            x = e[0]
            y = e[1]
            pygame.draw.rect(screen, (196, 127, 0), pygame.Rect(x, y, int(size_player / 2), int(size_player / 2)))

        if last_spawn >= max_fps * 2.5:
            spawn_food_random(food)
            last_spawn = 0
        last_spawn += 1

        pygame.display.update()


game_panel()
