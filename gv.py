# 2025.02.12 Created. Youtube 동영상 자동 생성 시스템에 대한, 글로벌 변수 모음
"""
todo : 반드시 아래 내용(차이)을 숙지/이해 하고, 사용해야 한다.
todo : 결국 두 방법 모두 글로벌 변수를 사용할 수 있지만, set_globals() 함수를 사용하는 방법이 더 유연하고 가독성이 좋습니다.
todo : 특히, 변수를 초기화하는 로직이 복잡해질 경우 함수로 분리하는 것이 유지보수에 유리합니다.
todo : 반면, 간단한 초기화가 필요할 경우에는 함수 없이 변수를 선언하는 방법도 유용할 수 있습니다.

todo : 가장 큰 차이는, 다른 파일(main.py 등)에서 사용할 때,
todo : A 방식에서는 ===> [gv.변수명]으로 사용 해야 하고, B 방식에서는 ===> [변수명]으로 사용 해야 한다는 것입니다.

###############################################################################################################
A 방식 : function 선언 해서 글로벌 변수 사용 방법
###############################################################################################################

# global_val.py
from datetime import datetime

# 글로벌 변수 선언
path_bs = ''
str_year = ''
str_ym = ''
str_ymd = ''
file_bs = ''
ext_bs = ''
num_var = 0  # 숫자형 글로벌 변수 추가

def set_globals():
    global path_bs, str_year, str_ym, str_ymd, file_bs, ext_bs, num_var
    path_bs = 'G:\\Youtube\\DonGang\\MorningCafe\\'
    str_year = datetime.now().strftime('%Y')
    str_ym = datetime.now().strftime('%Y%m')
    str_ymd = datetime.now().strftime('%Y%m%d')
    file_bs = 'MorningCafe'
    ext_bs = '.xlsx'
    num_var = 42  # 숫자형 글로벌 변수에 값 할당

1. 초기화 시점: set_globals() 함수를 호출해야만 글로벌 변수가 초기화됩니다. 이로 인해 변수를 사용하는 코드가 실행되기 전에 반드시 이 함수를 호출해야 합니다.
2. 가독성: 변수를 초기화하는 로직이 함수로 분리되어 있어, 코드의 가독성이 높아집니다. 초기화 로직이 명확하게 드러나기 때문에, 다른 개발자가 코드를 이해하기 쉽습니다.
3. 유연성: 필요에 따라 여러 번 호출하여 변수를 재설정할 수 있습니다. 예를 들어, 다른 조건에 따라 변수를 다르게 초기화할 수 있습니다.

###############################################################################################################
B 방식 : function 선언 없이 글로벌 변수 사용 방법.
###############################################################################################################
# global_val.py
from datetime import datetime

global path_bs, str_year, str_ym, str_ymd, file_bs, ext_bs, num_var
path_bs = 'G:\\Youtube\\DonGang\\MorningCafe\\'
str_year = datetime.now().strftime('%Y')
str_ym = datetime.now().strftime('%Y%m')
str_ymd = datetime.now().strftime('%Y%m%d')
file_bs = 'MorningCafe'
ext_bs = '.xlsx'
num_var = 42  # 숫자형 글로벌 변수에 값 할당

1. 초기화 시점: global_val.py가 임포트될 때, 모든 변수가 즉시 초기화됩니다. 따라서, 변수를 사용하는 코드가 실행되기 전에 별도로 초기화할 필요가 없습니다.
2. 가독성: 모든 변수가 한 곳에 선언되어 있어 간단하게 보일 수 있지만, 초기화 로직이 복잡해지면 가독성이 떨어질 수 있습니다.
3. 유연성: 변수를 초기화하는 로직을 변경하기 어려워집니다. 예를 들어, 조건에 따라 다른 값을 설정하고 싶다면, 추가적인 로직을 구현해야 합니다.
"""
import os.path

# import os
from util import *
from datetime import datetime

CONNECTEDLOCAL = False
CONNECTEDWEB = False

PATH_BS = 'G:\\Youtube\\DonGang\\MorningCafe\\'  # 'D:\\BspDev\\Dev\\'
# path_bs = r'G:\Youtube\DonGang\' # r'G:~~' 이렇게 [r]을 먼저 써 주면, "\"가 1개만 있어야 된다.
STR_YEAR = datetime.now().strftime('%Y')
STR_YM = datetime.now().strftime('%Y%m')

# 2025.03.05 Conclusion. 오늘 날짜 지정...
STR_YMD = datetime.now().strftime('%Y%m%d')
# todo: 2025.03.05 Conclusion. 특정 날짜 강제 지정...
# STR_YMD = "20250304"

FILE_BS = 'MorningCafe'
EXT_BS = '.xlsx'

PATH_CURRENT = os.getcwd()  # "G:\Python\Workspace\PyAutoGui"
# print(f"path_current: {path_current}, path_bs: {path_bs}")

"""
2024.08.07 Conclusion.
datetime.datetime.now()에서 에러가 발생하는 이유는 datetime 모듈을 가져오는 방식에 있습니다. 
datetime 모듈을 import datetime로 가져오면 datetime 클래스에 접근하기 위해 datetime.datetime으로 호출해야 합니다. 
하지만 from datetime import datetime와 같이 datetime 클래스를 직접 가져오면 datetime.now()로 호출할 수 있습니다.
아래는 두 가지 방법을 보여주는 코드입니다:
"""

DATE_FORMAT = "%Y.%m.%d"  # 날짜 형식 지정

# now = datetime.datetime.now()
NOW = datetime.now()
YEAR_CURRENT = str(NOW.year)
MONTH_CURRENT = str(NOW.month).zfill(2)  # 'str' 변환이 없으면 에러: 'int' object has no attribute 'zfill'
MONTH_CURRENT = '{0:02d}'.format(NOW.month)  # 'str'
# 7월 생산 실적 등록...
# month_current = '{0:02d}'.format(now.month - 1)  # 'str'
DAY_CURRENT = '{0:02d}'.format(NOW.day)  # 'str'
DATE_CURRENT = NOW.date()  # "2024-08-05" <class 'str'>
# print(get_info(), f"year_current: {year_current}, month_current: {month_current}, day_current: {day_current}, date_current: {date_current}")
# print(get_info(), f"year_current.type: {type(year_current)}, month_current.type: {type(month_current)}, day_current.type: {type(day_current)}, type(date_current): {type(date_current)}")

FILE_FULL_NAME = FILE_BS + STR_YEAR + EXT_BS

PATH_BASE = os.path.join(PATH_BS, STR_YEAR, STR_YM, STR_YMD)
PATH = os.path.join(PATH_BASE, FILE_FULL_NAME) # 'MorningCafe2025.xlsx' : 이게 의미가 있나?

PATH_YEAR = os.path.join(PATH_BS, STR_YEAR)
PATH_YM = os.path.join(PATH_BS, STR_YEAR, STR_YM)
PATH_YMD = os.path.join(PATH_BS, PATH_YEAR, STR_YM, STR_YMD)

COMPANY_CODE = ""
HOST0 = ""
USER0 = ""
PASS0 = ""
DBNAME0 = ""
HOST1 = ""
USER1 = ""
PASS1 = ""
DBNAME1 = ""

MSSQLSERVERDB = "" # pymssql.connect(server=gv.host0, user=gv.user0, password=gv.pass0, database=gv.dbname0)
CURSARRAYSERVER = "" # gv.msSqlServerDb.cursor()

