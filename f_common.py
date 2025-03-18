# 2022.03.15 MS SQL 참고 자료
# https://ellieya.tistory.com/12
# https://blog9.tistory.com/39

import qrcode
# import serial
import sys
import os
import platform
import binascii
# # import xlrd, xlwt

# import mysql.connector  # 2022.03.18 Added. pymysql 보다 좋은가 본데...

# from tkinter import *  # import re 를 대신한다.
import re

# from tkinter import messagebox
from configparser import ConfigParser
# from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox,
#                              QMainWindow, QPushButton, QHBoxLayout,
#                              QVBoxLayout, QLabel, QLineEdit, QTextEdit,
#                              QListView)
# from PyQt5.QtCore import (pyqtSlot, pyqtSignal, QObject, QEventLoop, Qt, QDate, QTime, QPoint)
# from PyQt5.QtCore import (QRunnable, QThread, QThreadPool, pyqtSignal)
# from PyQt5.QtWidgets import *
# from PyQt5 import QtGui, QtCore
# from PyQt5.QtGui import QStandardItem, QStandardItemModel
# from datetime import datetime, timedelta, time, date
# from time import sleep, time, mktime, strptime, strftime
# # -*- coding: utf-8 -*-
# # import MySQLdb  # 대소문자 구분 한다...
import pymysql
# import pymssql
# import pyodbc
# import RPi.GPIO as GPIO
import datetime
import time
# import binascii

import inspect
from inspect import currentframe, getframeinfo

# frameinfo = getframeinfo(currentframe())
# print("frameinfo.filename: ", frameinfo.filename, ", frameinfo.lineno: ", frameinfo.lineno)
# print(os.path.basename(frameinfo.filename), frameinfo.lineno, ", value: xxx")  # , value)

# 2024.07.28 Added. 현재 프로그램 파일의 현재 라인 번호.
def get_info():
    stack = inspect.stack()
    frame = stack[1]
    filename = frame.filename
    lineno = frame.lineno
    return filename, lineno


# 2022.02.22 Added. 현재 프로그램 파일의 현재 라인 번호.
def get_line_no_old():
    cf = currentframe()  #.f_back
    file_name, line_no, function_name, lines, index = getframeinfo(cf)
    file_name = file_name.split("\\")[-1]
    # return file_name, line_no, function_name, lines, index
    return cf.f_back.f_lineno, file_name
    # return cf.f_back.f_filename, cf.f_back.f_lineno
    # return cf.f_back.f_lineno

# 2022.02.22 Added. 현재 프로그램 파일의 현재 라인 번호.
def get_line_no():
    cf = currentframe()  #.f_back
    file_name, line_no, function_name, lines, index = getframeinfo(cf)
    file_name = file_name.split("\\")[-1]
    # print(get_line_no(), "file_name: ", file_name)
    # print(get_line_no(), ", cf: ", cf)
    # print(get_line_no(), ", cf.f_back: ", cf.f_back)
    # return file_name, line_no, function_name, lines, index
    # return cf.f_back.f_lineno, file_name
    # return cf.f_back.f_lineno, file_name, cf, cf.f_back, cf.f_code
    # type_f_back = type(cf.f_back.f_back)

    # 2023.01.13 Conslusion. 정말 기가 막힌 파이썬이네. 여기 "cf.f_back" 의미는 "cf=currentframe()" 이므로,
    # 현재 프레임, 즉 "f_common.py"을 뜻하는 것이고,
    # "cf.f_back" 의미는, 현재 프레임 바로 앞 프레임, 즉 여기를 호출한 프레임을 의미하므로,
    # 만약 settings.py 에서 호출했으면, cf.f_back = settings.py 이고,
    # 만약 views.py 에서 호출했다면, cf.f_back = views.py 인 것이다.
    # 그러므로, "cf.f_back.f_back..." 이런식으로 계속 "f_back"을 찾을 수 있는 것이다.
    # 그러므로 "getframeinfo()" 펑션의 리턴 값이, Traceback(filename, lineno, frame.f_code.co_name, lines, index)
    # "Traceback(...)" 인 것이다.
    file_name_back, line_no_back, function_name_back, lines_back, index_back = getframeinfo(cf.f_back)
    file_name_back = file_name_back.split("\\")[-1]

    # file_name: 현재 프레임(파일), file_name_back: 호출한 프레임(파일)
    # return cf.f_back.f_lineno, file_name, file_name_back
    return cf.f_back.f_lineno, file_name_back

    # return cf.f_back.f_filename, cf.f_back.f_lineno
    # return cf.f_back.f_lineno

# 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
# 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
# CURRENT_FILE = sys._getframe().f_code.co_filename
# currentMethod = ""

remoteDbConnection = 0
localDbConnection = 0


# print("\nf_common 1 started.")

# 2020.12.09 Added. 품목 마스터 정보 등 기본 정보를 파이컴으로 업데이트 할지 여부 판단 루틴...
# msSqlServerDb, cursArrayServer = self.connectRemoteDB()
# cursArrayServer.execute(sql, values)  # 2019.08.25 Conclusion. 여기 리턴 값 [results]는 전혀 의미 없음.


# 2020.04.19 Added. 천신만고 끝에 찾아낸, [QThread] 클래스를 상속받는 GatheringReadPlc() 클래스에,
#   [인자.Parameter]를 전달하는 방식을 찾았다. 여기서 새로운 클래스 SendMsg()를 만들고,
#   SendMsg() 클래스 내부에 전달하고자 하는 [변수 값]들을 세팅하고,
#   GatheringReadPlc() 클래스를 생성할 때, 다중 클래스 상속으로 처리하면 된다.
#   GatheringReadPlc(QThread) ===> GatheringReadPlc(QThread, SendMsg) : 요래 처리하면 된다.
# updateGoodsMaster = 1
# updateEquipmentOfProduct = 2
# updateGroups = 3


class SendMsg():
    param1 = "1"
    param2 = 1
    # updateGoodsMaster = updateGoodsMaster
    # updateEquipmentOfProduct = updateEquipmentOfProduct
    # updateGroups = updateGroups


# @pyqtSlot()
def test():
    aaa = 2
    # print("f_common test() aaa : ", aaa)
    return 1


print(get_line_no(), " :: started...")


