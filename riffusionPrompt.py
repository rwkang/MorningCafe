# 2025.02.19 Added. suno, riffusion AI 추가 : 노래 생성.

from util import __windows_explorer_path, __windows_explorer_save
from wrtnPrompt import *

import pyautogui
import pyperclip
import time

def __getMusic(prompt, music_file_name, PATH_YMD, DOWNLOAD_PATH, DOWNLOAD_SAVE, DOWNLOAD_ALREADY_IMAGE,
               SCREEN_TO_FIND_DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_SAVE,
               SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE,
               CENTERX, CENTERY, RIFFUSION, RIFFUSION_GENERATE, SCREEN_TO_FIND_RIFFUSION_GENERATE,
               RIFFUSION_GHOSTWRITER, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER,
               RIFFUSION_GHOSTWRITER_UPDATE, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE):

    # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
    if is_chrome_running():
        print(get_info(), "크롬 브라우저가 이미 열려 있습니다.")

        # 0.1 크롬 브라우저 첫번째 열었던 브라우저 화면 클릭
        pyautogui.moveTo(CENTERX - 840, CENTERY + 520, 1)
        # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
        time.sleep(1)
        pyautogui.moveTo(CENTERX - 840, CENTERY + 470, 1)
        pyautogui.click()
        time.sleep(1)
        # 0.2 첫번째 열었던 브라우저에서, 4번째 태그(wrtn) 클릭
        pyautogui.moveTo(CENTERX - 260, CENTERY - 520, 1)
        pyautogui.click()
        time.sleep(1)

    # print(get_info(), "CENTERX: ", CENTERX, ", CENTERY: ", CENTERY)

    # 1. site address 기존 내용 삭제
    pyautogui.moveTo(CENTERX + 300, CENTERY - 480, 1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    print(get_info(), "크롬 브라우저 기존 주소를 모두 지웠습니다.")

    print(get_info(), f"RIFFUSION: {RIFFUSION}")
    print(get_info(), "RIFFUSION AI를 엽니다!!!")

    ###############################################################################################################
    # todo: 2025.02.18 Added. [login_riffusion.png] 찾기 ===> wrtn.riffusion 로그인 안 되어 있는지 확인 추가.
    ###############################################################################################################

    ###############################################################################################################

    print(get_info(), "기존 사이트 자료를 지우고, WRTN.PROMPT 전용 사이트를 오픈 합니다!!!")
    # 1.4 site address : wrtn pro모드 열기.
    # pyautogui.typewrite(wrtn)
    pyperclip.copy(RIFFUSION)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(15)

    # todo: 혹 나중에 여기서 시간이 많이 걸리면,
    #  wrtn_input_box.png 또는 icon_copy.png 이미지가 나올 때 까지, while 문 돌리게 한다.

    # Lyrics 넣고 Generate

    # Prompt edit box 클릭
    pyautogui.moveTo(CENTERX - 150, CENTERY - 380, 1)
    pyautogui.click()

    # Lyrics edit box 클릭
    pyautogui.moveTo(CENTERX - 280, CENTERY - 310, 1)
    pyautogui.click()

    # Compose 버튼 클릭
    pyautogui.moveTo(CENTERX - 280, CENTERY - 370, 1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(CENTERX - 280, CENTERY - 310, 1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    pyperclip.copy(prompt)
    pyautogui.hotkey('ctrl', 'v')
    print(get_info(), "Music Prompt: ", prompt)
    print(get_info(), "Music Prompt를 입력하였습니다.")
    time.sleep(1)

    # Ghostwriter 버튼 클릭
    k = 1
    image_file = RIFFUSION_GHOSTWRITER
    screen_to_find_image = SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER
    while True:
        # 8. 이미지와 동일한 부분 클릭
        if find_image(image_file, screen_to_find_image):
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾아 클릭하여 복사했습니다. k: ", k)
            time.sleep(3)
            break
        else:
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾을 수 없습니다! 10초간 대기 계속 루프... k: ", k)
            # return # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.

            k += 1
            time.sleep(10)

    # Ghostwriter Prompt Edit Box 클릭
    print(get_info(), "Riffusion Ghostwriter 에디트 박스를 클릭합니다.")
    # pyautogui.moveTo(CENTERX - 330, CENTERY - 185, 1) # 여기가 유동적이네...
    # pyautogui.click()
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.press('delete')
    # time.sleep(1)

    # 그냥 [Ghostwriter] 버튼 클릭하고, 바로 "comic" 쓴다. [Ghostwriter] 버튼 클릭하면, 바로 [프롬프트 에디트 박스]에 커서가 있네.
    prompt_ghostwriter = RIFFUSION_GHOSTWRITER
    pyperclip.copy(prompt_ghostwriter)
    pyautogui.hotkey('ctrl', 'v')
    print(get_info(), "Ghostwriter Prompt를 기록하고, [Update] 버튼을 클릭합니다!")
    time.sleep(9)

    # Ghostwriter Update 버튼 찾기 및 클릭
    image_file = RIFFUSION_GHOSTWRITER_UPDATE
    screen_to_find_image = SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE
    k = 1
    while True:
        # 8. 이미지와 동일한 부분 클릭
        if find_image(image_file, screen_to_find_image):
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾아 클릭하여 복사했습니다. k: ", k)
            break
        else:
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾을 수 없습니다! 10초간 대기 계속 루프... k: ", k)
            # return # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.

            k += 1
            time.sleep(10)

    # todo: 1분간 대기 보다 더 오래 걸린다면,
    #       여기서, [riffusion_ghostwriter.png] 파일을 찾게 한다. 진행 중일 때는 버튼 앞, 아이콘 부분이 [빙글빙글] 돌아 간다.
    print(get_info(), "Riffusion Ghostwriter 'Update' 버튼을 클릭했습니다. 1분간 대기...")
    time.sleep(60)

    # Sound Prompt Edit Box ===> 아무 것도 입력 하지 않는다.

    # Generate 버튼 찾기 및 클릭.
    image_file = RIFFUSION_GENERATE
    screen_to_find_image = SCREEN_TO_FIND_RIFFUSION_GENERATE
    print(get_info(), "image_file: ", image_file)
    print(get_info(), "screen_to_find_image: ", screen_to_find_image)
    k = 1
    while True:
        # 8. 이미지와 동일한 부분 클릭
        if find_image(image_file, screen_to_find_image):
            print(get_info(), "Generate 버튼을 클릭하였습니다. 2분간 대기... k: ", k)
            break
        else:
            print(get_info(), "Generate 버튼을 찾을 수 없습니다! 10초간 대기 후 계속 루프... k: ", k)
            # return # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            time.sleep(10)
            k += 1

    time.sleep(60)

    # todo: 노래 생성 후 저장
    #  첫번째 노래 저장
    #  [...] 여기 클릭
    pyautogui.moveTo(CENTERX + 280, CENTERY - 230, 1)
    pyautogui.click()
    # 핫키 창에서, 바로 왼쪽으로 이동하고, 그 다음 아래로 이동해야 한다.
    pyautogui.moveTo(CENTERX + 160, CENTERY - 230, 1)
    time.sleep(1)
    # 핫키 창에서, Download m4a 버튼 클릭
    # pyautogui.moveTo(CENTERX + 160, CENTERY - 30, 1)
    pyautogui.moveTo(CENTERX + 160, CENTERY - 0, 1)
    time.sleep(1)
    # pyautogui.moveTo(CENTERX + 290, CENTERY - 30, 1)
    pyautogui.moveTo(CENTERX + 290, CENTERY - 0, 1)
    # pyautogui.moveTo(CENTERX + 290, CENTERY - 5, 1)
    pyautogui.moveTo(CENTERX + 290, CENTERY + 30, 1)
    pyautogui.click()
    time.sleep(9)

    # todo: 윈도우 탐색기 팝업창이 열리면서, 바로 파일 이름 쪽에 커서가 있으므로, 그냥 파일명을 [paste] 하고, [enter] 한다.
    #       [노래 제목]을 그대로 둔다??? ===? 아니다.
    #       ===> 아니다. 2개 노래 파일 생성 : 첫번째 파일명 : current_music_file_name, 두번째 파일명: current_music_file_name2.m4a
    # pyautogui.typewrite(music_file_name)
    print(get_info(), "music_file_name: ", music_file_name)
    pyperclip.copy(music_file_name)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    # pyautogui.press('enter') # [열기] 버튼 클릭 ===> [경로] 입력 전 이므로 바로 [enter] 하면, 절대 안 됨.
    # time.sleep(DELAY60)  # 30초 대기...

    # 윈도우 탐색기 창에서 경로 에디트 박스
    rs_path = __windows_explorer_path(DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_PATH)
    print(get_info(), "rs_path: ", rs_path)

    # todo: 탐색기 팝업창에서 [저장 경로 에디트 박스]를 이미 클릭 했다.
    # download path : ctrl + a => delete
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    # path_ymd 쓰기 : paste
    # pyautogui.typewrite(path_ymd)
    print(get_info(), "저장 경로, PATH_YMD: ", PATH_YMD)
    pyperclip.copy(PATH_YMD)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    rs_save = __windows_explorer_save(DOWNLOAD_SAVE, SCREEN_TO_FIND_DOWNLOAD_SAVE,
                                      DOWNLOAD_ALREADY_IMAGE, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE)

    print(get_info(), "첫번째 노래 파일을 저장하였습니다. 10초간 대기...")
    time.sleep(10)

    print(get_info(), "두번째 노래 파일 저장을 진행합니다...")

    # 두번째 노래 저장.
    #  [...] 여기 클릭
    pyautogui.moveTo(CENTERX + 280, CENTERY - 150, 1)
    pyautogui.click()
    # 핫키 창에서, 바로 왼쪽으로 이동하고, 그 다음 아래로 이동해야 한다.
    pyautogui.moveTo(CENTERX + 160, CENTERY - 150, 1)
    # 핫키 창에서, Download m4a 버튼 클릭
    # pyautogui.moveTo(CENTERX + 160, CENTERY + 50, 1)
    pyautogui.moveTo(CENTERX + 160, CENTERY + 80, 1)
    time.sleep(1)
    # pyautogui.moveTo(CENTERX + 290, CENTERY + 50, 1)
    pyautogui.moveTo(CENTERX + 290, CENTERY + 80, 1)
    # pyautogui.moveTo(CENTERX + 290, CENTERY + 80, 1)
    pyautogui.moveTo(CENTERX + 290, CENTERY + 110, 1) # m4a
    pyautogui.click()
    time.sleep(9)
    pyautogui.click()

    # todo: 윈도우 탐색기 팝업창이 열리면서, 바로 파일 이름 쪽에 커서가 있으므로, 그냥 파일명을 [paste] 하고, [enter] 한다.
    #       [노래 제목]을 그대로 둔다??? ===? 아니다.
    #       ===> 아니다. 두번째 파일명: current_music_file_name2.m4a
    music_title = os.path.splitext(music_file_name)[0]
    music_ext = os.path.splitext(music_file_name)[1]
    music_title2 = music_title + "2" + music_ext
    # pyautogui.typewrite(music_title2)
    print(get_info(), "music_title2: ", music_title2)
    pyperclip.copy(music_title2)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    # pyautogui.press('enter') # [열기] 버튼 클릭 ===> [경로] 입력 전이므로 바로 [enter] 하면, 절대 안 됨.
    # time.sleep(DELAY60)  # 30초 대기...

    # 윈도우 탐색기 창에서 경로 에디트 박스

    print(get_info(), "music_title2: ", music_title2)

    # 윈도우 탐색기 창에서 경로 에디트 박스
    rs_path = __windows_explorer_path(DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_PATH)
    print(get_info(), "rs_path: ", rs_path)

    # todo: 탐색기 팝업창에서 [저장 경로 에디트 박스]를 이미 클릭 했다.
    # download path : ctrl + a => delete
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    # path_ymd 쓰기 : paste
    # pyautogui.typewrite(path_ymd)
    print(get_info(), "저장 경로, PATH_YMD: ", PATH_YMD)
    pyperclip.copy(PATH_YMD)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    rs_save = __windows_explorer_save(DOWNLOAD_SAVE, SCREEN_TO_FIND_DOWNLOAD_SAVE,
                                      DOWNLOAD_ALREADY_IMAGE, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE)

    print(get_info(), "두번째 노래 파일을 저장하였습니다. 10초간 대기...")
    time.sleep(10)

    return rs_save
