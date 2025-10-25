### This file will contain different classes and variables related to the sprites used in the game

## Imports
import pygame # our game-centeric Python module and GUI class for dealing with visual elements.
from config import * # configuration file with all out settings and constants.
import math # used to calculate things like floors and cielings.
import random # used to create randomized enemy path roaming
import time # used to capture time to control flow of various events.
from typing import List, Tuple, Dict, Optional # used for more efficient type hinting
from collections import deque # used to import deque, which we will use for our BFS and path finding.

## Global variables
# Represents a coordinate on the grid (x_index, y_index)
GridNode = Tuple[int, int]

#This class represent all spritesheets of the game and the different associated methods of getting and cutting them from their image files
class Spritesheet:
    """
    Represents all spritesheets of the game and provides methods for cutting 
    sprites from their image files, handling transparency.
    """
    def __init__(self, file):
        """
        Loads the spritesheet image file and converts it to a format that
        supports per-pixel transparency (alpha channel).

        Arguments:
            file (str): The file path to the spritesheet image.
        """
        self.sheet = pygame.image.load(file).convert_alpha() # Get the img file

    # create a cutout from the sprites image
    def get_sprite(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """
        Creates a cutout (sub-surface) from the spritesheet image.

        Arguments:
            x (int): The starting X-coordinate for the cutout.
            y (int): The starting Y-coordinate for the cutout.
            width (int): The width of the sprite to cut out.
            height (int): The height of the sprite to cut out.

        Returns:
            pygame.Surface: A new Surface containing only the requested sprite image.
        """
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        return sprite
#This class represent the player's sprite, and how they are updated throughout gameplay
class Player(pygame.sprite.Sprite):
    """
    Represents the player's sprite, managing state, movement, statistics (HP/Mana), 
    collision, and animations throughout gameplay.
    """
    def __init__(self, game: 'Game', x: int, y: int):
        """
        Initializes the player sprite with game context and starting position.

        Arguments:
            game (Game): Reference to the main Game object.
            x (int): Starting X-coordinate (grid index).
            y (int): Starting Y-coordinate (grid index).
        """
        self.game = game
        self._layer = PLAYER_LAYER # Control which layer on the screen the sprite is on
        self.groups = self.game.all_sprites, self.game.players # Add sprite to these groups
        pygame.sprite.Sprite.__init__(self,self.groups)

        # Sprite sizing relative to game's tile size
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # x/y change to record changes in coordinates upon moving. Added to the x/y variables upon update.
        self.x_change = 0
        self.y_change = 0
        # controls the direction the sprite is facing after moving via movement(). Defaults to downward.
        self.facing = 'down'
        # controls the upcoming loop position of the sprite.
        self.animation_loop = 1
        self.death_loop = 1
        # The visual elements of the sprite itself: height, width, img used, etc.
        self.image = pygame.transform.scale(self.game.character_spritesheet.get_sprite(19, 20, 20, 26), (20*CHARACTER_SCALE, 26*CHARACTER_SCALE))
        # Sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.original_rect = self.rect
        self.original_center = self.rect.center
        self.rect.x = self.rect.x
        self.rect.y = self.rect.x
        self.is_moving = False
        # Health
        self.health = PLAYER_HP
        self.max_health = PLAYER_HP
        # Mana
        self.mana = PLAYER_MAX_MANA
        self.max_mana = PLAYER_MAX_MANA
        # Invincibility frames
        self.invincible = False
        self.invincible_timer = 0
        self.flicker_timer = 0
        self.is_shielded = False
        # Teleportation
        self.teleporting = False
        self.teleport_timer = 0
        self.teleport_timer_start = 0
        self.invulnerable = False
        self.teleport_target_x = 0
        self.teleport_target_y = 0
        self.speed = PLAYER_SPEED
        # Injury
        self.is_hurt = False
        self.is_dead = False
        self.is_attacking = False
        self.death_animation_finished = False
        # Presistant stages settings and win conditions
        self.all_open = False # unlocked all switches in current stage
        self.all_clear = False # cleared all stages
        self.stages_locked = [False, True, True, True, True] # Portal 1, portal 2, etc.
        self.current_stage = 0 # 0:tower, 1: stage 1, etc.
        self.stage_changed = False
        self.last_miasma_damage = pygame.time.get_ticks()

        # Create lists of each animation, get and store its associated sprites within
        # Walking
        '''self.down_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(19, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(84, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(148, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(212, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(277, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(342, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(406, 21, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                ]

        self.up_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 212, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 212, self.width, self.height),(PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(282, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(346, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(410, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                              ]

        self.left_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(22, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(87, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(151, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(214, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(278, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(343, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(407, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))                              
                                ]

        self.right_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(281, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(345, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(409, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))]'''
        
        self.down_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(19, 20, 20, 26), (20*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(84, 20, 19, 24), (19*CHARACTER_SCALE, 24*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(148, 18, 19, 25), (19*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(212, 18, 19, 26), (19*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(277, 20, 19, 24), (19*CHARACTER_SCALE, 24*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(342, 18, 18, 25), (18*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(406, 21, 17, 25), (17*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                ]

        self.up_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 212, 20, 25), (20*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 212, 18, 25),(18*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 210, 19, 26), (19*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 210, 19, 27), (19*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(282, 211, 19, 26), (19*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(346, 210, 19, 26), (19*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(410, 211, 18, 26), (18*CHARACTER_SCALE, 26*CHARACTER_SCALE))
                              ]

        self.left_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(22, 83, 17, 25), (17*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(87, 83, 16, 25), (16*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(151, 81, 16, 27), (16*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(214, 81, 17, 27), (17*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(278, 82, 17, 26), (17*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(343, 82, 16, 26), (16*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(407, 81, 16, 27), (16*CHARACTER_SCALE, 27*CHARACTER_SCALE))                              
                                ]

        self.right_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 147, 16, 25), (16*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 147, 16, 27), (16*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 145, 16, 28), (16*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 145, 17, 27), (17*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(281, 146, 17, 27), (17*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(345, 146, 16, 28), (16*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(409, 145, 16, 28), (16*CHARACTER_SCALE, 28*CHARACTER_SCALE))]
        
        # Damaged/Injured
        self.dmg_down_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(19, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(84, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(148, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(212, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(277, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(342, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(406, 21, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                                ]

        self.dmg_up_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 212, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 212, self.width, self.height),(PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(282, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(346, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                              pygame.transform.scale(self.game.character_spritesheet.get_sprite(410, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                              ]

        self.dmg_left_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(22, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(87, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(151, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(214, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(278, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(343, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_spritesheet.get_sprite(407, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))                              
                                ]

        self.dmg_right_animations = [pygame.transform.scale(self.game.character_spritesheet.get_sprite(25, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(89, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(153, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(217, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(281, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(345, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                 pygame.transform.scale(self.game.character_spritesheet.get_sprite(409, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))]
        
        # Death
        self.death_down_animations = [pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(19, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(84, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(148, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(212, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(277, 20, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(342, 18, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(406, 21, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                                ]

        self.death_up_animations = [pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(25, 212, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(89, 212, self.width, self.height),(PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(153, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(217, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(282, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(346, 210, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(410, 211, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                                ]

        self.death_left_animations = [pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(22, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(87, 83, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(151, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(214, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(278, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(343, 82, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(407, 81, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))                              
                                ]

        self.death_right_animations = [pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(25, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(89, 147, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(153, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(217, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(281, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(345, 146, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE)),
                                pygame.transform.scale(self.game.character_death_spritesheet.get_sprite(409, 145, self.width, self.height), (PLAYER_SCALE, PLAYER_SCALE))
                                ]
        
        # Attack
        self.attack_down_animations = [pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(19, 20, 20, 26), (20*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(80, 20, 24, 24), (24*CHARACTER_SCALE, 24*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(144, 19, 24, 25), (24*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(208, 24, 25, 28), (25*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(273, 21, 34, 31), (34*CHARACTER_SCALE, 31*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(337, 21, 33, 35), (33*CHARACTER_SCALE, 35*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(402, 21, 30, 35), (30*CHARACTER_SCALE, 35*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(473, 21, 15, 26), (15*CHARACTER_SCALE, 26*CHARACTER_SCALE))
                                ]
        
        self.attack_left_animations = [pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(24, 83, 16, 25), (16*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(84, 82, 19, 26), (19*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(153, 81, 17, 27), (17*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(211, 83, 20, 27), (20*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(265, 83, 28, 28), (28*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(329, 80, 29, 32), (29*CHARACTER_SCALE, 32*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(393, 81, 29, 30), (29*CHARACTER_SCALE, 30*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(467, 83, 18, 25), (18*CHARACTER_SCALE, 25*CHARACTER_SCALE))                              
                                ]
        self.attack_right_animations = [pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(25, 147, 16, 25), (16*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(82, 146, 22, 26), (22*CHARACTER_SCALE, 26*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(141, 145, 25, 27), (25*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(207, 147, 28, 28), (28*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(280, 147, 31, 28), (31*CHARACTER_SCALE, 28*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(347, 144, 28, 32), (28*CHARACTER_SCALE, 32*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(411, 145, 28, 30), (28*CHARACTER_SCALE, 30*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(475, 147, 18, 25), (18*CHARACTER_SCALE, 25*CHARACTER_SCALE))
                                ]
        
        self.attack_up_animations = [pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(24, 212, 20, 25), (20*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(88, 212, 22, 24),(22*CHARACTER_SCALE, 24*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(152, 211, 22, 25), (22*CHARACTER_SCALE, 25*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(215, 213, 26, 23), (26*CHARACTER_SCALE, 23*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(269, 209, 34, 27), (34*CHARACTER_SCALE, 27*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(335, 205, 32, 31), (32*CHARACTER_SCALE, 31*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(400, 205, 30, 31), (30*CHARACTER_SCALE, 31*CHARACTER_SCALE)),
                                pygame.transform.scale(self.game.character_attack_spritesheet.get_sprite(471, 213, 15, 23), (15*CHARACTER_SCALE, 23*CHARACTER_SCALE))
                                ]

        
        self.teleport_animations = [
            pygame.transform.scale(self.game.character_teleport_spritesheet.get_sprite(9, 22, 41, 19), (PLAYER_SCALE, PLAYER_SCALE)),
            pygame.transform.scale(self.game.character_teleport_spritesheet.get_sprite(86, 12, 19, 41), (PLAYER_SCALE, PLAYER_SCALE)),
            pygame.transform.scale(self.game.character_teleport_spritesheet.get_sprite(140, 24, 41, 19), (PLAYER_SCALE, PLAYER_SCALE)),
            pygame.transform.scale(self.game.character_teleport_spritesheet.get_sprite(213, 14, 19, 41), (PLAYER_SCALE, PLAYER_SCALE)),
        ]

        self.barrier_animations = [
            pygame.transform.scale(self.game.character_barrier_spritesheet.get_sprite(70, 80, 640, 640), (PLAYER_SCALE, PLAYER_SCALE))
        ]
    
    # Update current player with another player's stats. Used with loading save files.
    def update_player_stats(self, other_player: 'Player'):
        """
        Updates the current player's statistics and persistent game state 
        using data from a previous Player instance (e.g., after dying and restarting).

        Arguments:
            other_player (Player): The Player instance containing the saved stats.
        """
        # x/y change to record changes in coordinates upon moving. Added to the x/y variables upon update.
        self.x_change = 0
        self.y_change = 0
        # controls the direction the sprite is facing after moving via movement(). Defaults to downward.
        self.facing = 'down'
        # controls the upcoming loop position of the sprite.
        self.animation_loop = 1
        # The visual elements of the sprite itself: height, width, img used, etc.
        self.image = self.down_animations[0] 
        # Sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # Health
        self.health = PLAYER_HP
        self.max_health = PLAYER_HP
        # Mana
        self.mana = PLAYER_MAX_MANA
        self.max_mana = PLAYER_MAX_MANA
        # Invincibility frames
        self.invincible = False
        self.invincible_timer = 0
        self.flicker_timer = 0
        # Teleportation
        self.teleporting = False
        self.teleport_timer = 0
        self.teleport_timer_start = 0
        self.invulnerable = False
        self.teleport_target_x = 0
        self.teleport_target_y = 0
        self.speed = PLAYER_SPEED
        # Injury
        self.is_hurt = False
        self.is_dead = False
        self.death_animation_finished = False
        # Presistant stages settings and win conditions
        self.stages_locked = other_player.stages_locked
        self.current_stage = other_player.current_stage
        self.stage_changed = other_player.stage_changed

    # Method for updating the game after an action, e.g. movement or attacking
    def update(self):
        """
        Updates the player's state every frame. Handles teleportation logic, 
        movement, collision checks, invincibility timers, flickering effects,
        and mana regeneration/drain.
        """
        self.is_moving = False
        # Check if we are currently teleporting
        if self.teleporting:
            # Calculate the direction vector for the teleport
            dx = self.teleport_target_x - self.rect.x
            dy = self.teleport_target_y - self.rect.y
            distance = math.sqrt(dx**2 + dy**2)

            # Move a fraction of the distance each frame
            if distance > TELEPORT_SPEED:
                self.x_change = (dx / distance) * TELEPORT_SPEED
                self.y_change = (dy / distance) * TELEPORT_SPEED
            else:
                # End teleport when close enough to the target
                self.x_change = dx
                self.y_change = dy
                # Fix camera on collision
                match self.facing:
                        case 'left':
                            for sprite in self.game.all_sprites:
                                sprite.rect.x += TELEPORT_DISTANCE
                        case 'up':
                            for sprite in self.game.all_sprites:
                                sprite.rect.y += TELEPORT_DISTANCE
                        case 'right':
                            for sprite in self.game.all_sprites:
                                sprite.rect.x -= TELEPORT_DISTANCE
                        case 'down':
                            for sprite in self.game.all_sprites:
                                sprite.rect.y -= TELEPORT_DISTANCE
                self.teleporting = False
                self.invulnerable = False
            self.is_moving = True
        else:
            if not self.is_dead:
                self.is_moving = self.movement() # Call the movement method to capture any coordinate changes.

        self.animate() # Call the animate method to change sprites for animation effect.

        # Handle invincibility timer
        now = pygame.time.get_ticks()
        if self.invincible and now - self.invincible_timer > PLAYER_IFRAME_TIME:
            self.invincible = False
            self.image.set_alpha(255) # If enough time passed, make the sprite fully visible again

        # Reflect any change in coordinates, correct for collision, then reset the change values if player is still alive.
        if not self.is_dead:
            self.rect.x += self.x_change
            self.collide_obstacles('x')
            self.collide_enemy()
            self.rect.y += self.y_change
            self.collide_obstacles('y')
            self.x_change = 0
            self.y_change = 0

        # Induce flicker effect for invincibility frames
        if self.invincible:
            self.flicker_timer += 1
            if self.flicker_timer % 5 == 0:
                self.image.set_alpha(0) # Hide the sprite
            else:
                self.image.set_alpha(255) # Show the sprite
        else:
            self.image.set_alpha(255) # Ensure it's fully visible when not invincible
            self.flicker_timer = 0

        # Become immune to damage during teleport
        if self.teleporting:
            self.invulnerable = True
            self.teleport_timer += 1
            if self.teleport_timer >= TELEPORT_DURATION:
                self.teleporting = False
                self.invulnerable = False
                self.teleport_timer = 0
        else:
            self.invulnerable = False
            self.teleport_timer = 0
        
        # If player is currently shielded, drain their mana
        if self.is_shielded:
            # Drain mana by MANA_DRAIN_RATE points per update, unless mana is empty.
            self.mana = max(0, self.mana - MANA_DRAIN_RATE)
        
        # If player is at rest (not moving)
        if not self.is_moving and not self.is_dead:
            # Heal mana by MANA_HEAL_RATE points per update, unless mana is maxed.
            self.mana = min(self.max_mana, self.mana + MANA_HEAL_RATE)

    # Method for player sprite movement. Returns bool if player is currently moving.
    def movement(self) -> bool:
        """
        Handles player input for movement. Applies world scrolling (by moving 
        all sprites) and updates directional state. Adjusts speed based on 
        Shift key (boost) or terrain (slippery ice).

        Returns:
            bool: True if the player is currently pressing a movement key, False otherwise.
        """
        keys = pygame.key.get_pressed() # Capture keys that have ben pressed so far.
        slip_hits = pygame.sprite.spritecollide(self, self.game.slippery_ice, False)

        # if standing on slippery ice, boost speed
        if slip_hits:
            self.speed = PLAYER_SPEED_SLIDING
        else:
            # Set speed depending on whether Shift is currently pressed
            self.speed = PLAYER_SPEED_BOOSTED if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else PLAYER_SPEED
        
        # Increase/Decrease the x/y coordinates and sprite-facing depending on key pressed: Left, Up, Right, Down.
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += self.speed
            self.x_change -= self.speed
            self.facing = 'left' 
            return True
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += self.speed
            self.y_change -= self.speed
            self.facing = 'up'
            return True
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= self.speed
            self.x_change += self.speed
            self.facing = 'right'
            return True
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= self.speed
            self.y_change += self.speed
            self.facing = 'down'
            return True

        # Player is currently not moving.
        return False

    # Method for player sprite's collision detection w/ obstacle (e.g. block), depending on direction of collision. Returns True if collision occurs.
    def collide_obstacles(self, direction: str) -> bool:
        """
        Checks for player collision with solid objects (Walls, Blocks, Holes, Doors, Geo).
        Corrects player position and world scroll to prevent clipping. Also handles
        miasma damage if not shielded.

        Arguments:
            direction (str): The axis of movement being checked ('x' or 'y').

        Returns:
            bool: True if a collision with a solid obstacle occurred, False otherwise.
        """
        # checks if rectangle of one sprite is colliding with rectangle of another.
        hits_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_door = pygame.sprite.spritecollide(self, self.game.doors, False)
        geos_hits = pygame.sprite.spritecollide(self, self.game.ice_blocks, False)       
        waters_hits = pygame.sprite.spritecollide(self, self.game.waters, False) 
        miasma_hits = pygame.sprite.spritecollide(self, self.game.miasmas, False)
        
        # If player contacts miasma and is not shielded
        if miasma_hits and not self.is_shielded:            
            # Check if one second has passed since the last miasma damage
            now = pygame.time.get_ticks()
            # If more than 1 sec has passed since last dmg, incur damage
            if now - self.last_miasma_damage > 1000:
                self.health -= MIASAMA_DAMAGE
                self.last_miasma_damage = now
                self.game.sfxs['player_hit'].play()
                if self.health <= 0:
                    self.game.sfxs['player_death'].play()
                    self.is_dead = True

        if direction == "x":
                if not self.invulnerable:
                    # If not teleporting, check for holes too
                    hits_block.extend(pygame.sprite.spritecollide(self, self.game.holes, False))

                if hits_block:
                     # An obstacle has been collided with, and hits[0] is that obstacle. 
                     # If sprite is moving right, correct to left (while keeping the camera still)
                    if self.x_change > 0:
                        self.rect.x = hits_block[0].rect.left - self.rect.width
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += self.speed
                    # If sprite is moving left, correct to right
                    if self.x_change < 0:
                        self.rect.x = hits_block[0].rect.right 
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= self.speed
                    return True
                elif waters_hits:
                     # An obstacle has been collided with, and hits[0] is that obstacle. 
                     # If sprite is moving right, correct to left (while keeping the camera still)
                    if self.x_change > 0:
                        self.rect.x = waters_hits[0].rect.left - self.rect.width
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += self.speed
                    # If sprite is moving left, correct to right
                    if self.x_change < 0:
                        self.rect.x = waters_hits[0].rect.right 
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= self.speed
                    return True
                elif hits_door:
                    # A door has been collided with. 
                    if self.all_open:
                        # If it is unlocked on collide, clear the stage (Win!)
                        self.game.stage_clear()
                    else:
                        # Door is locked, treat it like an obstacle.
                        # If sprite is moving right, correct to left (while keeping the camera still)
                        if self.x_change > 0:
                            self.rect.x = hits_door[0].rect.left - self.rect.width
                            for sprite in self.game.all_sprites:
                                sprite.rect.x += self.speed
                        # If sprite is moving left, correct to right
                        if self.x_change < 0:
                            self.rect.x = hits_door[0].rect.right 
                            for sprite in self.game.all_sprites:
                                sprite.rect.x -= self.speed
                    return True
                elif geos_hits:
                    # An obstacle has been collided with, and hits[0] is that obstacle. 
                    # If sprite is moving right, correct to left (while keeping the camera still)
                    if self.x_change > 0:
                        self.rect.x = geos_hits[0].rect.left - self.rect.width
                        for sprite in self.game.all_sprites:
                            sprite.rect.x += self.speed
                    # If sprite is moving left, correct to right
                    if self.x_change < 0:
                        self.rect.x = geos_hits[0].rect.right 
                        for sprite in self.game.all_sprites:
                            sprite.rect.x -= self.speed
                    return True
                else:
                    return False        
        elif direction == "y":
                if not self.invulnerable:
                    # If not teleporting, check for holes too
                    hits_block.extend(pygame.sprite.spritecollide(self, self.game.holes, False))
                if hits_block:
                    # An obstacle has been collided with, and hits[0] is that obstacle
                    # If sprite is moving down, correct to up
                    if self.y_change > 0:
                        self.rect.y = hits_block[0].rect.top - self.rect.height
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += self.speed
                    # If sprite is moving up, correct to down
                    if self.y_change < 0:
                        self.rect.y = hits_block[0].rect.bottom
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= self.speed
                    self.teleporting = False
                    return True
                elif waters_hits:
                     # An obstacle has been collided with, and hits[0] is that obstacle
                    # If sprite is moving down, correct to up
                    if self.y_change > 0:
                        self.rect.y = waters_hits[0].rect.top - self.rect.height
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += self.speed
                    # If sprite is moving up, correct to down
                    if self.y_change < 0:
                        self.rect.y = waters_hits[0].rect.bottom
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= self.speed
                    self.teleporting = False
                    return True
                elif geos_hits:
                    # An ice block has been collided with, and hits[0] is that block
                    # If sprite is moving down, correct to up
                    if self.y_change > 0:
                        self.rect.y = geos_hits[0].rect.top - self.rect.height
                        for sprite in self.game.all_sprites:
                            sprite.rect.y += self.speed
                    # If sprite is moving up, correct to down
                    if self.y_change < 0:
                        self.rect.y = geos_hits[0].rect.bottom
                        for sprite in self.game.all_sprites:
                            sprite.rect.y -= self.speed
                    self.teleporting = False
                    return True
                elif hits_door:
                    # A door has been collided with. 
                    if self.all_open:
                        # If it is unlocked on collide, clear the stage (Win!)
                        self.game.stage_clear()
                    else:
                        # Door is locked, treat it like an obstacle.
                        # If sprite is moving right, correct to left (while keeping the camera still)
                        if self.y_change > 0:
                            self.rect.y = hits_door[0].rect.top - self.rect.height
                            for sprite in self.game.all_sprites:
                                sprite.rect.y += self.speed
                        # If sprite is moving up, correct to down
                        if self.y_change < 0:
                            self.rect.y = hits_door[0].rect.bottom
                            for sprite in self.game.all_sprites:
                                sprite.rect.y -= self.speed
                    return True
                else:
                    return False
        
    # Method for player sprite's collision detection w/ enemies. Returns True if valid enemy collision occurs.
    def collide_enemy(self):
        """
        Checks for player collision with enemies and applies damage, granting 
        invincibility frames (I-frames) upon a hit.

        Returns:
            bool: True if a non-invincible player collides with an enemy, False otherwise.
        """
        # Ignore the collision and don't take damage if invincible or invulnerable (teleporting)
        if self.invincible or self.invulnerable or self.is_shielded:
            return False
        # checks if rectangle of one sprite is colliding with rectangle of another.
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            # An enemy has been collided with while not invincible. Take damage.
            self.health -= ENEMY_COLLISION_DAMAGE
            self.game.sfxs['player_hit'].play()
            # Set invincibility and start the timer
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()
            if self.health <= 0:
                self.game.sfxs['player_death'].play()
                self.is_dead = True
            return True
        return False
    
    # Method for player sprite's animation
    def animate(self):
        """
        Manages the player's visual state based on priority: Death, Teleport, 
        Shield, Attack, Walk, or Idle. Updates the sprite image and animation loop 
        for the current state.
        """
        # Check for death state first, as this should override all other animations
        if self.is_dead:
            if not self.death_animation_finished:
                if self.facing == "down":
                    self.image = self.death_down_animations[math.floor(self.death_loop)]
                    self.death_loop += 0.1
                    if self.death_loop >= len(self.death_down_animations):
                        self.death_loop = 1
                        self.death_animation_finished = True
                        self.image = self.death_down_animations[-1] # Freeze on the last frame
                        self.game.playing = False 
                if self.facing == "up":
                    self.image = self.death_up_animations[math.floor(self.death_loop)]
                    self.death_loop += 0.1
                    if self.animation_loop >= len(self.death_up_animations):
                        self.death_loop = 1
                        self.death_animation_finished = True
                        self.image = self.death_up_animations[-1] # Freeze on the last frame
                        self.game.playing = False         
                if self.facing == "left":
                    self.image = self.death_left_animations[math.floor(self.death_loop)]
                    self.death_loop += 0.1
                    if self.death_loop >= len(self.death_left_animations):
                        self.death_loop = 1
                        self.death_animation_finished = True
                        self.image = self.death_left_animations[-1] # Freeze on the last frame
                        self.game.playing = False 
                if self.facing == "right":
                    self.image = self.death_right_animations[math.floor(self.death_loop)]
                    self.death_loop += 0.1
                    if self.death_loop >= len(self.death_right_animations):
                        self.death_loop = 1
                        self.death_animation_finished = True
                        self.image = self.death_right_animations[-1] # Freeze on the last frame
                        self.game.playing = False 
            # Skip below animations
            return None
        # While player is alive, check everything else.
        else:
            # Check for teleporting state
            if self.teleporting:
                # Play teleport animation, depending on direction player is facing
                if self.facing == "right":
                    self.image = self.teleport_animations[0]
                elif self.facing == "down":
                    self.image = self.teleport_animations[1]
                elif self.facing == "left":
                    self.image = self.teleport_animations[2]
                elif self.facing == "up":
                    self.image = self.teleport_animations[3]    
                # Skip below animations            
                return None
            
            # If currently shielded by barrier, ignore walk animation and convert player sprite to shield sprite.
            if self.is_shielded:
                self.image = self.barrier_animations[0]
                # Skip below animations
                return None
            
            
            # Check for attacks
            if self.is_attacking:
                # Use a list of sprites corresponding to the player's current facing direction
                current_animations = []
                if self.facing == "down": current_animations = self.attack_down_animations 
                elif self.facing == "up": current_animations = self.attack_up_animations
                elif self.facing == "left": current_animations = self.attack_left_animations 
                elif self.facing == "right": current_animations = self.attack_right_animations 
                
                # Advance the animation loop
                self.animation_loop += 0.2
                # Check if the animation loop is finished
                if self.animation_loop >= len(current_animations):
                    self.animation_loop = 1.0 # Reset loop, starting from 1 to align with walk loop logic
                    self.is_attacking = False # End the attack state
                    # Set image to a resting/idle sprite in the direction the player was facing
                    if self.facing == "down": self.image = self.down_animations[0] 
                    # Note: The existing movement function handles the final sprite assignment well enough 
                    # when self.is_attacking becomes False, but we explicitly set a default here just in case.
                else:
                    # Display the current attack frame
                    self.image = current_animations[math.floor(self.animation_loop)]
                    
                return None # Skip Shield/Walk/Idle logic
            
            # Use a movement animation sprites list depending on the direction player sprite is facing while moving: down, up, left, or right.
            # self.animation_loop: using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame), looping at the end of the list to create an animation.
            if self.facing == "down":
                if self.y_change == 0:
                    # If standing still, default to intial, first sprite facing downward
                    self.image = self.down_animations[0] 
                else:
                    # If the y has changed (Player moved down), 
                    self.image = self.down_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 7:
                        self.animation_loop = 1        
            if self.facing == "up":
                if self.y_change == 0:
                    # If standing still, default to intial, first sprite 
                    self.image = self.up_animations[0] 
                else:
                    # If the y has changed (Player moved up), 
                    self.image = self.up_animations[math.floor(self.animation_loop)]
                    # using 0.1 and floor allows us to change the animation every 10 frames
                    self.animation_loop += 0.1
                    if self.animation_loop >= 7:
                        self.animation_loop = 1        
            if self.facing == "left":
                if self.x_change == 0:
                    # If standing still, default to intial, first sprite 
                    self.image = self.left_animations[0] 
                else:
                    # If the x has changed (Player moved left), 
                    self.image = self.left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 7:
                        self.animation_loop = 1
            if self.facing == "right":
                if self.x_change == 0:
                    # If standing still, default to intial, first sprite 
                    self.image = self.right_animations[0] 
                else:
                    # If the x has changed (Player moved up), 
                    self.image = self.right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 7:
                        self.animation_loop = 1

    #  Method to draw the player's health bar
    def draw_health_bar(self):
        """
        Draws the player's health bar (green) and its border (gold) at the 
        top-left corner of the screen.
        """
        # Calculate the health ratio to determine the width of the green health bar
        health_ratio = self.health / self.max_health
        # Health bar dimensions
        bar_width = 150
        bar_height = 20
        # Position of the health bar (top-left corner)
        bar_x = 10
        bar_y = 10
        
        # Border thickness
        border_thickness = 2
        inner_width = bar_width - (border_thickness * 2)
        inner_height = bar_height - (border_thickness * 2)

        # Draw the golden background rectangle
        pygame.draw.rect(self.game.screen, GOLD, (bar_x, bar_y, bar_width, bar_height), border_thickness)
        # Draw the green health bar filling, inset by the border thickness
        pygame.draw.rect(self.game.screen, GREEN, (bar_x + border_thickness, bar_y + border_thickness, inner_width * health_ratio, inner_height))

    # Method to draw the player's mana bar
    def draw_mana_bar(self):
        """
        Draws the player's mana bar (blue) and its border (gold) directly below 
        the health bar.
        """
        # Calculate the mana ratio to determine the width of the blue mana bar
        mana_ratio = self.mana / self.max_mana
        # Mana bar dimensions
        bar_width = 150
        bar_height = 20
        # Position of the mana bar (below the health bar)
        bar_x = 10
        bar_y = 40  # 10 (health bar y) + 20 (height) + 10 (spacing)
        
        # Border thickness
        border_thickness = 2
        inner_width = bar_width - (border_thickness * 2)
        inner_height = bar_height - (border_thickness * 2)

        # Draw the golden background rectangle
        pygame.draw.rect(self.game.screen, GOLD, (bar_x, bar_y, bar_width, bar_height), border_thickness)
        # Draw the blue mana bar filling, inset by the border thickness
        pygame.draw.rect(self.game.screen, BLUE, (bar_x + border_thickness, bar_y + border_thickness, inner_width * mana_ratio, inner_height))

    # Method to teleport the player from one point to another on the map.
    def teleport(self):
        """
        Initiates the player's teleport sequence by setting the invulnerability 
        flags and calculating the target position based on the current facing direction.
        """
        # Make player invulnerable during teleport.
        self.teleporting = True
        self.invulnerable = True
        
        # Determine the target coordinates for the teleport based on current facing direction
        target_x = self.rect.x
        target_y = self.rect.y
        if self.facing == 'up':
            target_y -= TELEPORT_DISTANCE
        elif self.facing == 'down':
            target_y += TELEPORT_DISTANCE
        elif self.facing == 'left':
            target_x -= TELEPORT_DISTANCE
        elif self.facing == 'right':
            target_x += TELEPORT_DISTANCE

        # Set the target coordinates for the update method
        self.teleport_target_x = target_x
        self.teleport_target_y = target_y

# This class represent the various enemy sprites, and how they are updated throughout gameplay
class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy character. Manages movement (patrol/aggro), animations, 
    collision with obstacles, and health.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int, threat_level: int = 1):
        """
        Initializes the Enemy sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): Used to select the correct enemy sprite/animation set.
            threat_level (int): Defines HP and behavior (1=normal, 2=elite).
        """
        self.game = game
        self.stage_type = stage_type
        self.threat_level = threat_level # 1 for simple enemies, 2 for elites. Numbers used for scalability.
        self._layer = ENEMY_LAYER # Control which layer on the screen the sprite is on
        self.groups = self.game.all_sprites, self.game.enemies # Add sprite to the all_sprites and enemies groups
        pygame.sprite.Sprite.__init__(self,self.groups)

        # Sprite sizing relative to game's tile size
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.current_path: List[GridNode] = []
        
        # x/y change to record changes in coordinates upon moving. Added to the x/y variables upon update.
        self.x_change = 0
        self.y_change = 0

        # controls the direction the sprite is facing on load. Defaults to a random direction between left or right.
        self.facing = random.choice(['left', 'right'])
        # controls the upcoming loop position of the sprite (e.g. in a 3-sprites loop, 2 is the third sprite). Defaults to 1 (second sprite).
        self.animation_loop = 1
        # controls the movement loop (the patrolling behaviour) of the enemy.
        self.movement_loop = 0

        # Initialize lists of each animation, get and store its associated sprites within
        self.down_animations = []
        self.up_animations = []
        self.left_animations = []
        self.right_animations = []
        self.animation_loop_max = 0

        # Get Enemy sprite animations
        self.get_animations(self.stage_type)
        self.image = self.down_animations[0]
        self.image.set_colorkey(BLACK)
        # Set sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = ENEMY_SPEED
        # Health variables
        if threat_level >= 2:
            self.health = ELITE_ENEMY_HP
            self.max_health = ELITE_ENEMY_HP
        else:
            self.health = ENEMY_HP
            self.max_health = ENEMY_HP
        self.health_bar_visible = False
        # Invincibility frames
        self.invincible = False
        self.invincible_timer = 0
        self.flicker_timer = 0
        self.last_move_time = time.time()
        # controls enemy travel 
        self.max_travel_pixels = random.randint(7, 30) * TILESIZE  # can travel between between 7 and 30 pixels before returning to starting position
        self.current_direction = random.choice(['up', 'down', 'left', 'right'])
        self.patrol_step_timer = 0
        self.patrol_step_limit = FPS # Change direction in accordance with our framerate.
        # starting positions
        self.start_x = self.rect.x 
        self.start_y = self.rect.y

    # Gets the current pixel the enemy is on and converts it to a grid node.
    def get_current_node(self) -> GridNode:
        """
        Calculates the enemy's current grid position based on its pixel center.

        Returns:
            GridNode: The (x, y) grid coordinates.
        """
        x = self.rect.centerx // TILESIZE
        y = self.rect.centery // TILESIZE
        return (x, y)

    # Gets the current pixel the player is on and converts it to a grid node.
    def get_player_node(self, player_pos: pygame.math.Vector2) -> GridNode:
        """
        Calculates the player's grid position based on their pixel center.

        Arguments:
            player_pos (pygame.math.Vector2): Player's current pixel position.

        Returns:
            GridNode: The (x, y) grid coordinates of the player.
        """
        x = int(player_pos.x // TILESIZE)
        y = int(player_pos.y // TILESIZE)
        return (x, y)

    # Method for updating the game after an action, e.g. movement or attacking
    def update(self):
        """
        Updates the enemy's state, checks I-frames, handles movement selection 
        (aggro vs. patrol), and resolves sprite flicker.
        """
        # Only continue running enemy's update function while player is still alive.
        if not self.game.player.is_dead:
            self.animate() # Call the animate method to change sprites for animation effect.
            # Handle invincibility timer
            now = pygame.time.get_ticks()
            if self.invincible and now - self.invincible_timer > ENEMY_IFRAME_TIME:
                self.invincible = False
                self.image.set_alpha(255) # Make the sprite fully visible again
            # Reflect any change in coordinates, correct for collision, then reset the change values.
            self.collide_enemies()
            self.rect.x += self.x_change
            self.collide_obstacles('x')
            self.rect.y += self.y_change
            self.collide_obstacles('y')
            self.x_change = 0
            self.y_change = 0

            # Induce flicker effect for invincibility frames
            if self.invincible:
                self.flicker_timer += 1
                if self.flicker_timer % 3 == 0:
                    self.image.set_alpha(0) # Hide the sprite
                else:
                    self.image.set_alpha(255) # Show the sprite
            else:
                self.image.set_alpha(255)
                self.flicker_timer = 0   

            # Aggro setting: calculate distance to player and check for aggro. If less than 3 tiles, become aggro.
            player_pos = pygame.math.Vector2(self.game.player.rect.x, self.game.player.rect.y)
            enemy_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
            distance_to_player = enemy_pos.distance_to(player_pos)
            
            if distance_to_player < ENEMY_AGGRO_DISTANCE:
                self.aggro = True
            else:
                self.aggro = False

            if self.aggro and self.threat_level == 2:
                # If elite enemies, move towards the player
                #self.movement_aggro(player_pos, enemy_pos)        
                self.movement()  
            else:
                self.movement() # Call the movement method to capture any coordinate changes.

    # Method for sprite movement. 
    def movement(self):
        """
        Handles randomized patrol movement for the enemy. Includes boundary checks 
        to prevent wandering too far and immediate direction changes upon hitting 
        an obstacle.
        """
        current_time = time.time()
        if current_time - self.last_move_time > 1: # Change direction every second
            self.facing = random.choice(['left', 'right', 'up', 'down'])
            self.last_move_time = current_time
        
        # Force direction toward start if out of bounds
        current_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        start_pos = pygame.math.Vector2(self.start_x, self.start_y)
        distance_from_start = current_pos.distance_to(start_pos)

        if distance_from_start > self.max_travel_pixels:
            # Determine axis that's furthest from the start
            if abs(self.start_x - self.rect.x) > abs(self.start_y - self.rect.y):
                # Move horizontally back toward start
                self.current_direction = 'left' if self.rect.x > self.start_x else 'right'
            else:
                # Move vertically back toward start
                self.current_direction = 'up' if self.rect.y > self.start_y else 'down'
            # Reset timer to immediately apply new direction
            self.patrol_step_timer = self.patrol_step_limit

        correction_factor = 1.3
        if self.facing == 'left':
            self.rect.x -= self.speed
            self.x_change -= self.speed
            if self.collide_obstacles("x"): 
                self.rect.x += self.speed * correction_factor
                self.x_change += self.speed * correction_factor
                self.facing == 'right'
        elif self.facing == 'right':
            self.rect.x += self.speed
            self.x_change += self.speed
            if self.collide_obstacles("x"): 
                self.rect.x -= self.speed * correction_factor
                self.x_change -= self.speed * correction_factor
                self.facing == 'left'        
        elif self.facing == 'up':
            self.rect.y -= self.speed
            self.y_change -= self.speed
            if self.collide_obstacles("y"): 
                self.rect.y += self.speed * correction_factor
                self.y_change += self.speed * correction_factor
                self.facing == 'down'
        elif self.facing == 'down':
            self.rect.y += self.speed
            self.y_change += self.speed
            if self.collide_obstacles("y"): 
                self.rect.y -= self.speed * correction_factor
                self.y_change -= self.speed * correction_factor
                self.facing == 'up'

    # Method for sprite movement when aggro. Calculates a path to player and moves along it using TileMap.
    def movement_aggro(self, player_pos: pygame.math.Vector2, enemy_pos: pygame.math.Vector2):
        """
        Calculates the shortest path to the player using BFS pathfinding and 
        moves the enemy along the calculated path nodes.

        Arguments:
            player_pos (pygame.math.Vector2): The player's current pixel position.
            enemy_pos (pygame.math.Vector2): The enemy's current pixel position.
        """
        enemy_node = self.get_current_node()
        player_node = self.get_player_node(player_pos)

        '''Path Finding: Search for a new path (if the current one is finished).'''
        # Check if the player is in the last node of current path (to avoid recalculation).
        if not self.current_path or self.current_path[-1] != player_node:
            # Start search.
            new_path = find_path(
                self.game.tilemap, 
                enemy_node, 
                player_node         
            )

            # Path found.
            if new_path:
                # Discard the first node (which is the enemy's current position)
                self.current_path = new_path[1:]
            else:
                # No path found, run default movement.
                self.movement()
                return

        '''Movement: Move towards the next node in the path'''
        # Get the pixel position of the next target node's center
        if self.current_path:
            next_node_x, next_node_y = self.current_path[0]
            target_pixel_x = next_node_x * TILESIZE + TILESIZE // 2
            target_pixel_y = next_node_y * TILESIZE + TILESIZE // 2
            
            # Calculate the direction vector towards the center of the next tile
            direction_vector = pygame.math.Vector2(target_pixel_x, target_pixel_y) - enemy_pos
            
            # Check if we are close enough to the target node's center
            if direction_vector.length_squared() < (self.speed * self.speed * 2): # Small buffer
                # We've reached the current path node, remove it
                self.rect.center = (target_pixel_x, target_pixel_y) # Snap to center
                self.current_path.pop(0) 
                return # Stop and wait for the next update cycle
            
            # Normalize the vector and move (using your original movement method logic)
            direction_vector.normalize_ip()
            self.x_change = direction_vector.x * self.speed
            self.y_change = direction_vector.y * self.speed
            
            self.rect.x += self.x_change
            self.rect.y += self.y_change
            
            # Apply collision logic
            self.collide_obstacles("x")
            self.collide_obstacles("y")
            self.collide_enemies()

    # Method for sprite's collision detection w/ obstacle (e.g. block), depending on direction of collision. Returns True if collision occured, else False.
    def collide_obstacles(self, direction: str) -> bool:
        """
        Checks for enemy collision with walls, blocks, holes, and geo-obstacles.
        Corrects position to prevent clipping and returns True if a collision occurs.

        Arguments:
            direction (str): The axis of movement being checked ('x' or 'y').

        Returns:
            bool: True if a collision with a non-walkable sprite occurred, False otherwise.
        """
        # checks if rectangle of one sprite is colliding with rectangle of another: in this case, player's and all game blocks
        hits_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_holes = pygame.sprite.spritecollide(self, self.game.holes, False)
        geos_hits = pygame.sprite.spritecollide(self, self.game.ice_blocks, False)     
        waters_hits = pygame.sprite.spritecollide(self, self.game.waters, False) 

        if direction == "x":              
            if hits_block:
                    # An obstacle has been collided with, and hits[0] is that obstacle. 
                    # If sprite is moving right, correct to left 
                if self.x_change > 0:
                    self.rect.x = hits_block[0].rect.left - self.rect.width
                    return True
                # If sprite is moving left, correct to right
                if self.x_change < 0:
                    self.rect.x = hits_block[0].rect.right 
                    return True
            elif hits_holes:
                    # An obstacle has been collided with, and hits[0] is that obstacle. 
                    # If sprite is moving right, correct to left 
                if self.x_change > 0:
                    self.rect.x = hits_holes[0].rect.left - self.rect.width
                    return True
                # If sprite is moving left, correct to right
                if self.x_change < 0:
                    self.rect.x = hits_holes[0].rect.right 
                    return True
            elif geos_hits:
                    # An obstacle has been collided with, and hits[0] is that obstacle. 
                    # If sprite is moving right, correct to left 
                if self.x_change > 0:
                    self.rect.x = geos_hits[0].rect.left - self.rect.width
                    return True
                # If sprite is moving left, correct to right
                if self.x_change < 0:
                    self.rect.x = geos_hits[0].rect.right 
                    return True
            elif waters_hits:
                # An obstacle has been collided with, and hits[0] is that obstacle. 
                    # If sprite is moving right, correct to left 
                if self.x_change > 0:
                    self.rect.x = waters_hits[0].rect.left - self.rect.width
                    return True
                # If sprite is moving left, correct to right
                if self.x_change < 0:
                    self.rect.x = waters_hits[0].rect.right 
                    return True
            return False
                
        elif direction == "y":
            if hits_block:
                # An obstacle has been collided with, and hits[0] is that obstacle
                # If sprite is moving down, correct to up
                if self.y_change > 0:
                    self.rect.y = hits_block[0].rect.top - self.rect.height
                    return True
                # If sprite is moving up, correct to down
                if self.y_change < 0:
                    self.rect.y = hits_block[0].rect.bottom
                    return True
            elif hits_holes:
                    # An obstacle has been collided with, and hits[0] is that obstacle
                # If sprite is moving down, correct to up
                if self.y_change > 0:
                    self.rect.y = hits_holes[0].rect.top - self.rect.height
                    return True
                # If sprite is moving up, correct to down
                if self.y_change < 0:
                    self.rect.y = hits_holes[0].rect.bottom
                    return True
            elif geos_hits:
                # An obstacle has been collided with, and hits[0] is that obstacle
                # If sprite is moving down, correct to up
                if self.y_change > 0:
                    self.rect.y = geos_hits[0].rect.top - self.rect.height
                    return True
                # If sprite is moving up, correct to down
                if self.y_change < 0:
                    self.rect.y = geos_hits[0].rect.bottom
                    return True
            elif waters_hits:
                # An obstacle has been collided with, and hits[0] is that obstacle
                # If sprite is moving down, correct to up
                if self.y_change > 0:
                    self.rect.y = waters_hits[0].rect.top - self.rect.height
                    return True
                # If sprite is moving up, correct to down
                if self.y_change < 0:
                    self.rect.y = waters_hits[0].rect.bottom
                    return True
            return False

    # Method for sprite's collision detection w/ enemy, depending on direction of collision
    def collide_enemies(self):
        """
        Handles enemy-to-enemy collision detection, applying a push vector 
        to prevent enemies from overlapping and getting stuck.
        """
        # checks if rectangle of one sprite is colliding with rectangle of another: in this case, player's and all game blocks
        hits_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)
        
        for hit in hits_enemy:
            # Make sure sprite is not itself
            if hit != self:
                # Calculate vector from this enemy to the other enemy
                push_vector = pygame.math.Vector2(self.rect.x - hit.rect.x, self.rect.y - hit.rect.y)
                # Ensure consistent push
                if push_vector.length() > 0:
                    push_vector.normalize_ip()
                # Push this enemy away from the other enemy
                self.rect.x += push_vector.x * self.speed
                self.rect.y += push_vector.y * self.speed
     # Method for sprite's animation
    
    # Method to get the right sprite for enemy
    def get_animations(self, stage_type: int):
        """
        Loads the correct sprite animation sets (up/down/left/right) based on 
        the current stage type (1-5) and enemy type (Slime, Vampire, Orc).

        Arguments:
            stage_type (int): The current stage number to determine the enemy skin.
        """   
        self.stage_type = stage_type

        # Green Slime
        if self.stage_type == 1: 
            self.down_animations = [pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(24, 24, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(89, 22, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(152, 20, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(215, 18, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(278, 17, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(340, 17, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(404, 27, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(470, 25, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.up_animations = [pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(24, 88, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(88, 86, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(151, 84, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(214, 82, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(278, 81, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(341, 81, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(404, 91, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(471, 89, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.left_animations = [pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(24, 153, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(88, 150, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(151, 148, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(214, 146, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(278, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(340, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(404, 156, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(470, 154, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.right_animations = [pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(24, 217, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(89, 214, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(152, 212, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(215, 210, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(278, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(340, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(404, 220, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_green_spritesheet.get_sprite(470, 218, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.animation_loop_max = 8
        # Blue slime
        if self.stage_type == 2:
            self.down_animations = [pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(24, 24, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(89, 22, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(152, 20, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(215, 18, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(278, 17, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(340, 17, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(404, 27, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(470, 25, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.up_animations = [pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(24, 88, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(88, 86, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(151, 84, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(214, 82, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(278, 81, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(341, 81, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(404, 91, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(471, 89, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.left_animations = [pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(24, 153, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(88, 150, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(151, 148, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(214, 146, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(278, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(340, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(404, 156, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(470, 154, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.right_animations = [pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(24, 217, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(89, 214, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(152, 212, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(215, 210, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(278, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(340, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(404, 220, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_blue_spritesheet.get_sprite(470, 218, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.animation_loop_max = 8
        # Red slime
        if self.stage_type == 3: 
            self.down_animations = [pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(24, 24, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(89, 22, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(152, 20, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(215, 18, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(278, 17, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(340, 17, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(404, 27, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(470, 25, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.up_animations = [pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(24, 88, 17, 16), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(88, 86, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(151, 84, 18, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(214, 82, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(278, 81, 21, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(341, 81, 24, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(404, 91, 25, 13), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(471, 89, 20, 15), (SLIME_SCALE, SLIME_SCALE))]
            self.left_animations = [pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(24, 153, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(88, 150, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(151, 148, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(214, 146, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(278, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(340, 145, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(404, 156, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(470, 154, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.right_animations = [pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(24, 217, 18, 15), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(89, 214, 16, 18), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(152, 212, 19, 20), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(215, 210, 20, 22), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(278, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(340, 209, 23, 23), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(404, 220, 22, 12), (SLIME_SCALE, SLIME_SCALE)),
                                    pygame.transform.scale(self.game.slime_red_spritesheet.get_sprite(470, 218, 20, 14), (SLIME_SCALE, SLIME_SCALE))]
            self.animation_loop_max = 8
        # Vampire
        if self.stage_type == 4:
            self.down_animations = [pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(20, 19, 23, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(85, 17, 21, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(147, 18, 25, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(213, 19, 23, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(278, 17, 21, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(340, 18, 25, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE))]
            
            self.up_animations = [pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(20, 83, 23, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(85, 81, 21, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(147, 82, 25, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(213, 83, 23, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(278, 81, 21, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(340, 82, 25, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE))]
            
            self.left_animations = [pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(22, 167, 20, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(86, 145, 17, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(150, 164, 21, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(214, 147, 21, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(278, 145, 19, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(342, 146, 22, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE))]
            
            self.right_animations = [pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(21, 211, 20, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(88, 209, 17, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(148, 210, 21, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(212, 211, 21, 25), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(278, 209, 19, 27), (VAMPIRE_SCALE, VAMPIRE_SCALE)),
                                    pygame.transform.scale(self.game.vampire_spritesheet.get_sprite(339, 210, 22, 26), (VAMPIRE_SCALE, VAMPIRE_SCALE))]
            self.animation_loop_max = 6
        # Orc
        if self.stage_type == 5:
            self.down_animations = [pygame.transform.scale(self.game.orc_spritesheet.get_sprite(10, 16, 34, 28), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(74, 13, 35, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(138, 14, 34, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(203, 16, 33, 27), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(267, 13, 34, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(331, 14, 34, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE))]
            
            self.up_animations = [pygame.transform.scale(self.game.orc_spritesheet.get_sprite(21, 80, 33, 22), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(84, 77, 34, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(149, 78, 33, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(213, 80, 32, 27), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(277, 77, 32, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(341, 78, 32, 29), (ORC_SCALE+ORC_SCALE_MODIFIER, ORC_SCALE))]
            
            self.left_animations = [pygame.transform.scale(self.game.orc_spritesheet.get_sprite(22, 143, 17, 27), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(84, 142, 20, 28), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(147, 141, 20, 29), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(211, 143, 20, 27), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(276, 142, 19, 28), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(341, 141, 18, 29), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE))]
            
            self.right_animations = [pygame.transform.scale(self.game.orc_spritesheet.get_sprite(23, 207, 19, 27), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(89, 206, 18, 28), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(153, 205, 19, 29), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(217, 207, 20, 27), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(281, 205, 18, 30), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE)),
                                    pygame.transform.scale(self.game.orc_spritesheet.get_sprite(345, 205, 17, 29), (ORC_SCALE-ORC_SCALE_MODIFIER, ORC_SCALE))]
            self.animation_loop_max = 6
    
    # Method for sprite's animation
    def animate(self):
        """
        Cycles through the current enemy animation frames based on movement direction.
        """   
        # Use an animation sprites list depending on the direction sprite is facing while moving: down, up, left, or right.
        # self.animation_loop: using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame), looping at the end of the list to create an animation.
        if self.facing == "down":
            if self.y_change == 0:
                # If standing still, default to intial, first sprite facing downward
                self.image = self.down_animations[0]
            else:
                # If the y has changed (Player moved down), 
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= self.animation_loop_max:
                    self.animation_loop = 1        
        if self.facing == "up":
            if self.y_change == 0:
                # If standing still, default to intial, first sprite 
                self.image = self.up_animations[0]
            else:
                # If the y has changed (Player moved up), 
                self.image = self.up_animations[math.floor(self.animation_loop)]
                # using 0.1 and floor allows us to change the animation every 10 frames
                self.animation_loop += 0.1
                if self.animation_loop >= self.animation_loop_max:
                    self.animation_loop = 1        
        if self.facing == "left":
            if self.x_change == 0:
                # If standing still, default to intial, first sprite 
                self.image = self.left_animations[0]
            else:
                # If the x has changed (Player moved left), 
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= self.animation_loop_max:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                # If standing still, default to intial, first sprite 
                self.image = self.right_animations[0]
            else:
                # If the x has changed (Player moved up), 
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= self.animation_loop_max:
                    self.animation_loop = 1
    
    # Method to draw the enemy's health bar
    def draw_health_bar(self):
        """
        Draws the enemy's health bar (red) above the enemy sprite. Only called 
        when the health_bar_visible flag is True (i.e., after the enemy has been hit).
        """
        # Calculate the health ratio to determine the width of the green health bar
        health_ratio = self.health / self.max_health
        # Health bar dimensions
        bar_width = TILESIZE
        bar_height = 5
        # Position the health bar above the enemy
        bar_x = self.rect.x
        bar_y = self.rect.y - 10
        
        # Border thickness
        border_thickness = 1
        inner_width = bar_width - (border_thickness * 2)
        inner_height = bar_height - (border_thickness * 2)

        # Draw the golden background rectangle
        pygame.draw.rect(self.game.screen, GOLD, (bar_x, bar_y, bar_width, bar_height), border_thickness)
        # Draw the green health bar filling, inset by the border thickness
        pygame.draw.rect(self.game.screen, RED, (bar_x + border_thickness, bar_y + border_thickness, inner_width * health_ratio, inner_height))

# This class is for a tile map's stage path finding, used with enemies
class TileMap:
    """
    Utility class for parsing the string-array tilemap data into a grid. 
    Provides methods for pathfinding algorithms to check tile type 
    and connectivity.
    """
    def __init__(self, tilemap_data: tuple[str]):
        """
        Initializes the TileMap with map data and calculates grid dimensions.

        Arguments:
            tilemap_data (tuple[str]): The grid data.
        """
        self.data = tilemap_data
        # Map dimensions based on provided tile map data
        self.height = len(tilemap_data) 
        self.width = len(tilemap_data[0]) if self.height > 0 else 0

    def get_tile_char(self, x: int, y: int) -> Optional[str]:
        """
        Gets the character at the given grid coordinates.

        Arguments:
            x (int): The grid column index.
            y (int): The grid row index.

        Returns:
            Optional[str]: The tile character ('W', 'P', '.') or None if out of bounds.
        """
        # Get the character at the given grid coordinates, or None if out of bounds.
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.data[y][x]
        return None

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Checks if a given grid coordinate is within bounds and not an obstacle 
        based on the NON_WALKABLE_CHARS list in config.py.

        Arguments:
            x (int): The grid column index.
            y (int): The grid row index.

        Returns:
            bool: True if the tile is safe to walk on, False if it is an obstacle or out of bounds.
        """
        # Check if a given grid coordinate is within bounds and not an obstacle.
        char = self.get_tile_char(x, y)
        # Check if coordinate is out of bound
        if char is None:
            return False 
        
        # Check coordinate against defined set of non-walkable characters
        return char not in NON_WALKABLE_CHARS

    # Gets valid neighboring grids (up, down, left, right) that are walkable
    def get_neighbors(self, node: GridNode) -> List[GridNode]:
        """
        Returns a list of valid, walkable neighboring grid nodes (up, down, left, right).

        Arguments:
            node (GridNode): The starting (x, y) grid coordinates.

        Returns:
            List[GridNode]: A list of reachable neighbor coordinates.
        """
        x, y = node
        potential_neighbors = [
            (x + 1, y),  # Right
            (x - 1, y),  # Left
            (x, y + 1),  # Down
            (x, y - 1)   # Up
        ]
        
        # Filter out neighbors that are obstacles or out of bounds
        return [
            neighbor for neighbor in potential_neighbors 
            if self.is_walkable(neighbor[0], neighbor[1])
        ]

# A recursive function for finding a path from the enemy grid to the player grid using the BFS (Breadth-First Search) method.
def find_path(tilemap: TileMap, start_node: GridNode, end_node: GridNode) -> Optional[List[GridNode]]:  
    """
    Finds the shortest path between two grid nodes using BFS algorithm.

    Arguments:
        tilemap (TileMap): The map structure used to check walkability.
        start_node (GridNode): The enemy's starting (x, y) grid position.
        end_node (GridNode): The player's target (x, y) grid position.

    Returns:
        Optional[List[GridNode]]: The shortest path from start_node to end_node as a list of nodes, or None if no path exists.
    """
    if start_node == end_node:
        return [start_node]
        
    if not tilemap.is_walkable(start_node[0], start_node[1]) or \
       not tilemap.is_walkable(end_node[0], end_node[1]):
        return None 

    # Setup queue and history tracker
    queue = deque([start_node]) # Initialize the BFS queue
    # Creat dict to track the path: {current node: node we came from}
    came_from: Dict[GridNode, Optional[GridNode]] = {start_node: None} # <- CHANGED: Used to reconstruct the shortest path

    # Create a search loop
    while queue:
        current_node = queue.popleft() # Use FIFO (queue)

        if current_node == end_node:
            break

        for next_node in tilemap.get_neighbors(current_node):
            if next_node not in came_from:
                # This is the shortest way to reach next_node, so record it
                queue.append(next_node)
                came_from[next_node] = current_node # Record path history
    else:
        # No path found
        return None 

    # 3. Path Reconstruction 
    current = end_node
    path: List[GridNode] = []
    
    while current is not None:
        path.append(current)
        current = came_from[current]
        
    return path[::-1] # <- CHANGED: Reverse path to go start -> end

#This class represent obstacle block sprites, and how they are updated throughout gameplay
class Wall(pygame.sprite.Sprite):
    """
    Represents a solid, impassable wall or border object.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int):
        """
        Initializes a Wall sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): Used to select the correct visual asset.
        """
        self.game = game
        self.stage_type = stage_type
        self.groups = self.game.all_sprites, self.game.blocks
        # Call the inherited method of pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self._layer = BLOCK_LAYER

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(288, 480, 32, 32)

        if self.stage_type == 1:
            self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height) # Borders/walls brown rock
        elif self.stage_type == 2:
            self.image = self.game.terrain_spritesheet.get_sprite(928, 480, self.width, self.height) # Borders/walls ice rock
        elif self.stage_type == 3:
            self.image = self.game.terrain_spritesheet.get_sprite(994, 546, self.width, self.height) # Borders/walls fire rock
        elif self.stage_type == 4:
            pass
        elif self.stage_type == 5:
            pass
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#This class represent a normal obstacle block sprites, such as rocks, and how they are updated throughout gameplay
class Block(pygame.sprite.Sprite):
    """
    Represents a standard solid obstacle block (e.g., rocks).
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int):
        """
        Initializes a Block sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): Used to select the correct visual asset.
        """
        self.game = game
        self.stage_type = stage_type
        self.groups = self.game.all_sprites, self.game.blocks
        # Call the inherited method of pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self._layer = BLOCK_LAYER

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(224, 416, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) # Large brown rock

        # read the block sprite suitable for the given stage typed
        if self.stage_type == 1:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(834, 628, 58, 41), (BLOCK_SCALE, BLOCK_SCALE)) # Large brown rock
        elif self.stage_type == 2:
            self.image = self.game.terrain_spritesheet.get_sprite(960, 480, 32,32) # Small ice rocks
        elif self.stage_type == 3:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(960, 576, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) # Large black rock
        elif self.stage_type == 4:
            pass
        elif self.stage_type == 5:
            pass
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#This class represent a geological obstacle sprites, such as lava, lakes, etc. and how they are updated throughout gameplay
class Geo(pygame.sprite.Sprite):
    """
    Represents stage-unique environmental sprites like slippery ice, miasma, etc. 
    Handles animation for miasma effects.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int, geo_type: int, geo_layer: int):
        """
        Initializes a Geo sprite, placing it into the correct collision/interaction group.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): The current stage (determines base sprite set).
            geo_type (int): Specific type within the stage (e.g., 1=lava, 2=ice).
            geo_layer (int): The drawing layer (e.g., GROUND_LAYER or BLOCK_LAYER).
        """
        self.game = game
        self.stage_type = stage_type # each stage has different geo sprites: 1, 2, 3, etc.
        self.geo_type = geo_type # within each stage, geos can be different items like lakes, petals, etc. Valued as 1, 2, 3, etc.

        # place geo in appropriate sprite group depending on stage
        if stage_type == 1 and geo_type == 1:
            self.groups = self.game.all_sprites, self.game.geos, self.game.holes
        elif stage_type == 2 and geo_type == 2:
            self.groups = self.game.all_sprites, self.game.geos, self.game.ice_blocks
        elif stage_type == 2 and geo_type == 1:
            self.groups = self.game.all_sprites, self.game.geos, self.game.slippery_ice
        elif stage_type == 3 and geo_type == 1:
            self.groups = self.game.all_sprites, self.game.geos, self.game.blocks
        elif stage_type == 4 and geo_type == 1:
            self.groups = self.game.all_sprites, self.game.geos, self.game.miasmas
        elif stage_type == 4 and geo_type == 3:
            self.groups = self.game.all_sprites, self.game.geos, self.game.waters
        else:
            self.groups = self.game.all_sprites, self.game.geos
        # Call the inherited method of pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self._layer = geo_layer # Making the geo flexible allows us to layer geos on top of each other.

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(352, 352, 32, 32), (32, 32)) # Grass

        # read the geo sprite suitable for the given stage typed
        if self.stage_type == 1:
            if geo_type == 0:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(352, 352, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) # Grass
            if geo_type == 1:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(483, 546, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) # Water
                # Consider this geo obstacle a hole
            if geo_type == 2:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(354, 548, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) # Petals
        elif self.stage_type == 2:
            if geo_type == 1:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(483, 546, 32, 32), (32, 34)) # slippy ice
                # Consider this geo obstacle a hole
            elif geo_type == 2:
                self.image = pygame.transform.scale(self.game.ice_cube_spritesheet.get_sprite(0, 0, 32,32), (BLOCK_SCALE, BLOCK_SCALE)) # Small ice rocks
        elif self.stage_type == 3:
            if geo_type == 1:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(480, 160, 20, 20), (BLOCK_SCALE, BLOCK_SCALE)) # Lava
        elif self.stage_type == 4:
            if geo_type == 1:
                self.geo_animations = [pygame.transform.scale(self.game.miasma_spritesheet.get_sprite(0, 4, 32, 124), (32, 32)),
                           pygame.transform.scale(self.game.miasma_spritesheet.get_sprite(40, 8, 24, 120), (32, 32)),
                           pygame.transform.scale(self.game.miasma_spritesheet.get_sprite(68, 4, 28, 124), (32, 32)),
                           pygame.transform.scale(self.game.miasma_spritesheet.get_sprite(100, 8, 32, 120), (32, 32))]
                self.image = pygame.transform.scale(self.game.miasma_spritesheet.get_sprite(132, 8, 28, 120), (32, 32)) # Miasma
                self.animation_loop = 0
                self.animation_loop_max = 4
            elif geo_type == 2:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(64, 160, 32, 32), (BLOCK_SCALE, BLOCK_SCALE)) #  temple ground, outside
            elif geo_type == 3:
                self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(483, 546, 32, 32), (32, 34)) # Water
        elif self.stage_type == 5:
            pass
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        Updates the Geo sprite (primarily used for animated elements like miasma).
        """
        self.animate() # Call the animate method to change sprites for animation effect

    # Method for sprite's animation
    def animate(self):   
        """
        Cycles through the animation frames for Geo types that require it (e.g., Miasma).
        """
        if self.stage_type == 4 and self.geo_type == 1:
            # Using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 per frame).   
            self.image = self.geo_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop > self.animation_loop_max:
                self.animation_loop = 0 
    
#This class represent obstacle pitfall/hole sprites, and how they are updated throughout gameplay
class Hole(pygame.sprite.Sprite):
    """
    Represents a dangerous pitfall or hole that acts as an impassable obstacle, but can be jumped over.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int):
        """
        Initializes a Hole sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): Used to select the correct visual asset.
        """
        self.stage_type = stage_type
        self.game = game
        self.groups = self.game.all_sprites, self.game.holes
        # Call the inherited method of pygame.sprite.Sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self._layer = BLOCK_LAYER

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = self.game.terrain_spritesheet.get_sprite(681, 70, self.width, self.height)

        # read the hole sprite suitable for the given stage type
        if self.stage_type == 1:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(681, 70, 82, 79), (HOLE_SCALE, HOLE_SCALE)) # plains hole
        elif self.stage_type == 2:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(704, 544, 64, 64), (HOLE_SCALE, HOLE_SCALE)) # ice hole
        elif self.stage_type == 3:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(489, 70, 81, 79), (HOLE_SCALE, HOLE_SCALE)) # fire hole
        elif self.stage_type == 4:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(777, 70, 81, 79), (HOLE_SCALE, HOLE_SCALE)) # fire hole
        elif self.stage_type == 5:
            pass
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
#This class represent ground sprites, sprites the player traverses, and how they are updated throughout gameplay
class Ground(pygame.sprite.Sprite):
    """
    Represents the non-collidable background tile (floor) of a stage.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_type: int):
        """
        Initializes a Ground sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_type (int): Used to select the correct visual asset (Grass, Ice, Fire, etc.).
        """
        self.stage_type = stage_type
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(256, 480, 32, 32)

        # read the ground sprite suitable for the given stage type
        if stage_type == 1:
            self.image = self.game.terrain_spritesheet.get_sprite(58,544, self.width, self.height) # dark ground
        elif stage_type ==2:
            self.image = self.game.terrain_spritesheet.get_sprite(578,544, self.width, self.height) # ice ground
        elif self.stage_type == 3:
            self.image = self.game.terrain_spritesheet.get_sprite(417, 93, self.width, self.height) # fire ground
        elif self.stage_type == 4:
            self.image = pygame.transform.scale(self.game.terrain_spritesheet.get_sprite(928, 672, 64, 64), (BLOCK_SCALE, BLOCK_SCALE)) #  temple ground
        elif stage_type == 5:
            self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height) # grass ground
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

#This class represent switch sprites (unlocks doors)
class Switch(pygame.sprite.Sprite):
    """
    Represents a switch that the player must trigger to unlock doors. 
    Supports 'normal' (permanent) and 'timed' (temporary) types.
    """
    def __init__(self, game: 'Game', x: int, y: int, switch_type: str):
        """
        Initializes a Switch sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            switch_type (str): 'normal' or 'timed'.
        """
        self._layer = BLOCK_LAYER
        self.game = game
        self.groups = self.game.all_sprites, self.game.switches, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.locked_image = pygame.transform.scale(self.game.switch_spritesheet.get_sprite(2, 2, 12, 13), (SWITCH_SCALE, SWITCH_SCALE))
        self.unlocked_image = pygame.transform.scale(self.game.switch_spritesheet.get_sprite(18, 2, 12, 13), (SWITCH_SCALE, SWITCH_SCALE))
        self.image = self.locked_image

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.is_on = False
        self.switch_type = switch_type
        self.last_hit_time = 0
        self.permanent_on = False

    # update how the switch looks
    def update_image(self):
        """
        Updates the switch sprite to reflect its current ON/OFF state.
        """
        if self.is_on and self.switch_type == 'normal':
            self.image = self.unlocked_image
        elif self.is_on and self.switch_type == 'timed':
            self.image = self.unlocked_image
        elif self.switch_type == 'normal':
            self.image = self.locked_image
        elif self.switch_type == 'timed':
            self.image = self.locked_image

    # actions that occur on hit
    def on_hit(self) -> bool:
        """
        Handles the interaction when the switch is hit. 
        Activates normal switches permanently or timed switches temporarily.

        Returns:
            bool: True if the switch state changed, False otherwise.
        """
        if self.switch_type == 'normal' and not self.is_on:
            self.set_permanent_on()
            self.update_image()
            return True
        elif self.switch_type == 'timed' and not self.permanent_on:
            self.last_hit_time = time.time()
            self.is_on = True
            self.update_image()
            return True
        return False
    
    # reset switch status
    def reset(self):
        """
        Resets a timed switch to its original (unhit) state if it is not 
        set to permanent_on.
        """
        if not self.permanent_on:
            self.is_on = False
            self.last_hit_time = 0
            self.update_image()
        
    # set switch status as permanently on
    def set_permanent_on(self):
        """
        Sets the switch to a permanently ON state, typically used for normal switches 
        or when timed switches are successfully combined.
        """
        self.permanent_on = True
        self.is_on = True
        self.game.player.all_open == True
        self.update_image()

#This class represent door sprites (unlocked by switches)
class Door(pygame.sprite.Sprite):
    """
    Represents a stage exit door, which acts as a block until its linked switches 
    are all activated.
    """
    def __init__(self, game: 'Game', x: int, y: int, linked_switches: list[Switch]):
        """
        Initializes a Door sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            linked_switches (list[Switch]): List of Switch objects required to unlock the door.
        """
        self._layer = BLOCK_LAYER
        self.game = game
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.door_spritesheet.get_sprite(0, 0, 18, 32)
        
        self.open_animations = [pygame.transform.scale(self.game.door_spritesheet.get_sprite(18, 0, 18, 32), (DOOR_SCALE, DOOR_SCALE)),
                                pygame.transform.scale(self.game.door_spritesheet.get_sprite(36, 0, 18, 32), (DOOR_SCALE, DOOR_SCALE)),
                                pygame.transform.scale(self.game.door_spritesheet.get_sprite(54, 0, 18, 32), (DOOR_SCALE, DOOR_SCALE)),
                                pygame.transform.scale(self.game.door_spritesheet.get_sprite(72, 0, 18, 32), (DOOR_SCALE, DOOR_SCALE))]

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # controls the upcoming loop position of the sprite.
        self.animation_loop = 0
        self.linked_switches = linked_switches
        self.locked = True

    def update(self):
        """
        Checks the status of linked switches every frame. If all are permanently ON, 
        the door unlocks and plays its opening animation.
        """
        if self.locked:
            # Check if all linked switches are permenantly on; unlock door if they are
            all_on = True
            for switch in self.linked_switches:
                if not switch.permanent_on:
                    all_on = False
                    break
            if all_on:
                self.locked = False
                self.game.player.all_open = True
                self.game.sfxs['opened_all_switches'].play()
                self.open_animate()

    # Method for sprite's door opening animation
    def open_animate(self):
        """
        Plays the door opening animation by cycling through the open_animations array.
        """   
        # Using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame).
        while self.animation_loop < 4:
            self.image = self.open_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            # At animation loop 4, animation is complete: break
            if self.animation_loop == 4:
                break

#This class represent a stage portal: it carries a different interaction with the player whether it is locked or not, and leads to various stages depending on stage number.
class Portal(pygame.sprite.Sprite):
    """
    Represents a teleportation portal, either locked or unlocked, leading to different stages.
    """
    def __init__(self, game: 'Game', x: int, y: int, stage_number: int, is_locked: bool):
        """
        Initializes a Portal sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting grid column.
            y (int): Starting grid row.
            stage_number (int): The stage number the portal leads to (1-5).
            is_locked (bool): True if the portal is currently inaccessible.
        """
        self._layer = BLOCK_LAYER
        self.game = game
        self.is_locked = is_locked
        self.stage_number = stage_number
        self.groups = self.game.all_sprites, self.game.portals
        if self.is_locked:
            self.groups = self.game.all_sprites, self.game.portals_locked
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.portal_spritesheet.get_sprite(0, 0, 32, 32)

        self.portal_animation = [self.game.portal_spritesheet.get_sprite(0, 0, 32, 32),
                                self.game.portal_spritesheet.get_sprite(34, 0, 29, 32),
                                self.game.portal_spritesheet.get_sprite(66, 0, 28, 32),
                                self.game.portal_spritesheet.get_sprite(97, 0, 32, 32),
                                self.game.portal_spritesheet.get_sprite(130, 0, 30, 32),
                                self.game.portal_spritesheet.get_sprite(161, 0, 30, 32),
                                self.game.portal_spritesheet.get_sprite(194, 0, 28, 32),
                                self.game.portal_spritesheet.get_sprite(225, 0, 31, 32)]
        
        if self.is_locked:
            self.image = self.game.portal_locked_spritesheet.get_sprite(0, 0, 32, 32)
            self.portal_animation = [self.game.portal_locked_spritesheet.get_sprite(0, 0, 32, 32),
                                self.game.portal_locked_spritesheet.get_sprite(34, 0, 29, 32),
                                self.game.portal_locked_spritesheet.get_sprite(66, 0, 28, 32),
                                self.game.portal_locked_spritesheet.get_sprite(97, 0, 32, 32),
                                self.game.portal_locked_spritesheet.get_sprite(130, 0, 30, 32),
                                self.game.portal_locked_spritesheet.get_sprite(161, 0, 30, 32),
                                self.game.portal_locked_spritesheet.get_sprite(194, 0, 28, 32),
                                self.game.portal_locked_spritesheet.get_sprite(225, 0, 31, 32)]

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # controls the upcoming loop position of the sprite.
        self.animation_loop = 0

    def update(self):
        """
        Updates the portal's animation and checks for collision with the player 
        if the portal is unlocked.
        """
        self.animate() # Call the animate method to change sprites for animation effect
        if not self.is_locked:
            self.collide_player() # Call the collide_player method to detect if player touched unlocked portal

    # Method for sprite's animation
    def animate(self):   
        """
        Cycles through the portal animation frames.
        """
        # Using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 per frame).   
        # If player is facing up, use the up-facing images for animation
        self.image = self.portal_animation[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= PORTAL_FRAME_LIMIT:
            self.animation_loop = 0 

    # Method for colliding with player
    def collide_player(self) -> bool:
        """
        Checks for player collision and triggers a stage change to the portal's 
        destination stage number.

        Returns:
            bool: True if collision occurred and stage change was initiated.
        """
        # checks if a player has collided with this portal
        hits_player = pygame.sprite.spritecollide(self, self.game.players, False)
        
        # change the current stage when the player enters a portal.
        if hits_player:
            if self.stage_number == 1:
                self.game.player.current_stage = 1
                self.game.player.stage_changed = True
                return True
            if self.stage_number == 2:
                self.game.player.current_stage = 2
                self.game.player.stage_changed = True
                return True
            if self.stage_number == 3:
                self.game.player.current_stage = 3
                self.game.player.stage_changed = True
                return True
            if self.stage_number == 4:
                self.game.player.current_stage = 4
                self.game.player.stage_changed = True
                return True
            if self.stage_number == 5:
                self.game.player.current_stage = 5
                self.game.player.stage_changed = True
                return True
            else:
                self.game.player.current_stage = 0
                self.game.player.stage_changed = True
                return True
        return False
            
#This class represent a player's normal attack
class Attack(pygame.sprite.Sprite):
    """
    Represents the player's sprite for the normal (sword) attack.
    """
    def __init__(self, game: 'Game', x: int, y: int):
        """
        Initializes the Attack sprite.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting pixel x-coordinate of the hitbox.
            y (int): Starting pixel y-coordinate of the hitbox.
        """
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        # controls the upcoming loop position of the sprite (e.g. in a 3-sprites loop, 2 is the third sprite). Defaults to 1 (second sprite).
        self.animation_loop = 0
        #the visual elements of the sprite itself: height, width, img used, etc.
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)
        #sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.sfxs['attack'].play()

        # Create lists of each animation, get and store its associated sprites within
        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    # Method for updating the game after an action, e.g. movement or attacking
    def update(self):
        """
        Updates the attack state: checks for collisions and advances the animation loop.
        """
        self.collide() # Call the movement method to capture any coordinate changes.
        self.animate() # Call the animate method to change sprites for animation effect.

    # Method to check if attack collides with enemy
    def collide(self):
        """
        Checks for collision with enemies and switches. Deals damage and kills 
        enemies on hit. Triggers switches.
        """
        # checks if rectangle of attack sprite is colliding with rectangle of enemy's.
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        switch_hits = pygame.sprite.spritecollide(self, self.game.switches, False)

        if enemy_hits:
            for enemy in enemy_hits:
                # When enemy is hit, reduce its health and give it invincibility frames for a time. If the hit reduced enemy health to 0, kill it.
                if not enemy.invincible:
                        enemy.health -= ATTACK_DAMAGE
                        self.game.sfxs['enemy_hit'].play()
                        enemy.invincible = True
                        enemy.invincible_timer = pygame.time.get_ticks()
                        # Restore mana when a normal attack hits
                        self.game.player.mana += SLASH_MANA_RESTORE
                        if self.game.player.mana > self.game.player.max_mana:
                            self.game.player.mana = self.game.player.max_mana
                        # Make the enemy health bar visible
                        enemy.health_bar_visible = True
                        if enemy.health <= 0:
                            self.game.sfxs['enemy_death'].play()
                            enemy.kill()
        if switch_hits:
            for switch in switch_hits:
                self.game.sfxs['switch_hit'].play()
                switch.on_hit()

    # Method for attack sprite's animation
    def animate(self):
        """
        Advances the attack animation loop. Kills the attack sprite when the 
        animation is complete to remove the hitbox.
        """
        direction = self.game.player.facing # get the player's current direction to control the sprite choice

        # Use an animation sprites list depending on the direction player sprite is facing while moving: down, up, left, or right.
        # self.animation_loop: using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame), looping at the end of the list to create an animation.
        if direction == "down":
            # If player is facing up, use the up-facing images for animation
            self.image = self.down_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()       
        if direction == "up":
            # If player is facing up, use the up-facing images for animation
            self.image = self.up_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill() 
        if direction == "left":
            # If player is facing up, use the up-facing images for animation
            self.image = self.left_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill() 
        if direction == "right":
            # If player is facing up, use the up-facing images for animation
            self.image = self.right_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill() 

#This class represent a player's fireball spell
class Fireball(pygame.sprite.Sprite):
    """
    Represents a ranged projectile spell. Moves in a fixed direction until collision.
    """
    def __init__(self, game: 'Game', x: int, y: int, direction: str, is_from_explosion: bool = False):
        """
        Initializes the Fireball projectile.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting pixel x-coordinate.
            y (int): Starting pixel y-coordinate.
            direction (str): The direction of travel ('up', 'down', 'left', 'right').
            is_from_explosion (bool): Flag if the fireball originated from an Explosion (used for logic separation).
        """
        self.game = game
        self.direction = direction
        self._layer = PLAYER_LAYER
        self.is_from_explosion = is_from_explosion
        self.groups = self.game.all_sprites, self.game.fireballs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        # controls the upcoming loop position of the sprite (e.g. in a 3-sprites loop, 2 is the third sprite). Defaults to 1 (second sprite).
        self.animation_loop = 0
        #the visual elements of the sprite itself: height, width, img used, etc.
        self.image = self.game.fireball_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)
        #sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.sfxs['fireball'].play()

        # Create lists of each animation, get and store its associated sprites within
        self.right_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(3, 8, 13, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(23, 8, 15, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(44, 8, 14, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(61, 8, 17, 4), (FIREBALL_SCALE, FIREBALL_SCALE))]

        self.down_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(8, 62, 4, 12), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(28, 65, 4, 14), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(48, 64, 4, 15), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(67, 68, 4, 12), (FIREBALL_SCALE, FIREBALL_SCALE))]

        self.left_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(3, 28, 17, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(23, 28, 14, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(41, 28, 15, 4), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(66, 28, 12, 4), (FIREBALL_SCALE, FIREBALL_SCALE))]

        self.up_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(8, 42, 4, 12), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(28, 42, 4, 15), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(48, 42, 4, 14), (FIREBALL_SCALE, FIREBALL_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(68, 42, 4, 17), (FIREBALL_SCALE, FIREBALL_SCALE))]

    # Method for updating the game after an action, e.g. movement or attacking
    def update(self):
        """
        Updates the fireball state: checks collision, advances animation, and moves the projectile.
        """
        self.collide() # Call the movement method to capture any coordinate changes.
        self.animate() # Call the animate method to change sprites for animation effect.

        if self.direction == 'up':
            self.rect.y -= FIREBALL_SPEED
        if self.direction == 'down':
            self.rect.y += FIREBALL_SPEED
        if self.direction == 'left':
            self.rect.x -= FIREBALL_SPEED
        if self.direction == 'right':
            self.rect.x += FIREBALL_SPEED

    # Method to heck if fireball collides with enemy
    def collide(self):
        """
        Checks for collision with enemies, blocks, and switches. Deals damage to 
        enemies, kills itself on any obstacle hit, and may destroy certain Geo blocks (ice).
        """
        # checks if rectangle of fireball sprite is colliding with rectangle of enemy's.
        hits_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)
        switch_hits = pygame.sprite.spritecollide(self, self.game.switches, False)
        geos_hits = pygame.sprite.spritecollide(self, self.game.ice_blocks, False)

        if switch_hits:
            for switch in switch_hits:
                self.game.sfxs['switch_hit'].play()
                switch.on_hit()
        if hits_enemy:
            for enemy in hits_enemy:
                # When enemy is hit, reduce its health and give it invincibility frames for a time. If the hit reduced enemy health to 0, kill it.
                if not enemy.invincible:
                    enemy.health -= FIREBALL_DAMAGE
                    self.game.sfxs['fireball_impact'].play()
                    enemy.invincible = True
                    enemy.invincible_timer = pygame.time.get_ticks()
                    # Make the enemy health bar visible
                    enemy.health_bar_visible = True
                    if enemy.health <= 0:
                        self.game.sfxs['enemy_death'].play()
                        enemy.kill()
                    self.kill()
        # checks if rectangle of fireball sprite is colliding with a block.
        hits_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
        # When the spell hits a block, kill the sprite
        if hits_block:
            self.kill()
        # When the spell hits an ice block, kill the block along with the sprite
        if geos_hits:
            if geos_hits[0].geo_type == 2 and self.game.player.current_stage == 2:
                geos_hits[0].kill()
                self.kill()

    # Method for attack sprite's animation
    def animate(self):
        """
        Cycles through the fireball animation frames corresponding to its direction of travel.
        """
        direction = self.game.player.facing # get the player's current direction to control the sprite choice

        # Use an animation sprites list depending on the direction player sprite is facing while moving: down, up, left, or right.
        # self.animation_loop: using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame), looping at the end of the list to create an animation.
        if direction == "down":
            # If player is facing up, use the up-facing images for animation
            self.image = self.down_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0      
        if direction == "up":
            # If player is facing up, use the up-facing images for animation
            self.image = self.up_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0 
        if direction == "left":
            # If player is facing up, use the up-facing images for animation
            self.image = self.left_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0
        if direction == "right":
            # If player is facing up, use the up-facing images for animation
            self.image = self.right_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0 

#This class represent a player's Explosion spell
class Explosion(pygame.sprite.Sprite):
    """
    Represents the class for the Explosion 
    spell. It is a projectile that deals damage, 
    and spawns four Fireball projectiles in 4 
    cardinal directions upon collision.
    """
    def __init__(self, game: 'Game', x: int, y: int):
        """
        Initializes the Explosion spell.

        Arguments:
            game (Game): Reference to the main Game instance.
            x (int): Starting pixel x-coordinate.
            y (int): Starting pixel y-coordinate.
        """
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.explosions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        # controls the upcoming loop position of the sprite (e.g. in a 3-sprites loop, 2 is the third sprite). Defaults to 1 (second sprite).
        self.animation_loop = 0
        #the visual elements of the sprite itself: height, width, img used, etc.
        self.image = self.game.fireball_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)
        #sprite position/hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game.sfxs['explosion'].play(maxtime=2000)

        # Create lists of each animation, get and store its associated sprites within
        self.right_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(3, 8, 13, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(23, 8, 15, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(44, 8, 14, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(61, 8, 17, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE))]

        self.down_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(8, 62, 4, 12), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(28, 65, 4, 14), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(48, 64, 4, 15), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(67, 68, 4, 12), (EXPLOSION_SCALE, EXPLOSION_SCALE))]

        self.left_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(3, 28, 17, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(23, 28, 14, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(41, 28, 15, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(66, 28, 12, 4), (EXPLOSION_SCALE, EXPLOSION_SCALE))]

        self.up_animations = [pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(8, 42, 4, 12), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(28, 42, 4, 15), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(48, 42, 4, 14), (EXPLOSION_SCALE, EXPLOSION_SCALE)),
                           pygame.transform.scale(self.game.fireball_spritesheet.get_sprite(68, 42, 4, 17), (EXPLOSION_SCALE, EXPLOSION_SCALE))]

    # Method for updating the game after an action, e.g. movement or attacking
    def update(self):
        """
        Updates the explosion state: checks collision, advances animation, and determines 
        if the spell should expire and spawn Fireballs.
        """
        self.collide() # Call the movement method to capture any coordinate changes.
        self.animate() # Call the animate method to change sprites for animation effect.

        self.direction = self.game.player.facing

        if self.direction == 'up':
            self.rect.y -= FIREBALL_SPEED
        if self.direction == 'down':
            self.rect.y += FIREBALL_SPEED
        if self.direction == 'left':
            self.rect.x -= FIREBALL_SPEED
        if self.direction == 'right':
            self.rect.x += FIREBALL_SPEED

    # Method to heck if fireball collides with enemy
    def collide(self):
        """
        Checks for collision with targets. Deals damage, spawns 4 Fireballs 
        in cardinal directions, and kills itself.
        """
        # checks if rectangle of fireball sprite is colliding with rectangle of enemy's.
        hits_enemy = pygame.sprite.spritecollide(self, self.game.enemies, False)
        switch_hits = pygame.sprite.spritecollide(self, self.game.switches, False)
        geos_hits = pygame.sprite.spritecollide(self, self.game.ice_blocks, False)

        if switch_hits:
            for switch in switch_hits:
                self.game.sfxs['switch_hit'].play()
                switch.on_hit()
        if hits_enemy:
            for enemy in hits_enemy:
                # When enemy is hit, reduce its health and give it invincibility frames for a time. If the hit reduced enemy health to 0, kill it.
                if not enemy.invincible:
                    enemy.health -= EXPLOSION_DAMAGE
                    self.game.sfxs['fireball_impact'].play()
                    enemy.invincible = True
                    enemy.invincible_timer = pygame.time.get_ticks()
                    # Make the enemy health bar visible
                    enemy.health_bar_visible = True
                    if enemy.health <= 0:
                        enemy.kill()
                    self.game.sfxs['fireball_impact'].play()
                    # After hit, explode into 4 fireballs
                    Fireball(self.game, self.rect.x, self.rect.y, 'up')
                    Fireball(self.game, self.rect.x, self.rect.y, 'down')
                    Fireball(self.game, self.rect.x, self.rect.y, 'left')
                    Fireball(self.game, self.rect.x, self.rect.y, 'right')
                    self.kill()
        # checks if rectangle of fireball sprite is colliding with a block.
        hits_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits_wall = pygame.sprite.spritecollide(self, self.game.blocks, False)
        # When the spell hits a block, kill the sprite
        if hits_block:
            # After hit, explode into 4 fireballs
            Fireball(self.game, self.rect.x, self.rect.y, 'up')
            Fireball(self.game, self.rect.x, self.rect.y, 'down')
            Fireball(self.game, self.rect.x, self.rect.y, 'left')
            Fireball(self.game, self.rect.x, self.rect.y, 'right')
            self.kill()
        if hits_wall:
            # After hit, explode into 4 fireballs
            Fireball(self.game, self.rect.x, self.rect.y, 'up')
            Fireball(self.game, self.rect.x, self.rect.y, 'down')
            Fireball(self.game, self.rect.x, self.rect.y, 'left')
            Fireball(self.game, self.rect.x, self.rect.y, 'right')
            self.kill()
        if geos_hits:
            geos_hits[0].kill()
            # After hit, explode into 4 fireballs
            Fireball(self.game, self.rect.x, self.rect.y, 'up')
            Fireball(self.game, self.rect.x, self.rect.y, 'down')
            Fireball(self.game, self.rect.x, self.rect.y, 'left')
            Fireball(self.game, self.rect.x, self.rect.y, 'right')
            self.kill()

    # Method for attack sprite's animation
    def animate(self):
        """
        Cycles through the explosion animation frames.
        """
        direction = self.game.player.facing # get the player's current direction to control the sprite choice

        # Use an animation sprites list depending on the direction player sprite is facing while moving: down, up, left, or right.
        # self.animation_loop: using 0.1 and math.floor allows us to move to the next sprite in the list every 10 frames (incrementing 0.1 [per frame), looping at the end of the list to create an animation.
        if direction == "down":
            # If player is facing up, use the up-facing images for animation
            self.image = self.down_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0      
        if direction == "up":
            # If player is facing up, use the up-facing images for animation
            self.image = self.up_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0 
        if direction == "left":
            # If player is facing up, use the up-facing images for animation
            self.image = self.left_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0
        if direction == "right":
            # If player is facing up, use the up-facing images for animation
            self.image = self.right_animations[math.floor(self.animation_loop)]
            # using 0.5 and floor allows us to change the animation every 2 frames
            self.animation_loop += FIREBALL_FRAME_INCREMENT
            if self.animation_loop >= FIREBALL_FRAME_LIMIT:
                self.animation_loop = 0 
