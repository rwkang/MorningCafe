# 2025.02.14 Created. MySQL DB

import sys
import pymysql
import pymssql
import platform

from util import *
from configparser import ConfigParser

from gv import *

'''
import gv
# todo: 2025.02.14 Conclusion. 여기서는 절대 전역 변수 초기화를 시키면 안 되네.
gv.set_globals()
'''

def connectLocalDB():
    # # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1
    # global BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    # global FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE
    # global WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, TO_WAREHOUSE
    # global FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE
    # global MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL

    # print("\nf_common.connectDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
        TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getLocalDbParameter()
        # print("\nf_common.connectDB COMPANY_CODE : " + COMPANY_CODE + "\n")

        # todo: 2025.02.17 Edited. 아래 내용은 MorningCafe 에서는 불 필요.
        # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
        # PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = getFacParameter()

        # # print("\n__connectDB LINE_CODE : " + str(LINE_CODE) + "\n")
        # # print("\n__connectDB GROUPS : " + str(GROUPS) + "\n")
        # # print("\n__connectDB PROCESS : " + str(PROCESS) + "\n")
        # # print("\n__connectDB FACODE : " + str(FACODE) + "\n")
        # print("\n__connectDB TRADE : " + str(TRADE) + "\n")
        # print("\n__connectDB BAUDRATE : " + str(BAUDRATE) + "\n")
        # print("\n__connectDB SERIALPORT : " + str(SERIALPORT) + "\n")

        # 2019.07.12 Conclusion. 그러니까 여기서 설혹 모든 변수 값이 "None"로 받어질 수가 없다.
        # 왜냐하면, Pi 컴 세팅 프로그램인 "setpi.py" 프로그램으로 이미 변수 값을 정확하게 저장하였기 때문이다.

        # MySQL 접속
        # MYSQLLOCALDB = mysql.connector.connect(host=HOST1, user=USER1, password=PASS1, database=DBNAME1)
        MYSQLLOCALDB = pymysql.connect(host=HOST1, port=3306, user=USER1, password=PASS1, db=DBNAME1, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # MYSQLLOCALDB = pymysql.connect(host=HOST1, port=3306, user=USER1, password=PASS1, db=DBNAME1, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME1 : ' + str(DBNAME1))

        CURSARRAYLOCAL = MYSQLLOCALDB.cursor()
        CURSDICTLOCAL = MYSQLLOCALDB.cursor(pymysql.cursors.DictCursor)
        # CURSDICTLOCAL = MYSQLLOCALDB.cursor(dictionary=True)  # 이건 안 되네...
        # CURSDICTLOCAL = MYSQLLOCALDB.cursor(cursor_class=MySQLCursorDict)  # cursor = db.cursor(cursor_class=MySQLCursorDict)

        # print(get_info(), 'CURSARRAYLOCAL : ', CURSARRAYLOCAL)
        # print(get_info(), 'CURSDICTLOCAL : ', CURSDICTLOCAL)

        if MYSQLLOCALDB is None:
            print(get_info(), f"connectDB MYSQLLOCALDB {HOST1} {DBNAME1} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, -1, \
                   "N", "N", "N", "N", "N", \
                   "N", "N", "N", "N", "N"
                   # "N", "N", "N", "N", "N", \
                   # "N", "N", "N", "N", "N", "N", "N", "N", "N", \
                   # "N", "N", "N", "N", "N", "N", "N"
        else:
            MYSQLLOCALDB.ping(True)
            # print("MYSQLLOCALDB.ping(True)")
            print(get_info(), f"connectDB 내 컴퓨터 {HOST1} {DBNAME1} 접속 성공 !!!")
            # print("\n__connectDB SERIALPORT : " + str(SERIALPORT) + "\n")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, \
                   COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
                   BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
                   # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
                   # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
                   # FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT

    except:
        # print(get_info(), ', connectLocalDB... HOST1 : ', HOST1)
        # print(get_info(), ', connectLocalDB... USER1 : ', USER1)
        # print(get_info(), ', connectLocalDB... PASS1 : ', PASS1)
        # print(get_info(), ', connectLocalDB... DBNAME1 :', DBNAME1)
        print(get_info(), f".connectLocalDB, 내 컴퓨터 {HOST1} {DBNAME1} 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, -1, \
               "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", "N", "N", "N"


# 2022.03.28 Conclusion. 여기 connectWebDB()가 최초 MS SQL DB 와 연결되는 함수이다.
# 그런데, 오늘부로 MySql DB 로 전환되어 사용하게 됨에 따라, 기존에 __dbMrp() 파일에 연결된, connectDB()를 사용하기 위해,
# 위의 connectWebDB()를 MySql DB 와 연결되는, connectWebMyDb()로 바로 연결해 준다. 아래 원본은 삭제하지 않는다.
def connectWebDB():
    msSqlServerDb, cursArrayServer, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
    BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()


# 2022.03.28 Conclusion. 여기 connectWebDB()가 최초 MS SQL DB 와 연결되는 함수이다.
# 그런데, 오늘부로 MySql DB 로 전환되어 사용하게 됨에 따라, 기존에 __dbMrp() 파일에 연결된, connectDB()를 사용하기 위해,
# 위의 connectWebDB()를 MySql DB 와 연결되는, connectWebMyDb()로 바로 연결해 준다. 아래 원본은 삭제하지 않는다.
# def connectWebDB():
#     # print("\nf_common.connectWebDB...")
#     try:
#         # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
#         # HOST3, USER3, PASS3, DBNAME3 = getWebDbParameter()  # connectRemoteDB() 하고는 Return 값이 다른다.
#         COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33,\
#         BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getWebDbParameter()
#         # print("\nf_common.connectWebDB HOST3 : ", HOST3)
#         # print("f_common.connectWebDB USER3 : ", USER3)
#         # print("f_common.connectWebDB PASS3 : ", PASS3)
#         # print("f_common.connectWebDB DBNAME3 : ", DBNAME3, "\n")
#
#         # MSSQL 접속
#         # print("==========================================================================================")
#         # print("f_common.connectWebDB 웹 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...")
#         # print("==========================================================================================")
#         msSqlServerDb = pymssql.connect(server=HOST3, user=USER3, password=PASS3, database=DBNAME3)
#         # msSqlServerDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
#         # print('1 f_common.msSqlServerDb.msSqlServerDb : ', msSqlServerDb)
#         # cursArrayServer = msSqlServerDb.cursor(as_dict=True)
#         cursArrayServer = msSqlServerDb.cursor()
#         # cursDictServer = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
#         # print('2 f_common.connectWebDB.cursArrayServer : ', cursArrayServer)
#
#         # remoteDbConnection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...
#
#         if msSqlServerDb is None:
#             print("\nf_common.connectWebDB MYSQLLOCALDB is None")
#             # time.sleep(0.1)
#             # __init__()
#             return -1
#         else:
#             # msSqlServerDb.ping(True)
#             # print("msSqlServerDb.ping(True)")
#             print("\nf_common.connectWebDB 웹 컴퓨터 ERP 접속 성공 !!!")
#
#             # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
#             # cursArrayServer.close()
#             # msSqlServerDb.close()
#
#             return msSqlServerDb, cursArrayServer, HOST3, USER3, PASS3, DBNAME3, \
#                    BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
#
#     except:
#         print("f_common connectWebDB 웹 컴퓨터 ERP 접속 실패")
#         # time.sleep(0.1)
#         # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')
#
#         return -1, -1, "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectWebMyDB():
    # print("\nf_common.connectWebDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        # HOST3, USER3, PASS3, DBNAME3 = getWebDbParameter()  # connectRemoteDB() 하고는 Return 값이 다른다.
        COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getWebDbParameter()
        # print(get_info(), "connectWebWmsDB HOST3 : ", HOST3)
        # print(get_info(), "connectWebWmsDB USER3 : ", USER3)
        # print(get_info(), "connectWebWmsDB PASS3 : ", PASS3)
        # print(get_info(), "connectWebWmsDB DBNAME3 : ", DBNAME3)

        # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
        # PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = getFacParameter()
        # # # print("\connectWebDB LINE_CODE : " + str(LINE_CODE) + "\n")
        # # # print("\connectWebDB GROUPS : " + str(GROUPS) + "\n")
        # # # print("\connectWebDB PROCESS : " + str(PROCESS) + "\n")
        # # # print("\connectWebDB FACODE : " + str(FACODE) + "\n")
        # # print("\connectWebDB TRADE : " + str(TRADE) + "\n")
        # # print("\connectWebDB BAUDRATE : " + str(BAUDRATE) + "\n")

        # MYSQLWEBDB = mysql.connector.connect(host=HOST3, user=USER3, password=PASS3, database=DBNAME3)
        MYSQLWEBDB = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME3, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # MYSQLLOCALDB = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME3, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print(get_info(), 'connectWebWmsDB.MYSQLWEBDB : ', MYSQLWEBDB)

        CURSARRAYWEB = MYSQLWEBDB.cursor()
        CURSDICTWEB = MYSQLWEBDB.cursor(pymysql.cursors.DictCursor)
        # CURSDICTLOCAL = MYSQLLOCALDB.cursor(dictionary=True)  # 이건 안 되네...
        # print(get_info(), 'connectWebWmsDB.CURSARRAYWEB : ', CURSARRAYWEB)
        # print(get_info(), 'connectWebWmsDB.CURSDICTWEB : ', CURSDICTWEB)

        if MYSQLWEBDB is None:
            print(get_info(), f", connectWebMyDB {HOST3} {DBNAME3} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"
        else:
            MYSQLWEBDB.ping(True)
            # print(get_info(), "connectWebWmsMyDB.ping(True)")
            print(get_info(), f"connectWebMyDB 웹 컴퓨터 {HOST3} {DBNAME3} 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            # MYSQLWEBDB, CURSARRAYWEB, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            # BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            return MYSQLWEBDB, CURSARRAYWEB, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
                   BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
            # return MYSQLWEBDB, CURSARRAYWEB, CURSDICTWEB, \
            #        COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            #        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
            #        FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
            #        WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
            #        FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT

    except:
        print(get_info(), f"connectWebDB 웹 컴퓨터 {HOST3} ERP 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"



def getLocalDbParameter():
    # # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1
    # global BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS

    # print('__getLocalDbParameter 함수 내부')

    # QMessageBox.about(self, '__getLocalDbParameter', '__getLocalDbParameter')

    # print('getLocalDbParameter config : 함수 __open_config_file()로 들어 갑니다.')
    config = __open_config_file()
    # print('getLocalDbParameter config : ' + str(config))
    # time.sleep(5)

    # config = ConfigParser()
    # # print('1 __getLocalDbParameter 함수 내부')
    #
    # # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    # if getattr(sys, 'frozen', False):
    #     # pyinstaller로 패키징한 실행파일의 경우
    #     cur_path = os.path.dirname(sys.executable)
    #     # print('if cur_path : ' + str(cur_path))
    # elif __file__:
    #     # *.py 형태의 파일로 실행할 경우 로직
    #     cur_path = os.path.dirname(os.path.abspath(__file__))
    #     # print('elif cur_path : ' + str(cur_path))
    #
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # # print("__getLocalDbParameter currentDir : " + currentDir)
    # # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')
    #
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    config.options('LOCAL')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('getLocalDbParameter config : ' + str(config))
    if 'LOCAL' in config:
        COMPANY_CODE = config.get('LOCAL', 'COMPANY_CODE')  # COMPANY_CODE = "PSB001" # "KFTCBJ"
        HOST1 = config.get('LOCAL', 'host1')
        USER1 = config.get('LOCAL', 'user1')
        PASS1 = config.get('LOCAL', 'pass1')
        DBNAME1 = config.get('LOCAL', 'dbname1')
        BOUNCE_TIME = int(config.get('LOCAL', 'bounce_time'))
        SLEEP_TIME = int(config.get('LOCAL', 'sleep_time'))
        SLEEP_TIME = float(SLEEP_TIME / 1000)
        TIME_GAP = int(config.get('LOCAL', 'time_gap'))
        TIME_GAP = float(TIME_GAP / 1000)
        NIGHT_CLOSING_HHMMSS = config.get('LOCAL', 'night_closing_hhmmss')
        DAY_CLOSING_HHMMSS = config.get('LOCAL', 'day_closing_hhmmss')

        # print("호출 후 COMPANY_CODE : " + COMPANY_CODE)
        # print("호출 후 HOST1 : " + HOST1)
        # print("호출 후 USER1 : " + USER1)
        # print("호출 후 PASS1 : " + PASS1)
        # print("호출 후 DBNAME1 : " + DBNAME1)
        # print("호출 후 BOUNCE_TIME : " + str(BOUNCE_TIME))
        # print("호출 후 SLEEP_TIME : " + str(SLEEP_TIME))
        # print("호출 후 TIME_GAP : " + str(TIME_GAP))
        # print("호출 후 NIGHT_CLOSING_HHMMSS : " + str(NIGHT_CLOSING_HHMMSS))
        # print("호출 후 DAY_CLOSING_HHMMSS : " + str(DAY_CLOSING_HHMMSS))

        # IN_OK_PIN_DEFAULT = config.get('LOCAL', 'in_ok_pin_default')
        # IN_NG_PIN_DEFAULT = config.get('LOCAL', 'in_ng_pin_default')

        return COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
               TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    else:
        print(get_info(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

        return "N", "N", "N", "N", "N", "N", "N", 0, "N", "N"

# @pyqtSlot()
def getWebDbParameter():
    # # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1
    # global BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS

    # print('getLocalDbParameter config : 함수 __open_config_file()로 들어 갑니다.')
    config = __open_config_file()
    # print('getLocalDbParameter config : ' + str(config))
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    config.options('WEB')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print(get_info(), ', getLocalDbParameter config : ', config)
    # print(get_info(), ', getLocalDbParameter len(config) : ', len(config))
    if 'WEB' in config:
        COMPANY_CODE = config.get('WEB', 'COMPANY_CODE')  # COMPANY_CODE = "PSB001" # "KFTCBJ"
        HOST3 = config.get('WEB', 'host3')
        USER3 = config.get('WEB', 'user3')
        PASS3 = config.get('WEB', 'pass3')
        DBNAME3 = config.get('WEB', 'dbname3')
        DBNAME32 = config.get('WEB', 'dbname32')
        DBNAME33 = config.get('WEB', 'dbname33')
        BOUNCE_TIME = int(config.get('WEB', 'bounce_time'))
        SLEEP_TIME = int(config.get('WEB', 'sleep_time'))
        SLEEP_TIME = float(SLEEP_TIME / 1000)
        TIME_GAP = int(config.get('WEB', 'time_gap'))
        TIME_GAP = float(TIME_GAP / 1000)
        NIGHT_CLOSING_HHMMSS = config.get('WEB', 'night_closing_hhmmss')
        DAY_CLOSING_HHMMSS = config.get('WEB', 'day_closing_hhmmss')

        print(get_info(), "getWebDbParameter 호출 후 COMPANY_CODE : ", COMPANY_CODE)
        print(get_info(), "getWebDbParameter 호출 후 HOST3 : ", HOST3)
        # print(get_info(), ",,f_common_getWebDbParameter 호출 후 USER3 : ", USER3)
        # print(get_info(), ",,f_common_getWebDbParameter 호출 후 DBNAME3 : ", DBNAME3)
        # print(get_info(), "getWebDbParameter 호출 후 DBNAME32 : ", DBNAME32)
        # print(get_info(), "getWebDbParameter 호출 후 DBNAME33 : ", DBNAME33)
        # print(get_info(), "getWebDbParameter 호출 후 BOUNCE_TIME : " + str(BOUNCE_TIME))
        # print(get_info(), "getWebDbParameter 호출 후 SLEEP_TIME : " + str(SLEEP_TIME))
        # print(get_info(), "getWebDbParameter 호출 후 TIME_GAP : " + str(TIME_GAP))
        # print(get_info(), "getWebDbParameter 호출 후 NIGHT_CLOSING_HHMMSS : " + str(NIGHT_CLOSING_HHMMSS))
        # print(get_info(), "getWebDbParameter 호출 후 DAY_CLOSING_HHMMSS : " + str(DAY_CLOSING_HHMMSS))

        # IN_OK_PIN_DEFAULT = config.get('LOCAL', 'in_ok_pin_default')
        # IN_NG_PIN_DEFAULT = config.get('LOCAL', 'in_ng_pin_default')

        return COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33, BOUNCE_TIME, SLEEP_TIME, \
               TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    else:
        print(get_info(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

        return "N", "N", "N", "N", "N", "N", "N", 0, 0, 0, "N", "N"


# @pyqtSlot()  # 가져오기
def getFacParameter():
    # # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
    #     WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, TO_WAREHOUSE, FACODE, \
    #     PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE

    # print("__getFacParameter 내부 : ")
    # print("__getFacParameter LINE_CODE : ", LINE_CODE)
    # print("__getFacParameter GROUPS : ", GROUPS)
    # print("__getFacParameter PROCESS : ", PROCESS)
    # print("__getFacParameter FACODE : ", FACODE)
    # print("__getFacParameter CAVITY : ", CAVITY)
    # print("__getFacParameter PRODUCTSELECTION : ", PRODUCTSELECTION)
    # print("__getFacParameter PLCBIT : ", PLCBIT)
    # print("__getFacParameter FRONTJISNO : ", FRONTJISNO)
    # print("f_common TRADE : " + str(TRADE))
    # print("f_common UI : " + str(UI))

    # QMessageBox.about(self, '__getFacParameter', '__getFacParameter')
    # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global FORPRODUCINGORDERDATA, process, groups, DESCRIPTION_TEXT, line_code
    # global WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY
    # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수(__startWork())에 정의되야 한다.
    # global description, work_date_ymd_string

    # print("__getFacParameter 1 : ")

    config = __open_config_file()
    # print('getFacParameter config : ' + str(config))
    # time.sleep(5)

    # config = ConfigParser()
    # # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    # if getattr(sys, 'frozen', False):
    #     # print("1")
    #     # pyinstaller로 패키징한 실행파일의 경우
    #     cur_path = os.path.dirname(sys.executable)
    #     # print('if cur_path : ' + str(cur_path))
    # elif __file__:
    #     # print("2")
    #     # *.py 형태의 파일로 실행할 경우 로직
    #     cur_path = os.path.dirname(os.path.abspath(__file__))
    #     # print('elif cur_path : ' + str(cur_path))
    #
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # # print("__getLocalDbParameter currentDir : " + currentDir)
    # # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '../config.ini', encoding='utf-8')
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    # # config.read('/home/pi/dev/gathering/config.ini')  # INI 파일 읽기
    # # # ['config.ini']
    # # config.sections()  # 섹션 리스트 읽기
    # # # ['LOCAL']
    config.options('PRODUCT_ENV')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('getFacParameter config : ' + str(config))
    if 'PRODUCT_ENV' in config:
        FORPRODUCINGORDERDATA = config.get('PRODUCT_ENV', 'forproducingorderdata')
        PROCESS = config.get('PRODUCT_ENV', 'process')
        GROUPS = config.get('PRODUCT_ENV', 'groups')
        DESCRIPTION_TEXT = config.get('PRODUCT_ENV', 'description')
        LINE_CODE = config.get('PRODUCT_ENV', 'line_code')
        WORK_DATE = config.get('PRODUCT_ENV', 'work_date')
        DAY_NIGHT = config.get('PRODUCT_ENV', 'day_night')
        GOODS = config.get('PRODUCT_ENV', 'goods')
        CODE = config.get('PRODUCT_ENV', 'code')
        CAVITY = config.get('PRODUCT_ENV', 'cavity')
        TO_WAREHOUSE = config.get('PRODUCT_ENV', 'to_warehouse')
        FACODE = config.get('PRODUCT_ENV', 'facode')
        PRODUCTSELECTION = config.get('PRODUCT_ENV', 'productselection')
        PLCBIT = config.get('PRODUCT_ENV', 'plcbit')
        FRONTJISNO = config.get('PRODUCT_ENV', 'frontjisno')
        TRADE = config.get('PRODUCT_ENV', 'trade')
        UI = config.get('PRODUCT_ENV', 'ui')
        SERIALPORT = config.get('PRODUCT_ENV', 'serialport')
        BAUDRATE = config.get('PRODUCT_ENV', 'baudrate')
        GOODSRIGHT = config.get('PRODUCT_ENV', 'goodsright')
        CODERIGHT = config.get('PRODUCT_ENV', 'coderight')
        CAVITYRIGHT = config.get('PRODUCT_ENV', 'cavityright')
        # print('__getFacParameter PROCESS : ' + str(PROCESS))
        # print("__getFacParameter GROUPS : " + str(GROUPS))
        # print("__getFacParameter DESCRIPTION_TEXT : " + str(DESCRIPTION_TEXT))
        # print("__getFacParameter LINE_CODE : " + str(LINE_CODE))
        # print("__getFacParameter WORK_DATE : " + str(WORK_DATE))
        # print("__getFacParameter DAY_NIGHT : " + str(DAY_NIGHT))
        # print("__getFacParameter GOODS : " + str(GOODS))
        # print("__getFacParameter CODE : " + str(CODE))
        # print("__getFacParameter CAVITY : " + str(CAVITY))
        # print("__getFacParameter TO_WAREHOUSE : " + str(TO_WAREHOUSE))
        # print("__getFacParameter FACODE : " + str(FACODE))
        # print("__getFacParameter PRODUCTSELECTION : " + str(PRODUCTSELECTION))
        # print("__getFacParameter PLCBIT : " + str(PLCBIT))
        # print("__getFacParameter FRONTJISNO : " + str(FRONTJISNO))
        # print("__getFacParameter TRADE : " + str(TRADE))
        # print("__getFacParameter UI : " + str(UI))
        # print("__getFacParameter BAUDRATE : " + str(BAUDRATE))
        # print("__getFacParameter SERIALPORT : " + str(SERIALPORT))
        # print("__getFacParameter GOODSRIGHT : " + str(GOODSRIGHT))
        # print("__getFacParameter CODERIGHT : " + str(CODERIGHT))
        # print("__getFacParameter CAVITYRIGHT : " + str(CAVITYRIGHT))
        return FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
               WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
               PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT
    else:
        print(get_info(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

        return "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", 0, "N", "N", 0, "N", "N", \
               "N", "N", "N", "N", "N", 0, 0

def setFacParameter(PROCESS, GROUPS, DESCRIPTION, LINE_CODE, work_date_ymd_string,
                    DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE,
                    PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT):
    # print('\setFacParameter CAVITY : ', CAVITY)
    # print('setFacParameter CAVITYRIGHT : ', CAVITYRIGHT)
    print(get_info(), ', setFacParameter SERIALPORT : ', SERIALPORT)

    # config.set('PRODUCT_ENV', 'FORPRODUCINGORDERDATA', yn_producing_order_data)

    config = __open_config_file()
    # print('setFacParameter config : ' + str(config))
    # time.sleep(5)

    # config = ConfigParser()
    # # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    # if getattr(sys, 'frozen', False):
    #     # pyinstaller로 패키징한 실행파일의 경우
    #     cur_path = os.path.dirname(sys.executable)
    #     # print('if cur_path : ' + str(cur_path))
    # elif __file__:
    #     # *.py 형태의 파일로 실행할 경우 로직
    #     cur_path = os.path.dirname(os.path.abspath(__file__))
    #     # print('elif cur_path : ' + str(cur_path))
    #
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # # print("__getLocalDbParameter currentDir : " + currentDir)
    # # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '../config.ini', encoding='utf-8')
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    # # config.read('/home/pi/dev/gathering/config.ini')  # INI 파일 읽기
    # # # ['config.ini']
    # # config.sections()  # 섹션 리스트 읽기
    # # # ['LOCAL']
    config.options('PRODUCT_ENV')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('setFacParameter config : ' + str(config))
    if 'PRODUCT_ENV' in config:
        # QMessageBox.about(self, '__setDbParameter', 'PROCESS : ' + str(PROCESS))
        # print("\n\n\n\n")
        PROCESS, GROUPS, DESCRIPTION, LINE_CODE, work_date_ymd_string,
        DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE,
        PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT
        # print("__setFacParameter PROCESS : " + str(PROCESS))
        # print("__setFacParameter groups : " + str(GROUPS))
        # print("__setFacParameter description : " + str(DESCRIPTION))
        # print("__setFacParameter line_code : " + str(LINE_CODE))
        # print("__setFacParameter work_date_ymd_string : " + str(work_date_ymd_string))
        # print("__setFacParameter DAY_NIGHT : " + str(DAY_NIGHT))
        # print("__setFacParameter GOODS : " + str(GOODS))
        # print("__setFacParameter CODE : " + str(CODE))
        # print("__setFacParameter CAVITY : " + str(CAVITY))
        # print("__setFacParameter GOODSRIGHT : " + str(GOODSRIGHT))
        # print("__setFacParameter CODERIGHT : " + str(CODERIGHT))
        # print("__setFacParameter CAVITYRIGHT : " + str(CAVITYRIGHT))
        # print("__setFacParameter CAVITYRIGHT : " + str(CAVITYRIGHT))
        # print("__setFacParameter TO_WAREHOUSE : " + str(TO_WAREHOUSE))
        # print("__setFacParameter FACODE : " + str(FACODE))
        # print("__setFacParameter PRODUCTSELECTION : " + str(PRODUCTSELECTION))
        # print("__setFacParameter PLCBIT : " + str(PLCBIT))
        # print("__setFacParameter FRONTJISNO : " + str(FRONTJISNO))
        # print("__setFacParameter TRADE : " + str(TRADE))
        # print("__setFacParameter UI : " + str(UI))
        # print("__setFacParameter BAUDRATE : " + str(BAUDRATE))
        print(get_info(), ", __setFacParameter SERIALPORT : " + str(SERIALPORT))
        #
        # print("\n\n\n\n")
        config.set('PRODUCT_ENV', 'process', PROCESS)
        config.set('PRODUCT_ENV', 'groups', GROUPS)
        config.set('PRODUCT_ENV', 'description', DESCRIPTION)
        config.set('PRODUCT_ENV', 'line_code', LINE_CODE)
        config.set('PRODUCT_ENV', 'work_date', work_date_ymd_string)
        if DAY_NIGHT == '2' or DAY_NIGHT == '야' or DAY_NIGHT == '夜':
            DAY_NIGHT = '2'
        else:
            DAY_NIGHT = '1'
        config.set('PRODUCT_ENV', 'day_night', DAY_NIGHT)
        config.set('PRODUCT_ENV', 'goods', GOODS)
        config.set('PRODUCT_ENV', 'code', CODE)
        config.set('PRODUCT_ENV', 'cavity', CAVITY)
        config.set('PRODUCT_ENV', 'to_warehouse', TO_WAREHOUSE)
        config.set('PRODUCT_ENV', 'facode', FACODE)
        config.set('PRODUCT_ENV', 'productselection', PRODUCTSELECTION)
        config.set('PRODUCT_ENV', 'plcbit', PLCBIT)
        config.set('PRODUCT_ENV', 'frontjisno', FRONTJISNO)
        config.set('PRODUCT_ENV', 'trade', TRADE)
        config.set('PRODUCT_ENV', 'ui', UI)
        config.set('PRODUCT_ENV', 'serialport', SERIALPORT)
        config.set('PRODUCT_ENV', 'baudrate', BAUDRATE)
        config.set('PRODUCT_ENV', 'goodsright', GOODSRIGHT)
        config.set('PRODUCT_ENV', 'coderight', CODERIGHT)
        config.set('PRODUCT_ENV', 'cavityright', CAVITYRIGHT)

        # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')
        # config_file = open('/home/pi/dev/gathering/config.ini', 'w')
        # config_file = open('config.ini', 'w')

        is_write = __save_config_file(config)
        # print("setFacParameter is_write : ", is_write)
        return is_write

        # currentDir = os.path.dirname(os.path.realpath(__file__))
        # config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
        # config.write(config_file)
        # config_file.close()
        # print("setFacParameter config_file : ", config_file)
        # return 1


def __open_config_file():
    # print('f_common.py.__open_config_file() config : ')
    config = ConfigParser()
    # print('f_common.py.__open_config_file() 함수 내부')

    # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    if getattr(sys, 'frozen', False):
        # pyinstaller로 패키징한 실행 파일의 경우
        cur_path = os.path.dirname(sys.executable)
        # print('f_common.py.__open_config_file() if cur_path : ' + str(cur_path))
    elif __file__:
        # *.py 형태의 파일로 실행할 경우 로직
        cur_path = os.path.dirname(os.path.abspath(__file__))
        # print('f_common.py.__open_config_file() elif cur_path : ' + str(cur_path))

    # 2021.01.25 Conclusion. os가 윈도우일 경우에는, 즉 일반 PC 사용자일 경우에는,
    # [config.ini] 파일을 [C:\Windows\SysWOW64\config] 루트 드라이브 및 윈도우 폴더를 활용한다.
    # print('f_common.py.__open_config_file() 함수 내부 type(platform.system()):', type(platform.system()))
    # print('f_common.py.__open_config_file() 함수 내부 platform.system():', platform.system())
    if platform.system() == 'Windows':
        projectDir = os.path.dirname(os.path.realpath(__file__))[2:]  # \ps\ppp : [C:\] 드라이브는 뺀다.
        # print("f_common.py.__open_config_file()  projectDir : " + projectDir)
        currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang" + projectDir
        print(get_info(), " 합 currentDir : " + currentDir)

        # 2021.12.30 Added. .exe 파일로 컴파일 할 경우,
        # 폴더가 이상하게도
        # "C:\Windows\SysWOW64\config\\rwkang\Users\ADMINI~1\AppData\Local\Temp\_MEI306602"로 세팅되네...
        if currentDir.find("Users"):
            currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang\\Python\\Workspace\\app5"

        currentDir = currentDir.replace("\\", '/')

        # todo: 2025.02.17 Edited. MorningCafe/2025 사용.
        currentDir = PATH_YEAR
        print(get_info(), " 합 currentDir : " + currentDir)

        # path = "./python/test"
        if not os.path.isdir(currentDir):
            # print("f_common.py.__open_config_file() 이쪽으로 들어 왔나?")
            try:
                # 2021.01.25 Conclusion. 아래 명령으로 폴더는 못 만드네... 그냥 수동으로 반드시 만들고 진행한다.
                # os.mkdirs(currentDir, exist_ok=True)
                # kkk = os.mkdirs(currentDir)
                print(get_info(), " 설정 폴더가 없습니다. "
                                     "관리자에게 문의하시오! currentDir: ", currentDir)
                # time.sleep(5)
                return
            except Exception as e:
                # except EnvironmentError.errno:
                print(get_info(), " 만들었나? Exception.e : " + e)
                # print("f_common.py.__open_config_file()만들었나? EnvironmentError.errno : " + EnvironmentError.errno)
                # print("f_common.py.__open_config_file()만들었나? EnvironmentError.strerror : " + EnvironmentError.strerror)
        else:
            print(get_info(), "f_common.py.__open_config_file() 이미 파일이 있습니다. currentDir : " + currentDir)
            pass
    else:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        print(get_info(), "f_common.py.__open_config_file() 여기 os는 ? ", platform.system())  # : Raspberry PI.라즈베리파이컴은, 현재 디렉토리로 바로 온다...
        # print("f_common.py.__open_config_file() 여기 os는 ? currentDir : " + currentDir)

    # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')
    # todo: 2025.02.17 Edited. MorningCafe/2025 사용.
    config.read(filenames=PATH_YEAR + '/config.ini', encoding='utf-8')

    # ['config.ini']
    config.sections()  # 섹션 리스트 읽기
    # ['LOCAL']
    config.options('LOCAL')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print(get_info(), '.__open_config_file() config : ', config)
    # print(get_info(), '.__open_config_file() type(config) : ', type(config))
    # if 'LOCAL' in config:
    #     # print(get_info(), " config.options() : ")
    #     # print("f_common.py.__open_config_file() config.options() : ", config.options())
    #     FORPRODUCINGORDERDATA = config.get('PRODUCT_ENV', 'forproducingorderdata')
    #     PROCESS = config.get('PRODUCT_ENV', 'process')
    #     GROUPS = config.get('PRODUCT_ENV', 'groups')
    #     DESCRIPTION_TEXT = config.get('PRODUCT_ENV', 'description')
    #     LINE_CODE = config.get('PRODUCT_ENV', 'line_code')
    #     WORK_DATE = config.get('PRODUCT_ENV', 'work_date')
    #     DAY_NIGHT = config.get('PRODUCT_ENV', 'day_night')
    #     GOODS = config.get('PRODUCT_ENV', 'goods')
    #     CODE = config.get('PRODUCT_ENV', 'code')
    #     CAVITY = config.get('PRODUCT_ENV', 'cavity')
    #     TO_WAREHOUSE = config.get('PRODUCT_ENV', 'to_warehouse')
    #     FACODE = config.get('PRODUCT_ENV', 'facode')
    #     PRODUCTSELECTION = config.get('PRODUCT_ENV', 'productselection')
    #     PLCBIT = config.get('PRODUCT_ENV', 'plcbit')
    #     FRONTJISNO = config.get('PRODUCT_ENV', 'frontjisno')
    #     TRADE = config.get('PRODUCT_ENV', 'trade')
    #     UI = config.get('PRODUCT_ENV', 'ui')
    #     GOODSRIGHT = config.get('PRODUCT_ENV', 'goodsright')
    #     CODERIGHT = config.get('PRODUCT_ENV', 'coderight')
    #     CAVITYRIGHT = config.get('PRODUCT_ENV', 'cavityright')
    #     HOST1 = config.get('LOCAL', 'host1')
    # print(get_info(), ' HOST1 : ', HOST1)
    # else:
    #     print("f_common.py.__open_config_file() config.options() : ???")

    print(get_info(), "리턴 currentDir : " + currentDir)
    # print(get_info(), "리턴 config : " + config)
    # print(get_info(), "리턴 config : " + config)

    return config


def __save_config_file(config):
    # print(get_info(), ".__save_config_file(): config", config)

    # 2021.01.25 Conclusion. os가 윈도우일 경우에는, 즉 일반 PC 사용자일 경우에는,
    # [config.ini] 파일을 [C:\Windows\SysWOW64\config] 루트 드라이브 및 윈도우 폴더를 활용한다.
    # print('f_common.py.__save_config_file() 함수 내부 type(platform.system()):', type(platform.system()))
    # print('f_common.py.__save_config_file() 함수 내부 platform.system():', platform.system())
    if sys.platform.system() == 'Windows':
        projectDir = os.path.dirname(os.path.realpath(__file__))[2:]  # \ps\ppp : [C:\] 드라이브는 뺀다.
        # print(get_info(), ".setPlcDataLog() __getLocalDbParameter projectDir : " + projectDir)
        currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang" + projectDir
        # print(get_info(), ".setPlcDataLog() 합 __getLocalDbParameter currentDir : " + currentDir)

        # 2021.12.30 Added. .exe 파일로 컴파일 할 경우,
        # 폴더가 이상하게도 "C:\Windows\SysWOW64\config\\rwkang\Users\ADMINI~1\AppData\Local\Temp\_MEI306602"로 세팅되네...
        if currentDir.find("Users"):
            currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang\\Python\\Workspace\\app5"

        currentDir = currentDir.replace("\\", '/')
        # print("f_common.py.__save_config_file() 합 변환 currentDir : " + currentDir)
    else:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        # print("f_common.py.__save_config_file() 여기 os는 ? ", platform.system()) : Raspberry PI.라즈베리파이컴은, 현재 디렉토리로 바로 온다...
        print(get_info(), ".__save_config_file() 여기 os는 ? currentDir : " + currentDir)

    config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    # print(get_info(), ".__save_config_file() config_file : ", config_file)
    config.write(config_file)
    # print(get_info(), ".__save_config_file() config_file : ", config_file)
    config_file.close()
    return 1

    # config = __open_config_file()
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    # config.write(config_file)
    # config_file.close()
    # return 1


# 2025.02.14 Added. G:/Youtube/DonGang/MorningCafe/2025/config.ini/MySql/PowErpPsc
def creating_morning_cafe_idea(MYSQLLOCALDB, CURSARRAYLOCAL):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS morning_cafe_idea (" \
          "ID bigint(20) unsigned Not Null Auto_Increment," \
          "CODE_IDEA varchar(20) Not Null PRIMARY KEY," \
          "TITLE varchar(500)," \
          "CONTENT text," \
          "USER_ID varchar(100)," \
          "MODIFIED_DATE datetime Not Null Default Current_TimeStamp," \
          "CREATED_DATE datetime Not Null Default Current_TimeStamp " \
          ")"
    CURSARRAYLOCAL.execute(sql)
    try:
        MYSQLLOCALDB.commit()
        print(get_info(), "1 : Local 제품 테이블(morning_cafe_idea) 생성 완료! ")
        # sleep(1)  # 10분 = 600
        tf = True
    except:
        MYSQLLOCALDB.rollback()
        print(get_info(), "2 : Local 제품 테이블(morning_cafe_idea) 생성 실패! ")
        # sleep(1)  # 10분 = 600
        sys.exit()
        tf = False
    return sql, tf

# 2025.02.14 Added. G:/Youtube/DonGang/MorningCafe/2025/config.ini/MySql/PowErpPsc
def creating_morning_cafe_scene(MYSQLLOCALDB, CURSARRAYLOCAL):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS morning_cafe_scene (" \
          "ID bigint(20) unsigned Not Null Auto_Increment," \
          "DIRECTORY varchar(500)," \
          "CODE_IDEA varchar(20) Not Null," \
          "TITLE varchar(500)," \
          "CONTENT text," \
          "CODE_SCENE varchar(20) Not Null PRIMARY KEY," \
          "SCENE text," \
          "SCENARIO text," \
          "IMAGE_NAME varchar(500)," \
          "VIDEO_NAME varchar(500)," \
          "MUSIC_NAME varchar(500)," \
          "USER_ID varchar(100)," \
          "MODIFIED_DATE datetime Not Null Default Current_TimeStamp," \
          "CREATED_DATE datetime Not Null Default Current_TimeStamp " \
          ")"
    CURSARRAYLOCAL.execute(sql)
    try:
        MYSQLLOCALDB.commit()
        print(get_info(), "1 : Local 제품 테이블(morning_cafe_snene) 생성 완료! ")
        # sleep(1)  # 10분 = 600
        tf = True
    except:
        MYSQLLOCALDB.rollback()
        print(get_info(), "2 : Local 제품 테이블(morning_cafe_snene) 생성 실패! ")
        # sleep(1)  # 10분 = 600
        sys.exit()
        tf = False
    return sql, tf


# 2025.02.20 Added. 테이블 수정
def __alterTable(CONNECTEDLOCAL, MYSQLLOCALDB, CURSARRAYLOCAL, sql):
    try:
        # todo: 2025.02.20 Conclusion. with connection.cursor() as cursor:
        # 컨텍스트 매니저 사용: with 구문은 Python의 컨텍스트 매니저를 사용하여 블록 내에서 특정 리소스를 안전하게 관리합니다.
        # 자동 자원 관리: with 블록이 끝나면 cursor가 자동으로 닫히고, 리소스가 해제됩니다. 이는 코드의 가독성을 높이고, 리소스 누수를 방지하는 데 도움이 됩니다.
        # 예외 처리: with 블록 내에서 예외가 발생하더라도, 커서는 안전하게 닫히므로 안정적인 코드 실행이 보장됩니다.
        with CURSARRAYLOCAL: # MYSQLLOCALDB.cursor() as cursor: ===> CURSARRAYLOCAL = MYSQLLOCALDB.cursor()
            CURSARRAYLOCAL.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except pymysql.MySQLError as e:  # DB 연결을 한 번 더 시도...
        print(get_info(), "MySQL Error: ", str(e))
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
                BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")
        try:
            with CURSARRAYLOCAL:  # MYSQLLOCALDB.cursor() as cursor: ===> CURSARRAYLOCAL = MYSQLLOCALDB.cursor()
                CURSARRAYLOCAL.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        except pymysql.MySQLError as e:
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            print(get_info(), "Error: ", str(e))
        else:
            print(get_info(), "Successfully Modified: ", sql)

    # finally: # todo: 여기서 커서 close() 해 버리면, 아래에서 커서를 사용할 수 없는 에러가 난다.
    #     MYSQLLOCALDB.close()

    try:
        with CURSARRAYLOCAL:  # MYSQLLOCALDB.cursor() as cursor: ===> CURSARRAYLOCAL = MYSQLLOCALDB.cursor()
            CURSARRAYLOCAL.execute(sql)
        MYSQLLOCALDB.commit()
        print(get_info(), "1 : Local 제품 테이블(morning_cafe_idea) 수정 성공! ")
        # sleep(1)  # 10분 = 600
        rs_alter_table = True
    except pymysql.MySQLError as e:
        MYSQLLOCALDB.rollback()
        print(get_info(), "MySQL Error: ", str(e))
        print(get_info(), "2 : Local 제품 테이블(morning_cafe_idea) 수정 실패! ")
        # sleep(1)  # 10분 = 600
        # sys.exit()
        rs_alter_table = False

    finally:
        print(get_info(), "MYSQLLOCALDB 커서를 닫습니다!!!")
        MYSQLLOCALDB.close()

    return rs_alter_table

"""
def creating_gathering_goods(MYSQLLOCALDB, CURSARRAYLOCAL):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS gathering_goods (" \
          "Id bigint(20) unsigned Not Null Auto_Increment PRIMARY KEY ," \
          "code varchar(100) unique," \
          "code_no varchar(100)," \
          "part_no varchar(100)," \
          "marking_no varchar(100)," \
          "goods varchar(255)," \
          "process varchar(255)," \
          "step1 varchar(255)," \
          "step2 varchar(255)," \
          "step3 varchar(255)," \
          "step4 varchar(255)," \
          "step9 varchar(255)," \
          "goods0 int," \
          "goods1 int," \
          "goods2 int," \
          "goods3 int," \
          "description int Not Null," \
          "goods_assets int Not Null," \
          "unit bigint(20)," \
          "box_qty bigint(20)," \
          "trade bigint(20)," \
          "trade_name varchar(255)," \
          "user_id varchar(100)," \
          "modified_date datetime Not Null Default Current_TimeStamp " \
          ")"
    CURSARRAYLOCAL.execute(sql)
    try:
        MYSQLLOCALDB.commit()
        print(get_info(), "1 : Local 제품 테이블(gathering_goods) 생성 완료! ")
        # sleep(1)  # 10분 = 600
        tf = True
    except:
        MYSQLLOCALDB.rollback()
        print(get_info(), "2 : Local 제품 테이블(gathering_goods) 생성 실패! ")
        # sleep(1)  # 10분 = 600
        sys.exit()
        tf = False
    return sql, tf
"""
