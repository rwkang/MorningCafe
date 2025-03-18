import pyautogui
import time

# 잠시 대기하여 사용자가 마우스를 원하는 위치로 이동할 수 있도록 함
time.sleep(5)  # 5초 대기

width, height = pyautogui.size()
center_x, center_y = width//2, height//2

print(f"center_x: {center_x}, center_y: {center_y}")

# 현재 마우스 커서의 좌표 얻기
while True:
    current_x, current_y = pyautogui.position()

    print(f"현재 마우스 좌표: {current_x, current_y}")
    print(f"센터에서는... : {current_x - center_x, current_y - center_y}")

    time.sleep(3)
