import pygame
import random
import string

# initialize pygame
pygame.init()

# set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Typing Game")

# set up the clock
clock = pygame.time.Clock()

# set up the font
font = pygame.font.SysFont("ComicSansMs", 60)

# set up the sound effects
keypress_sound = pygame.mixer.Sound("correct.wav")
gameover_sound = pygame.mixer.Sound("game_over.mp3")

background_image = pygame.image.load("background.jpg").convert()

# set up variables
word = ""
typed_word = ""
correct_letters = []
incorrect_letters = []
score = 0
lives = 3
game_over = False
power_up = None
time_remaining = 60
start_ticks = pygame.time.get_ticks()

# set up the words list
with open("words.txt", "r") as file:
    words = file.readlines()

# set up the music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# game loop
while not game_over:
    # set up the word
    if not word:
        word = random.choice(words).strip()
        typed_word = ""
        correct_letters = []
        incorrect_letters = []

        # generate a power-up randomly
        power_up_num = random.randint(1, 3)
        if power_up_num == 1:
            power_up = "Extra life"
        elif power_up_num == 2:
            power_up = "Score multiplier"
        elif power_up_num == 3:
            power_up = "Speed boost"

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.unicode in string.ascii_letters:
                keypress_sound.play()
                if event.unicode == word[len(typed_word)]:
                    correct_letters.append(event.unicode)
                    typed_word += event.unicode
                    if len(typed_word) == len(word):
                        score += 1
                        word = ""
                        # apply power-up if generated
                        if power_up == "Extra life":
                            lives += 1
                        elif power_up == "Score multiplier":
                            score *= 2
                        elif power_up == "Speed boost":
                            clock.tick(120)
                        power_up = None
                else:
                    incorrect_letters.append(event.unicode)
                    lives -= 1
                    if lives == 0:
                        gameover_sound.play()
                        game_over = True

    # calculate remaining time
    time_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_remaining = max(0, 60 - int(time_elapsed))

    # fill the screen
    screen.blit(background_image, (0, 0))

    # display the word
    word_surface = font.render(word, True, (0, 0, 0))
    word_rect = word_surface.get_rect(center=(400, 300))
    screen.blit(word_surface, word_rect)

    # display the typed letters
    typed_surface = font.render(typed_word, True, (0, 255, 0))
    typed_rect = typed_surface.get_rect(center=(400, 400))
    screen.blit(typed_surface, typed_rect)

    # display the correct letters
    for i, letter in enumerate(correct_letters):
        letter_surface = font.render(letter, True, (0, 255, 0))
        letter_rect = letter_surface.get_rect(center=(400-20*(len(correct_letters)-i), 400))
        screen.blit(letter_surface, letter_rect)

    # display the incorrect letters
    for i, letter in enumerate(incorrect_letters):
        letter_surface = font.render(letter, True, (255, 0, 0))
        letter_rect = letter_surface.get_rect(center=(400+20*(i+1), 400))
        screen.blit(letter_surface, letter_rect)

    # display the score, lives, and time remaining
    score_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_surface.get_rect(topright=(785, 10))
    screen.blit(score_surface, score_rect)

    lives_surface = font.render(f"Lives: {lives}", True, (0, 0, 0))
    lives_rect = lives_surface.get_rect(topleft=(15, 10))
    screen.blit(lives_surface, lives_rect)

    time_surface = font.render(f"Time: {time_remaining}", True, (0, 0, 0))
    time_rect = time_surface.get_rect(center=(400, 100))
    screen.blit(time_surface, time_rect)

    # update the display
    pygame.display.update()

# game over screen
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_over = False
                score = 0
                lives = 3
                time_remaining = 60
                start_ticks = pygame.time.get_ticks()
                break

    # fill the screen
    screen.fill((255, 255, 255))

    # display the game over message
    gameover_surface = font.render("Game Over", True, (255, 0, 0))
    gameover_rect = gameover_surface.get_rect(center=(400, 200))
    screen.blit(gameover_surface, gameover_rect)

    # display the final score
    final_score_surface = font.render(f"Final Score: {score}", True, (0, 0, 0))
    final_score_rect = final_score_surface.get_rect(center=(400, 300))
    screen.blit(final_score_surface, final_score_rect)

    # display the instructions to restart
    restart_surface = font.render("Press SPACE to play again", True, (0, 0, 0))
    restart_rect = restart_surface.get_rect(center=(400, 400))
    screen.blit(restart_surface, restart_rect)

    # update the display
    pygame.display.update()
    clock.tick(60)