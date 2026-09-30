import pygame
import random
import math
import wave
import struct
import os

# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

try:
    pygame.mixer.init()
except:
    pass

WIDTH = 1000
HEIGHT = 650
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival")

clock = pygame.time.Clock()

# Virtual game surface
game_surface = pygame.Surface((WIDTH, HEIGHT))

fullscreen = False


# =========================================================
# COLORS
# =========================================================

BLACK = (8, 8, 10)
WHITE = (245, 245, 245)

GREEN = (60, 220, 80)
DARK_GREEN = (25, 100, 35)

RED = (220, 50, 50)
DARK_RED = (90, 20, 20)

BLUE = (60, 150, 255)
DARK_BLUE = (30, 80, 150)

YELLOW = (255, 220, 50)

ORANGE = (255, 140, 40)

PURPLE = (180, 70, 220)

GRAY = (130, 130, 130)
DARK_GRAY = (30, 32, 35)

CYAN = (60, 230, 230)


# =========================================================
# FONTS
# =========================================================

font_big = pygame.font.Font(None, 72)
font_title = pygame.font.Font(None, 88)
font_medium = pygame.font.Font(None, 44)
font_small = pygame.font.Font(None, 28)
font_tiny = pygame.font.Font(None, 22)


# =========================================================
# SOUND SYSTEM
# =========================================================

SOUND_FOLDER = "zombie_sounds"

if not os.path.exists(SOUND_FOLDER):
    os.makedirs(SOUND_FOLDER)


def create_sound(filename, frequency, duration, volume=0.3):

    path = os.path.join(SOUND_FOLDER, filename)

    if os.path.exists(path):
        return

    sample_rate = 44100
    frames = int(sample_rate * duration)

    data = []

    for i in range(frames):

        t = i / sample_rate

        value = math.sin(
            2 * math.pi * frequency * t
        )

        fade = 1 - (i / frames)

        value *= fade
        value *= volume

        sample = int(value * 32767)

        data.append(
            struct.pack("<h", sample)
        )

    with wave.open(path, "w") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        wav.writeframes(
            b"".join(data)
        )


# Create sounds
create_sound("shoot.wav", 700, 0.07, 0.35)
create_sound("hit.wav", 180, 0.08, 0.25)
create_sound("coin.wav", 900, 0.12, 0.25)
create_sound("power.wav", 500, 0.25, 0.25)
create_sound("damage.wav", 100, 0.15, 0.3)
create_sound("wave.wav", 350, 0.35, 0.25)


def load_sound(filename):

    try:

        return pygame.mixer.Sound(
            os.path.join(
                SOUND_FOLDER,
                filename
            )
        )

    except:

        return None


shoot_sound = load_sound("shoot.wav")
hit_sound = load_sound("hit.wav")
coin_sound = load_sound("coin.wav")
power_sound = load_sound("power.wav")
damage_sound = load_sound("damage.wav")
wave_sound = load_sound("wave.wav")


def play_sound(sound):

    if sound is not None:

        try:
            sound.play()
        except:
            pass


# =========================================================
# DIFFICULTIES
# =========================================================
#
# Important:
# Damage is NOT applied every frame.
# Every zombie has an attack cooldown.
#
# difficulty_growth controls how quickly the game gets harder.
#

