import pygame
from paddle import Paddle
from ball import Ball

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIZE = (700, 500)

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

carryOn = True

clock = pygame.time.Clock()

scoreA = 0
scoreB = 0

winnerA = False
winnerB = False

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.move_up(5)
    if keys[pygame.K_s]:
        paddleA.move_down(5)
    if keys[pygame.K_UP]:
        paddleB.move_up(5)
    if keys[pygame.K_DOWN]:
        paddleB.move_down(5)

    all_sprites_list.update()

    if ball.rect.x >= 690:
        scoreA += 1
        if scoreA == 5:
            carryOn = False
            winnerA = True

        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        scoreB += 1
        if scoreB == 5:
            carryOn = False
            winnerB = True
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), True, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), True, WHITE)
    screen.blit(text, (420, 10))

    pygame.display.flip()

    clock.tick(60)

if winnerA:
    font = pygame.font.Font(None, 74)
    text = font.render("Player A Wins!", True, WHITE)
    screen.blit(text, (150, 200))
    pygame.display.flip()
elif winnerB:
    font = pygame.font.Font(None, 74)
    text = font.render("Player B Wins!", True, WHITE)
    screen.blit(text, (150, 200))
    pygame.display.flip()

# if any key is pressed, reset the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            pygame.quit()
