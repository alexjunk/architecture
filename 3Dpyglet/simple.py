# code from https://www.youtube.com/watch?v=Hqg4qePJV2U
# Pyglet OpenGL tutorial by DLC ENERGY
# As taught by Aiden Ward

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import random

class Element:

    def get_tex(self,file):
        """
        given a png file, create a pyglet texture
        """
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z, texture):

        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) # back
        self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords) # front

        self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
        self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

        self.batch.add(4, GL_QUADS, texture[1],   ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
        self.batch.add(4, GL_QUADS, texture[2],   ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top

    def genleaves(self,X,Y,Z,H,R):
        """
        X Y Z : position de l'extrémité inférieure du tronc de l'arbre
        H : offset vertical de la couche de feuille par rapport à Z
        R : "rayon" de la couche de feuille
        """
        spruce_leave=self.spruce_leave
        for y in range(1,R+1):
            self.add_block(Y+y,Z+H,X,spruce_leave)
            self.add_block(Y-y,Z+H,X,spruce_leave)
        for x in range(1,R+1):
            for y in range(1,R-x+1):
                self.add_block(Y+y,Z+H,X+x,spruce_leave)
                self.add_block(Y+y,Z+H,X-x,spruce_leave)
                self.add_block(Y-y,Z+H,X+x,spruce_leave)
                self.add_block(Y-y,Z+H,X-x,spruce_leave)
        for x in range(1,R+1):
            self.add_block(Y,Z+H,X+x,spruce_leave)
            self.add_block(Y,Z+H,X-x,spruce_leave)

    def spruce_tree(self,X,Y,Z,H):
        """
        génération d'un sapin de hauteur H au point X Y Z
        on part du principe que les feuilles poussent à partir de Z+3
        les couches de feuilles sont espacées d'un bloc vertical les unes des autres
        le rayon du sapin sera donc de (H-3)//3 + 1
        // est la division entière !
        """
        for z in range(0,H):
            self.add_block(Y,Z+z,X,self.spruce_wood)
        HL=3
        R=1+(H-3)//2
        while HL<H:
            self.genleaves(X,Y,Z,HL,R)
            HL+=2
            R-=1
        self.add_block(Y,H,X,self.spruce_leave)

    def romanTower(self,xc,yc,zc,L,hauteur):
        """
        xc,yx,zc : coordonnées du centre de la tour
        L : demi-largeur de la tour
        hauteur : hauteur de la tour
        """
        # 4 coins
        for z in range(0,hauteur,2):
            for y in (yc-L,yc+L):
                for x in (xc-L,xc+L):
                    self.add_block(y,zc+z,x,self.uni2)
                    self.add_block(y,zc+z+1,x,self.uni1)
        # 2 murs
        for y in range(-L+1,L):
            for z in range(hauteur):
                uni=random.choice(self.uni1_tab)
                self.add_block(yc+y,zc+z,xc-L,uni)
                self.add_block(yc+y,zc+z,xc+L,uni)
        #créneaux
        for y in range(-L+1,L,2):
            self.add_block(yc+y,zc+hauteur,xc-L,self.uni1)
            self.add_block(yc+y,zc+hauteur,xc+L,self.uni1)

        # 2 murs
        for x in range(-L+1,L):
            for z in range(hauteur):
                uni=random.choice(self.uni1_tab)
                self.add_block(yc+L,zc+z,xc+x,uni)
                self.add_block(yc-L,zc+z,xc+x,uni)
        #créneaux
        for x in range(-L+1,L,2):
            self.add_block(yc+L,zc+hauteur,xc+x,self.uni1)
            self.add_block(yc-L,zc+hauteur,xc+x,self.uni1)

        #toit
        for x in range(-L+1,L):
            for y in range(-L+1,L):
                self.add_block(yc+y,zc+hauteur-2,xc+x,self.spruce_wood)

    def romanWalls(self,xs,ys,zs,l,e,h,dir):
        """
        xs,ys,zs=coordonnées du point de départ du mur
        l=longueur du mur
        h=hauteur du mur
        e=epaisseur du mur
        dir=direction(x ou y)
        """
        if dir=="x":
            for x in range(l):
                for y in range(e):
                    for z in range(h):
                        uni=random.choice(self.uni1_tab)
                        self.add_block(ys+y,zs+z,xs+x,uni)

        if dir=="y":
            for x in range(e):
                for y in range(l):
                    for z in range(h):
                        uni=random.choice(self.uni1_tab)
                        self.add_block(ys+y,zs+z,xs+x,uni)

    def castle(self,z,htc,htt,htower,l,ep):
        """
        chateau
        z : altitude du chateau
        htc : half taille chateau
        htt : half taille tower
        htower : hauteur tower
        l=longueur murs
        ep=epaisseur murs
        """
        self.romanWalls(-htc+htt,htc-1,z,l,ep,htower-7,"x")

        self.romanWalls(-htc+htt,-htc-1,z,l,ep,htower-7,"x")

        self.romanWalls(htc-1,-htc+htt,z,l,ep,htower-7,"y")

        self.romanWalls(-htc-1,-htc+htt,z,l,ep,htower-7,"y")

        self.romanTower(htc,htc,z,htt,htower)

        self.romanTower(htc,-htc,z,htt,htower)

        self.romanTower(-htc,-htc,z,htt,htower)

        self.romanTower(-htc,htc,z,htt,htower)


    def __init__(self):

        # chargement des textures depuis les png de taille 16*16
        _grass_side = self.get_tex('grass_side.png')
        _grass_bottom = self.get_tex('dirt.png')
        _grass_top = self.get_tex('grass_top.png')
        _brick_side = self.get_tex('brick_side.png')
        _brick_tb = self.get_tex('brick_top.png')
        _sL = self.get_tex('spruce_leaves1.png')
        _sW = self.get_tex('spruce_wood_trunc.png')
        _Bl = self.get_tex('birch_leaves.png')
        _Bw_top = self.get_tex('birch_top.png')
        _Bw_side = self.get_tex('birch_wood.png')
        _Sstone_side = self.get_tex('sandstone_side.png')
        _Sstone_top = self.get_tex('sandstone_top.png')
        _Sstonebrick_side = self.get_tex('sandstone_brick_side.png')
        _Sstonebrick_top = self.get_tex('sandstone_brick_top.png')
        _Colombage_right_side = self.get_tex('colombageWallRight.png')
        _Colombage_right_up_side = self.get_tex('colombageWallRight_up.png')
        _Colombage_left_side = self.get_tex('colombageWallLeft.png')
        _Colombage_left_up_side = self.get_tex('colombageWallLeft_up.png')
        _Colombage_top = self.get_tex('colombageWall_TOP.png')

        # définition des briques sous la forme d'une liste de 3 textures [side,bottom,top]
        self.grass=[_grass_side,_grass_bottom,_grass_top]
        self.brick=[_brick_side,_brick_tb,_brick_tb]
        self.dirt=[_grass_bottom,_grass_bottom,_grass_bottom]
        self.spruce_leave=[_sL,_sL,_sL]
        self.spruce_wood=[_sW,_sW,_sW]
        self.birch_leave=[_Bl,_Bl,_Bl]
        self.birch_wood=[_Bw_side,_Bw_top,_Bw_top]
        self.sandstone=[_Sstone_side,_Sstone_top,_Sstone_top]
        self.sandstone_brick=[_Sstonebrick_side,_Sstonebrick_top,_Sstonebrick_top]
        self.colombage_cornersLeft_down=[_Colombage_left_side,_Colombage_right_side,_Colombage_top]
        self.colombage_cornersRight_down=[_Colombage_right_side,_Colombage_left_side,_Colombage_top]
        self.colombage_cornersLeft_up=[_Colombage_left_up_side,_Colombage_right_up_side,_Colombage_top]
        self.colombage_cornersRight_up=[_Colombage_right_up_side,_Colombage_left_up_side,_Colombage_top]
        self.colombage_right=[_Colombage_right_side,_Colombage_left_side,_Colombage_top]
        self.colombage_left=[_Colombage_left_side,_Colombage_right_side,_Colombage_top]
        self.colombage_right_up=[_Colombage_right_up_side,_Colombage_left_up_side,_Colombage_top]
        self.colombage_left_up=[_Colombage_left_up_side,_Colombage_right_up_side,_Colombage_top]

        # textures des murs
        path="uni"

        top = self.get_tex('sandstone_brick_top.png')

        uni1=[self.get_tex('{}/uni1.png'.format(path)),top,top]
        self.uni1=uni1
        uni1_clair=[self.get_tex('{}/uni1_clair.png'.format(path)),top,top]
        uni1_clair2=[self.get_tex('{}/uni1_clair2.png'.format(path)),top,top]
        uni1_sombre=[self.get_tex('{}/uni1_sombre.png'.format(path)),top,top]
        uni1_sombre2=[self.get_tex('{}/uni1_sombre2.png'.format(path)),top,top]
        self.uni1_tab=[uni1,uni1,uni1_clair,uni1_clair2,uni1_sombre,uni1_sombre2]

        self.top=top
        self.uni2=[self.get_tex('{}/uni2.png'.format(path)),top,top]

        self.batch = pyglet.graphics.Batch()

        # (y,z,x) ??
        for y in range(-50,50,1):
            for x in range(-50,50,1):
                ground=random.choice([self.dirt, self.grass, self.grass, self.grass, self.grass, self.grass, self.grass, self.grass])
                self.add_block(y, -1, x, ground)


        """
        for z in range(0,25):
            self.add_block(-4, z, -4, brick)
            self.add_block(4, z, -4, brick)
            self.add_block(-4, z, 4, brick)
            self.add_block(4, z, 4, brick)
        """

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self,dt,keys):
        sens = 0.1
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s
        print(self.pos, self.rot)

class Window(pyglet.window.Window):

    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.pays = Element()
        #self.player = Player((0.5,1.5,1.5),(-30,0))
        #self.player = Player((6.6,12.5,18),(-51.5,7.8))
        #self.player = Player((11.3, 53.6, 64.2),(-43.6, 16.4))
        #self.player = Player((11.3, 6.269626999999993, 64.2), (18.65, -20.349999999999994))
        self.player = Player((8.4, 70, 10.5), (-84.9, 1.3))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.pays.draw()
        glPopMatrix()

"""
if __name__ == '__main__':
    window = Window(width=800, height=600, caption='architecture',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    pyglet.app.run()
"""
