import sys
import pygame
import os
from random import randint, choice

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

WIDTH = 25
HEIGHT = 20
FPS = 60
SCALE = 2
BLOCKSIZE = 16
RUNNING = True
APPRUN = True
PAUSE = False
SCORE = 0
PATH = os.getcwd()
UPKEY = pygame.K_UP
DOWNKEY = pygame.K_DOWN
LEFTKEY = pygame.K_LEFT
RIGHTKEY = pygame.K_RIGHT
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,214,42)
orange = (255,103,0)
magenta = (255,0,255)
purple = (128,0,128)
pink =  (255,105,180)
lightblue = (143,252,255)
gray = (128, 128, 128)
lightgray = (200, 200, 200)
SOUNDTRACK = None
BACKGROUND = black
objects = []
clock = pygame.time.Clock()
icon = pygame.transform.scale(pygame.image.load(PATH+"/Sprites/sputefix.png"), (32, 32))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH*BLOCKSIZE*SCALE, HEIGHT*BLOCKSIZE*SCALE))

def excepthook(type, value, traceback, oldhook=sys.excepthook):
	 oldhook(type, value, traceback)
	 pygame.quit()
	 input("Press ENTER to close.")
sys.excepthook = excepthook
class Sprite:
	 def __init__(self, filename, PATH):
		  self.sheet = pygame.image.load(PATH + filename)
		  self.rect = self.sheet.get_rect()
		  self.cols = self.rect.width/BLOCKSIZE
		  self.rows = self.rect.height/BLOCKSIZE
		  self.tot_cells = self.cols * self.rows
		  self.sheet = pygame.transform.scale(self.sheet, (BLOCKSIZE*SCALE*self.cols, BLOCKSIZE*SCALE*self.rows))
		  self.rect = self.sheet.get_rect()
		  self.w = self.rect.width / self.cols
		  self.h = self.rect.height / self.rows

		  self.cells = list(
				[(index % self.cols * self.w, index / self.cols * self.h, self.w, self.h) for index in range(self.tot_cells)])

	 def draw(self, index, surface, x, y):
		  surface.blit(self.sheet, (x, y), self.cells[index])

def spriteLoad(filename, PATH):
	 image = Sprite(filename, PATH)
	 return image, (image.w, image.h)

class Object:
	def __init__(self, x, y, image, type, color, display):
		 self.x = x
		 self.y = y
		 self.vx = 0
		 self.vy = 0
		 self.image = image
		 try:
			self.sprite, self.size = spriteLoad(image, PATH+"/Sprites/")
			self.shrect = pygame.Rect(0, 0, self.sprite.w, self.sprite.h)
		 except:
			self.sprite = None
			self.size = (BLOCKSIZE*SCALE, BLOCKSIZE*SCALE)
			self.shrect = pygame.Rect(0, 0, self.size[0], self.size[1])
		 self.type = type
		  
		 self.color = color
		 self.display = display
		 self.animation = "IDLE"
		 self.animations = {"IDLE":[0]}
		 self.maxlatency = 0
		 self.latency = 0
		 self.index = 0

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.shrect.x = self.x
		self.shrect.y = self.y
		self.latency -= 1
		if self.latency <= 0:
			self.latency = self.maxlatency
			self.index += 1
		if self.index >= len(self.animations[self.animation]):
			self.index = 0

	def draw(self):
		if self.sprite:
			self.sprite.draw(self.animations[self.animation][self.index], self.display, self.x, self.y)
		else:
			pygame.draw.rect(self.display, self.color, (self.x, self.y, self.size[0], self.size[1]))

def clearScreen():
	screen.fill(BACKGROUND)

def display():
	pygame.display.update()
	clock.tick(FPS)

def resizeScreen(width, height):
	WIDTH = width
	HEIGHT = height
	screen = pygame.display.set_mode((WIDTH * BLOCKSIZE * SCALE, HEIGHT * BLOCKSIZE * SCALE))

def screenTitle(title):
	pygame.display.set_caption(title)
screenTitle("Sputefix Game Engine")

def toggle(boolean):
	if not boolean:
		 return True
	return False

def text_objects(text, color, fontt):
	textSurface = fontt.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message(msg, color, x, y, fontsize):
	font = pygame.font.Font(PATH+"/Font/amstrad_cpc464.ttf", fontsize)
	textSurf, textRect = text_objects(msg, color, font)
	textRect.center = x, y
	screen.blit(textSurf, textRect)

def events():
	global RUNNING, PAUSE
	pygameEvents = pygame.event.get()
	for event in pygameEvents:
		if event.type == pygame.QUIT:
			if not DONECHOOSING:
				APPRUN = False
			else:
				RUNNING = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if not DONECHOOSING:
					APPRUN = False
				else:
					RUNNING = False
			if event.key == pygame.K_RETURN:
				PAUSE = toggle(PAUSE)
	return pygameEvents

