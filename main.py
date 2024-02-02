from pygame import *
from random import randint

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter 2D')

clock = time.Clock()

mixer.init()
mixer.music.load('music.mp3.mp3')
mixer.music.play()
mixer.music.set_volume(0.015)

fire_sound = mixer.Sound('klassicheskiy-zvuk-fleytyi-42266.mp3')
fire_sound.set_volume(0.055)

zombi_sound = mixer.Sound('inecraft_zombie_.mp3')
zombi_sound.set_volume(0.025)

font.init()
stats_font = font.SysFont('Arial', 32)
main_font = font.SysFont('Arial', 72)
hp_font = font.SysFont('Arial', 18)

win_text = main_font.render("You win!", True, (50,200,0))
lose_text = main_font.render("You lose!", True, (200,50,0))

fps = 60
game_run = True
game_finish = False

enemy_respawn_delay = fps * 2
enemy_respawn_timer = enemy_respawn_delay

asteroid_respawn_delay = fps * 3
asteroid_respawn_timer = asteroid_respawn_delay

health_respawn_delay = fps * 5
health_respawn_timer = health_respawn_delay

zombi_respawn_delay = fps * 10
zombi_respawn_timer = zombi_respawn_delay

heart_respawn_delay = fps * 5
heart_respawn_timer = heart_respawn_delay

