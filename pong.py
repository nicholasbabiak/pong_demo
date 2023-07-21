import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong Demo")
clock = pygame.time.Clock()
running = True
motion = False
redraw_text = True
dt = 0
screen_center = screen.get_width() / 2

ball_width = 20
ball = pygame.Rect((screen.get_width() - ball_width) / 2, (screen.get_height() - ball_width) / 2, ball_width, ball_width)

def initial_ball_vector():
	return (random.randrange(-10, 10, 1), random.randrange(-20, 20, 1))

def initial_ball_pos():
	return (screen.get_width() - ball_width) / 2, (screen.get_height() - ball_width) / 2
ball_vector_step = initial_ball_vector()

def wall_sfx():
	pygame.mixer.music.load("sounds_ping_pong_8bit/ping_pong_8bit_beeep.ogg")
	pygame.mixer.music.play()

def bar_sfx():
	pygame.mixer.music.load("sounds_ping_pong_8bit/ping_pong_8bit_peeeeeep.ogg")
	pygame.mixer.music.play()

def score_sfx():
	pygame.mixer.music.load("sounds_ping_pong_8bit/ping_pong_8bit_plop.ogg")
	pygame.mixer.music.play()

player1_bar = pygame.Rect(10, screen.get_height() / 2, 30, 200)
player2_bar = pygame.Rect(screen.get_width() - 40, screen.get_height() / 2, 30, 200)

player1_score = 0
player2_score = 0

font = pygame.font.Font('/System/Library/Fonts/Supplemental/Courier New.ttf', 25)

move_amount = 8

while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")

	#pygame.draw.circle(screen, "red", ball_pos, 40)
	pygame.draw.rect(screen, "white", player1_bar)
	pygame.draw.rect(screen, "white", player2_bar)

	for i in range(10, screen.get_height() - 40, 50):
		pygame.draw.line(screen, "white", (screen_center, i), (screen_center, i + 30), 5)

	if redraw_text:
		text_player1 = font.render(f"Points: {player1_score:02}", True, "white")
		textRect_player1 = text_player1.get_rect()
		textRect_player1.center = (screen.get_width() * 0.20, 28)
		text_player2 = font.render(f"Points: {player2_score:02}", True, "white")
		textRect_player2 = text_player2.get_rect()
		textRect_player2.center = (screen.get_width() * 0.80, 28)
		redraw_text = False
	
	screen.blit(text_player1, textRect_player1)
	screen.blit(text_player2, textRect_player2)

	if motion:
		if ball.top < 0 or ball.bottom > screen.get_height():
			ball_vector_step = (ball_vector_step[0], ball_vector_step[1] * -1)
			wall_sfx()
		
		ball.move_ip(ball_vector_step)

		if ball.left < 0 or ball.right > screen.get_width():
			if ball.left < 0:
				player1_score += 1
			else:
				player2_score += 1
			
			redraw_text = True
			motion = False
			ball_vector_step = initial_ball_vector()
			ball.centerx, ball.centery = initial_ball_pos()
			score_sfx()
		

	pygame.draw.rect(screen, "white", ball)

	keys = pygame.key.get_pressed()
	if keys[pygame.K_q] and player1_bar.top > 10:
		player1_bar.move_ip(0, move_amount * -1)
		motion = True
	if keys[pygame.K_a] and player1_bar.bottom < screen.get_height() - 10:
		player1_bar.move_ip(0, move_amount)
		motion = True
	if keys[pygame.K_p] and player2_bar.top > 10:
		player2_bar.move_ip(0, move_amount * -1)
		motion = True
	if keys[pygame.K_l] and player2_bar.bottom < screen.get_height() - 10:
		player2_bar.move_ip(0, move_amount)
		motion = True
	if keys[pygame.K_SPACE]:
		motion = False
		ball_vector_step = initial_ball_vector()
		ball.centerx, ball.centery = initial_ball_pos()


	if ball.colliderect(player1_bar) or ball.colliderect(player2_bar):
		ball_vector_step = (ball_vector_step[0] * -1, ball_vector_step[1])
		bar_sfx()

	# flip() the display to put your work on screen
	pygame.display.flip()

	# limits FPS to 60
	# dt is delta time in seconds since last frame, used for framerate-
	# independent physics.
	dt = clock.tick(60) / 1000

pygame.quit()