DIFFICULTIES = [

    {
        "name": "Easy",
        "color": GREEN,

        # Starting zombies
        "base_zombies": 4,

        # Zombies added every wave
        "wave_zombies": 1.2,

        # Zombie speed
        "speed_multiplier": 0.72,

        # Zombie health
        "health_multiplier": 0.75,

        # Zombie damage
        "damage_multiplier": 0.65,

        # Fast zombie chance
        "fast_chance": 0.10,

        # Strong zombie chance
        "strong_chance": 0.025,

        # How quickly stats increase
        "difficulty_growth": 0.025,

        # Time between zombie attacks
        "attack_cooldown": 75,

        # How much health comes back every wave
        "wave_heal": 12
    },

    {
        "name": "Normal",
        "color": WHITE,

        "base_zombies": 5,

        "wave_zombies": 1.8,

        "speed_multiplier": 0.95,

        "health_multiplier": 0.95,

        "damage_multiplier": 0.90,

        "fast_chance": 0.18,

        "strong_chance": 0.06,

        "difficulty_growth": 0.055,

        "attack_cooldown": 65,

        "wave_heal": 8
    },

    {
        "name": "Hard",
        "color": ORANGE,

        "base_zombies": 6,

        "wave_zombies": 2.2,

        "speed_multiplier": 1.08,

        "health_multiplier": 1.10,

        "damage_multiplier": 1.05,

        "fast_chance": 0.25,

        "strong_chance": 0.10,

        "difficulty_growth": 0.075,

        "attack_cooldown": 55,

        "wave_heal": 6
    },

    {
        "name": "Extreme",
        "color": RED,

        "base_zombies": 7,

        "wave_zombies": 2.8,

        "speed_multiplier": 1.20,

        "health_multiplier": 1.22,

        "damage_multiplier": 1.20,

        "fast_chance": 0.32,

        "strong_chance": 0.15,

        "difficulty_growth": 0.095,

        "attack_cooldown": 48,

        "wave_heal": 4
    },

    {
        "name": "Impossible",
        "color": PURPLE,

        "base_zombies": 8,

        "wave_zombies": 3.3,

        "speed_multiplier": 1.35,

        "health_multiplier": 1.35,

        "damage_multiplier": 1.35,

        "fast_chance": 0.40,

        "strong_chance": 0.22,

        "difficulty_growth": 0.12,

        "attack_cooldown": 42,

        "wave_heal": 2
    }

]


difficulty_index = 0
difficulty = DIFFICULTIES[difficulty_index]


# =========================================================
# PARTICLES
# =========================================================

particles = []


def create_particles(
    x,
    y,
    color,
    amount=10
):

    for _ in range(amount):

        particles.append({

            "x": x,
            "y": y,

            "vx": random.uniform(-3, 3),
            "vy": random.uniform(-3, 3),

            "life": random.randint(15, 30),

            "color": color,

            "size": random.randint(2, 5)

        })


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1

        particle["size"] *= 0.94

        if particle["life"] <= 0:

            particles.remove(particle)


def draw_particles():

    for particle in particles:

        pygame.draw.circle(

            game_surface,

            particle["color"],

            (
                int(particle["x"]),
                int(particle["y"])
            ),

            max(
                1,
                int(particle["size"])
            )
        )


# =========================================================
# PLAYER
# =========================================================

class Player:

    def __init__(self):

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.radius = 18

        self.speed = 5

        self.health = 100
        self.max_health = 100

        self.score = 0

        self.coins = 0

        self.kills = 0

        self.shoot_cooldown = 0

        self.rapid_fire = 0

        self.shield = 0

        self.damage_flash = 0

    def update(self):

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1

        if keys[pygame.K_s]:
            dy += 1

        if keys[pygame.K_a]:
            dx -= 1

        if keys[pygame.K_d]:
            dx += 1

        if dx != 0 or dy != 0:

            length = math.sqrt(
                dx * dx + dy * dy
            )

            dx /= length
            dy /= length

            self.x += dx * self.speed
            self.y += dy * self.speed

        self.x = max(
            self.radius,
            min(
                WIDTH - self.radius,
                self.x
            )
        )

        self.y = max(
            self.radius,
            min(
                HEIGHT - self.radius,
                self.y
            )
        )

        if self.shoot_cooldown > 0:

            self.shoot_cooldown -= 1

        if self.rapid_fire > 0:

            self.rapid_fire -= 1

        if self.shield > 0:

            self.shield -= 1

        if self.damage_flash > 0:

            self.damage_flash -= 1

    def shoot(
        self,
        mouse_x,
        mouse_y
    ):

        if self.shoot_cooldown > 0:

            return

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        if distance == 0:

            return

        dx /= distance
        dy /= distance

        bullets.append(
            Bullet(
                self.x,
                self.y,
                dx,
                dy
            )
        )

        if self.rapid_fire > 0:

            self.shoot_cooldown = 3

        else:

            self.shoot_cooldown = 9

        play_sound(shoot_sound)

    def damage(self, amount):

        # Shield blocks damage
        if self.shield > 0:

            create_particles(
                self.x,
                self.y,
                BLUE,
                5
            )

            return

        self.health -= amount

        self.health = max(
            0,
            self.health
        )

        self.damage_flash = 10

        play_sound(damage_sound)

        create_particles(
            self.x,
            self.y,
            RED,
            12
        )


# =========================================================
# BULLET
# =========================================================