lost, kills = 0, 0


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()

        self.image = transform.scale(
            image.load(img),
            (w, h)
        )

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    fire_delay = fps * 0.25
    fire_timer = fire_delay
    can_fire = True
    health = 3

    def update(self):
        hp_txt = hp_font.render(f'HP : {self.health}', True, (0, 200, 25))

        if not self.can_fire:
            if self.fire_timer > 0:
                self.fire_timer -= 1
            else:
                self.fire_timer = self.fire_delay
                self.can_fire = True

        keys = key.get_pressed()
        if keys[K_d] or keys[K_RIGHT]:
            if self.rect.x < win_width - self.image.get_width():
                self.rect.x += self.speed
        if keys[K_a] or keys[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[K_SPACE]:
            if self.can_fire:
                self.fire()
                self.can_fire = False

        window.blit(hp_txt, (self.rect.x + self.image.get_width() / 2 - hp_txt.get_width() / 2, self.rect.y - 25))

    def fire(self):
        new_bullet = Bullet('fire.png', self.rect.centerx, self.rect.y, 38, 42, 5)
        bullet_group.add(new_bullet)
        fire_sound.play()


class Enemy(GameSprite):
    health = randint(1, 2)

    def update(self):
        global lost

        hp_txt = hp_font.render(f'HP : {self.health + 1}', True, (200, 200, 200))

        if self.rect.y >= win_width:
            lost += 1
            self.kill()
        elif sprite.collide_rect(self, player):
            player.health -= 1
            self.kill()
        else:
            self.rect.y += self.speed

        window.blit(hp_txt, (self.rect.x + self.image.get_width() / 2 - hp_txt.get_width() / 2, self.rect.y - 25))


class Asteroid(GameSprite):
    def update(self):
        if self.rect.y >= win_width:
            self.kill()
        elif sprite.collide_rect(self, player):
            player.health -= 1
            self.kill()
        else:
            self.rect.y += self.speed


class Health(GameSprite):
    def update(self):
        if player.health < 3:
            if self.rect.y >= win_width:
                self.kill()
            elif sprite.collide_rect(self, player):
                player.health += 1
                self.kill()
            else:
                self.rect.y += self.speed
        else:
            self.kill()


class Heart(GameSprite):
    def update(self):
        if player.health == 1:
            if self.rect.y >= win_width:
                self.kill()
            elif sprite.collide_rect(self, player):
                player.health += 2
                self.kill()
            else:
                self.rect.y += self.speed
        else:
            self.kill()


class Zombi(GameSprite):
    def update(self):
        if self.rect.y >= win_width:
            self.kill()
        elif sprite.collide_rect(self, player):
            player.health -= 3
            self.kill()
        else:
            self.rect.y += self.speed
            zombi_sound.play()


bg = GameSprite('img.png', 0, 0, win_width, win_height, 0)
player = Player('vey.png', win_width / 2, win_height - 170, 112, 125, 7)

enemys_group = sprite.Group()
bullet_group = sprite.Group()
asteroid_group = sprite.Group()
health_group = sprite.Group()
zombi_group = sprite.Group()
heart_group = sprite.Group()


class Bullet(GameSprite):
    def update(self):
        global kills

        if self.rect.y <= 0:
            self.kill()

        enemy = sprite.spritecollide(self, enemys_group, False)

        if enemy:
            enemy = enemy[0]
            if enemy.health <= 0:
                kills += 1
                enemy.kill()
            else:
                enemy.health -= 1
            self.kill()

        self.rect.y -= self.speed


win_sound = mixer.Sound("9f3d770d1446e6c.mp3")
lose_sound = mixer.Sound("b1314089d5efb25.mp3")

while game_run:
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False

    if not game_finish:
        kills_text = stats_font.render(f'Усунено: {kills}', True, (220, 220, 220))
        lost_text = stats_font.render(f'У вас проблеми: {lost}', True, (220, 220, 220))

        if enemy_respawn_timer > 0:
            enemy_respawn_timer -= 1
        else:
            new_enemy = Enemy("ghost.png", randint(0, win_width - 72), -72, 72, 64, randint(2, 4))
            new_enemy.health = randint(0,2)
            enemys_group.add(new_enemy)
            enemy_respawn_timer = enemy_respawn_delay

        if asteroid_respawn_timer > 0:
            asteroid_respawn_timer -= 1
        else:
            new_asteroid = Asteroid("Fiirree1.png", randint(
                0, win_width - 72), -72, 72, 64, randint(4, 6))
            asteroid_group.add(new_asteroid)
            asteroid_respawn_timer = asteroid_respawn_delay

        if health_respawn_timer > 0:
            health_respawn_timer -= 1
        else:
            new_health = Health("health.png", randint(0, win_width - 72), -72, 72, 64, randint(2, 4))
            health_group.add(new_health)
            health_respawn_timer = health_respawn_delay

        if zombi_respawn_timer > 0:
            zombi_respawn_timer -= 1
        else:
            new_zombi = Zombi("zombi.png", randint(0, win_width - 72), -72, 72, 64, randint(2, 4))
            zombi_group.add(new_zombi)
            zombi_respawn_timer = zombi_respawn_delay

        if heart_respawn_timer > 0:
            heart_respawn_timer -= 1
        else:
            new_heart = Heart("heart.png", randint(0, win_width - 72), -72, 72, 64, randint(2, 4))
            heart_group.add(new_heart)
            heart_respawn_timer = heart_respawn_delay



        bg.reset()
        player.reset()
        enemys_group.draw(window)
        bullet_group.draw(window)
        asteroid_group.draw(window)
        health_group.draw(window)
        zombi_group.draw(window)
        heart_group.draw(window)

        player.update()
        enemys_group.update()
        bullet_group.update()
        asteroid_group.update()
        health_group.update()
        zombi_group.update()
        heart_group.update()

        window.blit(kills_text, (5, 5))
        window.blit(lost_text, (5, 38))

        if kills >= 10:
            window.blit(win_text, (win_width / 2 - win_text.get_width() / 2, win_height / 2 - win_text.get_height()))
            win_sound.play()
            lose_sound.set_volume(0.055)
            game_finish = True

        if lost >= 5 or player.health <= 0:
            window.blit(lose_text, (win_width / 2 - lose_text.get_width() / 2, win_height / 2 - lose_text.get_height()))
            lose_sound.play()
            lose_sound.set_volume(0.055)
            game_finish = True

        display.update()

    clock.tick(fps)