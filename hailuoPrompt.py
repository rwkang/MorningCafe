# 2025.02.21 Conslusion. 영상 파일 생성

from util import *
from mysqldbdata import __updateRowData, __updateData

import pyautogui
import pyperclip
import time


def __getVideo(CONNECTEDLOCAL, HAILUO, CENTERX, CENTERY, PATH_YMD, FILE_OPEN, OPEN_PATH,
               SCREEN_TO_FIND_OPEN_PATH,
               SCREEN_TO_FIND_FILE_OPEN, FILE_DOESNT_EXIST, SCREEN_TO_FIND_FILE_DOESNT_EXIST,
               SCREEN_TO_FIND_VIDEO_TWINS, DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_PATH,
               DOWNLOAD_ALREADY_IMAGE,SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE,
               DOWNLOAD_SAVE, SCREEN_TO_FIND_DOWNLOAD_SAVE,
               DOWNLOAD_ALREADY_IMAGE_YES, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES,
               HAILUO_VIDEO_QUEUING, SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING,
               HAILUO_CAMERA_MOVEMENT, HAILUO_CAMERA_DEBUT, HAILUO_CAMERA_FREEDOM,
               HAILUO_CAMERA_RIGHTCIRCLING, HAILUO_CAMERA_UPWARDTILT, HAILUO_CAMERA_SCENICSHOT,
               SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT, SCREEN_TO_FIND_HAILUO_CAMERA_12345,
               HAILUO_VIDEO_GENERATE, SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE,
               HAILUO_VIDEO_REEDIT, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT,
               HAILUO_VIDEO_REEDIT_REPLACE, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE,
               HAILUO_VIDEO_VIOLATED, SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED,
               code_scene, current_video_prompt,
               current_image_file_name, current_music_file_name, current_video_file_name):
    print(get_info(), "동영상 생성을 위한, hailuo 사이트로 바로 넘어 갑니다!!!")
    
    ###############################################################################################################
    ###############################################################################################################
    # 14. hailuo 동영상 생성 : https://hailuoai.video/create
    ###############################################################################################################
    ###############################################################################################################
    # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
    # 0. 크롬 브라우저 아이콘 클릭
    # pyautogui.moveTo(CENTERX - 840, CENTERY + 515, 1)
    # pyautogui.click()
    # time.sleep(9)
    
    if is_chrome_running():
        # 0.1 크롬 브라우저 첫번째 열었던 브라우저 화면 클릭
        pyautogui.moveTo(CENTERX - 840, CENTERY + 515, 1)
        # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
        time.sleep(1)
        pyautogui.moveTo(CENTERX - 840, CENTERY + 470, 1)
        pyautogui.click()
        time.sleep(1)
        # 0.2 첫번째 열었던 브라우저에서, 3번째 태그(ideogram) 클릭
        pyautogui.moveTo(CENTERX - 400, CENTERY - 520, 1)
        pyautogui.click()
        time.sleep(1)
    
    # 1. site address 기존 내용 삭제
    pyautogui.moveTo(CENTERX + 300, CENTERY - 480, 1)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    
    # 1.4 site address : hailuo 열기.
    # pyautogui.typewrite(HAILUO)
    pyperclip.copy(HAILUO)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(20)  # 30초 대기...
    
    print(get_info(), "https://hailuoai.video/create 열었습니다!!!")
    
    # -400 -110 : [Image History] 버튼 클릭
    pyautogui.moveTo(CENTERX - 400, CENTERY - 110, 1)
    pyautogui.click()
    time.sleep(10)
    # -865 -265 : [Upload Image] 버튼 클릭
    pyautogui.moveTo(CENTERX - 865, CENTERY - 265, 1)
    pyautogui.click()
    time.sleep(10)
    
    # todo: [폴더 경로] download_path.png 이미지 찾기 및 클릭
    #  1. [폴더 경로] 이미지 (download_path.png) 파일 존재 확인
    k = 1
    image_file = OPEN_PATH
    screen_to_find_image = SCREEN_TO_FIND_OPEN_PATH
    while True:
        # todo: 윈도우 탐색기 팝업창이 열리면서, 바로 파일 이름 쪽에 커서가 있으므로, 그냥 파일명을 [paste] 하고, [enter] 한다.
        # pyautogui.typewrite(current_image_file_name)
        print(get_info(), "current_image_file_name: ", current_image_file_name)
        pyperclip.copy(current_image_file_name)  # 텍스트를 클립보드에 반드시 복사
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # pyautogui.press('enter') # [열기] 버튼 클릭 ===> [경로] 입력 전이므로 바로 [enter] 하면, 절대 안 됨.
        # time.sleep(60)  # 30초 대기...
        # 2. [폴더 경로] 이미지와 동일한 부분 클릭
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "윈도우 탐색기 팝업 창을 열 수 없습니다. 1분 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)  # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
        else:
            print(get_info(), "윈도우 탐색기 팝업 창을 열고, 이미지 파일을 업로드 합니다.")
            break

    # 2. 이미지와 동일한 부분 클릭
    # todo: 탐색기 팝업창에서 [열기 경로 에디트 박스]를 이미 클릭 했다.
    # download path : ctrl + a => delete
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    # path_ymd 쓰기 : paste
    # pyautogui.typewrite(PATH_YMD)
    print(get_info(), "열기 경로, PATH_YMD: ", PATH_YMD)
    pyperclip.copy(PATH_YMD)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    
    # todo: 여기는 [경로] 입력 후 enter.
    pyautogui.press('enter')  # 여기는 경로 입력 후 엔터.
    time.sleep(3)
    
    # # todo: 여기는 [열기] 버튼 클릭을 위한 enter. ===> 이렇게는 안 되네...
    # pyautogui.press('enter') # [열기] 버튼 클릭.
    # time.sleep(3)

    k = 1
    image_file = FILE_OPEN
    screen_to_find_image = SCREEN_TO_FIND_FILE_OPEN
    while True:
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "윈도우 탐색기 팝업 창에서 [열기] 버튼 이미지를 찾을 수 없습니다!!! 1분간 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)  # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
        else:
            print(get_info(), "탐색기 팝업 창에서 [열기] 버튼을 클릭하였습니다!!! 파일 업로드 중... 1분간 대기...")
            time.sleep(60)  #
            break


    # todo: file_doesnt_exist.png [파일 없음] 팝업 창 확인.
    #  if file_doesnt_exist.png 화면 찾기 성공 : 팝업 창이 떳다는 이야기...

    # 2. 노랑 삼감형 [파일 없음 아이콘] 이미지와 동일한 부분 확인 : 여기서는 우/하 이동, [Yes] 버튼 클릭.
    # while True: # 여기서는 불 필요.
    k = 1
    image_file = FILE_DOESNT_EXIST
    screen_to_find_image = SCREEN_TO_FIND_FILE_DOESNT_EXIST
    # todo: 여기서만 [True] 일 때, 프로그램을 종료하게 한다. ∵) 현재 폴더에 이미지 [파일 없음] 이므로...
    while True:
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "[파일 없음] 팝업 창이 나오지 않고, 정상적으로 진행합니다!!!")
            break
        else:
            print(get_info(), f"동영상을 만들 이미지 파일, {current_image_file_name}이 없습니다. 1분간 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)

    ###############################################################################################################
    # 동영상 프롬프트 쓰기
    ###############################################################################################################
    # -900 +50 : 프롬프트 위치
    # ctrl + a => delete
    pyautogui.moveTo(CENTERX - 850, CENTERY + 50, 1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)

    # current_video_prompt 쓰기 : paste
    # pyautogui.typewrite(current_video_prompt)
    pyperclip.copy(current_video_prompt)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    print(get_info(), "current_video_prompt: ", current_video_prompt)
    print(get_info(), "동영상 프롬프트를 작성하였습니다...")
    time.sleep(1)

    index = int(code_scene[-1])
    print(get_info(), "code_scene: ", code_scene, ", index: ", index)

    # 2025.03.18 Added. 1 and 2 만 카메라 위치를 지정하고, 나머지 3,4,5는 랜덤...
    if index <= 3:
        # +70 +450 : Insert Camera Movements
        image_file = HAILUO_CAMERA_MOVEMENT
        screen_to_find_image = SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT
        k = 1
        while True:
            if find_image(image_file, screen_to_find_image):
                print(get_info(), f"동영상 생성을 위한 카메라 무브먼트 hailuo_camera_movement.png 아이콘을 클릭하였습니다.")
                time.sleep(1)
                break
            else:
                print(get_info(), f"동영상 생성을 위한 카메라 무브먼트 hailuo_camera_movement.png 아이콘을 찾을 수 없습니다. 10초 대기... k: ", k)
                # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                k += 1
                time.sleep(10)

        # 220, 130 : 카메라 무브먼트 화면으로 이동...
        pyautogui.moveTo(CENTERX + 220, CENTERY + 130, 1)
        time.sleep(1)

        if index < 5:
            scroll_up()
        # elif index == 5:
        #     scroll_down()
        else:
            print(get_info(), "index: ", index)

        if index == 1:
            # image_file = HAILUO_CAMERA_DEBUT
            image_file = HAILUO_CAMERA_SCENICSHOT
            pyautogui.moveTo(CENTERX + 270, CENTERY - 80, 1)
            pyautogui.click()
            time.sleep(1)
        elif index == 2:
            image_file = HAILUO_CAMERA_FREEDOM
            pyautogui.moveTo(CENTERX + 450, CENTERY - 80, 1)
            pyautogui.click()
            time.sleep(1)
        elif index == 3:
            image_file = HAILUO_CAMERA_RIGHTCIRCLING
            pyautogui.moveTo(CENTERX + 270, CENTERY + 70, 1)
            pyautogui.click()
            time.sleep(1)
        elif index == 4:
            image_file = HAILUO_CAMERA_UPWARDTILT
            pyautogui.moveTo(CENTERX + 460, CENTERY + 60, 1)
            pyautogui.click()
            time.sleep(1)
        elif index == 5:
            image_file = HAILUO_CAMERA_SCENICSHOT
            # image_file = HAILUO_CAMERA_STAGELEFT
            pyautogui.moveTo(CENTERX + 660, CENTERY + 220, 1) # HAILUO_CAMERA_STAGELEFT
            pyautogui.click()
            time.sleep(1)
        else:
            image_file = HAILUO_CAMERA_DEBUT
            pyautogui.moveTo(CENTERX + 270, CENTERY - 80, 1)
            pyautogui.click()
            time.sleep(1)

        # screen_to_find_image = SCREEN_TO_FIND_HAILUO_CAMERA_12345
        # k = 1
        # while True:
        #     if find_image(image_file, screen_to_find_image):
        #         print(get_info(), f"동영상 생성을 위한 카메라 무브먼트 {index}을(를) 선택하였습니다.")
        #         time.sleep(1)
        #         break
        #     else:
        #         print(get_info(), f"동영상 생성을 위한 카메라 무브먼트 {index}을(를) 선택할 수 없습니다. 10초 대기... k: ", k)
        #         # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
        #         # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
        #         k += 1
        #         time.sleep(10)

    time.sleep(3)

    # +70 +450 : 동영상 생성 버튼 클릭 : 30 크레딧 감소
    # pyautogui.moveTo(CENTERX + 70, CENTERY + 450, 1)
    # time.sleep(10)
    # pyautogui.click() # hailuo_video_generate.png 아이콘 클릭...
    # ===> 아래와 같이 "생성 버튼" 직접 찾아서 클릭...
    k = 1
    kk = 1
    while True:
        image_file = HAILUO_VIDEO_GENERATE
        screen_to_find_image = SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), f"동영상 생성을 위한 [동영상 생성] 버튼 이미지를 찾을 수 없습니다. 1분 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)
        else:
            # 2025.03.18 Added. todo: Text content violated. "Xi, Xu, Xi Jinping, Xu Jinping ..."
            image_file = HAILUO_VIDEO_VIOLATED
            screen_to_find_image = SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED
            if find_image(image_file, screen_to_find_image):
                print(get_info(), f"동영상 생성을 위한 텍스트 프롬프트에 [위반 내용]이 있습니다. 시스템 종료!!!")
                # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                k = -1
                break
            else:
                print(get_info(), "동영상 [생성] 버튼을 클릭하였습니다!!! 5분간 대기합니다...")
                time.sleep(300)  # 5분 대기.

            # todo: 동영상 생성 완료 확인 : [current_video_file_name] 이 파일이 2개 있는지 확인 하면 된다.
            print(get_info(), "current_image_file_name: ", current_image_file_name)
            image_file = HAILUO_VIDEO_QUEUING  # current_image_file_name  # 영상 생성 참조 이미지 원본 파일
            screen_to_find_image = SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING # SCREEN_TO_FIND_VIDEO_TWINS
            while True:
                # 2025.03.04 Conclusion. 아래 find_image_twins()는 안 되네.
                # if not find_image_twins(image_file, screen_to_find_image):
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "동영상 생성이 아직 진행 중 입니다. 3분 대기... kk: ", kk)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    kk += 1
                    time.sleep(180)  # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
                else:
                    # todo: 2025.03.18 Added. 동영상 생성 시 프롬프트 에러: Re-edit 발생 체크
                    image_file = HAILUO_VIDEO_REEDIT
                    screen_to_find_image = SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT
                    if not find_image(image_file, screen_to_find_image):
                        kk = -1
                        print(get_info(), "동영상 생성이 완료 되었습니다. kk: ", kk)
                        break
                    else:
                        # 프롬프트 자동 수정 팝업 창이 나오면, REPLACE 버튼 클릭
                        image_file = HAILUO_VIDEO_REEDIT_REPLACE
                        screen_to_find_image = SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE
                        if find_image(image_file, screen_to_find_image):
                            print(get_info(), "동영상 생성이 아직 진행 중 입니다. 5분 대기...kk: ", kk)
                        else: # 프롬프트 자동 수정 팝업 창이 안 나오면, 바로 "동영상 생성" 버튼 다시 클릭
                            print(get_info(), "프롬프트 에러 수정 후, 동영상을 다시 생성합니다!!! kk: ", kk)
                        time.sleep(1)
                        break # REPLACE 버튼 클릭 후에는 무조건 "break" 후, 다시 "동영상 생성" 버튼 클릭.

        if kk == -1:
            break

    if k <= 0: # Text content violated. ===> 프로그램 종료하고 프롬프트 규칙 수정해야 한다. "Xi, Xu, Xi Jinping ..."
        return False


    # +800 -75 : 동영상 저장 버튼 클릭
    pyautogui.moveTo(CENTERX + 800, CENTERY - 75, 1)
    pyautogui.click()
    time.sleep(10)
    
    # todo: download_path.png 이미지 찾기 및 클릭
    # 1. [경로 아이콘] 이미지 (download_path.png) 파일 존재 확인
    k = 1
    image_file = DOWNLOAD_PATH
    # current_video_file_name = STR_YMD + str(ii) + "0.mp4"
    print(get_info(), "current_video_file_name: ", current_video_file_name)
    # 2. todo: [탐색기] 창이 열릴때가지 기다리게 한다. 이미지와 동일한 부분 클릭
    screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_PATH
    while True:
        # download path : ctrl + v => enter ===> path_ymd : "G:\Youtube\DonGang\MorningCafe\2025\202502\20250203"
        # todo: 파일 저장 팝업 창...
        #       클릭한 상태에서, 팝업 창에 바로 쓰기 : 110.png 파일 명 먼저 쓰기 ===> 팝업 창이 비 고정 이므로...
        # pyautogui.typewrite(current_video_file_name)
        pyperclip.copy(current_video_file_name)  # 텍스트를 클립보드에 반드시 복사
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "윈도우 탐색기 팝업 창을 열 수 없습니다!!! 1분간 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)  # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
        else:
            print(get_info(), "탐색기 팝업 창에서 [경로 아이콘]이 있는 [에디트 박스]를 클릭하였습니다!!!")
            break


    # todo: 탐색기 팝업창에서 [저장 경로 에디트 박스]를 이미 클릭 했다.
    # download path : ctrl + a => delete
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    # path_ymd 쓰기 : paste
    # pyautogui.typewrite(PATH_YMD)
    print(get_info(), "저장 경로, PATH_YMD: ", PATH_YMD)
    pyperclip.copy(PATH_YMD)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    
    # 2. 이미지와 동일한 부분 클릭
    k = 1
    image_file = DOWNLOAD_SAVE
    screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_SAVE
    while True:
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "윈도우 탐색기 창에서 [저장] 버튼 이미지를 찾을 수 없습니다!!!, 1분간 대기... k: ", k)
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            k += 1
            time.sleep(60)  # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
        else:
            print(get_info(), "탐색기 팝업 창에서 [저장] 버튼을 클릭하였습니다!!! 동영상 파일 저장 중... 10초간 대기...")
            time.sleep(10)
            break


    # todo: download_already_image.png 파일 찾기 및 클릭
    #  if download_already_image.png 화면 찾기 성공 : 팝업 창이 떳다는 이야기...
    # 1. 노랑 삼각형 [파일 이미 존재 아이콘] 이미지 (download_already_image.png) 파일 존재 확인
    # 2. 노랑 삼감형 [파일 이미 존재 아이콘] 이미지와 동일한 부분 확인 : 여기서는 클릭 불필요.
    image_file = DOWNLOAD_ALREADY_IMAGE
    screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE
    while True:
        if not find_image(image_file, screen_to_find_image):
            print(get_info(), "[파이 이미 있음] 팝업 창이 나오지 않고, 즉시 저장되었습니다.")
            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            time.sleep(1)
        else:
            print(get_info(), "[파이 이미 있음] 팝업 창이 나오면서, 바로 덮어쓰기 팝업 창이 나왔습니다.")
            time.sleep(1)
            # todo: download_already_image_yes.png 파일 찾기 및 클릭
            # 1. 덮어 쓰기를 위한 [Yes] 버튼 이미지 (download_already_image_yes.png) 파일 존재 확인
            # 2. 덮어 쓰기를 위한 [Yes] 버튼 이미지와 동일한 부분 클릭
            k = 1
            image_file = DOWNLOAD_ALREADY_IMAGE_YES
            screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES
            while True:
                if not find_image(image_file, screen_to_find_image):
                    print(get_info(), "[파일 이미 있음] 팝업 창에서, 파일 덮어쓰기 [Yes] 이미지를 찾을 수 없습니다!!! 1분간 대기... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(60)
                else:
                    print(get_info(), "이미지 저장 팝업 창에, 파일 [덮어 쓰기] [Yes]로 클릭하였습니다!!!")
                    time.sleep(15)
                    break
        # print(get_info(), f"ii: {ii}번째 동영상 파일을 저장했습니다. 저장을 위한 15초 대기...", current_video_file_name)
        break

    ###############################################################################################################
    # MORNING_CAFE_SCENE.VIDEO.NAME 파일명 저장
    ###############################################################################################################
    ###############################################################################################################
    # todo: video_name 저장....
    #  MORNING_CAFE_SCENE.VIDEO_NAME
    ###############################################################################################################
    print(get_info(), "code_scene: ", code_scene)
    print(get_info(), "current_image_file_name: ", current_image_file_name)
    print(get_info(), "비디오 파일, 테이블에 정리, 저장 작업을 진행 합니다...")
    while True:
        sql = """
        UPDATE MORNING_CAFE_SCENE SET VIDEO_NAME = %s WHERE CODE_SCENE = %s
        """
        values = (current_video_file_name, code_scene)
        rsUpdateCommit = __updateData(CONNECTEDLOCAL, sql, values)

        if not rsUpdateCommit:
            print(get_info(), f"{current_video_file_name} 업데이트 실패! 10초 후 다시 진행...")
            time.sleep(5)
        else:
            print(get_info(), f"{current_video_file_name} 업데이트 성공!")
            break

    print(get_info(), f"{code_scene} 비디오 파일명 업데이트 완료... 잠시 쉽니다!!!")
    time.sleep(5)

    # todo: 2025.03.04 Conclusion. 아래 __updateRowData()는 __updateData()로 대체한다. sql 문을 직접 던져 주는 방식으로 변경한다.
    # k = 1
    # while True:
    #     print(get_info(), "code_scene: ", code_scene)
    #     print(get_info(), "current_image_file_name: ", current_image_file_name)
    #     print(get_info(), "current_video_file_name: ", current_video_file_name)
    #     print(get_info(), "current_music_file_name: ", current_music_file_name)
    #     rsUpdateCommit = __updateRowData(CONNECTEDLOCAL, code_scene, current_image_file_name, current_video_file_name,
    #                                      current_music_file_name)
    #
    #     if not rsUpdateCommit:
    #         print(get_info(), f"{current_image_file_name}.png, {current_video_file_name}.mp4 파일 저장 실패! 10초 후 다시 진행... k: ", k)
    #         k += 1
    #         time.sleep(10)
    #     else:
    #         print(get_info(), f"{current_image_file_name}.png, {current_video_file_name}.mp4 파일 저장 성공!")
    #         break
    #
    # # print(get_info(), f"{i}.{ii}번째 완료... 잠시 쉽니다!!!")
    # time.sleep(10)
    
    ###############################################################################################################
    ###############################################################################################################
    
    # print(get_info(), ii, "개 이미지, 동영상 파일을 모두 생성하였습니다.")
    
    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################