class Bullet:

    def __init__(
        self,
        x,
        y,
        dx,
        dy
    ):

        self.x = x
        self.y = y

        self.dx = dx
        self.dy = dy

        self.speed = 13

        self.radius = 5

        self.damage = 25

    def update(self):

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):

        pygame.draw.circle(

            game_surface,

            YELLOW,

            (
                int(self.x),
                int(self.y)
            ),

            self.radius
        )


# =========================================================
# ZOMBIE
# =========================================================

class Zombie:

    def __init__(self, zombie_type):

        # Spawn outside screen

        side = random.randint(0, 3)

        if side == 0:

            self.x = random.randint(
                0,
                WIDTH
            )

            self.y = -40

        elif side == 1:

            self.x = random.randint(
                0,
                WIDTH
            )

            self.y = HEIGHT + 40

        elif side == 2:

            self.x = -40

            self.y = random.randint(
                0,
                HEIGHT
            )

        else:

            self.x = WIDTH + 40

            self.y = random.randint(
                0,
                HEIGHT
            )

        self.type = zombie_type

        # -------------------------------------------------
        # BASE STATS
        # -------------------------------------------------

        if zombie_type == "normal":

            self.radius = 20

            base_speed = 1.45
            base_health = 50
            base_damage = 8

            self.color = GREEN

        elif zombie_type == "fast":

            self.radius = 15

            base_speed = 2.45
            base_health = 35
            base_damage = 6

            self.color = ORANGE

        else:

            self.radius = 28

            base_speed = 0.75
            base_health = 120
            base_damage = 15

            self.color = PURPLE

        # -------------------------------------------------
        # WAVE GROWTH
        # -------------------------------------------------

        growth = (

            1
            +
            (wave_number - 1)
            *
            difficulty["difficulty_growth"]

        )

        self.speed = (

            base_speed
            *
            difficulty["speed_multiplier"]
            *
            growth

        )

        self.health = int(

            base_health
            *
            difficulty["health_multiplier"]
            *
            growth

        )

        self.damage = max(

            1,

            int(

                base_damage
                *
                difficulty["damage_multiplier"]
                *
                growth

            )

        )

        # -------------------------------------------------
        # ATTACK SYSTEM
        # -------------------------------------------------

        self.attack_cooldown = 0

        # Slightly different cooldown per zombie
        self.attack_delay = max(
            25,
            int(
                difficulty["attack_cooldown"]
                *
                random.uniform(
                    0.85,
                    1.15
                )
            )
        )

        # Prevent instant damage when spawning
        self.attack_cooldown = 20

        self.hit_flash = 0

    def update(self):

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(
            dx * dx + dy * dy
        )

        # Move toward player

        if distance > 0:

            dx /= distance
            dy /= distance

            self.x += dx * self.speed
            self.y += dy * self.speed

        # Attack cooldown

        if self.attack_cooldown > 0:

            self.attack_cooldown -= 1

        # Attack player

        if (

            distance
            <
            self.radius
            +
            player.radius
            +
            3

        ):

            if self.attack_cooldown <= 0:

                player.damage(
                    self.damage
                )

                # THIS IS THE IMPORTANT FIX:
                # Zombie cannot damage every frame.

                self.attack_cooldown = (
                    self.attack_delay
                )

                # Push zombie away

                if distance > 0:

                    push_x = (
                        self.x - player.x
                    ) / distance

                    push_y = (
                        self.y - player.y
                    ) / distance

                    self.x += (
                        push_x * 18
                    )

                    self.y += (
                        push_y * 18
                    )

    def draw(self):

        # Hit flash

        color = self.color

        if self.hit_flash > 0:

            color = WHITE

            self.hit_flash -= 1

        pygame.draw.circle(

            game_surface,

            color,

            (
                int(self.x),
                int(self.y)
            ),

            self.radius
        )

        # Eyes

        eye_offset = max(
            4,
            self.radius // 3
        )

        pygame.draw.circle(

            game_surface,

            WHITE,

            (
                int(
                    self.x - eye_offset
                ),
                int(
                    self.y - eye_offset
                )
            ),

            4
        )

        pygame.draw.circle(

            game_surface,

            WHITE,

            (
                int(
                    self.x + eye_offset
                ),
                int(
                    self.y - eye_offset
                )
            ),

            4
        )

        pygame.draw.circle(

            game_surface,

            BLACK,

            (
                int(
                    self.x - eye_offset
                ),
                int(
                    self.y - eye_offset
                )
            ),

            2
        )

        pygame.draw.circle(

            game_surface,

            BLACK,

            (
                int(
                    self.x + eye_offset
                ),
                int(
                    self.y - eye_offset
                )
            ),

            2
        )


