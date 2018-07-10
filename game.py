import pygame, random

class Surface(object):
  def __init__(self, image_path):
    self.image = pygame.image.load(image_path).convert_alpha()
    self.set_dimensions()
    self.x = 0
    self.y = 0
  def resize(self, width, height):
    self.image = pygame.transform.scale(self.image, (width, height))
    self.set_dimensions()
  def set_dimensions(self):
    self.width = self.image.get_rect().width
    self.height = self.image.get_rect().height
  def blit(self, screen):
    screen.blit(self.image, (self.x, self.y))

class Astronaut(object):
  def __init__(self, image_paths):
    self.frames = []
    for image_path in image_paths:
      frame = Surface(image_path)
      self.frames.append(frame)
    width, height = pygame.display.get_surface().get_size()
    self.resize(width, height)
    self.x = 0.5
    # self.y = float(height - self.height) / height
    self.y = 0
    self.ground = float(height - self.height) / height
    self.frame = 0
    self.image = self.frames[self.frame].image
    self.going_right = False
    self.going_left = False
    self.going_up = False
    self.y_speed = 0
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
  def gravity(self):
    if self.y < self.ground:
      self.y_speed += 0.01
  def lift(self):
    self.y_speed = -0.03
  def y_move(self):
    self.y += self.y_speed
    width, height = pygame.display.get_surface().get_size()
    if self.y > self.ground:
      self.y = self.ground
  def blit(self, screen, width, height):
    screen.blit(self.image, (self.x * width, self.y * height))

class UFO(Surface):
  def __init__(self, image_path):
    super(UFO, self).__init__(image_path)
    width, height = pygame.display.get_surface().get_size()
    self.x = -0.1
    self.y = random.random() / 2
    self.resize(width, height)
    self.ground = float(height - self.height) / height
    self.x_speed = 0.01
  def move(self):
    self.x += self.x_speed
  def reset(self):
    self.x = -0.1
    self.y = self.y = random.random() / 2
  def resize(self, width, height):
    self.width = int(.1 * width)
    self.height = int(.1 * height)
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
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
  ufo_images = ['./images/red-ship.png', './images/blue-ship.png', './images/orange-ship.png']
  surfaces = [background, astronaut]

  stop_game = False
  time = 0
  add_ufo_time = 1500
  num_ufos = 5
  ufo_i = 0
  ufos = []
  walk_left = False
  walk_right = False
  while not stop_game:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          width, height = (800, 600)
          screen, surfaces = resize(width, height, screen, surfaces)
        if event.key == pygame.K_LEFT:
          astronaut.going_left = True
        if event.key == pygame.K_RIGHT:
          astronaut.going_right = True
        if event.key == pygame.K_UP:
          astronaut.going_up = True
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          astronaut.going_left = False
        if event.key == pygame.K_RIGHT:
          astronaut.going_right = False
        if event.key == pygame.K_UP:
          astronaut.going_up = False
      if event.type == pygame.VIDEORESIZE:
        width, height = event.dict['size']
        screen, surfaces = resize(width, height, screen, surfaces)
      if event.type == pygame.QUIT:
        stop_game = True
    if pygame.time.get_ticks() > add_ufo_time:
      if ufo_i < num_ufos:
        ufos.append(UFO(ufo_images[ufo_i % 3]))
      else:
        ufos[ufo_i % num_ufos].reset()
      ufo_i += 1
      add_ufo_time += 1500
    surfaces = [background, astronaut] + ufos
    astronaut.y_move()
    astronaut.gravity()
    if astronaut.going_left:
      astronaut.walk_left()
    elif astronaut.going_right:
      astronaut.walk_right()
    if astronaut.going_up:
      astronaut.lift()
    for ufo in ufos:
      ufo.move()
    screen.fill((0, 0, 0))
    background.blit(screen)
    astronaut.blit(screen, width, height)
    for ufo in ufos:
      ufo.blit(screen, width, height)
    pygame.display.update()
    clock.tick(30)
    frame += 1
  pygame.quit()

if __name__ == '__main__':
  main()

# import cProfile as profile
# profile.run('main()')