def keydown(key, event):
	 if event.type == pygame.KEYDOWN:
		  if event.key == key:
				return True
	 return False

def keyup(key, event):
	 if event.type == pygame.KEYUP:
		  if event.key == key:
				return True
	 return False

def genMap(filename, idSet):
	 file = open(PATH+"/Levels/"+filename, "r")
	 file = file.read()
	 file = file.split("\n")
	 for i in range(len(file)):
		  file[i] = file[i].split(", ")
	 for y in range(len(file)):
		  for x in range(len(file[y])):
				if file[y][x] in idSet:
					 objectsAdd(create(x, y, idSet[file[y][x]][1], idSet[file[y][x]][2], idSet[file[y][x]][0]))

def update(object):
	 object.update()

def draw(object):
	 object.draw()

def create(x, y, sprite, color, type):
	 object = Object(x * BLOCKSIZE * SCALE, y * BLOCKSIZE * SCALE, sprite, type, color, screen)
	 return object

def objectsAdd(object):
	 objects.append(object)

def objectsRemove(object):
	 objects.remove(object)

def collision(object1, object2, tags):
	 collide = False
	 # # Collisions Horizontales
	 # if object2.type in tags:
	 #	  if object1.y < object2.y + object2.size[1] and object1.y >= object2.y or object1.y + object1.size[1] <= object2.y + object2.size[1] and object1.y + object1.size[1] > object2.y:
	 #			if object1.x + object1.vx < object2.x + object2.size[0] + object2.vx and object1.x + object1.vx > object2.x + object2.vx:
	 #				 collide = True
	 #			if object1.x + object1.vx + object1.size[0] > object2.x + object2.vx and object1.x + object1.vx + object1.size[0] < object2.x + object2.size[0] + object2.vx:
	 #				 collide = True
	 #
	 #	  # Collisions Verticales
	 #	  if object1.x < object2.x + object2.size[0] and object1.x >= object2.x or object1.x + object1.size[0] <= object2.x + object2.size[0] and object1.x + object1.size[0] > object2.x:
	 #			if object1.y + object1.vy < object2.y + object2.size[1] + object2.vy and object1.y + object1.vy > object2.y + object2.vy:
	 #				 collide = True
	 #			if object1.y + object1.vy + object1.size[1] > object2.y + object2.vy and object1.y + object1.vy + object1.size[1] < object2.y + object2.size[1] + object2.vy:
	 #				 collide = True
	 if object2.type in tags:
		if object1.shrect.colliderect(object2.shrect):
			collide = True

	 return collide

def clone(object):
	 objectsAdd(create(object.x, object.y, object.image, screen, object.type))

def musicLoad(filename):
	 SOUNDTRACK = pygame.mixer.Sound(PATH+"/Sounds/Musics/"+filename)

def musicPlay():
	 SOUNDTRACK.play(-1)

def musicStop():
	 SOUNDTRACK.stop()

def soundLoad(filename):
	 return pygame.mixer.Sound(PATH+"/Sounds/SFX/"+filename)

def soundPlay(sound):
	 sound.play()

def soundStop(sound):
	 sound.stop()


CHOOSEINDEX = 0
DONECHOOSING = False
SCRIPTS = os.listdir(PATH)
erased = 0
for i in range(len(SCRIPTS)):
	 if SCRIPTS[i-erased] == "Sputefix Game Engine.py" or not SCRIPTS[i-erased][-3:] == ".py":
		  SCRIPTS.pop(i-erased)
		  erased += 1
BACKGROUND = black
while APPRUN:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			APPRUN = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				APPRUN = False
			if event.key == pygame.K_UP:
				CHOOSEINDEX -= 1
				if CHOOSEINDEX == -1:
					CHOOSEINDEX = len(SCRIPTS)-1
			if event.key == pygame.K_DOWN:
				CHOOSEINDEX += 1
				if CHOOSEINDEX == len(SCRIPTS):
					CHOOSEINDEX = 0
			if event.key == pygame.K_RETURN:
				DONECHOOSING = True

	if DONECHOOSING:
		  exec(open(PATH+"/"+SCRIPTS[CHOOSEINDEX], "r").read())
		  DONECHOOSING = False
		  RUNNING = True
		  screenTitle("Sputefix Game Engine")
		  SCORE = 0
	clearScreen()
	message("Choose a game:", white, (WIDTH*BLOCKSIZE), (HEIGHT*BLOCKSIZE)/2, 20)
	message(SCRIPTS[CHOOSEINDEX], white, (WIDTH*BLOCKSIZE), ((HEIGHT*BLOCKSIZE)/4)*3, 25)
	message("Press ENTER to run.", white, (WIDTH*BLOCKSIZE), (HEIGHT*BLOCKSIZE), 20)
	display()
