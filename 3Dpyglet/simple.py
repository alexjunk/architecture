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

        if len(texture)==3:
            self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) # back
            self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords) # front

            self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
            self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

            self.batch.add(4, GL_QUADS, texture[1],   ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
            self.batch.add(4, GL_QUADS, texture[2],   ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top

        if len(texture)==6:
            self.batch.add(4, GL_QUADS, texture[0],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) # back
            self.batch.add(4, GL_QUADS, texture[1],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords) # front

            self.batch.add(4, GL_QUADS, texture[2],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
            self.batch.add(4, GL_QUADS, texture[3],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

            self.batch.add(4, GL_QUADS, texture[4],   ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
            self.batch.add(4, GL_QUADS, texture[5],   ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top



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

    def castle(self,XC,YC,z,dct,htt,htower,ep):
        """
        chateau

        XC,YC : coordonnées du centre du chateau

        z : altitude du chateau

        dct : distance entre les centres de 2 tours alignées suivant x ou y

        htt : half taille tower

        htower : hauteur tower

        ep=epaisseur murs

        On va faire appel à 2 variables intermédiaires :

        - d moitié de dct

        - l longueur des murs
        """
        d=dct//2

        l=dct-2*htt

        self.romanWalls(XC-d+htt,YC+d-1,z,l,ep,htower-7,"x")

        self.romanWalls(XC-d+htt,YC-d-1,z,l,ep,htower-7,"x")

        self.romanWalls(XC+d-1,YC-d+htt,z,l,ep,htower-7,"y")

        self.romanWalls(XC-d-1,YC-d+htt,z,l,ep,htower-7,"y")

        self.romanTower(XC+d,YC+d,z,htt,htower)

        self.romanTower(XC+d,YC-d,z,htt,htower)

        self.romanTower(XC-d,YC-d,z,htt,htower)

        self.romanTower(XC-d,YC+d,z,htt,htower)

    def colombageFloor(self, XC, YC, ZC, H, L, l, nbw=[2,6,2,5]):
        """
        un étage de maison à colombage de hauteur H

        L, l : longueur et largeur

        XC, YC, ZC : position of the front left corner of the floor

        nbw : tableau des nombres de fenêtres par face (front, right, back, left)
        """
        verbose=False
        L=2*(L//2)
        l=2*(l//2)
        y=YC
        x=XC

        def tirage(y,taille,nb=2,plus=1):
            """
            nested function
            tire des nombres aléatoires entre y et y+plus*taille

            plus vaut 1 ou -1

            retourne un tableau de taille nb contenant ces nombres
            """
            a=[]
            while len(a) < nb :
                tirage=y+plus*random.choice(range(taille))
                if tirage not in a:
                    a.append(tirage)
            if verbose:
                print("tirage réalisé entre {} et {}".format(y,y+plus*taille))
                print("le tirage est {}".format(a))
            return a

        def hauteur(x,y,textures,plus=[0,1]):
            """
            nested function !!!
            monte une unité de mur sur toute la hauteur
            """
            for z in range(ZC,ZC+H-1):
                if ( ( abs(plus[0])*x + abs(plus[1])*y ) in a ) and z > ZC:
                    self.add_block(y, z, x, textures[2])
                else:
                    self.add_block(y, z, x, textures[0])
                if ( ( abs(plus[0])*(x+plus[0]) + abs(plus[1])*(y+plus[1]) ) in a ) and z > ZC:
                    self.add_block(y+plus[1], z, x+plus[0], textures[2])
                else:
                    self.add_block(y+plus[1], z, x+plus[0], textures[1])
            self.add_block(y, ZC+H-1, x, textures[3])
            self.add_block(y+plus[1], ZC+H-1, x+plus[0], textures[3])


        t=[self.CBLCFront,self.CBM,self.Window,self.CBALLBFront]

        if verbose:
            print("nous sommes à (x={},y={})".format(x,y))
        a=tirage(y, L-2, min(nbw[0],L-2), 1)

        while y<YC+L:
            hauteur(x,y,t,plus=[0,1])
            y+=2
        y-=1
        x-=1

        if verbose:
            print("nous sommes à (x={},y={})".format(x,y))
        a=tirage(x, l-2, min(nbw[1],l-2), -1)

        t=[self.CBRCFront,self.CBM,self.Window,self.CBALLBRight]

        while x>=XC-l:
            hauteur(x,y,t,plus=[-1,0])
            x-=2
        y-=1
        x+=1

        if verbose:
            print("nous sommes à (x={},y={})".format(x,y))
        a=tirage(y, L-2, min(nbw[2],L-2), -1)

        t=[self.CBRCBack,self.CBM,self.Window,self.CBALLBBack]

        while y>YC-1:
            hauteur(x,y,t,plus=[0,-1])
            y-=2
        y+=1
        x+=1

        if verbose:
            print("nous sommes à (x={},y={})".format(x,y))
        a=tirage(x, l-2 , min(nbw[3],l-2), 1)

        t=[self.CBLCBack,self.CBM,self.Window,self.CBALLBLeft]

        while x<=XC:
            hauteur(x,y,t,plus=[1,0])
            x+=2

    def __init__(self):
        """
        1) chargement des textures depuis les png de taille 16*16

        2) définition des briques sous la forme d'une liste de :
                - 3 textures [side,bottom,top]
                - 6 textures [front,back,left,right,bottom,top]
        """
        path="grass"

        _grass_side = self.get_tex('{}/grass_side.png'.format(path))
        _grass_bottom = self.get_tex('{}/dirt.png'.format(path))
        _grass_top = self.get_tex('{}/grass_top.png'.format(path))

        self.grass=[_grass_side,_grass_bottom,_grass_top]
        self.dirt=[_grass_bottom,_grass_bottom,_grass_bottom]

        path="brick"

        _brick_side = self.get_tex('{}/brick_side.png'.format(path))
        _brick_tb = self.get_tex('{}/brick_top.png'.format(path))

        self.brick=[_brick_side,_brick_tb,_brick_tb]

        path="tree_spruce"

        _sL = self.get_tex('{}/spruce_leaves1.png'.format(path))
        _sW = self.get_tex('{}/spruce_wood_trunc.png'.format(path))

        self.spruce_leave=[_sL,_sL,_sL]
        self.spruce_wood=[_sW,_sW,_sW]

        """
        birch trees not yet created
        """
        path="tree_birch"

        _Bl = self.get_tex('{}/birch_leaves.png'.format(path))
        _Bw_top = self.get_tex('{}/birch_top.png'.format(path))
        _Bw_side = self.get_tex('{}/birch_wood.png'.format(path))

        """
        self.birch_leave=[_Bl,_Bl,_Bl]
        self.birch_wood=[_Bw_side,_Bw_top,_Bw_top]
        """

        """
        sandstone not used - uni utilisé à la place
        top utilisé dans uni - cf plus loin
        """
        path="sandstone"
        _Sstone_side = self.get_tex('{}/sandstone_side.png'.format(path))
        _Sstone_top = self.get_tex('{}/sandstone_top.png'.format(path))
        _Sstonebrick_side = self.get_tex('{}/sandstone_brick_side.png'.format(path))
        _Sstonebrick_top = self.get_tex('{}/sandstone_brick_top.png'.format(path))
        top = self.get_tex('{}/sandstone_brick_top.png'.format(path))
        """
        self.sandstone=[_Sstone_side,_Sstone_top,_Sstone_top]
        self.sandstone_brick=[_Sstonebrick_side,_Sstonebrick_top,_Sstonebrick_top]
        """

        # textures des murs du chateau pour simuler une coinstruction en bloc de pierre de type calcaire
        path="uni"

        uni1=[self.get_tex('{}/uni1.png'.format(path)),top,top]
        self.uni1=uni1
        uni1_clair=[self.get_tex('{}/uni1_clair.png'.format(path)),top,top]
        uni1_clair2=[self.get_tex('{}/uni1_clair2.png'.format(path)),top,top]
        uni1_sombre=[self.get_tex('{}/uni1_sombre.png'.format(path)),top,top]
        uni1_sombre2=[self.get_tex('{}/uni1_sombre2.png'.format(path)),top,top]
        self.uni1_tab=[uni1,uni1,uni1_clair,uni1_clair2,uni1_sombre,uni1_sombre2]

        self.top=top
        self.uni2=[self.get_tex('{}/uni2.png'.format(path)),top,top]

        path="colombage"

        _CBR = self.get_tex('{}/colombageWallRight.png'.format(path))
        _CBL = self.get_tex('{}/colombageWallLeft.png'.format(path))
        _CBT = self.get_tex('{}/colombageWall_TOP.png'.format(path))
        _CBM = self.get_tex('{}/colombageWallMiddle.png'.format(path))
        _CBAllB = self.get_tex('{}/colombageWallAllBorders.png'.format(path))
        _CBF = self.get_tex('{}/colombageWallFULL.png'.format(path))
        _Window = self.get_tex('{}/Window.png'.format(path))
        _DoorUp = self.get_tex('{}/DoorUpB.png'.format(path))
        _DoorDown = self.get_tex('{}/DoorDownB.png'.format(path))
        """
        # NOT USED
        _CBRU = self.get_tex('{}/colombageWallRight_up.png'.format(path))
        _CBLU = self.get_tex('{}/colombageWallLeft_up.png'.format(path))
        _CBU = self.get_tex('{}/colombageWallUp.png'.format(path))
        _CBLD = self.get_tex('{}/colombageWallLeftDown.png'.format(path))
        _CBRD = self.get_tex('{}/colombageWallRightDown.png'.format(path))
        _CBD = self.get_tex('{}/colombageWallDown.png'.format(path))
        _CBMU = self.get_tex('{}/colombageWallMiddleUp.png'.format(path))
        """
        self.CBLCFront = [_CBT,_CBL,_CBR,_CBT,_CBT,_CBT]
        self.CBRCFront = [_CBT,_CBR,_CBT,_CBL,_CBT,_CBT]
        self.CBLCBack = [_CBR,_CBT,_CBL,_CBT,_CBT,_CBT]
        self.CBRCBack = [_CBL,_CBT,_CBT,_CBR,_CBT,_CBT]
        self.CBM = [_CBM,_CBM,_CBM,_CBM,_CBT,_CBT]
        self.CBALLBFront = [_CBAllB,_CBF,_CBF,_CBF,_CBF,_CBAllB]
        self.CBALLBRight = [_CBF,_CBF,_CBAllB,_CBF,_CBF,_CBAllB]
        self.CBALLBLeft = [_CBF,_CBF,_CBF,_CBAllB,_CBF,_CBAllB]
        self.CBALLBBack = [_CBF,_CBAllB,_CBF,_CBF,_CBF,_CBAllB]
        self.Window = [_Window,_sW,_sW]
        self.DoorU = [_DoorUp,_sW,_sW]
        self.DoorD = [_DoorDown,_sW,_sW]
        """
        NOT USED
        """
        """
        self.CBNormal = [_CBT,_CBT,_CBT]
        self.CBLCFrontUP = [_CBT,_CBLU,_CBRU,_CBT,_CBT,_CBLD]
        self.CBRCFrontUP = [_CBT,_CBRU,_CBT,_CBLU,_CBT,_CBRD]
        self.CBLCBackUP = [_CBRU,_CBT,_CBLU,_CBT,_CBT,_CBLU]
        self.CBRCBackUP = [_CBLU,_CBT,_CBT,_CBRU,_CBT,_CBRU]
        self.CBFrontUP = [_CBT,_CBU,_CBT,_CBT,_CBT,_CBD]
        self.CBLeftUP = [_CBT,_CBT,_CBU,_CBT,_CBT,_CBL]
        self.CBRightUP = [_CBT,_CBT,_CBT,_CBU,_CBT,_CBR]
        self.CBBackUP = [_CBU,_CBT,_CBT,_CBT,_CBT,_CBU]
        """

        self.batch = pyglet.graphics.Batch()

        """
        la maison à colombage
        """
        # fondations en briques
        L=18
        l=18
        XC=25
        YC=25
        z=0
        H=4
        """
        La porte est toujours sur la face de devant
        YD = position y de la porte
        """
        YD=YC+L//2-1

        self.add_block(YD,z+1,XC,self.DoorU)
        self.add_block(YD+1,z+1,XC,self.DoorU)

        for y in range(YC    , YC+L  , 1):
            if y not in [YD,YD+1]:
                self.add_block(y       , z, XC  , self.brick)
            else:
                self.add_block(y       , z, XC  ,self.DoorD)

        for x in range(XC-1  , XC-1-l,-1):
            self.add_block(YC+L-1  , z, x   , self.brick)

        for y in range(YC-2+L, YC-2  ,-1):
            self.add_block(y       , z, XC-l, self.brick)

        for x in range(XC+1-l, XC+1  , 1):
            self.add_block(YC-1    , z, x   , self.brick)

        # rajouter le nombre de fenêtres comme dernière variable
        self.colombageFloor(XC  , YC  , z+1   , H, L  , l, nbw=[1,3,2,5])
        """
        dec vaut soit 0 soit 1
        si dec vaut 1, l'étage du dessus est plus grand que l'étage du dessus
        """
        dec=1
        self.colombageFloor(XC+dec, YC-dec, z+1+H , H, L+2*dec, l+2*dec)
        self.colombageFloor(XC+dec, YC-dec, z+1+2*H , H, L+2*dec, l+2*dec, nbw=[3,8,2,23])

        # (y,z,x) ??
        htu=50
        for y in range(-htu,htu,1):
            for x in range(-htu,htu,1):
                ground=random.choice([self.dirt, self.grass, self.grass, self.grass, self.grass, self.grass, self.grass, self.grass])
                self.add_block(y, -1, x, ground)

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
        #print(self.pos, self.rot)

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
