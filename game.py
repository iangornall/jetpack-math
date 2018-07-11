import pygame, random, time

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

class Math(object):
  def __init__(self, num_answers = 4):
    self.num_answers = 4
    self.wrong_answers = []
    self.operation = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
    operation_functions = {'addition': self.addition, 'subtraction': self.subtraction, 'multiplication': self.multiplication, 'division': self.division}
    operation_functions[self.operation]()
  def addition(self):
    self.operand = '+'
    self.num_1 = random.randint(0, 100)
    self.num_2 = random.randint(0, 100)
    self.expression = '%d %s %d' % (self.num_1, self.operand, self.num_2)
    self.target_answer = eval(self.expression)
    for i in range(self.num_answers - 1):
      random_answer = self.target_answer
      while random_answer == self.target_answer:
        random_answer = random.randint(0, 200)
      self.wrong_answers.append(random_answer)
  def subtraction(self):
    self.operand = '-'
    self.num_2 = random.randint(0, 100)
    self.num_1 = random.randint(self.num_2, 100)
    self.expression = '%d %s %d' % (self.num_1, self.operand, self.num_2)
    self.target_answer = eval(self.expression)
    for i in range(self.num_answers - 1):
      random_answer = self.target_answer
      while random_answer == self.target_answer:
        random_answer = random.randint(self.num_2, self.num_1)
      self.wrong_answers.append(random_answer)
  def multiplication(self):
    self.operand = '*'
    self.num_1 = random.randint(0, 12)
    self.num_2 = random.randint(0, 12)
    self.expression = '%d %s %d' % (self.num_1, self.operand, self.num_2)
    self.target_answer = eval(self.expression)
    for i in range(self.num_answers - 1):
      random_answer = self.target_answer
      while random_answer == self.target_answer:
        random_answer = random.randint(min(self.num_1, self.num_2), self.num_1 * self.num_2)
      self.wrong_answers.append(random_answer)
  def division(self):
    self.operand = '/'
    self.num_2 = random.randint(1, 12)
    self.num_1 = self.num_2 * random.randint(1, 12)
    self.expression = '%d %s %d' % (self.num_1, self.operand, self.num_2)
    self.target_answer = int(eval(self.expression))
    for i in range(self.num_answers - 1):
      random_answer = self.target_answer
      while random_answer == self.target_answer:
        random_answer = random.randint(1, 12)
      self.wrong_answers.append(random_answer)

class Astronaut(object):
  def __init__(self, image_paths, lift_path):
    self.frames = []
    for image_path in image_paths:
      frame = Surface(image_path)
      self.frames.append(frame)
    width, height = pygame.display.get_surface().get_size()
    self.lift_surface = Surface(lift_path)
    self.resize(width, height)
    self.x = 0.5
    self.ground = float(height - self.height) / height
    self.y = self.ground
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
    width = int(1.1 * width)
    height = int(1.4 * height)
    self.lift_surface.resize(width, height)
    self.lift_image_right = self.lift_surface.image
    self.lift_image_left = pygame.transform.flip(self.lift_image_right, True, False)
    self.lift_image = self.lift_image_right
  def walk_right(self):
    self.lift_image = self.lift_image_right
    if self.frame >= len(self.frames):
      self.frame = 0
    self.image = self.frames[self.frame].image
    self.frame += 1
    self.x += 0.005
    if self.x > 1:
      self.x = 0
  def walk_left(self):
    self.lift_image = self.lift_image_left
    if self.frame >= len(self.frames):
      self.frame = 0
    self.image = pygame.transform.flip(self.frames[self.frame].image, True, False)
    self.frame += 1
    self.x -= 0.005
    if self.x < 0:
      self.x = 1
  def gravity(self):
    if self.y < self.ground:
      self.y_speed += 0.005
  def lift(self):
    self.image = self.lift_image
    self.y_speed = -0.015
  def y_move(self):
    self.y += self.y_speed
    width, height = pygame.display.get_surface().get_size()
    if self.y > self.ground:
      self.y = self.ground
  def blit(self, screen, width, height):
    screen.blit(self.image, (self.x * width, self.y * height))
  def reset(self):
    self.x = 0.5
    self.y = self.ground
  def hide(self):
    self.x = -1000000
    self.y = -1000000
    self.going_left = False
    self.going_right = False
    self.going_up = False

