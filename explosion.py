import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Create explosions"""
    def __init__(self, game, x, y):
        """Initialize explosion fields"""
        super().__init__()
        self.screen = game.screen
        self.images = []
        self.index = 0
        self.counter = 0
        self._load_images()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def _load_images(self):
        """Loads explosion images & put them in the list"""
        img_num = 3
        for i in range(img_num):
            image = pygame.image.load(f"images/exp{i}.bmp")
            image = pygame.transform.scale(image, (90, 90))
            self.images.append(image)

    def update(self):
        """Update explosion images"""
        explosion_time = 10
        # update explosion animation
        self.counter += 1
        if self.counter >= explosion_time and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if (self.index >= len(self.images) - 1 and
                self.counter >= explosion_time):
            self.kill()
