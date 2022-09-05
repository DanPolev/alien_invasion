import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Create explosions"""
    def __init__(self, x, y, px_x, px_y):
        """Initialize explosion fields"""
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        self._load_images(px_x, px_y)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def _load_images(self, px_x, px_y):
        """Loads explosion images & put them in the list"""
        filenames = ["exp0.bmp", "exp1.bmp", "exp2.bmp"]
        img_num = len(filenames)
        for i in range(img_num):
            path = "images/" + filenames[i]
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (px_x, px_y))
            self.images.append(image)

    def update(self):
        """Update explosion animation"""
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
