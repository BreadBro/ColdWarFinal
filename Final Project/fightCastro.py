import pygame, sys, random, time, os, threading, datetime, math
from threading import *
from datetime import datetime
from pygame import mouse

class Boss:
    x = 0
    y = 0
    hp = 0
    hpRedBar = pygame.Rect(20, 20, 984, 40)
    def __init__(self, name, image, hp):
        self.name = name
        self.image = image
        self.hp = hp
        self.hpBar = pygame.Rect(20, 20, int(984 * float(hp/100)), 40)
        self.direction = True
        self.hitbox = pygame.Rect(self.x+43, self.y, 170, 256)
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setHP(self, hp):
        self.y = hp
    def setImage(self, image):
        self.image = image
    def getBar(self):
        return self.hpBar
    def changeDir(self, direction):
        if direction != self.direction and (castro.x < 383 or castro.x > 385):
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction
    def getCenter(self):
        return (self.x + 128, self.y + 128)
    def updateHitbox(self):                 #46
        self.hitbox = pygame.Rect(self.x+63, self.y, 130, 200)
    def updatehpBar(self):
        self.hpBar = pygame.Rect(20, 20, int(984 * float(self.hp/100)), 40)
        
    def pointCollide(self, point):
        if point[0] > self.x + 43 and point[0] < self.x + 213:
            if point[1] > self.y and point[1] < self.y + 256:
                return True
        return False
class Player:
    x = 0
    y = 0
    hp = 0
    hpBackground = pygame.Rect(10, 830, 220, 60)
    def __init__(self, name, image, hp):
        self.name = name
        self.image = image
        self.hp = hp
        self.direction = True
        self.hpBar = pygame.Rect(20, 840, int(200 * float(hp/100)), 40)
        self.hitbox = pygame.Rect(self.x+19, self.y, 90, 128)
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def setHP(self, hp):
        self.y = hp
    def setImage(self, image):
        self.image = image
    def changeDir(self, direction):
        if direction != self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction
    def getCenter(self):
        return (self.x + 64, self.y + 64)
    def updateHitbox(self):
        self.hitbox = pygame.Rect(self.x+30, self.y, 68, 128)
    def updatehpBar(self):
        self.hpBar = pygame.Rect(20, 840, int(200 * float(self.hp/100)), 40)
        

class Bullet:
    ammo = 5
    slope = 0
    speed = 2
    def __init__(self, agent):
        self.x = agent.x + 64
        self.y = agent.y + 64
        self.color = black
        self.defPoints = [(-10, 5), (-10, -5), (10, -5), (10, 5)]
        self.damage = 1
    def changeWeapon(self, weaponType):
        if weaponType == 1:
            self.speed = 1
            self.defPoints = [(-10, 5), (-10, -5), (10, -5), (10, 5)]
            self.color = black
            self.damage = 3
        if weaponType == 2:
            self.speed = 0.1
            self.defPoints = [(-20, 8), (-20, -8), (20, -8), (20, 8)]
            self.color = (139, 69, 19)
            self.damage = 10
        
    def render(self, mx, my, agent):
        # get length of the sides of triangle from center to cursor
        x = mx - agent.x - 64
        y = my - agent.y - 64

        # slope = y / x
        self.slope = y / x
        #angle = math.asin(y / hypo)

        # x1 = topL, x2 = botL, x3 = botR, x4 = topR
        # put points to correct starting position
        #points = [(agent.x + 54, agent.y + 59), (agent.x + 54, agent.y + 69), (agent.x + 74, agent.y + 69), (agent.x + 74, agent.y + 59)]
        cursAng = math.atan(y / x)
        points = [(0,0), (0,0), (0,0), (0,0)]
        if x < 0:
            cursAng += math.pi
        # rotation matrix
        for i in range(0, 4):
            temp = list(self.defPoints[i])
            tempX = temp[0]
            tempY = temp[1]
            temp[0] = tempX * math.cos(cursAng) - tempY * math.sin(cursAng)
            temp[1] = tempX * math.sin(cursAng) + tempY * math.cos(cursAng)
            temp[0] += agent.x + 64
            temp[1] += agent.y + 64
            points[i] = tuple(temp)
        return points
    def reset(self):
        return [(-200, -200), (-200, -300), (-100, -200), (-100, -300)]

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target()

