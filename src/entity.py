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
import json

import pyglet
import cocos
from cocos import collision_model

class Entity(object):
    """An entity in Longsword
    
    Entities represent the base class of all game objects
    in Longsword. It has facilities to load the entity's 
    sprite with animations from a descriptor json file as
    well as sets up collision detection for it. Another vital
    function this class serves is to clone entities without
    creating multiple copies of them. Cloning does not have to
    be handled separately. The first time load is called, it loads
    the entity and creates the necessary data structures. The second
    time onwards, it just recycles references from the first prototype. 
    """
    
    #Reference to the first instance of this entity type created
    prototypalInstances = {}
    entityIdCounter = 0
    
    def __init__(self, replicateFrom=None,spawnPt=cocos.euclid.Vector2(0,0)):
        self.entityName = None #name of the entity type

        self.sprite = None    #sprite used to visually depict this entity
        self.zval = 6 #Z value in layer being added to
        self.layer = None #The cocos layer that this entity is added to

        self.imageGrids = [] #grids containing this entity's animation frames
        self.isAnimated = False #Indicates if this entity is animated
        self.animations = {} #animations defined for this entity, referenced against names
        self.defaultFrame = 0 #default frame of this entity animation
        self.currentAnimation = None #Animation currently in progress

        self.isCollider = False #Indicates if this entity responds to collisions
        self.colliderExts = [0.0,0.0] #extents of this entity's collider
        self.cshape = None #Collision shape for this entity
        self.collidingEntities = []    #List of entities that collided with this one at a given update
        self.boundLines = [] #List of lines used to debug draw this entity's bounds    
        self.boundsVisible = False #Boolean used to switch on and off the drawing of bounds

        self.gameManager = None #Reference to the game manager
        self.isPrototype = False #Indicates if this entity is the class prototype
        
        self.spawnPt = spawnPt

        self.life = 1000.0 #Life for this entity
        self.isDead = False

        self.entityId = Entity.entityIdCounter
        Entity.entityIdCounter += 1
        
    def load(self, path):
        """Loads a sprite animation from specified directory path. 
        
        The directory path must contain both the image file containing
        the sprite sheet itself and the XML file containing information about
        animation sequences.
        
        Note that this method clones the prototype instance for this class
        if it exists.
        
        Keyword arguments:
        path -- path to directory containing sprite data (sprite sheet and XML)
        
        """
        #First check if there is an instance of this entity among the
        #previously loaded prototypical instances
        if path in Entity.prototypalInstances.keys():
            return self.clone(path)
        
        #If we got here, it means that there is no previously loaded
        #prototype and that we are about to load the prototype for entity
        #located at the specified path. So we register it.
        self.isPrototype = True
        Entity.prototypalInstances[path] = self
        
        descriptorFileName = None        
        for filename in os.listdir(path):            
            if os.path.splitext(filename)[1] == ".json":
                descriptorFileName = filename
                self.entityName = os.path.splitext(filename)[0]
                break
        
        if not descriptorFileName:            
            raise Exception("Cannot find descriptor JSON file at specified path!")
        
        filepath = os.path.join(path,descriptorFileName)
        entityData = None
        with open(filepath) as file:
            entityData = json.load(file)        
        #First load the image
        self.isAnimated = entityData["isAnimated"]
        if self.isAnimated:
            #We start by parsing all the image grids
            #Note that one of the grids must be assigned as the default grid
            #If it isn't specified, we simply take the first grid as the default
            defaultGridIndex = 0
            for indx,grid in enumerate(entityData["imageGrids"]):
                imageGridEntry = {}
                imageGridEntry["image"] = pyglet.resource.image(grid["image"])                
                imageGridEntry["grid"] = pyglet.image.ImageGrid(imageGridEntry["image"],
                                                                grid["rows"],
                                                                grid["columns"])        
                imageGridEntry["timePerFrame"] = grid["timePerFrame"]
                if "default" in imageGridEntry.keys():
                    if imageGridEntry["default"]:
                        defaultGridIndex = indx
                self.imageGrids.append(imageGridEntry)
            
            if len(self.imageGrids)==0:
                raise Exception("No image grids found in " + self.entityName + " entity definition file!")
            
            #Next we parse all the animations
            for animationName in entityData["animations"]:
                animationTrack = entityData["animations"][animationName]
                #If the grid index was is explicitly specified, we just
                #use the first image grid for this animation
                gridIndex = 0
                if "gridIndex" in animationTrack.keys():
                    gridIndex = animationTrack["gridIndex"]
                currImageGrid = self.imageGrids[gridIndex]["grid"]
                gridTimePerFrame = self.imageGrids[gridIndex]["timePerFrame"]             
                #We allow 2 ways of allowing frame number specification 
                #for a particular animation track 
                frameSequence = None
                # a)The animation frame numbers can be manually specified, frame by frame
                if "sequence" in animationTrack:
                    frameSequence = []
                    frameNumberList = animationTrack["sequence"]
                    for frameNumber in frameNumberList:
                        frameSequence.append(currImageGrid[frameNumber])
                # b)The animation start frame and end frame can be specified        
                else:    
                    frameSequence = currImageGrid[animationTrack["startFrame"]:
                                                   animationTrack["endFrame"]]
                
                #We set the time per frame based on what is specified for the
                #image grid corresponding to this animation, as well as any
                #overrides specified in the animation track itself                    
                timePerFrame = 1.0
                if "timePerFrame" in animationTrack:
                    timePerFrame = animationTrack["timePerFrame"]
                else:
                    timePerFrame = gridTimePerFrame
                
                #Handle looping for the animation
                mustLoop = False
                if "loop" in animationTrack:
                    mustLoop = animationTrack["loop"]
                animation = pyglet.image.Animation.from_image_sequence(frameSequence,
                                                                       timePerFrame,
                                                                       mustLoop)
                self.animations[animationName] = [animation,mustLoop]
            
            #We also add a still frame that we start the sprite with
            defaultFrameGridIndex = defaultGridIndex
            if "gridIndex" in entityData["defaultFrame"].keys():
                defaultFrameGridIndex = entityData["defaultFrame"]["gridIndex"]
            defaultFrameNumber = entityData["defaultFrame"]["frame"]
            self.defaultFrame = self.imageGrids[defaultFrameGridIndex]["grid"][defaultFrameNumber]            
            #Initialise the sprite with the default frame
            self.sprite = cocos.sprite.Sprite(self.defaultFrame)
            
        else:
            #Non animated entity
            staticImageGridEntry = {}
            staticImageGridEntry["image"] = pyglet.resource.image(entityData["imageGrids"][0]["image"])
            self.imageGrids.append(staticImageGridEntry)            
            self.sprite = cocos.sprite.Sprite(self.imageGrids[0]["image"])    
                    
        #self.sprite.schedule_interval(self.update,0.02)
        self.sprite.position = self.spawnPt
        self.sprite.on_animation_end = self.registerAnimationEnd
        
        collider = True
        if "isCollider" in entityData:
            collider = entityData["isCollider"] 

        if collider:
            self.isCollider = True        
            self.colliderExts = entityData["colliderExts"][0],entityData["colliderExts"][1]
            self.cshape = collision_model.CircleShape(cocos.euclid.Vector2(self.sprite.position[0],self.sprite.position[1]),
                                                      self.sprite.width*0.25)
            self.boundLines = []
            for i in range(4):
                self.boundLines.append(cocos.draw.Line((0,0),(100,100),(255,255,255,255)))
            self.updateBounds(True)    
            self.showBounds(self.boundsVisible)

    def clone(self, path):
        """Clones the entity from the specified path from a
        a previously loaded instance of the same. 
        NOTE: DO NOT USE THIS METHOD DIRECTLY. ALWAYS USE 'load' FOR CREATING
        ENTITIES. CLONING IS AUTOMATICALLY TAKEN CARE OF.
        
        Keyword arguments:
        path -- path to directory containing sprite data (sprite sheet and XML)
        """
        #Make sure that the prototypical instance of the entity at
        #specified path already exists
        if not path in Entity.prototypalInstances.keys():
            raise Exception("Cannot clone an entity without prototype!")
        
        #print("Cloning instance of entity from path " + path)
        prototype = Entity.prototypalInstances[path]

        self.gameManager = prototype.gameManager
        self.entityName = prototype.entityName

        self.imageGrids = prototype.imageGrids
        self.isAnimated = prototype.isAnimated
        self.animations = prototype.animations
        self.defaultFrame = prototype.defaultFrame

        if self.isAnimated:
            self.sprite = cocos.sprite.Sprite(self.defaultFrame)
        else:
            self.sprite = cocos.sprite.Sprite(self.imageGrids[0]["image"])
            
        self.sprite.position = self.spawnPt
        self.sprite.on_animation_end = self.registerAnimationEnd

        self.isCollider = prototype.isCollider
        self.colliderExts = prototype.colliderExts    
        self.cshape = collision_model.CircleShape(cocos.euclid.Vector2(self.sprite.position[0],
                                                                       self.sprite.position[1]),
                                                  self.sprite.width*0.25)
        self.boundLines = [] #List of lines used to debug draw this entity's bounds    
        for i in range(4):
                self.boundLines.append(cocos.draw.Line((0,0),(100,100),(255,255,255,255)))
        self.updateBounds(True)    
        self.showBounds(self.boundsVisible)
    
    def register(self, gameManager, gameLayer):
        """Registers this entity with the specified layer"""
        gameLayer.add(self.sprite,self.zval)
        if self.isCollider:
            for line in self.boundLines:
                gameLayer.add(line)
        self.layer = gameLayer
        self.gameManager = gameManager
        
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        """Update method repeatedly called on the entity"""
        #print("Callback occurred at: " + str(timeSinceLastUpdate))
        pass

    def registerAnimationEnd(self):
        if not self.currentAnimation:
            raise Exception("Received animation end notification though there is no animation playing!" +
                                " Something is amiss!")
        #Check if the current animation is a looping animation
        #If so, we must ignore the animation end notification    
        #If not, we register the animation end
        if not self.animations[self.currentAnimation][1]:    
            self.currentAnimation = None
            
    def playAnimation(self, animationName):
        """Plays a particular animation sequence
        
        Keyword arguments:
        animationName -- name of the animation being played
        
        """
        if not animationName in self.animations:
            raise Exception("Entity named " + self.entityName + " does not have any animation named " + 
                                animationName + " registered.")
        self.sprite.image = self.animations[animationName][0]
        self.currentAnimation = animationName
                
    def isAnimationPlaying(self, animationName=None):
        """Checks if a particular animation is playing. Returns boolean indicating same.
        If no animationName has been specified, it returns a boolean indicating if any
        animation defined for this sprite is in progress.
        
        Keyword arguments:
        animationName -- name of the animation to check for
        
        """
        if not self.currentAnimation:
            return False
        if not animationName==self.currentAnimation:
            return False
        return True
    
    def stopAnimation(self):
        """Stops the animation currently in progress and goes to the default frame"""
        self.currentAnimation = None
        self.sprite.image = self.defaultFrame
            
    def updateCollision(self):
        """Updates the colllision shape, after the game logic phase of game update"""
        self.collidingEntities[:] = []
        if self.isCollider:
            self.cshape.center = cocos.euclid.Vector2(self.sprite.x,self.sprite.y)
            self.updateBounds()
    
    def notifyCollision(self,other):
        """Updates the collision lists for colliders"""
        if self.isCollider:
            self.collidingEntities.append(other)
    
    def translate(self, x, y):
        """Translates the given entity by specified amount
        
        Keyword arguments:
        x -- displacement along x direction
        y -- displacement along y direction
        
        """
        self.sprite.x += x
        self.sprite.y += y
            
    def moveTo(self, x, y):
        """Moves the entity to specified coordinates
        
        Keyword arguments:
        x -- x position of the entitiy
        y -- y position of the entity
        
        """
        self.sprite.x = x
        self.sprite.y = y        

    def rotateBy(self,angle):
        """Rotates this entity by specified angle
        
        Keyword arguments:
        angle -- angle by which this entity must be rotated
        """
        self.sprite.rotation += angle
            
    def rotateTo(self,angle):
        """Sets the angle of rotation for this sprite
        
        Keyword arguments:
        angle -- angle that this entity's rotation must be set to
        """
        self.sprite.rotation = angle
            
    def showBounds(self,show=True):
        """Shows or hides the bounds of this entity
        
        Keyword arguments:
        show -- boolean indicating whether the bounds must be shown or hidden
        """
        for line in self.boundLines:
            line.visible = show
        self.boundsVisible = show    
    
    def updateBounds(self, forceUpdate=False):
        """Updates the lines used to debug draw the bounds of this entity"""        
        #If the bounds are not visible, we dont bother updating
        #the coordinates
        if not self.boundsVisible or not forceUpdate:
            return
        minmax = self.cshape.minmax()
        minx = minmax[0]
        maxx = minmax[1]
        miny = minmax[2]
        maxy = minmax[3]        
        verts = []
        verts.append(cocos.euclid.Vector2(minx,miny))
        verts.append(cocos.euclid.Vector2(maxx,miny))
        verts.append(cocos.euclid.Vector2(maxx,maxy))
        verts.append(cocos.euclid.Vector2(minx,maxy))
        self.boundLines[0].start = verts[0]
        self.boundLines[0].end = verts[1]        
        self.boundLines[1].start = verts[1]
        self.boundLines[1].end = verts[2]
        self.boundLines[2].start = verts[2]
        self.boundLines[2].end = verts[3]        
        self.boundLines[3].start = verts[3]
        self.boundLines[3].end = verts[0]
        color = (255,255,255,255)
        if len(self.collidingEntities)>0:
            color = cocos.euclid.Vector4(255,0,0,255)
        for line in self.boundLines:
            line.color = color
    
    def destroy(self):
        """Removes this entity"""
        if not self.sprite:
            raise Exception("Unable to find sprite of the entity named " + self.entityName)        
        #Attempting to remove sprite from layer
        #print("Removing entity with id:" + str(self.entityId) + " with name " + self.entityName)

        self.layer.remove(self.sprite)
        #As long as this object is not a protypal instance
        #we can delete the sprite and cshape objects
        if not self.isPrototype:
            self.sprite = None
            self.cshape = None
        #print("Finished removing entity with id" + str(self.entityId))    