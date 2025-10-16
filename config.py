# This file will contain all settings and configurations of the game, including classes and variables

###############
#   Settings    #
###############

# General
WIN_WIDTH = 640
WIN_HEIGHT = 480
SMALL_WIN_WIDTH = 400
SMALL_WIN_HEIGHT = 300
TILESIZE = 32
BTN_FONT_SIZE = 18
FPS = 60
FADE_DURATION = 1500  # Fade duration in milliseconds
SPLASH_SCREEN_DURATION = 3000  # How long the logo stays on screen (3 seconds max)
SCROLLING_TEXT_DURATION = 100000  # How long the scrolling text screen lasts (100 secs max)
SCROLLING_TEXT_SPEED = 0.3
SCROLLING_TEXT_SPEED_FAST = 1.5
SKIP_THRESHOLD_MS = 200 # Time in milliseconds to distinguish a click from a hold
TEXT_BORDER_THICKNESS = 2
GROUND_LAYER = 0
BLOCK_LAYER = 1
ENEMY_LAYER = 2
PLAYER_LAYER = 3

# Texts and Saves
SAVE_FILEPATH = "./assets/saves/save.json"
STAGE_HINTS = {
            1: "Find and hit (Z) all switches to open the door leading to the crystal. Look out for enemies!",
            2: "Brrr! It's c-c-cold! By the way, your spells are for more than just defeating enemies. Did you know fire (X) melts ice? Watch out for slippery floors!",
            3: "Phew! Hot here, isn't it? Lava's not good for your skin. Maybe there is a way to travel the SPACE across lava without falling in?",
            4: "Watch out, that temple is full of deadly miasma! Try using your barrier (A) to protect yourself. You can hit switches from afar using the Fire Spell (X).",
            5: "Your last challenge: The Orcs Guantlet! There are no switches here, defeat powerful enemies while heading to the door. Good luck!"
        }
STORY = [
            "In a world where magic is fading,",
            "you, a young squire, are tasked with a critical quest:",
            "to collect five ancient crystals.", 
            "These crystals, scattered across the land,",
            "are believed to be the key to restoring magic to the world.",
            "",
            "Your journey begins in your master's study,", 
            "his sanctuary at the top of the grand tower.",
            "Within are five mystical portals. Four are locked,",
            "but one awaits your first step into the unknown.",
            "",
            "Each portal leads to a crystal, held and guarded",
            "by powerful foes. It is a long and perilous journey,",
            "but the fate of the world rests on your success. When",
            "the fifth crystal collected, magic will return",
            "to the world. A new age of wonder will begin.",
            "", 
            "Go forth, and begin your quest!"
        ]

# Credits Text 
CREDITS = [
    "THE GREAT RESTORATION IS COMPLETE.",
    "",
    "Through five mystical portals,",
    "you bravely faced powerful foes and retrieved the ancient crystals.",
    "",
    "The five crystals and are together at last.",
    "The fading light of the world has surged into a brilliant dawn.",
    "",
    "Magic is restored.",
    "The age of scarcity is over. A new age of wonder begins now,",
    "paved by the courage and will of a single, young squire.",
    "",
    "Your name will be the first legend spoken of in this glorious era.",
    "",
    "====================================",
    "",
    "A PYQREN PRODUCTION",
    "Developed by Abdullah Al Miqren",
    "",
    "FONTS", 
    "DaFont",
    "",
    "SPRITESHEETS", 
    "itch.io",
    "Craftpix ",
    "Rappenem",
    "ArtisticCarCras",
    "",
    "BG IMAGES",
    "BrandCrowd",
    "InPrnt",
    "ChatGPT"
    "",
    "MUSIC",
    "Fesliyan Studios",
    "Pixabay ",
    "",
    "THANK YOU FOR PLAYING!",
    "",
    "THE END."
]