MYSQLLOCALDB = "" # pymysql.connect(host=gv.host1, port=3306, user=gv.user1, password=gv.pass1, db=gv.dbname1, charset='utf8')
CURSARRAYLOCAL = "" # gv.mySqlLocalDb.cursor()
CURSDICTLOCAL = "" # gv.mySqlLocalDb.cursor(pymysql.cursors.DictCursor)

BOUNCE_TIME = 0
SLEEP_TIME = 0
TIME_GAP = 0
NIGHT_CLOSING_HHMMSS = ""
DAY_CLOSING_HHMMSS  = ""

# print(get_info(), "file_full_name: ", file_full_name)
print(get_info(), "PATH_BASE: ", PATH_BASE)
print(get_info(), "PATH: ", PATH)
print(get_info(), "PATH_YEAR: ", PATH_YEAR)
print(get_info(), "PATH_YM: ", PATH_YM)
print(get_info(), "PATH_YMD: ", PATH_YMD)

ICON_EDIT_FILE = 'icon_edit.png'
ICON_EDIT_POS_FILE = 'icon_edit_pos.png'
ICON_EDIT = os.path.join(PATH_YEAR, ICON_EDIT_FILE)
ICON_EDIT_POS = os.path.join(PATH_YEAR, ICON_EDIT_POS_FILE)
print(get_info(), "ICON_EDIT: ", ICON_EDIT)
print(get_info(), "ICON_EDIT_POS: ", ICON_EDIT_POS)

SCREEN_TO_FIND_EDIT_ICON_FILE = 'screen_to_find_edit_icon_file.png'
SCREEN_TO_FIND_EDIT_ICON = os.path.join(PATH_YEAR, SCREEN_TO_FIND_EDIT_ICON_FILE)

ICON_HANGUL_FILE = 'icon_hangul.png'  # 770,500
ICON_HANGUL_POS_FILE = 'icon_hangul_pos.png'
ICON_HANGUL = os.path.join(PATH_YEAR, ICON_HANGUL_FILE)
ICON_HANGUL_POS = os.path.join(PATH_YEAR, ICON_HANGUL_POS_FILE)
print(get_info(), "ICON_HANGUL: ", ICON_HANGUL)
print(get_info(), "ICON_HANGUL_POS: ", ICON_HANGUL_POS)

ICON_ENGLISH_FILE = 'icon_english.png'
ICON_ENGLISH_POS_FILE = 'icon_english_pos.png'
ICON_ENGLISH = os.path.join(PATH_YEAR, ICON_ENGLISH_FILE)
ICON_ENGLISH_POS = os.path.join(PATH_YEAR, ICON_ENGLISH_POS_FILE)

ICON_COPY_FILE = 'icon_copy.png'
ICON_COPY_RED_FILE = 'icon_copy_red.png'
ICON_COPY_POS_FILE = 'icon_copy_pos.png'
ICON_COPY = os.path.join(PATH_YEAR, ICON_COPY_FILE)
ICON_COPY_RED = os.path.join(PATH_YEAR, ICON_COPY_RED_FILE)
ICON_COPY_POS = os.path.join(PATH_YEAR, ICON_COPY_POS_FILE)

CHROME_SELECT_USER_FILE = 'chrome_select_user.png'
CHROME_SELECT_USER = os.path.join(PATH_YEAR, CHROME_SELECT_USER_FILE)
SCREEN_TO_FIND_CHROME_USER_FILE = 'screen_to_find_chrome_user.png'
SCREEN_TO_FINE_CHROME_USER = os.path.join(PATH_YEAR, SCREEN_TO_FIND_CHROME_USER_FILE)

SCREEN_TO_FIND_COPY_ICON_FILE = 'screen_to_find_copy_icon.png'
# icon_copy_pos_file = 'icon_english_pos.png'
SCREEN_TO_FIND_COPY_ICON = os.path.join(PATH_YEAR, SCREEN_TO_FIND_COPY_ICON_FILE)
# icon_copy_pos = os.path.join(path_year, icon_copy_pos_file)

IDEOGRAM_COVER_FILE = 'ideogram_cover.png'
IDEOGRAM_COVER = os.path.join(PATH_YEAR, IDEOGRAM_COVER_FILE)
SCREEN_TO_FIND_IDEOGRAM_ICON_FILE = 'screen_to_find_ideogram_icon.png'
SCREEN_TO_FIND_IDEOGRAM_ICON = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_ICON_FILE)

IDEOGRAM_GENERATION_COMPLETE_FILE = "ideogram_generation_complete.png"
IDEOGRAM_GENERATION_COMPLETE = os.path.join(PATH_YEAR, IDEOGRAM_GENERATION_COMPLETE_FILE)
SCREEN_TO_FIND_IDEOGRAM_GENERATION_COMPLETE = "screen_to_find_ideogram_generation_complete_file.png"
SCREEN_TO_FIND_IDEOGRAM_GENERATION = os.path.join(PATH_YEAR, IDEOGRAM_GENERATION_COMPLETE_FILE)

DOWNLOAD_PATH_FILE = 'download_path.png'
DOWNLOAD_PATH = os.path.join(PATH_YEAR, DOWNLOAD_PATH_FILE)
SCREEN_TO_FIND_DOWNLOAD_PATH_FILE = 'screen_to_find_download_path.png'
SCREEN_TO_FIND_DOWNLOAD_PATH = os.path.join(PATH_YEAR, SCREEN_TO_FIND_DOWNLOAD_PATH_FILE)

# download_path_file0 = 'download_path0.png'
# download_path0 = os.path.join(path_year, download_path_file0)
# screen_to_find_download_path_file0 = 'screen_to_find_download_path0.png'
# screen_to_find_download_path0 = os.path.join(path_year, screen_to_find_download_path_file0)
# download_path_file1 = 'download_path1.png'
# download_path1 = os.path.join(path_year, download_path_file1)
# screen_to_find_download_path_file1 = 'screen_to_find_download_path1.png'
# screen_to_find_download_path1 = os.path.join(path_year, screen_to_find_download_path_file1)

DOWNLOAD_SAVE_FILE = 'download_save.png'
DOWNLOAD_SAVE = os.path.join(PATH_YEAR, DOWNLOAD_SAVE_FILE)
SCREEN_TO_FIND_DOWNLOAD_SAVE_FILE = 'screen_to_find_download_save.png'
SCREEN_TO_FIND_DOWNLOAD_SAVE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_DOWNLOAD_SAVE_FILE)

DOWNLOAD_ALREADY_IMAGE_FILE = 'download_already_image.png'
DOWNLOAD_ALREADY_IMAGE = os.path.join(PATH_YEAR, DOWNLOAD_ALREADY_IMAGE_FILE)
SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_FILE = 'screen_to_find_download_image.png'
SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_FILE)

DOWNLOAD_ALREADY_IMAGE_YES_FILE = 'download_already_image_yes.png'
DOWNLOAD_ALREADY_IMAGE_YES = os.path.join(PATH_YEAR, DOWNLOAD_ALREADY_IMAGE_YES_FILE)
SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES_FILE = 'screen_to_find_download_image_yes.png'
SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES = os.path.join(PATH_YEAR, SCREEN_TO_FIND_DOWNLOAD_ALREADY_IMAGE_YES_FILE)

