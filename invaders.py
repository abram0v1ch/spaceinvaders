#-- import libraries needed
import pygame
from time import time
import os

#-- Global constants
BASE_PATH = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_PATH, 'fonts')
IMAGE_PATH = os.path.join(BASE_PATH, 'images')
SOUND_PATH = os.path.join(BASE_PATH, 'sounds')

#-- Colors
WHITE = (255,255,255)

#-- Initialise pygame and clock
pygame.init()
clock = pygame.time.Clock()

#-- Blank screen
size = (640,480)
screen = pygame.display.set_mode(size)

#-- Title and icon of the window
pygame.display.set_caption('Space invaders')
pygame.display.set_icon(pygame.image.load(os.path.join(IMAGE_PATH, 'ship.png')))

#-- font and sound variables
font = pygame.font.Font(os.path.join(FONT_PATH, 'space_invaders.ttf'), 26)
invaderkilled = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'invaderkilled.wav'))
invadershot = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'invadershot.wav'))
playershot = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'playershot.wav'))
playerhit = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'playerhit.wav'))
background_image = pygame.image.load(os.path.join(IMAGE_PATH, 'background.jpg'))

#-- variables
last_time = time()
u_time = time()
done = False
change = 0
score = 0
lives = 5

#--Classes

#--Define the class player which is a sprite
class player(pygame.sprite.Sprite):
	# define the constructor for player
	def __init__(self):
		# call the sprite constructor
		super().__init__()
		#create a sprite with image
		self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'ship.png')).convert_alpha()
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = 300
		self.rect.y = 400
	#endfunction

	# define function to move player
	def update(self, change):
		if self.rect.x + change >= 590:
			self.rect.x = 590
			change = 0
		#endif
		if self.rect.x + change <= 0:
			self.rect.x = 0
			change = 0
		#endif
		self.rect.x = self.rect.x + change
	#endfunction

# define the class user_shot
class user_shot(pygame.sprite.Sprite):
	def __init__(self, player):
		# call the sprite constructor
		super().__init__()
		#create a sprite and fill it with color
		self.image = pygame.Surface([4, 4])
		self.image.fill(WHITE)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = player.rect.x + 24
		self.rect.y = 400
	#endfunction

	# define function to move user's bullet
	def update(self, lst):
		if self.rect.y <= 0:
			lst.remove(self)
		else:
			self.rect.y = self.rect.y - 6
		#endif
	#endfunction

#define the class enemy
class enemy(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos):
		# call the sprite constructor
		super().__init__()
		# create a sprite with image
		self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'enemy.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x_pos
		self.rect.y = y_pos
	#endfunction

	# define function to move enemy
	def update(self):
		if self.rect.x >= 620:
			self.rect.x = 0
			self.rect.y += 30
		self.rect.x += 1
		#endif
	#endfunction

# define the class enemy shot
class enemy_shot(pygame.sprite.Sprite):
	def __init__(self, enemy):
		# call the sprite constructor
		super().__init__()
		#create a sprite and fill it with color
		self.image = pygame.Surface([4, 4])
		self.image.fill(WHITE)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = enemy.rect.x + 8
		self.rect.y = enemy.rect.y + 16
	#endfunction

	# define function to move enemy's bullet
	def update(self, lst):
		if self.rect.y >= 476:
			lst.remove(self)
		else:
			self.rect.x += 1
			self.rect.y = self.rect.y + 6
		#endif
	#endfunction

# list of the user shots
shot_list = pygame.sprite.Group()

# list of the enemies shots
en_shot_list = pygame.sprite.Group()

# list of all sprites except shots and enemies
all_sprites_list = pygame.sprite.Group()

# list of enemies
all_enemies_list = pygame.sprite.Group()

# define player
player = player()

# add player to the list
all_sprites_list.add(player)

# main menu function
def main(done, change, score, lives, last_time, u_time):
	#main loop
	while not done:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				game(done, change, score, lives, last_time, u_time)
			#endif
		#endfor

		#initialize background
		screen.blit(background_image, [0, 0])

		#define text
		f_line = font.render('Space invaders', False, WHITE)
		s_line = font.render('Press any key to start', False, WHITE)

		#draw text
		screen.blit(f_line,(190,175))
		screen.blit(s_line,(130,250))

		#--flip display to reveal new position of objects
		pygame.display.flip()
		clock.tick(60)
	#endwhile
#endfunction

