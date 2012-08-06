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
import random

import pyglet
import cocos
from cocos import collision_model

import entity
import player
import npc

#from cocos import tiles
#from cocos.director import director
#from cocos.scene import Scene

class GameManager():
    """Game manager for Longsword. Entry point of all game synchronisation"""
    
    singletonInstance = None #Instance of game manager
    
    def __init__(self):
        #Initialise the cocos system
        cocos.director.director.init(width=720, height=512, do_not_scale=True)
        #Create the layer into which we'll be adding our sprites
        #self.mainLayer = cocos.layer.ColorLayer(0,0,0,255)
        #self.mainLayer = tiled2cocos.load_map('assets/maps/level1.tmx')
        #Create a scrolling map manager
        self.scrollingManager = cocos.tiles.ScrollingManager()
        #Load map resource from tmx file
        resource = cocos.tiles.load_tmx('radsLevel.tmx')
        #Load each layer
        layerNames = ["grass","horizongrass","cobblestones","vegetation","fences","shrubs","forest","sea","forest1","forest2","coast","details","stall"]
        self.bgLayers = []
        for layerName in layerNames:
            layer = resource.get_resource(layerName)
            self.bgLayers.append(layer)
            self.scrollingManager.add(layer)
        self.mainLayer = resource.get_resource("main")
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
        self.fonts = {}
        #Initialise resource paths
        self.initResources()
        GameManager.singletonInstance = self
        
        self.humans = ["agent","baldric","duke","fbi","mage","rivera","soldiernormal","soldierzombie"]
        self.aliens = ["blackrobo", "devilman", "mech1", "mech2", "skeleton", "whiterobo"]
        self.characterTypes = ["humans","aliens"]
        self.npcs = [self.humans, self.aliens]
        self.npcRatio = 0.5
        self.lastSpawnAt = 0.0
        self.timer = 0.0
        
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
        
        #Here we also load the fonts
        pyglet.font.add_file('assets/fonts/outtt.ttf')
        self.fonts["outlandish"] = pyglet.font.load('Outlands Truetype', bold=True)
        self.oneSpawn = False

    def startGame(self):
        """Starts running the game"""
        self.debugText = cocos.text.RichLabel(text="Logging",
                                              position=(300,10),
                                              font_size=12,
                                              font_name='Arial',
                                              color=(0,0,0,255))     
        self.mainLayer.add(self.debugText)
        
        self.player = player.Player()        
        self.addEntity(self.player)
        self.player.registerEventHandlers(self.mainLayer)
        
        npchar = npc.NPC("baldric","humans",cocos.euclid.Vector2(100.0,100.0))
        self.addEntity(npchar, self.mainLayer)        
        self.text = cocos.text.RichLabel(text='Kill aliens without hurting humans!',
                                         position=(100,200),
                                         font_size=24,
                                         font_name='Outlands Truetype',
                                         color=(0,0,0,255))
        self.textTimer = 0.0
        
        self.mainLayer.add(self.text,z=4)
        cocos.director.director.run(self.mainScene)
                
    def getMainLayer(self):
        return self.mainLayer    
    
    def getScrollingManager(self):
        return self.scrollingManager
    
    def addEntity(self,entity,layer=None):
        entityIndx = len(self.entityList)
        self.entityList.append(entity)
        if layer:
            entity.register(self,layer)
        else:
            entity.register(self,self.mainLayer)
    
    def removeEntity(self,entity):
        self.entityList.remove(entity)
        
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        #We start by clearing the collision manager
        self.timer += timeSinceLastUpdate
        self.collisionManager.clear()
        
        #As required by the Cocos collision API, we now add all the
        #collider entities into it again
        for entity in self.entityList:
            if entity.isCollider:
                self.collisionManager.add(entity)
        #Beam is handled in a special way, using a string of circular subcolliders
        #along its length. 
        self.player.beam.addToCollisionManager(self.collisionManager)
                
        #Handle all collisions between entities
        for firstObject, secondObject in self.collisionManager.iter_all_collisions():
            if firstObject.isCollider:
                firstObject.notifyCollision(secondObject)
            elif firstObject.beamSubCollider:
                self.player.beam.notifyCollision(secondObject)            
            if secondObject.isCollider:
                secondObject.notifyCollision(firstObject)
            elif secondObject.beamSubCollider:    
                self.player.beam.notifyCollision(firstObject)
                        
        #Now we update the game logic for the entities        
        for entity in self.entityList:
            entity.update(timeSinceLastUpdate, args, kwargs)
                
        #Finally, we handle the post collision check updates for the
        #entities    
        for entity in self.entityList:
            if hasattr(entity,'isCollider') or hasattr(entity,'isBeam'):
                entity.updateCollision()
        
        self.textTimer += timeSinceLastUpdate
        if self.textTimer > 5.0:
            self.text.visible = False
        
        self.debugText.x = self.player.sprite.x+200
        if self.debugText.x<250:
            self.debugText.x = 250
            
        #Spawn npc
        if (self.timer-self.lastSpawnAt)>2.0 and self.oneSpawn==False:
            self.lastSpawnAt = self.timer
            randLoc = cocos.euclid.Vector2(0.0,0.0)
            randLoc.x = self.player.currentFocus.x + 50
            randLoc.y = random.randint(30,348)
            charTypeId = random.randint(0,1)
            charType = self.characterTypes[charTypeId]
            entityNameIndx = random.randint(0,len(self.npcs[charTypeId])-1)
            entityName = self.npcs[charTypeId][entityNameIndx]
            print("Spawning " + charType + " entity named " + entityName)
            npchar = npc.NPC(entityName,charType,randLoc)            
            self.addEntity(npchar, self.mainLayer)