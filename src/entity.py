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
	"""An entity in Longsword"""
	
	def __init__(self, replicateFrom=None):
		self.sprite = None	#sprite used to visually depict this entity
		self.image = None #pyglet image object used to represent this entity
		self.imageGrid = None #a grid containing this entity's animation frames
		self.animations = {} #animations defined for this entity, referenced against names
		self.entityName = "" #name of the entity type
		self.defaultFrame = 0 #default frame of this entity animation
		self.isAnimated = False #Indicates if this entity is animated
		self.colliderExts = [0.0,0.0] #extents of this entity's collider
		self.currentAnimation = None #Animation currently in progress
		self.zval = 1 #Z value in layer being added to
		self.life = 1000.0
		self.isCollider = False
		self.cshape = None
		self.collidingEntities = []
		
	def load(self, path):
		"""Loads a sprite animation from specified directory path. 
		
		The directory path must contain both the image file containing
		the sprite sheet itself and the XML file containing information about
		animation sequences
		
		Keyword arguments:
		path -- path to directory containing sprite data (sprite sheet and XML)
		
		"""
		descriptorFileName = None		
		for filename in os.listdir(path):			
			if os.path.splitext(filename)[1] == ".json":
				descriptorFileName = filename
				self.entityName = os.path.splitext(filename)[0]
				break
		
		if not descriptorFileName:			
			raise Exception("Cannot find descriptor JSON file at specified path!")
		
		filepath = os.path.join(path,descriptorFileName)
		with open(filepath) as file:
			entityData = json.load(file)	
		
		#First load the image
		self.image = pyglet.resource.image(entityData["image"])
		self.isAnimated = entityData["isAnimated"]
		if self.isAnimated:
			self.imageGrid = pyglet.image.ImageGrid(self.image,
													entityData["imageGrid"]["rows"],
													entityData["imageGrid"]["columns"])		
			defaultTimePerFrame = entityData["imageGrid"]["timePerFrame"]
			for animationName in entityData["animations"]:
				sequence = entityData["animations"][animationName]
				frameSequence = self.imageGrid[sequence["startFrame"]:sequence["endFrame"]]
				timePerFrame = 1.0
				if "timePerFrame" in sequence:
					timePerFrame = sequence["timePerFrame"]
				else:
					timePerFrame = defaultTimePerFrame				
				mustLoop = False
				if "loop" in sequence:
					mustLoop = sequence["loop"]
				animation = pyglet.image.Animation.from_image_sequence(frameSequence,timePerFrame,mustLoop)
				self.animations[animationName] = [animation,mustLoop]
			
			#We also add a still frame that we start the sprite with
			defaultFrameNumber = entityData["defaultFrame"]
			self.defaultFrame = self.imageGrid[defaultFrameNumber]
			
			#Initialise the sprite with the default frame
			self.sprite = cocos.sprite.Sprite(self.defaultFrame)
		else:
			self.sprite = cocos.sprite.Sprite(self.image)	
					
		#self.sprite.schedule_interval(self.update,0.02)
		self.sprite.position = 320,240
		self.sprite.on_animation_end = self.registerAnimationEnd
		
		if entityData["isCollider"]:
			self.isCollider = True		
			self.colliderExts = entityData["colliderExts"][0],entityData["colliderExts"][1]
			self.cshape = collision_model.AARectShape(self.sprite.position,
													 self.sprite.width*0.5,
													 self.sprite.height*0.5)

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
	
	def registerAnimationEnd(self):
		if not self.currentAnimation:
			raise Exception("Received animation end notification though there is no animation playing!" +
								" Something is amiss!")
		#Check if the current animation is a looping animation
		#If so, we must ignore the animation end notification	
		#If not, we register the animation end
		if not self.animations[self.currentAnimation][1]:	
			self.currentAnimation = None
			
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
	
	def onCollision(self):
		"""Handles collisions with other entities"""
		pass
	
	def register(self, gameLayer):
		"""Registers this entity with the specified layer"""
		gameLayer.add(self.sprite,self.zval)
		
	def update(self, timeSinceLastUpdate, *args, **kwargs):
		#print("Callback occurred at: " + str(timeSinceLastUpdate))
		pass
	
	def updateCollision(self):
		"""Updates the colllision shape, after the game logic phase of game update"""
		self.collidingEntities[:] = []
		if self.isCollider:
			self.cshape.center = self.sprite.position
	
	def notifyCollision(self,other):
		"""Updates the collision lists for colliders"""
		if self.isCollider:
			self.collidingEntities.append(other)
		print(self.entityName + " collided with " + other.entityName)	
	
	def translate(self, x, y):
		"""Translates the given entity by specified amount
		
		Keyword arguments:
		x -- displacement along x direction
		y -- displacement along y direction
		
		"""
		self.sprite.x += x
		self.sprite.y += y
		if self.isCollider:
			self.cshape.center = self.sprite.position
		
	def moveTo(self, x, y):
		"""Moves the entity to specified coordinates
		
		Keyword arguments:
		x -- x position of the entitiy
		y -- y position of the entity
		
		"""
		self.sprite.x = x
		self.sprite.y = y		
		if self.isCollider:
			self.cshape.center = self.sprite.position	