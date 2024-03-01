import pygame

axisX = 0.0
axisY = 0.0
axisT = 0.0
button1 = 0
button2 = 0
button3 = 0
button4 = 0
button5 = 0
button6 = 0

def init_gamepad():
    # pygame 초기화
    pygame.init()

    # 게임 패드 초기화
    pygame.joystick.init()

    # 연결된 게임 패드의 수
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("게임 패드가 연결되어 있지 않습니다.")
        return None

    # 첫 번째 게임 패드 얻기
    joystick = pygame.joystick.Joystick(0)

    # 게임 패드 초기화
    joystick.init()

    print(f"{joystick.get_name()} 게임 패드가 연결되었습니다.")
    return joystick

def get_gamepad_input(joystick):
    # 이벤트 처리
    global axisX, axisY, axisT, button1, button2, button3, button4, button5, button6
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            #print(f"축 {event.axis}: {event.value * 100}")
            if event.axis == 0 :
                #print(f"x: {(int)(event.value * 500)}")
                if event.value * 250 > -5 and event.value * 250 < 5:
                    axisX = 0
                else:
                    axisX = event.value * 500
            if event.axis == 1 :
                #print(f"y: {(int)(event.value * 500)}")
                if event.value * 250 > -5 and event.value * 250 < 5:
                    axisY = 0
                else:
                    axisY = event.value * 500
            if event.axis == 3 :
                #print(f"y: {(int)(event.value * 500)}")
                axisT = event.value * 250
        elif event.type == pygame.JOYBUTTONDOWN:
            #print(f"버튼 {event.button} 눌림")
            if event.button == 0:
                button1 = 1
            if event.button == 1:
                button2 = 1
            if event.button == 2:
                button3 = 1
            if event.button == 3:
                button4 = 1
            if event.button == 4:
                button5 = 1
            if event.button == 5:
                button6 = 1
        elif event.type == pygame.JOYBUTTONUP:
            #print(f"버튼 {event.button} 떼어짐")
            if event.button == 0:
                button1 = 0
            if event.button == 1:
                button2 = 0
            if event.button == 2:
                button3 = 0
            if event.button == 3:
                button4 = 0
            if event.button == 4:
                button5 = 0
            if event.button == 5:
                button6 = 0

if __name__ == "__main__":
    gamepad = init_gamepad()

    if gamepad:
        while True:
            get_gamepad_input(gamepad)
            print(axisX, ',', axisY, ',', axisT, ',', button1, ',', button2, ',', button3, ',', button4, ',', button5, ',', button6)