OPEN_PATH_FILE = 'open_path.png'
OPEN_PATH = os.path.join(PATH_YEAR, OPEN_PATH_FILE)
SCREEN_TO_FIND_OPEN_PATH_FILE = 'screen_to_find_open_path.png'
SCREEN_TO_FIND_OPEN_PATH = os.path.join(PATH_YEAR, SCREEN_TO_FIND_OPEN_PATH_FILE)

FILE_OPEN_FILE = 'file_open.png'
FILE_OPEN = os.path.join(PATH_YEAR, FILE_OPEN_FILE)
SCREEN_TO_FIND_FILE_OPEN_FILE = 'screen_to_find_file_open.png'
SCREEN_TO_FIND_FILE_OPEN = os.path.join(PATH_YEAR, SCREEN_TO_FIND_FILE_OPEN_FILE)

FILE_DOESNT_EXIST_FILE = 'file_doesnt_exist.png'
FILE_DOESNT_EXIST = os.path.join(PATH_YEAR, FILE_DOESNT_EXIST_FILE)
SCREEN_TO_FIND_FILE_DOESNT_EXIST_FILE = 'screen_to_find_file_doesnt_exist.png'
SCREEN_TO_FIND_FILE_DOESNT_EXIST = os.path.join(PATH_YEAR, SCREEN_TO_FIND_FILE_DOESNT_EXIST_FILE)

RIFFUSION_GHOSTWRITER_FILE = 'riffusion_ghostwriter.png'
RIFFUSION_GHOSTWRITER = os.path.join(PATH_YEAR, RIFFUSION_GHOSTWRITER_FILE)
SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_FILE = 'screen_to_find_riffusion_ghostwriter.png'
SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER = os.path.join(PATH_YEAR, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_FILE)

RIFFUSION_GHOSTWRITER_UPDATE_FILE = 'riffusion_ghostwriter_update.png'
RIFFUSION_GHOSTWRITER_UPDATE = os.path.join(PATH_YEAR, RIFFUSION_GHOSTWRITER_UPDATE_FILE)
SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE_FILE = 'screen_to_find_riffusion_ghostwriter_update.png'
SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_RIFFUSION_GHOSTWRITER_UPDATE_FILE)

RIFFUSION_GENERATE_FILE = 'riffusion_generate.png'
RIFFUSION_GENERATE = os.path.join(PATH_YEAR, RIFFUSION_GENERATE_FILE)
SCREEN_TO_FIND_RIFFUSION_GENERATE_FILE = 'screen_to_find_riffusion_generate.png'
SCREEN_TO_FIND_RIFFUSION_GENERATE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_RIFFUSION_GENERATE_FILE)

SCREEN_TO_FIND_VIDEO_TWINS_FILE = 'screen_to_find_video_twins.png'
SCREEN_TO_FIND_VIDEO_TWINS = os.path.join(PATH_YEAR, SCREEN_TO_FIND_VIDEO_TWINS_FILE)

IDEOGRAM_EDITBOX1_FILE = 'ideogram_editbox1.png'
IDEOGRAM_EDITBOX1 = os.path.join(PATH_YEAR, IDEOGRAM_EDITBOX1_FILE)
SCREEN_TO_FIND_IDEOGRAM_EDITBOX1_FILE = 'screen_to_find_ideogram_editbox1.png'
SCREEN_TO_FIND_IDEOGRAM_EDITBOX1 = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_EDITBOX1_FILE)

IDEOGRAM_EDITBOX2_FILE = 'ideogram_editbox2.png'
IDEOGRAM_EDITBOX2 = os.path.join(PATH_YEAR, IDEOGRAM_EDITBOX2_FILE)
SCREEN_TO_FIND_IDEOGRAM_EDITBOX2_FILE = 'screen_to_find_ideogram_editbox2.png'
SCREEN_TO_FIND_IDEOGRAM_EDITBOX2 = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_EDITBOX2_FILE)

IDEOGRAM_REALISTIC_FILE = 'ideogram_realistic.png'
IDEOGRAM_REALISTIC = os.path.join(PATH_YEAR, IDEOGRAM_REALISTIC_FILE)
SCREEN_TO_FIND_IDEOGRAM_REALISTIC_FILE = 'screen_to_find_ideogram_realistic.png'
SCREEN_TO_FIND_IDEOGRAM_REALISTIC = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_REALISTIC_FILE)

IDEOGRAM_GENERATE_FILE = 'ideogram_generate.png'
IDEOGRAM_GENERATE = os.path.join(PATH_YEAR, IDEOGRAM_GENERATE_FILE)
SCREEN_TO_FIND_IDEOGRAM_GENERATE_FILE = 'screen_to_find_ideogram_generate.png'
SCREEN_TO_FIND_IDEOGRAM_GENERATE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_GENERATE_FILE)

IDEOGRAM_DOWNLOAD_FILE = 'ideogram_download.png'
IDEOGRAM_DOWNLOAD = os.path.join(PATH_YEAR, IDEOGRAM_DOWNLOAD_FILE)
SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_FILE = 'screen_to_find_ideogram_download.png'
SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_FILE)

IDEOGRAM_DOWNLOAD_PNG_FILE = 'ideogram_download_png.png'
IDEOGRAM_DOWNLOAD_PNG = os.path.join(PATH_YEAR, IDEOGRAM_DOWNLOAD_PNG_FILE)
SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_PNG_FILE = 'screen_to_find_ideogram_download_png.png'
SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_PNG = os.path.join(PATH_YEAR, SCREEN_TO_FIND_IDEOGRAM_DOWNLOAD_PNG_FILE)

HAILUO_VIDEO_GENERATE_FILE = 'hailuo_video_generate.png'
HAILUO_VIDEO_GENERATE = os.path.join(PATH_YEAR, HAILUO_VIDEO_GENERATE_FILE)
SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE_FILE = 'screen_to_find_hailuo_video_generate.png'
SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_VIDEO_GENERATE_FILE)

HAILUO_VIDEO_VIOLATED_FILE = 'hailuo_video_violated.png'
HAILUO_VIDEO_VIOLATED = os.path.join(PATH_YEAR, HAILUO_VIDEO_VIOLATED_FILE)
SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED_FILE = 'screen_to_find_hailuo_video_violated.png'
SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_VIDEO_VIOLATED_FILE)

HAILUO_VIDEO_REEDIT_FILE = 'hailuo_video_reedit.png'
HAILUO_VIDEO_REEDIT = os.path.join(PATH_YEAR, HAILUO_VIDEO_REEDIT_FILE)
SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_FILE = 'screen_to_find_hailuo_video_reedit.png'
SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_FILE)

HAILUO_VIDEO_REEDIT_REPLACE_FILE = 'hailuo_video_reedit_replace.png'
HAILUO_VIDEO_REEDIT_REPLACE = os.path.join(PATH_YEAR, HAILUO_VIDEO_REEDIT_REPLACE_FILE)
SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE_FILE = 'screen_to_find_hailuo_video_reedit_replace.png'
SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_VIDEO_REEDIT_REPLACE_FILE)

HAILUO_VIDEO_QUEUING_FILE = 'hailuo_video_queuing.png'
HAILUO_VIDEO_QUEUING = os.path.join(PATH_YEAR, HAILUO_VIDEO_QUEUING_FILE)
SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING_FILE = 'screen_to_find_hailuo_video_queuing.png'
SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_VIDEO_QUEUING_FILE)

HAILUO_CAMERA_MOVEMENT_FILE = 'hailuo_camera_movement.png'
HAILUO_CAMERA_MOVEMENT = os.path.join(PATH_YEAR, HAILUO_CAMERA_MOVEMENT_FILE)
SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT_FILE = 'screen_to_find_hailuo_camera_movement.png'
SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_CAMERA_MOVEMENT_FILE)

