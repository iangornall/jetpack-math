import pygame, random

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
    width, height = pygame.display.get_surface().get_size()
    self.x = 0.5
    self.y = 0.75
    self.resize(width, height)
    self.frame = 0
    self.image = self.frames[self.frame].image
  def resize(self, width, height):
    width = int(.05 * width)
    height = int(.1 * height)
    for frame in self.frames:
      frame.resize(width, height)
    self.width = self.frames[0].width
    self.height = self.frames[0].height
  def walk_right(self):
    if self.frame >= len(self.frames):
      self.frame = 0
    self.image = self.frames[self.frame].image
    self.frame += 1
    self.x += 0.01
    if self.x > 1:
      self.x = 0
  def walk_left(self):
    if self.frame >= len(self.frames):
      self.frame = 0
    self.image = pygame.transform.flip(self.frames[self.frame].image, True, False)
    self.frame += 1
    self.x -= 0.01
    if self.x < 0:
      self.x = 1
  def blit(self, screen, width, height):
    screen.blit(self.image, (self.x * width, self.y * height))



def resize(width, height, screen, surfaces):
  screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)
  width, height = pygame.display.get_surface().get_size()
  for surface in surfaces:
    surface.resize(width, height)
  return screen, surfaces

def main():
  pygame.init()
  clock = pygame.time.Clock()
  frame = 0
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
  time = 0
  walk_time = 0
  change_direction_time = 0
  walk_left = True
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
    if pygame.time.get_ticks() > walk_time:
      if walk_left:
        astronaut.walk_left()
      else:
        astronaut.walk_right()
      walk_time += 100
    if pygame.time.get_ticks() > change_direction_time:
      if random.random() > 0.5:
        walk_left = not walk_left
      change_direction_time += 1000
    screen.fill((0, 0, 0))
    screen.blit(background.image, (0,0))
    astronaut.blit(screen, width, height)
    pygame.display.update()
    clock.tick(30)
    frame += 1
  pygame.quit()

if __name__ == '__main__':
  main()

# import cProfile as profile
# profile.run('main()')