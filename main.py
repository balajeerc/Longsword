#
# cocos2d
# http://cocos2d.org
#
# This code is so you can run the samples without installing the package
import sys
import os
import pyglet

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import cocos

# A color layer  is a Layer with the a color attribute
class MainCanvas(cocos.layer.ColorLayer):
    def __init__(self):
        self.initResources()        
        # blueish color
        super(MainCanvas,self).__init__( 0,0,0,255)
        # similar to cocos.text.Label, a cocos.sprite.Sprite
        # is a subclass of pyglet.sprite.Sprite with the befits of
        # being a CocosNode
        plyrImage = pyglet.resource.image('professor.png')
        animationSequence = pyglet.image.ImageGrid(plyrImage, 4, 9) 
        sprite_anim = cocos.sprite.Sprite(pyglet.image.Animation.from_image_sequence(animationSequence, 0.1)) 
        # sprite in the center of the screen (default is 0,0)
        sprite_anim.position = 320,240        
        self.add(sprite_anim,z=1)
                
    def initResources(self):
        resource_path_list = []
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        assetDirectory = os.path.join(currentDirectory,'assets')
        print("Asset directory: " + assetDirectory)
        #convert function
        for rootFolder, subFolders, files in os.walk(assetDirectory):
            resource_path_list.append(rootFolder[rootFolder.find("assets"):])
            print(rootFolder[rootFolder.find("assets"):])
        pyglet.resource.path = resource_path_list
        pyglet.resource.reindex()
        
if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    # We create a new layer, an instance of MainCanvas
    main_layer = MainCanvas()
    
    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene (main_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)