HAILUO_CAMERA_DEBUT_FILE = 'hailuo_camera_debut.png'
HAILUO_CAMERA_DEBUT = os.path.join(PATH_YEAR, HAILUO_CAMERA_DEBUT_FILE)
HAILUO_CAMERA_FREEDOM_FILE = 'hailuo_camera_freedom.png'
HAILUO_CAMERA_FREEDOM = os.path.join(PATH_YEAR, HAILUO_CAMERA_FREEDOM_FILE)
HAILUO_CAMERA_RIGHTCIRCLING_FILE = 'hailuo_camera_rightcircling.png'
HAILUO_CAMERA_RIGHTCIRCLING = os.path.join(PATH_YEAR, HAILUO_CAMERA_RIGHTCIRCLING_FILE)
HAILUO_CAMERA_UPWARDTILT_FILE = 'hailuo_camera_upwardtilt.png'
HAILUO_CAMERA_UPWARDTILT = os.path.join(PATH_YEAR, HAILUO_CAMERA_UPWARDTILT_FILE)
HAILUO_CAMERA_SCENICSHOT_FILE = 'hailuo_camera_scenicshot.png'
HAILUO_CAMERA_SCENICSHOT = os.path.join(PATH_YEAR, HAILUO_CAMERA_SCENICSHOT_FILE)
SCREEN_TO_FIND_HAILUO_CAMERA_12345_FILE = 'screen_to_find_hailuo_camera_12345.png'
SCREEN_TO_FIND_HAILUO_CAMERA_12345 = os.path.join(PATH_YEAR, SCREEN_TO_FIND_HAILUO_CAMERA_12345_FILE)

WIDTH, HEIGHT = pyautogui.size()
CENTERX, CENTERY = WIDTH // 2, HEIGHT // 2

# wrtn Pro모드
# wrtn = "https://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/66a6aba08c86fb9e8153cdb4"
# wrtn AI 이미지
# wrtn = "https://wrtn.ai/chat/u/66309fe4fa99736573f691be/c/6786a4938470afebf6598b56"

# wrtn AI 과제와 업무-Pro
WRTN = "https://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/67a0ec8b5f86b8e4ad7b8385" # beijingdrivekang@gmail.com
# WRTN = "https://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/67162c57ad426ae86455fdf1" # rwkang321@gmail.com

IDEA_PROMPT = [
            "이제부터 너는 코믹 유튜브 영상 제작 전문 작가야. 매우 유머러스하고 해학적인 전문 작가야. ",
            "유튜브 채널에 대한 재미있고 터무니없고 완전히 허구적인 동영상 아이디어를 먼저 만들어 봐.",
            "이야기는 혼란스럽고 예측할 수 없으며, 세계 지도자, 유명 인사, 유명 인사가 미친 짓을 하거나 성격이 맞지 않는 일을 하는 내용으로 해.",
            "예를 들어, 트럼프가 엘론 머스크와 경쟁하거나 외계 인과 싸우는 테일러 스위프트, 외과의사 르브론 제임스와 같은 시나리오를 생각해 봐.",
            "아주 유머러스하고 코믹하면서도 흥미를 끌 수 있는, 가벼운 아이디어를 AI가 제작한 동영상에 완벽하게 적용할 수 있게 만들어 줘.",
            "영어를 사용하고, 내용을 2줄로 Title과 Content로 나누어서 만들어 줘.",
            ]
IDEA_STR = "\n".join(IDEA_PROMPT)
print(f"IDEA_STR: {IDEA_STR}, type(IDEA_STR): ", type(IDEA_STR), ", len(IDEA_STR): ", len(IDEA_STR))

# todo: 2025.02.27 Created. 심각하고 부드러운 비판 ===> 해결 방법 제안 ???
IDEA_PROMPT = [
    """
    미국 전 대통령 바이든, 현 대통령 트럼프, 러시아 대통령 푸틴, 프랑스 총리 바이루, 영국 총리 스타머,
    페이스북 주크버그, 테슬라 머스크, 오픈 AI 샘 올트만, 앤트로픽 다니엘라 아모데이, 
    이상 인물의 각각의 특징을 옷이나 패션 악세사리, 소지품 등을 살려, 
    누가 봐도 그 동물이 그 사람인 것을 알 수 있도록, 1:1 매칭이 되는 동물 이미지를 Image Generation AI에게 줄 프롬프트를 작성해 줘. 
    먼저 이 내용을 그대로 영어로 번역해 줘.
    
    Former U.S. President Biden, current President Trump, Russian President Putin, French Prime Minister Borne, 
    UK Prime Minister Starmer, Facebook's Zuckerberg, Tesla's Musk, OpenAI's Sam Altman, and Anthropic's Daniela Amodei:
    For each of these individuals, create an animal image that reflects their characteristics through clothing, 
    fashion accessories, and personal items, so that anyone can clearly identify 
    which animal represents which person in a 1:1 matching format. 
    Write prompts for Image Generation AI accordingly.
    
    Joe Biden (Former U.S. President)
    Prompt: "Create an image of a dignified tiger wearing a classic blue suit and a red tie, with a warm smile and a small American flag in its paw, symbolizing strength, leadership, and a friendly approach to governance."

    Donald Trump (Current President)
    Prompt: "Generate an image of a flamboyant peacock with bright orange and blue feathers, wearing a tailored suit and a red Make America Great Again hat, showcasing confidence and showmanship."

    Vladimir Putin (Russian President)
    Prompt: "Design an image of a strong bear dressed in a military uniform, complete with medals and a fur hat, exuding power and authority, representing a fierce leader."

    Élisabeth Borne (French Prime Minister)
    Prompt: "Illustrate a stylish fox wearing a chic blazer and holding a baguette under its arm, embodying sophistication and the essence of French culture."

    Keir Starmer (UK Prime Minister)
    Prompt: "Create an image of a dignified lion in a formal black suit and glasses, holding a briefcase, representing strength and seriousness in leadership."

    Mark Zuckerberg (Facebook CEO)
    Prompt: "Generate an image of a tech-savvy chameleon wearing a hoodie and holding a smartphone, symbolizing adaptability and innovation in the tech world."

    Elon Musk (Tesla CEO)
    Prompt: "Design an image of an adventurous eagle wearing futuristic sunglasses and a space suit, soaring through the sky, reflecting ambition and vision for the future."

    Sam Altman (OpenAI CEO)
    Prompt: "Create an image of an intelligent owl with glasses, surrounded by books and a laptop, representing knowledge and the pursuit of artificial intelligence."

    Daniela Amodei (Anthropic CEO)
    Prompt: "Illustrate a thoughtful dolphin wearing a lab coat and holding a clipboard, symbolizing intelligence, ethics, and the development of safe AI."

    """
]

