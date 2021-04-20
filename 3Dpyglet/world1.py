from simple import *

window = Window(width=800, height=600, caption='architecture',resizable=True)

glClearColor(0.5,0.7,1,1)

glEnable(GL_DEPTH_TEST)

#glEnable(GL_CULL_FACE)

"""
simulation d'une plantation de sapin
"""
window.pays.spruce_tree(35,85,0,10)
window.pays.spruce_tree(35,35,0,12)

"""
z : altitude du chateau
dct : distance entre les centres de 2 tours alignées suivant x ou y
htt : half taille tower
htower : hauteur tower
ep=epaisseur murs
"""
dct=40
htt=5
htower=15
ep=3
window.pays.castle(-40,-30,0,dct,htt,htower,ep)

pyglet.app.run()
