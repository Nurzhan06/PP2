import pygame
import os

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("music player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MUSIC_FOLDER = r"C:\Users\Kanat\Desktop\music"
tracks = [os.path.join(MUSIC_FOLDER, file) for file in os.listdir(MUSIC_FOLDER) if file.endswith(".mp3")]

if not tracks:
    print("No music files found!")
    exit()

current_track = 0

def play_music():
    pygame.mixer.music.load(tracks[current_track])
    pygame.mixer.music.play()
    print(f"playing: {os.path.basename(tracks[current_track])}")


def stop_music():
    pygame.mixer.music.stop()
    print("music stopped.")


def next_track():
    global current_track
    current_track = (current_track + 1) % len(tracks)
    play_music()


def prev_track():
    global current_track
    current_track = (current_track - 1) % len(tracks)
    play_music()


play_music()

print("Music Player Controls:")
print("SPACE - Play/Pause")
print("S - Stop")
print("N - Next Track")
print("P - Previous Track")

running = True
paused = False
while running:
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Now Playing: {os.path.basename(tracks[current_track])}", True, BLACK)
    screen.blit(text, (20, 130))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    if paused:
                        pygame.mixer.music.unpause()
                        print("Resumed")
                    else:
                        pygame.mixer.music.pause()
                        print("Paused")
                    paused = not paused
                else:
                    play_music()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_p:
                prev_track()

pygame.quit()