# =========================================================
# COIN
# =========================================================

class Coin:

    def __init__(
        self,
        x,
        y
    ):

        self.x = x
        self.y = y

        self.radius = 8

        self.life = 600

    def update(self):

        self.life -= 1

    def draw(self):

        pygame.draw.circle(

            game_surface,

            YELLOW,

            (
                int(self.x),
                int(self.y)
            ),

            self.radius
        )

        pygame.draw.circle(

            game_surface,

            ORANGE,

            (
                int(self.x),
                int(self.y)
            ),

            self.radius,

            2
        )


# =========================================================
# POWER UP
# =========================================================

class PowerUp:

    def __init__(
        self,
        x,
        y,
        power_type
    ):

        self.x = x
        self.y = y

        self.type = power_type

        self.radius = 14

        self.life = 600

    def update(self):

        self.life -= 1

    def draw(self):

        if self.type == "rapid":

            color = YELLOW

            text = "R"

        else:

            color = BLUE

            text = "S"

        pygame.draw.circle(

            game_surface,

            color,

            (
                int(self.x),
                int(self.y)
            ),

            self.radius
        )

        rendered = font_small.render(
            text,
            True,
            BLACK
        )

        game_surface.blit(

            rendered,

            (
                int(
                    self.x
                    -
                    rendered.get_width() / 2
                ),
                int(
                    self.y
                    -
                    rendered.get_height() / 2
                )
            )
        )


# =========================================================
# GAME OBJECTS
# =========================================================

player = Player()

bullets = []

zombies = []

coins = []

powerups = []


# =========================================================
# WAVE VARIABLES
# =========================================================

wave_number = 1

zombies_to_spawn = 0

spawn_timer = 0

wave_delay = 0


def start_wave():

    global zombies_to_spawn
    global spawn_timer
    global wave_delay

    zombies_to_spawn = int(

        difficulty["base_zombies"]
        +
        wave_number
        *
        difficulty["wave_zombies"]

    )

    # Faster spawning on harder difficulties

    spawn_timer = int(

        35
        /
        difficulty["spawn_speed"]

    )

    wave_delay = 60

    play_sound(wave_sound)


# =========================================================
# SPAWN ZOMBIE
# =========================================================

def spawn_zombie():

    chance = random.random()

    # Strong zombie

    if (

        wave_number >= 4
        and
        chance < difficulty["strong_chance"]

    ):

        zombie_type = "strong"

    # Fast zombie

    elif (

        chance
        <
        difficulty["fast_chance"]

    ):

        zombie_type = "fast"

    else:

        zombie_type = "normal"

    zombies.append(
        Zombie(zombie_type)
    )


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global player
    global zombies
    global bullets
    global coins
    global powerups

    global wave_number
    global zombies_to_spawn
    global spawn_timer
    global wave_delay

    player = Player()

    zombies.clear()
    bullets.clear()
    coins.clear()
    powerups.clear()

    particles.clear()

    wave_number = 1

    zombies_to_spawn = 0

    spawn_timer = 0

    wave_delay = 0

    start_wave()


# =========================================================
# BACKGROUND
# =========================================================

def draw_background():

    game_surface.fill(
        (18, 22, 25)
    )

    grid_size = 50

    for x in range(
        0,
        WIDTH,
        grid_size
    ):

        pygame.draw.line(

            game_surface,

            (25, 30, 34),

            (x, 0),

            (x, HEIGHT)
        )

    for y in range(
        0,
        HEIGHT,
        grid_size
    ):

        pygame.draw.line(

            game_surface,

            (25, 30, 34),

            (0, y),

            (WIDTH, y)
        )


# =========================================================
# PLAYER DRAW
# =========================================================

def draw_player():

    # Shield

    if player.shield > 0:

        pygame.draw.circle(

            game_surface,

            BLUE,

            (
                int(player.x),
                int(player.y)
            ),

            player.radius + 9,

            3
        )

    # Damage flash

    if player.damage_flash > 0:

        color = WHITE

    else:

        color = BLUE

    pygame.draw.circle(

        game_surface,

        color,

        (
            int(player.x),
            int(player.y)
        ),

        player.radius
    )


