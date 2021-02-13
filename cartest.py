import pymunk
import pymunk.pygame_util
import pygame
import math
from pymunk.vec2d import Vec2d
#import math
#from PIL import Image
space = pymunk.Space()
space.gravity = 0, -100
b0 = space.static_body
size = w, h = 1200, 600
fps = 30
steps = 10
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
WHITE = (255, 255, 255)
def info(body):
    print("m={body.mass:.0f} moment={body.moment:.0f}")
    cg = body.center_of_gravity
    print(cg.x, cg.y)
class PinJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0)):
        joint = pymunk.constraint.PinJoint(b, b2, a, a2)
        space.add(joint)
class PivotJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), collide=True):
        joint = pymunk.constraint.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        space.add(joint)
class SlideJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), min=50, max=100, collide=True):
        joint = pymunk.constraint.SlideJoint(b, b2, a, a2, min, max)
        joint.collide_bodies = collide
        space.add(joint)
class GrooveJoint:
    def __init__(self, a, b, groove_a, groove_b, anchor_b):
        joint = pymunk.constraint.GrooveJoint(
            a, b, groove_a, groove_b, anchor_b)
        joint.collide_bodies = False
        space.add(joint)
class DampedRotarySpring:
    def __init__(self, b, b2, angle, stiffness, damping):
        joint = pymunk.constraint.DampedRotarySpring(
            b, b2, angle, stiffness, damping)
        space.add(joint)
class RotaryLimitJoint:
    def __init__(self, b, b2, min, max, collide=True):
        joint = pymunk.constraint.RotaryLimitJoint(b, b2, min, max)
        joint.collide_bodies = collide
        space.add(joint)
class RatchetJoint:
    def __init__(self, b, b2, phase, ratchet):
        joint = pymunk.constraint.GearJoint(b, b2, phase, ratchet)
        space.add(joint)
class SimpleMotor:
    def __init__(self, b, b2, rate):
        joint = pymunk.constraint.SimpleMotor(b, b2, rate)
        space.add(joint)
class GearJoint:
    def __init__(self, b, b2, phase, ratio):
        joint = pymunk.constraint.GearJoint(b, b2, phase, ratio)
        space.add(joint)
class Segment:
    def __init__(self, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0.5
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)
class Circle:
    def __init__(self, pos, radius=20):
        self.body = pymunk.Body()
        self.body.position = pos
        shape = pymunk.Circle(self.body, radius)
        shape.density = 0.1
        self.collide_bodies = False
        shape.friction = 0.5
        shape.elasticity = 1
        space.add(self.body, shape)
class Box:
    def __init__(self, p0=(0, 0), p1=(w, h), d=4):
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(
                space.static_body, pts[i], pts[(i+1) % 4], d)
            segment.elasticity = 0
            segment.friction = 0
            space.add(segment)
class Poly:
    def __init__(self, pos, vertices):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos
        shape = pymunk.Poly(self.body, vertices)
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.density = 0.01
        shape.elasticity = 0.5
        shape.color = (255, 0, 0, 0)
        space.add(self.body, shape)
class Polygon:
    def __init__(self, pos, vertices, density=0.1):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos
        shape = pymunk.Poly(self.body, vertices)
        shape.density = 0.1
        shape.elasticity = 1
        space.add(self.body, shape)
class Rectangle:
    def __init__(self, pos, size=(80, 50)):
        self.body = pymunk.Body()
        self.body.position = pos
        shape = pymunk.Poly.create_box(self.body, size)
        shape.density = 0.1
        shape.elasticity = 1
        shape.friction = 1
        space.add(self.body, shape)
class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.image.save(self.screen, 'shape.png')
            self.screen.fill((220, 220, 220))
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)
        pygame.quit()
if __name__ == '__main__':
    Box()
##################################
#Add your code here!
    body = pymunk.Body(mass=1, moment=1000)
    for i in range(10):
        body1 = pymunk.Body(mass=1, moment=1000)
        body1.position = (300, 280)
        body1.apply_impulse_at_local_point((10, 0), (0, 1))

        shape = pymunk.Segment(body1, (60,30),(10,0), radius=5)
        shape.elasticity = 1
        shape.friction = 1
        shape.density=1
        shape.mass = 0.8

        shape2 = pymunk.Segment(body1, (60,30),(0,-10), radius=5)
        shape2.elasticity = 0.5
        shape2.density = 0.1
        shape2.friction = 0
        shape2.mass = 0.8
        space.add(body1,shape)

    space.add(body)

p = Vec2d(100,150)
vs = [(-60,-25),(60,-10),(40,20),(-50,15)]
v0,v1,v2,v3 = vs
chassis = Poly(p,vs)


#wheel2 = Circle(p+v1,30)
#wheel2.elasticity = 0
#wheel2.friction = 1


#PivotJoint(chassis.body,wheel2.body,v1,(0,0),False)
#SimpleMotor(chassis.body, wheel1.body,0.1)

#objective: create
p0 = p+(60,-10)
v = Vec2d(80, 10)
arm = Segment(p0, v)
arm.elasticity = 0
arm.friction = 0.5
PivotJoint(chassis.body, arm.body, (60,-10),(0,00))
SimpleMotor(chassis.body, arm.body, 0.5)
arm2 = Segment(p0+v, v)
PivotJoint(arm.body, arm2.body, v, (0, 0))
#RotaryLimitJoint(arm.body, arm2.body, 0, 2)
DampedRotarySpring(arm.body, arm2.body, 0, 100000, 10000)

p0 = p+(-60,-25)
armb = Segment(p0, v)
armb.friction = 100
armb.elasticity = 0
PivotJoint(chassis.body, armb.body, (-60,-25),(0,00))
GearJoint(arm.body, armb.body, 2.5, 10000)


#SimpleMotor(chassis.body, arm.body, 5)
arm2b = Segment(p0+v, v)
PivotJoint(armb.body, arm2b.body, v, (0, 0))
#RotaryLimitJoint(armb.body, arm2b.body, 0, 2)
DampedRotarySpring(armb.body, arm2b.body, 0, 100000, 10000)
#Circle(p0+(0,0), 20)

wheel1 = Circle(p+v,30)
wheel1.friction = 1
wheel1.elasticity = 1
PivotJoint(arm2b.body,wheel1.body,v,(0,0),False)
SimpleMotor(armb.body, wheel1.body,0.1)

#wheel2 = Circle(p+(30,0),30)
#wheel2.friction = 1
#wheel2.elasticity = 1
#PivotJoint(wheel2.body,arm2.body,(0,0),(0,0),False)
################################3
App().run()