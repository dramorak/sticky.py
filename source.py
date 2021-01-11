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
        self.win = None
        
    def __repr__(self):
        return "Just draw it the stick figure, I don't want to stringify it."

    def draw(self, win=None, breadth=False):
        if win==None:
            self.win = GraphWin('', 1000,1000)
            self.win.setCoords(-500, -500, 500, 500)
        else:
            self.win = win
            

        if breadth:
            def bfiter(root):
                nodes = [root]
                while nodes:
                    new = []
                    for x in nodes:
                        new += x.children
                        yield x
                    nodes = new
                    
            for x in bfiter(self.root):
                for child in x.children:
                    Line(x.val, child.val).draw(self.win)
        else:
            def r(root: TreeNode):
                for child in root.children:
                    r(child)
                    Line(root.val, child.val).draw(self.win)
            r(self.root)

    def close(self):
        if self.win == None:
            return "Failed: window not open"
        else:
            self.win.close()
            self.win == None
                
    def save(self, filepath, filename):
        if self.win==None:
            return "Failed: nothing to save."
        else:
            save_location = filepath + '\\' + filename + '.eps'
            self.win.postscript(file=save_location, colormode='color')
            return 'Saved.'
        
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

def recurse(f):
    return f(lambda: recurse(f))

def create_rec(step):
    def f1(f):
        return step(f())
    return f1

# This is confusing !
# hahaha
    

### TESTING AND PLAYGROUND ### 

def fractal1(d):
    if d == 0:
        return StickFigure()

    left = fractal1(d-1)
    right = fractal1(d-1)

    left.scale(0.83)
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

def fractal2(d):
    if d == 0:
        return StickFigure()

    left = fractal2(d-1)
    right = left.copy()
    center = left.copy()

    left.scale(0.5)
    right.scale(0.5)
    center.scale(0.7)
    left.rotate(pi/5)
    right.rotate(-pi/5)

    cur = Stick(Point(0,0), Point(0,70))

    cur.attatch(left)
    cur.attatch(right)
    cur.attatch(center)

    return cur

def fractal3(d):
    if d == 0:
        return StickFigure()

    left = fractal3(d-1)
    right = left.copy()

    left.rotate(pi/4)
    right.rotate(-pi/4)
    
    left.scale(0.6)
    right.scale(0.6)
    
    p1 = Point(0,0)
    p2 = Point(50,50)
    p3 = Point(-50,50)
    p4 = Point(0,100)

    s1 = Stick(p1,p2)
    s2 = Stick(p1,p3)
    s3 = Stick(p3,p4)
    
    s3.attatch(left, s3.branch)
    s2.attatch(s3, s2.branch)
    s1.attatch(s2, s1.root)
    s1.attatch(right, s1.branch)
    
    return s1
    
def fractal4(d):
    if d == 0:
        return StickFigure()

    left = fractal4(d-1)
    right = left.copy()

    left.scale(0.5)
    left.rotate(pi/6)

    right.rotate(-pi/6)
    right.scale(0.4)
    
    p1 = Point(0,0)
    p2 = Point(0,50)
    p3 = Point(0,80)
    p4 = Point(0,100)

    s1 = Stick(p1,p2)
    s2 = Stick(p2,p3)
    s3 = Stick(p3,p4)

    s1.attatch(s2,s1.branch)
    s2.attatch(s3,s2.branch)
    s2.attatch(right, s2.branch)
    s1.attatch(left, s1.branch)

    return s1
    
f1 = fractal1(10)
f2 = f1.copy()
f2.rotate(pi)

f1.attatch(f2, f1.root)

f1.draw(breadth=True)



    
