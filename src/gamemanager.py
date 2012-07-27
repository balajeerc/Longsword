#    Copyright 2012 Balajee.R.C
#    
#    This file is part of Longsword
#    
#    Longsword is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    Longsword is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with Longsword.  If not, see <http://www.gnu.org/licenses/>.

import os

import pyglet
import cocos

import entity
import player

class GameManager():
    """Game manager for Longsword. Entry point of all game synchronisation"""
    
    singletonInstance = None #Instance of game manager
    
    def __init__(self):
        #Initialise the cocos system
        cocos.director.director.init()
        #Create the layer into which we'll be adding our sprites
        self.mainLayer = cocos.layer.ColorLayer(0,0,0,255)
        #Make sure that this layer receives input events
        self.mainLayer.is_event_handler = True
        #Create the main scene
        self.mainScene = cocos.scene.Scene(self.mainLayer)
        #Initialise resource paths
        self.initResources()
        GameManager.singletonInstance = self
        
    @classmethod
    def getInstance(cls):
        return GameManager.singletonInstance
        
    def initResources(self):
        """Initialises resource paths"""
        #Pyglet requires that all resources used must be from registered
        #resource paths. We make a list of all directories (and their subdirectories
        #and so forth, recursively) in the assets folder and add them to the
        #pyglet resource paths
        resource_path_list = []
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        rootDirectory = os.path.dirname(currentDirectory)
        assetDirectory = os.path.join(rootDirectory,'assets')
        #Pyglet does not recursively search sub-directories, so we walk the hierarchy
        for rootFolder, subFolders, files in os.walk(assetDirectory):
            resource_path_list.append(rootFolder[rootFolder.find("assets"):])
        #Register the list of paths found
        pyglet.resource.path = resource_path_list
        pyglet.resource.reindex()
        
    def startGame(self):
        """Starts running the game"""
        self.player = player.Player()
        self.addEntity(self.player)
        self.player.registerEventHandlers(self.mainLayer)
        
        cocos.director.director.run(self.mainScene)
        
    def getMainLayer(self):
        return self.mainLayer    
    
    def addEntity(self,entity,layer=None):
        if layer:
            entity.register(layer)
        else:
            entity.register(self.mainLayer)          
