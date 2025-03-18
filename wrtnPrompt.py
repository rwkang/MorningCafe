
from util import *

import pyautogui
import pyperclip


def __openWrtnSite(browser, WRTN, CENTERX, CENTERY, ICON_EDIT, SCREEN_TO_FIND_EDIT_ICON):
    print(get_info(), "CENTERX: ", CENTERX, ", CENTERY: ", CENTERY)

    rsWrtnOpen = False

    # todo: 2025.02.12 Conclusion. 크롬 브라우저는 3개(wrtn,ideogram,hailuo)를 순서대로 열어 놓고, 프로그램을 실행 해야 한다.
    # # 0. 크롬 브라우저 아이콘 클릭
    # print(get_info(), "크롬 브라우저를 엽니다!!!")
    # pyautogui.moveTo(CENTERX - 840, CENTERY + 520, 1)
    # pyautogui.click()
    # time.sleep(DELAY9)
    #
    # # 9초 후 화면 체크 : [사용자 선택 화면]이 나오면...
    # # 아이콘 이미지 (icon_edit.png) 파일 존재 확인
    # image_file = chrome_select_user
    # screen_to_find_image = screen_to_find_chrome_user
    #
    # if not check_file_exists(icon_edit):
    #     print(get_info(), "크롬 사용자 이미지 파일, chrome_select_user.png 파일이 없습니다. 다시 확인 하시오!!!")
    #     return
    #
    # if not find_image(image_file, screen_to_find_image):
    #     print(get_info(), "center_img_x: -1, center_img_y: -1, 이미지를 찾을 수 없습니다!!!")
    #     # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
    #     # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.

    # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
    if is_chrome_running():
        print(get_info(), "크롬 브라우저가 이미 열려 있습니다.")

        # 0.1 크롬 브라우저 첫번째 열었던 브라우저 화면 클릭
        if browser == "WRTN":
            pyautogui.moveTo(CENTERX - 840, CENTERY + 520, 1) # 작업 표시줄 1번 위치
            # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
            time.sleep(1)
            pyautogui.moveTo(CENTERX - 840, CENTERY + 470, 1) # 작업 표시줄 1번 위치
        # elif browser == "RIFFUSION":
        #     pyautogui.moveTo(CENTERX + 465, CENTERY + 520, 1) # 작업 표시줄 29번 위치
        #     # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
        #     time.sleep(1)
        #     pyautogui.moveTo(CENTERX + 465, CENTERY + 470, 1)  # 작업 표시줄 29번 위치
        else:
            pyautogui.moveTo(CENTERX - 840, CENTERY + 520, 1)  # 작업 표시줄 1번 위치
            # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
            time.sleep(1)
            pyautogui.moveTo(CENTERX - 840, CENTERY + 470, 1)  # 작업 표시줄 1번 위치
        pyautogui.click()
        time.sleep(1)
        # 0.2 첫번째 열었던 브라우저에서, 첫번째 태그(wrtn) 클릭
        pyautogui.moveTo(CENTERX - 880, CENTERY - 520, 1)
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
    
    # 0. 한/영 키보드를 영문으로 전환.
    # if is_hangul(): # 이 함수로는 작동이 안 되네...
    #     print("현재 한글 키보드 입니다. 영문 키보드로 전환합니다!!!")
    #     switch_to_english()
    
    """
    # x, y = 770, 500
    x, y = 1730, 1040
    # icon_hangul = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_hangul.png" # G:\Youtube\DonGang\MorningCafe\2025
    # icon_hangul_pos = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_hangul_pos.png"
    
    icon_file = ICON_HANGUL
    icon_pos_file = ICON_HANGUL_POS
    tolerance = 30
    
    2025.02.11 Conclusion. pyautogui.typewrite(IDEA_ENG) ===> pyautogui.pyperclip(IDEA_ENG)
    
    # 1.1 이미지 파일 존재 확인
    if not check_file_exists(icon_file):
        print(get_info(), "한글 [가] 모양의 icon_hangul.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    
    # 1.3 화면 우측 하단 한/영 아이콘 체크 : 한글 [가] 아이콘 이면, 클릭하여, 영문 [A] 아이콘으로 만든다.
    if check_icon_at_position(x, y, icon_file, icon_pos_file, tolerance):
        print(get_info(), "한글 키보드 상태 입니다. [가] 아이콘을 클릭하여 영문 키보드 상태로 변경합니다.")
        pyautogui.moveTo(x + 10, y + 10, 1)
        pyautogui.click()
        time.sleep(delay1)
    else:
        print(get_info(), "영문 [A] 아이콘 상태입니다. 그대로 진행합니다!!!")
    """
    
    print(get_info(), f"wrtn: {WRTN}")
    print(get_info(), "뤼튼(wrtn) AI를 엽니다!!!")
    
    ###############################################################################################################
    # todo: 2025.02.18 Added. [login_wrtn.png] 찾기 ===> wrtn.뤼튼 로그인 안 되어 있는지 확인 추가.
    ###############################################################################################################
    # todo: login_wrtn.png 파일은 이미 있음. [로그인] 아이콘 확인만 하고, 로그인은 수동으로 시킬 것.
    
    
    ###############################################################################################################
    
    print(get_info(), "기존 사이트 자료를 지우고, WRTN.PROMPT 전용 사이트를 오픈 합니다!!!")
    # 1.4 site address : wrtn pro모드 열기.
    # pyautogui.typewrite(wrtn)
    pyperclip.copy(WRTN)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(15)
    
    # todo: 혹 나중에 여기서 시간이 많이 걸리면,
    #  wrtn_input_box.png 또는 icon_copy.png 이미지가 나올 때 까지, while 문 돌리게 한다.
    
    
    # 2. 뤼튼, wrtn 좌측 [편집] 화면 숨기기.
    
    # 2025.02.11 Conclusion. ***** 중요 *****
    # 아래 방법과 같이, 편집 아이콘인 "|<-" 요 이미지를, icon_edit.png 파일을 저장해 두고,
    # Ⅰ. 이것이 항상 고정적으로 위치하는 곳을, icon_edit.png 이미지의 width, height 만큼 그대로 가져가서,
    #    서로 비교하여, 이 이미지가 현재 있는지, 아니면 감춰져 있는지 확인하여,
    #    현재 화면에 있으면, 그 이미지 아이콘을 클릭하여, [해당 편집 화면 부분]을 닫게 하는 것이다.
    #    그런데, 이것은 비교할 때, [tolerance] 값도 필요한 것 처럼, 정확성이 담보되지 않네.
    # Ⅱ. 다른 방법으로, icon_edit.png 이미지 파일을 그대로 두고,
    #    현재 웹 브라우져 화면을 캡쳐하여 저장하고, 거기서 이 icon_edit.png 이미지를 찾아서,
    #    있으면, 클릭하여, [해당 편집 화면 부분]을 닫게 하는 것이다.
    #    이것이 더 좋을 듯 하여, 이 방법을 사용하기로 최종 결정 한다.
    
    # Ⅱ. 방법
    # 아이콘 이미지 (icon_edit.png) 위치 정보 가져오기.
    image_file = ICON_EDIT
    screen_to_find_image = SCREEN_TO_FIND_EDIT_ICON
    
    if not find_image(image_file, screen_to_find_image):
        print(get_info(), "center_img_x: -1, center_img_y: -1, [wrtn 에디트 아이콘] 이미지를 찾을 수 없습니다. 편집 화면이 숨겨져 있다는 뜻입니다.")
        # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
        # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
        rsWrtnOpen = True


    """
    # Ⅰ. 방법
    x, y = 105, 133
    # icon_edit = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_edit.png"
    # icon_edit_pos = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_edit_pos.png"
    icon_file = icon_edit
    icon_pos_file = icon_edit_pos
    tolerance = 30
    
    # 2.1 이미지 파일 존재 확인
    if not check_file_exists(icon_file):
        print(get_info(), "|<- 이런 모양의 icon_edit.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    
    # 2.2 화면 좌측 상단 체크 : [wrtn.] / [|<- 편집] / [+ 새 대화] : 여기서, 가운데 [|<- 편집] 화면 숨기기
    if check_icon_at_position(x, y, icon_file, icon_pos_file, tolerance):
        print(get_info(), "편집 화면이 떠 있어, 숨기기 아이콘(|<-)을 클릭합니다.")
        pyautogui.moveTo(x + 10, y + 10, 1)
        pyautogui.click()
        time.sleep(delay1)
    else:
        print(get_info(), "편집 화면이 숨겨져 있어, 그대로 진행합니다!!!")
    """

    print(get_info(), f"rsWrtnOpen: {rsWrtnOpen}")
    return rsWrtnOpen

    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################

