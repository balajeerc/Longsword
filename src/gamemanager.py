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
from cocos import collision_model

import tiled2cocos

import entity
import player

#from cocos import tiles
#from cocos.director import director
#from cocos.scene import Scene

class GameManager():
    """Game manager for Longsword. Entry point of all game synchronisation"""
    
    singletonInstance = None #Instance of game manager
    
    def __init__(self):
        #Initialise the cocos system
        cocos.director.director.init(width=640, height=480)
        #Create the layer into which we'll be adding our sprites
        #self.mainLayer = cocos.layer.ColorLayer(0,0,0,255)
        self.mainLayer = tiled2cocos.load_map('assets/maps/level1.tmx')
        #Create a scrolling map manager
        self.scrollingManager = cocos.tiles.ScrollingManager()
        self.scrollingManager.add(self.mainLayer)
        #Make sure that this layer receives input events
        self.mainLayer.is_event_handler = True
        #Create the main scene
        self.mainScene = cocos.scene.Scene(self.scrollingManager)
        #Create a list to store all entities in scene
        self.entityList = []
        #Create a collision manager to respond to collisions
        self.collisionManager = cocos.collision_model.CollisionManagerGrid(0, 1200, 0, 480, 128, 128)
        #Schedule updates at 16 fps on this manager
        self.mainLayer.schedule(self.update)
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
        self.debugText = cocos.text.Label("", x=10, y=10,multiline=True)        
        self.mainLayer.add(self.debugText)
        
        self.player = player.Player()        
        self.addEntity(self.player)
        self.player.registerEventHandlers(self.mainLayer)
        
        #Test collision with black robot
        blackRobo = entity.Entity()
        blackRobo.load('assets/aliens/blackRobo')
        blackRobo.moveTo(640, 320)
        self.addEntity(blackRobo, self.mainLayer)

        cocos.director.director.run(self.mainScene)
                
    def getMainLayer(self):
        return self.mainLayer    
    
    def getScrollingManager(self):
        return self.scrollingManager
    
    def addEntity(self,entity,layer=None):
        self.entityList.append(entity)
        if layer:
            entity.register(layer)
        else:
            entity.register(self.mainLayer)
            
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        #We start by clearing the collision manager
        self.collisionManager.clear()
        #As required by the Cocos collision API, we now add all the
        #collider entities into it again
        for entity in self.entityList:
            if entity.isCollider:
                self.collisionManager.add(entity)
        #Handle all collisions between entities
        for entity, otherObject in self.collisionManager.iter_all_collisions():
            entity.notifyCollision(otherObject)
        #Now we update the game logic for the entities        
        for entity in self.entityList:
            if entity.isCollider:
                entity.update(timeSinceLastUpdate, args, kwargs)
        #Finally, we handle the post collision check updates for the
        #entities    
        for entity in self.entityList:
            if entity.isCollider:
                entity.updateCollision()
            