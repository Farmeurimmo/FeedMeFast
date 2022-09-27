import random
import sys
import pygame
import time

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
base_y = 20
food_bar = 200

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
    if HEIGHT >= player.y + modifier + player.height >= player.height + base_y:
        player.y += modifier


def spawn_food_random(food):
    x = random.randint(0, WIDTH)
    y = random.randint(base_y, HEIGHT)
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
    max_options = 3
    while True:
        clock.tick(max_fps)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_window()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if selected < max_options:
                        selected += 1
                if event.key == pygame.K_z or event.key == pygame.K_UP:
                    if selected > 0:
                        selected -= 1
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        game()
                    if selected == 1:
                        pass
                    if selected == 2:
                        pass
                    if selected == 3:
                        exit_window()

        render_text1(int(clock.get_fps()), 0, 0)
        if selected == 0:
            render_text2(">>>> FeedMeFast", 100, 100, True)
        else:
            render_text2("FeedMeFast", 100, 100, False)
        if selected == 1:
            render_text2(">>>> Settings", 100, 200, True)
        else:
            render_text2("Settings", 100, 200, False)
        if selected == 2:
            render_text2(">>>> Credits", 100, 300, True)
        else:
            render_text2("Credits", 100, 300, False)
        if selected == 3:
            render_text2(">>>> Quitter", 100, 400, True)
        else:
            render_text2("Quitter", 100, 400, False)

        pygame.display.update()


def game():
    food_eated = 0
    speed = 7
    size_player = 30
    player = pygame.Rect(0, base_y, size_player, size_player)
    food = []
    last_spawn = 0
    food_level = food_bar
    last_r = time.time()
    while True:
        clock.tick(max_fps)
        speed = food_level/20
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_panel()

        key = pygame.key.get_pressed()
        if key[pygame.K_z] or key[pygame.K_UP]:
            move_y(-speed, player)
            food_level -= 0.10
        if key[pygame.K_q] or key[pygame.K_LEFT]:
            move_x(-speed, player)
            food_level -= 0.10
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            move_y(speed, player)
            food_level -= 0.10
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            move_x(speed, player)
            food_level -= 0.10

        if is_food_in_radius(player, food, size_player):
            food_eated += 1
            food_level += food_bar/10

        if len(food) < 1:
            spawn_food_random(food)
            last_spawn = 0

        if time.time() > last_r + 0.75:
            food_level -= 5
            last_r = time.time()
            if food_level < 0:
                game_panel()

        pygame.draw.rect(screen, (0, 20, 40), pygame.Rect(0, 0, WIDTH, base_y))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(WIDTH-food_bar, 0, food_bar, base_y))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(WIDTH-food_bar, 0, food_level, base_y))
        render_player(player)
        render_text1(int(clock.get_fps()), 0, 0)
        render_text1(food_eated, 25, 0)

        for e in food:
            x = e[0]
            y = e[1]
            pygame.draw.rect(screen, (196, 127, 0), pygame.Rect(x, y, int(size_player / 2), int(size_player / 2)))

        if last_spawn >= max_fps * 4:
            spawn_food_random(food)
            last_spawn = 0
        last_spawn += 1

        pygame.display.update()


game_panel()