# Gameplay Stats
PLAYER_HP = 100
PLAYER_IFRAME_TIME = 3000 # 3 seconds
PLAYER_MAX_MANA = 100
MANA_DRAIN_RATE = 0.2
MANA_HEAL_RATE = 0.05
FIREBALL_MANA_COST = 20
EXPLOSION_MANA_COST = 35
SLASH_MANA_RESTORE = 5
ATTACK_DAMAGE = 25
FIREBALL_DAMAGE = 25
EXPLOSION_DAMAGE = 50
SMALL_FIREBALL_DAMAGE = 10
ENEMY_HP = 50
ELITE_ENEMY_HP = 100
ENEMY_COLLISION_DAMAGE = 25
ENEMY_HIT_DAMAGE = 25
MIASAMA_DAMAGE = 10
ENEMY_IFRAME_TIME = 1000   # 1 second
ENEMY_AGGRO_DISTANCE = 4 * TILESIZE
PLAYER_SPEED = 3
PLAYER_SPEED_BOOSTED = 6
PLAYER_SPEED_SLIDING = 8
ENEMY_SPEED = 1
FIREBALL_SPEED = 5
ATTACK_FRAME_LIMIT = 5
FIREBALL_FRAME_INCREMENT = 0.5
FIREBALL_FRAME_LIMIT = 4
PORTAL_FRAME_LIMIT = 8
DOOR_FRAME_LIMIT = 5
BLOCK_SCALE= 32
HOLE_SCALE= 30
DOOR_SCALE= 30
PLAYER_SCALE = 45
CHARACTER_SCALE = 1.5
ELITE_MODIFIER = 2
SLIME_SCALE = 25
VAMPIRE_SCALE = 35
ORC_SCALE = 30
ORC_SCALE_MODIFIER = 10
ORC_SCALE_ELITE = 30 * ELITE_MODIFIER
ORC_SCALE_MODIFIER_ELITE = 10 * ELITE_MODIFIER
FIREBALL_SCALE= 15
EXPLOSION_SCALE= 20
SWITCH_SCALE= 20
TELEPORT_SPEED = 9
TELEPORT_DISTANCE = 4 * TILESIZE
TELEPORT_DURATION = 15

# Colors
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (26, 79, 24)
GOLD = (141, 145, 9)
PINK = (143, 90, 242)
PURPLE = (10, 2, 26)

###############
#   assets    #
###############

# Fonts
MINECRAFTIA = './assets/fonts/Minecraft.ttf' # Pixel
MINECRAFTIA_REGULAR = './assets/fonts/Minecraftia_Regular.ttf' # Pixel
DAYDREAM = './assets/fonts/Daydream.otf' # Cartoony
PLANES_VALMORE = './assets/fonts/Planes_ValMore.ttf'
PIXELMAX = './assets/fonts/Pixelmax-Regular.otf'

# Images
STUDIO_LOGO_IMAGE = './assets/img/logo.png'
INTRO_IMAGE = './assets/img/tower.png'
CREDITS_IMAGE = './assets/img/credits.png'
MENU = './assets/img/main_menu.png'
GAMEOVER = './assets/img/gameover.png'
CONTROLS = './assets/img/icons/controls.png'
CONTROLS_CLICKED = './assets/img/icons/controls_clicked.png'
LOADING_1 = './assets/img/icons/Loading_1.png'
LOADING_2 = './assets/img/icons/Loading_2.png'
LOADING_3 = './assets/img/icons/Loading_3.png'
LOADING_4 = './assets/img/icons/Loading_4.png'
LOADING_5 = './assets/img/icons/Loading_5.png'
VICTORY = './assets/img/icons/victory.png'
CLEAR = './assets/img/icons/clear.png'

# Music and sound effects
MUSIC_STORY = './assets/sound/music/story.mp3'
MUSIC_CREDITS = './assets/sound/music/credits.mp3'
MENU_MUSIC = './assets/sound/music/intro.mp3'
TOWER_MUSIC = './assets/sound/music/tower.mp3'
STAGE_1_MUSIC = './assets/sound/music/stage_1.mp3'
STAGE_2_MUSIC = './assets/sound/music/stage_2.mp3'
STAGE_3_MUSIC = './assets/sound/music/stage_3.mp3'
STAGE_4_MUSIC = './assets/sound/music/stage_4.mp3'
STAGE_5_MUSIC = './assets/sound/music/stage_5.mp3'
GAMEOVER_MUSIC = './assets/sound/music/game_over.mp3'
FINALE_MUSIC = './assets/sound/music/finale.mp3'
CHIME_SFX = './assets/sound/sfx/logo.mp3'
BARRIER_SFX = './assets/sound/sfx/barrier.mp3'
SWITCH_HIT_SFX = './assets/sound/sfx/switch_hit.mp3'
SWITCH_OPEN_ALL_SFX ='./assets/sound/sfx/opened_all_switches.mp3' 
VICTORY_SFX = './assets/sound/sfx/victory.mp3'
PAUSE_SFX = './assets/sound/sfx/pause.mp3'
UNPAUSE_SFX = './assets/sound/sfx/unpause.mp3'
ATTACK_SFX = './assets/sound/sfx/hit.wav'
FIREBALL_SFX = './assets/sound/sfx/fireball.wav'
PLAYER_HIT_SFX = './assets/sound/sfx/player_hit.wav'
PLAYER_DEATH_SFX = './assets/sound/sfx/destroy_player.wav'
ENEMY_HIT_SFX = './assets/sound/sfx/enemy_hit.wav'
ENEMY_DEATH_SFX = './assets/sound/sfx/destroy_enemy.wav'
FIREBALL_IMPACT_SFX = './assets/sound/sfx/fireball_hit.wav'
EXPLOSION_SFX = './assets/sound/sfx/explosion.wav'
SMALL_FIREBALL_SFX = './assets/sound/sfx/fireball_hit.wav'
MUSIC_VOLUME = 0.5 # between 0 and 1
SFX_VOLUME = 0.5 # between 0 and 1

