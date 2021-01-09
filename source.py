# Sticky.py
#
# Language of sticks
#
#
# This module builds on the simple graphics library graphics.py
# Designed as a simple language to facilitate the creation
# of recursive patterns, particularly fractals.
#
# The fundemental object of the module is the 'stickfigure', a
# general purpose multinode stick comprised object. Combination
# of objects can occur by specifying:
#   a) the two objects to be combined
#   b) which object is to be attatched to which
#   c) which node in each object is to be attatched.

import math
from graphics import *

# global constants
pi = math.pi

class TreeNode():
    def __init__(self, val = Point(0,0), *children):
        self.val = val
        self.children = list(children)
        
class StickFigure():

    """Generic base class of all objects in the language """
    def __init__(self, root = TreeNode()):
        self.root = root
        
    def __repr__(self):
        return "Just draw it the stick figure, I don't want to stringify it."
    
    def draw(self, win=None):
        if win==None:
            win = GraphWin('', 1000,1000)
            win.setCoords(-500, -500, 500, 500)
        
        def r(root: TreeNode):
            for child in root.children:
                r(child)
                Line(root.val, child.val).draw(win)
        r(self.root)
                
    
    def transform(self, f):
        # f: Point -> Point
        def r(root: TreeNode):
            root.val = f(root.val)

            for child in root.children:
                r(child)
            return
        
        r(self.root)
        
    def rotate(self, angle):
        #rotates stick figure about root by angle
        x = self.root.val.x
        y = self.root.val.y
        
        def f(point):
            dx = point.x - x
            dy = point.y - y

            t = math.cos(angle) * dx - math.sin(angle) * dy
            dy = math.sin(angle) * dx + math.cos(angle) * dy
            dx = t
            
            return Point(x+dx, y+dy)

        self.transform(f)
            
    def translate(self, dx, dy):
        # translates stick figure by dx and dy
        def f(point):
            return Point(point.x + dx, point.y + dy)
        self.transform(f)
    
    def reflect(self, angle):
        #reflects stick figure around line running through root
        def f(point):
            return Point(-point.x,point.y)
        self.rotate(-angle)
        self.transform(f)
        self.rotate(angle)

    def scale(self, factor):
        x = self.root.val.x
        y = self.root.val.y

        def f(point):
            dx = point.x - x
            dy = point.y - y
            dx = dx*factor
            dy = dy*factor

            return Point(x+dx, y+dy)
        self.transform(f)
        
    def attatch(self, stick, node=None):
        if stick == None:
            return
        if node == None:
            node = self.branch
        
        x = node.val.x
        y = node.val.y
        
        stick.translate(x - stick.root.val.x, y - stick.root.val.y)

        for x in stick.root.children:
            node.children.append(x)

    def copy(self):

        def h(node):
            root = TreeNode(node.val)
            for child in node.children:
                root.children.append(h(child))
            return root

        return StickFigure(h(self.root))
        
class Stick(StickFigure):
    def __init__(self, pt1: Point, pt2: Point):
        self.branch = TreeNode(pt2)
        self.root   = TreeNode(pt1, self.branch)
        
"""
###### TESTING ########

p1 = Point(0,0)
p2 = Point(0,100)
p3 = Point(100,0)

s1 = Stick(p1,p2)
s2 = Stick(p1,p3)

s1.attatch(s1.branch, s2)

s1.draw()
"""

def fractal1(d):
    if d == 0:
        return StickFigure()

    left = fractal(d-1)
    right = fractal(d-1)

    left.scale(0.75)
    right.scale(0.65)
    left.rotate(pi/6 + pi/12)
    right.rotate(-pi/6)

    if d >= 12:
        cur = Stick(Point(0,0),Point(0,60))
    else:
        cur = Stick(Point(0,0),Point(0,100))
    cur.attatch(left)
    cur.attatch(right)

    return cur

f = fractal(13)
f2 = f.copy()
f2.rotate(pi)
f.attatch(f2, f.root)

f.draw()



    