# game function
def game(done, change, score, lives, last_time, u_time):

	# initialize enemies
	for y in range(1, 4):
		for x in range(1, 9):
			enemy_object = enemy(x * 70, 30 + y * 60)
			all_enemies_list.add(enemy_object)
		#endfor
	#endfor

###-- Game Loop
	while not done:
		#check user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					change = -3
				elif event.key == pygame.K_RIGHT:
					change = 3
				elif event.key == pygame.K_SPACE:
					if time()-u_time > 0.5:
						shot_list.add(user_shot(player))
						playershot.play()
						u_time = time()
					#endif
				#endif
			#endif
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					change = 0
				#endif
			#endif
		#endfor

		# Game logic goes after this comment

		en_ar = [] # list of enemies that can shoot

		# add all enemies to list en_ar; remove enemies that can't shoot from list en_ar
		# I wasn't able to do it in another way :(
		for x in all_enemies_list:
			en_ar.append(x)
			for y in all_enemies_list:
				if x.rect.y == y.rect.y:
					pass
				elif x.rect.y + 60 == y.rect.y and x.rect.x == y.rect.x:
					en_ar.remove(x)
					break
				elif x.rect.y + 120 == y.rect.y and x.rect.x == y.rect.x:
					en_ar.remove(x)
					break
				elif x.rect.y + 180 == y.rect.y and x.rect.x == y.rect.x:
					en_ar.remove(x)
					break
				#endif
			#endfor
		#endfor

		# check if enemies that can shoot are able to 'see' the player; shoot with 0.7s intervals
		for x in en_ar:
			if x.rect.x - player.rect.x <= 30 and x.rect.x - player.rect.x >= -10:
				if time()-last_time > 0.7:
					en_shot_list.add(enemy_shot(x))
					invadershot.play()
					last_time = time()
				#endif
			#endif
		#endfor

		#call moving functions of sprites and groups
		player.update(change)
		shot_list.update(shot_list)
		en_shot_list.update(en_shot_list)
		all_enemies_list.update()

		# define background
		screen.blit(background_image, [0, 0])

		#define text
		score_text = font.render('Score:' + ' ' + str(score), False, WHITE)
		lives_text = font.render('Lives:' + ' ' + str(lives), False, WHITE)
		
		#-- Draw all sprites from groups, text
		all_sprites_list.draw(screen)
		shot_list.draw(screen)
		all_enemies_list.draw(screen)
		en_shot_list.draw(screen)
		screen.blit(score_text,(480,1))
		screen.blit(lives_text,(20,1))

		#check if invader was hit by player's bullet
		if pygame.sprite.groupcollide(all_enemies_list, shot_list, True, True):
			invaderkilled.play()
			score += 1
		#endif

		#check if player was hit by invader's bullet
		if pygame.sprite.groupcollide(all_sprites_list, en_shot_list, False, True):
			playerhit.play()
			lives -= 1
		#endif

		#--flip display to reveal new position of objects
		pygame.display.flip()

		#check if all enemies are killed or if player has no more lives
		if score == 24 or lives == 0:
			screen.blit(background_image, [0, 0])
			end(done, score, lives)
			done = True
			all_enemies_list.empty()
		#endif

		clock.tick(60)
	#endwhile

# function of the end of the game
def end(done, score, lives):
	#main loop
	while not done:
		#check if player wins
		if score == 24:
			# define text
			f_line = font.render('You won!', False, WHITE)
			s_line = font.render('Press ESCAPE to exit', False, WHITE)
			t_line = font.render('Press ENTER to play again', False, WHITE)

			# draw text
			screen.blit(f_line,(260,150))
			screen.blit(s_line,(150,225))
			screen.blit(t_line,(110,300))

			#--flip display to reveal new position of objects
			pygame.display.flip()

			#check user input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						done = True
					elif event.key == pygame.K_ESCAPE:
						exit()
					#endif
				#endif
			#endfor

			clock.tick(60)
		#endif

		#check if player loses
		if lives == 0:
			#define text
			f_line = font.render('You lost', False, WHITE)
			s_line = font.render('Press ESCAPE to exit', False, WHITE)
			t_line = font.render('Press ENTER to play again', False, WHITE)

			#draw text
			screen.blit(f_line,(250,150))
			screen.blit(s_line,(150,225))
			screen.blit(t_line,(110,300))

			#--flip display to reveal new position of objects
			pygame.display.flip()

			#check user input
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						done = True
					elif event.key == pygame.K_ESCAPE:
						exit()
					#endif
				#endif
			#endfor

			clock.tick(60)

#call main function
main(done, change, score, lives, last_time, u_time)

###--End of game loop
pygame.quit()