# Objects
TERRAIN_SPRITE = './assets/img/terrain.png'
ICE_CUBE_SPRITE = './assets/img/ice_cube.PNG'
SWITCH_SPRITE = './assets/img/lever.png'
DOOR_SPRITE = './assets/img/Door_Open.png'
PORTAL_SPRITE = './assets/img/Portal.png'
PORTAL_LOCKED_SPRITE = './assets/img/Portal_locked.png'
MIASMA_SPRITE = './assets/img/miasma.png'

# Player
PLAYER_WALK_SPRITE = './assets/img/player/movement.png'
PLAYER_TELEPORT_SPRITE = './assets/img/player/teleport.png'
PLAYER_BARRIER_SPRITE = './assets/img/player/barrier.png'
PLAYER_DEATH_SPRITE = './assets/img/player/death.png'
PLAYER_HURT_SPRITE = './assets/img/player/hurt.png'
PLAYER_ATTACK_SPRITE = './assets/img/attack.png'
CHARACTER_ATTACK_SPRITE = './assets/img/player/attack.png'
PLAYER_FIREBALL_SPRITE = './assets/img/fireball.png'
PLAYER_EXPLOSION_SPRITE = './assets/img/fireball.png'

# Enemies
GREEN_SLIME_WALK_SPRITE = './assets/img/enemies/slime_green/walk/body.png'
RED_SLIME_WALK_SPRITE = './assets/img/enemies/slime_red/walk/body.png'
BLUE_SLIME_WALK_SPRITE = './assets/img/enemies/slime_blue/walk/body.png'
VAMPIRE_WALK_SPRITE = './assets/img/enemies/vampire/walk/body.png'
ORC_WALK_SPRITE = './assets/img/enemies/orc/walk/body.png'

# The following section contains grid-based tilemaps that allow us to 'draw' the various stages of our game.
tower_hub = (
    'WWWWWWWWWWWWWWWWWWWW',
    'W..................W',
    'W.........3........W',
    'W..................W',
    'W......2.....4.....W',
    'W.........V........W',
    'W....1.........5...W',
    'W.........P........W',
    'W..................W',
    'W..................W',
    'W..................W',
    'W..................W',
    'W..................W',
    'W..................W',
    'WWWWWWWWWWWWWWWWWWWW',
)

tilemap1 = (
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W.......................................W',
    'W............_____________..............W',
    'W............___.......___..............W',
    'W............___...D...___..............W',
    'W............___.......___..............W',
    'W............_____________..............W',
    'W.......................................W',
    'W.......................................W',
    'W.......................................W',
    'WWWWWWWWWWWWWWWWWWBBB..BBBBWWWWWWWWWWWWWW',
    'W.......................................W',
    'W..................S....................W',
    'W.......................................W',
    'W................E.......E.........E....W',
    'W.......................................W',
    'W.......................................W',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWBBBB..BBBWWW',
    'W.......................................W',
    'W.............E............S............W',
    'W.......................................W',
    'W.......................................W',
    'WWWWWWWBBB..BBBBWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W.......................................W',
    'W...................P...S...............W',
    'W........E..............................W',
    'WWWWWWWWWWWWWWWBBBB..BBBWWWWWWWWWWWWWWWWW',
    'W.......................................W',
    'W.......................................W',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
)