IDEA_PROMPT = [
    """
    우크라이나 전쟁과 이스라엘 전쟁, 그리고 지구 온난화 현상에 대한 이슈에 있어,
    세계를 이끌고 있는 상기 9명의 지도자들이, 그동안 해 왔던 스텐스에 대하여, 
    매우 진지하고 심각하게 힐란하고 비판하는 내용의 이미지를 AI에게 만들게 할 것인데,
    이에 적합한 프롬프트를 각자의 개성을 살려 이미지를 생성할 프롬프트를 만들어 줘.
    위 내용을 이미지 생성 AI, ideogram AI에 맞는 프롬프트로 번역해 줘.
    
    Create a dramatic and intense digital artwork featuring nine world leaders standing in a semi-circle, 
    each with a distinct expression of seriousness and critique. 
    The scene is set against a chaotic backdrop: 
    a split sky with one side showing war-torn Ukraine with smoke and tanks, 
    another with Israel's conflict zones with rubble and fire, 
    and a third with melting glaciers and rising seas symbolizing global warming. 
    Each leader's attire and posture reflects their unique personality—e.g., 
    a bold American leader in a suit pointing accusingly, 
    a stoic Russian figure in military attire with a cold stare, 
    a contemplative Chinese leader in traditional robes holding a scroll, 
    a charismatic British leader with a sharp gesture, etc. 
    The mood is dark, critical, and urgent, with vivid colors and surreal details, 
    like cracked earth beneath their feet and stormy clouds above. 
    Highly detailed, cinematic lighting, 4K resolution."


    
    Joe Biden (Former U.S. President)
    Prompt: "Create an image of a dignified tiger wearing a classic blue suit and a red tie, with a warm smile and a small American flag in its paw, symbolizing strength, leadership, and a friendly approach to governance."
    먼저 위 내용을 그대로 영어로 번역해 줘.
    
    Regarding the issues of the Ukraine war and the Israel war, 
    create prompts for AI to generate images of the nine world leaders mentioned above, 
    seriously and critically reflecting on their stances and actions taken so far, 
    while highlighting each leader's unique characteristics.

    Joe Biden (Former U.S. President)
    Prompt: "Create an image of a dignified tiger wearing a classic blue suit and a red tie, with a serious expression and a small American flag in its paw, symbolizing strength, leadership, and a critical stance on global conflicts."
    Donald Trump (Current President)
    Prompt: "Generate an image of a bold peacock with bright orange and blue feathers, wearing a tailored suit and a stern expression, standing on a podium with a speech bubble that reads 'Make Peace Great Again,' reflecting a critical view on international affairs."
    Vladimir Putin (Russian President)
    Prompt: "Design an image of a fierce bear in a military uniform, looking contemplative with a serious gaze, surrounded by maps and flags, representing his complex stance on the Ukraine conflict."
    Élisabeth Borne (French Prime Minister)
    Prompt: "Illustrate a poised fox in a chic blazer, holding a newspaper with headlines about the wars, displaying a concerned expression, symbolizing France's critical perspective on global conflicts."
    Keir Starmer (UK Prime Minister)
    Prompt: "Create an image of a thoughtful lion in a formal black suit, examining international reports with a serious demeanor, representing the UK's critical stance on the ongoing wars."
    Mark Zuckerberg (Facebook CEO)
    Prompt: "Generate an image of a tech-savvy chameleon wearing a hoodie and glasses, looking at a digital map of the conflicts with concern, symbolizing the role of social media in shaping public opinion about the wars."
    Elon Musk (Tesla CEO)
    Prompt: "Design an image of an adventurous eagle wearing futuristic sunglasses, perched on a globe with a serious expression, reflecting on the impact of the wars on technology and innovation."
    Sam Altman (OpenAI CEO)
    Prompt: "Create an image of an intelligent owl wearing glasses, surrounded by data charts and reports, with a serious look, symbolizing the importance of ethical AI in conflict resolution."
    Daniela Amodei (Anthropic CEO)
    Prompt: "Illustrate a thoughtful dolphin in a lab coat, looking at a map of global conflicts with a concerned expression, representing the need for ethical considerations in AI development related to war."
    """
]

IDEA_STR = "\n".join(IDEA_PROMPT)
print(f"IDEA_STR: {IDEA_STR}, type(IDEA_STR): ", type(IDEA_STR), ", len(IDEA_STR): ", len(IDEA_STR))

# todo: 2025.02.01 Created. 랜덤 코믹 IDEA 5가지 요청 프롬프트 : 영상이 너무 빨라서 AI 생성으로는 부 적합.
# IDEA_KOR = "이제부터 너는 코믹 유튜브 영상 제작 전문 작가야. 매우 유머러스하고 해학적인 전문 작가야. 유튜브 채널에 대한 재미있고 터무니없고 완전히 허구적인 동영상 아이디어를 먼저 만들어 봐. 이야기는 혼란스럽고 예측할 수 없으며, 세계 지도자, 유명 인사, 유명 인사가 미친 짓을 하거나 성격이 맞지 않는 일을 하는 내용으로 해. 예를 들어, 트럼프가 엘론 머스크와 경쟁하거나 외계 인과 싸우는 테일러 스위프트, 외과의사 르브론 제임스와 같은 시나리오를 생각해 봐. 아주 유머러스하고 코믹하면서도 흥미를 끌 수 있는, 가벼운 아이디어를 AI가 제작한 동영상에 완벽하게 적용할 수 있게 만들어 줘. 영어를 사용하고, 내용을 2줄로 Title과 Content로 나누어서 만들어 줘."
IDEA_KOR = IDEA_STR

# 파파고 번역
IDEA_ENG = "From now on, you are a professional comic YouTube video producer. A very humorous and humorous professional writer. Make fun, ridiculous and completely fictional video ideas for YouTube channels first. The story is confusing and unpredictable, and it's about world leaders, celebrities, and celebrities doing crazy things or out of character. Consider, for example, scenarios like Taylor Swift, where Trump competes with Elon Musk or fights aliens, and LeBron James, a surgeon. Make it perfect for AI-generated videos with a very humorous, comical yet engaging idea. Please use English and make the content divided into Title and Content in 2 lines.  When the copy icon is clicked, make sure to have double asterisks on both Title and Content like this: **Title:**, **Content:**"
# wrtn 번역
IDEA_ENG = "From now on, you are a professional comic YouTube video producer. You are a very humorous and witty writer. Create fun, ridiculous, and completely fictional video ideas for a YouTube channel. The stories should be confusing and unpredictable, featuring world leaders and celebrities (excluding Korean figures) doing crazy things or acting out of character. Consider scenarios like Trump competing with Elon Musk or Taylor Swift fighting aliens, and LeBron James as a surgeon. Make it engaging and suitable for AI-generated videos with a light-hearted tone. Please use English and divide the content into Title and Content in two lines.  When the copy icon is clicked, make sure to have double asterisks on both Title and Content like this: **Title:**, **Content:**"

# todo: 2025.02.20 Edited. 주간 세계 이슈 5가지 요청 프롬프트
IDEA_KOR = """
이제부터 너는 코밀 유튜브 영상 전문가야. 매우 유머러스하고 해학적인 작가로 최고 전문가야. 
먼저 영상 아이디어를 만드는데, 지난 주에 정치, 경제, 사회, 문화, 체육, 환경, 전쟁 등, 
전 세계를 강타한 핵심 이슈 5개를 뽑아서, 매우 코믹하고 해학적이면서, 
약간은 anti 스럽고 고발적인 시각으로 작성해 줘. 
예를 들어, 트럼프, 푸틴, 시진핑, 엘론 머스크, 쥬크버그, 김정은 등 유명 인사 위주로 선정하여, 
매우 유머러스하고 코민하면서도 재미있고 흥미를 끌 수 있는 아이디어로 AI가 제작한 영상을 완벽하게 적용할 수 있계 작성해 줘. 
영어를 사용하고 그 내용을 2줄로 Title과 Content로 나누어 작성해 줘.
"""
# 위 내용은 유튜브 영상 제작을 위한 프롬프트인데, 일단 영어로 번역해 줘."
IDEA_ENG = """
From now on, you are a comic YouTube video expert. 
You are a very humorous and witty writer, the best in the field. 
First, create video ideas by selecting five key issues that have hit the world in the past week, 
such as politics, economics, society, culture, sports, environment, and war. 
Write them in a very comic and humorous way, with a slightly anti-establishment and critical perspective. 
For example, focus on famous figures like Trump, Putin, Xu Jinping, Elon Musk, Zuckerberg, and Kim Jong-un, 
and create ideas that are very humorous and entertaining while being engaging and interesting for AI-generated videos. 
Please use English and divide the content into Title and Content in two lines. 
When the copy icon is clicked, make sure to have double asterisks on both Title and Content like this: **Title:**, **Content:**
"""

