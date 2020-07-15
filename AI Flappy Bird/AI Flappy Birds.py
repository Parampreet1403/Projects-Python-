# Parampreet Singh - 07/07/20
# AI Flappy Birds


# Packages
import time
import os
import random
import neat
import pygame
pygame.font.init()


# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

GEN = 0


# Objects
class Bird:
    # Constants
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # Degrees
    ROT_VEL = 20
    ANIMATION_TIME = 5  # Seconds

    def __init__(self, x, y):  # Constructor
        # Private:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # Member Functions
    def jump(self):
        self.vel = -10.5  # Negative means up
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        disp = self.vel * self.tick_count + 1.5*self.tick_count**2
        # -10.5 + 1.5 = -9 (9 pixels up), as time increases disp increases

        if disp >= 16:  # 16 is the greatest amount we can move down
            disp = 16
        elif disp < 0:  # If we are moving up, then move up a little more
            disp -= 2

        self.y = self.y + disp

        if disp < 0 or self.y < self.height + 50:  # If we are moving up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # Tilt bird downwards
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL  # Keep rotating downwards untill at 90 degree

    def draw(self, win):
        self.img_count += 1

        # Handles Wing Flap Loop
        if self.img_count < self.ANIMATION_TIME:  # (up) 5 seconds
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:  # (mid) 10 seconds
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:  # (down) 15 seconds
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:  # (mid) 20 seconds
            self.img = self.IMGS[1]
        # (down) 21 seconds
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0  # Reset Loop

        if self.tilt <= -80:  # If moving down
            self.img = self.IMGS[1]  # Keep bird (mid) constant
            self.img_count = self.ANIMATION_TIME*2  # Join back into wing flap loop

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # If no collide returns None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:  # If off screen
            self.x1 = self.x2 + self.WIDTH  # cycle back

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, gene in genomes:  # Setting up neural network for genome
        net = neat.nn.FeedForwardNetwork.create(gene, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        gene.fitness = 0
        ge.append(gene)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # pygame window
    clock = pygame.time.Clock()
    run = True

    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:  # Quit the game
            run = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            output = nets[i].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

            # bird.move()
        remove = []
        add_pipe = False

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1  # Encourages to not hit pipe
                    # Remove bird, neural network and genome from list
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # If pipe off the screen
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for gene in ge:
                gene.fitness += 5
            pipes.append(Pipe(700))  # Create new pipe

        for item in remove:
            pipes.remove(item)  # Remove passed pipe

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:  # Hit the floor
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    # Load in Neat Config File
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)  # Set Population
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 50)  # Calls main() 50x


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "Neat-config-file.txt")
    run(config_path)
