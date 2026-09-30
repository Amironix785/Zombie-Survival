# 🧟 Zombie Survival

A simple but challenging **2D Zombie Survival Game** made with **Python and Pygame**.

The goal is simple: **survive as long as possible, defeat zombies, collect coins, use power-ups, and survive increasingly difficult waves.**

---

## 🎮 Features

* 🧟 Multiple zombie types
* 🌊 Wave-based survival system
* 🎯 Mouse aiming and shooting
* 🔫 Shooting cooldown system
* ❤️ Player health system
* 🛡️ Shield power-up
* ⚡ Rapid Fire power-up
* 🪙 Coin collection system
* 💯 Score system
* 💀 Kill counter
* ✨ Particle effects
* 🔊 Automatically generated sound effects
* ⏱️ Survival timer
* ⏸️ Pause system
* 🖥️ Fullscreen support
* 🎚️ Five difficulty levels
* 📈 Increasing difficulty as waves progress
* 🎨 Simple grid-based game environment

---

## 🎚️ Difficulty Levels

The game has **5 difficulty levels**:

| Difficulty    | Description                     |
| ------------- | ------------------------------- |
| 🟢 Easy       | Slower zombies and lower damage |
| ⚪ Normal      | Balanced difficulty             |
| 🟠 Hard       | Faster and stronger zombies     |
| 🔴 Extreme    | Very difficult survival         |
| 🟣 Impossible | Extremely challenging           |

Each difficulty changes several gameplay values, including:

* Zombie speed
* Zombie health
* Zombie damage
* Number of zombies
* Fast zombie chance
* Strong zombie chance
* Zombie attack cooldown
* Difficulty growth
* Health restored between waves

---

## 🧟 Zombie Types

There are currently **3 types of zombies**.

### Normal Zombie

The standard enemy.

* Medium speed
* Medium health
* Normal damage

### Fast Zombie

A smaller and faster zombie.

* High speed
* Lower health
* Lower damage

### Strong Zombie

A large and powerful zombie.

* Slow movement
* High health
* High damage

Strong zombies become available starting from **Wave 4**.

---

## ⚡ Power-Ups

Zombies have a chance to drop power-ups when defeated.

### ⚡ Rapid Fire

Temporarily increases the player's firing speed.

### 🛡️ Shield

Temporarily protects the player from zombie damage.

Power-ups disappear if they are not collected within a certain amount of time.

---

## 🪙 Coins & Score

Defeating zombies can cause them to drop coins.

Collecting a coin:

* Adds **1 coin**
* Adds **25 score**

Killing a zombie:

* Adds **1 kill**
* Adds **100 score**

---

## 🌊 Wave System

The game uses a wave-based survival system.

Each new wave increases the number and strength of zombies.

As the wave number increases:

* Zombie health increases
* Zombie speed increases
* Zombie damage increases
* More zombies spawn
* The chance of stronger zombie types changes depending on difficulty

The player also receives a small amount of health between waves.

---

## 🔊 Sound System

The game automatically generates its own `.wav` sound effects when they don't already exist.

The following sounds are generated:

```text
zombie_sounds/
├── shoot.wav
├── hit.wav
├── coin.wav
├── power.wav
├── damage.wav
└── wave.wav
```

This means you don't need to manually download sound files to run the basic game.

---

## 🎮 Controls

| Key / Button        | Action                  |
| ------------------- | ----------------------- |
| `W`                 | Move Up                 |
| `A`                 | Move Left               |
| `S`                 | Move Down               |
| `D`                 | Move Right              |
| `Left Mouse Button` | Shoot                   |
| `↑ / ↓`             | Select Difficulty       |
| `Enter`             | Start Game              |
| `P`                 | Pause / Resume          |
| `R`                 | Restart after Game Over |
| `F11`               | Toggle Fullscreen       |
| `ESC`               | Exit Fullscreen / Game  |

---

## 🛠️ Requirements

You need:

* Python 3.x
* Pygame

Install Pygame with:

```bash
pip install pygame
```

---

## ▶️ Running the Game

Clone or download this repository.

Then open a terminal in the project folder and run:

```bash
python main.py
```

The game should start with the main menu.

---

## 📁 Project Structure

A basic project structure can look like this:

```text
Zombie-Survival/
│
├── main.py
│
├── zombie_sounds/
│   ├── shoot.wav
│   ├── hit.wav
│   ├── coin.wav
│   ├── power.wav
│   ├── damage.wav
│   └── wave.wav
│
└── README.md
```

The `zombie_sounds` folder is automatically created by the game if it doesn't exist.

---

## 🧠 What I Learned From This Project

This project is also useful as a **Python/Pygame learning project**.

Some of the programming concepts used include:

* Classes and Objects
* Functions
* Variables
* Lists
* Dictionaries
* `if / elif / else`
* `for` loops
* `while` loops
* Random numbers
* Collision detection
* Game states
* Timers and cooldowns
* Event handling
* Mouse input
* Keyboard input
* Sound generation
* File and folder handling
* Basic vector/movement calculations
* Particle systems
* Object spawning
* Game loops

---

## 📌 Important

This is a **2D survival game project** created with Python and Pygame.

The project is designed to be simple enough to understand and modify while still containing several real game-development concepts.

You can modify the code to add:

* New weapons
* New zombies
* More power-ups
* Boss fights
* Different maps
* Shops
* More difficulty levels
* High scores
* Better graphics
* Music
* Multiplayer features

---

## 🧟 Survive the Waves

**How long can you survive?**

Good luck.
**The zombies are getting stronger...**
