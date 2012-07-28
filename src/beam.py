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

import pyglet
import cocos

import entity
import debug

class Beam(entity.Entity):
    """Player's beam for Longsword"""

    def __init__(self):
        super(Beam,self).__init__()
        self.load("assets/beam")
#        self.beamTiledImage = pyglet.image.TileableTexture.create_for_image(self.image)
##        self.beamTiledImage.blit_tiled(0.0, 0.0, 0.0, 300, 12)
#        self.beamTiledImage = pyglet.image.Texture.create(128, 32)
#        self.beamTiledImage.blit_into(self.image, 0, 0, 1)
#        self.beamTiledImage.blit_into(self.image, 33, 0, 1)
#        self.beamTiledImage.blit_into(self.image, 65, 0, 1)                
#        self.sprite = cocos.sprite.Sprite(self.beamTiledImage)    
#        self.sprite.position = 320,180    