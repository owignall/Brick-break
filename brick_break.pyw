'''
This is a brick breaking paddle game with a number of levels
Could add:
  - Additional levels
  - Additional power ups
'''
import pygame
import random
pygame.init()
pygame.font.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Brick Break')
clock = pygame.time.Clock()
class paddle(object):
	def __init__(self, x, y, colour, vel, width, height):
		self.x = x
		self.y = y
		self.colour = colour
		self.vel = vel
		self.width = width
		self.height = height
	def draw_paddle(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
class ball(object):
	def __init__(self, x, y, colour, xvel, yvel, radius):
		self.x = x
		self.y = y
		self.colour = colour
		self.xvel = xvel
		self.yvel = yvel
		self.radius = radius
	def draw_ball(self, win):
		pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)
class ball2(ball):
	pass
class block(object):
	def __init__(self, x, y, colour, vel, width, height):
		self.x = x
		self.y = y
		self.xstart = x
		self.ystart = y
		self.colour = colour
		self.vel = vel
		self.width = width
		self.height = height
	def draw_block(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
class block2(block):
	pass
class item(object):
	def __init__(self, x, y, typ, colour, width, height):
		self.x = x
		self.y = y
		self.typ = typ
		self.colour = colour
		self.vel = 3
		self.width = width
		self.height = height
	def draw_item(self, win):
		pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.width, self.height))
		pygame.draw.rect(win, self.colour, ((self.x + 1), (self.y + 1), (8), (8)))
class item2(item):
	pass
def draw_walls():
	pygame.draw.rect(win, (200, 200, 215), (0, 0, 6, 500))
	pygame.draw.rect(win, (200, 200, 215), (494, 0, 6, 500))
	pygame.draw.rect(win, (200, 200, 215), (0, 0, 500, 6))
def draw_clock():
	font_clock = pygame.font.SysFont('timesnewroman', 12)
	text_clock = font_clock.render(frames_to_time(frames_taken), False, (255, 255, 255))
	win.blit(text_clock, (10, 480))
def draw():
	win.fill((0, 0, 0))
	if clock:
		draw_clock()
	pad.draw_paddle(win)
	for ball in balls:
		ball.draw_ball(win)
	for block in blocks:
		block.draw_block(win)
	for item in items:
		item.draw_item(win)
	draw_walls()
	pygame.display.update()
def game_over():
	game_over_sound.play()
	for n in range(5):
		win.fill((0, 0, 0))
		pygame.display.update()
		pygame.time.delay(200)
		draw()
		pygame.time.delay(200)
def new_level():
	level_up_sound.play()
	for n in range(3):
		win.fill((0, 0, 0))
		pad.draw_paddle(win)
		pygame.display.update()
		pygame.time.delay(100)
		draw()
		pygame.time.delay(100)
def frames_to_time(frames):
	seconds_total = round((frames * 15) / 1000)
	seconds = seconds_total
	minutes = 0
	while seconds > 60:
		seconds -= 60
		minutes += 1
	if seconds < 10:
		seconds = '0%s' %(seconds)
	return '%s:%s' % (minutes, seconds)
def game_complete():
	game_completed = True
	font = pygame.font.SysFont('timesnewroman', 35)
	font_2 = pygame.font.SysFont('timesnewroman', 25)
	text = font.render('Game Complete!', False, (255, 255, 255))
	text_2 = font_2.render('Time take:%s' %(frames_to_time(frames_taken)), False, (255, 255, 255))
	falling_balls = []
	count = 0
	while game_completed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				game_completed = False
		if count == 0:
			x = round(random.random() * 500)
			falling_balls.append(ball2(x, 0, (255, 0, 0), 0, 5, 6))
			count = 5
		count -= 1
		win.fill((0, 0, 0))
		for ball in falling_balls:
			ball.y += ball.yvel
			ball.draw_ball(win)
		pad.draw_paddle(win)
		draw_walls()
		win.blit(text, (130, 200))
		win.blit(text_2, (170, 280))
		pygame.display.update()
		pygame.time.delay(15)
