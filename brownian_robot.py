import numpy as np
import pygame
import random
import sys

class BrownianRobot:
    def __init__(self, arena_size=500, speed=2):
        self.arena_size = arena_size
        self.speed = speed
        self.position = np.array([arena_size // 2, arena_size // 2], dtype=float)  # Start in the middle
        self.angle = random.uniform(0, 2 * np.pi)  # Random initial direction (in radians)
        self.radius = 10  # Robot size for visualization

    def move(self):
        # Calculate movement vector based on current angle
        dx = self.speed * np.cos(self.angle)
        dy = self.speed * np.sin(self.angle)
        self.position += np.array([dx, dy])

        # Check for collision with arena boundaries
        if self.position[0] <= 0 or self.position[0] >= self.arena_size:
            self.position[0] = np.clip(self.position[0], 0, self.arena_size)
            self._rotate()
        if self.position[1] <= 0 or self.position[1] >= self.arena_size:
            self.position[1] = np.clip(self.position[1], 0, self.arena_size)
            self._rotate()

    def _rotate(self):
        # Rotate by a random angle between -180 and 180 degrees
        self.angle += random.uniform(-np.pi, np.pi)

    def get_position(self):
        return self.position

def run_simulation(save_gif=False):
    pygame.init()
    arena_size = 500
    screen = pygame.display.set_mode((arena_size, arena_size))
    pygame.display.set_caption("Brownian Robot Simulation")
    clock = pygame.time.Clock()

    robot = BrownianRobot(arena_size)
    frames = []
    running = True
    frame_count = 0
    max_frames = 300 if save_gif else float('inf')  # Limit frames for GIF

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update robot position
        robot.move()

        # Draw
        screen.fill((255, 255, 255))  # White background
        pygame.draw.circle(screen, (0, 0, 255), robot.get_position().astype(int), robot.radius)  # Blue robot
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, arena_size, arena_size), 2)  # Black arena border

        if save_gif:
            # Capture frame for GIF
            frame = pygame.surfarray.array3d(screen)
            frames.append(np.transpose(frame, (1, 0, 2)))  # Transpose for correct orientation

        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        frame_count += 1

    pygame.quit()

    if save_gif and frames:
        import imageio
        imageio.mimsave('brownian_robot.gif', frames, fps=60)
        print("GIF saved as 'brownian_robot.gif'")

if __name__ == "__main__":
    run_simulation(save_gif=True)
