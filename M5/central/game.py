import threading

from paddle import Paddle
from ball import Ball
from central import run_central
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SIZE = (700, 500)

FPS = 60


# a daemon thread that runs central in the background
class BackgroundCentral(threading.Thread):
    def __init__(self, pygameInstance):
        threading.Thread.__init__(self)
        self.daemon = True
        self.pygameInstance = pygameInstance

    def run(self):
        run_central(
            self.pygameInstance
        )


def run_game():
    pygame.init()

    # run central in the background
    background_central = BackgroundCentral(pygame)
    background_central.start()

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

    # use imu to control paddleA and paddleB

    while carryOn:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    carryOn = False
                if event.key == pygame.K_UP:
                    paddleA.move_up(5)
                if event.key == pygame.K_DOWN:
                    paddleA.move_down(5)

                if event.key == pygame.K_w:
                    paddleB.move_up(5)
                if event.key == pygame.K_s:
                    paddleB.move_down(5)

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

    pygame.time.wait(10000)

    pygame.quit()


if __name__ == "__main__":
    run_game()
