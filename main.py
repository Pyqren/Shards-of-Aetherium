### The main Python file that should be run to start the game.

## Imports
import pygame
import sys
from sprites import *
from config import *
import json # Used for handling jason data in save file I/O

class Game:
     # This code is for game bootup 
    def __init__(self):
        pygame.init()
        # Initialize the mixer for audio
        pygame.mixer.init()
        #Width and height of display
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #Framerate
        self.clock = pygame.time.Clock()
        #font used
        self.font = pygame.font.Font(PIXELMAX, 16)
        # Set the game as running on initialization
        self.running = True
        # Set the game as not currently paused on initialization (can change depending on player action)
        self.paused = False
        # Set the game as having not shown the controls to the player yet upon initialization
        self.controls_shown = False
        # Parameter to check if currently showing a hint window (to avoid overlap with pause screen)
        self.showing_hint = False
        self.hint_not_shown = True
        # Tile object
        self.tilemap = None

        # Load in all sprites and images to be used
        # Player and terrain
        self.character_spritesheet = Spritesheet(PLAYER_WALK_SPRITE)
        self.character_hurt_spritesheet = Spritesheet(PLAYER_HURT_SPRITE)
        self.character_death_spritesheet = Spritesheet(PLAYER_DEATH_SPRITE)
        self.character_attack_spritesheet = Spritesheet(CHARACTER_ATTACK_SPRITE)
        self.character_teleport_spritesheet = Spritesheet(PLAYER_TELEPORT_SPRITE)
        self.character_barrier_spritesheet = Spritesheet(PLAYER_BARRIER_SPRITE)
        self.terrain_spritesheet = Spritesheet(TERRAIN_SPRITE)
        self.ice_cube_spritesheet = Spritesheet(ICE_CUBE_SPRITE)
        self.switch_spritesheet = Spritesheet(SWITCH_SPRITE)
        self.door_spritesheet = Spritesheet(DOOR_SPRITE)
        self.portal_spritesheet = Spritesheet(PORTAL_SPRITE)
        self.portal_locked_spritesheet = Spritesheet(PORTAL_LOCKED_SPRITE)
        self.miasma_spritesheet = Spritesheet(MIASMA_SPRITE)
        # Enemies
        self.slime_green_spritesheet = Spritesheet(GREEN_SLIME_WALK_SPRITE)
        self.slime_red_spritesheet = Spritesheet(RED_SLIME_WALK_SPRITE)
        self.slime_blue_spritesheet = Spritesheet(BLUE_SLIME_WALK_SPRITE)
        self.vampire_spritesheet = Spritesheet(VAMPIRE_WALK_SPRITE)
        self.orc_spritesheet = Spritesheet(ORC_WALK_SPRITE)
        # Abilities
        self.attack_spritesheet = Spritesheet(PLAYER_ATTACK_SPRITE)
        self.fireball_spritesheet = Spritesheet(PLAYER_FIREBALL_SPRITE)
        self.explosion_spritesheet = Spritesheet(PLAYER_EXPLOSION_SPRITE)
        # Misc
        self.menu_background = pygame.image.load(MENU)
        self.menu_background = pygame.transform.scale(self.menu_background, (WIN_WIDTH, WIN_HEIGHT))
        self.game_over_background = pygame.image.load(GAMEOVER)
        self.game_over_background = pygame.transform.scale(self.game_over_background, (WIN_WIDTH, WIN_HEIGHT))
        self.studio_logo = pygame.image.load(STUDIO_LOGO_IMAGE).convert_alpha()
        self.studio_logo = pygame.transform.scale(self.studio_logo, (WIN_WIDTH, WIN_HEIGHT))
        self.intro_background = pygame.image.load(INTRO_IMAGE).convert()
        self.intro_background = pygame.transform.scale(self.intro_background, (WIN_WIDTH, WIN_HEIGHT))
        self.credits_background = pygame.image.load(CREDITS_IMAGE).convert()
        self.credits_background = pygame.transform.scale(self.credits_background, (WIN_WIDTH, WIN_HEIGHT))
        self.controls_image = pygame.image.load(CONTROLS)
        self.controls_clicked_image = pygame.image.load(CONTROLS_CLICKED)
        self.loading_1_image = pygame.image.load(LOADING_1)
        self.loading_1_image = pygame.transform.scale(self.loading_1_image, (WIN_WIDTH, WIN_HEIGHT))
        self.loading_2_image = pygame.image.load(LOADING_2)
        self.loading_2_image = pygame.transform.scale(self.loading_2_image, (WIN_WIDTH, WIN_HEIGHT))
        self.loading_3_image = pygame.image.load(LOADING_3)
        self.loading_3_image = pygame.transform.scale(self.loading_3_image, (WIN_WIDTH, WIN_HEIGHT))
        self.loading_4_image = pygame.image.load(LOADING_4)
        self.loading_4_image = pygame.transform.scale(self.loading_4_image, (WIN_WIDTH, WIN_HEIGHT))
        self.loading_5_image = pygame.image.load(LOADING_5)
        self.loading_5_image = pygame.transform.scale(self.loading_5_image, (WIN_WIDTH, WIN_HEIGHT))
        self.victory_image = pygame.image.load(VICTORY)
        self.victory_image = pygame.transform.scale(self.victory_image, (WIN_WIDTH, WIN_HEIGHT))
        self.clear_image = pygame.image.load(CLEAR)
        self.clear_image = pygame.transform.scale(self.clear_image, (WIN_WIDTH, WIN_HEIGHT))
        # Semi-transparent (60% opacity, i.e. 150 out of 255 alpha) overlay for bg images.
        self.overlay_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        self.overlay_surface.fill(BLACK)
        self.overlay_surface.set_alpha(150) 

        # Load sound effects
        self.sfxs = {
            'logo_chime': pygame.mixer.Sound(CHIME_SFX),
            'switch_hit': pygame.mixer.Sound(SWITCH_HIT_SFX),
            'opened_all_switches': pygame.mixer.Sound(SWITCH_OPEN_ALL_SFX),
            'victory': pygame.mixer.Sound(VICTORY_SFX),
            'pause': pygame.mixer.Sound(PAUSE_SFX),
            'unpause': pygame.mixer.Sound(UNPAUSE_SFX),
            'attack': pygame.mixer.Sound(ATTACK_SFX),
            'fireball': pygame.mixer.Sound(FIREBALL_SFX),
            'fireball_impact': pygame.mixer.Sound(FIREBALL_IMPACT_SFX),
            'explosion': pygame.mixer.Sound(EXPLOSION_SFX),
            'player_hit': pygame.mixer.Sound(PLAYER_HIT_SFX),
            'enemy_hit': pygame.mixer.Sound(ENEMY_HIT_SFX),
            'enemy_death': pygame.mixer.Sound(ENEMY_DEATH_SFX),
            'player_death': pygame.mixer.Sound(PLAYER_DEATH_SFX),
            'barrier': pygame.mixer.Sound(BARRIER_SFX),
        }

        # Set volume for music and sound effects
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        for sfx in self.sfxs.keys():
            self.sfxs[sfx].set_volume(SFX_VOLUME)
        # Special consideration to the logo chime, which is especially loud
        self.sfxs['logo_chime'].set_volume(0.1)

    # This method creates a tile map via a loop through tilemap's rows and columns, replacing characters with tiles.
    def createTileMap(self, curr_tilemap: tuple[str], stage_type: int, curr_player: Player = None):        
        '''
        Different tile art will be used depending on the stage type (1 to 5).
        Type 1: plains
        Type 2: ice
        Type 3: fire
        Type 4: temple
        Type 5: maze
        '''

        # Assign the tile map to the TileMap object for path finding.
        self.tilemap = TileMap(curr_tilemap)

        # Remove all sprites from all groups before transitioning.
        for sprite in self.all_sprites:
            sprite.kill()
        # Explicitly clear the screen and update the display to remove old sprites.
        self.screen.fill(BLACK)
        pygame.display.flip() 
        for i, row in enumerate(curr_tilemap):
            for j, column in enumerate(row):
                # for stage 2, place slippery ice under enemies
                if stage_type == 2:
                    if column == ".":
                        Ground(self, j, i, stage_type)
                    else:
                        Geo(self, j, i, stage_type, 1, GROUND_LAYER)
                else:
                    Ground(self, j, i, stage_type)
                if column == "P":
                    # Place Player sprite at x=j and y=i coordinates
                    if curr_player == None:
                        print("went through none")
                        # Player entered stage through portal
                        if stage_type == 4:
                            Geo(self, j, i, stage_type, 2, GROUND_LAYER)
                        else:
                            Ground(self, j, i, stage_type)
                        self.player = Player(self, j, i)
                        print(j, " ", i)
                        self.player.current_stage = stage_type
                        if stage_type == 5:
                            self.player.all_open = True
                        else:
                            self.player.all_open = False
                        self.load_progress()
                        print("self.player.rect", self.player.rect)
                    else:
                        # Player is replaying stage after dying
                        print("went through other one")
                        if stage_type == 4:
                            Geo(self, j, i, stage_type, 2, GROUND_LAYER)
                        else:
                            Ground(self, j, i, stage_type)
                        self.player = Player(self, j, i)
                        print(j, " ", i)
                        self.player.current_stage = stage_type
                        if stage_type == 5:
                            self.player.all_open = True
                        else:
                            self.player.all_open = False
                        self.player.update_player_stats(curr_player)  
                        print("self.player.rect", self.player.rect)
                if column == "W":
                    # Place a wall sprite at x=j and y=i coordinates
                        Wall(self, j, i, stage_type)
                if column == "B":
                    # Place a block sprite at x=j and y=i coordinates
                        Block(self, j, i, stage_type)
                if column == "H":
                    # Place a hole sprite at x=j and y=i coordinates
                    Hole(self, j, i, stage_type)
                if column == "E":
                    # Place weak enemy (threat level = 1) sprite at x=j and y=i coordinates
                    if stage_type == 4:
                        Ground(self, j, i, stage_type)
                        Geo(self, j, i, stage_type, 1, BLOCK_LAYER)
                    Enemy(self, j, i, stage_type, 1)
                if column == "L":
                    # Place an elite enemy (threat level = 2) sprite at x=j and y=i coordinates
                    if stage_type == 4:
                        Ground(self, j, i, stage_type)
                        Geo(self, j, i, stage_type, 1, BLOCK_LAYER)
                    Enemy(self, j, i, stage_type, 2)
                if column == "S":
                    # Place a switch sprite at x=j and y=i coordinates
                    Ground(self, j, i, stage_type)
                    switch = Switch(self, j, i, 'normal')
                    self.switches_list.append(switch)
                if column == "_":
                    # Place a ground_layer type-0 geo sprite at x=j and y=i coordinates
                        Geo(self, j, i, stage_type, 2, GROUND_LAYER)
                if column == "-":
                    # Place a ground_layer type-1 geo sprite at x=j and y=i coordinates
                        if stage_type == 4:
                            Geo(self, j, i, stage_type, 3, GROUND_LAYER)
                        else:
                            Geo(self, j, i, stage_type, 1, GROUND_LAYER)
                            
        # Second enumerate for items that have dependencies on the existence of objects in first enumerate
        for i, row in enumerate(curr_tilemap):
            for j, column in enumerate(row):
                if column == "1":
                    # Place a portal for stage 1 sprite at x=j and y=i coordinates
                        Portal(self, j, i, 1, self.player.stages_locked[0])
                if column == "2":
                    # Place a portal for stage 2 sprite at x=j and y=i coordinates
                        Portal(self, j, i, 2, self.player.stages_locked[1])
                if column == "3":
                    # Place a portal for stage 3 sprite at x=j and y=i coordinates
                        Portal(self, j, i, 3, self.player.stages_locked[2])
                if column == "4":
                    # Place a portal for stage 4 sprite at x=j and y=i coordinates
                        Portal(self, j, i, 4, self.player.stages_locked[3])
                if column == "5":
                    # Place a portal for stage 5 sprite at x=j and y=i coordinates
                        Portal(self, j, i, 5, self.player.stages_locked[4])
                if column == "D":
                    # Door + Find all switches linked to this door's coordinates
                    linked_switches = self.switches_list
                    Door(self, j, i, linked_switches)
                if column == "=":
                    # Place a block_layer type-2 geo sprite at x=j and y=i coordinates, on top of another Geo
                        if stage_type == 1:
                            Geo(self, j, i, stage_type, 1, GROUND_LAYER)
                            Geo(self, j, i, stage_type, 2, BLOCK_LAYER)
                        elif stage_type == 2:
                            Geo(self, j, i, stage_type, 2, BLOCK_LAYER)
                        elif stage_type == 4:
                            Geo(self, j, i, stage_type, 1, BLOCK_LAYER)
                
    # Check for timed switches every 1 second
    def timed_switches_check(self):
        # Iterate through each locked door, get its timed switches (if any)
        for door in self.doors:
            if not door.locked:
                continue
            timed_switches = [self.switches_by_coord.get(coord) for coord in door.linked_switches if self.switches_by_coord.get(coord).switch_type == 'timed']
            if not timed_switches:
                continue
            
            last_hit = 0 # First timed switch hit
            all_hit = True # Set to False if the timing is off

            for switch in timed_switches: 
                 # if the switch has been hit 
                if switch.last_hit_time > 0:
                    if last_hit == 0: # If this is the first switch being checked, record hit time
                        last_hit = switch.last_hit_time
                    elif abs(switch.last_hit_time - last_hit) > 1.0: # If it's not the first, calculate absolute (to ensure positive value) difference between current switch's hit time and the last_hit time
                        # If difference is greater than 1 second, player was too slow: set all_hit to False and break out of loop
                        all_hit = False
                        break
                 # if the switch has not been hit, set all_hit = False by default
                else:
                    all_hit = False
                    break
            # player hit all the timed switches within the 1-second window
            if all_hit:
                for switch in timed_switches:
                    switch.set_permanent_on()
            # player failed the timing
            else:
                for switch in timed_switches:
                    # Check if a timed switch needs to be reset due to being hit in the attempt
                    if time.time() - switch.last_hit_time > 1.0: 
                        switch.reset()
    # This method runs whenever we start a new game
    def set_stage(self, current_stage: int, player: Player = None):
        #indicates that the player is currently alive and playing
        self.playing = True
        #this object contains all game sprites, including environment, player and enemies, etc., allowing sprite update
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.geos = pygame.sprite.LayeredUpdates()
        self.ice_blocks = pygame.sprite.LayeredUpdates()
        self.slippery_ice = pygame.sprite.LayeredUpdates()
        self.miasmas = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.holes = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.fireballs = pygame.sprite.LayeredUpdates()
        self.explosions = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.switches = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()
        self.portals_locked = pygame.sprite.LayeredUpdates()
        self.switches_list = []

        # Setup the game's tilemap, depending on stage entered
        if current_stage == 1:
            self.createTileMap(tilemap1, 1, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(STAGE_1_MUSIC)
            pygame.mixer.music.play(-1,3)
        elif current_stage == 2:
            self.createTileMap(tilemap2, 2, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(STAGE_2_MUSIC)
            pygame.mixer.music.play(-1,3)
        elif current_stage == 3:
            self.createTileMap(tilemap3, 3, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(STAGE_3_MUSIC)
            pygame.mixer.music.play(-1)
        elif current_stage == 4:
            self.createTileMap(tilemap4, 4, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(STAGE_4_MUSIC)
            pygame.mixer.music.play(-1)
        elif current_stage == 5:
            self.createTileMap(tilemap5, 5, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(STAGE_5_MUSIC)
            pygame.mixer.music.play(-1)
        # Stage 0 indicates the tower hub area, where all other stages portals are.
        elif current_stage == 0:
            self.createTileMap(tower_hub, 0, player)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(TOWER_MUSIC)
            pygame.mixer.music.play(-1)

        if current_stage != 0:
            # Show hint for current stage if it's not the tower hub
            self.show_hint()
        # On entering any stage, save progress
        self.save_progress()
        
        # Find the player sprite's position in current map, and offset all sprites make it the center of attention.
        initial_offset_x = (WIN_WIDTH // 2) - self.player.rect.centerx
        initial_offset_y = (WIN_HEIGHT // 2) - self.player.rect.centery
        for sprite in self.all_sprites:
            sprite.rect.x += initial_offset_x
            sprite.rect.y += initial_offset_y    

    # Game loop events, e.g. clicks and keyboard presses
    def events(self):
        for event in pygame.event.get():
            # If the quit button has been pressed, stop the game
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                return
            
            # If a keyboard key has been pressed and game was paused
            elif event.type == pygame.KEYDOWN and self.paused and not self.player.is_dead:
                if event.key == pygame.K_ESCAPE: # If Esc is pressed, unpause
                    self.paused = False
                    self.sfxs['unpause'].play()
            # If a keyboard key has been pressed and game was unpaused
            elif event.type == pygame.KEYDOWN and not self.paused and not self.player.is_dead:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    self.sfxs['pause'].play()
                # If Space or Z has been pressed, perform normal attack, with position of animation changing depending on player facing
                elif event.key == pygame.K_z and not self.player.is_shielded and not self.player.is_dead:
                    factor = 1
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE*factor)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE*factor)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE*factor, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE*factor, self.player.rect.y)
                    self.player.is_attacking = True
                # If X has been pressed, cast fireball if player has enough mana
                elif event.key == pygame.K_x and not self.player.is_shielded and not self.player.is_dead:
                    if self.player.mana >= FIREBALL_MANA_COST:
                        if self.player.facing == 'up':
                            Fireball(self, self.player.rect.x, self.player.rect.y - TILESIZE, self.player.facing)
                        if self.player.facing == 'down':
                            Fireball(self, self.player.rect.x, self.player.rect.y + TILESIZE, self.player.facing)
                        if self.player.facing == 'left':
                            Fireball(self, self.player.rect.x - TILESIZE, self.player.rect.y, self.player.facing)
                        if self.player.facing == 'right':
                            Fireball(self, self.player.rect.x + TILESIZE, self.player.rect.y, self.player.facing)
                        self.player.mana -= FIREBALL_MANA_COST
                        self.player.is_attacking = True
                # If C has been pressed, cast explosion if player has enough mana
                elif event.key == pygame.K_c and not self.player.is_shielded and not self.player.is_dead:
                    if self.player.mana >= EXPLOSION_MANA_COST:
                        if self.player.facing == 'up':
                            Explosion(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        if self.player.facing == 'down':
                            Explosion(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        if self.player.facing == 'left':
                            Explosion(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                        if self.player.facing == 'right':
                            Explosion(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                        self.player.mana -= EXPLOSION_MANA_COST
                        self.player.is_attacking = True
                # If Space has been pressed, teleport
                elif event.key == pygame.K_SPACE and not self.player.teleporting and not self.player.is_dead:
                    self.player.teleport()
                # If A has been pressed, Barrier/Shield is deployed and stays up until the button is unpressed. No attacks can be performed while shielded.
                elif event.key == pygame.K_a and not self.player.is_dead:
                    self.player.is_shielded = True
                    self.sfxs['barrier'].play()
                # If Esc has been pressed, Pause/Unpause the game
                elif event.key == pygame.K_ESCAPE and not self.player.is_dead:
                    if self.paused:
                        self.paused == False
                        self.sfxs['unpause'].play()
                    else:
                        self.paused == True
                        self.sfxs['pause'].play()
            else:
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    self.player.is_shielded = False


    # Updates to game's values as events trigger
    def update(self):
        if not self.paused:
            # find update method in each sprite in the group "all_sprites" and run it
            self.all_sprites.update()
        if self.player.stage_changed:
            current_stage = self.player.current_stage
            self.player.stage_changed = False
            curr_player = self.player
            # Remove all sprites from all groups before transitioning
            for sprite in self.all_sprites:
                sprite.kill()
            # Clear screen and update the display to remove old sprites
            self.screen.fill(BLACK)
            pygame.display.flip() 
            # Proceed to the stage
            self.loading_screen(current_stage, curr_player)

    # Draw/display sprites in response to events and updates
    def draw(self):
        self.screen.fill(BLACK)
        # go through each sprite in the group "all_sprites", finds image and rect, and draws that unto the window
        self.all_sprites.draw(self.screen)
        # Draw the player's health bar
        self.player.draw_health_bar()
        # Draw the player's mana bar
        self.player.draw_mana_bar()
        # Draw enemy health bars if visible
        for enemy in self.enemies:
            if enemy.health_bar_visible:
                enemy.draw_health_bar()
        # tick the framerate clock according to the fps in the config file
        self.clock.tick(FPS)
        # If the game is currently paused, draw a "PAUSED" text on screen
        if self.paused:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Black with 150 alpha (out of 255)
            self.screen.blit(overlay, (0, 0))

            # If the pause is from the hint screen, show that, otherwise do a normal pause and show text
            if self.showing_hint:
                if self.player.current_stage != 0:
                    self.hint_screen(STAGE_HINTS[self.player.current_stage])
            else:
                # Draw "PAUSED" text with black stroke and white fill
                pause_text_stroke = self.font.render("PAUSED", True, BLACK)
                pause_text = self.font.render("PAUSED", True, WHITE)

                # Center the text
                text_rect_stroke = pause_text_stroke.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
                text_rect = pause_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

                # Draw the stroke and then the main text
                self.screen.blit(pause_text_stroke, (text_rect_stroke.x - 2, text_rect_stroke.y - 2))
                self.screen.blit(pause_text_stroke, (text_rect_stroke.x + 2, text_rect_stroke.y - 2))
                self.screen.blit(pause_text_stroke, (text_rect_stroke.x - 2, text_rect_stroke.y + 2))
                self.screen.blit(pause_text_stroke, (text_rect_stroke.x + 2, text_rect_stroke.y + 2))
                self.screen.blit(pause_text, text_rect)
        # finally, update the screen with the changes
        pygame.display.update()
        
    def main(self):
        # Main loop of the game, where we keep track of various things
        while self.playing:                
            self.events()          
            self.update()
            self.draw()     

    # Used to wrap text into the width of a window
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if current_line == "":
                current_line = word
            elif font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def show_hint(self):
        # Show a hint for current stage if it hasn't been shown yet
        if self.player.current_stage in STAGE_HINTS.keys():
            self.paused = True
            self.showing_hint = True

    def hint_screen(self, message: str):
        #self.draw() # Draw the game first so the overlay is on top

        window_width = 450
        window_height = 200
        window_x = (WIN_WIDTH - window_width) // 2
        window_y = (WIN_HEIGHT - window_height) // 2
        window_rect = pygame.Rect(window_x, window_y, window_width, window_height)

        text_width = window_width - 40 # 20px padding on each side

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    self.paused = False
                    self.showing_hint = False
                    self.hint_not_shown = False
                    return
                # If any button is pressed, navigate away from hint window and unpause
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.paused = False
                    self.showing_hint = False
                    self.hint_not_shown = False
                    return

            # Draw the window with a purple background and pink border
            pygame.draw.rect(self.screen, PURPLE, window_rect)
            pygame.draw.rect(self.screen, PINK, window_rect, 4)

            # Render and display the wrapped text
            wrapped_lines = self.wrap_text(message, self.font, text_width)
            total_text_height = len(wrapped_lines) * 40 # 40px line height

            y_offset = window_y + (window_height - total_text_height) // 2
            for line in wrapped_lines:
                text_surface = self.font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIN_WIDTH // 2, y_offset))
                
                # Draw text with a black stroke
                stroke_surface = self.font.render(line, True, BLACK)
                self.screen.blit(stroke_surface, (text_rect.x - 2, text_rect.y - 2))
                self.screen.blit(stroke_surface, (text_rect.x + 2, text_rect.y - 2))
                self.screen.blit(stroke_surface, (text_rect.x - 2, text_rect.y + 2))
                self.screen.blit(stroke_surface, (text_rect.x + 2, text_rect.y + 2))
                
                self.screen.blit(text_surface, text_rect)
                y_offset += 40

            pygame.display.flip()
            self.clock.tick(FPS) 

    def game_over(self):
        if self.player.is_dead: 
            curr_player = self.player
            self.screen.fill(BLACK)
            for sprite in self.all_sprites:
                sprite.kill() # Remove all sprites on gameover 
            
            # Stop game music and play game over music
            pygame.mixer.music.stop()
            pygame.mixer.music.load(GAMEOVER_MUSIC)
            pygame.mixer.music.play(-1)

            # Game Over screen visuals and its button
            self.screen.blit(self.game_over_background, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            
            while self.running:
                for event in pygame.event.get():
                    # If the 'x' window button is pressed, exit game over and cease running the game
                    if event.type == pygame.QUIT:
                        self.playing = False
                        self.running = False
                    # If a mouse button is clicked, start the game
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.music.stop()
                        self.fade_to_black(FADE_DURATION)
                        # If the restart button is clicked, create a brand new game
                        self.set_stage(self.player.current_stage, curr_player)
                        self.main()           

    # What happens when a stage is cleared.
    def stage_clear(self):
        # Unlock the next stage when current stage is cleared
        if self.player.current_stage == 1:
            self.player.stages_locked[1] = False
        elif self.player.current_stage == 2:
            self.player.stages_locked[2] = False
        elif self.player.current_stage == 3:
            self.player.stages_locked[3] = False
        elif self.player.current_stage == 4:
            self.player.stages_locked[4] = False
        # Win the game if stage 5 is cleared.
        elif self.player.current_stage == 5:
            self.player.all_clear = True
        
        # Load normal loading screen on clearing a stage, or credits after clearing all
        if not self.player.all_clear:
            self.loading_screen(0, self.player)
        else:

            self.credits_screen()
    
    # A pop-up window that displays the game's control scheme upon first starting it.
    def controls_window(self):
        self.paused = True

        # Window height and width
        window_width = 350
        window_height = 450
        # Window x and y positions on screen
        window_x = (WIN_WIDTH - window_width) // 2
        window_y = (WIN_HEIGHT - window_height) // 2
        window_rect = pygame.Rect(window_x, window_y, window_width, window_height)
        last_swap_time = pygame.time.get_ticks()
        current_image = self.controls_image

        # Main loop for the controls window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.paused = False
                    return # Exit the window when any key is pressed or mouse is clicked
                
            # Swap the clicked and normal version of the image every 1 second (for animation)
            if pygame.time.get_ticks() - last_swap_time > 500:
                last_swap_time = pygame.time.get_ticks()
                if current_image == self.controls_image:
                    current_image = self.controls_clicked_image
                else:
                    current_image = self.controls_image

            # Draw the window
            pygame.draw.rect(self.screen, PURPLE, window_rect) # Dark purple background
            pygame.draw.rect(self.screen, PINK, window_rect, 4) # Thick pink border

            # Draw the image in the center of the window
            image_rect = self.controls_image.get_rect(center=window_rect.center)
            self.screen.blit(current_image, image_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    # Helps with smooth transition between screens by fading to black. 
    def fade_to_black(self, duration: int):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration:
            # Alpha controls the opaqueness of the color pixels
            alpha = int(255 * (pygame.time.get_ticks() - start_time) / duration)
            fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)
        self.screen.fill(BLACK)
    
    # Helps with smooth transition between screens by fading back from black. 
    def fade_from_black(self, duration: int, background_surface: pygame.Surface):
        self.screen.fill(BLACK)
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration:
            alpha = int(255 * (1 - (pygame.time.get_ticks() - start_time) / duration))
            fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(alpha)
            self.screen.blit(background_surface, (0,0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

    # Studio logo splash screen
    def splash_screen(self):
        self.screen.fill(BLACK)
        pygame.display.update()
        
        # Fade the logo in
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < FADE_DURATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # Check for a mouse click to skip the screen
                    self.fade_to_black(FADE_DURATION)
                    return
            # Alpha controls the opaqueness of the color pixels
            alpha = int(255 * (pygame.time.get_ticks() - start_time) / FADE_DURATION)
            self.studio_logo.set_alpha(alpha)
            logo_rect = self.studio_logo.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
            self.screen.fill(BLACK)
            self.screen.blit(self.studio_logo, logo_rect)
            pygame.display.update()
            self.clock.tick(FPS)
            
        self.sfxs['logo_chime'].play()

        # Hold the logo on screen for the duration
        time.sleep(SPLASH_SCREEN_DURATION / 1000)
        
        # Fade out logo
        self.fade_to_black(FADE_DURATION)

    # Scrolling text intro screen
    def intro_screen(self):
        self.fade_from_black(FADE_DURATION, self.intro_background)

        # Play the background music
        pygame.mixer.music.load(MUSIC_STORY)
        pygame.mixer.music.play(-1) 

        start_time = pygame.time.get_ticks()
        text_y_offset = WIN_HEIGHT # Start the text off the bottom of the screen
        last_line_index = len(STORY) - 1 # We use this to know when to stop scrolling

        is_holding_mouse = False
        mouse_down_time = 0
        
        # While within the duration of the text scroll, check for events
        while pygame.time.get_ticks() - start_time < SCROLLING_TEXT_DURATION:
            current_tme = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    return
                else: 
                    # Check for a mouse or key click to skip the screen
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # Check for a mouse or key click to skip the screen
                        is_holding_mouse = True
                        mouse_down_time = current_tme
                    # Check for a quick click to skip
                    if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                        is_holding_mouse = False        
                        if current_tme - mouse_down_time < SKIP_THRESHOLD_MS:
                            pygame.mixer.music.stop()
                            self.fade_to_black(FADE_DURATION)
                            return

            # Draw intro_background img 
            self.screen.blit(self.intro_background, (0, 0))

            # Apply semi-transparent overlay
            self.screen.blit(self.overlay_surface, (0, 0))

            # Draw the instruction text at the top right corner
            skip_text = self.font.render("Press any key to skip, hold to scroll", True, WHITE)
            skip_text_rect = skip_text.get_rect(topright=(WIN_WIDTH - 10, 10))
            self.screen.blit(skip_text, skip_text_rect)
            
            # Update the text position to create scrolling effect
            current_speed = SCROLLING_TEXT_SPEED_FAST if is_holding_mouse else SCROLLING_TEXT_SPEED
            text_y_offset -= current_speed

            # For each line in the story
            for i, line in enumerate(STORY):
                # Render the text with a white color
                text_surface = self.font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIN_WIDTH / 2, text_y_offset + (i * 40)))
                
                # Draw the text black border by drawing a slightly offset black text surface
                outline_surface = self.font.render(line, True, BLACK)
                self.screen.blit(outline_surface, (text_rect.x - TEXT_BORDER_THICKNESS, text_rect.y - TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x + TEXT_BORDER_THICKNESS, text_rect.y - TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x - TEXT_BORDER_THICKNESS, text_rect.y + TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x + TEXT_BORDER_THICKNESS, text_rect.y + TEXT_BORDER_THICKNESS))
                self.screen.blit(text_surface, text_rect)

            # Check if the last line of text has reached the center of the screen
            if text_y_offset + (last_line_index * 40) <= WIN_HEIGHT / 2:
                # Keep the final text on screen for a moment
                time.sleep(5)
                pygame.mixer.music.stop()
                self.fade_to_black(FADE_DURATION)
                return  
            pygame.display.update()
            self.clock.tick(FPS)
            
        pygame.mixer.music.stop()
        self.fade_to_black(FADE_DURATION)
    
    # Scrolling text credits screen
    def credits_screen(self):
        pygame.mixer.music.stop()
        # Play the background music
        pygame.mixer.music.load(MUSIC_CREDITS)
        pygame.mixer.music.play(-1) 
        self.fade_from_black(FADE_DURATION, self.credits_background)
        
        start_time = pygame.time.get_ticks()
        text_y_offset = WIN_HEIGHT # Start the text off the bottom of the screen
        last_line_index = len(CREDITS) - 1 # We use this to know when to stop scrolling

        is_holding_mouse = False
        mouse_down_time = 0
        
        # While within the duration of the text scroll, check for events
        while pygame.time.get_ticks() - start_time < SCROLLING_TEXT_DURATION:
            current_tme = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    return
                else: 
                    # Check for a mouse or key click to skip the screen
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # Check for a mouse or key click to skip the screen
                        is_holding_mouse = True
                        mouse_down_time = current_tme
                    # Check for a quick click to skip
                    if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                        is_holding_mouse = False        
                        if current_tme - mouse_down_time < SKIP_THRESHOLD_MS:
                            pygame.mixer.music.stop()
                            self.fade_to_black(FADE_DURATION)
                            self.loading_screen(-1, self.player)
                            return

            # Draw intro_background img 
            self.screen.blit(self.credits_background, (0, 0))

            # Apply semi-transparent overlay
            self.screen.blit(self.overlay_surface, (0, 0))

            # Draw the instruction text at the top right corner
            skip_text = self.font.render("Press any key to skip, hold to scroll", True, WHITE)
            skip_text_rect = skip_text.get_rect(topright=(WIN_WIDTH - 10, 10))
            self.screen.blit(skip_text, skip_text_rect)
            
            # Update the text position to create scrolling effect
            current_speed = SCROLLING_TEXT_SPEED_FAST if is_holding_mouse else SCROLLING_TEXT_SPEED
            text_y_offset -= current_speed

            # For each line in the story
            for i, line in enumerate(CREDITS):
                # Render the text with a white color
                text_surface = self.font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIN_WIDTH / 2, text_y_offset + (i * 40)))
                
                # Draw the text black border by drawing a slightly offset black text surface
                outline_surface = self.font.render(line, True, BLACK)
                self.screen.blit(outline_surface, (text_rect.x - TEXT_BORDER_THICKNESS, text_rect.y - TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x + TEXT_BORDER_THICKNESS, text_rect.y - TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x - TEXT_BORDER_THICKNESS, text_rect.y + TEXT_BORDER_THICKNESS))
                self.screen.blit(outline_surface, (text_rect.x + TEXT_BORDER_THICKNESS, text_rect.y + TEXT_BORDER_THICKNESS))
                self.screen.blit(text_surface, text_rect)

            # Check if the last line of text has reached the center of the screen
            if text_y_offset + (last_line_index * 40) <= WIN_HEIGHT / 2:
                # Keep the final text on screen for a moment
                time.sleep(5)
                pygame.mixer.music.stop()
                self.fade_to_black(FADE_DURATION)
                return  
            pygame.display.update()
            self.clock.tick(FPS)
            
        pygame.mixer.music.stop()
        self.fade_to_black(FADE_DURATION)
        self.loading_screen(-1, self.player)

    # The start-up menu screen, displaying the game logo
    def menu_screen(self):
        intro = True
        self.fade_from_black(FADE_DURATION, self.menu_background)
        
        # Load and play the intro music
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1) # -1 for music loop

        # While on the intro screen, do the following. Otherwise, move on to the actual game.
        while intro:
            # If the 'x' window button is pressed, exit intro and cease running the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.playing = False
                    self.running = False
                # If a mouse or key button is clicked, start the game
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    intro = False
                    pygame.mixer.music.stop()
                    self.fade_to_black(FADE_DURATION)
                    self.controls_window()
            
            # Intro screen visuals and its button
            self.screen.blit(self.menu_background, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
    # The loading screen, when transitioning between stages/screens
    def loading_screen(self, stage_num: int, curr_player: int):
        pygame.mixer.music.stop() # stop all music
        self.fade_to_black(FADE_DURATION)
        
        # When entering a new stage, show the loading screen and set the stage depending on stage num.
        if stage_num == 1:
            self.fade_from_black(FADE_DURATION, self.loading_1_image)
            self.screen.blit(self.loading_1_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(1)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(1, curr_player)
        elif stage_num == 2:
            self.fade_from_black(FADE_DURATION, self.loading_2_image)
            self.screen.blit(self.loading_2_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(1)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(2, curr_player)
        elif stage_num == 3:
            self.fade_from_black(FADE_DURATION, self.loading_3_image)
            self.screen.blit(self.loading_3_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(1)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(3, curr_player)
        elif stage_num == 4:
            self.fade_from_black(FADE_DURATION, self.loading_4_image)
            self.screen.blit(self.loading_4_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(1)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(4, curr_player)
        elif stage_num == 5:
            self.fade_from_black(FADE_DURATION, self.loading_5_image)
            self.screen.blit(self.loading_5_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(1)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(5, curr_player)
        elif stage_num == 0: # Back to Tower hub area
            self.sfxs['victory'].play()
            self.fade_from_black(FADE_DURATION, self.victory_image)
            self.screen.blit(self.victory_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()
            time.sleep(6)
            self.fade_to_black(FADE_DURATION)
            self.set_stage(0, curr_player)
        elif stage_num == -1: # all stages cleared
            self.sfxs['victory'].play()
            on_clear_screen = True
            self.fade_from_black(FADE_DURATION, self.clear_image)
            self.screen.blit(self.clear_image, (0,0))
            self.clock.tick(FPS)
            pygame.display.update()

            while on_clear_screen:
                # If the 'x' window button is pressed, exit intro and cease running the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        on_clear_screen = False
                        self.playing = False
                        self.running = False
                    # If a mouse button is clicked, start the game
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        on_clear_screen = False
                        self.fade_to_black(FADE_DURATION)
                        self.splash_screen()
                        self.intro_screen()
                        self.menu_screen()
                        g.set_stage(0)
    # Saves the progress of the current player locally upon clearing a stage.
    def save_progress(self):
        # Store progress as a dict
        player_data = {
            "stages_locked": self.player.stages_locked,
            "health": self.player.health,
            "mana": self.player.mana,
            "all_open": self.player.all_open,
            "all_clear": self.player.all_clear,
            "current_stage": self.player.current_stage,
        }
        # Save progress to a JSON file
        with open(SAVE_FILEPATH, 'w') as file:
            json.dump(player_data, file, indent=4)

    # Load the progress of the current player upon boot up, if a save file exists.
    def load_progress(self):
        # Try to find the file and read data from it: if successful, copy the progress to the current game's player.
        try:
            with open(SAVE_FILEPATH, 'r') as file:
                # Load player progress data from the JSON file
                player_data = json.load(file)

                # Copy it to current player
                self.player.stages_locked = player_data.get("stages_locked", self.player.stages_locked)
        except FileNotFoundError:
            # Couldn't find save file due to either being deleted or not existing yet, start game with initialized values
            print("Failed to find player save. Starting game with initialized values.")
        except json.JSONDecodeError:
            # File was corrupted, raise exception and prompt user to delete the file or replace it with a valid one before restarting the game.
            raise Exception("Crticial Error: Failed to load player data due to file corruption. Please delete your save file, or replace it with a valid one.")

# Main code where the game runs, triggers when running main.py
if __name__ == "__main__":
    g = Game()

    g.splash_screen()
    g.intro_screen()
    g.menu_screen()

    g.set_stage(0)
    # While the game is running, run the main game loop, and if that loop ends, run the gameover method.
    while g.running:
        g.main()
        g.game_over()
    # Once out of the main game loop, quit program.
    pygame.quit()
    sys.exit()  
