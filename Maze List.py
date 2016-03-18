import random
import pygame
import sys


boardx = 250
boardy = 250
root = [[0,0]]

# Check that two lists don't share any elements
def overlap(ls1,ls2):
	x = False
	for i in ls1:
		x = (x or (i in ls2))
	return x

# Make sure the specified position is not adjacent to any filled squares
def isolated(ls,psn):
	assert isinstance(psn,list) and len(psn) == 2
	x = psn[0]
	y = psn[1]
	surrounding = [[x-1,y+1],[x,y+1],[x+1,y+1],
		  [x-1,y],[x,y],[x+1,y],
		  [x-1,y-1],[x,y-1],[x+1,y-1]]
	def search(element):
		return element in surrounding
	return filter(search,ls) == []

directions = ["up","down","left","right"]
# Given a position and a direction to add a new square, give a list of
# squares that should be empty
def empties(psn, direction):
	assert isinstance(direction,str)
	assert isinstance(psn,list) and len(psn) == 2
	x = psn[0]
	y = psn[1]
	if direction == "up":
		return [[x-1,y+1],[x,y+1],[x+1,y+1],
				[x-1,y+2],[x,y+2],[x+1,y+2]]
	elif direction == "down":
		return [[x-1,y-1],[x,y-1],[x+1,y-1],
				[x-1,y-2],[x,y-2],[x+1,y-2]]
	elif direction == "right":
		return [[x+1,y-1],[x+1,y],[x+1,y+1],
				[x+2,y-1],[x+2,y],[x+2,y+1]]
	elif direction == "left":
		return [[x-1,y-1],[x-1,y],[x-1,y+1],
				[x-2,y-1],[x-2,y],[x-2,y+1]]
	else:
		error("Invalid direction!")

# Check that the given position is on the board
def within(psn):
	assert isinstance(psn, list) and len(psn) == 2
	return (0 <= psn[0] <= boardx-1) and (0 <= psn[1] <= boardy-1)

# Add a square at the given direction
def add(psn, direction):
	assert isinstance(psn, list) and len(psn) == 2
	if direction == "left":
		return [psn[0]-1,psn[1]]
	elif direction == "right":
		return [psn[0]+1,psn[1]]
	elif direction == "up":
		return [psn[0],psn[1]+1]
	elif direction == "down":
		return [psn[0],psn[1]-1]
	else:
		error("Invalid direction!")

def seed(ls,i):
	assert isinstance(ls,list)
	psn = ls[i]
	def check(direction):
		return (not overlap(empties(psn,direction),ls))
	def listmoves(direction):
		return add(psn,direction)
	possible = filter(within,map(listmoves,filter(check, directions)))
	if possible == []:
		return ls
	else:
		new = random.choice(possible)
		ls.append(new)
		return seed(ls,i+1)

def gen2_aux(ls,i):
	assert isinstance(ls,list)
	psn = ls[i]
	def check(direction):
		return (not overlap(empties(psn,direction),ls))
	def listmoves(direction):
		return add(psn,direction)
	possible = filter(within,map(listmoves,filter(check, directions)))
	if possible == []:
		return ls
	else:
		new = random.choice(possible)
		ls.append(new)
		return gen2_aux(ls,len(ls)-1)

def gen2(ls):
	i = 0
	seed(ls,0)
	for coord in ls:
		gen2_aux(ls,i)
		i = i+1

def gen1_aux(ls,i):
	l = len(ls)
	assert isinstance(ls,list)
	
	while i < l-1:
		psn = ls[i]
		def check(direction):
			return (not overlap(empties(psn,direction),ls))
		def listmoves(direction):
			return add(psn,direction)
		possible = filter(within,map(listmoves,filter(check, directions)))
		if possible == []:
			i = i+1
		else:
			new = random.choice(possible)
			ls.append(new)
			i = i+1
	return ls

def gen1(ls):
	seed(ls,0)
	for i in range(boardx*boardy/10):
		print i
		gen1_aux(ls,0)

"Rendering"
r = 15 #square size
def render(ls):
	pygame.init()
	display=pygame.display.set_mode(((boardx+2)*r,(boardy+2)*r),0,32)
	fore = (255,255,255)
	back = (0,0,20)
	red = (255,0,0)
	display.fill(back)
	i = 0
	font = pygame.font.Font(None, int(r*0.75))
	for coord in ls:
		#txt = font.render(str(i),1,back,back)
		pygame.draw.rect(display,fore,((coord[0]+1)*r,(coord[1]+1)*r,r,r))
		#display.blit(txt, sqr, None, 0)
		i = i+1
	end_coord = max(ls)
	pygame.draw.rect(display,red,((end_coord[0]+1)*r,(end_coord[1]+1)*r,r,r))
	pygame.draw.rect(display,red,(r,r,r,r))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.image.save(display, "maze.png")
				pygame.quit()
				sys.exit()
		pygame.display.update()

#Generate the maze in list format.
gen2(root)
#Render the maze.
render(root)
