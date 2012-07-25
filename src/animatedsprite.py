import cocos

class AnimatedSprite():
	"""An animated sprite"""
	
	def __init__(self):
		pass
		
	def load(self, path):
		"""Loads a sprite animation from specified directory path. 
		
		The directory path must contain both the image file containing
		the sprite sheet itself and the XML file containing information about
		animation sequences
		
		Keyword arguments:
		path -- path to directory containing sprite data (sprite sheet and XML)
		
		"""
		pass
	
	def setFrameRate(self, frameRate):
		"""Sets the frame rate for the animation sequences in this sheet
		
		Keyword arguments:
		frameRate -- rate at which animation should play, in frames per second
		
		"""
		pass
	
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
	
	
		
	