# # @pyqtSlot()
# def connectServerBaseMsDB():
#     # 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
#     # 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
#     # currentMethod = sys._getframe().f_code.co_name  # = "__init__"
#     # print(CURRENT_FILE, currentMethod, ":: started...")
#
#     # print("\nf_common.connectRemoteWmsDB...")
#     try:
#         # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
#         HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerMsDbParameter()
#         # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
#         # print("\nf_common.connectRemoteWmsDB HOST0 : ", HOST0)
#         # print("f_common.connectRemoteWmsDB USER0 : ", USER0)
#         # print("f_common.connectRemoteWmsDB PASS0 : ", PASS0)
#         print(get_line_no(), "connectServerBaseDB DBNAME0 : ", DBNAME0)
#
#         DBNAME0 = 'POWERERP'
#
#         # MSSQL 접속
#         msSqlServerBaseDb = pymssql.connect(server=HOST0, user=USER0, password=PASS0, database=DBNAME0)
#         # msSqlServerWmsDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
#         # print('1 f_common.connectRemoteWmsDB.msSqlServerDb : ', msSqlServerWmsDb)
#         cursArrayServer = msSqlServerBaseDb.cursor()
#         # cursArrayServerWms = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
#         # print('2 f_common.connectRemoteWmsDB.cursArrayServerAms : ', cursArrayServerWms)
#         # print('f_common.connectRemoteWmsDB.cursDictLocal : ' + str(cursDictLocal))
#
#         # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...
#
#         if msSqlServerBaseDb is None:
#             # print("\nf_common.connectRemoteBaseDB msSqlServerBaseDb is None")
#             # time.sleep(0.1)
#             # __init__()
#             return -1, -1, "N", "N", "N", "N", "N"
#
#         else:
#             # msSqlServerBaseDb.ping(True)
#             # print("msSqlServerBaseDb.ping(True)")
#             print(get_line_no(), "connectServerBaseDB 서버 컴퓨터 POWERERP 접속 성공 !!!")
#
#             # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
#
#             return msSqlServerBaseDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION
#
#     except:
#         print(get_line_no(), "connectServerBaseDB 서버 컴퓨터 POWERERP 접속 실패")
#         # time.sleep(0.1)
#         # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')
#
#         return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectServerBaseMyDB():
    # 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
    # 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
    # currentMethod = sys._getframe().f_code.co_name  # = "__init__"
    # print(CURRENT_FILE, currentMethod, ":: started...")

    # print("\nf_common.connectRemoteWmsDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerDbParameter()
        # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
        # print("\nf_common.connectRemoteWmsDB HOST0 : ", HOST0)
        # print("f_common.connectRemoteWmsDB USER0 : ", USER0)
        # print("f_common.connectRemoteWmsDB PASS0 : ", PASS0)
        print(get_line_no(), "connectServerBaseDB DBNAME0 : ", DBNAME0)

        DBNAME0 = 'POWERERP'

        # MySql 접속
        # mySqlServerBaseDb = mysql.connector.connect(host=HOST0, user=USER0, password=PASS0, database=DBNAME0)
        mySqlServerBaseDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0,
                                            charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayServer = mySqlServerBaseDb.cursor()
        cursDictServer = mySqlServerBaseDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...
        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlServerBaseDb is None:
            # print("\nf_common.connectRemoteBaseDB msSqlServerBaseDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"

        else:
            # msSqlServerBaseDb.ping(True)
            # print("msSqlServerBaseDb.ping(True)")
            print(get_line_no(), "connectServerBaseDB 서버 컴퓨터 POWERERP 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlServerBaseDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION

    except:
        print(get_line_no(), "connectServerBaseDB 서버 컴퓨터 POWERERP 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# # @pyqtSlot()
# def connectServerWmsMsDB():
#     # 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
#     # 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
#     # currentMethod = sys._getframe().f_code.co_name  # = "__init__"
#     # print(CURRENT_FILE, currentMethod, ":: started...")
#
#     # print("\nf_common.connectRemoteWmsDB...")
#     try:
#         # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
#         HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerMsDbParameter()
#         # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
#         # print("\nf_common.connectRemoteWmsDB HOST0 : ", HOST0)
#         # print("f_common.connectRemoteWmsDB USER0 : ", USER0)
#         # print("f_common.connectRemoteWmsDB PASS0 : ", PASS0)
#         print(get_line_no(), "connectServerWmsDB DBNAME0 : ", DBNAME0)
#
#         DBNAME0 = 'PWMS'
#
#         # MSSQL 접속
#         msSqlServerWmsDb = pymssql.connect(server=HOST0, user=USER0, password=PASS0, database=DBNAME0)
#         # msSqlServerWmsDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
#         # print('1 f_common.connectRemoteWmsDB.msSqlServerDb : ', msSqlServerWmsDb)
#         cursArrayServer = msSqlServerWmsDb.cursor()
#         # cursArrayServerWms = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
#         # print('2 f_common.connectRemoteWmsDB.cursArrayServerAms : ', cursArrayServerWms)
#         # print('f_common.connectRemoteWmsDB.cursDictLocal : ' + str(cursDictLocal))
#
#         # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...
#
#         if msSqlServerWmsDb is None:
#             # print("\nf_common.connectRemoteWmsDB mySqlLocalDb is None")
#             # time.sleep(0.1)
#             # __init__()
#             return -1, -1, "N", "N", "N", "N", "N"
#
#         else:
#             # msSqlServerDb.ping(True)
#             # print("msSqlServerDb.ping(True)")
#             print(get_line_no(), "connectServerWmsDB 원격 컴퓨터 PWMS 접속 성공 !!!")
#
#             # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
#
#             return msSqlServerWmsDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION
#
#     except:
#         print(get_line_no(), "connectServerWmsDB 원격 컴퓨터 PWMS 접속 실패")
#         # time.sleep(0.1)
#         # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')
#
#         return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectServerWmsMyDB():
    # 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
    # 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
    # currentMethod = sys._getframe().f_code.co_name  # = "__init__"
    # print(CURRENT_FILE, currentMethod, ":: started...")

    # print("\nf_common.connectRemoteWmsDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerDbParameter()
        # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
        # print("\nf_common.connectRemoteWmsDB HOST0 : ", HOST0)
        # print("f_common.connectRemoteWmsDB USER0 : ", USER0)
        # print("f_common.connectRemoteWmsDB PASS0 : ", PASS0)
        print(get_line_no(), "connectServerWmsDB DBNAME0 : ", DBNAME0)

        DBNAME0 = 'PWMS'

        # MySql 접속
        # mySqlServerWmsDb = mysql.connector.connect(host=HOST0, user=USER0, password=PASS0, database=DBNAME0)
        mySqlServerWmsDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0,
                                           charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayServer = mySqlServerWmsDb.cursor()
        cursDictServer = mySqlServerWmsDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...
        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlServerWmsDb is None:
            # print("\nf_common.connectRemoteWmsDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"

        else:
            # mySqlServerWmsDb.ping(True)
            # print("mySqlServerWmsDb.ping(True)")
            print(get_line_no(), "connectServerWmsDB 원격 컴퓨터 PWMS 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlServerWmsDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION

    except:
        print(get_line_no(), "connectServerWmsDB 원격 컴퓨터 PWMS 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# 2022.02.20 Added. MSSQL PWMS DB 를 MySql PWMS DB 로 모두 전환했다.
# ∴ 오늘부터는 Remote DB Server 또한 MySql PWMS DB 를 사용하도록 한다.
# @pyqtSlot()
def connectRemoteWmsMyDB():
    # 2020.01.15 Conclusion. 본 파일 f_common.py 는, 유틸 기능의 파일로써, 속도 향상을 위해,
    # 아래 파일명 찾기 함수와 각 함수의 이름 찾기 함수 조차도 실행하지 않게 한다.
    # currentMethod = sys._getframe().f_code.co_name  # = "__init__"
    # print(CURRENT_FILE, currentMethod, ":: started...")

    # print("\nf_common.connectRemoteWmsDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST6, USER6, PASS6, DBNAME6 = getRemoteDbParameter()
        # print("\nf_common.connectRemoteWmsDB HOST6 : ", HOST6)
        # print("f_common.connectRemoteWmsDB USER6 : ", USER6)
        # print("f_common.connectRemoteWmsDB PASS6 : ", PASS6)
        # print("f_common.connectRemoteWmsDB DBNAME6 : ", DBNAME6, "\n")

        DBNAME0 = 'PWMS'

        # MySql 접속
        # mySqlRemoteDb = mysql.connector.connect(host=HOST6, user=USER6, password=PASS6, database=DBNAME6)
        mySqlRemoteDb = pymysql.connect(host=HOST6, port=3306, user=USER6, password=PASS6, db=DBNAME6, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayRemote = mySqlRemoteDb.cursor()
        cursDictRemote = mySqlRemoteDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...
        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlRemoteDb is None:
            # print("\nf_common.connectRemoteWmsDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, -1, "N", "N", "N", "N"
        else:
            # mySqlRemoteDb.ping(True)
            # print("mySqlRemoteDb.ping(True)")
            print(get_line_no(), "connectRemoteWmsDB 원격 컴퓨터 PWMS 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlRemoteDb, cursArrayRemote, cursDictRemote, HOST6, USER6, PASS6, DBNAME6

    except:
        print(get_line_no(), "connectRemoteWmsDB 원격 컴퓨터 PWMS 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, -1, "N", "N", "N", "N"


# # @pyqtSlot()
# def connectServerAmsMsDB():
#     # print("\nf_common.connectRemoteAmsDB...")
#     try:
#         # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
#         HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerMsDbParameter()
#         # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
#         # print("\nf_common.connectRemoteAmsDB HOST0 : ", HOST0)
#         # print("f_common.connectRemoteAmsDB USER0 : ", USER0)
#         # print("f_common.connectRemoteAmsDB PASS0 : ", PASS0)
#         print(get_line_no(), "connectServerAmsDB DBNAME0 : ", DBNAME0)
#
#         DBNAME0 = 'PERP1'
#
#         # MSSQL 접속
#         msSqlServerAmsDb = pymssql.connect(server=HOST0, user=USER0, password=PASS0, database=DBNAME0)
#         # msSqlServerAmsDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
#         # print('1 f_common.connectRemoteAmsDB.msSqlServerDb : ', msSqlServerAmsDb)
#         cursArrayServer = msSqlServerAmsDb.cursor()
#         # cursArrayServerAms = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
#         # print('2 f_common.connectRemoteAmsDB.cursArrayServerAms : ', cursArrayServerAms)
#         # print('f_common.connectRemoteDB.cursDictLocal : ' + str(cursDictLocal))
#
#         # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...
#
#         if msSqlServerAmsDb is None:
#             # print("\nf_common.connectRemoteAmsDB mySqlLocalDb is None")
#             # time.sleep(0.1)
#             # __init__()
#             return -1, -1, "N", "N", "N", "N", "N"
#
#         else:
#             # msSqlServerAmsDb.ping(True)
#             # print("msSqlServerAmsDb.ping(True)")
#             print(get_line_no(), "connectServerAmsDB 원격 컴퓨터 PERP1 접속 성공 !!!")
#
#             # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
#
#             return msSqlServerAmsDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION
#
#     except:
#         print(get_line_no(), "f, _common connectServerAmsDB 원격 컴퓨터 PERP1 접속 실패")
#         # time.sleep(0.1)
#         # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')
#
#         return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectServerAmsMyDB():
    # print("\nf_common.connectRemoteAmsDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerDbParameter()
        # HOST0, USER0, PASS0, DBNAME0 = getRemoteMsDbParameter()
        # print("\nf_common.connectRemoteAmsDB HOST0 : ", HOST0)
        # print("f_common.connectRemoteAmsDB USER0 : ", USER0)
        # print("f_common.connectRemoteAmsDB PASS0 : ", PASS0)
        print(get_line_no(), "connectServerAmsDB DBNAME0 : ", DBNAME0)

        DBNAME0 = 'PERP1'

        # MySql 접속
        # mySqlServerAmsDb = mysql.connector.connect(host=HOST0, user=USER0, password=PASS0, database=DBNAME0)
        mySqlServerAmsDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0,
                                           charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayServer = mySqlServerAmsDb.cursor()
        cursDictServer = mySqlServerAmsDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...
        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlServerAmsDb is None:
            # print("\nf_common.connectRemoteAmsDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"

        else:
            # mySqlServerAmsDb.ping(True)
            # print("mySqlServerAmsDb.ping(True)")
            print(get_line_no(), "connectServerAmsDB 원격 컴퓨터 PERP1 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlServerAmsDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION

    except:
        print(get_line_no(), "f, _common connectServerAmsDB 원격 컴퓨터 PERP1 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# 2022.02.20 Added. MSSQL PERP1 DB 를 MySql PERP1 DB 로 모두 전환했다.
# ∴ 오늘부터는 Remote DB Server 또한 MySql PERP1 DB 를 사용하도록 한다.
# @pyqtSlot()
def connectRemoteAmsMyDB():
    # print("\nf_common.connectRemoteAmsMyDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST6, USER6, PASS6, DBNAME6 = getRemoteDbParameter()
        # print("\nf_common.connectRemoteAmsMyDB HOST6 : ", HOST6)
        # print("f_common.connectRemoteAmsMyDB USER6 : ", USER6)
        # print("f_common.connectRemoteAmsMyDB PASS6 : ", PASS6)
        # print("f_common.connectRemoteAmsMyDB DBNAME6 : ", DBNAME6, "\n")

        DBNAME0 = 'PERP1'

        # MySql 접속
        # mySqlRemoteDb = mysql.connector.connect(host=HOST6, user=USER6, password=PASS6, database=DBNAME6)
        mySqlRemoteDb = pymysql.connect(host=HOST6, port=3306, user=USER6, password=PASS6, db=DBNAME6, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayRemote = mySqlRemoteDb.cursor()
        cursDictRemote = mySqlRemoteDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...

        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlRemoteDb is None:
            # print("\nf_common.connectRemoteAmsMyDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, -1, "N", "N", "N", "N"
        else:
            # mySqlRemoteDb.ping(True)
            # print("mySqlRemoteDb.ping(True)")
            print(get_line_no(), "connectRemoteAmsMyDB 원격 컴퓨터 PERP1 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlRemoteDb, cursArrayRemote, cursDictRemote, HOST6, USER6, PASS6, DBNAME6

    except:
        print(get_line_no(), "connectRemoteAmsMyDB 원격 컴퓨터 PERP1 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, -1, "N", "N", "N", "N"


# # 2022.03.25 Conclusion. 여기 connectRemoteDB()와 아래 connectServerMsDB()는 완전히 같아야 하고, 완전히 동일하다.
# # 다만, 이전에 프로그램된 gatheringthreading~~, gatheringiljin~~, threadingreading~~, threadingiljin~~ 등을,
# # 지원하기 위해, 여기 connectRemoteDB()를 그대로 두고, 합리적인 이름인 connectServerMsDB()를, 동일하게 만들어,
# # 오늘 이후에는 connectServerMsDB()를 사용하도록 한다.
# # 그런데 오늘 이후로, pymssql 을 사용하지 않게 되므로, 주석 처리 한다. 여기와 연결된 모든 .py 들도 주석 처리해야 한다.
# # @pyqtSlot()
# def connectRemoteDB():
#     # global remoteDbConnection
#     print(get_line_no(), "connectRemoteDB() 내부로 들어 왔네요...")
#     msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = connectServerMsDB()
#
#
# # 2022.03.25 Conclusion. 여기 connectRemotreDB()와 아래 connectServerMsDB()는 완전히 같아야 하고, 완전히 동일하다.
# # 다만, 이전에 프로그램된 gatheringthreading~~, gatheringiljin~~, threadingreading~~, threadingiljin~~ 등을,
# # 지원하기 위해, 여기 connectRemoteDB()를 그대로 두고, 합리적인 이름인 connectServerMsDB()를, 동일하게 만들어,
# # 오늘 이후에는 connectServerMsDB()를 사용하도록 한다.
# # @pyqtSlot()
# def connectServerMsDB():
#     # global remoteDbConnection
#     print(get_line_no(), "connectServerMSDB() 내부로 들어 왔네요...")
#     try:
#         # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
#         HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerMsDbParameter()
#         # print(get_line_no(), "connectRemoteDB HOST0 : ", HOST0)
#         # print(get_line_no(), "connectRemoteDB USER0 : ", USER0)
#         # print(get_line_no(), "connectRemoteDB PASS0 : ", PASS0)
#         # print(get_line_no(), "connectRemoteDB DBNAME0 : ", DBNAME0)
#
#         # MSSQL 접속
#         msSqlServerDb = pymssql.connect(server=HOST0, user=USER0, password=PASS0, database=DBNAME0)
#         # msSqlServerDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
#         # print('1 f_common.connectRemoteDB.msSqlServerDb : ', msSqlServerDb)
#         cursArrayServer = msSqlServerDb.cursor()
#         # cursDictServer = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
#         # print('2 f_common.connectRemoteDB.cursArrayServer : ', cursArrayServer)
#         # print('f_common.connectRemoteDB.cursDictServer : ' + str(cursDictServer))
#
#         # remoteDbConnection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...
#
#         if msSqlServerDb is None:
#             # print("\nf_common.connectRemoteDB mySqlLocalDb is None")
#             # time.sleep(0.1)
#             # __init__()
#             return -1, -1, "N", "N", "N", "N", "N"
#
#         else:
#             # msSqlServerDb.ping(True)
#             # print("msSqlServerDb.ping(True)")
#             print(get_line_no(), "connectServerMSDB 원격 컴퓨터 ERP 접속 성공 !!!", HOST0)
#
#             # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
#
#             return msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION
#
#     except:
#         print(get_line_no(), "connectServerMSDB 원격 컴퓨터 ERP 접속 실패, config.ini 파일을 확인하시오!")
#         # print("f_common.connectRemoteDB HOST0 : ", HOST0)
#         # print("f_common.connectRemoteDB USER0 : ", USER0)
#         # print("f_common.connectRemoteDB PASS0 : ", PASS0)
#         # print("f_common.connectRemoteDB DBNAME0 : ", DBNAME0, "\n")
#         # time.sleep(0.1)
#         # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')
#
#         return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectServerMyDB():
    # global remoteDbConnection
    print(get_line_no(), "connectServerMyDB() 내부로 들어 왔네요...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST0, USER0, PASS0, DBNAME0, RECENTOPTION = getServerDbParameter()
        # print(get_line_no(), "connectRemoteDB HOST0 : ", HOST0)
        # print(get_line_no(), "connectRemoteDB USER0 : ", USER0)
        # print(get_line_no(), "connectRemoteDB PASS0 : ", PASS0)
        # print(get_line_no(), "connectRemoteDB DBNAME0 : ", DBNAME0)

        # MySql 접속
        # mySqlServerDb = mysql.connector.connect(host=HOST0, user=USER0, password=PASS0, database=DBNAME0)
        mySqlServerDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0,
                                        charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME0 : ' + str(DBNAME0))

        cursArrayServer = mySqlServerDb.cursor()
        cursDictServer = mySqlServerDb.cursor(pymysql.cursors.DictCursor)
        # cursDictServer = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...
        # cursDictServer = mySqlRemoteDb.cursor(dictionary=True)  # 이건 안 되네...
        # print('f_common.cursArrayServer : , cursArrayServer)
        # print('f_common.cursDictServer : ', cursDictServer)

        # remote_db_connection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlServerDb is None:
            # print("\nf_common.connectRemoteDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"

        else:
            # mySqlServerDb.ping(True)
            # print("mySqlServerDb.ping(True)")
            print(get_line_no(), "connectServerDB 원격 컴퓨터 ERP 접속 성공 !!!", HOST0)

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0, RECENTOPTION

    except:
        print(get_line_no(), "connectServerDB 원격 컴퓨터 ERP 접속 실패, config.ini 파일을 확인하시오!")
        # print("f_common.connectRemoteDB HOST0 : ", HOST0)
        # print("f_common.connectRemoteDB USER0 : ", USER0)
        # print("f_common.connectRemoteDB PASS0 : ", PASS0)
        # print("f_common.connectRemoteDB DBNAME0 : ", DBNAME0, "\n")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# 2022.03.07 Added. 이젠 아래와 같은 여러 형식의 전환이 필요하게 되었다. 아래 조건을 모두 만족시키기 위해, [REMOTE]를 추가한다.
# 1. Server 1 MSSQL AAA.DB ===> Remote 1 MySql AAA.DB : 같은 원격 컴에서 같은 DB 로 전환.
# 2. Server 1 MSSQL AAA.DB ===> Remote 2 MySql AAA.DB : 다른 원격 컴에서 같은 DB 로 전환.
# 3. Server 1 MSAQL AAA.DB ===> Remote 1 MySql BBB.DB : 같은 원격 컴에서 다른 DB 로 전환.
# 4. Server 1 MSAQL AAA.DB ===> Remote 2 MySql BBB.DB : 다른 원격 컴에서 다른 DB 로 전환.
# 2022.02.20 Added. MSSQL PowErpPsc DB 를 MySql PowErpBhj DB 로 모두 전환했다.
# ∴ 오늘부터는 Server DB Server 또한 MySql PowErpBhj DB 를 사용하도록 한다.
# @pyqtSlot()
def connectRemoteMyDB():
    # global remoteDbConnection
    # print(get_line_no(), "connectRemoteMyDB() 내부로 들어 왔네요...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        HOST6, USER6, PASS6, DBNAME6 = getRemoteDbParameter()
        # print(get_line_no(), "connectRemoteMyDB HOST6 : ", HOST6)
        # print(get_line_no(), "connectRemoteMyDB USER6 : ", USER6)
        # print(get_line_no(), "connectRemoteMyDB PASS6 : ", PASS6)
        print(get_line_no(), "connectRemoteMyDB DBNAME6 : ", DBNAME6)

        # 2022.03.07 Conclusion. 여기 'getFacParameter()' 메소드는, connectDB()와 같이 사용한다. Target DB 이므로...
        # ===> 아니다. 이건 필요가 없다. 단지 MSSQL 테이블을 MySql 테이블로 '생성'만 하는 작업이다.
        # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
        # PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = getFacParameter()

        # MySql 접속
        # mySqlRemoteDb = mysql.connector.connect(host=HOST6, user=USER6, password=PASS6, database=DBNAME6)
        mySqlRemoteDb = pymysql.connect(host=HOST6, port=3306, user=USER6, password=PASS6, db=DBNAME6, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlRemoteDb = pymysql.connect(host=HOST0, port=3306, user=USER0, password=PASS0, db=DBNAME0, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print(get_line_no(), ', connectRemoteMyDB... mySqlRemoteDb : ', mySqlRemoteDb)

        cursArrayRemote = mySqlRemoteDb.cursor()
        cursDictRemote = mySqlRemoteDb.cursor(pymysql.cursors.DictCursor)
        # cursDictRemote = mySqlRemoteDb.cursor(mysql.cursors.DictCursor)  # 이건 안 되네...

        # print(get_line_no(), 'cursArrayRemote : ', cursArrayRemote)
        # print(get_line_no(), 'cursDictRemote : ', cursDictRemote)

        if mySqlRemoteDb is None:
            print(get_line_no(), "connectRemoteMyDB mySqlLocalDb is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, -1, "N", "N", "N", "N"

        else:
            # mySqlRemoteDb.ping(True)
            # print(get_line_no(), ", mySqlRemoteDb.ping(True)")

            # cursDictRemote.ping(True)
            # print("cursDictRemote.ping(True)")
            # print(get_line_no(), "connectRemoteMyDB 원격 컴퓨터 ERP 접속 성공 !!!", HOST6, ": ", DBNAME6)
            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlRemoteDb, cursArrayRemote, cursDictRemote, HOST6, USER6, PASS6, DBNAME6

    except:
        print(get_line_no(), "connectRemoteMyDB HOST6.원격 컴퓨터 ERP 접속 실패, config.ini 파일을 확인하시오!")
        # print("f_common.connectRemoteMyDB HOST6 : ", HOST6)
        # print("f_common.connectRemoteMyDB USER6 : ", USER6)
        # print("f_common.connectRemoteMyDB PASS6 : ", PASS6)
        # print("f_common.connectRemoteMyDB DBNAME6 : ", DBNAME6, "\n")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, -1, "N", "N", "N", "N"


# @pyqtSlot()
def connectLocalDB():
    # # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1
    # global BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    # global FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE
    # global WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, TO_WAREHOUSE
    # global FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE
    # global mySqlLocalDb, cursArrayLocal, cursDictLocal

    # print("\nf_common.connectDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
        TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getLocalDbParameter()
        # print("\nf_common.connectDB COMPANY_CODE : " + COMPANY_CODE + "\n")

        FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
        PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = getFacParameter()
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
        # mySqlLocalDb = mysql.connector.connect(host=HOST1, user=USER1, password=PASS1, database=DBNAME1)
        mySqlLocalDb = pymysql.connect(host=HOST1, port=3306, user=USER1, password=PASS1, db=DBNAME1, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST1, port=3306, user=USER1, password=PASS1, db=DBNAME1, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print('__connectDB... DBNAME1 : ' + str(DBNAME1))

        cursArrayLocal = mySqlLocalDb.cursor()
        cursDictLocal = mySqlLocalDb.cursor(pymysql.cursors.DictCursor)
        # cursDictLocal = mySqlLocalDb.cursor(dictionary=True)  # 이건 안 되네...
        # cursDictLocal = mySqlLocalDb.cursor(cursor_class=MySQLCursorDict)  # cursor = db.cursor(cursor_class=MySQLCursorDict)

        # print(get_line_no(), 'cursArrayLocal : ', cursArrayLocal)
        # print(get_line_no(), 'cursDictLocal : ', cursDictLocal)

        if mySqlLocalDb is None:
            print(get_line_no(), f"connectDB mySqlLocalDb {HOST1} {DBNAME1} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, -1, \
                   "N", "N", "N", "N", "N", \
                   "N", "N", "N", "N", "N", \
                   "N", "N", "N", "N", "N", \
                   "N", "N", "N", "N", "N", "N", "N", "N", "N", \
                   "N", "N", "N", "N", "N", "N", "N"
        else:
            mySqlLocalDb.ping(True)
            # print("mySqlLocalDb.ping(True)")
            print(get_line_no(), f"connectDB 내 컴퓨터 {HOST1} {DBNAME1} 접속 성공 !!!")
            # print("\n__connectDB SERIALPORT : " + str(SERIALPORT) + "\n")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            return mySqlLocalDb, cursArrayLocal, cursDictLocal, \
                   COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
                   BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
                   FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
                   WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
                   FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT

    except:
        # print(get_line_no(), ', connectLocalDB... HOST1 : ', HOST1)
        # print(get_line_no(), ', connectLocalDB... USER1 : ', USER1)
        # print(get_line_no(), ', connectLocalDB... PASS1 : ', PASS1)
        # print(get_line_no(), ', connectLocalDB... DBNAME1 :', DBNAME1)
        print(get_line_no(), f".connectLocalDB, 내 컴퓨터 {HOST1} {DBNAME1} 접속 실패")
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
#             print("\nf_common.connectWebDB mySqlLocalDb is None")
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
        # print(get_line_no(), "connectWebWmsDB HOST3 : ", HOST3)
        # print(get_line_no(), "connectWebWmsDB USER3 : ", USER3)
        # print(get_line_no(), "connectWebWmsDB PASS3 : ", PASS3)
        # print(get_line_no(), "connectWebWmsDB DBNAME3 : ", DBNAME3)

        # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE, \
        # PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = getFacParameter()
        # # # print("\connectWebDB LINE_CODE : " + str(LINE_CODE) + "\n")
        # # # print("\connectWebDB GROUPS : " + str(GROUPS) + "\n")
        # # # print("\connectWebDB PROCESS : " + str(PROCESS) + "\n")
        # # # print("\connectWebDB FACODE : " + str(FACODE) + "\n")
        # # print("\connectWebDB TRADE : " + str(TRADE) + "\n")
        # # print("\connectWebDB BAUDRATE : " + str(BAUDRATE) + "\n")

        # mySqlWebDb = mysql.connector.connect(host=HOST3, user=USER3, password=PASS3, database=DBNAME3)
        mySqlWebDb = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME3, charset='utf8')
        # 2022.01.17 Upgraded. 아래와 같은 내용이, cursDict 이다.
        # mySqlLocalDb = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME3, charset='utf8',
        #                                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        # print(get_line_no(), 'connectWebWmsDB.mySqlWebDb : ', mySqlWebDb)

        cursArrayWeb = mySqlWebDb.cursor()
        cursDictWeb = mySqlWebDb.cursor(pymysql.cursors.DictCursor)
        # cursDictLocal = mySqlLocalDb.cursor(dictionary=True)  # 이건 안 되네...
        # print(get_line_no(), 'connectWebWmsDB.cursArrayWeb : ', cursArrayWeb)
        # print(get_line_no(), 'connectWebWmsDB.cursDictWeb : ', cursDictWeb)

        if mySqlWebDb is None:
            print(get_line_no(), f", connectWebMyDB {HOST3} {DBNAME3} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"
        else:
            mySqlWebDb.ping(True)
            # print(get_line_no(), "connectWebWmsMyDB.ping(True)")
            print(get_line_no(), f"connectWebMyDB 웹 컴퓨터 {HOST3} {DBNAME3} 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')

            # mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            # BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            return mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
                   BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
            # return mySqlWebDb, cursArrayWeb, cursDictWeb, \
            #        COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            #        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
            #        FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
            #        WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
            #        FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT

    except:
        print(get_line_no(), f"connectWebDB 웹 컴퓨터 {HOST3} ERP 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', '데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N", "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectWebWmsMyDB():
    # print(get_line_no(), "connectWebWmsDB...")
    try:
        # print(get_line_no(), "connectWebWmsDB...")
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        # HOST3, USER3, PASS3, DBNAME3 = getWebDbParameter()  # connectRemoteDB() 하고는 Return 값이 다른다.
        COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getWebDbParameter()
        print(get_line_no(), "connectWebWmsDB HOST3 : ", HOST3)
        # print(get_line_no(), "connectWebWmsDB USER3 : ", USER3)
        # print(get_line_no(), "connectWebWmsDB PASS3 : ", PASS3)
        # print(get_line_no(), "connectWebWmsDB DBNAME32 : ", DBNAME32)

        # MSSQL 접속
        # print("==========================================================================================")
        # print("f_common.connectWebWmsDB 웹 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...")
        # print("==========================================================================================")
        # todo: 2022.03.31 Conclusion. 아래 "mysql.connector.connect()"로 접속을 시도하면, 이상하게도 접속이 안 되네...
        #  저쪽 Python/Workspace/app5/에서는 잘 되었는데...
        # print(get_line_no(), "===========================================================================")
        try:
            mySqlWebDb = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME32, charset='utf8')
        except:
            # mySqlWebDb = mysql.connector.connect(host=HOST3, user=USER3, password=PASS3, database=DBNAME32)
            mySqlWebDb = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME32, charset='utf8')
        # mySqlWebDb = pymysql.connect(host=HOST3, user=USER3, password=PASS3, db=DBNAME32, port=3306, use_unicode=True, charset='utf8')

        # print(get_line_no(), 'connectWebWmsDB.mySqlWebDb : ', mySqlWebDb)
        # cursArrayServer = msSqlServerDb.cursor(as_dict=True)

        cursArrayWeb = mySqlWebDb.cursor()

        # cursDictWeb = mySqlWebDb.cursor(pymysql.cursors.DictCursor)

        # cursArrayServer = msSqlServerDb.cursor()
        # cursDictServer = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
        # print(get_line_no(), 'connectWebWmsDB.cursArrayWeb : ', cursArrayWeb)
        # print(get_line_no(), 'connectWebWmsDB.cursDictWeb : ', cursDictWeb)

        # remoteDbConnection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        # if msSqlServerDb is None:
        if mySqlWebDb is None:
            print(get_line_no(), f"connectWebWmsDB {HOST3} {DBNAME32} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"
        else:
            mySqlWebDb.ping(True)
            # print(get_line_no(), "connectWebWmsMyDB.ping(True)")
            # print(get_line_no(), f"connectWebWmsMyDB 웹 컴퓨터 {HOST3} {DBNAME32} 접속 성공 !!!")

            # # 2022.04.06 Added. 잠시 테스트... todo: ***** AWS EC2 MySql 에서는 대문자만 써야되네...
            # userId = "rwkang@naver.com"
            # password = "qq"
            # values = (userId, password)
            # print(get_line_no(), f"userId: ", userId)
            # print(get_line_no(), f"password: ", password)
            # print(get_line_no(), f"values: ", values)
            # sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP Where ID = %s AND PASSWORD = %s ORDER BY ID "
            # # sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP "
            # # sql = "Select CODE, LANGUAGE2, LANGUAGE3 From PROCESS "
            # print(get_line_no(), f"sql: ", sql)
            # try:
            #     cursArrayWeb.execute(sql)
            #     cursArrayWeb.execute(sql, values)
            # except:
            #     print(get_line_no(), "cursArrayWeb 접속 에러!!!")
            #     try:
            #         cursDictWeb.execute(sql)
            #         cursDictWeb.execute(sql, values)
            #     except:
            #         print(get_line_no(), "cursDictWeb 접속 에러!!!")
            #
            # sqlUserInfo = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
            # print(get_line_no(), " sqlUserInfo: ", sqlUserInfo)
            # print(get_line_no(), " len(sqlUserInfo): ", len(sqlUserInfo))

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
            # cursArrayServer.close()
            # msSqlServerDb.close()

            return mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32

    except:
        print(get_line_no(), f"connectWebWmsDB 웹 컴퓨터 {HOST3} {DBNAME32} 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', 'connectWebWmsDB 데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def connectWebAmsMyDB():
    # print("\nf_common.connectWebAmsDB...")
    try:
        # 2019.01.16 Added. config.ini 값을 함수로 얻어오기.
        # HOST3, USER3, PASS3, DBNAME3 = getWebDbParameter()  # connectRemoteDB() 하고는 Return 값이 다른다.
        COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = getWebDbParameter()
        # print("\nf_common.connectWebAmsDB HOST3 : ", HOST3)
        # print("f_common.connectWebAmsDB USER3 : ", USER3)
        # print("f_common.connectWebAmsDB PASS3 : ", PASS3)
        # print("f_common.connectWebAmsDB DBNAME32 : ", DBNAME32, "\n")

        # MSSQL 접속
        # print("==========================================================================================")
        # print("f_common.connectWebAmsDB 웹 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...")
        # print("==========================================================================================")
        # mySqlWebDb = mysql.connector.connect(host=HOST3, user=USER3, password=PASS3, database=DBNAME33)
        mySqlWebDb = pymysql.connect(host=HOST3, port=3306, user=USER3, password=PASS3, db=DBNAME33, charset='utf8')
        # msSqlServerDb = pymssql.connect(server=HOST3, user=USER3, password=PASS3, database=DBNAME33)
        # msSqlServerDb = pymssql.connect(server="192.168.1.107", user="sa", password="*963210z", database="PowErpKftcbj")
        # print('1 f_common.connectWebAmsDB.msSqlServerDb : ', msSqlServerDb)
        # cursArrayServer = msSqlServerDb.cursor(as_dict=True)
        cursArrayWeb = mySqlWebDb.cursor()
        cursDictWeb = mySqlWebDb.cursor(pymysql.cursors.DictCursor)
        # cursArrayServer = msSqlServerDb.cursor()
        # cursDictServer = msSqlServerDb.cursor(pymssql.cursors.DictCursor)
        # print('2 f_common.connectWebAmsDB.cursArrayServer : ', cursArrayServer)

        # remoteDbConnection = 1  # 사실 이 변수는 [시스템 전체 글로벌 변수]로 가야 되는데...

        if mySqlWebDb is None:
        # if msSqlServerDb is None:
            print(get_line_no(), f"connectWebAmsMyDB {HOST3} {DBNAME33} is None")
            # time.sleep(0.1)
            # __init__()
            return -1, -1, "N", "N", "N", "N", "N"
        else:
            # mySqlWebDb.ping(True)
            # print("mySqlWebDb.ping(True)")
            print(get_line_no(), f"connectWebAmsMyDB 웹 컴퓨터 {HOST3} {DBNAME33} 접속 성공 !!!")

            # QMessageBox.about(self, 'Connection', 'Successfully Connected to DB')
            # cursArrayServer.close()
            # msSqlServerDb.close()

            return mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME33

    except:
        print(get_line_no(), f"connectWebAmsMyDB 웹 컴퓨터 {HOST3} {DBNAME33} 접속 실패")
        # time.sleep(0.1)
        # QMessageBox.about(self, '데이터베이스 연결', 'connectWebWmsDB 데이터베이스 연결 실패!!! 시스템을 종료합니다!!!!!')

        return -1, -1, "N", "N", "N", "N", "N"


# @pyqtSlot()
def getServerDbParameter():
    # 2018.08.09 config.ini 파일로 설정해서, 프로그램이 루프 돌고 있을 때,
    # config.ini 파일 값을 변경한 것이, 프로그램에 바로 적용될 수 있도록 한다.

    config = __open_config_file()
    # print('getLocalDbParameter config : ' + str(config))
    # time.sleep(5)

    config.options('SERVER')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    if 'SERVER' in config:
        HOST0 = config.get('SERVER', 'host0')
        USER0 = config.get('SERVER', 'user0')
        PASS0 = config.get('SERVER', 'pass0')
        DBNAME0 = config.get('SERVER', 'dbname0')
        # 2022.03.14 Added. 가장 최근 DB 전환 작업 옵션 내용. [LOCAL/REMOTE] 2개만 있을 수 있다.
        RECENTOPTION = config.get('SERVER', 'recentoption')

    # print(get_line_no(), 'getRemoteDbParameter host0 : ', HOST0)
    # print(get_line_no(), 'getRemoteDbParameter user0 : ', USER0)
    # print(get_line_no(), 'getRemoteDbParameter pass0 : ', PASS0)
    # print(get_line_no(), 'getRemoteDbParameter dbname0 : ', DBNAME0)
    # print(get_line_no(), 'getRemoteDbParameter RECENTOPTION : ', RECENTOPTION)

    remote_db_connection = 1

    # IN_OK_PIN_DEFAULT = config.get('LOCAL', 'in_ok_pin_default')
    # IN_NG_PIN_DEFAULT = config.get('LOCAL', 'in_ng_pin_default')

    return HOST0, USER0, PASS0, DBNAME0, RECENTOPTION


# @pyqtSlot()
def getRemoteDbParameter():
    # 2018.08.09 config.ini 파일로 설정해서, 프로그램이 루프 돌고 있을 때,
    # config.ini 파일 값을 변경한 것이, 프로그램에 바로 적용될 수 있도록 한다.

    config = __open_config_file()
    # print('getLocalDbParameter config : ' + str(config))
    # time.sleep(5)

    config.options('REMOTE')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    if 'REMOTE' in config:
        HOST6 = config.get('REMOTE', 'host6')
        USER6 = config.get('REMOTE', 'user6')
        PASS6 = config.get('REMOTE', 'pass6')
        DBNAME6 = config.get('REMOTE', 'dbname6')

    # print(get_line_no(), 'getRemoteDbParameter host6 : ', HOST6)
    # print(get_line_no(), 'getRemoteDbParameter user6 : ', USER6)
    # print(get_line_no(), 'getRemoteDbParameter pass6 : ', PASS6)
    # print(get_line_no(), 'getRemoteDbParameter dbname6 : ', DBNAME6)

    # IN_OK_PIN_DEFAULT = config.get('LOCAL', 'in_ok_pin_default')
    # IN_NG_PIN_DEFAULT = config.get('LOCAL', 'in_ng_pin_default')

    return HOST6, USER6, PASS6, DBNAME6


# @pyqtSlot()
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
        print(get_line_no(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

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
    # print(get_line_no(), ', getLocalDbParameter config : ', config)
    # print(get_line_no(), ', getLocalDbParameter len(config) : ', len(config))
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

        print(get_line_no(), "getWebDbParameter 호출 후 COMPANY_CODE : ", COMPANY_CODE)
        print(get_line_no(), "getWebDbParameter 호출 후 HOST3 : ", HOST3)
        # print(get_line_no(), ",,f_common_getWebDbParameter 호출 후 USER3 : ", USER3)
        # print(get_line_no(), ",,f_common_getWebDbParameter 호출 후 DBNAME3 : ", DBNAME3)
        # print(get_line_no(), "getWebDbParameter 호출 후 DBNAME32 : ", DBNAME32)
        # print(get_line_no(), "getWebDbParameter 호출 후 DBNAME33 : ", DBNAME33)
        # print(get_line_no(), "getWebDbParameter 호출 후 BOUNCE_TIME : " + str(BOUNCE_TIME))
        # print(get_line_no(), "getWebDbParameter 호출 후 SLEEP_TIME : " + str(SLEEP_TIME))
        # print(get_line_no(), "getWebDbParameter 호출 후 TIME_GAP : " + str(TIME_GAP))
        # print(get_line_no(), "getWebDbParameter 호출 후 NIGHT_CLOSING_HHMMSS : " + str(NIGHT_CLOSING_HHMMSS))
        # print(get_line_no(), "getWebDbParameter 호출 후 DAY_CLOSING_HHMMSS : " + str(DAY_CLOSING_HHMMSS))

        # IN_OK_PIN_DEFAULT = config.get('LOCAL', 'in_ok_pin_default')
        # IN_NG_PIN_DEFAULT = config.get('LOCAL', 'in_ng_pin_default')

        return COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, DBNAME32, DBNAME33, BOUNCE_TIME, SLEEP_TIME, \
               TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    else:
        print(get_line_no(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

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
        print(get_line_no(), ", 먼저 config.ini .파일을 세팅하시오! 관리자에게 문의하시오!!!")

        return "N", "N", "N", "N", "N", \
               "N", "N", "N", "N", 0, "N", "N", 0, "N", "N", \
               "N", "N", "N", "N", "N", 0, 0


# @pyqtSlot()  # 가져오기
def getFrequencyStandard():
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
        print(get_line_no(), ", getFacParameter ???")


# @pyqtSlot()  # 세팅하기
def setFacParameter(PROCESS, GROUPS, DESCRIPTION, LINE_CODE, work_date_ymd_string,
                    DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, FACODE,
                    PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT):
    # print('\setFacParameter CAVITY : ', CAVITY)
    # print('setFacParameter CAVITYRIGHT : ', CAVITYRIGHT)
    print(get_line_no(), ', setFacParameter SERIALPORT : ', SERIALPORT)

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
        print(get_line_no(), ", __setFacParameter SERIALPORT : " + str(SERIALPORT))
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


# @pyqtSlot()  # 가져오기 1
def getQrcode():
    # global VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, QRCODEDATA, FILL, BACK_COLOR

    # QMessageBox.about(self, '__getFacParameter', '__getFacParameter')
    # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수에 정의되야 한다.
    # global FORPRODUCINGORDERDATA, process, groups, DESCRIPTION_TEXT, line_code
    # global WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY
    # 2017.01.17 Conclusion. global 변수는 반드시 "최초 지정"하는 함수(__startWork())에 정의되야 한다.
    # global description, work_date_ymd_string

    config = __open_config_file()
    # print('getQrcode config : ' + str(config))
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
    # # config.read(filenames=currentDir + '../config.ini', encoding='utf-8')
    # config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    # # config.read('/home/pi/dev/gathering/config.ini')  # INI 파일 읽기
    # # # ['config.ini']
    # # config.sections()  # 섹션 리스트 읽기
    # # # ['LOCAL']
    config.options('QRCODE')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('getQrcode config : ' + str(config))
    if 'QRCODE' in config:
        VERSION = config.get('QRCODE', 'version')
        ERROR_CORRECTION = config.get('QRCODE', 'error_correction')
        BOX_SIZER = config.get('QRCODE', 'box_sizer')
        BORDER = config.get('QRCODE', 'border')
        QRCODEDATA = config.get('QRCODE', 'qrcodedata')
        FILL = config.get('QRCODE', 'fill')
        BACK_COLOR = config.get('QRCODE', 'back_color')
        # print("__getQrcode VERSION : " + str(VERSION))
        # print("__getQrcode ERROR_CORRECTION : " + str(ERROR_CORRECTION))
        # print("__getQrcode BOX_SIZER : " + str(BOX_SIZER))
        # print("__getQrcode BORDER : " + str(BORDER))
        # print("__getQrcode DATA : " + str(DATA))
        return VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, QRCODEDATA, FILL, BACK_COLOR


# @pyqtSlot()  # 세팅하기
def setQrcode(VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, QRCODEDATA, FILL, BACK_COLOR):
    # config.set('PRODUCT_ENV', 'FORPRODUCINGORDERDATA', yn_producing_order_data)
    config = __open_config_file()
    # print('setQrcode config : ' + str(config))
    # time.sleep(5)

    # config = ConfigParser()
    # # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    # if getattr(sys, 'frozen', False):
    #     print("1")
    #     # pyinstaller로 패키징한 실행파일의 경우
    #     cur_path = os.path.dirname(sys.executable)
    #     print('if cur_path : ' + str(cur_path))
    # elif __file__:
    #     print("2")
    #     # *.py 형태의 파일로 실행할 경우 로직
    #     cur_path = os.path.dirname(os.path.abspath(__file__))
    #     print('elif cur_path : ' + str(cur_path))
    #
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # # print("__getLocalDbParameter currentDir : " + currentDir)
    # # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')
    # # ['config.ini']
    # config.sections()  # 섹션 리스트 읽기
    # # ['LOCAL']
    # # config.read('/home/pi/dev/gathering/config.ini')  # INI 파일 읽기
    # # # ['config.ini']
    # # config.sections()  # 섹션 리스트 읽기
    # # # ['LOCAL']
    config.options('QRCODE')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('setQrcode config : ' + str(config))
    if 'QRCODE' in config:
        # return VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, DATA, FILL, BACK_COLOR
        config.set('QRCODE', 'version', VERSION)
        config.set('QRCODE', 'error_correction', ERROR_CORRECTION)
        config.set('QRCODE', 'box_sizer', BOX_SIZER)
        config.set('QRCODE', 'border', BORDER)
        config.set('QRCODE', 'fill', FILL)
        config.set('QRCODE', 'qrcodedata', QRCODEDATA)
        config.set('QRCODE', 'back_color', BACK_COLOR)
        # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')
        # config_file = open('/home/pi/dev/gathering/config.ini', 'w')
        # config_file = open('config.ini', 'w')

        # config = __open_config_file()

        is_write = __save_config_file(config)
        # print("setQrcode is_write : ", is_write)

        return is_write


# @pyqtSlot()  # 세팅하기
def setServer(HOST0, USER0, PASS0, DBNAME0, RECENTOPTION):
    config = __open_config_file()
    # # # ['SERVER']
    config.options('SERVER')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print('setServer config : ', config)
    if 'SERVER' in config:
        # return VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, DATA, FILL, BACK_COLOR
        config.set('SERVER', 'host0', HOST0)
        config.set('SERVER', 'user0', USER0)
        config.set('SERVER', 'pass0', PASS0)
        config.set('SERVER', 'dbname0', DBNAME0)
        # 2022.03.14 Added. 가장 최근 DB 전환 작업 옵션 내용. [LOCAL/REMOTE] 2개만 있을 수 있다.
        config.set('SERVER', 'recentoption', RECENTOPTION)

        is_write = __save_config_file(config)
        # print("setServer is_write : ", is_write)

        return is_write


# @pyqtSlot()  # 세팅하기
def setRemote(HOST6, USER6, PASS6, DBNAME6):
    config = __open_config_file()
    # # # ['REMOTE']
    config.options('REMOTE')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print(get_line_no(), ', setRemote config : ', config)
    if 'REMOTE' in config:
        # return VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, DATA, FILL, BACK_COLOR
        # print(get_line_no(), ", HOST6: ", HOST6)
        config.set('REMOTE', 'host6', HOST6)
        config.set('REMOTE', 'user6', USER6)
        config.set('REMOTE', 'pass6', PASS6)
        config.set('REMOTE', 'dbname6', DBNAME6)

        print(get_line_no(), " DBNAME6: ", DBNAME6)
        is_write = __save_config_file(config)
        # print(get_line_no(), ", setRemote is_write : ", is_write)

        return is_write


# @pyqtSlot()  # 세팅하기
def setLocal(HOST1, USER1, PASS1, DBNAME1):
    config = __open_config_file()
    # # # ['REMOTE']
    config.options('LOCAL')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print(get_line_no(), ', setRemote config : ', config)
    if 'LOCAL' in config:
        # return VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, DATA, FILL, BACK_COLOR
        # print(get_line_no(), ", HOST1: ", HOST1)
        config.set('LOCAL', 'host1', HOST1)
        config.set('LOCAL', 'user1', USER1)
        config.set('LOCAL', 'pass1', PASS1)
        config.set('LOCAL', 'dbname1', DBNAME1)
        # print(get_line_no(), ", DBNAME1: ", DBNAME1)
        is_write = __save_config_file(config)
        # print(get_line_no(), ", setRemote is_write : ", is_write)

        return is_write


# def __generateQrcode():
#     # q = pyqrcode.create("My first Qrcode")
#     # q.png('MyFirstQrcode.png', scale=6)
#     qr = qrcode.make('My first Qrcode')
#     qr.save('MyFirstQrcode.png')
#     print("Qrcode generated ...")

# @pyqtSlot()
def generateQrcode(qrcodeGenerateData):
    VERSION, ERROR_CORRECTION, BOX_SIZER, BORDER, QRCODEDATA, FILL, BACK_COLOR = getQrcode()
    # print("generateQrcode VERSION : " + str(VERSION) + "\n")
    # print("generateQrcode ERROR_CORRECTION : " + str(ERROR_CORRECTION) + "\n")
    # print("generateQrcode BOX_SIZER : " + str(BOX_SIZER) + "\n")
    # print("generateQrcode BORDER : " + str(BORDER) + "\n")
    # print("generateQrcode generateQrcode QRCODEDATA : " + str(QRCODEDATA) + "\n")
    # print("generateQrcode generateQrcode FILL : " + str(FILL) + "\n")
    # print("generateQrcode generateQrcode BACK_COLOR : " + str(BACK_COLOR) + "\n")

    # print("generateQrcode generateQrcode qrcodeGenerateData : " + str(qrcodeGenerateData) + "\n")

    # 2019.10.19 Created. QRCode 생성 기준
    # 1. 191019 : 날짜 : 8자리
    # 2. PSB001 : 회사명 : 6자리
    # 3. 01 : 생산 라인 번호
    # 4. 1 : 주/야간
    # 5. F374EXFDE03 또는 PSKEI4321 : 품번
    # 6. 0001 : 해당 일자 기준 일련 번호
    # 7. 9999 : 박스(파렛트) 포장 기준 수량 : 20개면 : 0020

    # qr = qrcode.QRCode(
    #     version=VERSION,
    #     error_correction=ERROR_CORRECTION,
    #     box_size=BOX_SIZER,
    #     border=BORDER
    # )
    qr = qrcode.QRCode(
        version=VERSION,
        box_size=BOX_SIZER,
        border=BORDER
    )
    qrcodeSerialNo = "0001"
    data = qrcodeGenerateData  # '191022PSB0010518000013052'
    qr.add_data(qrcodeGenerateData)
    qr.make(fit=True)
    img = qr.make_image(fill=FILL, back_color=BACK_COLOR)

    config = ConfigParser()
    # print('1 __getLocalDbParameter 함수 내부')

    # pyinstaller를 사용하지 않는다면, elif 부분만 필요함
    if getattr(sys, 'frozen', False):
        # pyinstaller로 패키징한 실행파일의 경우
        cur_path = os.path.dirname(sys.executable)
        # print('if cur_path : ' + str(cur_path))
    elif __file__:
        # *.py 형태의 파일로 실행할 경우 로직
        cur_path = os.path.dirname(os.path.abspath(__file__))
        # print('elif cur_path : ' + str(cur_path))

    currentDir = os.path.dirname(os.path.realpath(__file__))
    # print("__getLocalDbParameter currentDir : " + currentDir)
    # config.read(filenames='/home/pi/dev/gathering/config.ini', encoding='utf-8')  # INI 파일 읽기
    # config.read(filenames=currentDir + '/config.ini', encoding='utf-8')

    current_date = datetime.date.today()
    # print("\ngenerateQrcode current_date : " + str(current_date))
    date_format = "%y%m%d"  # 소문자 "y"임에 주의, "%Y%m%d" = "20191022" : 대문자 "Y"임에 주의.
    # current_date_ymd_string = current_date.toString("yyMMdd")  # 2019.10.22 Conclusion. 요기 today() 값은 에러 난다.
    current_date_ymd_string = current_date.strftime(date_format)
    # print("\ngenerateQrcode current_date_ymd_string : " + str(current_date_ymd_string))

    qrcodeDir = currentDir + '/qrcode/'
    if os.path.isdir(qrcodeDir):
        os.path.join(currentDir, 'qrcode')  # 기존 경로와 새로운 폴더 이름을 합쳐서 하위 경로 만들기.
    else:
        os.mkdir(qrcodeDir)
    os.chdir(qrcodeDir)  # 작업 경로 바꾸기: os.chdir(path)

    qrcodeDirYear = qrcodeDir + '/' + current_date_ymd_string + '/'
    if os.path.isdir(qrcodeDirYear):
        os.path.join(qrcodeDirYear, 'current_date_ymd_string')  # 기존 경로와 새로운 폴더 이름을 합쳐서 하위 경로 만들기.
    else:
        os.mkdir(qrcodeDirYear)
    os.chdir(qrcodeDirYear)  # 작업 경로 바꾸기: os.chdir(path)

    # 2019.10.22 Added. 여기서 Qrcode 마지막 시리얼 번호를 찾는다. 파일명의 끝에서 4자리.
    path = "./"
    file_list = os.listdir(path)
    file_list_png = [file for file in file_list if file.endswith(".png")]
    # print("1 generateQrcode file_list_png: {}".format(file_list_png))
    file_list_png.reverse()
    # print("1 generateQrcode reverse file_list_png: {}".format(file_list_png))

    # path = "./"
    file_list = os.listdir(qrcodeDirYear)
    file_list_png = [file for file in file_list if file.endswith(".png")]
    # print("2 generateQrcode file_list_png: {}".format(file_list_png))
    file_list_png.reverse()
    # print("2 generateQrcode reverse file_list_png: {}".format(file_list_png))

    file_count = len(file_list_png)
    # print("generateQrcode file_count : ", file_count)

    if file_count == 0:
        qrcodeSerialNo = "QR0001"
    else:
        for i, fileNameFull in enumerate(file_list_png):  # 또는 for i in file_count:
            # print("generateQrcode i : " + str(i) + ", fileNameFull : " + fileNameFull)
            # fileNames = fileNameFull[0].split('.')  # 값은 리스트로 ['file name', 'extension name']
            # print("fileNames : ", fileNames)
            # fileName = fileNames[0]  # 값은 문자열로 'file name'
            # print("Only fileName : ", fileName)
            # qrcodeSerialNo = fileName[-4:]
            # print("\nqrcodeSerialNo : ", qrcodeSerialNo)

            fileNames = file_list_png[i].split('.')  # 값은 리스트로 ['file name', 'extension name']
            # print("generateQrcode fileNames : ", fileNames)
            fileName = fileNames[0]  # 값은 문자열로 'file name'
            # print("generateQrcode Only fileName : ", fileName)
            qrcodeSerialNo = fileName[-4:]
            # print("\ngenerateQrcode qrcodeSerialNo : ", qrcodeSerialNo)

            checkSpecialCharacters = '[A-Za-z@_!#$%^&*()<>?/\|}{~:]'  # '[A-Za-z!@#$%^&*]'
            # print("generateQrcode checkSpecialCharacters origin : ", checkSpecialCharacters)
            checkSpecialCharacters = re.compile(checkSpecialCharacters)
            # print("generateQrcode checkSpecialCharacters compiled : ", checkSpecialCharacters)
            # print("(checkSpecialCharacters.search(qrcodeSerialNo) : ", (checkSpecialCharacters.search(qrcodeSerialNo)))
            if (checkSpecialCharacters.search(qrcodeSerialNo) == None):  # 값이 모두 숫자임. 한 글자도 문자나 특수 문자가 없다.
                break
            else:  # 값 중에 한 글자라도 문자나 특수 문자가 있다면,
                qrcodeSerialNo = "0000"  # 초기화의 의미임.
                continue

        # print("\ngenerateQrcode 현재 파일 중 마지막 qrcodeSerialNo : ", qrcodeSerialNo)

    qrcodeSerialNo = str(int(qrcodeSerialNo) + 1).zfill(4)
    qrcodeSerialNo = "QR" + qrcodeSerialNo
    # print("\ngenerateQrcode 새로 발행할 최종 qrcodeSerialNo : ", qrcodeSerialNo)

    # qrcodeFileName = qrcodeGenerateData + "BOX0020" + qrcodeSerialNo  # 'YoutubeChannel.png'
    qrcodeFileName = qrcodeGenerateData + qrcodeSerialNo + '.png'  # 'YoutubeChannel.png'
    img.save(qrcodeFileName)
    # print("generateQrcode Qrcode generated qrcodeFileName : ", qrcodeFileName)

    os.chdir(currentDir)  # 작업경로 바꾸기: os.chdir(path)

    return qrcodeFileName


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
        print(get_line_no(), " 합 currentDir : " + currentDir)

        # 2021.12.30 Added. .exe 파일로 컴파일 할 경우,
        # 폴더가 이상하게도
        # "C:\Windows\SysWOW64\config\\rwkang\Users\ADMINI~1\AppData\Local\Temp\_MEI306602"로 세팅되네...
        if currentDir.find("Users"):
            currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang\\Python\\Workspace\\app5"

        currentDir = currentDir.replace("\\", '/')
        print(get_info(), " 최종 currentDir : ", currentDir)
        # path = "./python/test"
        if not os.path.isdir(currentDir):
            # print("f_common.py.__open_config_file() 이쪽으로 들어 왔나?")
            try:
                # 2021.01.25 Conclusion. 아래 명령으로 폴더는 못 만드네... 그냥 수동으로 반드시 만들고 진행한다.
                # os.mkdirs(currentDir, exist_ok=True)
                # kkk = os.mkdirs(currentDir)
                print(get_line_no(), " 설정 폴더가 없습니다. "
                                     "관리자에게 문의하시오! currentDir: ", currentDir)
                # time.sleep(5)
                return
            except Exception as e:
                # except EnvironmentError.errno:
                print(get_line_no(), " 만들었나? Exception.e : " + e)
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
    config.read(filenames=currentDir + '/config.ini', encoding='utf-8')

    # ['config.ini']
    config.sections()  # 섹션 리스트 읽기
    # ['LOCAL']
    config.options('LOCAL')  # 옵션 이름 리스트 얻기 # ['host0','user0','pass0','dbname0']
    # print(get_line_no(), '.__open_config_file() config : ', config)
    # print(get_line_no(), '.__open_config_file() type(config) : ', type(config))
    # if 'LOCAL' in config:
    #     # print(get_line_no(), " config.options() : ")
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
    # print(get_line_no(), ' HOST1 : ', HOST1)
    # else:
    #     print("f_common.py.__open_config_file() config.options() : ???")

    print(get_info(), "리턴 currentDir : " + currentDir)
    # print(get_info(), "리턴 config : " + config)
    # print(get_info(), "리턴 config : " + config)

    return config


def __save_config_file(config):
    # print(get_line_no(), ".__save_config_file(): config", config)

    # 2021.01.25 Conclusion. os가 윈도우일 경우에는, 즉 일반 PC 사용자일 경우에는,
    # [config.ini] 파일을 [C:\Windows\SysWOW64\config] 루트 드라이브 및 윈도우 폴더를 활용한다.
    # print('f_common.py.__save_config_file() 함수 내부 type(platform.system()):', type(platform.system()))
    # print('f_common.py.__save_config_file() 함수 내부 platform.system():', platform.system())
    if sys.platform.system() == 'Windows':
        projectDir = os.path.dirname(os.path.realpath(__file__))[2:]  # \ps\ppp : [C:\] 드라이브는 뺀다.
        # print(get_line_no(), ".setPlcDataLog() __getLocalDbParameter projectDir : " + projectDir)
        currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang" + projectDir
        # print(get_line_no(), ".setPlcDataLog() 합 __getLocalDbParameter currentDir : " + currentDir)

        # 2021.12.30 Added. .exe 파일로 컴파일 할 경우,
        # 폴더가 이상하게도 "C:\Windows\SysWOW64\config\\rwkang\Users\ADMINI~1\AppData\Local\Temp\_MEI306602"로 세팅되네...
        if currentDir.find("Users"):
            currentDir = "C:\\Windows\\SysWOW64\\config\\rwkang\\Python\\Workspace\\app5"

        currentDir = currentDir.replace("\\", '/')
        # print("f_common.py.__save_config_file() 합 변환 currentDir : " + currentDir)
    else:
        currentDir = os.path.dirname(os.path.realpath(__file__))
        # print("f_common.py.__save_config_file() 여기 os는 ? ", platform.system()) : Raspberry PI.라즈베리파이컴은, 현재 디렉토리로 바로 온다...
        print(get_line_no(), ".__save_config_file() 여기 os는 ? currentDir : " + currentDir)

    config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    # print(get_line_no(), ".__save_config_file() config_file : ", config_file)
    config.write(config_file)
    # print(get_line_no(), ".__save_config_file() config_file : ", config_file)
    config_file.close()
    return 1

    # config = __open_config_file()
    # currentDir = os.path.dirname(os.path.realpath(__file__))
    # config_file = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    # config.write(config_file)
    # config_file.close()
    # return 1


def setPlcDataLog(gathering_no_max_this, COMPANY_CODE, PROCESS, GROUPS, LINE_CODE, CODE, GOODS, PLC_ADDRESS, PLC_VALUE):
    # print('setPlcDataLog gathering_no_max_this : ', gathering_no_max_this)
    # print('setPlcDataLog COMPANY_CODE : ', COMPANY_CODE)
    # print('setPlcDataLog PROCESS : ', PROCESS)
    # print('setPlcDataLog GROUPS : ', GROUPS)
    # print('setPlcDataLog LINE_CODE : ', LINE_CODE)
    # print('setPlcDataLog CODE : ', CODE)
    # print('setPlcDataLog GOODS : ', GOODS)
    # print('setPlcDataLog PLC_ADDRESS : ', PLC_ADDRESS)
    # print('setPlcDataLog PLC_VALUE : ', PLC_VALUE)
    # print('setPlcDataLog COMPANY_CODE type : ', type(COMPANY_CODE))
    # print('setPlcDataLog PROCESS type : ', type(PROCESS))
    # print('setPlcDataLog GROUPS type : ', type(GROUPS))
    # print('setPlcDataLog LINE_CODE type : ', type(LINE_CODE))
    # print('setPlcDataLog CODE type : ', type(CODE))
    # print('setPlcDataLog GOODS type : ', type(GOODS))
    # print('setPlcDataLog PLC_ADDRESS type : ', type(PLC_ADDRESS))
    # print('setPlcDataLog PLC_VALUE type : ', type(PLC_VALUE))

    currentDir = os.path.dirname(os.path.realpath(__file__))

    date_time_current = datetime.datetime.now()
    time_format = "%Y-%m-%d %H:%M:%S"
    currentDateTime = datetime.date.today().strftime("%Y-%m-%d")  # 오늘 날짜만.  # .date.에 주의
    # print('\nsetPlcDataLog currentDateTime : ', currentDateTime, "\n")
    currentDateTimeStr = date_time_current.strftime(time_format)  # 오늘 날짜만.  # .date.에 주의
    # print('\nsetPlcDataLog currentDateTime : ', currentDateTime, "\n")
    currentMonth = date_time_current.month
    currentMonthStr = str("{0:0>2}".format(currentMonth))
    currentDay = date_time_current.day
    currentDayStr = str("{0:0>2}".format(currentDay))

    se = ","
    plcData = gathering_no_max_this + se + currentDateTimeStr + se + COMPANY_CODE + se + PROCESS + se + \
              GROUPS + se + LINE_CODE + se + CODE + se + GOODS + se + PLC_ADDRESS + se + PLC_VALUE + "\n"
    # print('\nsetPlcDataLog plcData : ', plcData, "\n")

    # file = './PlcDataLog' + currentMonthStr + currentDayStr + '.txt'
    fileName = '/PlcDataLog' + currentMonthStr + currentDayStr + '.txt'
    fileNameFull = currentDir + fileName
    # plcDataLog = open(file, 'w')  #
    # plcDataLog = open(file=currentDir + '/config.ini', mode='wt', encoding='utf-8')
    if os.path.isfile(fileNameFull):  # os.path.isfile(file) => 이건 파일 못 찾음.
        print(get_line_no(), ".setPlcDataLog() 파일이 있습니다. fileNameFull : ", fileNameFull)
        # time.sleep(0.03)
        plcDataLog = open(file=fileNameFull, mode='a', encoding='utf-8')
    else:
        print(get_line_no(), ".setPlcDataLog() 파일이 없네... fileNameFull : ", fileNameFull)
        # time.sleep(0.03)
        plcDataLog = open(file=fileNameFull, mode='wt', encoding='utf-8')
    is_write = plcDataLog.write(plcData)
    plcDataLog.close()
    print(get_line_no(), ".setPlcDataLog() setPlcDataLog is_write : ", is_write)
    return is_write


def __delete_PlcDataLog():
    # 최근 자료 10개 파일 삭제
    date_time_current = datetime.datetime.now()
    currentMonth = date_time_current.month
    currentMonthStr = str("{0:0>2}".format(currentMonth))
    currentDay = date_time_current.day
    currentDayStr = str("{0:0>2}".format(currentDay))

    time_format = "%Y-%m-%d %H:%M:%S"
    # now_utc = time.time()  # UTC 현재 시각(초)
    # print("now_utc : " + str(now_utc))
    # now_date = datetime.date.today().strftime("%Y-%m-%d")  # 오늘 날짜만.  # .date.에 주의
    now_date = datetime.date.today().strftime("%Y%m%d")  # 오늘 날짜만.  # .date.에 주의

    i = 1  # 2020.04.23 Modified. 어제 파일은 살려 둔다. 그제 파일까지 삭제하도록...
    while i < 9:
        i += 1

        deleteDay = currentDay - i
        if deleteDay == 0:
            currentMonth = currentMonth - 1
            if currentMonth == 0:
                currentMonth = 12
            if currentMonth == 4 or currentMonth == 6 or currentMonth == 9 or currentMonth == 11:
                currentDay = 30
            elif int(currentMonth) == 2:
                currentDay = 28
            else:
                currentDay = 31
        deleteDayStr = str("{0:0>2}".format(deleteDay))

        # file = './upload/test.txt'  # 하위 디렉토리 이용.
        # file = './PlcDataLog' + currentMonthStr + deleteDayStr + '.txt'
        # if os.path.isfile(file):

        currentDir = os.path.dirname(os.path.realpath(__file__))
        # file = './PlcDataLog' + currentMonthStr + deleteDayStr + '.txt'
        fileName = '/PlcDataLog' + currentMonthStr + deleteDayStr + '.txt'
        fileNameFull = currentDir + fileName
        if os.path.isfile(fileNameFull):  # os.path.isfile(file) => 이건 파일 못 찾음.
            print(get_line_no(), ", __delete_PlcDataLog 파일이 있습니다. fileNameFull : ", fileNameFull)
            os.remove(fileNameFull)
            time.sleep(0.1)
            return 'okay'
        else:
            print(get_line_no(), ", __delete_PlcDataLog 파일이 없네... fileNameFull : ", fileNameFull)
            time.sleep(0.1)
            return 'NG'


# 2022.02.17 Added. MS SQL 전체 테이블을, MySql 에서 한방에 생성하는 함수에서, 테이블 생성 sql 문장을 받아, 테이블 생성한다.
def creatingTable(mySqlDbDivision, cursArrayDivision, sql, target, hostDivision):
    # print("1 f_common.py.creatingTable sql: ", sql)

    lastPoint = sql.find(" ( ")  # - 1  # "CREATE TABLE IF NOT EXISTS MOVINGDATA1302 ( " 여기서 테이블명 바로 앞 문자 찾기.
    tableName = sql[27:lastPoint]

    # if target.upper() == "LOCAL":
    cursArrayDivision.execute(sql)
    # elif target.upper() == "REMOTE":
    #     cursArrayDivision.execute(sql)

    try:
        mySqlDbDivision.commit()
        if target.upper() == "LOCAL":
            print(get_line_no(), f", Local 컴퓨터에 테이블({tableName}) 생성 완료! \n")
        elif target.upper() == "REMOTE":
            print(get_line_no(), f", Remote.원격 컴퓨터에 테이블({tableName}) 생성 완료! \n")

        # sleep(1)  # 10분 = 600
        check = True
    except:
        mySqlDbDivision.rollback()
        if target.upper() == "LOCAL":
            print(get_line_no(), f", Local 컴퓨터에 테이블({tableName}) 생성 실패! \n")
        elif target.upper() == "REMOTE":
            print(get_line_no(), f", Remote.원격 컴퓨터({hostDivision})에 테이블({tableName}) 생성 실패! \n")
        # sleep(1)  # 10분 = 600
        sys.exit()
        check = False

    return sql, check


def creating_gathering_goods(mySqlLocalDb, cursArrayLocal):
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
    cursArrayLocal.execute(sql)
    try:
        mySqlLocalDb.commit()
        print(get_line_no(), ", Local 제품 테이블(gathering_goods) 생성 완료! ")
        # sleep(1)  # 10분 = 600
        tf = True
    except:
        mySqlLocalDb.rollback()
        print(get_line_no(), ", Local 제품 테이블(gathering_goods) 생성 실패! ")
        # sleep(1)  # 10분 = 600
        sys.exit()
        tf = False
    return sql, tf


def creating_gathering_description(mySqlLocalDb, cursArrayLocal):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS Gathering_Description (" \
          "Id bigint(20) unsigned Not Null Auto_Increment PRIMARY KEY ," \
          "Language1 varchar(255)," \
          "Language2 varchar(255)," \
          "Language3 varchar(255)," \
          "language4 varchar(255)," \
          "Process varchar(100) Not Null," \
          "GoodsAssets int Not Null," \
          "UserId varchar(100)," \
          "ModifiedDate datetime Not Null Default Current_TimeStamp " \
          ")"
    cursArrayLocal.execute(sql)

    # UNIQUE Column 만들기 위해서는, 테이블 생성 후 따로 명령한다.
    # ALTER TABLE Gathering_ProductionActual UNIQUE(ProductionActualNo(100));

    try:
        mySqlLocalDb.commit()
        tf = True
        print(" : Local 품명 테이블(Descrition) 생성 완료! ")
        time.sleep(1)  # 10분 = 600
    except:
        mySqlLocalDb.rollback()
        tf = False
        print(" : Local 품명 테이블(Description) 생성 실패! ")
        time.sleep(1)  # 10분 = 600
        sys.exit()

    return sql, tf


def creating_gathering_groups(mySqlLocalDb, cursArrayLocal):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS Gathering_Groups (" \
          "Id bigint(20) unsigned Not Null Auto_Increment PRIMARY KEY ," \
          "Code varchar(100) Not Null," \
          "PaCode varchar(100) Not Null, " \
          "Language1 varchar(255)," \
          "Language2 varchar(255)," \
          "Language3 varchar(255)," \
          "language4 varchar(255)," \
          "Process varchar(100) Not Null," \
          "Team int Not Null," \
          "LineCode int Not Null," \
          "FaCode varchar(100)," \
          "UserId varchar(100)," \
          "ModifiedDate datetime Not Null Default Current_TimeStamp " \
          ")"

    cursArrayLocal.execute(sql)
    # UNIQUE Column 만들기 위해서는, 테이블 생성 후 따로 명령한다.
    # ALTER TABLE Gathering_ProductionActual UNIQUE(ProductionActualNo(100));

    try:
        mySqlLocalDb.commit()
        tf = True
        print(" : Local 품명 테이블(Descrition) 생성 완료! ")
        time.sleep(1)  # 10분 = 600
    except:
        mySqlLocalDb.rollback()
        tf = False
        print(" : Local 품명 테이블(Description) 생성 실패! ")
        time.sleep(1)  # 10분 = 600
        sys.exit()

    return sql, tf


def creating_gathering_equipmentofproduct(mySqlLocalDb, cursArrayLocal):
    # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
    sql = "CREATE TABLE IF NOT EXISTS Gathering_EquipmentOfProduct (" \
          "Id bigint(20) unsigned Not Null AUTO_INCREMENT PRIMARY KEY ," \
          "Process varchar(100) Not Null," \
          "LineCode varchar(100) Not Null," \
          "Code varchar(100) Not Null," \
          "FaCode varchar(100), " \
          "BarcodeInfo varchar(200)," \
          "BeInUse varchar(10) Not Null," \
          "DescriptionEquipment varchar(200)," \
          "CreatedUser varchar(200)," \
          "CreatedDate datetime Not Null Default Current_TimeStamp," \
          "ModifiedUser varchar(200)," \
          "ModifiedDate datetime Not Null Default Current_TimeStamp " \
          ")"

    cursArrayLocal.execute(sql)
    # UNIQUE Column 만들기 위해서는, 테이블 생성 후 따로 명령한다.
    # ALTER TABLE Gathering_ProductionActual UNIQUE(ProductionActualNo(100));

    try:
        mySqlLocalDb.commit()
        tf = True
        print(" : Local 설비별 생산품 등록 테이블(Gathering_EquipmentOfProduct) 생성 완료! ")
        time.sleep(1)  # 10분 = 600
    except:
        mySqlLocalDb.rollback()
        tf = False
        print(" : Local 설비별 생산품 등록 테이블(Gathering_EquipmentOfProduct) 생성 실패! ")
        time.sleep(1)  # 10분 = 600
        sys.exit()

    return sql, tf


def getting_goodsmaster(msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0,
                        mySqlLocalDb, cursArrayLocal, cursDictLocal, HOST1, USER1, PASS1, DBNAME1):
    if len(DBNAME0) > 1:

        loop_count = 0
        # if remoteDbConnection == 1 and localDbConnection == 1:

        loop_count += 1
        # print("loop_count : "+str(loop_count))

        # 2018.11.05 Added. MySQL에서 테이블 존재 여부 확인 루틴
        # sql = "SELECT EXISTS (" \
        #       "FROM Information_schema.tables" \
        #       "WHERE table_name = 'gathering_goods' AND table_schema = 'PowerMes')" \
        #       "AS flag"

        # sql = "SELECT COUNT(*) FROM information_schema.tables " \
        #       "WHERE table_schema = 'PowerMes' AND table_name = 'gathering_goods'"

        # 2018.11.05 Added. 파이썬에서 테이블 존재 여부 확인 루틴
        check = "SHOW TABLES LIKE 'gathering_goods'"
        # cursArrayLocal.execute(check)
        try:
            result = cursArrayLocal.execute(check)
        except:
            mySqlLocalDb, cursArrayLocal, cursDictLocal, \
            COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
            TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
            FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
            WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
            FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = connectLocalDB()
            result = cursDictLocal.execute(check)

        result = cursArrayLocal.fetchall()
        # print("first result : ", str(result), "len(result) : ", len(result))
        if len(result) == 0:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_goods(mySqlLocalDb, cursArrayLocal)
            if tf:
                pass
            else:
                print("[Gathering_Goods] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                sys.exit()
        else:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 있으면 자동 삭제 : 일반적인 경우에는 사용하지 않고,
            # 테이블 삭제하고 새로 테이블을 생성하고자 할 때만, 아래 루틴을 사용한다.
            sql = "DROP TABLE gathering_goods"
            # print("2 else sql : ", sql)
            cursArrayLocal.execute(sql)
            # print("3 else cursArrayLocal : ", cursArrayLocal)
            array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
            # print("4 array_sets_server : " + str(len(array_sets_local)))

            check = "SHOW TABLES LIKE 'gathering_goods'"
            cursArrayLocal.execute(check)
            result = cursArrayLocal.fetchall()
            # print("5 else result : ", str(result), "len(result) : ", len(result))
            if len(result) == 0:
                pass
                # print("6 : Local 제품 테이블(gathering_goods) 존재 확인 완료! ")
                # sleep(1)  # 10분 = 600
                # sys.exit()
            else:
                pass
                # print("7 : Local 제품 테이블(gathering_goods) 존재 확인 실패! ")
                # sleep(1)  # 10분 = 600
                # sys.exit()

            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_goods(mySqlLocalDb, cursArrayLocal)
            # print("8 gathering_goods 테이블 생성 : sql : ", sql)
            # print("9 gathering_goods 테이블 생성 : tf : ", tf)
            # if len(result) == 0:
            if tf:
                pass
            else:
                # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
                sql, tf = creating_gathering_goods(mySqlLocalDb, cursArrayLocal)
                # print("11 gathering_goods 테이블 생성 : sql : ", sql)
                # print("12 gathering_goods 테이블 생성 : tf : ", tf)
                if tf:
                    pass
                else:
                    # print("13 [Gathering_Goods] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                    sys.exit()

        user_id = USER1
        today_ymd = datetime.date.today()
        # print("today_ymd Type : " + str(type(today_ymd)) + ", 값 : " + str(today_ymd))
        # today_ymd_string = datetime.date.today().strftime("%y%m%d")
        # print("today_ymd_string Type : " + str(type(today_ymd_string)) + ", 값 : " + str(today_ymd_string))

        # 2018.08.09 먼저 "Local.PowerMes.gathering_goods" 테이블의 기존 자료를 모두 삭제한다.
        # 아마도 "Foreign Key" 세팅으로 삭제가 안 되는 것 같은디, 그래서 그냥
        # "code"를 기준으로 먼저 찾게 하고, 없는 "품목"만 "Insert" 하게 한다.
        sql = "Delete From gathering_goods"
        # print(" : 삭제 sql : ", sql)
        # Where code=%s"
        # value = '8000010001'
        # cursDictLocal.execute(sql, value)
        cursDictLocal.execute(sql)
        try:
            mySqlLocalDb.commit()
            print(" : Local 제품 테이블에서 삭제 성공 XXXXXXXXXXXXX! ")
            # sleep(1)  # 10분 = 600
        except:
            mySqlLocalDb.rollback()
            print(" : Local 제품 테이블에서 삭제 실패 XXXXXXXXXXXXX! ")
            # sleep(1)  # 10분 = 600

        # 2018.08.09 서버 "GoodsMaster.자산=제품 And 폐기 안된 제품"만 가져온다.
        # sql = "Select code,goods From goodsmaster Where goodsassets=%s And abolitiondate is NULL Order By code "
        sql = "Select Code,Goods,Process,Description,GoodsAssets,CodeNo,PartNo,MarkingNo,Unit,Box_Qty," \
              "Goods0,Goods1,Goods2,Goods3,Step1,Step2,Step3,Step4,Step9, CompanyId " \
              "From GoodsMaster " \
              "Where (GoodsAssets=%s or GoodsAssets=%s) And abolitiondate is NULL Order By Code "
        product = 2
        semiproduct = 3
        values = (product, semiproduct)  # 재고 자산.goodsAssets.제품 코드.

        cursArrayServer.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
        # cursDictServer.execute(sql, values)  # array_sets_server.execute() 아님에 주의.

        array_sets_server = cursArrayServer.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(get_line_no(), ", array_sets_server : ", array_sets_server)

        row_count_server = len(array_sets_server)
        # print("서버 제품 마스터 총 수 : "+str(row_count_server))
        # sleep(5)  # 10분 = 600

        if row_count_server > 0:  # if array_sets_server is not None:

            r = 0
            for row in array_sets_server:
                r = r + 1
                # print("row_count_server : "+str(r)+", row : "+str(row))
                # print("row[0] :" + str(row[0]))
                # print("row[1] :" + str(row[1]))

                # code = row['code']
                code = row[0]
                code = code.strip()
                # goods = row['goods']
                goods = row[1]
                if goods is None: goods = ""
                goods = goods.strip()

                # print("code : "+str(code))
                # print("goods : " + str(goods))
                # sleep(1)  # 10분 = 600

                process = row[2]
                if process is None: process = ""
                process = process.strip()

                description = row[3]
                if description is None: description = 0

                goods_assets = row[4]
                if goods_assets is None: goods_assets = 0

                # 2019.07.26 Added. CodeNo, PartNo, MarkingNo, Unit, Box_qty,
                # Step1, Step2, Step3, Step4, Goods0, Goods1, Goods2, Goods3 필드 추가
                code_no = row[5]
                if code_no is None: code_no = ""
                code_no = code_no.strip()
                part_no = row[6]
                if part_no is None: part_no = ""
                part_no = part_no.strip()
                marking_no = row[7]
                if marking_no is None: marking_no = ""
                marking_no = marking_no.strip()
                unit = row[8]
                box_qty = row[9]
                if box_qty is None: box_qty = 0
                goods0 = row[10]
                if goods0 is None: goods0 = 0
                goods1 = row[11]
                if goods1 is None: goods1 = 0
                goods2 = row[12]
                if goods2 is None: goods2 = 0
                goods3 = row[13]
                if goods3 is None: goods3 = 0
                step1 = row[14]
                if step1 is None: step1 = ""
                step1 = step1.strip()
                step2 = row[15]
                if step2 is None: step2 = ""
                step2 = step2.strip()
                step3 = row[16]
                if step3 is None: step3 = ""
                step3 = step3.strip()
                step4 = row[17]
                if step4 is None: step4 = ""
                step4 = step4.strip()
                step9 = row[18]
                if step9 is None: step9 = ""
                step9 = step9.strip()
                trade = row[19]
                if trade is None: trade = 0
                # trade = trade.strip()

                # 거래처 이름 가져오기
                sql = "Select language2 From gathering_trade Where id = %s Order By id "
                cursDictLocal.execute(sql, trade)
                array_sets = cursDictLocal.fetchone()  # 맨 위의 첫번째 로우 값만 필요.
                trade_name = ""
                if array_sets is None:
                    # print("array_sets is None !")
                    trade_name = ""
                else:
                    trade_name = array_sets['language2']
                # trade_text = str(trade) + " " + trade_name
                # print("trade_text : ", trade_text)

                # 로컬 자료 가져와서 검색.
                sql = "Select code From gathering_goods Where code=%s Order By code "

                cursArrayLocal.execute(sql, code)  # "작업 일자"+"회사 코드"+"생산 라인"+"주야"+"제품 코드"+"일련 번호" 검색.
                # cursArrayLocal.execute(sql)
                # array_sets = cursArrayLocal.fetchone()  # 요넘 "fetchon()" 함수는 아래 "row_count = len(array_sets)"에서 에러가 발생한다.
                # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
                array_sets = cursArrayLocal.fetchall()
                row_count = len(array_sets)
                # print("array_sets_server.count() : "+str(row_count))

                if row_count < 1:
                    # 2020.03.05 Modified. PSC.평산 창주는 [goods] 값을 [GoodsMaster.Step9] 컬럼 값을 사용한다.
                    # print("dbname0 : ", dbname0)
                    if 'PSC' in DBNAME0.upper():
                        goods = step9

                    goods = goods[:37]  # 글자 수가 너무 많으면, [좌/우] 생산 설비를 화면에 뿌릴 때, 화면이 제대로 나오질 않는다.
                    sql = "Insert Into gathering_goods " \
                          "(code,goods,process,description,goods_assets,code_no,part_no,marking_no,unit,box_qty," \
                          "goods0,goods1,goods2,goods3,step1,step2,step3,step4,step9," \
                          "trade,trade_name,user_id,modified_date)" \
                          "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s)"
                    values = (
                        code, goods, process, description, goods_assets, code_no, part_no, marking_no, unit, box_qty,
                        goods0, goods1, goods2, goods3, step1, step2, step3, step4, step9,
                        trade, trade_name, user_id, today_ymd)

                    cursArrayLocal.execute(sql, values)  # array_sets.execute() 아님에 주의.

                    try:
                        mySqlLocalDb.commit()
                        # print(code+"."+goods + " : 로컬 컴퓨터에 제품 추가 성공!!! ")
                        # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
                        # sleep(1)  # 10분 = 600

                    except:
                        mySqlLocalDb.rollback()
                        print(code + "." + goods + " : 로컬 컴퓨터에 제품 추가 실패!!! ")
                        # sleep(1)  # 10분 = 600
                        # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

        print(str(row_count_server) + " 품목의 제품을 모두 로컬 컴퓨터에 성공적으로 추가하였습니다!!! ")
        return row_count_server


def getting_groups(msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0,
                   mySqlLocalDb, cursArrayLocal, cursDictLocal, HOST1, USER1, PASS1, DBNAME1):
    if len(DBNAME0) > 1:

        loop_count = 0
        # if remoteDbConnection == 1 and localDbConnection == 1:

        loop_count += 1
        # print("loop_count : "+str(loop_count))

        # 2018.11.05 Added. MySQL에서 테이블 존재 여부 확인 루틴
        # sql = "SELECT EXISTS (" \
        #       "FROM Information_schema.tables" \
        #       "WHERE table_name = 'Gathering_Groups' AND table_schema = 'PowerMes')" \
        #       "AS flag"

        # sql = "SELECT COUNT(*) FROM information_schema.tables " \
        #       "WHERE table_schema = 'PowerMes' AND table_name = 'Gathering_Groups'"

        # 2018.11.05 Added. 파이썬에서 테이블 존재 여부 확인 루틴
        check = "SHOW TABLES LIKE 'Gathering_Groups'"
        try:
            result = cursArrayLocal.execute(check)
        except:
            mySqlLocalDb, cursArrayLocal, cursDictLocal, \
            COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
            TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
            FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
            WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
            FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = connectLocalDB()
            result = cursDictLocal.execute(check)

        result = cursArrayLocal.fetchall()

        # print("first result : ", str(result), "len(result) : ", len(result))
        if len(result) == 0:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_groups(mySqlLocalDb, cursArrayLocal)
            if tf:
                pass
            else:
                print("[Gathering_Groups] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                sys.exit()
        else:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 있으면 자동 삭제 : 일반적인 경우에는 사용하지 않고,
            # 테이블 삭제하고 새로 테이블을 생성하고자 할 때만, 아래 루틴을 사용한다.
            sql = "DROP TABLE Gathering_Groups"
            # print("2 else sql : ", sql)
            cursArrayLocal.execute(sql)
            # print("3 else cursArrayLocal : ", cursArrayLocal)
            array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
            # print("4 array_sets_server : " + str(len(array_sets_local)))

            check = "SHOW TABLES LIKE 'Gathering_Groups'"
            cursArrayLocal.execute(check)
            result = cursArrayLocal.fetchall()
            # print("5 else result : ", str(result), "len(result) : ", len(result))
            if len(result) == 0:
                pass
                # print("6 : Local 작업조 테이블(Gathering_Groups) 존재 확인 완료! ")
                # sleep(1)  # 10분 = 600
                # sys.exit()
            else:
                pass
                # print("7 : Local 작업조 테이블(Gathering_Groups) 존재 확인 실패! ")
                # sleep(1)  # 10분 = 600
                # sys.exit()

            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_groups(mySqlLocalDb, cursArrayLocal)
            # print("8 Gathering_Groups 테이블 생성 : sql : ", sql)
            # print("9 Gathering_Groups 테이블 생성 : tf : ", tf)
            # if len(result) == 0:
            if tf:
                pass
            else:
                # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
                sql, tf = creating_gathering_groups(mySqlLocalDb, cursArrayLocal)
                # print("11 Gathering_Groups 테이블 생성 : sql : ", sql)
                # print("12 Gathering_Groups 테이블 생성 : tf : ", tf)
                if tf:
                    pass
                else:
                    # print("13 [Gathering_Goods] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                    sys.exit()

        user_id = USER1
        today_ymd = datetime.date.today()
        # print("today_ymd Type : " + str(type(today_ymd)) + ", 값 : " + str(today_ymd))
        # today_ymd_string = datetime.date.today().strftime("%y%m%d")
        # print("today_ymd_string Type : " + str(type(today_ymd_string)) + ", 값 : " + str(today_ymd_string))

        # 2018.08.09 먼저 "Local.PowerMes.Gathering_Groups" 테이블의 기존 자료를 모두 삭제한다.
        # 아마도 "Foreign Key" 세팅으로 삭제가 안 되는 것 같은디, 그래서 그냥
        # "code"를 기준으로 먼저 찾게 하고, 없는 "품목"만 "Insert" 하게 한다.
        sql = "Delete From Gathering_Groups "
        # value = '8000010001'
        # cursDictLocal.execute(sql, value)
        cursDictLocal.execute(sql)
        try:
            mySqlLocalDb.commit()
            print(" : Local 작업 그룹 테이블(Gathering_Groups)에서 모든 자료 삭제 성공 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
        except:
            mySqlLocalDb.rollback()
            print(" : Local 작업 그룹 테이블(Gathering_Groups)에서 모든 자료 삭제 실패 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
            sys.exit()

        # 2018.08.09 서버 "GoodsMaster.자산=제품 And 폐기 안된 제품"만 가져온다.
        # "From GoodsMaster INNER JOIN Description ON GoodsMaster.Description = Description.Id " \
        # "WHERE GoodsMaster.GoodsAssets = %s" \
        # "ORDER BY GoodsMaster.Description "
        # sql = "Select code,goods From goodsmaster Where goodsassets=%s And abolitiondate is NULL Order By code "
        # sql = "Select Code, PaCode, Process, Language3, Team From Groups Order By Code "
        sql = "Select Groups.Code, Groups.PaCode, Groups.Process, Groups.Language3, Groups.Team, " \
              "Machine.LineCode, Machine.FaCode " \
              "From Groups INNER JOIN Machine On Groups.PaCode = Machine.Code WHERE Groups.Used = '1' " \
              "Order By Groups.Code "

        cursArrayServer.execute(sql)  # array_sets.execute() 아님에 주의.
        # cursDictServer.execute(sql, values)  # array_sets.execute() 아님에 주의.

        array_sets_server = cursArrayServer.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("array_sets_server : " + str(array_sets_server))

        row_count_server = len(array_sets_server)
        # print("서버 제품 마스터 총 수 : "+str(row_count_server))
        # sleep(1)  # 10분 = 600

        if row_count_server > 0:  # if array_sets_server is not None:

            r = 0
            for row in array_sets_server:
                r = r + 1
                # print("row_count_server : "+str(r)+", row : "+str(row))
                # print("row[0] :" + str(row[0]))
                # print("row[1] :" + str(row[1]))

                # code = row['code']
                # code = row[0]
                code = row[0].strip()
                pacode = row[1].strip()
                process = row[2].strip()
                groups = row[3].strip()
                team = row[4]  # Integer.
                linecode = row[5]  # Integer.
                facode = row[6]
                # print("code : "+str(code))
                # print("groups : " + str(groups))
                # sleep(1)  # 10분 = 600

                # 로컬 자료 가져와서 검색.
                sql = "Select Code From Gathering_Groups Where Code=%s Order By Code "

                cursArrayLocal.execute(sql, code)  # "작업 일자"+"회사 코드"+"생산 라인"+"주야"+"제품 코드"+"일련 번호" 검색.
                # cursArrayLocal.execute(sql)
                # array_sets = cursArrayLocal.fetchone()  # 요넘 "fetchon()" 함수는 아래 "row_count = len(array_sets)"에서 에러가 발생한다. 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
                array_sets = cursArrayLocal.fetchall()
                row_count = len(array_sets)
                # print("array_sets_server.count() : "+str(row_count))

                if row_count < 1:
                    # print("Insert Into groups 시작합니다.")
                    sql = "Insert Into Gathering_Groups " \
                          "(Code, PaCode, Language1, Language2, Language3, Language4, Process, Team, " \
                          "LineCode, FaCode, UserId, ModifiedDate) " \
                          "Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values = (code, pacode, groups, groups, groups, groups, process, team,
                              linecode, facode, user_id, today_ymd)

                    cursArrayLocal.execute(sql, values)  # array_sets.execute() 아님에 주의.

                    try:
                        mySqlLocalDb.commit()
                        # print(code+"."+groups + " : 로컬 컴퓨터에 공정 추가 성공!!! ")
                        # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
                        # sleep(1)  # 10분 = 600

                    except:
                        mySqlLocalDb.rollback()
                        print(code + "." + groups + " : 로컬 컴퓨터에 공정 추가 실패!!! ")
                        time.sleep(1)  # 10분 = 600
                        # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

            print(str(row_count_server) + " 전체 공정을 모두 로컬 컴퓨터에 성공적으로 추가하였습니다!!! ")
            return row_count_server


def getting_description(msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0,
                        mySqlLocalDb, cursArrayLocal, cursDictLocal, HOST1, USER1, PASS1, DBNAME1):
    if len(DBNAME0) > 1:

        loop_count = 0
        # if remoteDbConnection == 1 and localDbConnection == 1:

        loop_count += 1
        # print("loop_count : "+str(loop_count))

        # 2018.11.05 Added. MySQL에서 테이블 존재 여부 확인 루틴
        # sql = "SELECT EXISTS (" \
        #       "FROM Information_schema.tables" \
        #       "WHERE table_name = 'Gathering_Description' AND table_schema = 'PowerMes')" \
        #       "AS flag"

        # sql = "SELECT COUNT(*) FROM information_schema.tables " \
        #       "WHERE table_schema = 'PowerMes' AND table_name = 'Gathering_Description'"

        # 2018.11.05 Added. 파이썬에서 테이블 존재 여부 확인 루틴
        check = "SHOW TABLES LIKE 'Gathering_Description'"
        # cursArrayLocal.execute(check)
        try:
            result = cursArrayLocal.execute(check)
        except:
            mySqlLocalDb, cursArrayLocal, cursDictLocal, \
            COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, BOUNCE_TIME, SLEEP_TIME, \
            TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
            FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
            WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
            FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE, SERIALPORT = connectLocalDB()
            result = cursDictLocal.execute(check)
        result = cursArrayLocal.fetchall()
        # print("getting_description first result : ", str(result), "len(result) : ", len(result))
        if len(result) == 0:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_description(mySqlLocalDb, cursArrayLocal)
            if tf:
                pass
            else:
                print("[품명 테이블(Description)] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                # sys.exit()
        else:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 있으면 자동 삭제 : 일반적인 경우에는 사용하지 않고,
            # 테이블 삭제하고 새로 테이블을 생성하고자 할 때만, 아래 루틴을 사용한다.
            sql = "DROP TABLE Gathering_Description"
            # print("2 else sql : ", sql)
            cursArrayLocal.execute(sql)
            # print("3 else cursArrayLocal : ", cursArrayLocal)
            array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
            # print("4 array_sets_server : " + str(len(array_sets_local)))

            check = "SHOW TABLES LIKE 'Gathering_Description'"
            cursArrayLocal.execute(check)
            result = cursArrayLocal.fetchall()
            # print("5 else result : ", str(result), "len(result) : ", len(result))
            if len(result) == 0:
                pass
                # print("6 : Local 품명 테이블(Gathering_Description) 존재 확인 완료! ")
                # sleep(1)  # 10분 = 600
            else:
                pass
                # print("7 : Local 품명 테이블(Gathering_Description) 존재 확인 실패! ")
                # sleep(1)  # 10분 = 600

            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_description(mySqlLocalDb, cursArrayLocal)
            # print("8 Gathering_Description 테이블 생성 : sql : ", sql)
            # print("9 Gathering_Description 테이블 생성 : tf : ", tf)
            # if len(result) == 0:
            if tf:
                pass
            else:
                # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
                sql, tf = creating_gathering_description(mySqlLocalDb, cursArrayLocal)
                # print("11 Gathering_Description 테이블 생성 : sql : ", sql)
                # print("12 Gathering_Description 테이블 생성 : tf : ", tf)
                if tf:
                    pass
                else:
                    pass
                    # print("13 [Gathering_Description] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                    # sys.exit()

        user_id = USER1
        today_ymd = datetime.date.today()
        # print("today_ymd Type : " + str(type(today_ymd)) + ", 값 : " + str(today_ymd))
        # today_ymd_string = datetime.date.today().strftime("%y%m%d")
        # print("today_ymd_string Type : " + str(type(today_ymd_string)) + ", 값 : " + str(today_ymd_string))

        # 2018.08.09 먼저 "Local.PowerMes.Gathering_Description" 테이블의 기존 자료를 모두 삭제한다.
        # 아마도 "Foreign Key" 세팅으로 삭제가 안 되는 것 같은디, 그래서 그냥
        # "code"를 기준으로 먼저 찾게 하고, 없는 "품목"만 "Insert" 하게 한다.
        sql = "Delete From Gathering_Description"
        # Where code=%s"
        # value = '8000010001'
        # cursDictLocal.execute(sql, value)
        cursDictLocal.execute(sql)
        try:
            mySqlLocalDb.commit()
            print(" : Local 품명 테이블(Descrition)에서 모든 자료 삭제 성공 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
        except:
            mySqlLocalDb.rollback()
            print(" : Local 품명 테이블(Description)에서 모든 자료 삭제 실패 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
            sys.exit()

        # 2018.08.09 서버 "GoodsMaster.품명 1개 and 자산=제품"만 가져온다.
        # sql = "Select ProductByDayPlanData.ProducingOrderNo, ProductByDayPlanData.Code, GoodsMaster.Goods " \
        #       "From ProductByDayPlanData " \
        #       "Inner Join GoodsMaster On ProductByDayPlanData.Code = GoodsMaster.Code " \
        #       "Where SUBSTR(ProductByDayPlanData.producingorderno,1,15)=%s " \
        #       "Order By ProductByDayPlanData.producingorderno"

        # 아래 1.번 또는 2.번 모두 동일한 값으로 검색된다.
        # 1.
        sql = "Select DISTINCT GoodsMaster.Description, Description.Language2, Description.Language3, " \
              "GoodsMaster.Process, GoodsMaster.GoodsAssets " \
              "From GoodsMaster INNER JOIN Description ON GoodsMaster.Description = Description.Id " \
              "WHERE GoodsMaster.GoodsAssets = %s or GoodsMaster.GoodsAssets = %s" \
              "ORDER BY GoodsMaster.Description "
        # 2.
        # sql = "Select DISTINCT GoodsMaster.Description, GoodsMaster.GoodsAssets, Description.Language3 " \
        #       "From GoodsMaster,Description " \
        #       "WHERE GoodsMaster.Description = Description.Id AND GoodsMaster.GoodsAssets = %s " \
        #       "ORDER BY GoodsMaster.Description "

        product = 2
        semiproduct = 3
        values = (product, semiproduct)  # 재고 자산.goodsAssets.제품/반제품 코드.

        cursArrayServer.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
        # cursDictServer.execute(sql, values)  # array_sets_server.execute() 아님에 주의.

        array_sets_server = cursArrayServer.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("array_sets_server : " + str(array_sets_server))

        # 2020.12.17 Conclusion. AutoIncreased = 1 : 자동 증가 값이 [ID] 값을 [1]부터 출발, 즉 초기화.
        # cursArrayServer.execute("Alter Table pp_DayTimeLine Auto_Increment=1")

        row_count_server = len(array_sets_server)
        print(get_line_no(), ", 서버 품명 총 수 : " + str(row_count_server) + "\n")
        # sleep(1)  # 10분 = 600

        if row_count_server > 0:  # if array_sets_server is not None:

            r = 0
            for row in array_sets_server:
                # r = r + 1
                # print("row_count_server : "+str(r)+", row : "+str(row))
                # print("row[0] :" + str(row[0]))
                # print("row[1] :" + str(row[1]))

                # code = row['code']
                description_id = row[0]
                # description_id = description_id.strip()
                # goods = row['goods']
                description_name = row[1]
                description_name = description_name.strip()
                description_name_chn = row[2]
                description_name_chn = description_name.strip()

                process = row[3]
                # print("\nprocess : " + str(process))
                if process is None:
                    process = ""
                else:
                    process = process.strip()
                # print("\nprocess : " + str(process) + "\n")

                goods_assets_id = row[4]
                # print("\ngoods_assets_id : %s\n" % goods_assets_id)

                # print("code : "+str(code))
                # print("goods : " + str(goods))
                # sleep(1)  # 10분 = 600

                # 로컬 자료 가져와서 검색.
                sql = "Select Id From Gathering_Description Where Id=%s Order By Id "

                cursArrayLocal.execute(sql, description_id)  #
                # cursArrayLocal.execute(sql)
                # array_sets = cursArrayLocal.fetchone()  # 요넘 "fetchon()" 함수는 아래 "row_count = len(array_sets)"에서 에러가 발생한다.
                # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
                array_sets = cursArrayLocal.fetchall()
                row_count = len(array_sets)
                # print("array_sets_server.count() : "+str(row_count))

                if row_count < 1:
                    # print("Insert Into gathering_data 시작합니다.")

                    sql = "Insert Into Gathering_Description (Id, Language1, Language2, Language3, Language4," \
                          "Process, GoodsAssets, UserId, ModifiedDate) " \
                          "Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (description_id, description_name, description_name, description_name, description_name,
                              process, goods_assets_id, user_id, today_ymd)

                    cursArrayLocal.execute(sql, values)  # array_sets.execute() 아님에 주의.
                    # print(str(description_id) + "." + description_name + " : 로컬 컴퓨터에 품명 추가 성공!!! ")

                try:
                    mySqlLocalDb.commit()
                    print(str(description_id) + "." + description_name + " : 로컬 컴퓨터에 Commit 성공!!! ")
                    # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
                    # sleep(1)  # 10분 = 600

                except:
                    mySqlLocalDb.rollback()
                    print(str(description_id) + "." + description_name + " : 로컬 컴퓨터에 품명 추가 실패!!! ")
                    time.sleep(1)  # 10분 = 600
                    # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

            print(str(row_count_server) + "개 품명 모두 로컬 컴퓨터에 성공적으로 추가하였습니다!\n")
            return row_count_server


def getting_equipmentofproduct(msSqlServerDb, cursArrayServer, HOST0, USER0, PASS0, DBNAME0,
                               mySqlLocalDb, cursArrayLocal, cursDictLocal, HOST1, USER1, PASS1, DBNAME1):
    if len(DBNAME0) > 1:

        loop_count = 0
        # if remoteDbConnection == 1 and localDbConnection == 1:

        loop_count += 1
        # print("loop_count : "+str(loop_count))

        # 2018.11.05 Added. MySQL에서 테이블 존재 여부 확인 루틴
        # sql = "SELECT EXISTS (" \
        #       "FROM Information_schema.tables" \
        #       "WHERE table_name = 'Gathering_EquipmentOfProduct' AND table_schema = 'PowerMes')" \
        #       "AS flag"

        # sql = "SELECT COUNT(*) FROM information_schema.tables " \
        #       "WHERE table_schema = 'PowerMes' AND table_name = 'Gathering_EquipmentOfProduct'"

        # 2018.11.05 Added. 파이썬에서 테이블 존재 여부 확인 루틴
        check = "SHOW TABLES LIKE 'Gathering_EquipmentOfProduct'"
        cursArrayLocal.execute(check)
        result = cursArrayLocal.fetchall()
        # print("getting_equipmentofproduct first result : ", str(result), "len(result) : ", len(result))
        if len(result) == 0:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_description(mySqlLocalDb, cursArrayLocal)
            if tf:
                pass
            else:
                print("[Local 설비별 생산품 등록 테이블(Gathering_EquipmentOfProduct) 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                # sys.exit()
        else:
            # 2018.11.05 Added. 테이블 존재 여부 확인, 있으면 자동 삭제 : 일반적인 경우에는 사용하지 않고,
            # 테이블 삭제하고 새로 테이블을 생성하고자 할 때만, 아래 루틴을 사용한다.
            sql = "DROP TABLE Gathering_EquipmentOfProduct"
            # print("2 else sql : ", sql)
            cursArrayLocal.execute(sql)
            # print("3 else cursArrayLocal : ", cursArrayLocal)
            array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
            # print("4 array_sets_server : " + str(len(array_sets_local)))

            check = "SHOW TABLES LIKE 'Gathering_EquipmentOfProduct'"
            cursArrayLocal.execute(check)
            result = cursArrayLocal.fetchall()
            # print("5 else result : ", str(result), "len(result) : ", len(result))
            if len(result) == 0:
                pass
                # print("6 : Local 설비별 생산품 등록 테이블(Gathering_EquipmentOfProduct) 존재 확인 완료! ")
                # sleep(1)  # 10분 = 600
            else:
                pass
                # print("7 : Local 설비별 생산품 등록 테이블(Gathering_EquipmentOfProduct) 존재 확인 실패! ")
                # sleep(1)  # 10분 = 600

            # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
            sql, tf = creating_gathering_equipmentofproduct(mySqlLocalDb, cursArrayLocal)
            # print("8 Gathering_EquipmentOfProduct 테이블 생성 : sql : ", sql)
            # print("9 Gathering_EquipmentOfProduct 테이블 생성 : tf : ", tf)
            # if len(result) == 0:
            if tf:
                pass
            else:
                # 2018.11.05 Added. 테이블 존재 여부 확인, 없으면 자동 생성.
                sql, tf = creating_gathering_equipmentofproduct(mySqlLocalDb, cursArrayLocal)
                # print("11 Gathering_Description 테이블 생성 : sql : ", sql)
                # print("12 Gathering_Description 테이블 생성 : tf : ", tf)
                if tf:
                    pass
                else:
                    pass
                    # print("13 [Gathering_EquipmentOfProduct] 테이블 생성에 실패하였습니다. 다시 확인하시오!")
                    # sys.exit()

        user_id = USER1
        today_ymd = datetime.date.today()
        # print("today_ymd Type : " + str(type(today_ymd)) + ", 값 : " + str(today_ymd))
        # today_ymd_string = datetime.date.today().strftime("%y%m%d")
        # print("today_ymd_string Type : " + str(type(today_ymd_string)) + ", 값 : " + str(today_ymd_string))

        # 2018.08.09 먼저 "Local.PowerMes.Gathering_Description" 테이블의 기존 자료를 모두 삭제한다.
        # 아마도 "Foreign Key" 세팅으로 삭제가 안 되는 것 같은디, 그래서 그냥
        # "code"를 기준으로 먼저 찾게 하고, 없는 "품목"만 "Insert" 하게 한다.
        sql = "Delete From Gathering_EquipmentOfProduct"
        # Where code=%s"
        # value = '8000010001'
        # cursDictLocal.execute(sql, value)
        cursDictLocal.execute(sql)
        try:
            mySqlLocalDb.commit()
            print(" : Local 설비별 생산품 등록 테이블(EquipmentOfProduct)에서 모든 자료 삭제 성공 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
        except:
            mySqlLocalDb.rollback()
            print(" : Local 설비별 생산품 등록 테이블(EquipmentOfProduct)에서 모든 자료 삭제 실패 XXXXXXXXXXXXX! ")
            time.sleep(1)  # 10분 = 600
            sys.exit()

        # 2018.08.09 서버 "GoodsMaster.자산=제품 And 폐기 안된 제품"만 가져온다.
        # "From GoodsMaster INNER JOIN Description ON GoodsMaster.Description = Description.Id " \
        # "WHERE GoodsMaster.GoodsAssets = %s" \
        # "ORDER BY GoodsMaster.Description "
        # sql = "Select code,goods From goodsmaster Where goodsassets=%s And abolitiondate is NULL Order By code "
        # sql = "Select Code, PaCode, Process, Language3, Team From Groups Order By Code "
        sql = "Select Process, LineCode, Code, FaCode, BarcodeInfo, BeInUse, DescriptionEquipment, " \
              "CreatedUser, ModifiedUser From EquipmentOfProduct Order By Process, LineCode, Code "

        cursArrayServer.execute(sql)  # array_sets.execute() 아님에 주의.
        # cursDictServer.execute(sql, values)  # array_sets.execute() 아님에 주의.

        array_sets_server = cursArrayServer.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("array_sets_server : " + str(array_sets_server))

        row_count_server = len(array_sets_server)
        # print("서버 제품 마스터 총 수 : "+str(row_count_server))
        # sleep(1)  # 10분 = 600

        if row_count_server > 0:  # if array_sets_server is not None:

            r = 0
            for row in array_sets_server:
                r = r + 1
                # print("row_count_server : "+str(r)+", row : "+str(row))
                # print("row[0] :" + str(row[0]))
                # print("row[1] :" + str(row[1]))

                # code = row['code']
                # code = row[0]
                process = row[0]
                if process is not None:
                    process = process.strip()
                linecode = row[1]
                code = row[2]
                if code is not None:
                    code = code.strip()
                facode = row[3]
                if facode is not None:
                    facode = facode.strip()
                barcodeinfo = row[4]
                # print("1 barcodeinfo : ", barcodeinfo)
                if barcodeinfo is not None:
                    barcodeinfo = barcodeinfo.strip()
                    # print("2 barcodeinfo : ", barcodeinfo)
                beinuse = row[5]
                descriptionequipment = row[6]
                if descriptionequipment is not None:
                    descriptionequipment = descriptionequipment.strip()
                createduser = row[7]
                if createduser is not None:
                    createduser = createduser.strip()
                modifieduser = row[8]
                if modifieduser is not None:
                    modifieduser = modifieduser.strip()
                # print("code : "+str(code))
                # sleep(1)  # 10분 = 600

                # 로컬 자료 가져와서 검색.
                sql = "Select Process,LineCode,Code From Gathering_EquipmentOfProduct " \
                      "Where Process=%s AND LineCode=%s AND Code=%s Order By Process,LineCode,Code "

                values = (process, linecode, code)
                cursArrayLocal.execute(sql, values)  # "작업 일자"+"회사 코드"+"생산 라인"+"주야"+"제품 코드"+"일련 번호" 검색.
                # cursArrayLocal.execute(sql)
                # array_sets = cursArrayLocal.fetchone()  # 요넘 "fetchon()" 함수는 아래 "row_count = len(array_sets)"에서 에러가 발생한다. 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
                array_sets = cursArrayLocal.fetchall()
                row_count = len(array_sets)
                # print("array_sets_server.count() : "+str(row_count))

                if row_count < 1:
                    # print("Insert Into Gathering_EquipmentOfProduct 시작합니다.")
                    sql = "Insert Into Gathering_EquipmentOfProduct " \
                          "(Process, LineCode, Code, FaCode, BarcodeInfo, BeInUse, DescriptionEquipment, " \
                          "CreatedUser, ModifiedUser) Values (%s,%s,%s,%s,%s, %s,%s,%s,%s)"
                    values = (process, linecode, code, facode, barcodeinfo, beinuse, descriptionequipment,
                              createduser, modifieduser)

                    cursArrayLocal.execute(sql, values)  # array_sets.execute() 아님에 주의.

                    try:
                        mySqlLocalDb.commit()
                        # print(process + "." + linecode + "." + code + " : 로컬 컴퓨터에 설비별 생산품 추가 성공!!! ")
                        # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
                        # sleep(1)  # 10분 = 600

                    except:
                        mySqlLocalDb.rollback()
                        print(process + "." + linecode + "." + code + " : 로컬 컴퓨터에 설비별 생산품 추가 실패!!! ")
                        time.sleep(1)  # 10분 = 600
                        # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

            print(str(row_count_server) + " 전체 공정을 모두 로컬 컴퓨터에 성공적으로 추가하였습니다!!! ")
            return row_count_server


# 2022.01.27 Added. 전체 테이블명 가져오기
def getAllTableName(msSqlServerDb, cursArrayServer, selected_table_name):
    # print("f_common.getAllTableName... msSqlServerDb: ", msSqlServerDb)
    # print("f_common.getAllTableName... cursArrayServer: ", cursArrayServer)
    print(get_line_no(), "getAllTableName... selected_table_name: ", selected_table_name)
    tableName = []
    try:
        # INFORMATION_SCHEMA.TABLE_CONSTRAINTS: PK_xxx, 즉 CONSTRAINT_NAME 컬럼이 지정된 테이블만의 명세.
        # INFORMATION_SCHEMA.TABLES: 모든 테이블 명세.
        if selected_table_name == "ALL":
            sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
        else:
            sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = %s "

        # sql = "SELECT NAME FROM SYS.TABLES "  # 사용자 테이블 정보만 보기.
        # view = "SELECT * FROM SYS.VIEWS "  # 사용자 뷰 정보만 보기.
        # proc = "SELECT * FROM SYS.PROCEDURES "  # 사용자 프로시져 정보만 보기.
        # index = "SELECT OBJECT_NAME(object_id) 테이블명, name 인덱스명, index_id 인덱스아이디,
        #                     type 인덱스타입코드, type_desc 인덱스타입명,
        #                     CASE WHEN is_unique = 1 THEN 'Y' ELSE 'N' END Unique유무,
        #                     CASE WHEN is_primary_key = 1 THEN 'Y' ELSE 'N' END PK유무
        #        FROM    sys.indexes "  # index 정보만 보기.
        # trigger = "SELECT OBJECT_NAME(parent_id) 테이블명,object_id 개체아이디,name 트리거명,
        #                      CASE WHEN is_disabled = 1 THEN 'Y' ELSE 'N' END 비활성화유무
        #         FROM  sys.triggers "  # 트리거 정보만 보기.
        # index_column = "SELECT OBJECT_NAME(A.object_id) 테이블명,B.name 인덱스명,
        #              COL_NAME(A.Object_id,A.column_id) 컬럼명,A.key_ordinal 인덱스순서,
        #              CASE WHEN is_descending_key = 1 THEN 'desc' ELSE 'asc' END 정렬
        #              FROM    sys.index_columns A
        #              INNER JOIN sys.indexes B
        #              ON  B.object_id  = A.object_id
        #              AND  B.index_id  = A.index_id "  # 인덱스 컬럼 정보 보기.
        # primary_key_and_unique_info = " SELECT OBJECT_NAME(A.parent_object_id) 테이블명,A.object_id 개체코드,A.name 개체명
        #                         FROM    sys.key_constraints A "  # Primary Key 또는 Unique 제약 조건 정보 보기.
        # 프로시져, 뷰, 함수 개체의 내용 보기.
        # procedure_view_function_contents = "SELECT OBJECT_NAME(id) 개체명,colid 내용순서, text FROM sys.syscomments "
        # 자동 증가 컬럼 얻기.
        # https://blog9.tistory.com/39

        if selected_table_name == "ALL":
            result = cursArrayServer.execute(sql)
        else:
            result = cursArrayServer.execute(sql, selected_table_name)

        results = cursArrayServer.fetchall()
        if len(results) > 0:  # results 타입이 튜플임에 주의. <class 'list'>
            # print("getAllTableName:table name: ", results, ", type(results): ", type(results))
            for i, tn in enumerate(results):  # results 타입이 튜플임에 주의. <class 'tuple'>
                # print("getAllTableName:table name: ", tn, ", type(tn): ", type(tn), ", i: ", i)
                # 먼저 튜플을 리스토로 변환.
                tnList = list(tn)

                # if i < 10:
                #     print("f_common.getAllTableInfo:table i: ", i, ", name: ", tnList, ", type(tnList): ", type(tnList))

                # 리스트이므로, 테이블명만 따로 뽑아 내야 한다. 현재 값이 ['TableName'] 이런 형식이다.
                # tableName = re.sub('[^A-Za-z0-9]', 'x', tnList)  # 이건 [문자열]일 때, [특수 문자]를 제거하는 것.
                # print("getAllTableName:table name: ", tableName, ", i: ", i)
                tableName.append(tnList[0])  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
        else:
            print("현재 데이터베이스에는 테이블이 1개도 없습니다!")
    except:
        pass

    if len(tableName) > 1:  # 1개 까지도 sorting 필요 없음.
        tableName.sort()

    return tableName


# 2022.01.28 Added. 전체 테이블 및 컬럼 정보 가져오기
def getAllTableColumnsInfo(msSqlServerDb, cursArrayServer, selected_table_name):
    # print("f_common:getAllTableColumnsInfo... msSqlServerDb: ", msSqlServerDb)
    # print("f_common:getAllTableColumnsInfo... cursArrayServer: ", cursArrayServer)
    tableColumnsInfo = []
    try:
        # INFORMATION_SCHEMA.COLUMNS: 모든 테이블 컬럼 명세.
        # ORDINAL_POSITION: 컬럼 순서
        # COLUMN_DEFAULT: 디폴트 값
        # IS_NULLABLE: NULL 값 허용 여부: YES/NO
        # DATA_TYPE: 컬럼 타입: [int, datetime, nvarchar, varchar, char, nchar, numeric, decamal]
        # CHARACTER_MAXMUM_LENGTH: 문자형 타입일 때, 최대 길이
        # NUMERIC_PRECISION: 숫자형 타입일 때, 컬럼 길이
        # NUMERIC_SCALE: 숫자형 타입일 때, 소수점 길이
        # CHARACTER_SET_NAME: 유니 코드 형식: [UNICODE, cp949]
        # COLLATION_NAME: 한글 완성형 형식: Korean_Wnssung_CLAS
        # sql = "SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, COLUMN_DEFAULT, IS_NULLABLE, DATA_TYPE, " \
        #       "CHARACTER_MAXMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE, CHARACTER_SET_NAME, COLLATION_NAME " \
        #       "FROM INFORMATION_SCHEMA.COLUMNS "
        if selected_table_name == "ALL":
            sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS "
        else:
            sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s "
        # sql = "SELECT * FROM SYS.COLUMNS "  # 특정 테이블 정보 보기.
        if selected_table_name == "ALL":
            result = cursArrayServer.execute(sql)
        else:
            result = cursArrayServer.execute(sql, selected_table_name)

        # print("f_common:getAllTableColumnsInfo: result", result, ", type(result): ", type(result))
        results = cursArrayServer.fetchall()
        if len(results) > 0:  # results 타입이 튜플임에 주의. <class 'list'>
            # print("f_common:getAllTableColumnsInfo:col: ", results, ", type(results): ", type(results))
            for i, col in enumerate(results):  # results 타입이 튜플임에 주의. <class 'tuple'>

                # if i < 10:
                #     print("f_common:getAllTableColumnsInfo: i: ", i, ", col: ", col, ", type(col): ", type(col))

                # 먼저 튜플을 리스토로 변환.
                colList = list(col)
                # 리스트이므로, 테이블명만 따로 뽑아 내야 한다. 현재 값이 ['ColumnName'] 이런 형식이다.
                # colName = re.sub('[^A-Za-z0-9]', 'x', tnList)  # 이건 [문자열]일 때, [특수 문자]를 제거하는 것.
                # print("getAllTableColumnsInfo:col name: ", colName, ", i: ", i)
                # tableColumnsInfo.append(colList[0])  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
                tableColumnsInfo.append(colList)  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
        else:
            print("f_common:getAllTableColumnsInfo 현재 데이터베이스에는 테이블이 1개도 없습니다!")
    except:
        pass

    return tableColumnsInfo


# 2022.02.15 Added. Primary Key, 프라이머리 키 컬럼을 찾는다.
# [PowErpPsc].[INFORMATION_SCHEMA].[KEY_COLUMN_USAGE] 테이블의 [TABLE_NAME], [COLUMN_NAME], [ORDINAL_POSITION] 이상,
# 3개 컬럼 값을 가져온다.
def getAllTablePrimaryKeyColumnsInfo(msSqlServerDb, cursArrayServer):
    # print("f_common:getAllTablePrimaryKeyColumnsInfo... msSqlServerDb: ", msSqlServerDb)
    # print("f_common:getAllTablePrimaryKeyColumnsInfo... cursArrayServer: ", cursArrayServer)
    tablePrimaryKeyColumnsInfo = []
    try:
        sql = "SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, CONSTRAINT_NAME " \
              "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE ORDER BY TABLE_NAME, ORDINAL_POSITION"
        # s = "SELECT OBJECT_NAME(A.parent_object_id) 테이블명,A.object_id 개체코드,A.name 개체명 FROM sys.key_constraints A"
        # sql = "SELECT TABLE_NAME(), COLUMN_NAME(), ORDINAL_POSITION(), CONSTRAINT_NAME() " \
        #       "FROM sys.key_constraints A ORDER BY A.parent_object_id, ORDINAL_POSITION"
        result = cursArrayServer.execute(sql)
        # print("f_common:getAllTablePrimaryKeyColumnsInfo: result", result, ", type(result): ", type(result))
        results = cursArrayServer.fetchall()
        if len(results) > 0:  # results 타입이 튜플임에 주의. <class 'list'>
            # print("f_common:getAllTablePrimaryKeyColumnsInfo:col: ", results, ", type(results): ", type(results))
            for i, col in enumerate(results):  # results 타입이 튜플임에 주의. <class 'tuple'>

                # if i < 10:
                #     print("f_common:getAllTablePrimaryKeyColumnsInfo: i: ", i, ", col: ", col, ", type(col): ", type(col))

                # 먼저 튜플을 리스토로 변환.
                colList = list(col)
                # 리스트이므로, 테이블명만 따로 뽑아 내야 한다. 현재 값이 ['ColumnName'] 이런 형식이다.
                # colName = re.sub('[^A-Za-z0-9]', 'x', tnList)  # 이건 [문자열]일 때, [특수 문자]를 제거하는 것.
                # print("getAllTablePrimaryKeyColumnsInfo:col name: ", colName, ", i: ", i)
                # tableColumnsInfo.append(colList[0])  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
                tablePrimaryKeyColumnsInfo.append(colList)  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
        else:
            print("f_common:getAllTablePrimaryKeyColumnsInfo 현재 데이터베이스에는 테이블이 1개도 없습니다!")
    except:
        pass

    return tablePrimaryKeyColumnsInfo


# 2022.02.15 Added. Auto_Increment, 자동 증가 값이 있는 컬럼을 찾는다. 2개 테이블 필요.
#    [PowErpPsc].[뷰].[시스템뷰].[sys].[key_constraints] 테이블의 컬럼 [name]에서,
#    [PK_테이블명]을 찾아서, 컬럼 [parent_object_id] 값을 가져와,
#    [PowErpPsc].[뷰].[시스템뷰].[sys].[identity_columns] 테이블의 컬럼 [object_id]에서 동일한 값을 찾는다.
#    만약 찾는다면, [identity_columns].[name] 값과 컬럼명을, 확인하는 차원에서 한번 더 체크하고,
#    [identity_columns].[seed_value], [identity_columns].[increment_value], [identity_columns].[last_value] 3개 컬럼 값을
#    가져온다.
def getAllTableAutoIncrementColumnsInfo(msSqlServerDb, cursArrayServer):
    # print("f_common:getAllTableAutoIncrementColumnsInfo... msSqlServerDb: ", msSqlServerDb)
    # print("f_common:getAllTableAutoIncrementColumnsInfo... cursArrayServer: ", cursArrayServer)
    tableAutoIncrementColumn = []
    try:
        sql = "SELECT object_id, name, parent_object_id, unique_index_id FROM sys.key_constraints ORDER BY name"
        # sql = "SELECT B.name AS [Table], A.name AS [Colum] FROM syscolumns A " \
        #       "JOIN sysobjects B ON B.id = A.id WHERE A.status = 128"
        # ===> Identity 컬럼은 0x80 값을 갖는다. AND B.name NOT LIKE 'queue_messages_%' ORDER BY B.name ASC ,A.name ASC;
        # 출처: https://icodebroker.tistory.com/1719 [ICODEBROKER]

        result = cursArrayServer.execute(sql)
        # print("f_common:getAllTableAutoIncrementColumnsInfo: result", result, ", type(result): ", type(result))
        results = cursArrayServer.fetchall()
        if len(results) > 0:  # results 타입이 튜플임에 주의. <class 'list'>
            # print("f_common:getAllTableAutoIncrementColumnsInfo:col: ", results, ", type(results): ", type(results))
            for i, col in enumerate(results):  # results 타입이 튜플임에 주의. <class 'tuple'>
                # if "PK_T_KAOQIN_RECORD" in col:  # 대소문자 구분 때문에, 이렇게는 검색이 안 되네...
                #     print(get_line_no(), "getAllTableAutoIncrementColumnsInfo: i: ", i, ", col: ", col,
                #           ", type(col): ", type(col))
                # if i < 100:
                #     print(get_line_no(), "getAllTableAutoIncrementColumnsInfo: i: ", i, ", col: ", col,
                #           ", type(col): ", type(col))

                # 먼저 튜플을 리스토로 변환.
                colList = list(col)
                # 리스트이므로, 테이블명만 따로 뽑아 내야 한다. 현재 값이 ['ColumnName'] 이런 형식이다.
                # colName = re.sub('[^A-Za-z0-9]', 'x', tnList)  # 이건 [문자열]일 때, [특수 문자]를 제거하는 것.
                # print("getAllTableAutoIncrementColumnsInfo:col name: ", colName, ", i: ", i)
                # tableColumnsInfo.append(colList[0])  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
                tableAutoIncrementColumn.append(colList)  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
        else:
            print("f_common:getAllTableAutoIncrementColumnsInfo 현재 데이터베이스에는 테이블이 1개도 없습니다!")
    except:
        pass

    tableAutoIncrementColumnInfo = []
    try:
        sql = "SELECT object_id, name, seed_value, increment_value, last_value " \
              "FROM sys.identity_columns ORDER BY object_id"
        result = cursArrayServer.execute(sql)
        # print("f_common:getAllTableAutoIncrementColumnsInfo: result", result, ", type(result): ", type(result))
        results = cursArrayServer.fetchall()
        if len(results) > 0:  # results 타입이 튜플임에 주의. <class 'list'>
            # print("f_common:getAllTableAutoIncrementColumnsInfo:col: ", results, ", type(results): ", type(results))
            for i, col in enumerate(results):  # results 타입이 튜플임에 주의. <class 'tuple'>

                # if i < 100:
                #     print("f_common:getAllTableAutoIncrementColumnsInfo: i: ", i, ", col: ", col, ", type(col): ", type(col))

                # 먼저 튜플을 리스토로 변환.
                colList = list(col)
                # 리스트이므로, 테이블명만 따로 뽑아 내야 한다. 현재 값이 ['ColumnName'] 이런 형식이다.
                # colName = re.sub('[^A-Za-z0-9]', 'x', tnList)  # 이건 [문자열]일 때, [특수 문자]를 제거하는 것.
                # print("getAllTableAutoIncrementColumnsInfo:col name: ", colName, ", i: ", i)
                # tableColumnsInfo.append(colList[0])  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
                tableAutoIncrementColumnInfo.append(colList)  # 1개만 있는 리스트이므로 [0]번 값이 곧 [테이블 이름] 임에 주의.
        else:
            print("f_common:getAllTableAutoIncrementColumnsInfo 현재 데이터베이스에는 테이블이 1개도 없습니다!")
    except:
        pass

    return tableAutoIncrementColumn, tableAutoIncrementColumnInfo


# 2022.02.19 Added. Database.데이터베이스 삭제.
def dropLocalDatabase(mySqlLocalDb, cursArrayLocal, database):
    print(get_line_no(), ".dropLocalDatabase dropDatabase: ", database)

    try:
        sql = "DROP DATABASE IF EXISTS " + database
        print(get_line_no(), ".dropLocalDatabas sql : ", sql)
        cursArrayLocal.execute(sql)
        print(get_line_no(), ".dropLocalDatabas cursArrayLocal : ", cursArrayLocal)
        # array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("4 f_common.py.dropLocalDatabas array_sets_server : " + str(len(array_sets_local)))
        return True
    except:
        return False


# 2022.02.19 Added. Database.데이터베이스 생성.
def createLocalDatabase(mySqlLocalDb, cursArrayLocal, database):
    print(get_line_no(), ".createLocalDatabase database: ", database)

    try:
        sql = "CREATE DATABASE " + database
        print(get_line_no(), ".createLocalDatabase sql : ", sql)
        cursArrayLocal.execute(sql)
        print(get_line_no(), ".createLocalDatabase cursArrayLocal : ", cursArrayLocal)
        # array_sets_local = cursArrayLocal.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("4 f_common.py.createLocalDatabase array_sets_server : " + str(len(array_sets_local)))
        return True
    except:
        return False


# 2022.02.20 Added. 해당 테이블에 대한 자료를 모두 가져온다.
# 2022.02.20 Added. 그동안 숙원 사업이였던, MS SQL ERP DB 전체 테이블 자료를, MySql 지정한 DB 로 한방에 자료를 전환한다.
# 코딩이 완료되면, 프로그램 파일명도 [transfer_erp_all_table_data.py]로 변경한다.
def getCurrentTableData(msSqlServerDb, cursArrayServer, table, currentTableColumnsInfo):
    # print("1 f_common.py.getCurrentTableData currentTable: ", currentTable)

    table = table.upper()
    if table.upper() == "GROUPS":
        table_my = "GROUPSS"
    else:
        table_my = table

    # # 2018.11.05 Added. 파이썬에서 테이블 존재 여부 확인 루틴
    # check = "SHOW TABLES LIKE '" + currentTable + "'"
    # cursArrayServer.execute(check)
    # result = cursArrayServer.fetchall()
    # # print("result : "+str(result))

    commandSelect = "SELECT "
    columnNamesMs = []
    columnNamesMy = []
    for ii, tableColumns in enumerate(currentTableColumnsInfo):
        if ii == 0:
            sql_ms = commandSelect
            sql_my = commandSelect
        columnName = tableColumns[3].upper()
        columnIndex = tableColumns[4]
        # columnDefaultValue = tableColumns[5]  # 의미 없음, 모두 "None" 처리.
        columnNull = tableColumns[6]
        if columnNull.upper() == "NO":
            columnNull = " NOT NULL"  # 맨 앞에 Space, 공백 문자가 반드시 있어야 한다.
        else:
            columnNull = ""
        columnType = tableColumns[7]
        columnCountChr = tableColumns[8]
        columnCountNum = tableColumns[10]
        columnCountDecimal = tableColumns[12]

        if columnName == "GROUPS":
            columnNameMy = "GROUPSS"
        elif columnName == "ROW" or columnName == "ROWS":
            columnNameMy = "ROW7"
        elif columnName == "GENERATED":
            columnNameMy = "GENERATED7"
        else:
            columnNameMy = columnName

        columnNamesMs.append(columnName)
        columnNamesMy.append(columnNameMy)

        sql_ms += columnName + ", "
        sql_my += columnNameMy + ", "

    sql_ms = sql_ms[:-2]  # 마지막 Space 공백 문자와 콤마(,) 제거...
    sql_ms += " FROM " + table
    # print(get_line_no(), ".getCurrentTableData sql_ms: ", sql_ms)

    cursArrayServer.execute(sql_ms)  # array_sets.execute() 아님에 주의.
    # cursDictServer.execute(sql_ms, values)  # array_sets.execute() 아님에 주의.

    array_sets_server = cursArrayServer.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
    # print("len(array_sets_server): ", len(array_sets_server))
    # print("type(array_sets_server): ", type(array_sets_server))

    row_count_server = len(array_sets_server)
    # print("서버 제품 마스터 총 수: ", row_count_server)

    # for i, col in enumerate(array_sets_server):
    #     print("i: ", i, ", col: ", col, ", type(col): ", type(col))

    # 2020.02.20 Conclusion. columnNameMs, sql_ms 변수는 여기 함수 내부에서만 사용하고,
    # return 값은, columnNameMy, sql_my 변수를 보내서, 그것을 사용하게 해야 한다.

    sql_my = sql_my[:-2]  # 마지막 Space 공백 문자와 콤마(,) 제거...
    sql_my += " FROM " + table_my
    # print(get_line_no(), ".getCurrentTableData sql_ms: ", sql_my)

    return columnNamesMy, array_sets_server, sql_my


# 2022.02.20 Added. 해당 테이블의 자료를, MySql 동일 테이블에 저장한다.
# 2022.02.20 Added. 그동안 숙원 사업이였던, MS SQL ERP DB 전체 테이블 자료를, MySql 지정한 DB 로 한방에 자료를 전환한다.
# 코딩이 완료되면, 프로그램 파일명도 [transfer_erp_all_table_data.py]로 변경한다.
def setCurrentTableData(mySqlDb, cursArray, currentTable, columnNamesMy, array_sets_server, sql_my):
    # print("0 f_common.py.setCurrentTableData currentTable: ", currentTable)
    # print("0 f_common.py.setCurrentTableData columnNamesMy: ", columnNamesMy)
    # print("0 f_common.py.setCurrentTableData sql_my: ", sql_my)

    # 2020.02.20 Conclusion. MySql 테이블에 이미 자료가 있다면, 그 자료는 먼저 모두 삭제해야 한다.
    # 다만, Auto_increment 자동 증가 컬럼의 값들은, 그렇게 되면, MS SQL 값과 다르게 Insert 된다는 것에 주의...

    cursArray.execute(sql_my)  # array_sets.execute() 아님에 주의.

    array_sets = cursArray.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
    # print("len(array_sets): ", len(array_sets))
    # print("type(array_sets): ", type(array_sets))

    row_count = len(array_sets)
    print(get_line_no(), ".기존 로컬 테이블 로우 총 수: ", row_count)

    if row_count > 0:
        sql = "DELETE FROM " + currentTable + " "
        cursArray.execute(sql)

        try:
            mySqlDb.commit()
            print(get_line_no(), ".테이블: ", currentTable, "의 모든 자료를, 로컬 컴퓨터에 성공적으로 삭제하고, COMMIT 성공!!!")
            # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
            # sleep(1)  # 10분 = 600

        except:
            mySqlDb.rollback()
            print(get_line_no(), ".테이블: ", currentTable, "의 모든 자료의 삭제 후 COMMIT 실패!!!")
            # sleep(1)  # 10분 = 600
            # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

    commandInsert = "INSERT INTO "
    pros = ""
    for i, col in enumerate(columnNamesMy):
        if i == 0:
            sql = commandInsert + currentTable + " ("
            pros = "("
        # if col.upper() == "GROUPS":
        #     col = "GROUPSS"
        # if col.upper() == "ROW" or col.upper() == "ROWS":
        #     col = "ROW7"
        # if col.upper() == "GENERATED":
        #     col = "GENERATED7"
        sql += col + ", "
        pros += "%s, "

    # print("1 f_common.py.setCurrentTableData sql: ", sql)
    # print("1 f_common.py.setCurrentTableData pros: ", pros)
    sql = sql[:-2]  # 마지막 Space 공백 문자와 콤마(,) 제거...
    sql += " ) "
    pros = pros[:-2]  # 마지막 Space 공백 문자와 콤마(,) 제거...
    pros += " ) "
    # print("2 f_common.py.setCurrentTableData sql: ", sql)
    # print("2 f_common.py.setCurrentTableData pros: ", pros)

    sql += "VALUES " + pros
    # print("\n7 f_common.py.setCurrentTableData sql: ", sql, "\n")

    for i, data in enumerate(array_sets_server):
        # if "CW_PZH" in currentTable:
        #     print(get_line_no(), ", i: ", i, ", data: ", data)

        # 2020.02.20 Conclusion. tuple.튜플은 [추가, 수정, 삭제]가 안 되므로, 먼저 [list.리스트]로 1차 자료를 만들고,
        # [tuple_data = tuple((list_data)), 괄호가 2개임에 특히 주의]로 튜플로 만들어, sql 문장을 완성한다.
        values_list = []
        for k, val in enumerate(data):
            # if "CW_PZH" in currentTable:
            # if "MOLD" in currentTable:
            #     print("k: ", k, ", val: ", val, ", type(val): ", type(val))
            if type(val) == str:
                val = val.strip()
                if len(val) > 254:
                    # if len(val) > 124:  # utf8mb4.emoji
                    #     print(get_line_no(), " currentTable: ", currentTable, ", val: ", val[:124])
                    val = val[:254]  # MySql 은 255 까지만 사용 가능.
                    # val = val[:124]  # MySql 은 255 까지만 사용 가능. # utf8mb4.emoji
            if type(val) == bytes:
                # 2022.02.21 Conclusion. PowErpPsc.cw_pzh.pzh 컬럼에서 값이, [timestamp.날짜+시간] 값이 넘어 오는데,
                # PERP1.mold.pict1,pict2,pict3,pict4,pict5 컬럼에서 val 값은, [사진 이미지] 값이 넘어 오는 관계로,
                # MySql로 전환시 [사진 이미지] bytes 값은 변환 에러가 발생하므로, 스킵 처리한다.
                # 즉, PowErpPsc.cw_pzh.pzh 컬럼 형식은 timestamp 형식으로, 그 값의 len().크기가 [8]이고,
                # PERP1.mold.pict1,pict2... 컬럼 형식은 image 형식으로, 그 값의 len().크기가 [1827], [28778]... 이다.
                if len(val) > 8:
                    # val = None  # Null 값으로 세팅해도 되는데, 아래와 같이 [timestamp] 값으로 넣어 줬다. 아무 의미는 없다.
                    val = b'\x00\x00\x00\x00\x00\x11\x88l'
                    # print("bin: ", val, ", type(val): ", type(val), ", len(val): ", len(val))
                int_timestamp = int(binascii.hexlify(val), 16)
                # print("Hexadecimal: ", int(binascii.hexlify(val), 16))
                # datetime_millsec = datetime.datetime.fromtimestamp(int_timestamp).strftime("%Y-%m-%d %H:%M:%S %f")
                # %f, 즉 millisecond.밀리초 형식을 빼야 되네...
                datetime_millsec = datetime.datetime.fromtimestamp(int_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                # print("datetime_milsec: ", datetime_millsec)
                val = datetime_millsec
            values_list.append(val)

        # print("k: ", k, ", values_list: ", values_list)
        values_tuple = tuple((values_list))
        # print("\ni: ", i, ".setCurrentTableData values_tuple: ", values_tuple, "\n")

        cursArray.execute(sql, values_tuple)  # array_sets.execute() 아님에 주의.

    try:
        mySqlDb.commit()
        print(get_line_no(), "t.테이블: ", currentTable, "의 모든 자료를, 성공적으로 추가하고, COMMIT 성공!!!")
        # QMessageBox.about(self, 'Successfully Saved','Saved to Remote Server DB Successfully')
        # sleep(1)  # 10분 = 600

    except:
        mySqlDb.rollback()
        print(get_line_no(), ", 테이블: ", currentTable, "의 모든 자료의 추가 후 COMMIT 실패!!!")
        # sleep(1)  # 10분 = 600
        # QMessageBox.about(self, 'Failure Saved', 'Saved to Remote Server DB Failure')

    return True


if __name__ == '__main__':
    try:
        INFINITELOOP = 1

        # 2019.03.02 Added. 사출 공정에 사용하는 투입 원료의 [재공 관련 정보] 관리 여부 변수.
        PROCESSING_CONTROL_BEINUSE = False  # True

        # INPUT_CODE_TYPE = "SELECT"

        in_ok_pin = 23
        ok_pin = 24
        in_ng_pin = 20
        ng_pin = 21
        out_pin = 18
        buzzer_pin = 4
        humidity_temperature_pin = 16

        ts_pin1 = 5
        ts_pin2 = 6
        ts_pin3 = 17

        mySqlLocalDb, cursArrayLocal, cursDictLocal = connectLocalDB()

    except:

        print("\n\n")
        # # print("now_utc : " + str(now_utc))
        # print("current_date : " + str(current_date))
        # print("modified_date : " + str(modified_date))
        print(get_line_no(), ", Main except :: 치명적 에러로 강제 종료 ! Completly.....")
        print("\n\n")
        sys.exit()  # 2019.07.16 Conclusion. 아래 명령어 "sys.exit(app.exec())"로는 프로그램이 단지 멈춰있을 뿐이다.
        # sys.exit(app.exec())