# todo: 2025.02.01 Created. 위 프롬프트에 대한 5가지 답변에 대해서, 다시 5가지 Scenario 요청 프롬프트.
# SCENE_KOR = "위 내용에 대해 5개 scene으로 구성하여, 구체적인 상황극으로 전개 해 줘. 영어로 해 주고, 내용을 2줄로 Scene, Scenario 나누어서 만들어 주고, copy icon을 클릭하면, 반드시 Scene 과 Scenario 양쪽에 별표 2개가 붙어 있게 해 줘. 이런식으로 : **Scene:**, **Scenario:**"
SCENE_KOR = """
아래 내용을 번역해 줘. 미드저니 AI 또는 ideogram AI 툴을 이용하여, 실사 이미지를 생성할 것이니, prompt 형식으로 번역해 줘. 
아래: 위 내용에 대해 5개 scene으로 구성하여, 구체적인 상황극으로 전개 해 줘. 
영어로 해 주고, 이 Scenaroo를 가지고, 미드저니 또는 ideogram AI Tool을 활용한 실사 사진 이미지 생성 Prompt로 활용할 거야. 
내용을 2줄로 Scene, Scenario 나누어서 만들어 주고, copy icon을 클릭하면, 반드시 Scene 과 Scenario 양쪽에 별표 2개가 붙어 있게 해 줘. 
이런식으로 : **Scene:**, **Scenario:**
"""

# SCENE_ENG = "Create a detailed scenario for each of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into 'SceneTitle' and 'SceneContent' in two lines."
# SCENE_ENG = "Create a detailed scenario of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into Scene and Scenario in two lines."
# SCENE_ENG = " : Create a detailed scenario of the five video ideas above, consisting of five scenes that develop a specific situation. Please write in English and divide the content into 'Scene' and 'Scenario' in two lines. When the copy icon is clicked, make sure to have double asterisks on both Scene and Scenario like this: **Scene:**, **Scenario:**"
SCENE_ENG = """
: For the content above, create a detailed scenario consisting of 5 scenes that develop a specific situation. 
This will be used as a prompt for generating realistic images using Midjourney or Ideogram AI tools. 
Please write in English and divide the content into 'Scene' and 'Scenario' in two lines. 
Scene: This is where you write a title for your image, and
Scenario: This is where you write a contextual description for your image.
When the copy icon is clicked, 
make sure to have double asterisks on both Scene and Scenario like this: **Scene:**, **Scenario:**. 
In particular, in Scene, don't write numbers like **Scene 1:**, Make sure to mark it like **Scene:**.
"""

# 사진 생성. https://ideogram.ai/t/explore
IDEOGRAM = "https://ideogram.ai/t/explore"

# 프롬프트 공통 추가 : "사람의 손가락 부분은 가능하면 너무 노골적으로 크게 표현되지 않도록 했으면 한다"
IMAGE_PROMPT_SUFFIX = """
Please ensure that any depiction of human fingers is not overly pronounced or explicit.
"""

# 비디오 생성. hailuo.video/create
HAILUO = "https://hailuoai.video/create"

VIDEO_PROMPT_SUFFIX = """
Generate a video based on the attached image, 
showcasing an elegant and smooth animation with slow, never fast, movements. 
The scene features refined and graceful motions, with soft transitions, vibrant details, 
and cinematic lighting in 4K resolution.
"""
# VIDEO_PROMPT_SUFFIX = """
# Generate a video based on the attached image,
# showcasing an elegant and smooth animation with extremely slow, never fast, movements.
# The scene features refined and graceful motions, with soft transitions, vibrant details,
# and cinematic lighting in 4K resolution.
# """

# suno AI, 노래 생성 : 유료
SUNO = "https://suno.com/create?wid=default"

# riffusion AI, 노래 생성 : 무료
RIFFUSION = "https://www.riffusion.com/library/my-songs"
MUSIC_PROMPT_SUFFIX = """
Now, I’ve created a 3-minute comic and humorous video based on the five themes above. 
Now, I want to write lyrics suitable for music that fits the atmosphere of the video.
"""

# RIFFUSION_GHOSTWRITER = "comic, kpop" # kpop: 가사 중간에 "한글"이 들어 가네...
RIFFUSION_GHOSTWRITER = "comic"

DELAY1 = 1
DELAY2 = 2
DELAY3 = 3
DELAY5 = 5
DELAY9 = 9
DELAY10 = 10
DELAY15 = 15
DELAY20 = 20
DELAY25 = 25
DELAY30 = 30
DELAY60 = 60
DELAY120 = 120
DELAY180 = 180
DELAY240 = 240
DELAY300 = 300
DELAY360 = 360
DELAY420 = 420
DELAY480 = 480
DELAY540 = 540
DELAY600 = 600
DELAY1200 = 1200
DELAY1800 = 1800
DELAY3600 = 3600


"""
# 그냥은 안 되고, 여기서 반드시 글로벌 변수를 먼저 선언해야 되네.
path_bs = ''
str_year = ''
str_ym = ''
str_ymd = ''
file_bs = ''
ext_bs = ''

path_current = ''
now = ''
year_current = ''
month_current = ''
month_current = ''
day_current = ''
date_current = ''
date_format = ''

file_full_name = ''
path_base = ''
path = ''
path_year = ''
path_ym = ''
path_ymd = ''

# 2025.02.14 MySQL DB
HOST = ''


icon_edit_file = ''
icon_edit_pos_file = ''
icon_edit = ''
icon_edit_pos = ''

icon_hangul_file = ''
icon_hangul_pos_file = ''
icon_hangul = ''
icon_hangul_pos = ''

icon_english_file = ''
icon_english_pos_file = ''
icon_english = ''
icon_english_pos = ''

icon_copy_file = ''
icon_copy_pos_file = ''
icon_copy = ''
icon_copy_pos = ''

chrome_select_user_file = ''
chrome_select_user = ''
screen_to_find_chrome_user_file = ''
screen_to_find_chrome_user = ''

screen_to_find_edit_icon_file = ''
screen_to_find_edit_icon = ''

screen_to_find_copy_icon_file = ''
screen_to_find_copy_icon = ''

ideogram_cover_file = ''
ideogram_cover = ''
screen_to_find_ideogram_icon_file = ''
screen_to_find_ideogram_icon = ''

download_path_file = ''
download_path = ''
screen_to_find_download_path_file = ''
screen_to_find_download_path = ''

# download_path_file0 = ''
# download_path0 = ''
# screen_to_find_download_path_file0 = ''
# screen_to_find_download_path0 = ''
# download_path_file1 = ''
# download_path1 = ''
# screen_to_find_download_path_file1 = ''
# screen_to_find_download_path1 = ''

download_save_file = ''
download_save = ''
screen_to_find_download_save_file = ''
screen_to_find_download_save = ''

download_already_image_file = ''
download_already_image = ''
screen_to_find_download_already_image_file = ''
screen_to_find_download_already_image = ''

download_already_image_yes_file = ''
download_already_image_yes = ''
screen_to_find_download_already_image_yes_file = ''
screen_to_find_download_already_image_yes = ''

open_path_file = ''
open_path = ''
screen_to_find_open_path_file = ''
screen_to_find_open_path = ''

file_open_file = ''
file_open = ''
screen_to_find_file_open_file = ''
screen_to_find_file_open = ''

file_doesnt_exist_file = ''
file_doesnt_exist = ''
screen_to_find_file_doesnt_exist_file = ''
screen_to_find_file_doesnt_exist = ''

width = 0
height = 0
center_x = 0
center_y = 0

ideogram = '' # 사진 생성. https://ideogram.ai/t/explore
hailuo = '' # 비디오 생성. hailuo.video/create
wrtn = '' # wrtn AI 과제와 업무-Pro

delay1 = 0
delay2 = 0
delay3 = 0
delay5 = 0
delay9 = 0
delay10 = 0
delay15 = 0
delay20 = 0
delay25 = 0
delay30 = 0
delay60 = 0
delay120 = 0
delay180 = 0
delay240 = 0
delay300 = 0
delay360 = 0
delay420 = 0
delay480 = 0
delay540 = 0
delay600 = 0
delay1200 = 0
delay1800 = 0
delay3600 = 0
"""

