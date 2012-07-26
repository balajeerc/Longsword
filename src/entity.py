import os
import json

import pyglet
import cocos

class Entity():
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
				self.animations[animationName] = animation
			
			self.sprite = cocos.sprite.Sprite(self.animations[self.animations.keys()[0]])
		else:
			self.sprite = cocos.sprite.Sprite(self.image)	
				
		self.colliderExts = entityData["colliderExts"][0],entityData["colliderExts"][1]		
		self.sprite.schedule_interval(self.update,0.5)
		self.sprite.position = 320,240 
		
	def playAnimation(self, animationName):
		"""Plays a particular animation sequence
		
		Keyword arguments:
		animationName -- name of the animation being played
		
		"""
		pass
	
	def isAnimationPlaying(self, animationName=None):
		"""Checks if a particular animation is playing. Returns boolean indicating same.
		If no animationName has been specified, it returns a boolean indicating if any
		animation defined for this sprite is in progress.
		
		Keyword arguments:
		animationName -- name of the animation to check for
		
		"""
		pass
	
	def stopAnimation(self):
		"""Stops the animation currently in progress"""
		pass
	
	def onCollision(self):
		"""Handles collisions with other entities"""
		pass
	
	def register(self, gameLayer):
		"""Registers this entity with the specified layer"""
		gameLayer.add(self.sprite,z=1)
		
	def update(self, timeSinceLastUpdate, *args, **kwargs):
		#print("Callback occurred at: " + str(timeSinceLastUpdate))
		pass