tilemap2 = (
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W-------------------D------------------W',
    'W--------------------------------------W',
    'W-----WWWWWWW-------------E------------W',
    'W-----=..S..=--------------------------W',
    'W-----=.....=--------------------------W',
    'W-----=======--------------------------W',
    'W-----------E--------------BBBBB-------W',
    'W----E-----------------B---------------W',
    'W--------------------------------------W',
    'W--------BBBBB-------------------------W',
    'W--------------------------------------W',
    'W--------------------------------------W',
    'W--------------------------------------W',
    'W----------WWWWW-------WWWWWWW---------W',
    'W----------=.S.=-------=..S..=---------W',
    'W----------=...=-------=.....=---------W',
    'W----------=====-------=======---------W',
    'W------------------E-------------------W',
    'W----------------BBBBB-----E-----------W',
    'W--------------------------------------W',
    'W--------------E-----------------------W',
    'W--------------------------------------W',
    'WWWWWWWWWWWWWWW.........WWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWW.........WWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWW....P....WWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWW.........WWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWW.........WWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
)

tilemap3 = (
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W--------.........D.........-----------W',
    'W----------...............-------------W',
    'W------------...........---------------W',
    'W--------------.......-----------------W',
    'W----------------...-------------------W',
    'W----------------HHH-------------------W',
    'W----------------...-------------------W',
    'W-----------.............--------------W',
    'W........H...................H.........W',
    'WS...E...H...................H....E...SW',
    'W........H...................H.........W',
    'W-----------.............--------------W',
    'W----------------...-------------------W',
    'W----------------HHH-------------------W',
    'W----------------...-------------------W',
    'W-----------.............--------------W',
    'W......................................W',
    'WS......E.......................E.....SW',
    'W......................................W',
    'W-----------.............--------------W',
    'W----------------...-------------------W',
    'W----------------HHH-------------------W',
    'W----------------...-------------------W',
    'W-----------.............--------------W',
    'W-----------.............--------------W',
    'W-----------......P......--------------W',
    'W-----------.............--------------W',
    'W-----------.............--------------W',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
)

tilemap4 = (
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'W=====================================W',
    'WWWWWWWWW=============================W',
    'W......HH..=====================WWWWWWW',
    'WD.....HH..===E=================..----W',
    'W......HH..=================E===..---SW',
    'WWWWWWWWW=======================..----W',
    'W===============================WWWWWWW',
    'W=====================================W',
    'WW====================================W',
    'WWWWWWWW==============================W',
    'W-------..E===========================W',
    'WS------..============================W',
    'W-------..============================W',
    'WWWWWWWW==============================W',
    'WW================E=...===============W',
    'W=================WW...WW=============W',
    'W=================W-----W=============W',
    'W=========E=======W--S--W=============W',
    'W=================W-----W=============W',
    'W=================WWWWWWW=============W',
    'W===========E=================E=======W',
    'W=====================================W',
    'W=====================================W',
    'WWWWWWWWWWWWWWWW.......WWWWWWWWWWWWWWWW',
    'W_____________________________________W',
    'W_____________________________________W',
    'W__________________P__________________W',
    'W_____________________________________W',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
)

tilemap5 = (
"WWWWWWWWWWWWWWDWWWWWWWWWWW",
"W..............WWWWWWW..WW",
"W..............WWWWWWW..WW",
"W...WWWWWWWWWWWWWWWWWW...W",
"W..WWW..WW...............W",
"W..WWW..WW...............W",
"W...........WWW.WWWWWWW..W",
"W.....L......W....W......W",
"W..WWWWW..W..WWW.........W",
"W..WW.W...W...W......W...W",
"W..WW.W...W.WWWWWWWWWW..WW",
"W..W.W.W...W......L......W",
"W..WWWWWWWWW.W...........W",
"W..WW........W...W....W.WW",
"WWWWWWW.....W.W..W.WW.W.WW",
"W.W..W...W..WW....W.W....W",
"W.W......W........W.WWWW.W",
"W.W......W.......W....W.WW",
"W....WWWWW.L.W.W.WW.WW.W.W",
"W......W.W...W.W...W....WW",
"W..WWWW.WWWW.W.WWWWWWW.W.W",
"W..WWW.W..W..W.W....W..W.W",
"W..WWW.W.W.WW.WW...WWWW.WW",
"W.L.WW.W.....WWW...W...W.W",
"W...WW.WWWW.WWWW...WWW.W.W",
"W...W.W.W..........W...W.W",
"W.........L....P...WWWWW.W",
"W...........W...W........W",
"WWWWWWWWWWWWWWWWWWWWWWWWWW"
)

# Define which characters are NOT walkable (obstacles)
NON_WALKABLE_CHARS = {'W', 'D', 'H', '-', 'S', 'B'} 
