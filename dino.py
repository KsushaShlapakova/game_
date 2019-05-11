from livewires import games, color
import random
import pygame
import numpy as np

games.init(screen_width=564, screen_height=423, fps=30)


class Dino(games.Animation):
    sound = games.load_sound('music/fire.wav')
    sound_end = games.load_sound('music/Frol2.wav')
    increment = 1
    images = []

    def __init__(self, x=300, y=265):

        for i in range(1, 3):
            Dino.images.append('img/Run' + str(i) + '.gif')
        super(Dino, self).__init__(images=Dino.images,
                                   x=x,
                                   y=y,
                                   repeat_interval=10,
                                   n_repeats=float('inf'))

        self.sc_text = games.Text(value='Score:',
                                  size=50,
                                  top=10,
                                  color=color.black,
                                  right=120,
                                  is_collideable=False)

        self.score = games.Text(value=0,
                                size=35,
                                top=17,
                                color=color.black,
                                right=160,
                                is_collideable=False)

        games.screen.add(self.sc_text)
        games.screen.add(self.score)

        self.x = x
        self.y = y
        self.fire = None
        self.dy = 0
        self.points = None
        self.d = {'score': None}

    def update(self):
        if games.keyboard.is_pressed(games.K_SPACE):
            Dino.sound.play()
            self.dy = -5
            self.fire_show()

        elif self.y == 265:
            games.screen.remove(self.fire)
            self.dy = 0

        else:
            games.screen.remove(self.fire)
            self.dy = 2.5

        if self.y <= 0:
            self.y = 0

        self.fire.y = self.y + 25

        if self.overlapping_sprites:
            Dino.sound.stop()
            games.music.stop()
            Dino.sound_end.play()
            games.screen.remove(self.fire)
            self.destroy()
            Dino.end_game()

        else:
            self.score.value += 1

    @staticmethod
    def end_game():
        end_msg = games.Message(value='YOU DIED',
                                size=150,
                                color=color.black,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime=13 * games.screen.fps,
                                after_death=games.screen.quit,
                                is_collideable=False)
        games.screen.add(end_msg)

    def add_fire(self, fire):
        self.fire = fire

    def fire_show(self):
        games.screen.add(self.fire)


class Fire(games.Animation):
    images = []

    def __init__(self, x=282, y=195, dy=0):
        for i in range(1, 4):
            Fire.images.append('img/Fire' + str(i) + '.gif')
        super(Fire, self).__init__(images=Fire.images,
                                   x=x,
                                   y=y,
                                   dy=dy,
                                   repeat_interval=10, n_repeats=float('inf'),
                                   is_collideable=False)
        self.x = x
        self.y = y
        self.dy = dy

    def update(self):
        if not self.overlapping_sprites:
            self.destroy()


class Ground(games.Sprite):
    image = games.load_image('img/Earth_.gif')

    def __init__(self, x=300, y=600):
        super(Ground, self).__init__(image=Ground.image,
                                     x=x,
                                     y=y,
                                     is_collideable=False)
        self.x = x
        self.y = y
        self.time = 1
        self.time_til_drop = 0
        self.update()
        self.angle = 1

    def update(self):
        self.angle -= 0.5 * Dino.increment
        if self.angle > 358:
            Dino.increment += 0.25
        self.f()

    def f(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1

        else:
            size = random.choice([1, 2, 3])
            new_obst = Obstacles(size)
            games.screen.add(new_obst)
            speed = random.choice(np.arange(0.4, 3, 0.2))
            y = random.randint(35, 140)
            new_obstacles = Asteroid(1000, y, speed)
            games.screen.add(new_obstacles)

            self.time_til_drop = random.randint(200, 350)


class Asteroid(games.Animation):

    images = []

    def __init__(self, x=600, y=50, speed=0.3):
        for i in range(0, 25):
            Asteroid.images.append('asteroid/' + str(i) + '.gif')
        super(Asteroid, self).__init__(images=Asteroid.images,
                                        x=x,
                                        y=y,
                                        dx=-speed,
                                        repeat_interval=10)

    def update(self):
        if self.x == -100:
            self.destroy()
            speed = random.choice(np.arange(0.3, 3, 0.1))
            y = random.randint(20, 50)
            new_obstacles = Asteroid(1000, y, speed)
            games.screen.add(new_obstacles)


class Obstacles(games.Sprite):
    ONE = 1
    TWO = 2
    THREE = 3
    images = {ONE: games.load_image('img/1.gif'),
              TWO: games.load_image('img/2.gif'),
              THREE: games.load_image('img/3.gif')}

    def __init__(self, size=1, x=300, y=600):
        super(Obstacles, self).__init__(image=Obstacles.images[size],
                                        x=x, y=y)
        self.x = x
        self.angle = 90
        self.update()

    def update(self):
        v = pygame.math.Vector2(325., 0.)
        self.angle -= 0.5 * Dino.increment
        v = v.rotate(self.angle)
        self.x = v.x + 300.
        self.y = v.y + 600.

        if self.x < 300 and self.y > 500:
            self.destroy()


def main():
    wall_image = games.load_image('img/bg.jpg', transparent=False)
    games.screen.background = wall_image

    games.music.load('music/star.mp3')
    games.music.play(-1)

    the_gr = Ground()
    the_dino = Dino()
    fire = Fire()
    the_dino.add_fire(fire)
    the_asteroid = Asteroid()
    games.screen.add(the_gr)
    games.screen.add(the_dino)
    games.screen.add(the_asteroid)

    games.mouse.is_visible = False

    games.screen.mainloop()


if __name__ == '__main__':
    main()
