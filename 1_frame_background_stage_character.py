import os
import pygame

pygame.init()  # 초기화(반드시 필요)

screen_width = 640  # 가로크기
screen_height = 480
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # 튜플의 형태로 가로와 세로의 크기를 삽입

# 화면 타이틀 생성
pygame.display.set_caption("jasper pang")

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화(배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)  # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")  # images 폴더 위치 반환

# 배경만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))


# 이벤트 루프
running = True  # 게임이 진행중인가

while running:
    dt = clock.tick(30)
    for event in pygame.event.get():  # 어떤 이벤트가 발생 하였는가
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가
            running = False

    screen.blit(background, (0, 0))
    pygame.display.update()
pygame.quit()
