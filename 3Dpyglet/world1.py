from simple import *

window = Window(width=800, height=600, caption='architecture',resizable=True)

glClearColor(0.5,0.7,1,1)

glEnable(GL_DEPTH_TEST)

#glEnable(GL_CULL_FACE)



"""
simulation d'une plantation de sapin
"""
window.pays.spruce_tree(0,0,0,10)
window.pays.spruce_tree(35,35,0,12)

"""
z : altitude du chateau
htc : half taille chateau
htt : half taille tower
htower : hauteur tower
l=longueur murs
ep=epaisseur murs
"""
z=0
htc=20
htt=5
htower=15
l=2*(htc-htt)
ep=3
window.pays.castle(z,htc,htt,htower,l,ep)

pyglet.app.run()
