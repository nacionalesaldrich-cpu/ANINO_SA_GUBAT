"""
Procedural asset generator - creates pixel art textures and sprites at runtime.
"""
import pygame
import math
import random
import os

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


def _ensure_dirs():
    for sub in ('textures', 'sprites', 'audio', 'fonts'):
        p = os.path.join(ASSET_DIR, sub)
        os.makedirs(p, exist_ok=True)


def generate_wall_texture(width=64, height=64, base_color=(60, 40, 25), variation=15, style='stone'):
    """Generate a pixelated wall texture."""
    surf = pygame.Surface((width, height))
    surf.fill(base_color)
    rng = random.Random(hash(base_color) + hash(style))

    if style == 'stone':
        for y in range(0, height, 8):
            offset = (y // 8 % 2) * 16
            for x in range(0, width, 32):
                bx = (x + offset) % width
                v = rng.randint(-variation, variation)
                color = tuple(max(0, min(255, c + v)) for c in base_color)
                rect = pygame.Rect(bx, y, 30, 6)
                pygame.draw.rect(surf, color, rect)
                pygame.draw.rect(surf, tuple(max(0, c - 30) for c in color), rect, 1)
    elif style == 'wood':
        for y in range(height):
            v = int(math.sin(y * 0.3) * 8)
            for x in range(width):
                noise = rng.randint(-5, 5)
                color = tuple(max(0, min(255, c + v + noise)) for c in base_color)
                surf.set_at((x, y), color)
        for y in range(0, height, 12):
            pygame.draw.line(surf, tuple(max(0, c - 20) for c in base_color), (0, y), (width, y))
    elif style == 'bamboo':
        segment_h = 16
        for seg in range(height // segment_h + 1):
            y0 = seg * segment_h
            v = rng.randint(-8, 8)
            seg_color = tuple(max(0, min(255, c + v)) for c in base_color)
            pygame.draw.rect(surf, seg_color, (8, y0, width - 16, segment_h))
            node_color = tuple(max(0, c - 25) for c in seg_color)
            pygame.draw.rect(surf, node_color, (6, y0, width - 12, 3))
        pygame.draw.line(surf, tuple(max(0, c - 15) for c in base_color), (width // 2, 0), (width // 2, height))
    elif style == 'balete':
        for y in range(height):
            for x in range(width):
                twist = int(math.sin(y * 0.15 + x * 0.1) * 12)
                v = rng.randint(-8, 8)
                color = tuple(max(0, min(255, c + twist + v)) for c in base_color)
                surf.set_at((x, y), color)
        for i in range(5):
            rx = rng.randint(0, width)
            pygame.draw.line(surf, tuple(max(0, c - 30) for c in base_color),
                             (rx, 0), (rx + rng.randint(-10, 10), height), 2)

    return surf


def generate_floor_texture(width=64, height=64, base_color=(25, 18, 12)):
    """Generate a dirt/ground texture."""
    surf = pygame.Surface((width, height))
    rng = random.Random(42)
    for y in range(height):
        for x in range(width):
            v = rng.randint(-10, 10)
            color = tuple(max(0, min(255, c + v)) for c in base_color)
            surf.set_at((x, y), color)
    for _ in range(20):
        px, py = rng.randint(0, width - 1), rng.randint(0, height - 1)
        surf.set_at((px, py), tuple(min(255, c + 20) for c in base_color))
    return surf


def generate_weapon_sprite(weapon_type='bolo', width=128, height=128):
    """Generate a simple weapon sprite for HUD display."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    if weapon_type == 'bolo':
        handle_color = (100, 60, 30)
        blade_color = (180, 180, 190)
        pygame.draw.rect(surf, handle_color, (50, 70, 12, 58))
        pygame.draw.polygon(surf, blade_color, [
            (40, 20), (72, 20), (76, 30), (68, 70), (44, 70), (36, 30)
        ])
        pygame.draw.polygon(surf, (150, 150, 160), [
            (42, 22), (70, 22), (74, 30), (66, 68), (46, 68), (38, 30)
        ])
        pygame.draw.rect(surf, (80, 50, 25), (46, 68, 20, 6))

    elif weapon_type == 'shotgun':
        barrel_color = (60, 60, 65)
        stock_color = (90, 55, 30)
        pygame.draw.rect(surf, stock_color, (45, 80, 40, 48))
        pygame.draw.polygon(surf, stock_color, [(45, 100), (30, 128), (55, 128), (55, 100)])
        pygame.draw.rect(surf, barrel_color, (50, 20, 14, 65))
        pygame.draw.rect(surf, barrel_color, (48, 20, 18, 65))
        pygame.draw.rect(surf, (50, 50, 55), (52, 18, 10, 4))
        pygame.draw.rect(surf, (70, 45, 25), (46, 78, 22, 6))

    elif weapon_type == 'revolver':
        body_color = (70, 70, 75)
        grip_color = (85, 50, 25)
        pygame.draw.rect(surf, body_color, (40, 55, 50, 18))
        pygame.draw.rect(surf, body_color, (42, 38, 8, 20))
        cylinder = (55, 64)
        pygame.draw.circle(surf, (80, 80, 85), cylinder, 10)
        pygame.draw.circle(surf, (60, 60, 65), cylinder, 8)
        pygame.draw.rect(surf, body_color, (65, 52, 35, 10))
        pygame.draw.rect(surf, (50, 50, 55), (98, 54, 6, 6))
        pygame.draw.polygon(surf, grip_color, [(42, 72), (56, 72), (60, 110), (38, 110)])
        for i in range(4):
            pygame.draw.line(surf, (70, 40, 20), (42, 80 + i * 6), (56, 80 + i * 6))

    return surf


def generate_enemy_sprite(enemy_type='aswang', width=64, height=64, state='idle'):
    """Generate a simple enemy sprite."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    if enemy_type == 'aswang':
        body_color = (40, 30, 35)
        eye_color = (220, 30, 30)
        pygame.draw.ellipse(surf, body_color, (16, 8, 32, 48))
        pygame.draw.ellipse(surf, (50, 35, 40), (20, 12, 24, 20))
        pygame.draw.circle(surf, eye_color, (28, 20), 3)
        pygame.draw.circle(surf, eye_color, (36, 20), 3)
        pygame.draw.line(surf, (60, 40, 45), (26, 30), (38, 30), 2)
        if state == 'attack':
            pygame.draw.polygon(surf, (60, 40, 45), [(24, 28), (40, 28), (32, 36)])
            pygame.draw.circle(surf, (255, 50, 50), (28, 20), 4)
            pygame.draw.circle(surf, (255, 50, 50), (36, 20), 4)
        pygame.draw.line(surf, body_color, (22, 50), (18, 62), 3)
        pygame.draw.line(surf, body_color, (42, 50), (46, 62), 3)

    elif enemy_type == 'manananggal':
        body_color = (50, 25, 35)
        wing_color = (70, 20, 30)
        pygame.draw.ellipse(surf, body_color, (20, 16, 24, 32))
        pygame.draw.ellipse(surf, (65, 35, 45), (24, 18, 16, 14))
        pygame.draw.circle(surf, (255, 40, 40), (30, 24), 2)
        pygame.draw.circle(surf, (255, 40, 40), (34, 24), 2)
        pygame.draw.polygon(surf, wing_color, [(20, 20), (2, 8), (8, 36)])
        pygame.draw.polygon(surf, wing_color, [(44, 20), (62, 8), (56, 36)])
        pygame.draw.line(surf, (180, 30, 30), (24, 48), (20, 60), 2)
        pygame.draw.line(surf, (180, 30, 30), (40, 48), (44, 60), 2)

    elif enemy_type == 'tikbalang':
        body_color = (80, 60, 40)
        pygame.draw.ellipse(surf, body_color, (18, 4, 28, 20))
        pygame.draw.polygon(surf, (90, 70, 45), [(26, 2), (32, 0), (38, 2), (36, 8), (28, 8)])
        pygame.draw.circle(surf, (255, 180, 0), (28, 12), 2)
        pygame.draw.circle(surf, (255, 180, 0), (36, 12), 2)
        pygame.draw.ellipse(surf, body_color, (16, 22, 32, 28))
        pygame.draw.line(surf, body_color, (22, 48), (18, 64), 4)
        pygame.draw.line(surf, body_color, (42, 48), (46, 64), 4)

    elif enemy_type == 'kapre':
        body_color = (45, 35, 25)
        pygame.draw.ellipse(surf, body_color, (10, 4, 44, 56))
        pygame.draw.ellipse(surf, (55, 42, 30), (18, 8, 28, 18))
        pygame.draw.circle(surf, (200, 100, 0), (28, 16), 3)
        pygame.draw.circle(surf, (200, 100, 0), (36, 16), 3)
        pygame.draw.rect(surf, (120, 80, 40), (40, 24, 18, 4))
        pygame.draw.ellipse(surf, (100, 60, 30), (42, 20, 8, 12))

    elif enemy_type == 'white_lady':
        pygame.draw.ellipse(surf, (220, 220, 230, 160), (16, 4, 32, 56))
        pygame.draw.ellipse(surf, (240, 240, 250, 180), (20, 6, 24, 18))
        pygame.draw.circle(surf, (0, 0, 0), (28, 14), 2)
        pygame.draw.circle(surf, (0, 0, 0), (36, 14), 2)
        for i in range(3):
            alpha = 100 - i * 30
            s = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (220, 220, 230, alpha), (14 - i * 2, 2, 36 + i * 4, 60 + i * 2))
            surf.blit(s, (0, 0))

    elif enemy_type == 'multo':
        for i in range(3):
            alpha = 80 - i * 20
            pygame.draw.ellipse(surf, (180, 180, 200, alpha),
                                (14 - i * 3, 8 - i * 2, 36 + i * 6, 48 + i * 4))
        pygame.draw.circle(surf, (100, 100, 120, 150), (28, 20), 2)
        pygame.draw.circle(surf, (100, 100, 120, 150), (36, 20), 2)

    elif enemy_type == 'sigbin':
        body_color = (50, 40, 45)
        pygame.draw.ellipse(surf, body_color, (8, 24, 48, 24))
        pygame.draw.ellipse(surf, (60, 45, 50), (12, 16, 20, 14))
        pygame.draw.circle(surf, (255, 60, 0), (20, 22), 2)
        pygame.draw.circle(surf, (255, 60, 0), (26, 22), 2)
        pygame.draw.line(surf, body_color, (14, 44), (10, 58), 3)
        pygame.draw.line(surf, body_color, (50, 44), (54, 58), 3)
        pygame.draw.line(surf, body_color, (50, 32), (60, 20), 2)

    return surf


def generate_pickup_sprite(pickup_type='health', size=32):
    """Generate pickup item sprites."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2

    if pickup_type == 'health':
        pygame.draw.rect(surf, (200, 40, 40), (4, 4, size - 8, size - 8), border_radius=4)
        pygame.draw.rect(surf, (255, 255, 255), (cx - 2, cy - 8, 4, 16))
        pygame.draw.rect(surf, (255, 255, 255), (cx - 8, cy - 2, 16, 4))
    elif pickup_type == 'ammo_shotgun':
        pygame.draw.rect(surf, (180, 140, 40), (8, 6, 16, 20), border_radius=2)
        pygame.draw.rect(surf, (200, 50, 50), (10, 4, 12, 6))
    elif pickup_type == 'ammo_revolver':
        for i in range(6):
            angle = i * math.pi / 3
            bx = cx + int(math.cos(angle) * 8)
            by = cy + int(math.sin(angle) * 8)
            pygame.draw.circle(surf, (180, 140, 40), (bx, by), 3)
            pygame.draw.circle(surf, (200, 50, 50), (bx, by), 2)
    elif pickup_type == 'salt':
        pygame.draw.rect(surf, (220, 220, 220), (8, 8, 16, 18), border_radius=2)
        pygame.draw.rect(surf, (180, 180, 180), (8, 8, 16, 5))
        for _ in range(8):
            px = random.randint(10, 22)
            py = random.randint(14, 24)
            surf.set_at((px, py), (240, 240, 240))
    elif pickup_type == 'garlic':
        pygame.draw.circle(surf, (230, 220, 200), (cx, cy), 10)
        pygame.draw.circle(surf, (210, 200, 180), (cx, cy), 8)
        pygame.draw.line(surf, (180, 170, 150), (cx, cy - 8), (cx, cy + 8))
        pygame.draw.arc(surf, (100, 140, 60), (cx - 4, cy - 14, 8, 8), 0, math.pi, 2)
    elif pickup_type == 'battery':
        pygame.draw.rect(surf, (60, 60, 70), (10, 8, 12, 20), border_radius=2)
        pygame.draw.rect(surf, (80, 80, 90), (12, 4, 8, 6))
        pygame.draw.rect(surf, (255, 220, 50), (12, 12, 8, 12))
    elif pickup_type == 'faith':
        pygame.draw.circle(surf, (80, 120, 220, 150), (cx, cy), 12)
        pygame.draw.circle(surf, (120, 160, 255, 200), (cx, cy), 6)
        for i in range(8):
            angle = i * math.pi / 4
            ex = cx + int(math.cos(angle) * 14)
            ey = cy + int(math.sin(angle) * 14)
            pygame.draw.line(surf, (100, 140, 240, 100), (cx, cy), (ex, ey))
    elif pickup_type == 'bible_page':
        pygame.draw.rect(surf, (220, 200, 160), (6, 4, 20, 26), border_radius=1)
        for i in range(5):
            pygame.draw.line(surf, (100, 80, 50), (9, 10 + i * 4), (23, 10 + i * 4))

    return surf


def generate_crosshair(size=16):
    """Generate a simple crosshair."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    gap = 2
    length = 5
    color = (255, 255, 255, 180)
    pygame.draw.line(surf, color, (cx, cy - gap - length), (cx, cy - gap), 1)
    pygame.draw.line(surf, color, (cx, cy + gap), (cx, cy + gap + length), 1)
    pygame.draw.line(surf, color, (cx - gap - length, cy), (cx - gap, cy), 1)
    pygame.draw.line(surf, color, (cx + gap, cy), (cx + gap + length, cy), 1)
    return surf


def generate_all_textures():
    """Generate and return all wall textures."""
    textures = {
        'stone': generate_wall_texture(64, 64, (70, 55, 40), 12, 'stone'),
        'wood': generate_wall_texture(64, 64, (90, 60, 30), 10, 'wood'),
        'bamboo': generate_wall_texture(64, 64, (100, 130, 60), 15, 'bamboo'),
        'balete': generate_wall_texture(64, 64, (50, 45, 30), 12, 'balete'),
        'door': generate_wall_texture(64, 64, (80, 50, 25), 8, 'wood'),
        'floor': generate_floor_texture(64, 64, (25, 18, 12)),
    }
    return textures


def generate_all_weapons():
    """Generate all weapon sprites."""
    return {
        'bolo': generate_weapon_sprite('bolo', 128, 128),
        'shotgun': generate_weapon_sprite('shotgun', 128, 128),
        'revolver': generate_weapon_sprite('revolver', 128, 128),
    }


def generate_all_enemies():
    """Generate all enemy sprites in different states."""
    enemies = {}
    types = ['aswang', 'manananggal', 'tikbalang', 'kapre', 'white_lady', 'multo', 'sigbin']
    for t in types:
        enemies[t] = {
            'idle': generate_enemy_sprite(t, 64, 64, 'idle'),
            'attack': generate_enemy_sprite(t, 64, 64, 'attack'),
        }
    return enemies


def generate_all_pickups():
    """Generate all pickup sprites."""
    pickup_types = ['health', 'ammo_shotgun', 'ammo_revolver', 'salt', 'garlic',
                    'battery', 'faith', 'bible_page']
    return {t: generate_pickup_sprite(t, 32) for t in pickup_types}