'''
def set_globals():
    global path_bs, str_year, str_ym, str_ymd, file_bs, ext_bs
    global path_base, file_full_name, path, path_year, path_ym, path_ymd
    global path_current, now, year_current, month_current, month_current, day_current, date_current

    global company_code, host0, user0, pass0, dbname0, host1, user1, pass1, dbname1
    global msSqlServerDb, cursArrayServer, mySqlLocalDb, cursArray, cursDict
    global bounce_time, sleep_time, time_gap, night_closing_hhmmss, day_closing_hhmmss

    # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global COMPANY_CODE, HOST0, USER0, PASS0, DBNAME0, HOST1, USER1, PASS1, DBNAME1
    # global BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    # global FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE
    # global WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, TO_WAREHOUSE
    # global FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE
    # global mySqlLocalDb, cursArray, cursDict

    global icon_edit_file, icon_edit_pos_file, icon_edit, icon_edit_pos, screen_to_find_edit_icon_file, screen_to_find_edit_icon
    global icon_hangul_file, icon_hangul_pos_file, icon_hangul, icon_hangul_pos
    global icon_english_file, icon_english_pos_file, icon_english, icon_english_pos
    global icon_copy_file, icon_copy_pos_file, icon_copy, icon_copy_pos
    global screen_to_find_copy_icon_file, screen_to_find_copy_icon

    global chrome_select_user_file, chrome_select_user, screen_to_find_chrome_user_file, screen_to_find_chrome_user
    global ideogram_cover_file, ideogram_cover, screen_to_find_ideogram_icon_file, screen_to_find_ideogram_icon

    global download_path_file, download_path, screen_to_find_download_path_file, screen_to_find_download_path
    # global download_path_file0, download_path0, screen_to_find_download_path_file0, screen_to_find_download_path0
    # global download_path_file1, download_path1, screen_to_find_download_path_file1, screen_to_find_download_path1

    global download_already_image_file, download_already_image, screen_to_find_download_already_image_file, screen_to_find_download_already_image
    global download_already_image_yes_file, download_already_image_yes, screen_to_find_download_already_image_yes_file, screen_to_find_download_already_image_yes

    global download_save_file, download_save, screen_to_find_download_save_file, screen_to_find_download_save

    global file_open_file, file_open, screen_to_find_file_open_file, screen_to_find_file_open
    global open_path_file, open_path, screen_to_find_open_path_file, screen_to_find_open_path
    global file_doesnt_exist_file, file_doesnt_exist, screen_to_find_file_doesnt_exist_file, screen_to_find_file_doesnt_exist

    global width, height, center_x, center_y

    global wrtn, ideogram, hailuo

    global delay1, delay2, delay3, delay5, delay9
    global delay10, delay15, delay20, delay25, delay30, delay60
    global delay120, delay180, delay240, delay300, delay360, delay420, delay480, delay540, delay600
    global delay1200, delay1800, delay3600

    path_bs = 'G:\\Youtube\\DonGang\\MorningCafe\\'  # 'D:\\BspDev\\Dev\\'
    # path_bs = r'G:\Youtube\DonGang\' # r'G:~~' 이렇게 [r]을 먼저 써 주면, "\"가 1개만 있어야 된다.
    str_year = datetime.now().strftime('%Y')
    str_ym = datetime.now().strftime('%Y%m')
    str_ymd = datetime.now().strftime('%Y%m%d')
    file_bs = 'MorningCafe'
    ext_bs = '.xlsx'

    path_current = os.getcwd()  # "G:\Python\Workspace\PyAutoGui"
    # print(f"path_current: {path_current}, path_bs: {path_bs}")

    """
    2024.08.07 Conclusion.
    datetime.datetime.now()에서 에러가 발생하는 이유는 datetime 모듈을 가져오는 방식에 있습니다. 
    datetime 모듈을 import datetime로 가져오면 datetime 클래스에 접근하기 위해 datetime.datetime으로 호출해야 합니다. 
    하지만 from datetime import datetime와 같이 datetime 클래스를 직접 가져오면 datetime.now()로 호출할 수 있습니다.
    아래는 두 가지 방법을 보여주는 코드입니다:
    """

    date_format = "%Y.%m.%d"  # 날짜 형식 지정

    # now = datetime.datetime.now()
    now = datetime.now()
    year_current = str(now.year)
    month_current = str(now.month).zfill(2)  # 'str' 변환이 없으면 에러: 'int' object has no attribute 'zfill'
    month_current = '{0:02d}'.format(now.month)  # 'str'
    # 7월 생산 실적 등록...
    # month_current = '{0:02d}'.format(now.month - 1)  # 'str'
    day_current = '{0:02d}'.format(now.day)  # 'str'
    date_current = now.date()  # "2024-08-05" <class 'str'>
    # print(get_info(), f"year_current: {year_current}, month_current: {month_current}, day_current: {day_current}, date_current: {date_current}")
    # print(get_info(), f"year_current.type: {type(year_current)}, month_current.type: {type(month_current)}, day_current.type: {type(day_current)}, type(date_current): {type(date_current)}")

    file_full_name = file_bs + str_year + ext_bs

    path_base = os.path.join(path_bs, str_year, str_ym, str_ymd)
    path = os.path.join(path_base, file_full_name) # 'MorningCafe2025.xlsx' : 이게 의미가 있나?

    path_year = os.path.join(path_bs, str_year)
    path_ym = os.path.join(path_bs, str_year, str_ym)
    path_ymd = os.path.join(path_bs, path_year, str_ym, str_ymd)

    company_code = ""
    host0 = ""
    user0 = ""
    pass0 = ""
    dbname0 = ""
    host1 = ""
    user1 = ""
    pass1 = ""
    dbname1 = ""

    msSqlServerDb = "" # pymssql.connect(server=gv.host0, user=gv.user0, password=gv.pass0, database=gv.dbname0)
    cursArrayServer = "" # gv.msSqlServerDb.cursor()

    mySqlLocalDb = "" # pymysql.connect(host=gv.host1, port=3306, user=gv.user1, password=gv.pass1, db=gv.dbname1, charset='utf8')
    cursArray = "" # gv.mySqlLocalDb.cursor()
    cursDict = "" # gv.mySqlLocalDb.cursor(pymysql.cursors.DictCursor)

    bounce_time = 0
    sleep_time = 0
    time_gap = 0
    night_closing_hhmmss = ""
    day_closing_hhmmss  = ""

    # print(get_info(), "file_full_name: ", file_full_name)
    print(get_info(), "path_base: ", path_base)
    print(get_info(), "path: ", path)
    print(get_info(), "path_year: ", path_year)
    print(get_info(), "path_ym: ", path_ym)
    print(get_info(), "path_ymd: ", path_ymd)

    icon_edit_file = 'icon_edit.png'
    icon_edit_pos_file = 'icon_edit_pos.png'
    icon_edit = os.path.join(path_year, icon_edit_file)
    icon_edit_pos = os.path.join(path_year, icon_edit_pos_file)
    print(get_info(), "icon_edit: ", icon_edit)
    print(get_info(), "icon_edit_pos: ", icon_edit_pos)

    screen_to_find_edit_icon_file = 'screen_to_find_edit_icon_file.png'
    screen_to_find_edit_icon = os.path.join(path_year, screen_to_find_edit_icon_file)

    icon_hangul_file = 'icon_hangul.png'  # 770,500
    icon_hangul_pos_file = 'icon_hangul_pos.png'
    icon_hangul = os.path.join(path_year, icon_hangul_file)
    icon_hangul_pos = os.path.join(path_year, icon_hangul_pos_file)
    print(get_info(), "icon_hangul: ", icon_hangul)
    print(get_info(), "icon_hangul_pos: ", icon_hangul_pos)

    icon_english_file = 'icon_english.png'
    icon_english_pos_file = 'icon_english_pos.png'
    icon_english = os.path.join(path_year, icon_english_file)
    icon_english_pos = os.path.join(path_year, icon_english_pos_file)

    icon_copy_file = 'icon_copy.png'
    icon_copy_pos_file = 'icon_copy_pos.png'
    icon_copy = os.path.join(path_year, icon_copy_file)
    icon_copy_pos = os.path.join(path_year, icon_copy_pos_file)

    chrome_select_user_file = 'chrome_select_user.png'
    chrome_select_user = os.path.join(path_year, chrome_select_user_file)
    screen_to_find_chrome_user_file = 'screen_to_find_chrome_user.png'
    screen_to_find_chrome_user = os.path.join(path_year, screen_to_find_chrome_user_file)

    screen_to_find_copy_icon_file = 'screen_to_find_copy_icon.png'
    # icon_copy_pos_file = 'icon_english_pos.png'
    screen_to_find_copy_icon = os.path.join(path_year, screen_to_find_copy_icon_file)
    # icon_copy_pos = os.path.join(path_year, icon_copy_pos_file)

    ideogram_cover_file = 'ideogram_cover.png'
    ideogram_cover = os.path.join(path_year, ideogram_cover_file)
    screen_to_find_ideogram_icon_file = 'screen_to_find_ideogram_icon.png'
    screen_to_find_ideogram_icon = os.path.join(path_year, screen_to_find_ideogram_icon_file)

    download_path_file = 'download_path.png'
    download_path = os.path.join(path_year, download_path_file)
    screen_to_find_download_path_file = 'screen_to_find_download_path.png'
    screen_to_find_download_path = os.path.join(path_year, screen_to_find_download_path_file)

    # download_path_file0 = 'download_path0.png'
    # download_path0 = os.path.join(path_year, download_path_file0)
    # screen_to_find_download_path_file0 = 'screen_to_find_download_path0.png'
    # screen_to_find_download_path0 = os.path.join(path_year, screen_to_find_download_path_file0)
    # download_path_file1 = 'download_path1.png'
    # download_path1 = os.path.join(path_year, download_path_file1)
    # screen_to_find_download_path_file1 = 'screen_to_find_download_path1.png'
    # screen_to_find_download_path1 = os.path.join(path_year, screen_to_find_download_path_file1)

    download_save_file = 'download_save.png'
    download_save = os.path.join(path_year, download_save_file)
    screen_to_find_download_save_file = 'screen_to_find_download_save.png'
    screen_to_find_download_save = os.path.join(path_year, screen_to_find_download_save_file)

    download_already_image_file = 'download_already_image.png'
    download_already_image = os.path.join(path_year, download_already_image_file)
    screen_to_find_download_already_image_file = 'screen_to_find_download_image.png'
    screen_to_find_download_already_image = os.path.join(path_year, screen_to_find_download_already_image_file)

    download_already_image_yes_file = 'download_already_image_yes.png'
    download_already_image_yes = os.path.join(path_year, download_already_image_yes_file)
    screen_to_find_download_already_image_yes_file = 'screen_to_find_download_image_yes.png'
    screen_to_find_download_already_image_yes = os.path.join(path_year, screen_to_find_download_already_image_yes_file)

    open_path_file = 'open_path.png'
    open_path = os.path.join(path_year, open_path_file)
    screen_to_find_open_path_file = 'screen_to_find_open_path.png'
    screen_to_find_open_path = os.path.join(path_year, screen_to_find_open_path_file)

    file_open_file = 'file_open.png'
    file_open = os.path.join(path_year, file_open_file)
    screen_to_find_file_open_file = 'screen_to_find_file_open.png'
    screen_to_find_file_open = os.path.join(path_year, screen_to_find_file_open_file)

    file_doesnt_exist_file = 'file_doesnt_exist.png'
    file_doesnt_exist = os.path.join(path_year, file_doesnt_exist_file)
    screen_to_find_file_doesnt_exist_file = 'screen_to_find_file_doesnt_exist.png'
    screen_to_find_file_doesnt_exist = os.path.join(path_year, screen_to_find_file_doesnt_exist_file)

    width, height = pyautogui.size()
    center_x, center_y = width // 2, height // 2

    # 사진 생성. https://ideogram.ai/t/explore
    ideogram = "https://ideogram.ai/t/explore"

    # 비디오 생성. hailuo.video/create
    hailuo = "https://hailuoai.video/create"

    # wrtn AI 과제와 업무-Pro
    wrtn = "https://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/67a0ec8b5f86b8e4ad7b8385"
    # wrtn Pro모드
    # wrtn = "https://wrtn.ai/chat/u/663397a3208f03982f4f7dae/c/66a6aba08c86fb9e8153cdb4"
    # wrtn AI 이미지
    # wrtn = "https://wrtn.ai/chat/u/66309fe4fa99736573f691be/c/6786a4938470afebf6598b56"

    delay1 = 1
    delay2 = 2
    delay3 = 3
    delay5 = 5
    delay9 = 9
    delay10 = 10
    delay15 = 15
    delay20 = 20
    delay25 = 25
    delay30 = 30
    delay60 = 60
    delay120 = 120
    delay180 = 180
    delay240 = 240
    delay300 = 300
    delay360 = 360
    delay420 = 420
    delay480 = 480
    delay540 = 540
    delay600 = 600
    delay1200 = 1200
    delay1800 = 1800
    delay3600 = 3600
    
'''