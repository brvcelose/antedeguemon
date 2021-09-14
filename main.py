import random, sys, pygame, math
from pygame.locals import *
from player import Player, PlayerBullet, HandleWeapon
from enemies import SkeletonEnemy, EnemySpell

pygame.font.init()
pygame.init()


clock = pygame.time.Clock()
mouse_x, mouse_y = pygame.mouse.get_pos()
font = pygame.font.Font("data/font/font.ttf", 20)
menuFont = pygame.font.Font("data/font/font.ttf", 130)


################# SCREEN #################

screen_w = 960
screen_h = 768
pygame.mouse.set_visible(True)
win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("ANTEDEGUEMON!")
menu = pygame.image.load("data/menu.jpg").convert_alpha()
menu = pygame.transform.scale(menu, (screen_w, screen_h))
bg = pygame.image.load('data/map/map1.png').convert_alpha()
bg2 = pygame.image.load('data/map/map2.png').convert_alpha()
cursor = pygame.image.load('data/projectiles/aim.png').convert_alpha()
cursor = pygame.transform.scale(cursor, (40, 40))
startButton = pygame.image.load('data/buttons/Start Button.png').convert_alpha()
gameCredits = pygame.image.load('data/credits.png').convert_alpha()
gameOverBg = pygame.image.load('data/game_over.png').convert_alpha()
gameOverBg = pygame.transform.scale(gameOverBg, (screen_w, screen_h))
icon = pygame.image.load('data/icon.png').convert_alpha()
pygame.display.set_icon(icon)


############## MUSIC AND SFX ################
def playsMusic(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)


playerShoot = pygame.mixer.Sound('data/SFX/gun-shot-3-8-bit.wav')
playerShoot.set_volume(0.05)

hit = pygame.mixer.Sound('data/SFX/hit-5-8-bit.wav')
hit.set_volume(0.2)

hit2 = pygame.mixer.Sound('data/SFX/hit-4-8-bit.wav')
hit2.set_volume(0.15)

################# OBJECTS #################
playerGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
spellGroup = pygame.sprite.Group()
knight = Player(playerGroup)
sword = HandleWeapon(knight)
playerBullets = []
score = 0


# Redraw screen.........................................................#
def redrawGamewindow(enemiesList, enemiesSpells, timeScore):

    win.blit(bg, (0, 0))
    knight.main(1)
    for index, enemy in enumerate(enemiesList):
        enemy.main()
        enemiesSpells[index].main()
        if pygame.sprite.spritecollide(enemiesSpells[index], playerGroup, False, pygame.sprite.collide_mask):
            hit2.play()
            knight.life -= 20
            enemiesSpells[index].spell_x = 1000
            enemiesSpells[index].spell_y = 1000
            enemiesSpells[index].angle = math.atan2(enemy.y - enemy.player.y - 15, enemy.x - enemy.player.x+5)
        if pygame.sprite.spritecollide(enemy, bulletGroup, False, pygame.sprite.collide_mask):
            hit.play()
            knight.score += 10
            knight.life += 10
            pygame.sprite.Sprite.kill(enemy)
            pygame.sprite.Sprite.kill(enemiesSpells[index])
            del enemiesSpells[index]
            del enemiesList[index]

    for bullet in playerBullets:
        if 32 < bullet.x < screen_w - 46 and -10 < bullet.y < screen_h + 20:
            bullet.main()
        else:
            pygame.sprite.Sprite.kill(bullet)
            del playerBullets[playerBullets.index(bullet)]

    enemyGroup.draw(win)
    playerGroup.draw(win)
    sword.main(win)
    spellGroup.draw(win)
    bulletGroup.draw(win)
    knight.dashBar(win)
    win.blit(bg2, (0, 0))

    # HUD...........................................................#
    knight.lifeBar(win)

    win.blit(pygame.font.Font.render(font, f"SURVIVED TIME: {timeScore/1000:.2f} SECONDS", False, (255, 255, 255)), (20, 40))
    win.blit(pygame.font.Font.render(font, f"SCORE: {knight.score} POINTS", False, (255, 255, 255)), (20, 60))


