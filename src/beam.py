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
        self.zval = 2 #To make sure that the beam is in front of player
        self.load("assets/beam")
        self.sprite.transform_anchor_x -= self.sprite.get_rect().width*0.5
        #We need to compose the beam     