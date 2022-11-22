import pygame                           # импортируем библиотеку pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def strip_from_sheet(self, col_row, col_span, width, height, scale, colour=(0, 0, 0)):
        """ Strips individual frames from specific sprite sheet. """
        images = []
        for i in range(col_span):
            for j in range(col_row):
                image = pygame.Surface((width, height )).convert_alpha()
                image.blit(self.sheet, (0, 0), (j * width, i * height, width, height))
                image = pygame.transform.scale(image, (width * scale, height * scale))
                image.set_colorkey(colour)
                images.append(image)
        return images