# =========================================================
# UI
# =========================================================

def draw_ui():

    # -----------------------------------------------------
    # HEALTH
    # -----------------------------------------------------

    pygame.draw.rect(

        game_surface,

        DARK_RED,

        (
            20,
            20,
            250,
            26
        )
    )

    health_width = int(

        250
        *
        max(
            0,
            player.health
        )
        /
        player.max_health

    )

    pygame.draw.rect(

        game_surface,

        RED,

        (
            20,
            20,
            health_width,
            26
        )
    )

    health_text = font_small.render(

        f"HP: {player.health}",

        True,

        WHITE
    )

    game_surface.blit(

        health_text,

        (
            30,
            21
        )
    )

    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    score_text = font_small.render(

        f"Score: {player.score}",

        True,

        WHITE
    )

    game_surface.blit(

        score_text,

        (
            20,
            60
        )
    )

    # -----------------------------------------------------
    # COINS
    # -----------------------------------------------------

    coin_text = font_small.render(

        f"Coins: {player.coins}",

        True,

        YELLOW
    )

    game_surface.blit(

        coin_text,

        (
            20,
            90
        )
    )

    # -----------------------------------------------------
    # KILLS
    # -----------------------------------------------------

    kills_text = font_small.render(

        f"Kills: {player.kills}",

        True,

        WHITE
    )

    game_surface.blit(

        kills_text,

        (
            20,
            120
        )
    )

    # -----------------------------------------------------
    # WAVE
    # -----------------------------------------------------

    wave_text = font_medium.render(

        f"WAVE {wave_number}",

        True,

        WHITE
    )

    game_surface.blit(

        wave_text,

        (
            WIDTH - wave_text.get_width() - 20,
            20
        )
    )

    # -----------------------------------------------------
    # DIFFICULTY
    # -----------------------------------------------------

    diff_text = font_small.render(

        difficulty["name"],

        True,

        difficulty["color"]
    )

    game_surface.blit(

        diff_text,

        (
            WIDTH
            -
            diff_text.get_width()
            -
            20,

            65
        )
    )

    # -----------------------------------------------------
    # POWER UPS
    # -----------------------------------------------------

    if player.rapid_fire > 0:

        rapid_text = font_small.render(

            f"RAPID FIRE: {player.rapid_fire // FPS}s",

            True,

            YELLOW
        )

        game_surface.blit(

            rapid_text,

            (
                WIDTH // 2
                -
                rapid_text.get_width() // 2,

                20
            )
        )

    if player.shield > 0:

        shield_text = font_small.render(

            f"SHIELD: {player.shield // FPS}s",

            True,

            BLUE
        )

        game_surface.blit(

            shield_text,

            (
                WIDTH // 2
                -
                shield_text.get_width() // 2,

                50
            )
        )


# =========================================================
# MENU
# =========================================================

def draw_menu():

    game_surface.fill(
        (10, 15, 18)
    )

    title = font_title.render(

        "ZOMBIE SURVIVAL",

        True,

        RED
    )

    game_surface.blit(

        title,

        (
            WIDTH // 2
            -
            title.get_width() // 2,

            70
        )
    )

    start = font_medium.render(

        "PRESS ENTER TO START",

        True,

        WHITE
    )

    game_surface.blit(

        start,

        (
            WIDTH // 2
            -
            start.get_width() // 2,

            165
        )
    )

    difficulty_text = font_medium.render(

        "DIFFICULTY",

        True,

        WHITE
    )

    game_surface.blit(

        difficulty_text,

        (
            WIDTH // 2
            -
            difficulty_text.get_width() // 2,

            240
        )
    )

    # Difficulty list

    start_y = 300

    for i, item in enumerate(
        DIFFICULTIES
    ):

        if i == difficulty_index:

            color = item["color"]

            # Selection box

            pygame.draw.rect(

                game_surface,

                (45, 45, 50),

                (
                    WIDTH // 2 - 170,
                    start_y + i * 42 - 4,
                    340,
                    36
                )
            )

            pygame.draw.rect(

                game_surface,

                color,

                (
                    WIDTH // 2 - 170,
                    start_y + i * 42 - 4,
                    5,
                    36
                )
            )

        else:

            color = GRAY

        text = font_small.render(

            item["name"],

            True,

            color
        )

        game_surface.blit(

            text,

            (
                WIDTH // 2
                -
                text.get_width() // 2,

                start_y + i * 42
            )
        )

    controls = font_tiny.render(

        "UP / DOWN = Difficulty     ENTER = Start",

        True,

        GRAY
    )

    game_surface.blit(

        controls,

        (
            WIDTH // 2
            -
            controls.get_width() // 2,

            520
        )
    )

    controls2 = font_tiny.render(

        "WASD = Move    Mouse = Aim    Left Click = Shoot    F11 = Fullscreen",

        True,

        GRAY
    )

    game_surface.blit(

        controls2,

        (
            WIDTH // 2
            -
            controls2.get_width() // 2,

            550
        )
    )


