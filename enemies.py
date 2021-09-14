import pygame.image
import random
import math

screen_w = 960
screen_h = 768


class SkeletonEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.player = player
        self.spellSpeed = 10
        self.angle = math.atan2(self.y - self.player.y-60, self.x - self.player.x-24)
        self.x_vel = math.cos(self.angle) * self.spellSpeed
        self.y_vel = math.sin(self.angle) * self.spellSpeed
        self.w = 60
        self.h = 60
        self.animationCount = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-500, 500)
        self.offset_y = random.randrange(-500, 500)
        self.left = False
        self.right = False
        self.lastSide = None
        self.image = pygame.image.load('data/sprites/skelet_idle_anim_f0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.char = pygame.image.load('data/sprites/skelet_idle_anim_f0.png').convert_alpha()
        self.walkRight = [pygame.image.load('data/sprites/skelet_run_anim_f0.png').convert_alpha(),
                          pygame.image.load('data/sprites/skelet_run_anim_f1.png').convert_alpha(),
                          pygame.image.load('data/sprites/skelet_run_anim_f2.png').convert_alpha(),
                          pygame.image.load('data/sprites/skelet_run_anim_f3.png').convert_alpha()]
        self.walkLeft = [pygame.transform.flip(self.walkRight[0], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[1], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[2], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[3], True, False).convert_alpha()]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def main(self):

        if self.animationCount >= 15:
            self.animationCount = 0
        self.animationCount += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-500, 500)
            self.offset_y = random.randrange(-500, 500)
            self.reset_offset = random.randrange(120, 150)

        else:
            self.reset_offset -= 1

        if (self.player.x + self.offset_x > self.x) and (self.x + 10 < screen_w - self.w):
            self.x += 1
            self.left = False
            self.right = True
            self.lastSide = 'right'

        elif (self.player.x + self.offset_x < self.x) and (self.x > 10):
            self.x -= 1
            self.left = True
            self.right = False
            self.lastSide = 'left'

        if (self.player.y + self.offset_y > self.y) and (self.y < screen_h - self.h):
            self.y += 1

            if self.lastSide == 'right':
                self.left = False
                self.right = True

            elif self.lastSide == 'left':
                self.left = True
                self.right = False

        elif (self.player.y + self.offset_y < self.y) and (self.y > 8):
            self.y -= 1

            if self.lastSide == 'right':
                self.left = False
                self.right = True

            elif self.lastSide == 'left':
                self.left = True
                self.right = False
            else:
                self.left = False
                self.right = False

        if self.right:
            self.image = pygame.transform.scale(self.walkRight[self.animationCount // 4], (self.w, self.h))
        elif self.left:
            self.image = pygame.transform.scale(self.walkLeft[self.animationCount // 4], (self.w, self.h))
        else:
            self.image = pygame.transform.scale(self.char, (self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class EnemySpell(pygame.sprite.Sprite):
    def __init__(self, enemy, *groups):
        super().__init__(*groups)
        self.spell_x = enemy.x
        self.spell_y = enemy.y
        self.enemy = enemy
        self.spellCount = 90
        self.spellSpeed = 10
        self.angle = math.atan2(self.enemy.y - self.enemy.player.y - 15, self.enemy.x - self.enemy.player.x+5)
        self.x_vel = math.cos(self.angle) * self.spellSpeed
        self.y_vel = math.sin(self.angle) * self.spellSpeed
        self.image = pygame.image.load("data/projectiles/spell.gif").convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = pygame.Rect(self.spell_x, self.spell_y, self.image.get_width(), self.image.get_height())

    def main(self):
        if self.spellCount > random.randrange(40, 100):
            self.spellCount = 0

        if (-20 < self.spell_x < screen_w - 55) and (-60 < self.spell_y < screen_h - 20):
            if self.spell_x == self.enemy.x and self.spell_y == self.enemy.y and self.spellCount != 0:
                self.spell_x = self.enemy.x
                self.spell_y = self.enemy.y
            elif self.spell_x == self.enemy.x and self.spell_y == self.enemy.y and self.spellCount == 0:
                self.spell_x -= int(self.x_vel)
                self.spell_y -= int(self.y_vel)

            elif self.spell_x != self.enemy.x or self.spell_y != self.enemy.y:
                self.spell_x -= int(self.x_vel)
                self.spell_y -= int(self.y_vel)

        elif self.spellCount == 0:
            self.spell_x = self.enemy.x
            self.spell_y = self.enemy.y
            self.angle = math.atan2(self.enemy.y - self.enemy.player.y - 15, self.enemy.x - self.enemy.player.x+5)

        self.rect = pygame.Rect(self.spell_x + 30, self.spell_y + 30, self.image.get_width(), self.image.get_height())
        self.x_vel = math.cos(self.angle) * self.spellSpeed
        self.y_vel = math.sin(self.angle) * self.spellSpeed

        self.spellCount += 1
