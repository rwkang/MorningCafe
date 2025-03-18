# -*- coding: utf-8 -*-

# 2025.01.15 Created by rwkang, 유튜브 영상 자동 제작 : DonGang 채널 참조: https://www.youtube.com/watch?v=gyzh5mTdcFA
# Youtube Morning Cafe 영상 자동 제작을 위한, PyAutoGui 이용, 매크로 프로그램.


# 1. G:\Youtube\DonGang\MorningCafe.xlsx 파일을, G:\Youtube\DonGang\MorningCafe\2025\202502\20250211(today) 폴더에 복사.
# 2.

# todo: main.py 파일을 제외한 나머지 파일에서는, 가능하면, 글로벌(대문자) 변수를, [파라미터]로 전달하여 사용하도록 한다. 메모리 문제 등.

import math
import sys
import re
import time

import pyautogui
import openpyxl
import pyperclip
import pandas as pd
import threading
import pyperclip

from mysqldb import __alterTable
from mysqldbdata import __getTodayData, __insertCurrentRow1, __delTodayData, __updateRowData, __updateData
from wrtnPrompt import __openWrtnSite, __getWrtnAnswer
from riffusionPrompt import __getMusic
from hailuoPrompt import __getVideo

from util import *

from openpyxl import load_workbook
from openpyxl.styles import Font
from itertools import islice
from pandas import DataFrame
# from datetime import datetime, timedelta
# from threading import Thread

from mysqldb import *

# 2025.02.12 Conclusion. ***** 글로벌 변수와 펑션 *****
# todo: 1. py 파일에서, set_globals() 펑션 내부에서, gloval 로 선언한 변수는,
#          반드시 [import gv]로 선언하고, 해당 변수 사용시에 반드시 [xxx] 형식으로 사용해야 한다.
# 2. py 파일에서, 변수 선언부에, 선언과 동시에 할당한 변수한 변수는 아래 [from gv import *]로 선언하고,
#    todo: [] 없이, 그냥 변수명 만으로 사용 해야 한다.
# todo: py 선언만 한 변수 사용 가능 : 즉, set_glovals() 내부에서 세팅한 변수만 사용을 위해서는, 아래 [from gv import *] : 여기가 없어야 한다.
from gv import *

'''
import gv
# todo: 여기서 글로벌 변수를 초기화 한다. 호출할 때 초기화 된다. 반드시 []을 사용해야 한다.
set_globals() # 글로벌 변수 초기화 : 필수.
'''

from mysqldbdata import *

# connectRemoteDB()

#   사용 불가: print(get_info(), "path_bs: ", path_bs) : 사용을 위해서는, [from gv import *]
# todo: 가능: print(get_info(), "path_bs: ", path_bs)

# # Esc key and Psuse Key 위한 이벤트 객체
# def exit_program():
#     def on_press(key):
#         if str(key) == 'Key.esc':
#             __production_actual.status = 'pause'
#             user_input = input('Program paused, would you like to continue? (y/n) ')
#
#             while user_input != 'y' and user_input != 'n':
#                 user_input = input('Incorrect input, try either "y" or "n" ')
#
#             if user_input == 'y':
#                 __production_actual.status = 'run'
#             elif user_input == 'n':
#                 __production_actual.status = 'exit'
#                 exit()
#
#     with keyboard.Listener(on_press=on_press) as listener:
#         listener.join()

# 일시 정지 및 재개를 위한 이벤트 객체
pause_event = threading.Event()
pause_event.set()  # 초기 상태는 실행 중

###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################

# class MorningCafe():
#     def __init__(self):
#         super(self.__class__, self).__init__()


# ESC 키 입력을 감지하는 함수
def listen_for_escape(stop_event):
    while not stop_event.is_set():
        if keyboard.is_pressed('esc'):
            print(get_info(), "ESC 키가 눌렸습니다. 루프를 종료합니다. 잠시 기다려 주세요...")
            stop_event.set()  # 이벤트 설정하여 루프 종료
        if keyboard.is_pressed('pause'):
            if pause_event.is_set():
                print(get_info(), "10초 일시 정지합니다.  잠시 기다려 주세요...")
                # print("다시 시작을 위해서는 한번 더 [PAUSE] 키를 누르고, 잠시 기다려 주세요...")
                pause_event.clear()  # 일시 정지
                time.sleep(10)
                print(get_info(), "재개합니다.")
            else:
                # print("재개합니다.")
                pause_event.set()  # 재개
                # pause_event가 설정될 때까지 대기
                print(get_info(), "다시 시작을 위해서는 한번 더 [PAUSE] 키를 누르고, 잠시 기다려 주세요...")
                keyboard.wait('pause')  # pause 키가 눌릴 때까지 대기

# class MyMain():
    # def __init__(self, parent=None):
    #     super(self.__class__, self).__init__(parent)

def __gettingRawData(PATH, stop_event):
    date_format = "%Y.%m.%d"  # 날짜 형식 지정
    return 1


def __makingImages(PATH, stop_event):
    return 2

def __makingVideos(PATH, stop_event):
    return 3

