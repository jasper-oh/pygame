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
background = pygame.image.load(os.path.join(image_path, "background_1.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character2.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0
# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러번 사용가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 [ 4개의 공에 대해 따로 처리]
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공에 따라서 속도가 다른것을 설정 - 공에 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -0]  # index 0 1 2 3 에 해당 하는 속도

# 공들
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,
    "to_x": 3,
    "to_y": -6,
    "init_spd_y": ball_speed_y[0]
})

# 이벤트 루프
running = True  # 게임이 진행중인가

while running:
    dt = clock.tick(30)
    for event in pygame.event.get():  # 어떤 이벤트가 발생 하였는가
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + \
                    (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_index = ball_val["img_idx"]
        ball_size = ball_images[ball_img_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 가로 벽에 닿았을떄 공의 이동방향 변경 (튕겨 내려오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height-stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:  # 그 외의 모든 경우에는 속도를 줄여나간다.
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_index = val["img_idx"]
        screen.blit(ball_images[ball_img_index], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()
pygame.quit()
