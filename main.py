#
# cocos2d
# http://cocos2d.org
#
# This code is so you can run the samples without installing the package
import sys
import os
import pyglet
import src.entity as entity
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import cocos

# A color layer  is a Layer with the a color attribute
class MainCanvas(cocos.layer.ColorLayer):
    def __init__(self):
        # blueish color
        super(MainCanvas,self).__init__( 0,0,0,255)
        # similar to cocos.text.Label, a cocos.sprite.Sprite
        # is a subclass of pyglet.sprite.Sprite with the befits of
        # being a CocosNode
#        plyrImage = pyglet.resource.image('professor.png')
#        animationImageGrid = pyglet.image.ImageGrid(plyrImage, 4, 9) 
#        self.animationSequences = []
#        self.animationSequences.append(pyglet.image.Animation.from_image_sequence(animationImageGrid[0:8], 0.1, loop=False))
#        self.animationSequences.append(pyglet.image.Animation.from_image_sequence(animationImageGrid[9:17], 0.1, loop=False))
#        self.animationSequences.append(pyglet.image.Animation.from_image_sequence(animationImageGrid[18:26], 0.1, loop=False))        
#        self.animIndex = 0
#        self.spriteInst = cocos.sprite.Sprite(self.animationSequences[self.animIndex])
#        self.spriteInst.on_animation_end = self.registerAnimEnd        
#        # sprite in the center of the screen (default is 0,0)
#        self.spriteInst.position = 320,240        
#        self.add(self.spriteInst,z=1)
                        
def InitResources():
    resource_path_list = []
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    assetDirectory = os.path.join(currentDirectory,'assets')
    #convert function
    for rootFolder, subFolders, files in os.walk(assetDirectory):
        resource_path_list.append(rootFolder[rootFolder.find("assets"):])
    pyglet.resource.path = resource_path_list
    pyglet.resource.reindex()
            
if __name__ == "__main__":    

    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    InitResources()
    
    # We create a new layer, an instance of MainCanvas
    main_layer = MainCanvas()

    newEntity = entity.Entity()
    newEntity.load("/Users/balajeerc/Projects/Longsword/assets/player")
    newEntity.register(main_layer)
        
    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene (main_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)
    
