import pygame, math

screen_w = 960
screen_h = 768


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.x = 300
        self.y = 50
        self.w = 48
        self.h = 84
        self.life = 100
        self.score = 0
        self.vel = 3.5
        self.left = False
        self.right = False
        self.animationCount = 0
        self.walkCount = 0
        self.dashCooldown = 500
        self.lastSide = None
        self.weaponImage = pygame.image.load('data/projectiles/weapon_anime_sword.png').convert_alpha()
        self.weaponImage = pygame.transform.rotate(self.weaponImage, -90)
        self.image = pygame.image.load('data/sprites/knight_m_run_anim_f0.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.walkRight = [pygame.image.load('data/sprites/knight_m_run_anim_f0.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_run_anim_f1.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_run_anim_f2.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_run_anim_f3.png').convert_alpha()]
        self.walkLeft = [pygame.transform.flip(self.walkRight[0], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[1], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[2], True, False).convert_alpha(),
                         pygame.transform.flip(self.walkRight[3], True, False).convert_alpha()]
        self.charRight = [pygame.image.load('data/sprites/knight_m_idle_anim_f0.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_idle_anim_f1.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_idle_anim_f2.png').convert_alpha(),
                          pygame.image.load('data/sprites/knight_m_idle_anim_f3.png').convert_alpha()]
        self.charLeft = [pygame.transform.flip(self.charRight[0], True, False).convert_alpha(),
                         pygame.transform.flip(self.charRight[1], True, False).convert_alpha(),
                         pygame.transform.flip(self.charRight[2], True, False).convert_alpha(),
                         pygame.transform.flip(self.charRight[3], True, False).convert_alpha()]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def moveset(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.x > 15:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.lastSide = "left"

        elif keys[pygame.K_d] and self.x < (screen_w - self.w - 15):
            self.x += self.vel
            self.left = False
            self.right = True
            self.lastSide = "right"

        if keys[pygame.K_w] and self.y > - 15:
            self.y -= self.vel

            if self.lastSide == "left":
                self.left = True
                self.right = False

            else:
                self.left = False
                self.right = True

        elif keys[pygame.K_s] and self.y < screen_h - (self.h * 1.2):

            if self.lastSide == "left":
                self.left = True
                self.right = False

            else:
                self.left = False
                self.right = True
            self.y += self.vel

        elif not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.right = False
            self.left = False
            self.walkCount = 0

    def main(self, nEnemies):
        if self.animationCount >= 20*nEnemies:
            self.animationCount = 0

        if self.walkCount >= 20*nEnemies:
            self.walkCount = 0

        if self.left:
            self.image = pygame.transform.scale(self.walkLeft[self.walkCount // 5 // nEnemies], (self.w, self.h))
            self.walkCount += 1

        elif self.right:
            self.image = pygame.transform.scale(self.walkRight[self.walkCount // 5 // nEnemies], (self.w, self.h))
            self.walkCount += 1

        elif self.lastSide == "right" or self.lastSide is None:
            self.image = pygame.transform.scale(self.charRight[self.animationCount // 5 // nEnemies], (self.w, self.h))

        elif self.lastSide == "left":
            self.image = pygame.transform.scale(self.charLeft[self.animationCount // 5 // nEnemies], (self.w, self.h))

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.animationCount += 1

    def dashBar(self, display):
        if self.dashCooldown > 150:
            self.dashCooldown = 150
        if self.dashCooldown > 8:
            self.vel = 3.5
        self.dashCooldown += 1
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(self.x + 12, self.y + 12, 170 // 5, 7))
        pygame.draw.rect(display, (32, 176, 247), pygame.Rect(self.x + 14, self.y + 13, self.dashCooldown // 5, 5))

    def lifeBar(self, display):
        if self.life > 100:
            self.life = 100
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(18, 18, 101 * 2, 20))
        pygame.draw.rect(display, (0, 255, 0), pygame.Rect(20, 20, self.life * 2, 16))


class HandleWeapon:
    def __init__(self, player):
        self.player = player
        self.weaponImage = pygame.image.load('data/projectiles/weapon_anime_sword.png').convert_alpha()
        self.weaponImage = pygame.transform.rotate(self.weaponImage, -90)

    def main(self, display):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.player.x-20, mouse_y - self.player.y-55
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        playerWeaponCopy = pygame.transform.rotate(self.weaponImage, angle)
        display.blit(playerWeaponCopy, (self.player.x+20-int(playerWeaponCopy.get_width()/2), self.player.y+55-int(playerWeaponCopy.get_height()/2)))


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y, player, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.player_x = player.x
        self.player_y = player.y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.image = pygame.image.load('data/projectiles/weapon_anime_sword.png').convert_alpha()
        self.projectileCopy = pygame.transform.rotate(self.image, -90)
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def main(self):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        rel_x, rel_y = self.mouse_x - self.player_x - 20, self.mouse_y - self.player_y - 55
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.image = pygame.transform.rotate(self.projectileCopy, angle)

        self.rect = pygame.Rect(self.x+5-int(self.image.get_width()/2), self.y-5-int(self.image.get_height()/2), self.image.get_width(), self.image.get_height())
