import sys

import pyglet
import cocos

class GameManager():

    def __init__(self):
        #Initialise the cocos system
        cocos.director.director.init(width=720,
                                    height=512,
                                    do_not_scale=True,
                                    audio_backend='sdl')
        
        #Create a scrolling map manager
        self.scrollingManager = cocos.tiles.ScrollingManager()
        
        #Load map from tmx file
        resource = cocos.tiles.load_tmx('gameLevel.tmx')
        #Load each layer
        layerNames = ["grass","horizongrass","cobblestones",
                      "vegetation","fences","shrubs","forest",
                      "sea","forest1","forest2","coast","details","stall"]
        self.bgLayers = []
        for layerName in layerNames:
            layer = resource.get_resource(layerName)
            self.bgLayers.append(layer)
            self.scrollingManager.add(layer)
        self.mainLayer = resource.get_resource("main")
        self.scrollingManager.add(self.mainLayer)
        
        self.mainScene = cocos.scene.Scene(self.scrollingManager)

    def startGame(self):
        cocos.director.director.run(self.mainScene)        
            
if __name__ == "__main__":
    gameManager = GameManager()
    gameManager.startGame()