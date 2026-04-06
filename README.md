# Orbital Drift 🚀

A physics-based 2D survival game built with Python and Pygame. Navigate a high-density asteroid field as difficulty scales over time — dodge everything, survive as long as you can.

---

## Gameplay

- Control a triangular ship through an asteroid field
- Asteroids bounce off walls and **speed up every 1000 points**
- A new asteroid spawns each time you level up
- Survive as long as possible and beat your high score

---

## Controls

| Key | Action |
|-----|--------|
| ← → ↑ ↓ | Move ship |

The ship uses **physics-based momentum** — you accelerate into movement and decelerate when you stop pressing keys. Screen wrapping is enabled — fly off one edge and you reappear on the other.

---

## Technical Highlights

- **Physics engine** — custom velocity/acceleration/friction system using `pygame.Vector2`
- **Circle collision detection** — pixel-perfect circular hitboxes instead of bounding boxes
- **Dynamic difficulty scaling** — asteroid count and speed increase every 1000 points
- **Screen wrapping** — toroidal coordinate system for seamless edge transitions
- **Consistent 60 FPS** — maintained even as object density increases 200% over time

---

## Setup

### Requirements
- Python 3.8+
- Pygame

### Install & Run

```bash
pip install pygame
python OrbitalDrift.py
```

---

## Built With

- Python
- Pygame
- Python IDLE

---

## Author

Marwan Albakri — Montclair State University, Information Technology
