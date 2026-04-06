import pygame
import random
import sys

# --- Configuration & Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN  = (0, 255, 255)
RED   = (255, 50, 50)
GRAY  = (100, 100, 100)
GOLD  = (255, 215, 0)

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """Handles player movement with physics-based momentum and screen wrapping."""
    def __init__(self):
        super().__init__()
        # Create a triangular ship using a polygon
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, CYAN, [(15, 0), (30, 30), (0, 30)])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # Physics setup
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.friction = -0.02

    def update(self):
        self.acc = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        
        # Movement controls
        if keys[pygame.K_LEFT]:  self.acc.x = -0.5
        if keys[pygame.K_RIGHT]: self.acc.x = 0.5
        if keys[pygame.K_UP]:    self.acc.y = -0.5
        if keys[pygame.K_DOWN]:  self.acc.y = 0.5

        # Apply laws of motion
        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Screen Wrapping Logic
        if self.pos.x > SCREEN_WIDTH: self.pos.x = 0
        if self.pos.x < 0: self.pos.x = SCREEN_WIDTH
        if self.pos.y > SCREEN_HEIGHT: self.pos.y = 0
        if self.pos.y < 0: self.pos.y = SCREEN_HEIGHT

        self.rect.center = self.pos

class Hazard(pygame.sprite.Sprite):
    """An asteroid that bounces off walls and increases speed over time."""
    def __init__(self):
        super().__init__()
        size = random.randint(20, 50)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw a circle for collision accuracy
        pygame.draw.circle(self.image, RED, (size//2, size//2), size//2, 2)
        
        # Random spawning location
        self.rect = self.image.get_rect(
            center=(random.randint(50, SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT-50))
        )
        self.vel = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
        self.radius = size // 2 # Used for circle collision

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Bounce off screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vel.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel.y *= -1

class Game:
    """Core Game Engine: Manages states, scoring, and UI."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Orbital Drift - Midterm")
        self.clock = pygame.time.Clock()
        
        # Font initialization
        self.font_main = pygame.font.SysFont("Arial", 32)
        self.font_huge = pygame.font.SysFont("Arial", 80, bold=True)
        
        self.state = "PLAYING"
        self.high_score = 0
        self.current_score = 0
        self.reset_level()

    def reset_level(self):
        """Prepares a new game session."""
        self.all_sprites = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Start with 5 hazards
        for _ in range(5):
            h = Hazard()
            self.all_sprites.add(h)
            self.hazards.add(h)
            
        self.current_score = 0
        self.state = "PLAYING"

    def level_up(self):
        """Increases difficulty every 1000 points."""
        new_h = Hazard()
        self.all_sprites.add(new_h)
        self.hazards.add(new_h)
        # Increase speed of existing hazards
        for h in self.hazards:
            h.vel *= 1.1

    def draw_button(self, text, y_pos, color):
        """Helper function to create UI buttons with hover effects."""
        btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover effect: turn white if mouse is over button
        is_hovered = btn_rect.collidepoint(mouse_pos)
        draw_color = WHITE if is_hovered else color
        
        pygame.draw.rect(self.screen, draw_color, btn_rect, 2)
        text_surf = self.font_main.render(text, True, draw_color)
        self.screen.blit(text_surf, (btn_rect.centerx - text_surf.get_width()//2, 
                                     btn_rect.centery - text_surf.get_height()//2))
        return btn_rect

    def run(self):
        while True:
            # 1. Background
            self.screen.fill(BLACK)
            
            # 2. Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Button click logic for Game Over screen
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == "GAMEOVER":
                    if self.play_btn.collidepoint(event.pos):
                        self.reset_level()
                    if self.quit_btn.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # 3. Game Logic (PLAYING)
            if self.state == "PLAYING":
                self.all_sprites.update()
                
                # Check for Level Up
                if self.current_score > 0 and self.current_score % 1000 == 0:
                    self.level_up()

                # Collision Detection using circles for fairness
                if pygame.sprite.spritecollide(self.player, self.hazards, False, pygame.sprite.collide_circle):
                    self.state = "GAMEOVER"
                    if self.current_score > self.high_score:
                        self.high_score = self.current_score
                
                self.current_score += 1
                self.all_sprites.draw(self.screen)
                
                # HUD Rendering
                lvl = (self.current_score // 1000) + 1
                score_txt = self.font_main.render(f"Score: {self.current_score}  |  Lvl: {lvl}", True, WHITE)
                self.screen.blit(score_txt, (20, 20))

            # 4. UI Logic (GAMEOVER)
            elif self.state == "GAMEOVER":
                # Dim background
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150)) 
                self.screen.blit(overlay, (0,0))

                # Display Stats
                title = self.font_huge.render("CRASHED!", True, RED)
                self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
                
                hs_text = f"NEW HIGH SCORE!" if self.current_score >= self.high_score else "HIGH SCORE"
                hs_color = GOLD if self.current_score >= self.high_score else WHITE
                
                hs_surf = self.font_main.render(f"{hs_text}: {self.high_score}", True, hs_color)
                self.screen.blit(hs_surf, (SCREEN_WIDTH//2 - hs_surf.get_width()//2, 230))
                
                # Buttons
                self.play_btn = self.draw_button("TRY AGAIN", 350, CYAN)
                self.quit_btn = self.draw_button("QUIT", 420, RED)

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error encountered: {e}")
        pygame.quit()