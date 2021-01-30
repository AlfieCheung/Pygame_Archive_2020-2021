import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import pygame
from pygame.locals import *
import random
space = pymunk.Space()
b0 = space.static_body
size = w, h = 700, 300
GRAY = (220, 220, 220)
GREEN = (14, 117, 30)
RED = (255, 0, 0)
WHITE = (255,255,255)
BROWN = (188,91,43)
screen = pygame.display.set_mode((0,0))

class Circle:
    def __init__(self, pos, radius=20):
        self.body = pymunk.Body()
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 0.01
        self.shape.friction = 0.9
        self.shape.elasticity = 1
        self.shape.color = (255,0,0,255)
        self.type = 0
        space.add(self.body, self.shape)

circleArr = []

class Box:
    def __init__(self, p0=(0, 0), p1=(w, h), d=1):
        x0, y0 = p0
        x1, y1 = p1
        ps = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(b0, ps[i], ps[(i+1) % 4], d)
            segment.elasticity = 0.7
            segment.friction = 1
            space.add(segment)
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((w,h))
        self.draw_options = DrawOptions(self.screen)
        self.running = True
        self.active_shape = None
        self.pulling = True
        self.p=(0,0)
        self.ps = (0, 0)
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.text = self.font.render("", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.p1score = 0
        self.p2score = 0
        self.pturn = 0
    def run(self):
        self.setup()
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
            self.detection()
            self.draw()
            space.step(0.001)



        pygame.quit()
    def do_event(self, event):
        keys = {K_LEFT: (-1, 0), K_RIGHT: (1, 0),
                K_UP: (0, 1), K_DOWN: (0, -1)}
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                self.running = False
            if event.key in keys:
                v = Vec2d(keys[event.key]) * 20
                if self.active_shape != None:
                    #print("Active Shape being moved!")
                    self.active_shape.body.position = self.active_shape.body.position + v
            if event.key == K_p:
                pygame.image.save(self.screen, 'mouse.png')
        elif event.type == MOUSEBUTTONDOWN:
            #print("Mouse Clicked")
            self.p = from_pygame(event.pos, self.screen)
            self.active_shape = None

            for s in circleArr:
                dist, info = s.shape.point_query(self.p)
                if s.type == 1:
                    if dist < 0:
                        self.active_shape = s.shape
                        s.body.angle = (self.p - s.body.position).angle
                        #print("Shape Activated")
            self.pulling = True
        elif event.type == MOUSEMOTION:
            if self.active_shape != None:
                self.ps = from_pygame(event.pos, self.screen)
                self.active_shape.body.angle = (self.ps - self.active_shape.body.position).angle
        elif event.type == MOUSEBUTTONUP:
            if self.active_shape != None:
                if self.pulling:
                    self.pulling = False
                    if self.pturn == 0:
                        self.pturn = 1
                    else:
                        self.pturn = 0
                    b = self.active_shape.body
                    p0 = Vec2d(b.position)
                    p1 = from_pygame(event.pos, self.screen)
                    impulse = 100 * Vec2d(p0 - p1).rotated(-b.angle)
                    b.apply_impulse_at_local_point(impulse)

    def gameover(self):
        if self.pturn == 1:
            self.text = self.font.render("GAMEOVER player one lost", True, (255, 255, 255))
            self.textRect = self.text.get_rect()
        else:
            self.text = self.font.render("GAMEOVER player two lost" , True, (255, 255, 255))
            self.textRect = self.text.get_rect()

    def detection(self):
        # hole 1 (bottom left)
        for s in circleArr:
            if s.shape != None:  # bottom
                dist, info = s.shape.point_query((20, 20))
                # print(dist)
                if dist < 0:
                    print("moved out top")
                    circleArr.remove(s)
                    space.remove(s.shape, s.shape.body)
                    self.active_shape = None
                    if s.type == 1:
                        print("game over")
                        self.gameover()
                    if s.type == 0:
                        if self.pturn == 1:
                            self.p1score += 1
                        else:
                            self.p2score += 1

        for s in circleArr:  # top
            if s.shape != None:
                dist, info = s.shape.point_query((20, 280))
                # print(dist)
                if dist < 0:
                    print("moved out")
                    circleArr.remove(s)
                    space.remove(s.shape, s.shape.body)
                    self.active_shape = None
                    if s.type == 1:
                        print("game over")
                        self.gameover()
                    if s.type == 0:
                        if self.pturn == 1:
                            self.p1score += 1
                        else:
                            self.p2score += 1
        for s in circleArr:  # right bottom
            if s.shape != None:
                dist, info = s.shape.point_query((680, 20))
                # print(dist)
                if dist < 0:
                    print("moved out")
                    circleArr.remove(s)
                    space.remove(s.shape, s.shape.body)
                    self.active_shape = None
                    if s.type == 1:
                        print("game over")
                        self.gameover()
                    if s.type == 0:
                        if self.pturn == 1:
                            self.p1score += 1
                        else:
                            self.p2score += 1
        for s in circleArr:  # right top
            if s.shape != None:
                dist, info = s.shape.point_query((680, 280))
                # print(dist)
                if dist < 0:
                    print("moved out")
                    circleArr.remove(s)
                    space.remove(s.shape, s.shape.body)
                    self.active_shape = None
                    if s.type == 1:
                        print("game over")
                        self.gameover()
                    if s.type == 0:
                        if self.pturn == 1:
                            self.p1score += 1
                        else:
                            self.p2score += 1

    def setup(self):
        Box()
        r = 16
        # 5th row
        y = 110
        for i in range(5):
            circleArr.append(Circle((100, y), r))
            y = y + 20
        # 4th row
        y = 185
        for i in range(4):
            circleArr.append(Circle((140, y), r))
            y = y - 20
        # 3rd row
        y = 175
        for i in range(3):
            circleArr.append(Circle((180, y), r))
            y = y - 20
        # 2rd row
        y = 165
        for i in range(2):
            circleArr.append(Circle((220, y), r))
            y = y - 20
        # 1st row
        circleArr.append(Circle((260, 155), r))
        # black ball
        # Circle((20, 145), r)
        # pink & blue ball
        # Circle((310, 155), r) #pink
        # Circle((510, 155), r) #blue
        # right-most 3 balls
        # Circle((610, 55), r) #bottom
        white = Circle((610, 155), r)  # middle
        circleArr.append(white)
        white.type = 1
        white.shape.color = (255, 255, 255, 255)
        for s in circleArr:
            s.shape.elasticity = 0.9


    def draw(self):
        self.screen.fill(GREEN)
        pygame.display.set_caption("player1: "+str(self.p1score) + "   player2: " +str(self.p2score))
        pygame.draw.circle(self.screen, (0,0,0),(20,20),16)
        pygame.draw.circle(self.screen, (0, 0, 0), (20, 280), 16)            #
        pygame.draw.circle(self.screen, (0, 0, 0), (680, 20), 16)
        pygame.draw.circle(self.screen, (0,0,0),(680,280),16)
        if self.active_shape != None:
            b = self.active_shape.body
            r = int(self.active_shape.radius)
            p0 = to_pygame(b.position, self.screen)
            pygame.draw.circle(self.screen, RED, p0, r, 3)
            if self.pulling:
                pygame.draw.line(self.screen, RED, p0, self.p, 3)
                pygame.draw.circle(self.screen, RED, self.p, r, 3)
        if self.active_shape != None:
            #print("Red Activated")
            s = self.active_shape
            r = int(s.radius)
            self.p = from_pygame(s.body.position, self.screen)
            #pygame.draw.circle(self.screen, RED, self.p, r+5)
            b = self.active_shape.body
            r = int(self.active_shape.radius)
            p0 = to_pygame(b.position, self.screen)
            #pygame.draw.circle(self.screen, RED, p0, r, 3)-
            if self.pulling:
                pygame.draw.line(self.screen, BROWN, (p0[0], p0[1]), (self.ps[0], -(self.ps[1]-300)), 5)
                pygame.draw.circle(self.screen, BROWN, (self.ps[0], -(self.ps[1]-300)), r, 5) ################################################################
                #self.pulling = False


        print(self.pturn)
        print("player 1:", self.p1score)
        print("player 2:", self.p2score)

        space.debug_draw(self.draw_options)

        self.textRect.center = (w // 2, h // 2)
        self.screen.blit(self.text, self.textRect)
        pygame.display.update()

if __name__ == '__main__':

        #Circle((610, 255), r) #top

        #holes

    App().run()