def __makingPrompts(PATH, stop_event):
    print(get_info(), "PATH: ", PATH)
    # print(get_info(), "path_bs: ", path_bs)
    # print(get_info(), "path_current: ", path_current)
    print(get_info(), "PATH_CURRENT: ", PATH_CURRENT)
    # print(get_info(), "path_bs: ", path_bs, ", path_current: ", path_current, ", path_year: ", path_year)
    # print(get_info(), "date_current: ", date_current, ", date_current: ", date_current)
    # print(get_info(), "delay1: ", delay1)

    # return

    # 디렉토리 생성 : "G:\Youtube\DonGang\MorningCafe\2025\202502\today() : 20250203" 맨 끝에는 "\" 없음에 유의
    k = 1
    while True:
        print(get_info(), "PATH_BS: ", PATH_BS, ", PATH_BASE: ", PATH_BASE, ", PATH_YEAR: ", PATH_YEAR)
        print(get_info(), "PATH_YEAR: ", PATH_YEAR, ", PATH_YM: ", PATH_YM, ", PATH_YMD: ", PATH_YMD)
        if not check_directory(PATH_YM, STR_YMD):  # [PATH_YMD]가 아님에 주의.
            print(get_info(), f"폴더가 이미 존재합니다. 기존 폴더 [{STR_YMD}]로 작업을 계속 진행합니다.")
            break
            # return
            # time.sleep(DELAY10)
        else:
            print(get_info(), "작업 폴더를 성공적으로 만들었습니다.")
            break

    # return

    # MYSQLWEBDB, CURSARRAYWEB, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
    #         BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()

    MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
    BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()

    print(get_info(), "HOST1: ", HOST1)
    print(get_info(), "USER1: ", USER1)
    print(get_info(), "PASS1: ", PASS1)
    print(get_info(), "DBNAME1: ", DBNAME1)
    print(get_info(), "NIGHT_CLOSING_HHMMSS: ", NIGHT_CLOSING_HHMMSS)
    print(get_info(), "DAY_CLOSING_HHMMSS: ", DAY_CLOSING_HHMMSS)

    print(get_info(), "MYSQLLOCALDB: ", MYSQLLOCALDB)
    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    # todo: 아래 [테이블 생성] 루틴은, 이제 절대 실행해서는 안 된다.
    # sql, tf = creating_morning_cafe_idea(MYSQLLOCALDB, CURSARRAYLOCAL)
    # print(get_info(), "sql: ", sql)
    # sql, tf = creating_morning_cafe_scene(MYSQLLOCALDB, CURSARRAYLOCAL)
    # print(get_info(), "sql: ", sql)
    # return

    # todo: 아래 [테이블 수정] 루틴은, 이제 절대 실행해서는 안 된다.
    table_name = "MORNING_CAFE_SCENE"
    # sql = f"""
    #     ALTER TABLE {table_name} DROP PRIMARY KEY,
    #     ADD COLUMN LYRICS_PROMPT text,
    #     ADD COLUMN LYRICS text,
    #     MODIFY COLUMN ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    #     MODIFY COLUMN CODE_SCENE varchar(20) NOT NULL,
    #     ADD PRIMARY KEY (CODE_SCENE);
    # """
    # # todo: 위 구분 처럼, "AUTO_INCREMENT"를 "PRIMARY KEY"로 사용해야 되네.
    # sql = f"""
    #         ALTER TABLE {table_name} ADD COLUMN LYRICS_PROMPT text, ADD COLUMN LYRICS text,
    #         MODIFY COLUMN ID bigint(20) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #         MODIFY COLUMN CODE_SCENE varchar(20) NOT NULL,
    #         ADD UNIQUE (CODE_SCENE);
    #     """
    # todo: 위 구분 처럼, "VIDEO_PROMPT" 추가: 영상 프롬프트는 "아주 간결하고, 천천히 움직이게 하는 것으로" ∵)빠르면 영상이 깨짐.
    sql = f"""
                ALTER TABLE {table_name} ADD COLUMN VIDEO_PROMPT text;
            """
    # print(get_info(), "sql: ", sql)
    # rs_alter_table = __alterTable(CONNECTEDLOCAL, MYSQLLOCALDB, CURSARRAYLOCAL, sql)
    # if not rs_alter_table:
    #     print(get_info(), "명령문: ", sql, "실행에 실패! 관리자에게 문의!")
    #     # 스레드 종료 신호 보내기
    #     stop_event.set()
    #     listener_thread.join()  # 스레드가 종료될 때까지 대기
    #     print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
    #     sys.exit()  # 프로그램 종료
    #     return
    # return

    ###############################################################################################################
    # todo: 2025.02.18 Added. Base Image 체크
    ###############################################################################################################
    isExist = False

    # EDIT 아이콘 이미지 (icon_edit.png) 파일 존재 확인
    image_file = ICON_EDIT
    if not check_file_exists(image_file):
        print(get_info(), "편집 아이콘 이미지 파일, icon_edit.png 파일이 없습니다. 다시 확인하시오!!!")
        # return
        isExist = True
    # 복사 아이콘 이미지 (icon_copy.png) 파일 존재 확인
    image_file = ICON_COPY
    if not check_file_exists(image_file):
        print(get_info(), "복사 아이콘 이미지 파일, icon_copy.png 파일이 없습니다. 다시 확인하시오!!!")
        # return
        isExist = True
    # 복사 아이콘 2 이미지 (icon_copy_red.png) 파일 존재 확인
    image_file = ICON_COPY_RED
    if not check_file_exists(image_file):
        print(get_info(), "복사 아이콘 이미지 파일, icon_copy.png 파일이 없습니다. 다시 확인하시오!!!")
        # return
        isExist = True

    # todo: download_path.png 이미지 찾기 및 클릭
    # 윈도우 탐색기 팝업 창에서, [경로 아이콘] 이미지 (download_path.png) 파일 존재 확인
    image_file = DOWNLOAD_PATH
    if not check_file_exists(image_file):
        print(get_info(), "윈도우 탐색기 팝업 창 경로 이미지를 찾을 수 없습니다!!!")
        isExist = True

    # todo: download_save.png 파일 찾기 및 클릭
    if not check_file_exists(image_file):
        print(get_info(), "탐색기 팝업 창에 [저장 버튼] 이미지 파일, [download_save.png]가 없습니다. 다시 확인하시오!!!")
        isExist = True

    # todo: download_already_image.png 파일 찾기 및 클릭
    #  if download_already_image.png 화면 찾기 성공 : 팝업 창이 떳다는 이야기...
    # download_already_image.png 이미지 찾기 및 클릭
    # 1. 노랑 삼각형 [파일 이미 존재 아이콘] 이미지 (download_already_image.png) 파일 존재 확인
    image_file = DOWNLOAD_ALREADY_IMAGE
    if not check_file_exists(image_file):
        print(get_info(), "[파일 이미 존재] 팝업 창에서, 노랑 삼각형 [파일 이미 존재 아이콘] 파일, [download_already_image.png]가 없습니다. 다시 확인하시오!!!")
        isExist = True

    image_file = IDEOGRAM_COVER
    if not check_file_exists(image_file):
        print(get_info(), "복사 아이콘 이미지 파일, icon_copy.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. [열기 버튼] 이미지 (file_open.png) 파일 존재 확인
    image_file = FILE_OPEN
    if not check_file_exists(image_file):
        print(get_info(), "탐색기 팝업 창에 [열기 버튼] 이미지 파일, [file_open.png]가 없습니다. 다시 확인하시오!!!")
        return

    # 1. 노랑 삼각형 [파일 없음 아이콘] 이미지 (file_doesnt_exist.png) 파일 존재 확인
    image_file = FILE_DOESNT_EXIST
    if not check_file_exists(image_file):
        print(get_info(),
              "[파일 없음] 팝업 창에서, 노랑 삼각형 [파일 없음 아이콘] 파일, [file_doesnt_exist.png]가 없습니다. 다시 확인하시오!!!")
        return

    # 1. 노랑 삼각형 [파일 이미 존재 아이콘] 이미지 (download_already_image.png) 파일 존재 확인
    image_file = DOWNLOAD_ALREADY_IMAGE
    if not check_file_exists(image_file):
        print(get_info(),
              "[파일 이미 존재] 팝업 창에서, 노랑 삼각형 [파일 이미 존재 아이콘] 파일, [download_already_image.png]가 없습니다. 다시 확인하시오!!!")
        return

    # 1. 덮어 쓰기를 위한 [Yes] 버튼 이미지 (download_already_image_yes.png) 파일 존재 확인
    image_file = DOWNLOAD_ALREADY_IMAGE_YES
    if not check_file_exists(image_file):
        print(get_info(),
              "[파일 이미 존재] 팝업 창에서, 덮어 쓰기를 위한 [Yes] 버튼 이미지 파일, [download_already_image_yes.png]가 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (ideogram_editbox.png) 파일 존재 확인
    image_file = IDEOGRAM_EDITBOX1
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 프롬프트 에디트 박스1 이미지 파일, ideogram_editbox1.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (ideogram_editbox.png) 파일 존재 확인
    image_file = IDEOGRAM_EDITBOX2
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 프롬프트 에디트 박스2 이미지 파일, ideogram_editbox2.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (ideogram_realistic.png) 파일 존재 확인
    image_file = IDEOGRAM_REALISTIC
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 [REALISTIC] 옵션 이미지 파일, ideogram_realistic.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # # 1. 이미지 (ideogram_magicprompt_on.png) 파일 존재 확인
    # image_file = IDEOGRAM_MAGICPROMPT_ON
    # if not check_file_exists(image_file):
    #     print(get_info(), "IDEOGRAM 이미지 생성 [MAGIC PROMPT-ON] 옵션 이미지 파일, ideogram_magicprompt_on.png 파일이 없습니다. 다시 확인하시오!!!")
    #     return
    #
    # # 1. 이미지 (ideogram_aspectratio_169.png) 파일 존재 확인
    # image_file = IDEOGRAM_ASPECTRATIO_169
    # if not check_file_exists(image_file):
    #     print(get_info(),
    #           "IDEOGRAM 이미지 생성 [ASPECT RATIO - 16:9] 옵션 이미지 파일, ideogram_aspectratio_169.png 파일이 없습니다. 다시 확인하시오!!!")
    #     return

    # 1. 이미지 (ideogram_generate.png) 파일 존재 확인
    image_file = IDEOGRAM_GENERATE
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 [GENERATE] 버튼 이미지 파일, ideogram_generate.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (ideogram_download.png) 파일 존재 확인
    image_file = IDEOGRAM_DOWNLOAD
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 [DOWNLOAD] 버튼 이미지 파일, ideogram_download.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (ideogram_download_png.png) 파일 존재 확인
    image_file = IDEOGRAM_DOWNLOAD_PNG
    if not check_file_exists(image_file):
        print(get_info(), "IDEOGRAM 이미지 생성 [DOWNLOAD PNG] 버튼 이미지 파일, ideogram_download_png.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (hailuo_video_queuing.png) 파일 존재 확인
    image_file = HAILUO_VIDEO_QUEUING
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_video_queuing.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (hailuo_camera_movement.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_MOVEMENT
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_movement.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # 1. 이미지 (hailuo_camera_debut.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_DEBUT
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_debut.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    # 1. 이미지 (hailuo_camera_freedom.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_FREEDOM
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_freedom.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    # 1. 이미지 (hailuo_camera_rightcircling.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_RIGHTCIRCLING
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_rightcircling.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    # 1. 이미지 (hailuo_camera_upwardtilt.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_UPWARDTILT
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_upwardtilt.png 파일이 없습니다. 다시 확인하시오!!!")
        return
    # 1. 이미지 (hailuo_camera_scenicshot.png) 파일 존재 확인
    image_file = HAILUO_CAMERA_SCENICSHOT
    if not check_file_exists(image_file):
        print(get_info(),
              "HAILUO 동영상 생성 진행 중 이미지 파일, hailuo_camera_scenicshot.png 파일이 없습니다. 다시 확인하시오!!!")
        return

    # print(get_info(), image_file, "을 찾았습니다. 계속 진행합니다.")

    if isExist:
        # 스레드 종료 신호 보내기
        stop_event.set()
        listener_thread.join()  # 스레드가 종료될 때까지 대기
        print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
        sys.exit()  # 프로그램 종료
        return

    ###############################################################################################################
    # todo: 오늘 날짜 자료를 확인하여, 자료가 모두 있으면, wrtn.scenario 생성은 하지 않는다.
    #       또한 image, video, music 파일을 체크하여, 이미 있으면, 생성하지 않는다.
    ###############################################################################################################

    param = "DIRECTORY"
    code_idea_current = STR_YMD + "1"
    code_scene_current = code_idea_current + "1"

    rsGetTodayData, dfScene = __getTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
    print(get_info(), "rsGetTodayData: ", rsGetTodayData)
    # print(get_info(), "dfScene: ", dfScene)
    print(get_info(), "len(dfScene): ", len(dfScene))

    # if len(dfScene) > 0:
    #     lastSceneCode = dfScene['CODE_SCENE'].iloc[-1] # 마지막 행의 'CODE_SCENE' 값 가져오기.
    #     lasti = int(lastSceneCode[-3])
    #     lastj = int(lastSceneCode[-2])
    #     print(get_info(), "lasti: ", lasti, ", lastj: ", lastj)

    # todo: 2025.02.17 Conclusion. 기존 자료 갯수가 5개가 아니면, 기존 자료 먼저 삭제 루틴은, 반드시 main()에서 처리해야 한다. .
    #       즉, 1개부터 24개까지 있으면, 삭제 한다. 없거나 25개 있으면, 자료는 그대로 두고, 프로그램은 계속 진행.
    # todo: 2025.02.18 Conclusion. ***** 여기서 [전체 삭제]를 하면 안 되고, 맨 마지막 조건 [scene] 별로 삭제 해야 한다.
    # if len(dfScene) > 0 and len(dfScene) < 25:
    #     print(get_info(), "len(dfScene): ", len(dfScene))
    #     rsDeleteCommit = __delTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
    #     print(get_info(), "rsDeleteCommit: ", rsDeleteCommit)
    #
    #     if not rsDeleteCommit:
    #         print(get_info(), f"{code_scene_current} 자료를 삭제하지 못 했습니다. 다시 확인하시오!")
    #         time.sleep(DELAY10)

    # todo: 2025.02.17 Conclusion. 현재 title 기준으로, 5개 SCENE 이면, 기존 자료 그대로 사용 하게 한다. 5개 이하면, 진행.
    # todo: 2025.02.17 Conclusion. 5 IDEA x 5 SCENE = 25 ROW 이면, [WRTN.뤼튼] 프롬프트 작업은 생략...
    if len(dfScene) == 25: # >= 25 ===> 25개 이상 이면 ???
        print(get_info(), f"현재 title {STR_YMD}는 기존 자료로 사용합니다.")
        print(get_info(), "바로 image, video, music 파일 생성 작업을 진행합니다............................................")

        # # 스레드 종료 신호 보내기
        # stop_event.set()
        # listener_thread.join()  # 스레드가 종료될 때까지 대기
        # print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
        # sys.exit()  # 프로그램 종료
        # return

    else:

        ###############################################################################################################
        # todo: 2025.02.12 Conclusion. 크롬 브라우저는 3개(wrtn,ideogram,hailuo)를 순서대로 열어 놓고, 프로그램을 실행 해야 한다.
        # todo: 2025.02.12 Added. WRTN.뤼튼 프롬프트 결과 받기.
        ###############################################################################################################
        print(get_info(), "WRTN.뤼튼 사이트를 오픈 합니다.")
        # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
        browser = "WRTN"
        rsWrtnOpen = __openWrtnSite(browser, WRTN, CENTERX, CENTERY, ICON_EDIT, SCREEN_TO_FIND_EDIT_ICON)
        print(get_info(), "rsWrtnOpen: ", rsWrtnOpen)

        if rsWrtnOpen:
            prompt = IDEA_ENG
            rsWrtnIdeas = __getWrtnAnswer(prompt, CENTERX, CENTERY, ICON_COPY, ICON_COPY_RED, SCREEN_TO_FIND_COPY_ICON)
        else:
            print(get_info(), "WRTN.뤼튼 사이트를 열지 못 했습니다. 관리자에게 문의 하시오!!!")
            # 스레드 종료 신호 보내기
            stop_event.set()
            listener_thread.join()  # 스레드가 종료될 때까지 대기
            print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
            sys.exit()  # 프로그램 종료
            return

        print(get_info(), "영상 제작을 위한, IDEA 입니다.")
        print(get_info(), rsWrtnIdeas)

        # todo: 정규 표현식을 사용하여 Title과 Content 추출
        ideas = rsWrtnIdeas
        # titles = re.findall(r'\*\*Title:\*\* (.*?)\s*\n', ideas) # [1. **Title:**] ===> [1. **Title:  ]
        titles = re.findall(r'\*\*Title:\*\* (.*?)\s*\n', ideas)
        contents = re.findall(r'\*\*Content:\*\* (.*?)\s*\n', ideas)
        print(get_info(), "Titles:", titles)
        print(get_info(), "Contents:", contents)

        # 각 변수에 저장 : locals() 변수임에 특히 유의.
        if len(titles) < 5 or len(contents) < 5:
            print(get_info(), "에러: [Title]과 [Contents]가 충분하지 않습니다. 다시 진행하시오!!!")
            title1, title2, title3, title4, title5 = titles + [''] * (5 - len(titles))
            content1, content2, content3, content4, content5 = contents + [''] * (5 - len(contents))
        else:
            title1, title2, title3, title4, title5 = titles
            content1, content2, content3, content4, content5 = contents

        title1 = title1.rstrip('*') # 맨 오른쪽 별표 없애기, 모든 별표 없애기는, title1.replace('*', '')
        title2 = title2.rstrip('*')
        title3 = title3.rstrip('*')
        title4 = title4.rstrip('*')
        title5 = title5.rstrip('*')

        # 결과 출력
        print(get_info(), "Titles:", title1, title2, title3, title4, title5)
        print(get_info(), "title1:", title1)
        print(get_info(), "title2:", title2)
        print(get_info(), "title3:", title3)
        print(get_info(), "title4:", title4)
        print(get_info(), "title5:", title5)
        print(get_info(), "Contents:", content1, content2, content3, content4, content5)
        print(get_info(), "content1:", content1)
        print(get_info(), "content2:", content2)
        print(get_info(), "content3:", content3)
        print(get_info(), "content4:", content4)
        print(get_info(), "content5:", content5)

        ###############################################################################################################
        ###############################################################################################################
        ###############################################################################################################

        # 2025.02.11 임시 값 정의...
        # title1 = "Trump and Musk: The Intergalactic Pizza Delivery Race!"
        # title2 = "LeBron James: The Chaotic Underwater Surgeon!"
        # title3 = "Taylor Swift’s Magical Musical Duel!"
        # title4 = "World Leaders in a Game Show Showdown!"
        # title5 = "Kim Kardashian: The Accidental Superhero!"
        # content1 = "Trump and Elon Musk race to deliver pizzas to aliens on distant planets, but their delivery methods lead to hilarious mishaps and unexpected detours!"
        # content2 = "LeBron finds himself in a deep-sea hospital, trying to perform surgery on fish while battling seaweed and an overly curious octopus!"
        # content3 = "Taylor Swift must face off against a sorcerer in a magical musical duel, where every song she sings accidentally transforms the audience into fantastical creatures!"
        # content4 = "World leaders compete in a wild game show, tackling absurd challenges like blindfolded cooking and extreme trivia, resulting in unexpected alliances and laughter!"
        # content5 = "Kim gains superpowers from a bizarre beauty product and must navigate her new life while trying to save her friends from fashion disasters in the most hilarious ways!"

        # 12. titil1 ~ title5 : 각각 사진 생성 프롬프트 생성 : 각각 5개 scene ===> 25개 scene

        # # scene_kor = "위 내용에 대해 5개 scene으로 구성하여, 구체적인 상황극으로 전개 해 줘. 영어로 해 주고, 내용을 2줄로 Scene, Scenario 나누어서 만들어 주고, copy icon을 클릭하면, 반드시 Scene 과 Scenario 양쪽에 별표 2개가 붙어 있게 해 줘. 이런식으로 : **Scene:**, **Scenario:**"
        # scene_kor = "아래 내용을 번역해 줘. 미드저니 AI 또는 ideogram AI 툴을 이용하여, 실사 이미지를 생성할 것이니, prompt 형식으로 번역해 줘. 아래: 위 내용에 대해 5개 scene으로 구성하여, 구체적인 상황극으로 전개 해 줘. 영어로 해 주고, 이 Scenaroo를 가지고, 미드저니 또는 ideogram AI Tool을 활용한 실사 사진 이미지 생성 Prompt로 활용할 거야. 내용을 2줄로 Scene, Scenario 나누어서 만들어 주고, copy icon을 클릭하면, 반드시 Scene 과 Scenario 양쪽에 별표 2개가 붙어 있게 해 줘. 이런식으로 : **Scene:**, **Scenario:**"
        #
        # # scene_eng = "Create a detailed scenario for each of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into 'SceneTitle' and 'SceneContent' in two lines."
        # # scene_eng = "Create a detailed scenario of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into Scene and Scenario in two lines."
        # # scene_eng = " : Create a detailed scenario of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into 'Scene' and 'Scenario' in two lines. When the copy icon is clicked, make sure to have double asterisks on both Scene and Scenario like this: **Scene:**, **Scenario:**"
        # scene_eng = " : For the content above, create a detailed scenario consisting of 5 scenes that develop a specific situation. This will be used as a prompt for generating realistic images using Midjourney or Ideogram AI tools. Please write in English and divide the content into 'Scene' and 'Scenario' in two lines. When the copy icon is clicked, make sure to have double asterisks on both Scene and Scenario like this: **Scene:**, **Scenario:**"
        # todo: 첫번째 문장 에러
        # print(get_info(), "delay1: ", delay1) # 에러 남.
        print(get_info(), "DELAY1: ", DELAY1) # 에러 안 남.
        for i in range(1, 6):
            # todo: 여기 for 문 내부에서는, 첫번째 문장(delay1)도 빨강색 밑줄만 안 보이지, 실제 프로스램 실행하면 에러 난다.
            # print(get_info(), "delay1: ", delay1)
            print(get_info(), "DELAY1: ", DELAY1)

            # todo: 제시된 코드에서 for 문 내에서 print("path_bs: ", path_bs)가 에러를 발생시키지 않는 이유는 Python의 스코프 규칙 때문입니다.
            #  스코프 규칙
            #  글로벌 변수: path_bs는 gv 모듈 내에서 글로벌 변수로 선언되어 있습니다.
            #  그러나 __makingPrompts 함수 내에서 path_bs를 직접적으로 사용하려고 하면, 해당 변수가 정의되지 않았기 때문에 에러가 발생합니다.
            #  for 문 내의 스코프: for 문 내에서는 path_bs가 에러를 발생시키지 않는 이유는,
            #  for 문이 __makingPrompts 함수의 로컬 스코프 내에 있기 때문입니다.
            #  Python은 for 문 내에서 로컬 변수를 찾고, 만약 로컬 스코프에 해당 변수가 없다면,
            #  상위 스코프(여기서는 __makingPrompts 함수의 스코프)에서 찾습니다.
            #  그러나 path_bs는 __makingPrompts 함수의 로컬 스코프에 정의되지 않았기 때문에, gv 모듈의 path_bs를 참조하게 됩니다."
            #  ===> Conclusion : 코드를 명확하게 하기 위해, path_bs를 사용하는 것이 좋습니다.
            #                    이렇게 하면 코드의 가독성이 높아지고, 어떤 변수를 참조하는지 명확해집니다.

            print(get_info(), f"i: {i}")

            # # 3.B.1 영어로 scene_eng_prompt 쓰기
            # pyautogui.moveTo(CENTERX - 400, CENTERY + 395, 1)
            # pyautogui.click()
            # pyautogui.hotkey('ctrl', 'a')
            # pyautogui.press('delete')
            # time.sleep(DELAY1)

            code_idea_current = STR_YMD + str(i)

            title_current = locals()[f'title{i}']
            content_current = locals()[f'content{i}']

            print(get_info(), f"i: {i}, title_current: {title_current}")
            print(get_info(), f"i: {i}, content_current: {content_current}")
            print(get_info(), f"i: {i}, locals()[f'title{i}']: ", locals()[f'title{i}'])
            print(get_info(), f"i: {i}, locals()[f'content{i}']: ", locals()[f'content{i}'])

            # scene_eng_prompt = os.path.join(globals()[f'title{i}'], globals()[f'content{i}'], scene_eng) # 이건 안 됨.
            # scene_eng_prompt0 = os.path.join(locals()[f'title{i}'], locals()[f'content{i}'], scene_eng) # .join() 안 됨.
            # print(get_info(), "scene_eng_prompt0: ", scene_eng_prompt0)

            # scene_eng_prompt2 = os.path.join(title_current, content_current, scene_eng)  # .join() 안 됨.
            # print(get_info(), "scene_eng_prompt2: ", scene_eng_prompt2)

            scene_eng_prompt = locals()[f'title{i}'] + " : " + locals()[f'content{i}'] + SCENE_ENG
            print(get_info(), "scene_eng_prompt: ", scene_eng_prompt)

            ###############################################################################################################
            # todo: 5개 idea 확인하여, 자료가 5개 모두 있으면, 저장하지 않고, 기존 자료를 사용한다.
            #       또한 image, video, music 파일을 체크하여, 이미 있으면, 생성하지 않는다.
            k = 1
            while True:
                param = "IDEA"
                code_scene_current = code_idea_current + "1"
                # code_scene_current = code_idea_current + str(ii)
                rsGetTodayData, dfScene = __getTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
                print(get_info(), "rsGetTodayData: ", rsGetTodayData)
                # print(get_info(), "dfScene: ", dfScene)
                print(get_info(), "code_idea_current:, ", code_idea_current, ", len(dfScene): ", len(dfScene))

                # # todo: 2025.02.17 Conclusion. 기존 자료 갯수가 5개가 아니면, 기존 자료 먼저 삭제 루틴은, 반드시 main()에서 처리해야 한다. .
                # #       즉, 1개부터 4개까지 있으면, 삭제 한다. 없거나 5개 있으면, 자료는 그대로 두고, 프로그램은 계속 진행.
                # todo: 2025.02.18 Conclusion. ***** 반드시 여기 [code_idea]를 체크해서, 있으면 여기서만 삭제해야 한다. *****
                #       위쪽 [DIRECTORY]를 기준한다거나, 아래쪽 [CODE_SCENE]를 기준하게 되면, 계속 [DELETE] 하고 [INSERT] 하게 된다.
                if len(dfScene) > 0 and len(dfScene) < 5:
                    print(get_info(), "len(dfScene): ", len(dfScene), ",k: ", k)
                    rsDeleteCommit = __delTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
                    print(get_info(), "rsDeleteCommit: ", rsDeleteCommit)
                    if rsDeleteCommit:
                        print(get_info(), f"{code_scene_current} 자료를 삭제하였습니다. 계속 image, video, music 파일 삭제.")

                        # todo: 2025.02.18 Conclusion. 파일 삭제는 하지 말고,
                        #       MORNING_CAFE_SCENE 테이블 자료를 삭제하고, 다시 해당 자료를 INSERT 했을 때,
                        #       IMAGE_NAME 컬럼 값이 없으면, IMAGE, VIDEO, MUSIC 파일을 생성하게 한다.
                        # for j in range(1, 6):
                        #     # image_name = STR_YMD + str(i) + str(j) + "0.png"
                        #     # video_name = STR_YMD + str(i) + str(j) + "0.mp4"
                        #     # music_name = STR_YMD + str(i) + str(j) + "04a
                        #     code_scene = STR_YMD + str(i) + str(j)
                        #     rsDeleteFile = __delFile(code_scene)
                        #     if not rsDeleteFile:
                        #         print(get_info(), code_scene, ".png, .mp4, .m4a 파일 삭제 실패하였습니다. 프로그램을 종료합니다.")
                        #         break

                    else:
                        print(get_info(), f"{code_scene_current} 자료를 삭제하지 못했습니다. 다시 확인하시오!")
                        time.sleep(DELAY10)
                        break

                    k += 1
                    time.sleep(DELAY1)

                # todo: 2025.02.17 Conclusion. 현재 title 기준으로, 5개 SCENE 이면, 기존 자료 그대로 사용 하게 한다. 5개 이하면, 진행.
                else:  # 0 or 5 or >= 5
                    rsDeleteCommit = True
                    print(get_info(), f"현재 title {title_current}는 최소한 1 or 2 or 3 or 4개는 아니네요. 계속 진행합니다.!")
                    break

            ###############################################################################################################

            ###############################################################################################################
            # todo: 2025.02.12 Added. WRTN.뤼튼 프롬프트 Scenarios 결과 받기.
            ###############################################################################################################
            # if rsWrtnOpen: # 이미 위에서 열려져 있다.
            prompt = SCENE_ENG
            rsWrtnScenarios = __getWrtnAnswer(prompt, CENTERX, CENTERY, ICON_COPY, ICON_COPY_RED, SCREEN_TO_FIND_COPY_ICON)
            # else:
            #     print(get_info(), "WRTN.뤼튼 사이트를 열지 못 했습니다. 관리자에게 문의 하시오!!!")
            #     # 스레드 종료 신호 보내기
            #     stop_event.set()
            #     listener_thread.join()  # 스레드가 종료될 때까지 대기
            #     print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
            #     sys.exit()  # 프로그램 종료
            #     return

            print(get_info(), "이미지 생성을 위한, Scenarios 입니다.")
            print(get_info(), rsWrtnScenarios)


            ###############################################################################################################
            ###############################################################################################################


            # copy 값 변수 저장
            globals()[f'scenes{i}'] = rsWrtnScenarios # pyperclip.paste()
            print(get_info(), f"i: {i}")
            print(get_info(), f"globals()[f'scenes{i}']: ", globals()[f'scenes{i}'])

            # 정규 표현식을 사용하여 Title과 Content 추출
            # globals()[f'titles{i}'] = re.findall(r'\*\*Title:\*\* (.*?)\s*\n', globals()[f'scenes{i}'])
            globals()[f'titles_scenes{i}'] = re.findall(r'\*\*Scene:\*\* (.*?)\s*\n', globals()[f'scenes{i}'])
            globals()[f'contents_scenarios{i}'] = re.findall(r'\*\*Scenario:\*\* (.*?)\s*\n', globals()[f'scenes{i}'])
            print(get_info(), f"i: {i}")
            print(get_info(), f"globals()[f'titles_scenes{i}']:", globals()[f'titles_scenes{i}'])
            print(get_info(), f"globals()[f'contents_scenarios{i}']:", globals()[f'contents_scenarios{i}'])

            # 각 변수에 저장
            if len(globals()[f'titles_scenes{i}']) < 5 or len(globals()[f'contents_scenarios{i}']) < 5:
                print(get_info(), "에러: [Scene]과 [Scenario]가 충분하지 않습니다. 다시 진행하시오!!!")
                # globals()[f'titles_scene1{i}'], globals()[f'titles_scene2{i}'], globals()[f'titles_scene3{i}'], globals()[f'titles_scene4{i}'], globals()[f'titles_scene5{i}'] = globals()[f'titles_scenes{i}'] + [''] * (5 - len(globals()[f'titles_scenes{i}']))
                # globals()[f'contents_scenario1{i}'], globals()[f'contents_scenario2{i}'], globals()[f'contents_scenario3{i}'], globals()[f'contents_scenario4{i}'], globals()[f'contents_scenario5{i}'] = globals()[f'contents_scenario{i}'] + [''] * (5 - len(globals()[f'contents_scenarios{i}']))
                globals()[f'titles_scene{i}1'], globals()[f'titles_scene{i}2'], globals()[f'titles_scene{i}3'], globals()[f'titles_scene{i}4'], globals()[f'titles_scene{i}5'] = globals()[f'titles_scenes{i}'] + [''] * (5 - len(globals()[f'titles_scenes{i}']))
                globals()[f'contents_scenario{i}1'], globals()[f'contents_scenario{i}2'], globals()[f'contents_scenario{i}3'], globals()[f'contents_scenario{i}4'], globals()[f'contents_scenario{i}5'] = globals()[f'contents_scenario{i}'] + [''] * (5 - len(globals()[f'contents_scenarios{i}']))
            else:
                # globals()[f'titles_scene1{i}'], globals()[f'titles_scene2{i}'], globals()[f'titles_scene3{i}'], globals()[f'titles_scene4{i}'], globals()[f'titles_scene5{i}'] = globals()[f'titles_scenes{i}']
                # globals()[f'contents_scenario1{i}'], globals()[f'contents_scenario2{i}'], globals()[f'contents_scenario3{i}'], globals()[f'contents_scenario4{i}'], globals()[f'contents_scenario5{i}'] = globals()[f'contents_scenarios{i}']
                globals()[f'titles_scene{i}1'], globals()[f'titles_scene{i}2'], globals()[f'titles_scene{i}3'], globals()[f'titles_scene{i}4'], globals()[f'titles_scene{i}5'] = globals()[f'titles_scenes{i}']
                globals()[f'contents_scenario{i}1'], globals()[f'contents_scenario{i}2'], globals()[f'contents_scenario{i}3'], globals()[f'contents_scenario{i}4'], globals()[f'contents_scenario{i}5'] = globals()[f'contents_scenarios{i}']

            # title1 = title1.rstrip('*')  # 맨 오른쪽 별표 없애기, 모든 별표 없애기는, title1.replace('*', '')
            # title2 = title2.rstrip('*')
            # title3 = title3.rstrip('*')
            # title4 = title4.rstrip('*')
            # title5 = title5.rstrip('*')

            # 결과 출력
            # print(get_info(), "Titles:", title1, title2, title3, title4, title5)
            print(get_info(), f"i: {i}")
            print(get_info(), f"globals()[f'titles_scene{i}1']:", globals()[f'titles_scene{i}1'])
            print(get_info(), f"globals()[f'titles_scene{i}2']:", globals()[f'titles_scene{i}2'])
            print(get_info(), f"globals()[f'titles_scene{i}3']:", globals()[f'titles_scene{i}3'])
            print(get_info(), f"globals()[f'titles_scene{i}4']:", globals()[f'titles_scene{i}4'])
            print(get_info(), f"globals()[f'titles_scene{i}5']:", globals()[f'titles_scene{i}5'])
            # print(get_info(), "Contents:", content1, content2, content3, content4, content5)
            print(get_info(), f"globals()[f'contents_scenario{i}1']:", globals()[f'contents_scenario{i}1'])
            print(get_info(), f"globals()[f'contents_scenario{i}2']:", globals()[f'contents_scenario{i}2'])
            print(get_info(), f"globals()[f'contents_scenario{i}3']:", globals()[f'contents_scenario{i}3'])
            print(get_info(), f"globals()[f'contents_scenario{i}4']:", globals()[f'contents_scenario{i}4'])
            print(get_info(), f"globals()[f'contents_scenario{i}5']:", globals()[f'contents_scenario{i}5'])
            print(get_info(), f"i: {i}")


            ###############################################################################################################
            # 13. 프롬프트 idea 5개와 각각의 idea에 대한 scene 5개, 즉 [25]개 자료 저장.
            ###############################################################################################################
            for ii in range(1, 6):

                print(get_info(), f"globals()[f'titles_scene{i}1']:", globals()[f'titles_scene{i}1'])
                print(get_info(), f"globals()[f'titles_scene{i}2']:", globals()[f'titles_scene{i}2'])
                print(get_info(), f"globals()[f'titles_scene{i}3']:", globals()[f'titles_scene{i}3'])
                print(get_info(), f"globals()[f'titles_scene{i}4']:", globals()[f'titles_scene{i}4'])
                print(get_info(), f"globals()[f'titles_scene{i}5']:", globals()[f'titles_scene{i}5'])
                # print(get_info(), "Contents:", content1, content2, content3, content4, content5)
                print(get_info(), f"globals()[f'contents_scenario{i}1']:", globals()[f'contents_scenario{i}1'])
                print(get_info(), f"globals()[f'contents_scenario{i}2']:", globals()[f'contents_scenario{i}2'])
                print(get_info(), f"globals()[f'contents_scenario{i}3']:", globals()[f'contents_scenario{i}3'])
                print(get_info(), f"globals()[f'contents_scenario{i}4']:", globals()[f'contents_scenario{i}4'])
                print(get_info(), f"globals()[f'contents_scenario{i}5']:", globals()[f'contents_scenario{i}5'])

                # todo: ===> 아래와 같이 1줄로 쓸 수 있다. 같은 결과가 나온다.

                # 프롬프트 공통 추가,
                # image: "사람의 손가락 부분은 가능하면 너무 노골적으로 크게 표현되지 않도록 했으면 한다"
                # video: "우아하고 부럽고 매우 천천히, 절대 빠르지 않게 움직이는 영상"

                print(get_info(), f"ii: ", {ii})
                print(get_info(), f"globals()[f'titles_scene{i}{ii}']: ", globals()[f'titles_scene{i}{ii}'])
                print(get_info(), f"globals()[f'contents_scenario{i}{ii}']: ", globals()[f'contents_scenario{i}{ii}'])

                scene_current = globals()[f'titles_scene{i}{ii}']
                scenario_current = globals()[f'titles_scene{i}{ii}'] + " : " + globals()[f'contents_scenario{i}{ii}'] + IMAGE_PROMPT_SUFFIX
                video_prompt_current = globals()[f'titles_scene{i}{ii}'] + " : " + globals()[f'contents_scenario{i}{ii}'] + VIDEO_PROMPT_SUFFIX

                current_image_file_name = STR_YMD + str(i) + str(ii) + "0.png"
                current_music_file_name = STR_YMD + str(i) + str(ii) + "0.m4a"
                current_video_file_name = STR_YMD + str(i) + str(ii) + "0.m4a"

                code_scene_current = STR_YMD + str(i) + str(ii)

                print(get_info(), "scene_current: ", scene_current)
                print(get_info(), "scenario_current: ", scenario_current)
                print(get_info(), "video_prompt_current: ", video_prompt_current)
                print(get_info(), "current_image_file_name: ", current_image_file_name)

                """
                Biden discovers that his favorite ice cream flavor has been stolen from the White House! Teaming up with Kevin Hart and Taylor Swift, they become amateur detectives, hilariously interrogating ice cream vendors and using ridiculous disguises, leading to an unexpected ice cream showdown in the middle of a county fair.
                "The Great Ice Cream Discovery!" : The video opens with Biden in the White House, eagerly anticipating his favorite ice cream flavor, only to find the freezer empty! Shocked and disappointed, he gathers Kevin Hart and Taylor Swift for an urgent meeting in the Oval Office. They comically brainstorm theories about the “ice cream thief,” leading to wild speculation and laughter. Please ensure that any depiction of human fingers is not overly pronounced or explicit.
                "The Great Ice Cream Discovery!" : The video opens with Biden in the White House, eagerly anticipating his favorite ice cream flavor, only to find the freezer empty! Shocked and disappointed, he gathers Kevin Hart and Taylor Swift for an urgent meeting in the Oval Office. They comically brainstorm theories about the “ice cream thief,” leading to wild speculation and laughter. Please ensure that any depiction of human fingers is not overly pronounced or explicit.
                """
                ###############################################################################################################
                # todo: 2025.02.14 Added. DB 저장
                ###############################################################################################################

                # todo: 2025.02.18 Conclusion. ***** 반드시 위쪽 [code_idea]를 체크해서, 있으면 거기서만 삭제해야 한다. *****
                #       최상단 [DIRECTORY]를 기준한다거나, 여기 [CODE_SCENE]를 기준하게 되면, 계속 [DELETE] 하고 [INSERT] 하게 된다.

                """
                # todo: 오늘 날짜 자료를 확인하여, 자료가 모두 있으면, wrtn.scenario 생성은 하지 않는다.
                #       또한 image, video, music 파일을 체크하여, 이미 있으면, 생성하지 않는다.
                k = 1
                while True:
                    param = "SCENE"
                    code_idea_current = STR_YMD + str(i)
                    code_scene_current = STR_YMD + str(i) + str(ii)
                    rsGetTodayData, dfScene = __getTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
                    print(get_info(), "rsGetTodayData ", rsGetTodayData)
                    # print(get_info(), "dfScene: ", dfScene)
                    print(get_info(), "code_idea_current:, ", code_idea_current, ", len(dfScene): ", len(dfScene))
    
                    # todo: 2025.02.17 Conclusion. 기존 자료 갯수가 5개가 아니면, 기존 자료 먼저 삭제 루틴은, 반드시 main()에서 처리해야 한다. .
                    #       즉, 1개부터 4개까지 있으면, 삭제 한다. 없거나 5개 있으면, 자료는 그대로 두고, 프로그램은 계속 진행.
                    if len(dfScene) > 0 and len(dfScene) < 5:
                        print(get_info(), "len(dfScene): ", len(dfScene), ",k: ", k)
                        rsDeleteCommit = __delTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
                        print(get_info(), "rsDeleteCommit: ", rsDeleteCommit)
                        if not rsDeleteCommit:
                            print(get_info(), f"{code_scene_current} 자료를 삭제하지 못했습니다. 다시 확인하시오!")
                            time.sleep(DELAY10)
                            break
    
                        k += 1
                        time.sleep(DELAY1)
    
                    # todo: 2025.02.17 Conclusion. 현재 title 기준으로, 5개 SCENE 이면, 기존 자료 그대로 사용 하게 한다. 5개 이하면, 진행.
                    else: # 0 or 5 or >= 5
                        rsDeleteCommit = True
                        print(get_info(), f"현재 title {title_current}는 최소한 1 or 2 or 3 or 4개는 아니네요. 계속 진행합니다.!")
                        break
                    """
                ###############################################################################################################

                rsInsertCommit = __insertCurrentRow1(CONNECTEDLOCAL, title_current, content_current, scene_current,
                                                     scenario_current, video_prompt_current,
                                                     code_idea_current, code_scene_current)

                print(get_info(), "rsInsertCommit: ", rsInsertCommit)
                if rsInsertCommit:
                    print(get_info(), code_scene_current, "자료를 Insert 성공하였습니다!!!")
                else:
                    print(get_info(), code_scene_current, "자료를 Insert 실패하였습니다. 확인 바랍니다!!!")
                    rsInsertCommit = False
                    break

                print(get_info(), f"{i}.{ii}번째 완료... 잠시 쉽니다!!!")
                time.sleep(DELAY3)
                # time.sleep(DELAY30)

                ###############################################################################################################
                ###############################################################################################################
                ###############################################################################################################
                ###############################################################################################################
                ###############################################################################################################

            if not rsInsertCommit:
                print(get_info(), f"{code_scene_current} 자료 추가에 실패하였습니다. 다시 확인하시오")

                print(get_info(), "The End........................................................")
                # 스레드 종료 신호 보내기
                stop_event.set()
                listener_thread.join()  # 스레드가 종료될 때까지 대기
                print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
                sys.exit()  # 프로그램 종료

        # return




    ###############################################################################################################
    ###############################################################################################################
    # todo: image, video, music 파일 생성 ##########################################################################
    ###############################################################################################################
    ###############################################################################################################

    # todo: 최 상단에서 실행했지만, 반드시 다시 실행해서, dfScene 자료를 새로 불러 와야 한다.
    param = "DIRECTORY"
    code_idea_current = STR_YMD + "1"
    code_scene_current = code_idea_current + "1"
    rsGetTodayData, dfScene = __getTodayData(CONNECTEDLOCAL, param, code_idea_current, code_scene_current)
    print(get_info(), "rsGetTodayData: ", rsGetTodayData)
    # print(get_info(), "dfScene: ", dfScene)
    print(get_info(), "len(dfScene): ", len(dfScene))

    print(get_info(), "image, video, music 파일을 생성합니다.")
    col_prn = ['CODE_IDEA', 'CODE_SCENE', 'IMAGE_NAME', 'VIDEO_NAME', 'MUSIC_NAME']
    # print(get_info(), "dfScene: \n", dfScene)
    print(get_info(), "dfScene[col_prn]: \n", dfScene[col_prn])
    print(get_info(), "len(dfScene): ", len(dfScene))

    if len(dfScene) >= 25:

        # 2025.02.19 Added. suno, riffusion AI 추가 : 노래 생성.
        scenarios = ""
        for i in range(len(dfScene)):
            print(get_info(), f"i: {i}")
            music_name = dfScene.iloc[i]['MUSIC_NAME']

            directory = dfScene.iloc[i]['DIRECTORY']
            code_idea = dfScene.iloc[i]['CODE_IDEA']
            code_scene = dfScene.iloc[i]['CODE_SCENE']
            scenario = str(i) + ". " + dfScene.iloc[i]['SCENARIO']
            video_prompt = str(i) + ". " + dfScene.iloc[i]['VIDEO_PROMPT']
            scenarios += scenario
            print(get_info(), "scenario: ", scenario)
            print(get_info(), "scenarios: ", scenarios)
            # music_prompt_suffix = "이제 나는 위의 다섯 가지 주제를 바탕으로 3분 길이의 코믹하고 유머러스한 영상을 만들었다. 이제 이 영상의 분위기에 맞는 음악 가사를 만들고 싶다."
            # music_prompt_suffix = "Now, I’ve created a 3-minute comic and humorous video based on the five themes above. Now, I want to write lyrics suitable for music that fits the atmosphere of the video."
            music_prompt = scenarios + " : " + MUSIC_PROMPT_SUFFIX
            print(get_info(), "music_prompt: ", music_prompt)
            music_file_name = directory + ".m4a"
            print(get_info(), "music_file_name: ", music_file_name)
        # 뮤직 파일이 있으면, skip...
        if music_name is not None:
            pass # 노래 파일이 이미 있으면, pass

        else: # 노래 파일이 없으면, 진행...

            ###############################################################################################################
            # todo: 2025.02.12 Added. 노래 가사를 위한, WRTN.뤼튼 프롬프트 Lyrics 결과 받기.
            ###############################################################################################################
            print(get_info(), "WRTN.뤼튼 사이트를 오픈 합니다.")
            # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
            browser = "RIFFUSION"
            rsWrtnOpen = __openWrtnSite(browser, WRTN, CENTERX, CENTERY, ICON_EDIT, SCREEN_TO_FIND_EDIT_ICON)
            print(get_info(), "rsWrtnOpen: ", rsWrtnOpen)

            if rsWrtnOpen:
                prompt = music_prompt
                rsWrtnMusic = __getWrtnAnswer(prompt, CENTERX, CENTERY, ICON_COPY, ICON_COPY_RED, SCREEN_TO_FIND_COPY_ICON)
            else:
                print(get_info(), "WRTN.뤼튼 사이트를 열지 못 했습니다. 관리자에게 문의 하시오!!!")
                # 스레드 종료 신호 보내기
                stop_event.set()
                listener_thread.join()  # 스레드가 종료될 때까지 대기
                print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
                sys.exit()  # 프로그램 종료
                return

            print(get_info(), "노래 생성을 위한, rsWrtnMusic 입니다.")
            print(get_info(), rsWrtnMusic)

            # todo: "이런 자료를 참고했어요" 앞에 까지만 가져 오기 : 이걸 꼭 먼저 처리 해야 한다.
            reference_start = rsWrtnMusic.find("이런 자료를 참고했어요")
            references = ""
            if reference_start != -1:
                lyrics_all = rsWrtnMusic[:reference_start].strip()  # 처음부터 ~ 시작 인덱스 까지 슬라이스
                references = rsWrtnMusic[reference_start + len("이런 자료를 참고했어요"):].strip()  # 구문 뒤 부터 ~ 끝까지 슬라이스
            print(get_info(), "lyrics_all: ", lyrics_all)  # str
            print(get_info(), "type(lyrics_all): ", type(lyrics_all))
            print(get_info(), "references: ", references)

            # todo: "###" 뒤 부터 가져 오기 : 맨 첫 줄 제거
            sharp_start = lyrics_all.find("###")
            if reference_start != -1:
                lyrics = lyrics_all[:reference_start].strip()  # 처음부터 ~ 시작 인덱스 까지 슬라이스
            print(get_info(), "lyrics: ", lyrics) # str
            print(get_info(), "type(lyrics): ", type(lyrics))

            # 모든 구절과 후렴을 찾기 위한 정규 표현식

            # pattern = r'### \*\*(Verse |Intro|Chorus|Bridge|Outro|Fional Chorus):\*\*'
            # todo: 위 pattern 구문은 ? 이 패턴은 제목만을 찾는 정규 표현식입니다.

            # pattern = r'### \*\*(Verse |Intro|Chorus|Bridge|Outro|Fional Chorus):\*\*([\s\S]*?)(?=### ]*]*|$)'
            # todo: 위 pattern 구문은 ?
            # 이 패턴은 특정 섹션(Verse, Intro, Chorus, Bridge, Outro, Final Chorus)의 제목을 찾고, 그 뒤에 오는 내용을 캡처합니다.
            # ([\s\S]*?)는 해당 제목 뒤에 오는 모든 텍스트를 비어 있는 줄이나 다음 제목이 나타날 때까지 캡처합니다.
            # (?=### ]*]*|$)는 제목이 끝나는 위치를 찾는 부분으로, 다음 제목이나 문자열의 끝을 기준으로 캡처를 종료합니다.

            # lyrics1 = re.findall(pattern, lyrics_all)
            # print(get_info(), "lyrics1: ", lyrics1)
            # print(get_info(), "type(lyrics1): ", type(lyrics1)) # list

            # pattern = r'### \*\*(Verse |Intro|Chorus|Bridge|Outro|Final Chorus):\*\*([\s\S]*?)(?=### ]*]*|$)'
            # pattern = r'### \*\*(Verse |Intro|Chorus|Bridge|Outro|Final Chorus):\*\*([\s\S]*?)(?=###|\Z)'
            # todo: 위 pattern 구문은 ?
            # 이 패턴은 특정 섹션(Verse, Intro, Chorus, Bridge, Outro, Final Chorus)의 제목을 찾고, 그 뒤에 오는 내용을 캡처합니다.
            # ([\s\S]*?)는 해당 제목 뒤에 오는 모든 텍스트를 비어 있는 줄이나 다음 제목이 나타날 때까지 캡처합니다.
            # (?=###|\Z)는 제목이 끝나는 위치를 찾는 부분으로, 문자열의 끝을 기준으로 캡처를 종료합니다.

            # lyrics2 = re.findall(pattern, lyrics_all)
            # print(get_info(), "lyrics2: ", lyrics2)
            # print(get_info(), "type(lyrics2): ", type(lyrics2)) # list

            # [### **Verse 1:**]에서 [###]과 [**] 제거
            lyrics_pure = "\n".join([ly.replace("### **", "").replace("**", "").strip() for ly in lyrics.splitlines() if ly.strip()])
            print(get_info(), "lyrics_pure: ", lyrics_pure)
            print(get_info(), "type(lyrics_pure): ", type(lyrics_pure)) # 이것도 list

            # lyrics_pure = lyrics.replace('### **', '').replace('**', '').replace('\n', ' ').strip()
            lyrics_pure = lyrics.replace('### **', '').replace('**', '').strip()
            print(get_info(), "lyrics_pure: ", lyrics_pure)
            print(get_info(), "type(lyrics_pure): ", type(lyrics_pure))  # str

            # lyrics = [ly.replace('### **', '').replace('**', '') for ly in lyrics] # list를 처리하면, 에러: AttributeError: 'tuple' object has no attribute 'replace'
            # lyrics = [ly.replace('### **', '').replace('**', '') for ly in lyrics_all] # list를 처리하면, 에러.
            # 첫 번째 요소만 사용하여 문자열로 변환
            # lyrics = [ly[1].replace('### **', '').replace('**', '').strip() for ly in lyrics]
            # 순수한 가사 부분만 가져오기
            # lyrics = [ly.strip() for _, ly in lyrics]

            # print(get_info(), "lyrics: ", lyrics)
            # print(get_info(), "type(lyrics): ", type(lyrics))

            # 결과 출력
            # for section in lyric:
            #     print(get_info(), "section: ", section)

            # print(get_info(), "lyric: ", lyric)

            # lyrics_chk = "" # lyrics 체크
            # for title, ly in lyrics:
            #     title = f"**{title}:**"
            #     lyric = ly.strip()
            #     print(get_info(), f"**{title}:**")
            #     print(get_info(), ly.strip())
            #     print(get_info(), "\n")
            #     lyrics += f'**{title}:**' + " : " + ly
            # print(get_info(), "lyrics_chk: ", lyrics_chk)

            # return

            ###############################################################################################################
            # todo: 2025.02.19 Added. suno, riffusion AI 추가 : 노래 생성.
            #       music 파일 생성
            #       2개 노래 파일 생성 : 첫번째 파일명 : current_music_file_name, 두번째 파일명: current_music_file_name2.m4a
            ###############################################################################################################
            print(get_info(), "lyrics_pure: ", lyrics_pure)
            print(get_info(), "type(lyrics_pure): ", type(lyrics_pure))
            prompt = lyrics_pure
            rs_music = __getMusic(prompt, music_file_name, PATH_YMD, DOWNLOAD_PATH, DOWNLOAD_SAVE, DOWNLOAD_ALREADY_IMAGE,
                                 SCREEN_TO_FIND_DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_SAVE,
                                 SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE,
                                 CENTERX, CENTERY, RIFFUSION, RIFFUSION_GENERATE, SCREEN_TO_FIND_RIFFUSION_GENERATE,
                                 RIFFUSION_GHOSTWRITER, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER,
                                 RIFFUSION_GHOSTWRITER_UPDATE, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE)

            print(get_info(), "rs_music: ", rs_music)
            print(get_info(), "노래 파일을 성공적으로 생성 완료 하였습니다.")

            # 여기서는 두번째 노래 파일 명은 필요가 없다.
            # if rs_save:
            #     music_name = os.path.splitext(current_image_file_name)[0]
            #     music_ext = os.path.splitext(current_image_file_name)[1]
            #     current_image_file_name2 = music_name + "2" + music_ext

            ###############################################################################################################
            # todo: music_name 저장....
            #  MORNING_CAFE_SCENE.LYRICS_PROMPT, .LYRICS : 가사 프롬프트, 가사 값 저장, music_name : 두번째 노래 파일은 저장 안 함.
            ###############################################################################################################
            print(get_info(), "directory: ", directory)
            print(get_info(), "code_idea: ", code_idea)
            print(get_info(), "music_file_name: ", music_file_name)
            print(get_info(), "prompt: ", prompt)
            print(get_info(), "type(prompt): ", type(prompt))
            print(get_info(), "lyrics: ", lyrics)
            print(get_info(), "type(lyrics): ", type(lyrics))
            print(get_info(), "뮤직 파일, 테이블에 정리, 저장 작업을 진행 합니다...")
            k = 1
            while True:
                sql = """
                    UPDATE MORNING_CAFE_SCENE SET LYRICS_PROMPT = %s, LYRICS = %s, MUSIC_NAME = %s 
                    WHERE DIRECTORY = %s
                """
                values = (prompt, lyrics, music_file_name, directory)
                rsUpdateCommit = __updateData(CONNECTEDLOCAL, sql, values)

                if not rsUpdateCommit:
                    print(get_info(), f"{music_file_name} 파일명 업데이트 실패! 10초 후 다시 진행... k: ", k)
                    k += 1
                    time.sleep(DELAY10)
                else:
                    print(get_info(), f"{music_file_name} 파일명 업데이트 성공!")
                    break

            print(get_info(), f"{directory} 노래 파일명 업데이트 완료... 잠시 쉽니다!!!")
            time.sleep(DELAY5)

            ###############################################################################################################
            ###############################################################################################################

            # return

        ###############################################################################################################
        # todo: 2025.02.19 Conclusion. image 파일만 먼저 생성한다. video 파일은 image 파일을 먼저 다 생성한 후에 따로 생성.
        ###############################################################################################################

        # todo: image 파일만 먼저 생성...


        ###############################################################################################################
        # todo: image 파일 생성 ##########################################################################
        ###############################################################################################################

        for i in range(len(dfScene)):
            print(get_info(), f"i: {i}")

            code_scene = dfScene.iloc[i]['CODE_SCENE']
            title = dfScene.iloc[i]['TITLE']
            content = dfScene.iloc[i]['CONTENT']
            scene = dfScene.iloc[i]['SCENE']
            scenario = dfScene.iloc[i]['SCENARIO']

            image_name = dfScene.iloc[i]['IMAGE_NAME']
            video_name = dfScene.iloc[i]['VIDEO_NAME']
            music_name = dfScene.iloc[i]['MUSIC_NAME']

            # 이미지 파일이 있으면, skip...
            if image_name is not None:
                continue

            current_scenario_prompt = scenario

            ii = int(code_scene.strip()[-2:])
            print(get_info(), f"ii: {ii}")

            current_image_file_name = STR_YMD + str(ii) + "0.png"
            current_video_file_name = STR_YMD + str(ii) + "0.mp4"
            current_music_file_name = STR_YMD + str(ii) + "0.m4a"

            print(get_info(), f"i: {i}, title: {title}")
            print(get_info(), f"i: {i}, content: {content}")
            print(get_info(), f"i: {i}, code_scene: {code_scene}")
            print(get_info(), f"i: {i}, scene: {scene}")
            print(get_info(), f"i: {i}, scenario: {scenario}")

            print(get_info(), "current_scenario_prompt: ", current_scenario_prompt)
            print(get_info(), "current_image_file_name: ", current_image_file_name)
            print(get_info(), "current_music_file_name: ", current_music_file_name)

            ###############################################################################################################
            # 13. Scene 과 Scenario 이용, 사진 이미지 생성
            ###############################################################################################################

            # 2025.02.12 Added. 현재 크롬 브라우저가 이미 열려 있는지 확인.
            # 0. 크롬 브라우저 아이콘 클릭
            # pyautogui.moveTo(CENTERX - 840, CENTERY + 515, 1)
            # pyautogui.click()
            # time.sleep(DELAY9)

            if is_chrome_running():
                # 0.1 크롬 브라우저 첫번째 열었던 브라우저 화면 클릭
                pyautogui.moveTo(CENTERX - 840, CENTERY + 515, 1)
                # pyautogui.click() # 여기는 클릭하면 안 되고, 그냥 이동만 해야 한다.
                time.sleep(DELAY1)
                pyautogui.moveTo(CENTERX - 840, CENTERY + 470, 1)
                pyautogui.click()
                time.sleep(DELAY1)
                # 0.2 첫번째 열었던 브라우저에서, 2번째 태그(ideogram) 클릭
                pyautogui.moveTo(CENTERX - 660, CENTERY - 520, 1)
                pyautogui.click()
                time.sleep(DELAY1)

            # 1. site address 기존 내용 삭제
            pyautogui.moveTo(CENTERX + 300, CENTERY - 480, 1)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(DELAY1)

            # 1.4 site address : ideogram pro모드 열기.
            # pyautogui.typewrite(IDEOGRAM)
            pyperclip.copy(IDEOGRAM)  # 텍스트를 클립보드에 반드시 복사
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(DELAY1)
            pyautogui.press('enter')
            time.sleep(DELAY20) # 30초 대기...

            # 디렉토리 생성 : "G:\Youtube\DonGang\MorningCafe\2025\202502\today() : 20250203" 맨 끝에는 "\" 없음에 유의
            # if not check_directory(PATH_YM, STR_YMD): # [PATH_YMD]가 아님에 주의.
            #     print(get_info(), "오늘 날짜의 폴더를 먼저 확인 하시오!!!")
            #     return

            print(get_info(), "PATH_BS: ", PATH_BS, ", PATH_BASE: ", PATH_BASE, ", PATH_YEAR: ", PATH_YEAR)
            print(get_info(), "PATH_YEAR: ", PATH_YEAR, ", PATH_YM: ", PATH_YM, ", PATH_YMD: ", PATH_YMD)

            ###############################################################################################################
            # 이미지 프롬프트 쓰기
            ###############################################################################################################
            # -500 -260 : 프롬프트 위치
            # ctrl + a => delete
            # pyautogui.moveTo(CENTERX - 500, CENTERY - 260, 1)
            # pyautogui.click()
            # ===> 이미지 찾아서 클릭 하는 방식으로 변경
            # 1. 이미지 (ideogram_editbox.png) 파일 존재 확인
            k = 1
            while True:
                if k % 2 == 0:
                    image_file = IDEOGRAM_EDITBOX1
                    screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_EDITBOX1
                else:
                    image_file = IDEOGRAM_EDITBOX2
                    screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_EDITBOX2
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 프롬프트 에디트 박스를 클릭하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... 프롬프트 에디트 박스 이미지를 찾을 수 없습니다. 10초간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)

            time.sleep(DELAY1)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(DELAY1)
            # # +180 -250 : 지우게 아이콘 클릭 : 한번 더 지우기.
            # pyautogui.moveTo(CENTERX + 180, CENTERY - 250, 1)
            # pyautogui.click()
            # time.sleep(DELAY1)

            # current_scenario_prompt 쓰기 : paste
            # pyautogui.typewrite(current_scenario_prompt)
            current_scenario_prompt = scenario
            pyperclip.copy(current_scenario_prompt)  # 텍스트를 클립보드에 반드시 복사
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(DELAY1)

            # -480 +20  : Auto 버튼 ===> Realistic 버튼 -260 +150
            # pyautogui.moveTo(CENTERX - 480, CENTERY + 150, 1) # Auto 버튼
            # pyautogui.moveTo(CENTERX - 270, CENTERY + 150, 1) # Realistic 버튼
            # pyautogui.click()
            # ===> 이미지 찾아서 클릭 하는 방식으로 변경
            # 1. 이미지 (ideogram_realistic.png) 파일 존재 확인
            k = 1
            image_file = IDEOGRAM_REALISTIC
            screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_REALISTIC
            while True:
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 [REALISTIC] 옵션 버튼을 클릭하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... [REALISTIC] 옵션 버튼 이미지를 찾을 수 없습니다. 10초간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)

            time.sleep(DELAY1)

            # +480 -315 : Magic Prompt => On 버튼
            pyautogui.moveTo(CENTERX + 480, CENTERY - 190, 1)
            pyautogui.click()
            time.sleep(DELAY1)
            # +525 -260 : Aspect ratio => 16:9
            pyautogui.moveTo(CENTERX + 525, CENTERY - 140, 1)
            pyautogui.click()
            time.sleep(DELAY1)
            # +420 -210 : Visibility => Public
            # pyautogui.moveTo(CENTERX + 420, CENTERY - 210, 1)
            # pyautogui.click()
            # time.sleep(DELAY1)

            # +500 +20 : Generate 버튼
            # pyautogui.moveTo(CENTERX + 500, CENTERY + 150, 1)
            # pyautogui.click()
            # ===> 이미지 찾아서 클릭 하는 방식으로 변경
            # 1. 이미지 (ideogram_generate.png) 파일 존재 확인
            k = 1
            image_file = IDEOGRAM_GENERATE
            screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_GENERATE
            while True:
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 [GENERATE] 버튼을 클릭하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... [GENERATE] 버튼 이미지를 찾을 수 없습니다. 10초간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)

            print(get_info(), "이미지 생성 버튼까지 클릭 했습니다!!! 1분간 대기합니다...")

            time.sleep(DELAY60)

            # todo: [ideogram_gemeration_complete.png] 이미지 파일 확인하여, 있으면, 다음 진행.
            # 나중에 필요하면... 이미지 생성 시, 시간이 너무 오래 걸리면, 아래 루틴 필요.

            # 1. 이미지 (ideogram_generation_complete.png) 파일 존재 확인
            # 2. ideogram_generation_complete.png 이미지 위치 값 가져 오기.
            image_file = IDEOGRAM_GENERATION_COMPLETE
            screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_GENERATION_COMPLETE
            while True:
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 이미지 생성을 완료하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... 이미지 생성이 아직 진행 중입니다. 다시 1분간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY60)

            # +400 +200 : 2/4면 그림 클릭
            pyautogui.moveTo(CENTERX + 400, CENTERY + 200, 1)
            pyautogui.click()
            time.sleep(DELAY5)

            # ideogram_cover.png 아이콘 찾기 및 클릭
            # 1. 이미지 (ideogram_cover.png) 파일 존재 확인
            image_file = IDEOGRAM_COVER
            # if not check_file_exists(image_file):
            #     print(get_info(), "복사 아이콘 이미지 파일, icon_copy.png 파일이 없습니다. 다시 확인하시오!!!")
            #     return

            # 2. ideogram_cover.png 이미지 위치 값 가져 오기.
            screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_ICON
            k = 1
            while True:
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "[cover] 이미지를 클릭했습니다.")
                    break
                else:
                    print(get_info(), "[cover] 이미지를 찾을 수 없습니다! 10초간 대기하고 찾을 때까지 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)

            # 3. ideogram_cover.png 이미지 위치를 기준으로, 클릭 위치 조정 ===> x 값을 그대로
            print(get_info(), "ideogram_cover.png 아이콘이 붙은 이미지를 클릭 했습니다!!!")

            time.sleep(DELAY5)

            # +800 -310 : 저장을 위한 설정 버튼 클릭
            # pyautogui.moveTo(CENTERX + 800, CENTERY - 310, 1)
            # pyautogui.click()
            # ===> 이미지 찾아서 클릭 하는 방식으로 변경
            # 1. 이미지 (ideogram_download.png) 파일 존재 확인
            k = 1
            image_file = IDEOGRAM_DOWNLOAD
            while True:
                screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 [DOWNLOAD] 버튼을 클릭하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... [DOWNLOAD] 버튼 이미지를 찾을 수 없습니다. 10초간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)
            time.sleep(DELAY1)

            # +670 +120 : [Download PNG] 버튼 클릭
            # pyautogui.moveTo(CENTERX + 670, CENTERY + 120, 1)
            # pyautogui.click()
            # ===> 이미지 찾아서 클릭 하는 방식으로 변경
            # 1. 이미지 (ideogram_download_png.png) 파일 존재 확인
            k = 1
            image_file = IDEOGRAM_DOWNLOAD_PNG
            while True:
                screen_to_find_image = SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_PNG
                if find_image(image_file, screen_to_find_image):
                    print(get_info(), "IDEOGRAM에서 [DOWNLOAD PNG] 버튼을 클릭하였습니다.")
                    break
                else:
                    print(get_info(), "IDEOGRAM... [DOWNLOAD PNG] 버튼 이미지를 찾을 수 없습니다. 10초간 대기하고, 루프 돕니다... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)

            time.sleep(DELAY10)

            print(get_info(), f"i: {i}, ii: {ii}")
            print(get_info(), "scene: ", scene)
            print(get_info(), "scenario: ", scenario)

            # download path : ctrl + v => enter ===> path_ymd : "G:\Youtube\DonGang\MorningCafe\2025\202502\20250203"
            # todo: 파일 저장 팝업 창...
            #       클릭한 상태에서, 팝업 창에 바로 쓰기 : 110.png 파일 명 먼저 쓰기 ===> 팝업 창이 비 고정 이므로...
            print(get_info(), "current_image_file_name: ", current_image_file_name)
            # pyautogui.typewrite(current_image_file_name)
            pyperclip.copy(current_image_file_name)  # 텍스트를 클립보드에 반드시 복사
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(DELAY1)

            # todo: [폴더 경로] download_path.png 이미지 찾기 및 클릭
            #  1. [폴더 경로] 이미지 (download_path.png) 파일 존재 확인
            image_file = DOWNLOAD_PATH
            screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_PATH
            # todo: 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
            while True:
                # 2. [폴더 경로] 이미지와 동일한 부분 클릭
                if not find_image(image_file, screen_to_find_image):
                    print(get_info(), "윈도우 탐색기 팝업 창이 열리지 않습니다. 1분간 대기... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY60) # 2025.02.13 Added. 파일 저정을 위한 [탐색기] 창이, 간혹 엄청 느리게 나오네.
                else:
                    break

            print(get_info(), "탐색기 팝업 창에서 [경로 아이콘]이 있는 [에디트 박스]를 클릭하였습니다!!!")

            # todo: 탐색기 팝업창에서 [저장 경로 에디트 박스]를 이미 클릭 했다.
            # download path : ctrl + a => delete
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(DELAY1)
            # path_ymd 쓰기 : paste
            # pyautogui.typewrite(path_ymd)
            print(get_info(), "저장 경로, PATH_YMD: ", PATH_YMD)
            pyperclip.copy(PATH_YMD)  # 텍스트를 클립보드에 반드시 복사
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(DELAY1)
            pyautogui.press('enter')
            time.sleep(DELAY3)

            # 2. 이미지와 동일한 부분 클릭
            k = 1
            image_file = DOWNLOAD_SAVE
            screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_SAVE
            while True:
                if not find_image(image_file, screen_to_find_image):
                    print(get_info(), "윈도우 탐색기 창에서 [저장] 버튼을 찾을 수 없습니다. 10초간 대기... k: ", k)
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    k += 1
                    time.sleep(DELAY10)
                else:
                    break

            print(get_info(), "탐색기 팝업 창에서 [저장] 버튼을 클릭하였습니다!!!")

            # todo: download_already_image.png 파일 찾기 및 클릭
            #  if download_already_image.png 화면 찾기 성공 : 팝업 창이 떳다는 이야기...
            # download_already_image.png 이미지 찾기 및 클릭
            # 1. 노랑 삼각형 [파일 이미 존재 아이콘] 이미지 (download_already_image.png) 파일 존재 확인
            # image_file = DOWNLOAD_ALREADY_IMAGE
            # if not check_file_exists(image_file):
            #     print(get_info(), "[파일 이미 존재] 팝업 창에서, 노랑 삼각형 [파일 이미 존재 아이콘] 파일, [download_already_image.png]가 없습니다. 다시 확인하시오!!!")
            #     return

            # 2. 노랑 삼감형 [파일 이미 존재 아이콘] 이미지와 동일한 부분 확인 : 여기서는 우/하 이동, [Yes] 버튼 클릭.
            # A.
            # # while True:
            # screen_to_find_image = screen_to_find_download_already_image
            # if not find_image(image_file, screen_to_find_image):
            #     print(get_info(), "center_img_x: -1, center_img_y: -1, 이미지를 찾을 수 없습니다!!!")
            #     return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
            #     # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
            # # else:
            # #     break
            # B.
            # todo: 2025.02.13 위 A.와 B. 다시 확인해 볼 것.
            #       1. [파일 이미 있음] 또는 [파일 없음] 팝업 창이 나오고, 안 나오고
            #       2. 나온 후, [파일 이미 있음] => [Yes] 또는 [파일 없음] => [확인] 버튼 클릭 등 처리...
            # todo: 여기서만 [True] 일 때, 프로그램을 종료하게 한다. ∵) 현재 폴더에 이미지 [파일 없음] 이므로...
            image_file = DOWNLOAD_ALREADY_IMAGE
            screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE
            while True:
                if not find_image(image_file, screen_to_find_image):
                    print(get_info(), f"동영상을 만들 이미지 파일, {current_image_file_name}이 없습니다. 프로그램을 종료합니다!")
                    break
                else:
                    print(get_info(), "[파일 이미 있음] 팝업 창이 나오지 않고, 덮어쓰기 [Yes] 팝업 창이 열렸습니다.")
                    # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                    # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                    time.sleep(DELAY1)

                    # todo: download_already_image_yes.png 파일 찾기 및 클릭
                    # 1. 덮어 쓰기를 위한 [Yes] 버튼 이미지 (download_already_image_yes.png) 파일 존재 확인
                    k = 1
                    image_file = DOWNLOAD_ALREADY_IMAGE_YES
                    # 2. 덮어 쓰기를 위한 [Yes] 버튼 이미지와 동일한 부분 클릭
                    screen_to_find_image = SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES
                    while True:
                        if find_image(image_file, screen_to_find_image):
                            print(get_info(), "[파일 이미 있음] 팝업 창에 덮어쓰기 [Yes] 버튼을 클릭하였습니다.")
                            break
                        else:
                            print(get_info(), "[파일 이미 있음] 팝업 창에 덮어쓰기 [Yes] 버튼 이미지를 찾을 수 없습니다!!! 10초가 대개... k: ", k)
                            # return  # 프로그램 종료하고, [에러 카톡 발송] 한다.
                            # return # 프로그램 종료가 아니고, 계속 진행한다. 이미 [편집 화면 부분]이 감춰져 있다는 의미임.
                            k += 1
                            time.sleep(DELAY10)

                    break # 이 화면은 안 뜬다는 것은, 기존 파일명이 없다는 것이므로, 이미 위 [저장] 버튼 클릭할 때, 저장되었다는 의미.

            print(get_info(), "이미지 저장 팝업 창에, 파일 [덮어 쓰기] [Yes]로 클릭하였습니다!!! 10초간 대기...")
            time.sleep(DELAY10)

            ###############################################################################################################
            # todo: IMAGE_NAME 저장....
            #  MORNING_CAFE_SCENE.IMAGE_NAME
            ###############################################################################################################
            print(get_info(), "code_idea: ", code_idea)
            print(get_info(), "code_scene: ", code_scene)
            print(get_info(), "current_image_file_name: ", current_image_file_name)
            print(get_info(), "이미지 파일, 테이블에 정리, 저장 작업을 진행 합니다...")
            while True:
                sql = """
                UPDATE MORNING_CAFE_SCENE SET IMAGE_NAME = %s WHERE CODE_SCENE = %s
                """
                values = (current_image_file_name, code_scene)
                rsUpdateCommit = __updateData(CONNECTEDLOCAL, sql, values)

                if not rsUpdateCommit:
                    print(get_info(), f"{current_image_file_name} 업데이트 실패! 10초 후 다시 진행...")
                    time.sleep(DELAY10)
                else:
                    print(get_info(), f"{current_image_file_name} 업데이트 성공!")
                    break

            print(get_info(), f"{code_scene} 이미지 파일명 업데이트 완료... 잠시 쉽니다!!!")
            time.sleep(DELAY5)

            ###############################################################################################################
            ###############################################################################################################

            print(get_info(), f"ii: {ii}번째 이미지 파일을 저장했습니다. ", current_image_file_name)

            print(get_info(), "동영상 hailuo 사이트로 바로 넘어 갑니다! ===> 아니고, 이미지 먼저 완료 하고 마지막에 동영상 생성!")
            # print(get_info(), f"{i}.{ii}번째 완료... 잠시 쉽니다!!!")
            time.sleep(DELAY5)



        ###############################################################################################################
        ###############################################################################################################
        # todo: hailuo 동영상 생성 : https://hailuoai.video/create
        ###############################################################################################################
        ###############################################################################################################
        print(get_info(), "동영상 hailuo 사이트로 바로 넘어 갑니다!")

        for i in range(len(dfScene)):
            print(get_info(), f"i: {i}, len(dfScene): {len(dfScene)}")

            print(get_info(), "동영상 hailuo 사이트로 넘어 가기 전에, 프로그램을 일단 종료 합니다!")
            # break

            code_scene = dfScene.iloc[i]['CODE_SCENE']
            title = dfScene.iloc[i]['TITLE']
            content = dfScene.iloc[i]['CONTENT']
            scene = dfScene.iloc[i]['SCENE']
            scenario = dfScene.iloc[i]['SCENARIO']
            video_prompt = dfScene.iloc[i]['VIDEO_PROMPT']

            image_name = dfScene.iloc[i]['IMAGE_NAME']
            video_name = dfScene.iloc[i]['VIDEO_NAME']
            music_name = dfScene.iloc[i]['MUSIC_NAME']

            print(get_info(), "code_scene: ", code_scene)
            print(get_info(), "image_name: ", image_name)
            print(get_info(), "music_name: ", music_name)
            print(get_info(), "video_name: ", video_name)
            # 이미지 파일이 있으면, skip...
            if video_name is not None:
                print(get_info(), "video_name: ", video_name, "이 이미 있습니다. 다음으로...")
                continue
            else:
                if video_name is not None:
                    print(get_info(), "len(video_name): ", len(video_name))
                # continue

            current_video_prompt = video_prompt

            ii = int(code_scene.strip()[-2:])
            print(get_info(), f"ii: {ii}")

            current_image_file_name = STR_YMD + str(ii) + "0.png"
            current_video_file_name = STR_YMD + str(ii) + "0.mp4"
            current_music_file_name = STR_YMD + str(ii) + "0.m4a"

            print(get_info(), f"i: {i}, title: {title}")
            print(get_info(), f"i: {i}, content: {content}")
            print(get_info(), f"i: {i}, code_scene: {code_scene}")
            print(get_info(), f"i: {i}, scene: {scene}")
            print(get_info(), f"i: {i}, scenario: {scenario}")
            print(get_info(), f"i: {i}, video_prompt: {video_prompt}")

            print(get_info(), "current_video_prompt: ", current_video_prompt)
            print(get_info(), "current_image_file_name: ", current_image_file_name)
            print(get_info(), "current_music_file_name: ", current_music_file_name)

            ###############################################################################################################
            ###############################################################################################################
            # todo: hailuo 동영상 생성 : https://hailuoai.video/create
            ###############################################################################################################
            ###############################################################################################################

            print(get_info(), "code_scene: ", code_scene)
            print(get_info(), "current_video_prompt: ", current_video_prompt)
            # 2025.03.04 Conclusion. "Xu Jinping" or "Xi Jinping" 모두 프롬프트에서 제거 해야 한다.
            current_video_prompt = current_video_prompt.replace("Xu ", "CB")
            current_video_prompt = current_video_prompt.replace("Xi ", "CB")
            current_video_prompt = current_video_prompt.replace("Xu Jinping", "ClearBrook")
            current_video_prompt = current_video_prompt.replace("Xi Jinping", "ClearBrook")
            print(get_info(), "current_video_prompt: ", current_video_prompt)

            print(get_info(), "current_image_file_name: ", current_image_file_name)
            print(get_info(), "current_music_file_name: ", current_music_file_name)
            print(get_info(), "current_video_file_name: ", current_video_file_name)
            rs_video = __getVideo(CONNECTEDLOCAL, HAILUO, CENTERX, CENTERY, PATH_YMD, FILE_OPEN, OPEN_PATH,
                                  SCREEN_TO_FIND_OPEN_PATH,
                                  SCREEN_TO_FIND_FILE_OPEN, FILE_DOESNT_EXIST, SCREEN_TO_FIND_FILE_DOESNT_EXIST,
                                  SCREEN_TO_FIND_VIDEO_TWINS, DOWNLOAD_PATH, SCREEN_TO_FIND_DOWNLOAD_PATH,
                                  DOWNLOAD_ALREADY_IMAGE, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE,
                                  DOWNLOAD_SAVE, SCREEN_TO_FIND_DOWNLOAD_SAVE,
                                  DOWNLOAD_ALREADY_IMAGE_YES, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES,
                                  HAILUO_VIDEO_QUEUING, SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING,
                                  HAILUO_CAMERA_MOVEMENT, HAILUO_CAMERA_DEBUT_FILE, HAILUO_CAMERA_FREEDOM,
                                  HAILUO_CAMERA_RIGHTCIRCLING, HAILUO_CAMERA_UPWARDTILT, HAILUO_CAMERA_SCENICSHOT,
                                  SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT, SCREEN_TO_FIND_HAILUO_CAMERA_12345,
                                  HAILUO_VIDEO_GENERATE, SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE,
                                  HAILUO_VIDEO_REEDIT, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT,
                                  HAILUO_VIDEO_REEDIT_REPLACE, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE,
                                  HAILUO_VIDEO_VIOLATED, SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED,
                                  code_scene, current_video_prompt,
                                  current_image_file_name, current_music_file_name, current_video_file_name)

            print(get_info(), "rs_video: ", rs_video)

            if not rs_video: # Text content violated. ===> 프로그램 종료하고 프롬프트 규칙 수정해야 한다. "Xi, Xu, Xi Jinping ..."
                print(get_info(), f"동영상 생성을 위한 텍스트 프롬프트에 [위반 내용]이 있습니다. 시스템 종료!!!")
                break

            # return


    else:
        print(get_info(), "dfhttps://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/67a0ec8b5f86b8e4ad7b8385Scene 자료가 1도 없습니다. 다시 확인하시오!!!")
        time.sleep(DELAY10)



    print(get_info(), "프로그램을 종료합니다........................................................")
    time.sleep(DELAY10)

    # 스레드 종료 신호 보내기
    stop_event.set()
    listener_thread.join()  # 스레드가 종료될 때까지 대기
    print("모든 스레드가 종료되었습니다. 프로그램을 종료합니다!")
    sys.exit()  # 프로그램 종료

    return

###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################

# print("ESC 키를 누릅니다!!!")
# pyautogui.press('esc')
# sys.exit()
# okng = "OK"
# return okng



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Caps Lock 상태 확인
    # if keyboard.is_pressed('capslock'):  # 요걸로는 안 되네...
    # # if keyboard.get_mods() & keyboard.modifiers['capslock']:
    #     # Caps Lock이 활성화된 경우, 다시 눌러서 비활성화
    #     keyboard.press_and_release('capslock')
    #     print("Caps Lock이 비활성화되었습니다.")
    # else:
    #     print("Caps Lock이 비활성화된 상태입니다.")

    turn_capslock_off()
    time.sleep(1)
    the_text = "THIS TEXT will always be writen in LOWERCASE!!!"
    # pyautogui.typewrite(the_text.lower(), interval=0.02) // 현재 화면에 한 번 쓰고 시작한다...

    # ///////////////////////////////////////////////////////////////////////////////////////////////////

    # ESC 키 감지.
    stop_event = threading.Event()  # 스레드 간 통신을 위한 이벤트 객체 생성

    # ESC 키 감지를 위한 스레드 시작
    # listener_thread = threading.Thread(target=listen_for_escape, args=(stop_event,))
    listener_thread = threading.Thread(target=listen_for_escape, args=(stop_event,))
    listener_thread.start()

    __makingPrompts(PATH, stop_event)

    # # 스레드가 종료될 때까지 대기
    listener_thread.join()

    # Thread(target=__production_actual(path)).start()
    # Thread(target=exit_program).start()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/



    # todo: 2025.02.14 클래스형 프로그램 : 아직 잘 안 되네...
    # try:
    #
    #     morningcafe = MorningCafe()
    #
    #     # listener_thread = threading.Thread(target=morningcafe.listen_for_escape, args=(stop_event,))
    #     # listener_thread.start()
    #
    #     morningcafe.__makingPrompts(path, stop_event)
    #     sys.exit()
    #
    #     # 스레드가 종료될 때까지 대기
    #     # listener_thread.join()
    #
    # except:
    #
    #     sys.exit()