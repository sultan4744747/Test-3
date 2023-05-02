import pygame
import random
from os import path

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Snake')

clock = pygame.time.Clock()
snake_block = 30
snake_step = 30
FPS = 10

music_dir = path.join(path.dirname(__file__), 'Music')
img_dir = path.join(path.dirname(__file__), 'img')

head_img = [pygame.image.load(path.join(img_dir, 'headR.png')).convert(),
            pygame.image.load(path.join(img_dir, 'headL.png')).convert(),
            pygame.image.load(path.join(img_dir, 'headD.png')).convert(),
            pygame.image.load(path.join(img_dir, 'headU.png')).convert()]

tail_img = [pygame.image.load(path.join(img_dir, 'tailL.png')).convert(),
            pygame.image.load(path.join(img_dir, 'tailR.png')).convert(),
            pygame.image.load(path.join(img_dir, 'tailU.png')).convert(),
            pygame.image.load(path.join(img_dir, 'tailD.png')).convert()]

bg = pygame.image.load(path.join(img_dir, 'трава.png')).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bg_rect = bg.get_rect()

eat = pygame.mixer.Sound(path.join(music_dir, 'apple_bite.ogg'))
eat.set_volume(0.5)

joke = pygame.mixer.Sound(path.join(music_dir, 'joke.ogg'))
joke.set_volume(5)

pygame.mixer.music.load(path.join(music_dir, 'Lose yourself.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)


def eating(xcor, ycor, food_x, food_y):
    if food_x - snake_block <= xcor <= food_x + snake_block:
        if food_y - snake_block <= ycor <= food_y + snake_block:
            return True
    else:
        return False


def create_mes(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [x, y])


def draw_head(i, snake_list):
    snake_img = head_img[i]
    snake_head = pygame.transform.scale(snake_img, (snake_block, snake_block))
    snake_head.set_colorkey(WHITE)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][1])
    screen.blit(snake_head, snake_head_rect)


def draw_tail(i, snake_list):
    snake_img = tail_img[i]
    snake_tail = pygame.transform.scale(snake_img, (snake_block, snake_block))
    snake_tail.set_colorkey(WHITE)
    snake_tail_rect = snake_tail.get_rect(x=snake_list[0][0], y=snake_list[0][1])
    screen.blit(snake_tail, snake_tail_rect)


def game_loop():
    i = 0

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    length = 2

    snake_list = []

    food_x = random.randrange(0, WIDTH - snake_block)
    food_y = random.randrange(0, HEIGHT - snake_block)

    food_img = [pygame.image.load(path.join(img_dir, 'банан.png')).convert(),
                pygame.image.load(path.join(img_dir, 'вишня.png')).convert(),
                pygame.image.load(path.join(img_dir, 'груша.png')).convert(),
                pygame.image.load(path.join(img_dir, 'яблоко.png')).convert()]

    food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))

    food.set_colorkey(WHITE)
    food_rect = food.get_rect(x=food_x, y=food_y)

    run = True
    game_close = False

    while run:
        while game_close:
            screen.fill('red')
            create_mes('''Game over ''', BLACK, 250, 200, 'chalkduster.ttf', 70)
            create_mes('''Press Q for exit or C for repeat ''', BLACK, 50, 400, 'chalkduster.ttf', 70)
            create_mes(f'Final score:{length - 2}', BLACK, 250, 300, 'chalkduster.ttf', 70)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:

                        run = False
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_step
                    y1_change = 0
                    i = 1
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_step
                    y1_change = 0
                    i = 0
                elif event.key == pygame.K_UP:
                    y1_change = - snake_step
                    x1_change = 0
                    i = 3
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_step
                    x1_change = 0
                    i = 2
                    # с помощье конструкци иф кдпр змейки
        if x1 >= WIDTH or x1 <= 0 or y1 >= HEIGHT or y1 <= 0:
            joke.play()
            game_close = True

        x1 += x1_change
        y1 += y1_change

        screen.fill(GREEN)
        screen.blit(bg, bg_rect)
        create_mes(f'Score:{length - 2}', BLACK, 700, 10, 'chalkduster.ttf', 30)
        screen.blit(food, food_rect)
        # pygame.draw.rect(screen,RED,[food_x,food_y,snake_block,snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        # snake_tail = [x1, y1]
        # snake_list.append(snake_tail)

        if len(snake_list) > length:
            del snake_list[0]
        for x in snake_list[1:]:
            snake_img = pygame.image.load(path.join(img_dir, 'змейка5.png')).convert()
            snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
            snake.set_colorkey(WHITE)
            screen.blit(snake, (x[0], x[1]))
            # pygame.draw.rect(screen, BLACK, [x[0], x[1], snake_block, snake_block])
        pygame.display.update()

        for x in snake_list[1:-1]:
            if x == snake_head:
                joke.play()
                game_close = True

        draw_head(i, snake_list)
        draw_tail(i, snake_list)

        if eating(x1, y1, food_x, food_y):
            food_x = random.randrange(0, WIDTH - snake_block)
            food_y = random.randrange(0, HEIGHT - snake_block)
            food_img = [pygame.image.load(path.join(img_dir, 'банан.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'вишня.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'груша.png')).convert(),
                        pygame.image.load(path.join(img_dir, 'яблоко.png')).convert()]

            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food.set_colorkey(WHITE)
            food_rect = food.get_rect(x=food_x, y=food_y)
            length += 1
            eat.play()

        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()


game_loop()