pygame.init()
pygame.mixer.init()
path = os.path.dirname(os.path.abspath(__file__))
path = str(path)
path = path + "\\PNGS\\"
background = pygame.image.load(path + "bg.png")
origCastro = pygame.image.load(path + "castro.png")
origAgent = pygame.image.load(path + "agent.png")
castroImg = pygame.transform.scale(origCastro, (256, 256))
agentImg = pygame.transform.scale(origAgent, (128, 128))
width = 1024
height = 900
screen = pygame.display.set_mode([width, height])
LETTER_FONT = pygame.font.SysFont('COPPERPLATE GOTHIC BOLD"', 40)
WORD_FONT = pygame.font.SysFont('COPPERPLATE GOTHIC BOLD"', 60)
TITLE_FONT = pygame.font.SysFont('COPPERPLATE GOTHIC BOLD"', 70)
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
castro = Boss("Castro", castroImg, 100)
agent = Player("Agent", agentImg, 100)
bullet = Bullet(agent)
direction = True
dt = 0
deathCount = 0
damageMult = 0.07
bossDamageMult = 0.15
clock = pygame.time.Clock()

def main():
    beginning()
    
def game():
    agent.hp = 100
    castro.hp = 100
    castEvent = 27
    global mx
    global my
    spacePressed = False
    weirdExcept = False
    dashing = False
    mouseDown = False
    circleSpeed = 0.1
    jumpCount = 100
    eventCount = 0
    done = False
    circleTemp = False
    renderOrNo = [1, 1, 1]
    mouse.set_pos(height/2, width/2)
    screen.blit(background, (0,-124))
    castro.y = 560
    screen.blit(background, (0, -124))
    past = datetime.now()
    beamTime = datetime.now()
    pastDash = datetime.now()
    circTimer = datetime.now()
    timeOfEventEnd = datetime.now()
    pauseTimer = datetime.now()
    startBeamTimer = True
    explosionCircle = False
    agent.setX(700)
    agent.setY(685)
    leftRect = pygame.Rect(112, 0, 200, 910)
    midRect = pygame.Rect(412, 0, 200, 910)
    rightRect = pygame.Rect(712, 0, 200, 910)
    halfRectL = pygame.Rect(0, 0, 512, 910)
    halfRectR = pygame.Rect(512, 0, 512, 910)
    botRect = pygame.Rect(0, 600, 1024, 400)
    moving = 0
    rDown = False
    switched = False
    lDown = False
    eventDone = True
    beamEvent = -1
    bulletMoving = False
    points = [(-200, -200), (-200, -300), (-100, -200), (-100, -300)]
    bulletExist = False
    dir = 0
    clock = pygame.time.Clock()
    randInRow = 0
    castTargetX = 0
    dt = 0
    
    while True:
        now = datetime.now()
        mx, my = mouse.get_pos()
        agent.updateHitbox()
        castro.updateHitbox()
        # sets background
        screen.blit(background, (0, -124))
        # boss random direction
        if ((now - past).total_seconds() > 0.7):
            temp = dir
            dir = random.randrange(-1, 2, 1)
            past = datetime.now()
            if temp == dir:
                randInRow += 1
            else:
                randInRow = 0
            if randInRow == 3:
                if dir == -1:
                    dir = random.randrange(0, 2, 1)
                elif dir == 0:
                    dir = random.randrange(-1, 2, 2)
                else:
                    dir = random.randrange(-1, 1, 1)
        
        if eventDone or castEvent == 1:
            castro.setX(castro.x + 0.25 * dir * dt)
            if (dir < 0):
                castro.changeDir(False)
            elif (dir > 0):
                castro.changeDir(True)
        if castro.x > 768:
            castro.x =  766.0
        if castro.x < 0:
            castro.x = 2.0
        # boxx movement
        if not eventDone and castro.x != castTargetX and (now - timeOfEventEnd).total_seconds() > 5 and castEvent == 0:
            if castTargetX < castro.x:
                dir = -1
                castro.changeDir(False)
            elif castTargetX > castro.x:
                dir = 1
                castro.changeDir(True)
            castro.setX(castro.x + 0.25 * dir * dt)
            if abs(castro.x - castTargetX) < 4:
                castro.x = 384
        # agent movement
        if not dashing and moving != 0 and (rDown == True or lDown == True) and (agent.x + 0.7 * moving * dt > 0 and agent.x + 0.7 * moving * dt < 900):
            agent.setX(agent.x + 0.7 * moving * dt)
        if (now - pastDash).total_seconds() < 0.1 and dashing and moving != 0 and (rDown == True or lDown == True) and (agent.x + 2 * moving * dt > 0 and agent.x + 2 * moving * dt < 900):
            agent.setX(agent.x + 3 * moving * dt)
        if (now - pastDash).total_seconds() > 0.2:
            dashing = False
            bossDamageMult = 0.15
        if mouseDown and not bulletExist and not weirdExcept:
            bullet.x = agent.x + 64
            bullet.y = agent.y + 64
            points = bullet.render(mx, my, agent)
            bulletMoving = True
            #explosionCircle = False
            bulletExist = True
            if my < agent.y + 64:
                if mx < agent.x + 64:
                    quadrant = 2
                else:
                    quadrant = 1
            else:
                if mx < agent.x + 64:
                    quadrant = 3
                else: 
                    quadrant = 4
        #jump
        if agent.y > 685:
            agent.y = 685
        if spacePressed:
            if jumpCount >= -100:
                neg = 1
                if jumpCount < 0:
                    neg = -1
                if not dashing:
                    #            parabola        height
                    agent.y -= (jumpCount ** 2) * 0.00009 * neg * dt
                    jumpCount -= 2
                else:
                    jumpCount = 0
            else:
                jumpCount = 100
                spacePressed = False
                agent.setY(685)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if bulletExist:
                        switched = True
                    else:
                        bullet.changeWeapon(1)
                if event.key == pygame.K_2:
                    if bulletExist:
                        switched = True
                    else:
                        bullet.changeWeapon(2)
                if event.key == pygame.K_ESCAPE:
                    tempx, tempy = mx, my
                    moving = 0
                    pauseTimer = datetime.now()
                    showExitMenu()
                    now = datetime.now()
                    pauseTimer -= now
                    past += pauseTimer
                    beamTime += pauseTimer
                    pastDash += pauseTimer
                    circTimer += pauseTimer
                    timeOfEventEnd += pauseTimer

                    # add everything else that needs to be blitted as well
                    # might not need to though since everything else moves
                    #screen.blit(background, (0,-124))
                    mouse.set_pos(tempx,tempy)
                if event.key == pygame.K_d:
                    agent.changeDir(True)
                    moving = 1
                    rDown = True
                if event.key == pygame.K_a:
                    agent.changeDir(False)
                    moving = -1
                    lDown = True
                if event.key == pygame.K_w:
                    spacePressed = True
                if event.key == pygame.K_LSHIFT:
                    if not dashing:
                        pastDash = datetime.now()
                        dashing = True
                        bossDamageMult = 0
            # if a button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True
                    if explosionCircle:
                        weirdExcept = False
                    if bulletExist and bullet.speed == 0.1:
                        bulletExist = False
                        bulletMoving == False
                        explosionCircle = True
                        if quadrant == 1 or quadrant == 4:
                            cigExplPoint = points[2]
                        if quadrant == 2 or quadrant == 3:
                            cigExplPoint = points[3]
                        circTimer = datetime.now()
                        r = 0
                        weirdExcept = True
                        points = bullet.reset()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseDown = False

            #if a button is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    lDown = False
                    if rDown == True:
                        agent.changeDir(True)
                        moving = 1
                if event.key == pygame.K_LSHIFT:
                    dashing = False
                if event.key == pygame.K_d:
                    rDown = False
                    if lDown == True:
                        agent.changeDir(False)
                        moving = -1


        #checks if there is a collision between castro and player
        if (agent.hitbox.colliderect(castro.hitbox) and not dashing):
            agent.hp -= bossDamageMult
            castro.hp -= damageMult

        if switched:
            if not bulletExist:
                if bullet.speed == 0.1:
                    bullet.changeWeapon(1)
                else:
                    bullet.changeWeapon(2)
                switched = False
        # boss attack patterns
        if eventDone and (now - timeOfEventEnd).total_seconds() > 5:
            temp = castEvent
            castEvent = random.randrange(0, 2, 1)
            if (temp == castEvent):
                eventCount += 1
            if eventCount == 3:
                if castEvent == 0:
                    castEvent == 1
                if castEvent == 1:
                    castEvent == 0

            if (temp != castEvent):
                eventCount = 0

            #random.randrange(0, 2, 1)
            if castEvent == 0:
                startBeamTimer = True
            if castEvent == 1:
                done = False
                renderOrNo = [1,1,1]
                circlePoints = [(castro.x + 128, castro.y + 128), (castro.x + 128, castro.y + 128), (castro.x + 128, castro.y + 128)]
            eventDone = False
        
        # Circle Pattern
        if castEvent == 1 and not eventDone:
            if not done and circlePoints[1][1] > 481:
                temp = list(circlePoints[0])
                temp[0] -= 0.3 * dt
                temp[1] -= 0.3 * dt
                circlePoints[0] = tuple(temp)

                temp = list(circlePoints[1])
                temp[1] -= 0.3 * dt
                circlePoints[1] = tuple(temp)

                temp = list(circlePoints[2])
                temp[0] += 0.3 * dt
                temp[1] -= 0.3 * dt
                circlePoints[2] = tuple(temp)

            if not done and circlePoints[1][1] > 477 and circlePoints[1][1] < 483:
                circleTemp = True
                for i in range(0, 3):
                    circlePoints[i] = tuple((circlePoints[i][0], 480))
            if not done and circleTemp:
                temp = list(circlePoints[0])
                temp[1] -= 0.3 * dt
                circlePoints[0] = tuple(temp)

                temp = list(circlePoints[1])
                temp[1] -= 0.3 * dt
                circlePoints[1] = tuple(temp)

                temp = list(circlePoints[2])
                temp[1] -= 0.3 * dt
                circlePoints[2] = tuple(temp)
            if not done and circlePoints[1][1] > 207 and circlePoints[1][1] < 213:
                circleTemp = False
                for i in range(0, 3):
                    circlePoints[i] = tuple((circlePoints[i][0], 210))
            if not done and circlePoints[1][1] < 213 and circlePoints[1][1] > 207:
                done = True
            if done:
                circSlopes = [(circlePoints[0][1] - agent.y - 64) / (circlePoints[0][0] - agent.x - 64)]
                circSlopes.append((circlePoints[1][1] - agent.y - 64) / (circlePoints[1][0] - agent.x - 64))
                circSlopes.append((circlePoints[2][1] - agent.y - 64) / (circlePoints[2][0] - agent.x - 64))
                for i in range(0, 3):
                    
                    if circlePoints[i][1] < agent.y + 64:
                        if circlePoints[i][0] < agent.x + 64:
                            temp = list(circlePoints[i])
                            temp[0] += (circleSpeed * dt) / math.sqrt(1 + pow(circSlopes[i],2)) * renderOrNo[i]
                            temp[1] += (circleSpeed * circSlopes[i] * dt) / math.sqrt(1 + pow(circSlopes[i], 2)) * renderOrNo[i]
                            circlePoints[i] = tuple(temp)

                        else:
                            temp = list(circlePoints[i])
                            temp[0] -= (circleSpeed * dt) / math.sqrt(1 + pow(circSlopes[i],2)) * renderOrNo[i]
                            temp[1] -= (circleSpeed * circSlopes[i] * dt) / math.sqrt(1 + pow(circSlopes[i], 2)) * renderOrNo[i]
                            circlePoints[i] = tuple(temp)
                    else:
                        if circlePoints[i][0] < agent.x + 64:
                            temp = list(circlePoints[i])
                            temp[0] += (circleSpeed * dt) / math.sqrt(1 + pow(circSlopes[i],2)) * renderOrNo[i]
                            temp[1] += (circleSpeed * circSlopes[i] * dt) / math.sqrt(1 + pow(circSlopes[i], 2)) * renderOrNo[i]
                            circlePoints[i] = tuple(temp)
                        else: 
                            temp = list(circlePoints[i])
                            temp[0] -= (circleSpeed * dt) / math.sqrt(1 + pow(circSlopes[i],2)) * renderOrNo[i]
                            temp[1] -= (circleSpeed * circSlopes[i] * dt) / math.sqrt(1 + pow(circSlopes[i], 2)) * renderOrNo[i]
                            circlePoints[i] = tuple(temp)
                for i in range(0, 3):
                    circleRect = pygame.Rect(circlePoints[i][0] - 20, circlePoints[i][1] - 20, 40, 40)
                    if circlePoints[i][0] < 0 or circlePoints [i][0] > 1028 or circlePoints[i][1] > 900 or circlePoints[i][1] < 0 or circleRect.colliderect(agent.hitbox) or circleRect.colliderect(castro.hitbox):
                        renderOrNo[i] = 0
                    if circleRect.colliderect(agent.hitbox):
                        if not dashing:
                            agent.hp -= bossDamageMult * 100
                        circlePoints[i] = tuple((-200, -200))
                    if circleRect.colliderect(castro.hitbox):
                        castro.hp -= bossDamageMult * 2
                        circlePoints[i] = tuple((-200, -200))
                    if pointInRect(points[0], circleRect):
                        circlePoints[i] = tuple((-200, -200))
                        bulletMoving = False
                        bulletExist = False
                        points = bullet.reset()

            for i in range(0, 3):
                if renderOrNo[i] == 1:
                    pygame.draw.circle(screen, black, circlePoints[i], 20)
            if renderOrNo[0] == 0 and renderOrNo[1] == 0 and renderOrNo[2] == 0:
                eventDone = True
                done = False
                timeOfEventEnd = datetime.now()

        # beam pattern
        if castEvent == 0 and not eventDone:
            if beamEvent == -1:
                beamEvent = random.randrange(0, 3, 1)
            castTargetX = 384
            if castro.x > 383 and castro.x < 385:
                castro.y = 200
                if startBeamTimer:
                    beamTime = datetime.now()
                    startBeamTimer = False 
                if (now - beamTime).total_seconds() > 4.4:
                    eventDone = True
                    castro.y = 560
                    timeOfEventEnd = datetime.now()
                    beamEvent = -1
        if castEvent == 0 and beamEvent == 0 and not eventDone and castro.y == 200:
            if (now - beamTime).total_seconds() < 0.8:
                if leftRect.height != 40:
                    leftRect.height = 40
                    midRect.height = 40
                    rightRect.height = 40
                pygame.draw.rect(screen, (0, 0, 255), leftRect)
                pygame.draw.rect(screen, (0, 0, 255), midRect)
                pygame.draw.rect(screen, (0, 0, 255), rightRect)
            if (now - beamTime).total_seconds() > 0.8:
                if leftRect.colliderect(agent.hitbox) or midRect.colliderect(agent.hitbox) or rightRect.colliderect(agent.hitbox):
                    agent.hp -= 3 * bossDamageMult
                if leftRect.height == 40:
                    leftRect.height = 910
                    midRect.height = 910
                    rightRect.height = 910
            pygame.draw.rect(screen, (0, 0, 255), leftRect)
            pygame.draw.rect(screen, (0, 0, 255), midRect)
            pygame.draw.rect(screen, (0, 0, 255), rightRect)

        if castEvent == 0 and beamEvent == 1 and not eventDone and castro.y == 200:
            if (now - beamTime).total_seconds() < 0.8:
                if halfRectL.height != 40:
                    halfRectL.height = 40
                pygame.draw.rect(screen, (0, 0, 255), halfRectL)
            if (now - beamTime).total_seconds() > 0.8:
                if halfRectL.colliderect(agent.hitbox):
                    agent.hp -= 3 * bossDamageMult
                if halfRectL.height == 40:
                    halfRectL.height = 910
            pygame.draw.rect(screen, (0, 0, 255), halfRectL)
        if castEvent == 0 and beamEvent == 2 and not eventDone and castro.y == 200:
            if (now - beamTime).total_seconds() < 0.8:
                if halfRectR.height != 40:
                    halfRectR.height = 40
                pygame.draw.rect(screen, (0, 0, 255), halfRectR)
            if (now - beamTime).total_seconds() > 0.8:
                if halfRectR.colliderect(agent.hitbox):
                    agent.hp -= 3 * bossDamageMult
                if halfRectR.height == 40:
                    halfRectR.height = 910
            pygame.draw.rect(screen, (0, 0, 255), halfRectR)

        if castEvent == 0 and beamEvent == 3 and not eventDone and castro.y == 200:
            botIndicL = pygame.Rect(0, 600, 40, 400)
            botIndicR = pygame.Rect(984, 600, 40, 400)
            if (now - beamTime).total_seconds() < 0.8:
                pygame.draw.rect(screen, (0, 0, 255), botIndicL)
                pygame.draw.rect(screen, (0, 0, 255), botIndicR)
            if (now - beamTime).total_seconds() > 0.8:
                if botRect.colliderect(agent.hitbox):
                    agent.hp -= 3 * bossDamageMult
                pygame.draw.rect(screen, (0, 0, 255), botRect)
        screen.blit(castro.image, (math.floor(castro.x), math.floor(castro.y)))
        screen.blit(agent.image, (agent.x, agent.y))

        screen.blit(castro.image, (math.floor(castro.x), math.floor(castro.y)))
        screen.blit(agent.image, (agent.x, agent.y))

        
         
        # bullet movement 
        if bulletMoving:
            if quadrant == 1:
                for i in range(0, 4):
                    temp = list(points[i])
                    temp[0] += (bullet.speed * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    temp[1] += (bullet.speed * bullet.slope * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    points[i] = tuple(temp)
            if quadrant == 2:
                for i in range(0, 4):
                    temp = list(points[i])
                    temp[0] -= (bullet.speed * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    temp[1] -= (bullet.speed * bullet.slope * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    points[i] = tuple(temp)
            if quadrant == 3:
                for i in range(0, 4):
                    temp = list(points[i])               
                    temp[0] -= (bullet.speed * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    temp[1] -= (bullet.speed * bullet.slope * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    points[i] = tuple(temp)
            if quadrant == 4:
                for i in range(0, 4):
                    temp = list(points[i])
                    temp[0] += (bullet.speed * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    temp[1] += (bullet.speed * bullet.slope * dt) / math.sqrt(1 + pow(bullet.slope, 2))
                    points[i] = tuple(temp)

            if points[0][0] < -30 or points[0][0] > 1040 or points[0][1] < -30 or points[0][1] > 920:
                bulletMoving = False
                bulletExist = False
            if bullet.speed == 0.1 and points[0][0] > -30 and points[0][0] < 1040 and ((points[0][1] < 802 and points[0][1] > 798) or castro.pointCollide(points[0])):
                bulletExist = False
                bulletMoving == False
                explosionCircle = True
                if quadrant == 1 or quadrant == 4:
                    cigExplPoint = points[2]
                if quadrant == 2 or quadrant == 3:
                    cigExplPoint = points[3]
                
                circTimer = datetime.now()
                r = 0
        
        # cigar explosion circle
        if explosionCircle == True:
            if (r < 50):
                r += 0.5 * dt
            pygame.draw.circle(screen, red, cigExplPoint, r)
            circRect = pygame.Rect(cigExplPoint[0] - r, cigExplPoint[1] - r, 2 * r, 2 * r)
            if circRect.colliderect(castro.hitbox):
                castro.hp -= dt * damageMult * 0.01
            if (now - circTimer).total_seconds() > 4 or (bullet.speed == 0.1 and bulletExist):
                explosionCircle = False

        castro.updatehpBar()
        agent.updatehpBar()
        pygame.draw.rect(screen, red, castro.hpRedBar)
        pygame.draw.rect(screen, green, castro.hpBar)
        pygame.draw.rect(screen, black, agent.hpBackground)
        pygame.draw.rect(screen, white, agent.hpBar)
        pygame.draw.polygon(screen, bullet.color, points)
        if castro.pointCollide(points[0]):
            castro.hp -= bullet.damage * damageMult
            bulletMoving = False
            bulletExist = False
            points = bullet.reset()

        if agent.hp < 0:
            endScene()
        if castro.hp < 0:
            castroDeath()
        pygame.display.update()
        dt = clock.tick(60)
def pointInRect(point, rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False
def beginning():
    time.sleep(1)
    castro.x = 390
    castro.y = 0
    castro.hp = 100
    while castro.y < 560:
        screen.blit(background, (0, -124))
        screen.blit(castro.image, (castro.x, castro.y))
        castro.setY(castro.y + 4)
        time.sleep(0.00002)
        pygame.display.update()
    tempBack = pygame.transform.scale(background, (3072,2700))
    time.sleep(0.7)
    screen.blit(tempBack, (-1100, -1700))
    tempCas = pygame.transform.scale(origCastro, (600, 600))
    screen.blit(tempCas, (180, 180))
    pygame.display.update()
    x = width
    textBox = pygame.Rect(x, 550, width, 350)
    time.sleep(1)
    if deathCount == 0:
        whiteBox(x, textBox)
        textAcross("It's me, Fidel Castro!")
        pygame.display.update()
        whiteBox(x, textBox)
        textAcross("You filthy capitalists will never kill me!")
        pygame.display.update()
    else:
        whiteBox(x, textBox)
        textAcross("I am Fidel Castro!")
        pygame.display.update()
        whiteBox(x, textBox)
        textAcross("You thought you could kill me?")
        pygame.display.update()
    game()

def whiteBox(x, textBox):
    while x > -14: 
        pygame.draw.rect(screen, white, textBox)
        x -= 4
        textBox = pygame.Rect(x, 600, 1024, 400)
        time.sleep(0.002)
        pygame.display.update() 

def castroDeath():
    time.sleep(1)
    castro.x = 390
    tempBack = pygame.transform.scale(background, (3072,2700))
    time.sleep(0.7)
    screen.blit(tempBack, (-1100, -1700))
    tempCas = pygame.transform.scale(origCastro, (600, 600))
    screen.blit(tempCas, (180, 185))
    pygame.display.update()
    x = width
    textBox = pygame.Rect(x, 550, width, 350)
    time.sleep(1)
    whiteBox(x, textBox)
    textAcross("Noooooooo! Not like this!")
    alphaSurf = pygame.Surface((1024, 900))
    alphaSurf.fill((0,0,0))
    alpha = 0
    alphaSurf.set_alpha(alpha)
    screen.blit(background, (0, -124))
    alpha += 1
    alphaSurf.set_alpha(alpha)
    screen.blit(castro.image, (castro.x, castro.y))
    castro.y = 560
    screen.blit(alphaSurf, (0,0))
    while castro.y < 1200:
        screen.blit(background, (0, -124))
        alpha += 2
        alphaSurf.set_alpha(alpha)
        screen.blit(castro.image, (castro.x, castro.y))
        screen.blit(agentImg, (agent.x, agent.y))
        castro.setY(castro.y + 2)
        screen.blit(alphaSurf, (0,0))
        time.sleep(0.00002)
        pygame.display.update()
    screen.blit(alphaSurf, (0, 0))
    changeDeathCount()
    whiteBox(x, textBox)
    textAcross("You thought it was over?")
    beginning()


def changeDeathCount():
    global deathCount
    deathCount += 1
    stri = "Castro Deaths: "
    tempStr = ""
    for i in range(0, len(stri)):
        tempStr += stri[i]
        screen.blit(WORD_FONT.render(tempStr, 1, white), (300, 440))
        time.sleep(0.008)
        pygame.display.update()
    textY = 440
    screen.blit(WORD_FONT.render(str((deathCount - 1)), 1, white), (650, textY))
    pygame.display.update()
    time.sleep(2)
    aboveRect = pygame.Rect(0, 0, 1024, 440,)
    belowRect = pygame.Rect(0, 480, 1024, 800)
    onRect = pygame.Rect(645, 430, 60, 900)
    while textY < 540:
        pygame.draw.rect(screen,black,onRect)
        screen.blit(WORD_FONT.render(str((deathCount - 1)), 1, white), (650, textY))
        screen.blit(WORD_FONT.render(str(deathCount), 1, white), (650, textY - 100))
        pygame.draw.rect(screen, black, aboveRect)
        pygame.draw.rect(screen, black, belowRect)
        textY += 0.5
        time.sleep(0.008)
        pygame.display.update()
    pauseText()
def textAcross(str):
    tempStr = ""
    for i in range(0, len(str)):
        tempStr += str[i]
        screen.blit(WORD_FONT.render(tempStr, 1, black), (100, 700))
        time.sleep(0.008)
        pygame.display.update()
    pauseText()

def showExitMenu():
    blurredBack = pygame.transform.smoothscale(screen, (100, 100))
    blurredBack = pygame.transform.smoothscale(blurredBack, (1024, 900))
    textA = WORD_FONT.render("Quit", 1, white)
    textC = WORD_FONT.render("Settings", 1, white)
    textB = WORD_FONT.render("Continue", 1, white)
    quitButton = pygame.Rect(362,650,300,100)
    settingsButton = pygame.Rect(362,450,300,100)
    backButton = pygame.Rect(362,250,300,100)
    screen.blit(blurredBack, (0,0))
    click = False
    settingBug = False
    x = 1
    while x == 1:
        mx, my = mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not settingBug:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    x = 0
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    settingBug = False
        if quitButton.collidepoint((mx,my)):
            if click:
                sys.exit()
        if settingsButton.collidepoint((mx,my)):
            if click:
                settings()
                click = False
                settingBug = True
        if backButton.collidepoint((mx,my)):
            if click:
                x = 0
        screen.blit(blurredBack, (0,0))
        pygame.draw.rect(screen, black, quitButton)
        pygame.draw.rect(screen, black, settingsButton)
        pygame.draw.rect(screen, black, backButton)
        screen.blit(textA, (int(width/2 - textA.get_width()/2), 680))
        screen.blit(textC, (int(width/2 - textC.get_width()/2), 480))
        screen.blit(textB, (int(width/2 - textB.get_width()/2), 280))
        pygame.display.update()

def settings():
    global damageMult
    global bossDamageMult
    textA = WORD_FONT.render("Easy", 1, white)
    textB = WORD_FONT.render("Medium", 1, white)
    textC = WORD_FONT.render("Hard", 1, white)
    textD = WORD_FONT.render("Back", 1, white)
    hardButton = pygame.Rect(362,650,300,100)
    mediumButton = pygame.Rect(362,450,300,100)
    easyButton = pygame.Rect(362,250,300,100)
    backButton = pygame.Rect(30, 800, 130, 70)
    pygame.draw.rect(screen, black, easyButton)
    pygame.draw.rect(screen, black, mediumButton)
    pygame.draw.rect(screen, black, hardButton)
    pygame.draw.rect(screen, black, backButton)
    screen.blit(textC, (int(width/2 - textA.get_width()/2), 680))
    screen.blit(textB, (int(width/2 - textB.get_width()/2), 480))
    screen.blit(textA, (int(width/2 - textC.get_width()/2), 280))
    screen.blit(textD, (45, 814))

    click = False
    
    x = 2
    while x == 2:
        mx, my = mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    time.sleep(0.5)
                    x = 1
        if easyButton.collidepoint((mx,my)):
            if click:
                damageMult = 0.07
                bossDamageMult = 0.8
                
        if mediumButton.collidepoint((mx,my)):
            if click:
                damageMult = 0.04
                bossDamageMult = 0.15

        if hardButton.collidepoint((mx,my)):
            if click:
                damageMult = 0.01
                bossDamageMult = 0.3
        if backButton.collidepoint((mx,my)):
            if click:
                time.sleep(0.5)
                x = 1
        
        pygame.display.update()

def endScene():
    blurredBack = pygame.transform.smoothscale(screen, (100, 100))
    blurredBack = pygame.transform.smoothscale(blurredBack, (1024, 900))
    textA = WORD_FONT.render("Quit", 1, white)
    textB = WORD_FONT.render("Retry", 1, white)
    textC = WORD_FONT.render("Settings", 1, white)
    quitButton = pygame.Rect(362,650,300,100)
    settingsButton = pygame.Rect(362,450,300,100)
    backButton = pygame.Rect(362,250,300,100)
    screen.blit(blurredBack, (0,0))
    pygame.draw.rect(screen, black, quitButton)
    pygame.draw.rect(screen, black, settingsButton)
    pygame.draw.rect(screen, black, backButton)
    screen.blit(textA, (int(width/2 - textA.get_width()/2), 680))
    screen.blit(textB, (int(width/2 - textB.get_width()/2), 280))
    screen.blit(textC, (int(width/2 - textC.get_width()/2), 480))
    click = False
    
    x = 1
    while x == 1:
        mx, my = mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    x = 0
        if quitButton.collidepoint((mx,my)):
            if click:
                sys.exit()
        if settingsButton.collidepoint((mx,my)):
            if click:
                settings()
        if backButton.collidepoint((mx,my)):
            if click:
                main()
        
        pygame.display.update()    

def pauseText():
    x = 1
    while x == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x = 0


main()