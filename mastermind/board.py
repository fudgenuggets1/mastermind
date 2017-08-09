import pygame, words, random
from colors import *


class Circle():

	def __init__(self, x, y, w=20, h=20, color=WHITE, action=None):

		self.x, self.y = x, y
		self.w, self.h = w, h
		self.color = color
		self.action = action

	def clicked(self):
		if self.action:
			self.action(self.color)

	def update(self, screen):
		c = self.w/2
		pygame.draw.circle(screen, self.color, (self.x+c, self.y+c), c+1)
		

class Peg_Slot(Circle):

	def __init__(self, x, y, index, action):
		Circle.__init__(self, x, y, color=BLACK, action=action)

		self.index = index

	def clicked(self):
		self.action(self.index)

class Code_Peg(Circle):

	def __init__(self, x, y, color, action=None):
		Circle.__init__(self, x, y, color=color, action=action)


class Key_Peg(Circle):

	def __init__(self, x, y, color=WHITE):
		Circle.__init__(self, x, y, 10, 10, color)

class Button():

	def __init__(self, x, y, w, h, msg, action):

		self.x, self.y = x, y
		self.w, self.h = w, h
		self.msg = msg
		self.action = action

	def clicked(self):
		self.action()

	def update(self, screen):
		pygame.draw.rect(screen, BLUE, (self.x, self.y, self.w, self.h))
		words.text_to_screen(screen, self.msg, self.x + (self.w/2), self.y + (self.h/2))


class Board():

	def __init__(self):

		self.question_mark = pygame.image.load('images/question_mark.png')
		self.pieces = []
		self.current_pegs = []

		self.new_game()

	def new_game(self):	

		self.level = 1
		self.mouse_color = None
		self.game_over = False
		self.current_pegs[:] = []

		self.pieces[:] = []
		self.pieces = [Button(420, 350, 100, 30, "Guess", self.submit_guess), Button(10, 350, 130, 30, "New Game", self.new_game)]
		self.base_colors = [BLUE, GREEN, RED, YELLOW, WHITE, ORANGE, HOT_PINK, PURPLE]
		i = 0
		for y in range(150, 290, 35):
			x = 435
			self.pieces.append(Code_Peg(x, y, self.base_colors[i], self.set_mouse_color))
			i+=1
			x+=35
			self.pieces.append(Code_Peg(x, y, self.base_colors[i], self.set_mouse_color))
			i+=1

		self.set_random_code()
		self.set_peg_slots()

	def set_random_code(self):
		colors = set([])
		while len(colors) < 4:
			colors.add(random.choice(self.base_colors))
		self.code_colors = list(colors)

	def set_mouse_color(self, color):
		self.mouse_color = color

	def set_peg_slots(self):
		self.current_pegs[:] = []
		if self.level == 9:
			self.game_over = True
			return
		level = self.level * 40
		y = 400 - level
		i = 0
		for x in range(228, 360, 35):
			self.current_pegs.append(Peg_Slot(x, y, i, self.add_peg))
			i+=1

	def add_peg(self, index):
		if self.mouse_color:
			color = self.mouse_color
		else:
			color = BLACK

		level = self.level * 40
		y = 400 - level
		x = 35 * index + 1
		x += 228
		self.current_pegs[index].color=color
		self.set_mouse_color(None)

	def set_code_pegs(self):
		level = self.level * 40
		y = 400 - level
		for x in range(228, 360, 35):
			self.pieces.append(Code_Peg(x, y, random.choice(self.base_colors)))
		
	def set_key_pegs(self, colors):
		level = self.level * 40
		for_y = 398 - level
		cap = for_y + 30
		i = 0
		for x in range(184, 204, 15):
			for y in range(for_y, cap, 15):
				if i+1 > len(colors):
					return
				self.pieces.append(Key_Peg(x, y, colors[i]))
				i+=1

	def check_peg_slots(self):
		ready = True
		for peg in self.current_pegs:
			if peg.color == BLACK:
				ready = False
				break
		return ready

	def submit_guess(self):
		if self.check_peg_slots():
			self.pieces.extend(self.current_pegs)
			self.compare_pegs()
			self.level += 1
			self.set_peg_slots()

	def compare_pegs(self):
		guessed_colors = set([])
		key_colors = []
		for x in range(4):
			if self.current_pegs[x].color == self.code_colors[x]:
				key_colors.append(RED)
				guessed_colors.add(self.code_colors[x])
				continue
		for x in range(4):
			for y in range(4):
				if x == y or self.code_colors[y] in guessed_colors:
					pass
				elif self.current_pegs[x].color == self.code_colors[y]:
					key_colors.append(WHITE)
					guessed_colors.add(self.code_colors[y])
					
		if len(key_colors):
			self.set_key_pegs(key_colors)
			if len(key_colors) == 4 and len(set(key_colors)) == 1 and key_colors[0] == RED:
				self.game_over = True

	def update(self, screen):
		for piece in self.pieces:
			piece.update(screen)
		for circle in self.current_pegs:
			circle.update(screen)
		if self.mouse_color:
			pos = pygame.mouse.get_pos()
			x = pos[0]
			y = pos[1]
			pygame.draw.circle(screen, self.mouse_color, (x, y), 11)
		if not self.game_over:
			for x in range(228, 360, 35):
				screen.blit(self.question_mark, (x, 32))
		else:	
			y = 30
			i = 0
			for x in range(228, 360, 35):
				pygame.draw.circle(screen, self.code_colors[i], (x+10, y+10), 11)
				i+=1	



	
board = Board()