# =========================================================
# PAUSE
# =========================================================

def draw_pause():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 160)
    )

    game_surface.blit(
        overlay,
        (0, 0)
    )

    text = font_big.render(

        "PAUSED",

        True,

        WHITE
    )

    game_surface.blit(

        text,

        (
            WIDTH // 2
            -
            text.get_width() // 2,

            HEIGHT // 2 - 60
        )
    )

    info = font_small.render(

        "Press P to continue",

        True,

        GRAY
    )

    game_surface.blit(

        info,

        (
            WIDTH // 2
            -
            info.get_width() // 2,

            HEIGHT // 2 + 20
        )
    )


# =========================================================
# GAME OVER
# =========================================================

def draw_game_over():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 175)
    )

    game_surface.blit(
        overlay,
        (0, 0)
    )

    text = font_big.render(

        "GAME OVER",

        True,

        RED
    )

    game_surface.blit(

        text,

        (
            WIDTH // 2
            -
            text.get_width() // 2,

            150
        )
    )

    score = font_medium.render(

        f"Score: {player.score}",

        True,

        WHITE
    )

    game_surface.blit(

        score,

        (
            WIDTH // 2
            -
            score.get_width() // 2,

            250
        )
    )

    wave_result = font_medium.render(

        f"Reached Wave: {wave_number}",

        True,

        WHITE
    )

    game_surface.blit(

        wave_result,

        (
            WIDTH // 2
            -
            wave_result.get_width() // 2,

            300
        )
    )

    difficulty_result = font_small.render(

        f"Difficulty: {difficulty['name']}",

        True,

        difficulty["color"]
    )

    game_surface.blit(

        difficulty_result,

        (
            WIDTH // 2
            -
            difficulty_result.get_width() // 2,

            345
        )
    )

    restart = font_small.render(

        "Press R to Restart",

        True,

        WHITE
    )

    game_surface.blit(

        restart,

        (
            WIDTH // 2
            -
            restart.get_width() // 2,

            410
        )
    )


# =========================================================
# WAVE MESSAGE
# =========================================================

def draw_wave_message():

    if wave_delay > 0:

        text = font_big.render(

            f"WAVE {wave_number}",

            True,

            WHITE
        )

        game_surface.blit(

            text,

            (
                WIDTH // 2
                -
                text.get_width() // 2,

                HEIGHT // 2 - 50
            )
        )


# =========================================================
# MOUSE CONVERSION
# =========================================================

def get_game_mouse_pos():

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen_width, screen_height = screen.get_size()

    if (
        screen_width <= 0
        or screen_height <= 0
    ):

        return mouse_x, mouse_y

    game_x = (

        mouse_x
        *
        WIDTH
        /
        screen_width

    )

    game_y = (

        mouse_y
        *
        HEIGHT
        /
        screen_height

    )

    return game_x, game_y


# =========================================================
# FULLSCREEN
# =========================================================

def toggle_fullscreen():

    global fullscreen
    global screen

    fullscreen = not fullscreen

    if fullscreen:

        screen = pygame.display.set_mode(

            (0, 0),

            pygame.FULLSCREEN
        )

    else:

        screen = pygame.display.set_mode(

            (
                WIDTH,
                HEIGHT
            )
        )


# =========================================================
# GAME STATES
# =========================================================

MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

game_state = MENU


# =========================================================
# TIMER
# =========================================================

game_start_time = 0

final_time = 0


def get_game_time():

    if game_state == GAME_OVER:

        return final_time

    if game_start_time == 0:

        return 0

    return (
        pygame.time.get_ticks()
        -
        game_start_time
    ) // 1000


