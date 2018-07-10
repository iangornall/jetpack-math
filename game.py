import pygame

class Surface(object):
  def __init__(self, image_path):
    self.image = pygame.image.load(image_path).convert_alpha()
    self.set_dimensions()
  def resize(self, width, height):
    self.image = pygame.transform.scale(self.image, (width, height))
    self.set_dimensions()
  def set_dimensions(self):
    self.width = self.image.get_rect().width
    self.height = self.image.get_rect().height

class Astronaut(object):
  def __init__(self, image_paths):
    self.frames = []
    for image_path in image_paths:
      frame = Surface(image_path)
      self.frames.append(frame)
      print frame.width
      print frame.height
    self.width = self.frames[0].width
    self.height = self.frames[0].height
  def resize(self, width, height):
    width = int(.05 * width)
    height = int(.1 * height)
    for frame in self.frames:
      frame.resize(width, height)

def resize(width, height, screen, surfaces):
  screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)
  width, height = pygame.display.get_surface().get_size()
  for surface in surfaces:
    surface.resize(width, height)
  return screen, surfaces

def main():
  pygame.init()
  clock = pygame.time.Clock()
  pygame.display.set_caption('Math Blaster')
  # set background and screen size
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
  width, height = pygame.display.get_surface().get_size()
  background = Surface('./images/bg5.jpg')
  background.resize(width, height)
  astronaut = Astronaut(['./images/astronaut-stand.png', './images/astronaut-walk1.png', './images/astronaut-walk2.png'])
  astronaut.resize(width, height)
  surfaces = (background, astronaut)

  stop_game = False
  while not stop_game:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          width, height = (800, 600)
          screen, surfaces = resize(width, height, screen, surfaces)
      if event.type == pygame.VIDEORESIZE:
        width, height = event.dict['size']
        screen, surfaces = resize(width, height, screen, surfaces)
      if event.type == pygame.QUIT:
        stop_game = True
    screen.fill((0, 0, 0))
    screen.blit(background.image, (0,0))
    screen.blit(astronaut.frames[0].image, (width / 4 - astronaut.width / 2, 3 * height / 4))
    screen.blit(astronaut.frames[1].image, (2 * width / 4 - astronaut.width / 2, 3 * height / 4))
    screen.blit(astronaut.frames[2].image, (3 * width / 4 - astronaut.width / 2, 3 * height / 4))
    pygame.display.update()
    clock.tick(60)
  pygame.quit()

if __name__ == '__main__':
  main()