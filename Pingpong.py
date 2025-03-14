from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self, up_key, down_key):
        keys = key.get_pressed()
        if keys[up_key] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

back = (200, 255, 255)
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
window.fill(back)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 35)

# Mode selection screen
def choose_mode():
    selecting = True
    while selecting:
        window.fill((50, 50, 50))
        text1 = font.render("Press 1 for 1v1", True, (255, 255, 255))
        text2 = font.render("Press 2 for 2v2", True, (255, 255, 255))
        window.blit(text1, (300, 250))
        window.blit(text2, (300, 300))
        
        display.update()
        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_1:
                    return 1
                if e.key == K_2:
                    return 2

mode = choose_mode()

racket1 = Player("racket.png", 30, 250, 4, 50, 150)
racket2 = Player("racket.png", 720, 250, 4, 50, 150)
ball = GameSprite("tenis_ball.png", 375, 275, 4, 50, 50)

if mode == 2:
    racket3 = Player("racket.png", 30, 350, 4, 50, 150)
    racket4 = Player("racket.png", 720, 350, 4, 50, 150)

lose1 = font.render("PLAYER 1 WINS!", True, (180, 0, 0))
lose2 = font.render("PLAYER 2 WINS!", True, (180, 0, 0))

speed_x = 3
speed_y = 3

score1 = 0
score2 = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        
        racket1.update(K_w, K_s)
        racket2.update(K_UP, K_DOWN)
        if mode == 2:
            racket3.update(K_a, K_d)
            racket4.update(K_LEFT, K_RIGHT)
        
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball) or (mode == 2 and (sprite.collide_rect(racket3, ball) or sprite.collide_rect(racket4, ball))):
            speed_x *= -1

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            score2 += 1
            ball.rect.x, ball.rect.y = win_width // 2, win_height // 2
            speed_x *= -1

        if ball.rect.x > win_width:
            score1 += 1
            ball.rect.x, ball.rect.y = win_width // 2, win_height // 2
            speed_x *= -1

        if score1 >= 5:
            finish = True
            window.blit(lose1, (300, 250))
        elif score2 >= 5:
            finish = True
            window.blit(lose2, (300, 250))

        racket1.reset()
        racket2.reset()
        if mode == 2:
            racket3.reset()
            racket4.reset()
        ball.reset()
        
        score_display = font.render(f"Score: {score1} - {score2}", True, (0, 0, 0))
        window.blit(score_display, (350, 20))

    display.update()
    clock.tick(FPS)