def __getWrtnAnswer(prompt, CENTERX, CENTERY, ICON_COPY, ICON_COPY_RED, SCREEN_TO_FIND_COPY_ICON):

    # 3. idea prompt 쓰기. 한글/영어
    pyautogui.moveTo(CENTERX - 400, CENTERY + 395, 1)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    
    """
    2025.02.11 Conclusion. 한글 prompt 인쇄 불가 : 글짜가 깨져서 써지네...
    
    # 3.A.1 한글로 idea 쓰기
    x, y = 1730, 1040
    # icon_hangul = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_hangul.png"
    # icon_hangul_pos = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_hangul_pos.png"
    icon_file = icon_hangul
    icon_pos_file = icon_hangul_pos
    tolerance = 30
    tolerance = 255
    
    # 3.A.2 한글 이미지 파일 존재 확인
    if not check_file_exists(icon_file):
        print(get_info(), "한글 [가] 모양의 icon_hangul.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    
    # 3.A.3 화면 우측 하단 한/영 아이콘 체크 : 한글 [가] 아이콘 이면, 클릭하여, 영문 [A] 아이콘으로 만든다.
    if check_icon_at_position(x, y, icon_file, icon_pos_file, tolerance):
        print(get_info(), "영문 키보드 상태 입니다. [A] 아이콘을 클릭하여 한글 키보드 상태로 변경합니다.")
        pyautogui.moveTo(x + 10, y + 10, 1)
        pyautogui.click()
        time.sleep(delay1)
    else:
        print(get_info(), "한글 [가] 아이콘 상태입니다. 그대로 진행합니다!!!")
    
    pyautogui.moveTo(center_x - 400, center_y + 395, 1)
    pyautogui.click()
    print(get_info(), "idea_kor: ", idea_kor)
    # pyautogui.typewrite(idea_kor)
    pyperclip.copy(IDEA_ENG) # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(delay1)
    
    # 4. idea prompt 쓰고, 우측 엔터 아이콘 클릭하기.
    pyautogui.moveTo(center_x + 270, center_y + 390, 1)
    pyautogui.click()
    time.sleep(delay15)
    
    # 6. 마우스 스크롤 다운 20번 강제로 진행...
    print(get_info(), "페이지 맨 아래로 스크롤 다운 합니다!!!")
    # scroll_down()
    for _ in range(20):
        pyautogui.scroll(-100)
        time.sleep(0.1)
    time.sleep(delay9)
    
    # 3.B.1 영어로 idea 쓰기
    x, y = 1730, 1040
    # icon_english = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_english.png"
    # icon_english_pos = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_english_pos.png"
    icon_file = ICON_ENGLISH
    icon_pos_file = ICON_ENGLISH_POS
    tolerance = 30
    tolerance = 255
    
    """
    ###############################################################################################################
    # 프롬프트 에디트 박스
    pyautogui.moveTo(CENTERX - 400, CENTERY + 395, 1)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    
    """
    2025.02.11 Conclusion. pyautogui.typewrite(IDEA_ENG) ===> pyautogui.pyperclip(IDEA_ENG)
    
    # 3.B.2 이미지 파일 존재 확인
    if not check_file_exists(icon_file):
        print(get_info(), "영어 [A] 모양의 icon_english.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    
    # 3.B.3 화면 우측 하단 한/영 아이콘 체크 : 한글 [가] 아이콘 이면, 클릭하여, 영문 [A] 아이콘으로 만든다.
    if check_icon_at_position(x, y, icon_file, icon_pos_file, tolerance):
        print(get_info(), "한글 키보드 상태 입니다. [가] 아이콘을 클릭하여 영문 키보드 상태로 변경합니다.")
        pyautogui.moveTo(x + 10, y + 10, 1)
        pyautogui.click()
        time.sleep(delay1)
    else:
        print(get_info(), "영문 [A] 아이콘 상태입니다. 그대로 진행합니다!!!")
    """
    
    # idea 프롬프트 paste.
    pyautogui.moveTo(CENTERX - 400, CENTERY + 395, 1)
    pyautogui.click()
    print(get_info(), "prompt: ", prompt)
    # pyautogui.typewrite(IDEA_ENG)
    pyperclip.copy(prompt)  # 텍스트를 클립보드에 반드시 복사
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    
    # 4. idea prompt 쓰고, 우측 엔터 아이콘 클릭하기.
    pyautogui.moveTo(CENTERX + 270, CENTERY + 390, 1)
    pyautogui.click()
    time.sleep(15)
    
    # 6. 마우스 스크롤 다운 20번 강제로 진행...
    print(get_info(), "페이지 맨 아래로 스크롤 다운 합니다!!!")
    scroll_down()
    # for _ in range(20):
    #     pyautogui.scroll(-100)
    #     time.sleep(0.1)
    
    time.sleep(9)
    
    ###############################################################################################################
    ###############################################################################################################
    
    # return
    
    """
    2025.02.11 Conclusion. 아래 복사 아이콘 이미지 저장 루틴은 인제 필요 없다. ∵) 이미 icon_copy.png 파일이 아래 루틴으로 생성.
    
    # 5. 뤼튼, 복사 아이콘 이미지로 저장 : icon_copy_pos.png
    x, y = 535, 675
    # icon_copy = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_copy.png"
    # icon_copy_pos = "G:\\Youtube\\DonGang\\MorningCafe\\2025\\icon_copy_pos.png"
    icon_file = icon_copy
    icon_pos_file = icon_copy_pos
    tolerance = 30
    
    # 2.1 이미지 파일 존재 확인
    if not check_file_exists(icon_file):
        print(get_info(), "복사 아이콘 icon_copy.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    
    # 2.2 화면 좌측 하중단, 복사 아이콘 클릭
    if check_icon_at_position(x, y, icon_file, icon_pos_file, tolerance):
        print(get_info(), "복사 아이콘을 클릭합니다.")
        pyautogui.moveTo(x + 10, y + 10, 1)
        pyautogui.click()
        time.sleep(delay1)
    else:
        print(get_info(), "복사 아이콘을 클릭합니다. 그대로 진행합니다!!!")
    """
    
    # 7. 복사 아이콘 이미지 (icon_copy.png) 파일 존재 확인
    k = 1
    while True:
        if k % 2 == 0:  # 짝수
            image_file = ICON_COPY_RED
        else:
            image_file = ICON_COPY

        # 8. 이미지와 동일한 부분 클릭
        screen_to_find_image = SCREEN_TO_FIND_COPY_ICON
    
        if find_image(image_file, screen_to_find_image):
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾아 클릭하여 복사했습니다. k: ", k)
            break
        else:
            print(get_info(), "[wrtn copy icon]: ", image_file, ", 이미지를 찾을 수 없습니다! 계속 루프... k: ", k)
            # return # 프로그램 종료하고, [에러 카톡 발송] 한다.
            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
    
            k += 1
            time.sleep(10)
            print(get_info(), "페이지 맨 아래로 스크롤 다운 합니다!!!")
            scroll_down()

    # 9. copy 값 변수 저장
    answer = pyperclip.paste()
    print(get_info(), "ideas: ", answer)

    return answer