def format_time(seconds):

    minutes = seconds // 60

    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    clock.tick(FPS)

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # -------------------------------------------------
        # KEYBOARD
        # -------------------------------------------------

        if event.type == pygame.KEYDOWN:

            # F11
            if event.key == pygame.K_F11:

                toggle_fullscreen()

            # ESC
            elif event.key == pygame.K_ESCAPE:

                if fullscreen:

                    fullscreen = False

                    screen = pygame.display.set_mode(

                        (
                            WIDTH,
                            HEIGHT
                        )
                    )

                else:

                    running = False

            # -------------------------------------------------
            # MENU
            # -------------------------------------------------

            elif game_state == MENU:

                if event.key == pygame.K_UP:

                    difficulty_index -= 1

                    if difficulty_index < 0:

                        difficulty_index = (
                            len(DIFFICULTIES) - 1
                        )

                    difficulty = (
                        DIFFICULTIES[
                            difficulty_index
                        ]
                    )

                elif event.key == pygame.K_DOWN:

                    difficulty_index += 1

                    if (
                        difficulty_index
                        >=
                        len(DIFFICULTIES)
                    ):

                        difficulty_index = 0

                    difficulty = (
                        DIFFICULTIES[
                            difficulty_index
                        ]
                    )

                elif event.key == pygame.K_RETURN:

                    reset_game()

                    game_start_time = (
                        pygame.time.get_ticks()
                    )

                    game_state = PLAYING

            # -------------------------------------------------
            # PLAYING
            # -------------------------------------------------

            elif game_state == PLAYING:

                if event.key == pygame.K_p:

                    game_state = PAUSED

            # -------------------------------------------------
            # PAUSED
            # -------------------------------------------------

            elif game_state == PAUSED:

                if event.key == pygame.K_p:

                    game_state = PLAYING

            # -------------------------------------------------
            # GAME OVER
            # -------------------------------------------------

            elif game_state == GAME_OVER:

                if event.key == pygame.K_r:

                    reset_game()

                    game_start_time = (
                        pygame.time.get_ticks()
                    )

                    game_state = PLAYING

        # -------------------------------------------------
        # MOUSE
        # -------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if (

                event.button == 1
                and
                game_state == PLAYING

            ):

                mouse_x, mouse_y = (
                    get_game_mouse_pos()
                )

                player.shoot(
                    mouse_x,
                    mouse_y
                )

    # =====================================================
    # PLAYING
    # =====================================================

    if game_state == PLAYING:

        player.update()

        # -------------------------------------------------
        # WAVE DELAY
        # -------------------------------------------------

        if wave_delay > 0:

            wave_delay -= 1

        # -------------------------------------------------
        # SPAWN ZOMBIES
        # -------------------------------------------------

        if (

            zombies_to_spawn > 0
            and
            wave_delay <= 0

        ):

            spawn_timer -= 1

            if spawn_timer <= 0:

                spawn_zombie()

                zombies_to_spawn -= 1

                # Harder difficulty = faster spawning

                spawn_timer = max(

                    10,

                    int(

                        38
                        /
                        difficulty["spawn_speed"]

                    )

                )

        # -------------------------------------------------
        # NEW WAVE
        # -------------------------------------------------

        if (

            zombies_to_spawn <= 0
            and
            len(zombies) == 0
            and
            wave_delay <= 0

        ):

            wave_number += 1

            # Heal a little between waves

            player.health = min(

                player.max_health,

                player.health
                +
                difficulty["wave_heal"]

            )

            start_wave()

        # -------------------------------------------------
        # BULLETS
        # -------------------------------------------------

        for bullet in bullets[:]:

            bullet.update()

            if (

                bullet.x < -30
                or
                bullet.x > WIDTH + 30
                or
                bullet.y < -30
                or
                bullet.y > HEIGHT + 30

            ):

                if bullet in bullets:

                    bullets.remove(bullet)

        # -------------------------------------------------
        # ZOMBIES
        # -------------------------------------------------

        for zombie in zombies[:]:

            zombie.update()

        # -------------------------------------------------
        # BULLET COLLISION
        # -------------------------------------------------

        for bullet in bullets[:]:

            bullet_hit = False

            for zombie in zombies[:]:

                distance = math.sqrt(

                    (
                        bullet.x
                        -
                        zombie.x
                    ) ** 2

                    +

                    (
                        bullet.y
                        -
                        zombie.y
                    ) ** 2

                )

                if (

                    distance
                    <
                    bullet.radius
                    +
                    zombie.radius

                ):

                    zombie.health -= (
                        bullet.damage
                    )

                    zombie.hit_flash = 5

                    play_sound(hit_sound)

                    create_particles(

                        bullet.x,
                        bullet.y,
                        RED,
                        8
                    )

                    if bullet in bullets:

                        bullets.remove(bullet)

                    bullet_hit = True

                    # Zombie killed

                    if zombie.health <= 0:

                        player.kills += 1

                        player.score += 100

                        # Coin

                        if random.random() < 0.50:

                            coins.append(

                                Coin(

                                    zombie.x,
                                    zombie.y

                                )

                            )

                        # Power-up

                        if random.random() < 0.08:

                            power_type = (
                                random.choice(
                                    [
                                        "rapid",
                                        "shield"
                                    ]
                                )
                            )

                            powerups.append(

                                PowerUp(

                                    zombie.x,
                                    zombie.y,

                                    power_type

                                )

                            )

                        create_particles(

                            zombie.x,
                            zombie.y,

                            zombie.color,

                            20

                        )

                        zombies.remove(
                            zombie
                        )

                    break

            if bullet_hit:

                continue

        # -------------------------------------------------
        # COINS
        # -------------------------------------------------

        for coin in coins[:]:

            coin.update()

            distance = math.sqrt(

                (
                    coin.x
                    -
                    player.x
                ) ** 2

                +

                (
                    coin.y
                    -
                    player.y
                ) ** 2

            )

            if (

                distance
                <
                coin.radius
                +
                player.radius

            ):

                player.coins += 1

                player.score += 25

                play_sound(coin_sound)

                create_particles(

                    coin.x,
                    coin.y,

                    YELLOW,

                    10

                )

                coins.remove(coin)

            elif coin.life <= 0:

                coins.remove(coin)

        # -------------------------------------------------
        # POWERUPS
        # -------------------------------------------------

        for power in powerups[:]:

            power.update()

            distance = math.sqrt(

                (
                    power.x
                    -
                    player.x
                ) ** 2

                +

                (
                    power.y
                    -
                    player.y
                ) ** 2

            )

            if (

                distance
                <
                power.radius
                +
                player.radius

            ):

                if power.type == "rapid":

                    player.rapid_fire = (
                        600
                    )

                else:

                    player.shield = (
                        600
                    )

                play_sound(power_sound)

                create_particles(

                    power.x,
                    power.y,

                    BLUE,

                    15

                )

                powerups.remove(power)

            elif power.life <= 0:

                powerups.remove(power)

        # -------------------------------------------------
        # PARTICLES
        # -------------------------------------------------

        update_particles()

        # -------------------------------------------------
        # GAME OVER
        # -------------------------------------------------

        if player.health <= 0:

            final_time = get_game_time()

            game_state = GAME_OVER

    # =====================================================
    # DRAW
    # =====================================================

    if game_state == MENU:

        draw_menu()

    else:

        draw_background()

        # Coins

        for coin in coins:

            coin.draw()

        # Powerups

        for power in powerups:

            power.draw()

        # Bullets

        for bullet in bullets:

            bullet.draw()

        # Zombies

        for zombie in zombies:

            zombie.draw()

        # Player

        draw_player()

        # Particles

        draw_particles()

        # UI

        draw_ui()

        # Wave message

        if (

            game_state == PLAYING
            and
            wave_delay > 0

        ):

            draw_wave_message()

        # Pause

        if game_state == PAUSED:

            draw_pause()

        # Game Over

        elif game_state == GAME_OVER:

            draw_game_over()

        # Time

        if game_state in (
            PLAYING,
            PAUSED
        ):

            time_text = font_small.render(

                format_time(
                    get_game_time()
                ),

                True,

                WHITE
            )

            game_surface.blit(

                time_text,

                (
                    WIDTH // 2
                    -
                    time_text.get_width() // 2,

                    HEIGHT - 35
                )
            )

    # =====================================================
    # FULLSCREEN SCALING
    # =====================================================

    screen_width, screen_height = (
        screen.get_size()
    )

    scaled_game = pygame.transform.scale(

        game_surface,

        (
            screen_width,
            screen_height
        )

    )

    screen.blit(

        scaled_game,

        (0, 0)
    )

    pygame.display.flip()


pygame.quit()