# GAME LOOP ...................................................#
def mainMenu():
    click = False
    playsMusic("data/music/grotte-01.ogg")
    while True:
        clock.tick(60)

        # MENU BUTTONS................................................#
        mouse_x, mouse_y = pygame.mouse.get_pos()

        playButtonRect = pygame.Rect(180, 200, 600, 200)
        creditsButtonRect = pygame.Rect(180, 450, 600, 200)

        pygame.draw.rect(win, (255, 0, 0), playButtonRect)
        pygame.draw.rect(win, (255, 0, 0), creditsButtonRect)
        win.blit(menu, (0, 0))
        win.blit(pygame.font.Font.render(menuFont, f"MAIN MENU", False, (255, 255, 255)), (190, 40))

        win.blit(startButton, playButtonRect)
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(200, 210, 500, 170))
        win.blit(pygame.font.Font.render(menuFont, f"START", False, (255, 255, 255)), (310, 232))

        win.blit(startButton, creditsButtonRect)
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(200, 470, 500, 170))
        win.blit(pygame.font.Font.render(menuFont, f"CREDITS", False, (255, 255, 255)), (250, 480))

        if playButtonRect.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.mixer.music.stop()
                inGame()
        if creditsButtonRect.collidepoint((mouse_x, mouse_y)):
            if click:
                inCredits()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def inGame():
    playsMusic("data/music/8BitBattleLoop.ogg")
    enemiesSpells = []
    enemiesList = []
    knight.life = 100
    enemySpawn = 60
    shootCount = 60
    running = True
    timeStart = pygame.time.get_ticks()
    knight.score = 0
    while running:
        timeScore = pygame.time.get_ticks() - timeStart
        clock.tick(60)
        shootCount -= 1
        if shootCount < 0:
            shootCount = 60
        enemySpawn -= 1
        if enemySpawn < 0:
            enemySpawn = 60
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed(3)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    playsMusic("data/music/8_bit_ice_cave_lofi.mp3")
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and knight.dashCooldown >= 150:
                    knight.vel *= 4
                    knight.dashCooldown = 0

        if mouse[0] and (shootCount % 20 == 0 and shootCount != 0):
            playerShoot.play()
            playerBullets.append(PlayerBullet(knight.x + 24, knight.y + 60, mouse_x, mouse_y, knight, bulletGroup))
        if enemySpawn == 0:
            enemiesList.append(SkeletonEnemy(random.randrange(15, screen_w - 50), random.randrange(20, 700), knight, enemyGroup))
            enemiesSpells.append(EnemySpell(enemiesList[-1], spellGroup))
        if knight.life <= 0:
            pygame.mixer.music.stop()
            playsMusic("data/music/8_bit_ice_cave_lofi.mp3")
            running = False
        knight.moveset()

        redrawGamewindow(enemiesList, enemiesSpells, timeScore)
        win.blit(cursor, (mouse_x - 20, mouse_y - 20))
        pygame.mouse.set_visible(False)
        pygame.display.update()

    for index, enemy in enumerate(enemiesList):
        pygame.sprite.Sprite.kill(enemy)
        pygame.sprite.Sprite.kill(enemiesSpells[index])
    for bullet in playerBullets:
        pygame.sprite.Sprite.kill(bullet)
    pygame.mouse.set_visible(True)
    gameOver(knight.score, timeScore)
    knight.score = 0


def gameOver(score, timeScore):
    click = False
    pygame.mouse.set_visible(True)
    running = True
    while running:
        clock.tick(60)

        # MENU BUTTONS................................................#
        mouse_x, mouse_y = pygame.mouse.get_pos()

        menuButtonRect = pygame.Rect(550, 500, 400, 133)

        pygame.draw.rect(win, (255, 0, 0), menuButtonRect)
        win.blit(gameOverBg, (0, 0))
        win.blit(pygame.font.Font.render(menuFont, f"GAME OVER", False, (255, 255, 255)), (195, 45))
        win.blit(pygame.font.Font.render(menuFont, f"GAME OVER", False, (200, 0, 0)), (190, 40))

        win.blit(pygame.transform.scale(startButton, (400, 133)), menuButtonRect)
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(565, 520, 360, 100))
        win.blit(pygame.font.Font.render(menuFont, f"MENU", False, (255, 255, 255)), (620, 500))
        win.blit(pygame.font.Font.render(font, f"YOUR SCORE: {score} POINTS", False, (255, 255, 255)), (375, 250))
        win.blit(pygame.font.Font.render(font, f"SURVIDED TIME: {timeScore/1000:.2f} SECONDS", False, (255, 255, 255)), (350, 300))

        if menuButtonRect.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.mixer.music.stop()
                mainMenu()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    playsMusic("data/music/grotte-01.ogg")
                    mainMenu()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def inCredits():
    y = 250
    running = True
    while running:
        clock.tick(60)

        win.blit(menu, (0, 0))
        win.blit(gameCredits, (15, y))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        if keys[pygame.K_s] and y > -4100:
            y -= 3.5
        if keys[pygame.K_w] and y < 260:
            y += 3.5

        pygame.display.update()


# GAME START ...................................................#
if __name__ == '__main__':
    mainMenu()