class UFO(Surface):
  def __init__(self, image_path, math_answer, target):
    super(UFO, self).__init__(image_path)
    width, height = pygame.display.get_surface().get_size()
    self.x = -0.1
    self.y = random.random() / 2 + 0.1
    self.ground = float(height - self.height) / height
    self.x_speed = 0.005
    self.target = target
    self.math_answer = math_answer
    font = pygame.font.Font(None, height / 20)
    self.answer_text = font.render(str(self.math_answer), True, (255, 255, 255))
    self.resize(width, height)
  def move(self):
    self.x += self.x_speed
  def reset(self):
    self.x = -0.1
    self.y = self.y = random.random() / 2
  def resize(self, width, height):
    self.width = int(.1 * width)
    self.height = int(.1 * height)
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    font = pygame.font.Font(None, height / 20)
    self.answer_text = font.render(str(self.math_answer), True, (255, 255, 255))
  def blit(self, screen, target_text, width, height):
    screen.blit(self.image, (self.x * width, self.y * height))
    screen.blit(self.answer_text, (self.x * width + self.width / 2 - self.answer_text.get_width() / 2, (self.y - 0.03) * height))
  def collide(self, astronaut):
    width, height = pygame.display.get_surface().get_size()
    if self.x + float(self.width) / width < astronaut.x:
      return False
    if astronaut.x + float(astronaut.width) / width < self.x:
      return False
    if self.y + float(self.height) / height < astronaut.y:
      return False
    if astronaut.y + float(astronaut.height) / height < self.y:
      return False
    return True
  def hide(self):
    self.x = -1000000
    self.y = -1000000

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
  pygame.mixer.init()
  right_sound = pygame.mixer.Sound('./sounds/right.wav')
  wrong_sound = pygame.mixer.Sound('./sounds/wrong.wav')
  pygame.mixer.music.load('./sounds/asteroid-fun.mp3')
  pygame.mixer.music.play(loops = -1)
  # set background and screen size
  screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
  width, height = pygame.display.get_surface().get_size()
  background = Surface('./images/bg5.jpg')
  background.resize(width, height)
  astronaut = Astronaut(['./images/astronaut-stand.png', './images/astronaut-walk1.png', './images/astronaut-walk2.png'], './images/astronaut-lift.png')
  astronaut.resize(width, height)
  ufo_images = ['./images/red-ship.png', './images/blue-ship.png', './images/orange-ship.png']
  surfaces = [background, astronaut]
  math = Math()
  font = pygame.font.Font(None, 25)
  white = (255, 255, 255)
  math_text = font.render(math.expression + ' = ?', True, white)
  target_text = font.render('Target', True, white)
  lives = 5
  lives_text = font.render('Lives: ' + str(lives), True, white)
  score = 0
  score_text = font.render('Score: ' + str(score), True, white)
  wrong_text = font.render('Wrong answer!  You lose a life!', True, white)
  right_text = font.render('Correct!  50 points!', True, white)
  game_over_text = font.render('Game Over.  Hit Enter to play again!', True, white)
  stop_game = False
  add_ufo_time = 1500
  num_ufos = 4
  ufo_i = 0
  ufos = []
  wrong_answer_i = 0
  right_answer = False
  wrong_answer = False
  target_answer_position = random.randint(0, num_ufos - 1)
  game_over = False
  while not stop_game:
    for event in pygame.event.get():
      if not game_over:
        if event.type == pygame.KEYDOWN:
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
      if game_over:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            score = 0
            lives = 5
            score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
            lives_text = font.render('Lives: ' + str(lives), True, white)
            astronaut.reset()
            math = Math()
            ufos = []
            math_text = font.render(math.expression + ' = ?', True, (255, 255, 255))
            ufo_i = 0
            wrong_answer_i = 0
            game_over = False
            target_answer_position = random.randint(0, num_ufos - 1)
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          width, height = (800, 600)
          screen, surfaces = resize(width, height, screen, surfaces)
      if event.type == pygame.VIDEORESIZE:
        width, height = event.dict['size']
        screen, surfaces = resize(width, height, screen, surfaces)
      if event.type == pygame.QUIT:
        stop_game = True
    if pygame.time.get_ticks() > add_ufo_time:
      if ufo_i < num_ufos:
        if ufo_i == target_answer_position:
          ufos.append(UFO(ufo_images[ufo_i % 3], math.target_answer, True))
        else:
          ufos.append(UFO(ufo_images[ufo_i % 3], math.wrong_answers[wrong_answer_i], False))
          wrong_answer_i += 1
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
      if ufo.collide(astronaut):
        if ufo.target:
          score += 50
          score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
          astronaut.reset()
          math = Math()
          ufos = []
          math_text = font.render(math.expression + ' = ?', True, (255, 255, 255))
          ufo_i = 0
          wrong_answer_i = 0
          right_answer = True
          right_answer_time = pygame.time.get_ticks() + 1000
        else:
          lives -= 1
          lives_text = font.render('Lives: ' + str(lives), True, (255, 255, 255))
          astronaut.reset()
          wrong_answer = True
          wrong_answer_time = pygame.time.get_ticks() + 1000
    screen.fill((0, 0, 0))
    background.blit(screen)
    if lives < 1:
      game_over = True
      screen.blit(game_over_text, (0.5 * width - game_over_text.get_width() / 2, 0.3 * height))
      for ufo in ufos:
        ufo.hide()
      astronaut.hide()
    if not game_over:
      astronaut.blit(screen, width, height)
      for ufo in ufos:
        ufo.blit(screen, target_text, width, height)
      screen.blit(math_text, (0.5 * width - math_text.get_width() / 2, 0.1 * height))
      screen.blit(score_text, (0.01 * width, 0.01 * height))
      screen.blit(lives_text, (width - 0.1 * width, 0.01 * height))
      if right_answer:
        screen.blit(right_text, (0.5 * width - right_text.get_width() / 2, 0.5 * height))
        right_sound.play()
        if pygame.time.get_ticks() > right_answer_time:
          right_answer = False
          target_answer_position = random.randint(0, num_ufos - 1)
      elif wrong_answer:
        screen.blit(wrong_text, (0.5 * width - wrong_text.get_width() / 2, 0.5 * height))
        wrong_sound.play()
        if pygame.time.get_ticks() > wrong_answer_time:
          wrong_answer = False
    
    pygame.display.update()
    clock.tick(60)
    frame += 1
  pygame.quit()

if __name__ == '__main__':
  main()

# import cProfile as profile
# profile.run('main()')