'''Game sound variables'''
block_break_sound = pygame.mixer.Sound('Game sounds/block_break.wav')
level_up_sound = pygame.mixer.Sound('Game sounds/level_up.wav')
paddle_hit_sound = pygame.mixer.Sound('Game sounds/paddle_hit.wav')
wall_hit_sound = pygame.mixer.Sound('Game sounds/wall_hit.wav')
power_up_sound = pygame.mixer.Sound('Game sounds/power_up.wav')
power_down_sound = pygame.mixer.Sound('Game sounds/power_down.wav')
game_over_sound = pygame.mixer.Sound('Game sounds/game_over.wav')
game_complete_sound = pygame.mixer.Sound('Game sounds/game_complete.wav')
pad = paddle(230, 480, (200, 200, 215), 4, 60, 8)
level = 0
total_levels = 5
'''Ball variables'''
balls = []
ball_limit = 1
ball_delay = 0
'''Other lists and variables'''
blocks = []
items = []
drop_percentage = 0.3
big_pad_count = 0
fast_ball_count = 0
power_ball_count = 0
extra_ball_count = 0
'''Main loop'''
frames_taken = 0
game_completed = False
run = True
clock = False
clock_cool = 0
while run:
	pygame.time.delay(15)
	frames_taken += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	for ball in balls:
		'''When ball hits paddle'''
		if ball.y + ball.radius >= pad.y and ball.y - ball.radius <= pad.y + pad.height and ball.x >= pad.x and ball.x <= pad.x + pad.width:
			ball.yvel *= -1
			paddle_hit_sound.play()
			center = pad.x + (pad.width / 2)
			if int(round((ball.x - center)/6)) == 0:
				if ball.x - center > 0:
					ball.xvel = 1
				elif ball.x - center < 0:
					ball.xvel = -1
				else: ball.xvel = 0
			else: 
				ball.xvel = int(round((ball.x - center)/6))
		'''Ball momentum, boundary bounce and game over'''
		if ball.y - 6 >= ball.radius and ball.y <= 500 - ball.radius:
			ball.y += ball.yvel
		elif ball.y > 500 - ball.radius:
			balls.pop(balls.index(ball))
			ball_limit -= 1
			if len(balls) == 0:	
				game_over()
				level -= 1
				ball_limit = 1
				fast_ball_count = 1
				power_ball_count = 1
				extra_ball_count = 1
				if big_pad_count > 1:
					big_pad_count = 1
				for item in range(len(items)):
					items.pop(0)	
				for block in range(len(blocks)):
					blocks.pop(0)
		else: 
			ball.yvel *= -1
			ball.y += ball.yvel
			wall_hit_sound.play()
		if ball.x - 6 >= ball.radius and ball.x <= 494 - ball.radius:
			ball.x += ball.xvel
		else: 
			ball.xvel *= -1
			ball.x += ball.xvel
			wall_hit_sound.play()
	for block in blocks:
		for ball in balls:
			'''Block collision physics'''
			if ball.x + ball.radius >= block.x and ball.x - ball.radius <= block.x + block.width and ball.y - ball.radius <= block.y + block.height and ball.y + ball.radius >= block.y:
				if power_ball_count == 0:
					if (ball.x - ball.xvel + ball.radius) >= block.x and (ball.x - ball.xvel - ball.radius) <= block.x + block.width:
						ball.yvel *= -1
					elif (ball.y - ball.yvel - ball.radius) <= block.y + block.height and (ball.y - ball.yvel + ball.radius) >= block.y:
						ball.xvel *= -1
				'''Item generation'''
				chance = random.random()
				if chance <= drop_percentage:
					type_percentage = random.random()
					if type_percentage < 0.3:
						items.append(item2((block.x + 5), (block.y + 5), 'Big paddle', (0, 0, 255), 10, 10))
					elif type_percentage < 0.6:
						items.append(item2((block.x + 5), (block.y + 5), 'Fast ball', (255, 0, 0), 10, 10))
					elif type_percentage < 0.8:
						items.append(item2((block.x + 5), (block.y + 5), 'Power ball', (255, 255, 0), 10, 10))
					elif type_percentage < 1:
						items.append(item2((block.x + 5), (block.y + 5), 'Extra balls', (0, 255, 0), 10, 10))
				blocks.pop(blocks.index(block))
				block_break_sound.play()
		if block.x >= block.xstart - 100 and block.x <= block.xstart + 100:
			block.x += block.vel
		else:
			block.vel *= -1
			block.x += block.vel
	for item in items:
		if item.y <= 500:
			item.y += item.vel
		else: items.pop(items.index(item))
		if (item.y + item.height) >= pad.y and item.y <= pad.y + pad.height and item.x + item.width >= pad.x and item.x <= pad.x + pad.width:
			'''If item is caught'''
			if item.typ == 'Big paddle' and big_pad_count == 0:
				power_up_sound.play()
				pad.x -= 12
				pad.width += 24
				big_pad_count = 1000
			elif item.typ == 'Big paddle' and big_pad_count > 0:
				big_pad_count = 1000
			if item.typ == 'Fast ball' and fast_ball_count == 0:
				power_down_sound.play()
				for ball in balls:
					if ball.yvel > 0:
						ball.yvel = 7
					if ball.yvel < 0:
						ball.yvel = -7
				fast_ball_count = 1000
			elif item.typ == 'Fast ball' and fast_ball_count > 0:
				fast_ball_count = 1000
			if item.typ == 'Power ball':
				power_up_sound.play()
				power_ball_count = 1000
			if item.typ == 'Extra balls':
				power_up_sound.play()
				ball_limit = 5
				extra_ball_count = 1000
			items.pop(items.index(item))
	keys = pygame.key.get_pressed()
	'''Controls'''
	if keys[pygame.K_RIGHT] and (pad.x + pad.width + pad.vel) <= 495:
		pad.x += pad.vel
	if keys[pygame.K_LEFT] and (pad.x - pad.vel) >= 5:
		pad.x -= pad.vel
	if keys[pygame.K_UP] and len(balls) < ball_limit and ball_delay == 0:
		balls.append(ball2((pad.x + (pad.width//2) + 1), (pad.y - 6), (255, 0, 0), 0, 5, 6))
		ball_delay = 20
	if keys[pygame.K_SPACE]:
		clock = True
		clock_cool = 100
	if clock_cool == 0:
		clock = False
	clock_cool -= 1
	if ball_delay > 0:
		ball_delay -= 1
	'''Item timmers'''
	if big_pad_count == 1:
		pad.x += 12
		pad.width -= 24
		big_pad_count -= 1
	elif big_pad_count > 0:
		big_pad_count -= 1
	if fast_ball_count == 1:
		for ball in balls:
			if ball.yvel > 0:
				ball.yvel = 5
			if ball.yvel < 0:
				ball.yvel = -5
		fast_ball_count -= 1
	elif fast_ball_count > 0:
		fast_ball_count -= 1
	if power_ball_count > 0:
		power_ball_count -= 1
	if extra_ball_count == 1:
		ball_limit = 1
		extra_ball_count -= 1
	elif extra_ball_count > 0:
		extra_ball_count -= 1
	if len(blocks) == 0 and level < total_levels:
		'''Level loading'''
		level += 1
		pygame.time.delay(200)
		if level == 1:
			for r in range(2):
				for c in range(5):
					blocks.append(block2((165 + (30 * c)), (50 + (25 * r)), (52, 164, 235), 0, 20, 20))
		if level == 2:
			changer = -1
			for r in range(3):
				changer *= -1
				for c in range(10):
					blocks.append(block2((100 + (30 * c)), (30 + (25 * r)), (235, 141, 19), (changer * 2), 20, 20))
		if level == 3:
			for r in range(10):
				for c in range(10):
					blocks.append(block2((95 + (30 * c)), (50 + (25 * r)), (52, 70, 235), 0, 20, 20))
		if level == 4:
			changer = -1
			for r in range(10):
				changer *= -1
				for c in range(10):
					blocks.append(block2((95 + (30 * c)), (50 + (25 * r)), (255, 55, 0), (changer * 2), 20, 20))
		if level == 5:
			for r in range(10):
				for c in range(16):
					if (c + r) % 2 == 0:
						blocks.append(block2((10 + (30 * c)), (50 + (25 * r)), (52, 70, 235), 0, 20, 20))
		if len(balls) > 0:
			for ball in balls:
				balls.pop(balls.index(ball))
		new_level()
		ball_limit = 1
	if len(blocks) == 0 and level == total_levels:
		game_complete_sound.play()
		game_complete()
		break
	draw()