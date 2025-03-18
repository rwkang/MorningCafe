# 2021.05.08 Created. 시스템 옵티마이징, MRP.물적 자원 관리 관련 DB.데이터베이스 테이블 핸들링 함수 모음
#####################################################################################################################
# 2021.05.06 Conclusion. 모든 테이블의 자료를 불러오는 것을, "테이블 단위"로 함수를 만들어 사용한다.
#####################################################################################################################

from datetime import time, date, datetime, timedelta
from django.utils import timezone

import datetime as dt  # todo: 엄청 중요 ***** 위의 from datetime import datetime 모듈과 구분하기 위해, 반드시 "dt"로 사용.

import pandas as pd
# import pandas.io.sql as pdsql  # 이것도 안 되네...
import numpy as np
import os

# from .f_common import connectDB, connectRemoteDB, connectWebDB, connectWebWmsDB, connectWebAmsDB
# from .f_common import connectLocalDB, connectRemoteMyDB, connectWebMyDB, connectWebWmsMyDB, connectWebAmsMyDB
from .f_common import *
from .f_powerp import __getMaxDate

from inspect import currentframe, getframeinfo

# 2023.02.06 Added. Django ORM 방식.
# from .models import Process

# 2021.03.17 Conclusion. Unix 시스템에는 실제로 "시스템 언어"가 없습니다.
# Unix는 다중 사용자 시스템이며 각 사용자는 선호하는 언어를 자유롭게 선택할 수 있습니다.
# 시스템 언어에 가장 가까운 것은 사용자가 계정을 구성하지 않을 경우 사용하는 기본 언어입니다.
# locale.setlocale(locale.LC_ALL, "")
# messageLanguage = locale.getlocale(locale.LC_MESSAGES)[0]
# print("messageLanguage: ", messageLanguage)

# windll = ctypes.windll.kernel32
# LANGUAGE_NO = windll.GetUserDefaultUILanguage()  # 1033, 1042 : int 숫자형...
# LANGUAGE_CODE = locale.windows_locale[windll.GetUserDefaultUILanguage()]  # "en_US", "ko_KR" : 문자형
# print(get_line_no(), "LANGUAGE_NO: ", LANGUAGE_NO, ", LANGUAGE_CODE: ", LANGUAGE_CODE)

# if sysName == "posix":  # nt: 윈도우, posix: 리눅스
#     LANGUAGE_NO = 1042
#     LANGUAGE_CODE = "en_US"
# else:
# LANGUAGE_NO = 1042
# LANGUAGE_CODE = "ko_KR"

beInUse = 1  # 현재 사용중인 공정만...
# CONNECTEDSERVER = False
CONNECTEDWEB = False
CONNECTEDWEBWMS = False
CONNECTEDWEBAMS = False
COMPANY_CODE = "" #2021.07.17 Added.


def __confirmRevisionHistory(sessionUserId, revision, dateCurrent, dateStartStr, dateEndStr):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or \
                type(cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # print(get_line_no(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    # 0. RevisionHistory 정리.
    sql = "Select REVISION From REVISIONHISTORY WHERE REVISION = %s Order By REVISION Desc "
    values = revision

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                # print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print(get_line_no(), ", __dbMrp.py array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # print(get_line_no(), ", __dbMrp.py array_sets_server is None!")
            # os.system("pause")
            # sql = "Insert Into REVISIONHISTORY (CONFIRMDATE, REVISIONCLASS, REVISION, CLASSMC, COSTCENTER, ID, " \
            #       "PLANFROM, PLANTO, RCVFROM, RCVTO, PRDFROM, PRDTO G1) " \  # todo: 2022.04.22 발견, 맨 끝 "G1", 이것은 뭔 일로 써졌는지 이해가 안 되네. 맨 처음 원본인 "www.pyongsan.kr" 파일인 "powerp_pyongsan_origin" 폴더에도, 같은 "G1' 문자가 들어가 있네. 단순 오기인 것 같은데...
            #       "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s)"
            sql = "Insert Into REVISIONHISTORY (CONFIRMDATE, REVISIONCLASS, REVISION, CLASSMC, COSTCENTER, ID, " \
                  "PLANFROM, PLANTO, RCVFROM, RCVTO, PRDFROM, PRDTO) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s)"

            values = (dateCurrent, "D", revision, 0, "01", sessionUserId,
                      dateStartStr, dateEndStr, dateStartStr, dateEndStr, dateStartStr, dateEndStr)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), ", __dbMrp.py values: ", values)
            # print("cursArrayWeb: ", cursArrayWeb)

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            sql = "Update REVISIONHISTORY Set CONFIRMDATE = %s, ID = %s Where REVISION = %s "

            values = (dateCurrent, sessionUserId, revision)
            cursArrayWeb.execute(sql, values)

        rs = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

        rs = False

    if rs:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), "REVISIONHISTORY: ", dateCurrent, ": ", revision, " 서버 저장 성공!")
            rs = True
        except KeyboardInterrupt:
            rs = False
            mySqlWebDb.rollback()
            print(get_line_no(), "REVISIONHISTORY: ", dateCurrent, ": ", revision, " 서버 저장 실패!")
    else:
        rs = False

    return rs


# todo: 2022.04.27 Added. "생산 실적 자료" 또한 여기 웹버전에서 직접 추가해 준다.
#  여기서 핵심은, "ProducByDayPlan.작업 지시" 자료가 잘 저장되지 않았다 할 지라도, 여기 "ProductionActual.생산 실적" 자료는
#  저장되는데 전혀 문제가 없이 진행된다는 것이다.
#  원래 "Powerbuilder" App 버전에서는, [1. 생산 계획, 2. 작업 지시, 3. 생산 실적] 이런 순서를 반드시 지켰었다.
def __setProductionActualData(sessionUserId, revision, dateCurrent, code, daywork, lineCode, dayNight, workdate,
                              workedtimes, workers, startWorkTime, endWorkTime, machineCode, groupsCode,
                              dfSetsProcess, process):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, COMPANY_CODE
    # print(get_line_no(), ", __dbMrp CONNECTEDWEB: ", CONNECTEDWEB)
    # print(get_line_no(), ", __dbMrp COMPANY_CODE: ", COMPANY_CODE, ", type(COMPANY_CODE): ", type(COMPANY_CODE))
    # print(get_line_no(), ", __dbMrp lineCode: ", lineCode, ", type(lineCode): ", type(lineCode))
    # print(get_line_no(), ", __dbMrp workdate: ", workdate, ", type(workdate): ", type(workdate))
    # print(get_line_no(), ", __dbMrp startWorkTime: ", startWorkTime, ", type(startWorkTime): ", type(startWorkTime))

    print(get_line_no(), "작업자 등록은 언제 할 건가? workers: ", workers, ", type(workers): ", type(workers))

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print("3 __resetProductionPlanDate Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", Database 연결을 확인하시오!")

    # print(get_line_no(), ", __dbMrp startWorkTime: ", startWorkTime, ", type(startWorkTime): ", type(startWorkTime))
    # print(get_line_no(), ", __dbMrp endWorkTime: ", endWorkTime, ", type(endWorkTime): ", type(endWorkTime))

    # 작업 지시 번호와 생산 실적 번호는 원래 같다.
    production_actual_no = __makingProducingOrderNo(workdate, COMPANY_CODE, lineCode, dayNight, code)
    # print(get_line_no(), ", __dbMrp production_actual_no: ", production_actual_no)

    # PRODUCTIONACTUALNO, LOTNO, REVISION, WORKDATE, WORKFROM, WORKTO,
    # CODE, COSTCENTER, WORKCENTER, MACHINE, GROUPSS, FACODE, PRODUCINGORDERNO,
    # PRODUCINGORDER, PRODUCED, DAYWORK, DAYNIGHT, GOODNESS, BADNESS, S_DATE, WORKER, ID,
    # FIRSTMODIFIED, LASTMODIFIED, MOVINGWAREHOUSE, MOVINGQTY, REQUIREDSTANDARD=1

    sql = "Select PRODUCTIONACTUALNO, GROUPSS From PRODUCTIONACTUAL WHERE PRODUCTIONACTUALNO = %s " \
          "Order By PRODUCTIONACTUALNO "
    values = (production_actual_no)

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                    cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                # print(get_line_no(), ", Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", Database 연결을 확인하시오!")

    try:
        # 2022.04.27 Added. 특정한 공정 코드에 대한 공정 정보 가져오기와 북경 조이 작업 일지 업로드 처리에서, "작업 위치" 값 가져오기
        # // 2020.06.14 Modified. 지금까지 처리 [위치-창고]를, BOM에서 등록한 [자동 이동 창고]를 기준으로 처리하였으나,
        # // 지금부터는 무조건 [창고 코드 기준.생산 위치 자기 자리]에 [재공.생산]과 [재고.입고]를 먼저 처리하고, 이후 차기 공정으로의 [재공.투입] 처리는,
        # // [소형 바코드 프린터 및 스캐너]를 활용한 [물류 시스템]을 도입하여 처리한다.
        # // Select MovingWarehouse Into :is_ParentWarehouse From t_Product Where Code=:ls_PaCode Using SQLCA;
        # todo: ===> Select WarehouseSt Into :is_ParentWarehouse From Process Where Code=:is_Process Using SQLCA;
        rs, process, processEng, processKor, processLoc, processChn, process_superior, warehouse_standard, colorSt = \
            __getProcessInfo(dfSetsProcess, process)

        m_code, required, tolerance = __getRequired(code)

        # 처음 connectWebMyDB() 연결에 실패하고, 두번째 연결에 성공했으면, 그 때 "생산 실적 번호"를 정상적으로 만들 수 있다.
        production_actual_no = __makingProducingOrderNo(workdate, COMPANY_CODE, lineCode, dayNight, code)
        # print(get_line_no(), ", __dbMrp production_actual_no: ", production_actual_no)

        cost_center = ""  # 의미 없지만, NULL 불인정이므로, 반드시 넣어줘야 한다.
        work_center = ""  # 의미 없지만, NULL 불인정이므로, 반드시 넣어줘야 한다.
        produced = 0  # 의미 없지만, NULL 불인정이므로, 반드시 넣어줘야 한다.

        badness = 0
        s_date = workdate.strftime('%Y-%m-%d')
        # print(get_line_no(), ", __dbMrp s_date: ", s_date)

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()
        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print(get_line_no(), ", __dbMrp PRODUCTIONACTUAL array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # PRODUCTIONACTUALNO, LOTNO, REVISION, WORKDATE, WORKFROM, WORKTO,
            # CODE, COSTCENTER, WORKCENTER, MACHINE, GROUPSS, FACODE, PRODUCINGORDERNO,
            # PRODUCINGORDER, PRODUCED, DAYWORK, DAYNIGHT, GOODNESS, BADNESS, S_DATE, WORKER, ID,
            # FIRSTMODIFIED, LASTMODIFIED, MOVINGWAREHOUSE, MOVINGQTY, REQUIREDSTANDARD=1
            # 2022.04.28 Conclusion. "date" 타입인 workdate 변수를, "datetime" 타입인 "WORKDATE" 컬럼에 넣는 것은 문제 없다.
            sql = "Insert Into PRODUCTIONACTUAL (PRODUCTIONACTUALNO, LOTNO, REVISION, WORKDATE, WORKFROM, WORKTO, " \
                  "CODE, COSTCENTER, WORKCENTER, MACHINE, GROUPSS, FACODE, " \
                  "PRODUCINGORDERNO, PRODUCINGORDER, PRODUCED, DAYWORK, DAYNIGHT, GOODNESS, " \
                  "BADNESS, S_DATE, WORKER, ID, FIRSTMODIFIED, LASTMODIFIED, MOVINGWAREHOUSE, MOVINGQTY, " \
                  "REQUIREDSTANDARD) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s) "
            # print(get_line_no(), ", __dbMrp PRODUCTIONACTUAL sql: ", sql)
            values = (production_actual_no, production_actual_no, revision, startWorkTime, startWorkTime, endWorkTime,
                      code, cost_center, work_center, machineCode, groupsCode, machineCode,
                      production_actual_no, daywork, produced, daywork, dayNight,
                      daywork, badness, s_date, workers, sessionUserId, dateCurrent, dateCurrent, warehouse_standard,
                      daywork, required)
            # print(get_line_no(), ", __dbMrp PRODUCTIONACTUAL values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), ", PRODUCTIONACTUAL cursArrayWeb: ", cursArrayWeb)

        else:  # row_count_server > 0 : 이미 생산 실적 자료가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            # PRODUCTIONACTUALNO, LOTNO, REVISION, WORKDATE, WORKFROM, WORKTO,
            # CODE, COSTCENTER, WORKCENTER, MACHINE, GROUPSS, FACODE, PRODUCINGORDERNO,
            # PRODUCINGORDER, PRODUCED, DAYWORK, DAYNIGHT, GOODNESS, BADNESS, S_DATE, WORKER, ID,
            # FIRSTMODIFIED, LASTMODIFIED, MOVINGWAREHOUSE, MOVINGQTY, REQUIREDSTANDARD=1
            sql = "Update PRODUCTIONACTUAL Set REVISION = %s, WORKDATE = %s, " \
                  "WORKFROM = %s, WORKTO = %s, MACHINE = %s, GROUPSS = %s, FACODE = %s, " \
                  "PRODUCINGORDER = %s, DAYWORK = %s, GOODNESS = %s, BADNESS = %s, S_DATE = %s, WORKER = %s, ID = %s, " \
                  "FIRSTMODIFIED = %s, LASTMODIFIED = %s, MOVINGWAREHOUSE = %s, MOVINGQTY = %s, REQUIREDSTANDARD = %s " \
                  "WHERE PRODUCINGORDERNO = %s "
            values = (revision, workdate, startWorkTime, endWorkTime, machineCode, groupsCode, machineCode,
                      daywork, daywork, daywork, badness, s_date, workers, sessionUserId, dateCurrent, dateCurrent,
                      warehouse_standard, daywork, required, production_actual_no)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), ", __dbMrp dayNight: ", dayNight, ", type(dayNight): ", type(dayNight))

        rtnResult = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), ", 경고, PRODUCTIONACTUAL [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rtnResult = False

    if rtnResult:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), ", PRODUCTIONACTUAL: ", workdate, " :: ", revision, " :: ", code,
            #       ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 성공!!! ")
            rs = True
        except KeyboardInterrupt:
            rs = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", PRODUCTIONACTUAL: ", workdate, " :: ", revision, " :: ", code,
                  ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
    else:
        print(get_line_no(), ", PRODUCTIONACTUAL: ", workdate, " :: ", revision, " :: ", code,
              ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
        rs = False
    return rs


# todo: 2022.04.27 Added. "작업 지시 자료" 또한 여기 웹버전에서 직접 추가해 준다.
def __setProductByDayPlanData(sessionUserId, revision, dateCurrent, code, daywork, lineCode, dayNight, workdate,
                              workedtimes, workers, startWorkTime, endWorkTime, machineCode, groupsCode):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, COMPANY_CODE
    # print(get_line_no(), ", CONNECTEDWEB: ", CONNECTEDWEB)
    # print(get_line_no(), ", COMPANY_CODE: ", COMPANY_CODE, ", type(COMPANY_CODE): ", type(COMPANY_CODE))
    # print(get_line_no(), ", lineCode: ", lineCode, ", type(lineCode): ", type(lineCode))
    # print(get_line_no(), ", lineCode: ", dayNight, ", type(dayNight): ", type(dayNight))
    # print(get_line_no(), ", workdate: ", workdate, ", type(workdate): ", type(workdate))

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print("3 __resetProductionPlanDate Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", Database 연결을 확인하시오!")

    # todo: Powerbuilder.w_i_ProductionDayPlan_wo:
    #  2018.10.15 Modified. 라즈베리 파이의 생산 실적 자동 수집 자료인 "Gathering_Data.Producing_Order_No"를,
    #  다시 검토한 결과, "작업 지시 번호 작성 기준"을 아래와 같이 수정한다.
    #  년도(2)+월도(2)+일도(2)+회사 코드(6)+생산 라인(2)+주야(1)+제품 코드(10)
    #  특정 날짜에 2번 이상 같은 제품을 생산할 경우에도(는) "작업 지시 번호"는 동일하다. 당연히 "생산 실적 번호"는 다르다.

    producing_order_no = __makingProducingOrderNo(workdate, COMPANY_CODE, lineCode, dayNight, code)
    # print(get_line_no(), ", __dbMrp producing_order_no: ", producing_order_no)

    # PRODUCINGORDERNO, FORCENORMAL="N", REVISION, CODE, GROUPSS, WORKINGORDERSEQ, FACODE, DAYNIGHT, PLANDATE, MA, MC,
    # PRODUCTION, LOTNO, MODIFIEDDATE, USERID

    sql = "Select PRODUCINGORDERNO, GROUPSS From PRODUCTBYDAYPLANDATA WHERE PRODUCINGORDERNO = %s " \
          "Order By PRODUCINGORDERNO "
    values = (producing_order_no)

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                    cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                # print("33 Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")
                # return False

    try:
        force_normal = "N"
        working_order_seq = 1

        # 처음 connectWebMyDB() 연결에 실패하고, 두번째 연결에 성공했으면, 그 때 "작업 지시 번호"를 정상적으로 만들 수 있다.
        producing_order_no = __makingProducingOrderNo(workdate, COMPANY_CODE, lineCode, dayNight, code)

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()
        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print(get_line_no(), "PRODUCTBYDAYPLANDATA array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # 2022.04.28 Conclusion. "date" 타입인 workdate 변수를, "datetime" 타입인 "PLANDATE" 컬럼에 넣는 것은 문제 없다.
            sql = "Insert Into PRODUCTBYDAYPLANDATA (PRODUCINGORDERNO, FORCENORMAL, REVISION, CODE, GROUPSS, " \
                  "WORKINGORDERSEQ, FACODE, DAYNIGHT, PLANDATE, MA, MC, PRODUCTION, LOTNO, MODIFIEDDATE, USERID) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s) "
            # print(get_line_no(), ", __dbMrp __setProductByDayPlanData sql: ", sql)
            values = (producing_order_no, force_normal, revision, code, groupsCode,
                      working_order_seq, machineCode, dayNight, workdate, daywork, daywork, daywork,
                      producing_order_no, dateCurrent, sessionUserId)
            # print(get_line_no(), ", __dbMrp workdate: ", workdate, ", type(workdate): ", type(workdate))
            # print(get_line_no(), ", __dbMrp __setProductByDayPlanData values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), ", __dbMrp __setProductByDayPlanData cursArrayWeb: ", cursArrayWeb)

        else:  # row_count_server > 0 : 이미 작업 지시 자료가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            # PRODUCINGORDERNO, FORCENORMAL="N", REVISION, CODE, GROUPSS, WORKINGORDERSEQ, FACODE, DAYNIGHT, PLANDATE, MA, MC,
            # PRODUCTION, LOTNO, MODIFIEDDATE, USERID
            sql = "Update PRODUCTBYDAYPLANDATA Set REVISION = %s, GROUPSS = %s, WORKINGORDERSEQ = %s, " \
                  "FACODE = %s, PLANDATE = %s, DAYNIGHT = %s, MA = %s, MC = %s, " \
                  "PRODUCTION = %s, LOTNO = %s, MODIFIEDDATE = %s, USERID = %s " \
                  "WHERE PRODUCINGORDERNO = %s "
            values = (revision, groupsCode, working_order_seq, machineCode, workdate, dayNight, daywork, daywork,
                      daywork, producing_order_no, dateCurrent, sessionUserId, producing_order_no)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), ", __dbMrp dayNight: ", dayNight, ", type(dayNight): ", type(dayNight))

        rtnResult = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, PRODUCTBYDAYPLANDATA [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rtnResult = False

    if rtnResult:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), "ProductionPlanDate: ", workdate, " :: ", revision, " :: ", code,
            #       ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 성공!!! ")
            rs = True
        except KeyboardInterrupt:
            rs = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", PRODUCTBYDAYPLANDATA: ", workdate, " :: ", revision, " :: ", code,
                  ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
    else:
        print(get_line_no(), ", PRODUCTBYDAYPLANDATA: ", workdate, " :: ", revision, " :: ", code,
              ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
        rs = False
    return rs


# 2021.06.20 Added. "작업 시간"을 추가하여, CS.생산 실적 정리할 때, 작업 시간을 끌고 가서 정리하게 한다.
def __setProductionPlanDate(sessionUserId, revision, dateCurrent, dayStr, code, daywork, lineCode, dayNight,
                            workdate, daywork1, daywork2, daywork3, daywork4, daywork5, daywork6,
                            workedtimes, workedtimes1, workedtimes2, workedtimes3, workedtimes4, workedtimes5,
                            workedtimes6, workers, startWorkTime, endWorkTime, machineCode, groupsCode):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    time_temp = datetime.datetime.min.time()
    # print(get_line_no(), "time_temp: ", time_temp)

    # print(get_line_no(), "CONNECTEDWEB: ", CONNECTEDWEB)
    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print("Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # print("0 __setProductionPlanDate dayStr: ", dayStr, ", monthStr: ", monthStr, ", yearStr: ", yearStr)
    # PRODUCTIONHISTORYDAY.DPxx Update...
    sql = "Select REVISION, CODE, MACHINE, GROUPSS From PRODUCTIONPLANDATE " \
          "WHERE REVISION = %s AND WORKDATE = %s AND CODE = %s AND GROUPSS = %s AND DAYNIGHT = %s " \
          "Order By REVISION, WORKDATE, CODE, GROUPSS, DAYNIGHT "

    # todo: 2022.06.15 Conclusion. 아래와 같이 시간(00:00:00) 표식를 하지 않고, 'date' 형으로도 검색이 가능하지만,
    #  더 정확성을 기하기 위해, 시간(00:00:00) 표식을 추가해 준다.
    if type(workdate) == date:
        workdate = datetime.datetime.combine(workdate, time_temp)

    # workdate = dt.datetime.strftime(workdate, '%Y-%m-%d %H:%M:%S')  # datetime => str
    # workdate = dt.datetime.strftime(workdate, '%Y-%m-%d %H:%M:%S.%f')  # str => datetime
    # workdate = dt.datetime.strptime(workdate, '%Y-%m-%d') # str => date

    values = (revision, workdate, code, groupsCode, dayNight)
    # print(get_line_no(), "values: \n", values)

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        # if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        if type(mySqlWebDb) is pymysql.connections.Connection or type(
            cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print("Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()
        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print(get_line_no(), "PRODUCTIONPLANDATE array_sets_server.count() : ", row_count_server)

        # print(get_line_no(), "workdate: ", workdate, ", type(workdate): ", type(workdate))
        # print(get_line_no(), "dateCurrent: ", dateCurrent, ", type(dateCurrent): ", type(dateCurrent))

        # if type(workdate) == datetime.date:  # 이렇게는 안 되네. 에러는 안 나는데, 인식을 못하네.
        # if type(workdate) == date:  # 그런데 이것은 "시간을 뺀" "순수 날짜" 값만 기록하는 것이 좋을 듯. ∴) 여기 라인을 실행을 안 시켜야 된다.
        #     workdate = datetime.datetime.combine(workdate, time_temp)

        # if type(dateCurrent) == datetime.date:  # 이렇게는 안 되네. 에러는 안 나는데, 인식을 못하네.
        if type(dateCurrent) == date:
            dateCurrent = datetime.datetime.combine(dateCurrent, time_temp)
        # print(get_line_no(), "workdate: ", workdate, ", type(workdate): ", type(workdate))
        # print(get_line_no(), "dateCurrent: ", dateCurrent, ", type(dateCurrent): ", type(dateCurrent))

        # print(get_line_no(), "sql: ", sql)

        # dateCurrent = dt.datetime.strftime(dateCurrent, '%Y-%m-%d %H:%M:%S')  # datetime => str

        # print(get_line_no(), "workedtimes: ", workedtimes, ", type(workedtimes): ", type(workedtimes))

        # todo: 2022.06.16 Conclusion. 매우 중요한 발견: TABLE.WORKERS 컬럼 타입이 'INT'이고,
        #  변수 workers 타입이 <class 'numpy.float64'> 또는 <class 'float'> 타입일 때,
        #  내 컴퓨터.MySQL에서는 문제없이 쿼리문(cursArrayWeb.execute(sql, values))을 실행하지만,
        #  AWS 아마존 서버에 있는 MySQL에서는 쿼리문(cursArrayWeb.execute(sql, values))에서, 실행 에러가 난다.
        #  또한, TABLE.DAYWORK1 컬럼 타입이 'DECIMAL 18.4'라고 할 지라도,
        #  변수 daywork1 타입이 <class 'numpy.float64'>이면, 즉 <class 'float'> 타입이 아니면,
        #  이 또한 내 컴퓨터.MySQL에서는 문제없이 쿼리문(cursArrayWeb.execute(sql, values))을 실행하지만,
        #  AWS 아마존 서버에 있는 MySQL에서는 쿼리문(cursArrayWeb.execute(sql, values))에서, 실행 에러가 난다.
        # print(get_line_no(), "workedtimes: ", workedtimes, ", type(workedtimes): ", type(workedtimes))
        # print(get_line_no(), "startWorkTime: ", startWorkTime, ", type(startWorkTime): ", type(startWorkTime))
        # print(get_line_no(), "endWorkTime: ", endWorkTime, ", type(endWorkTime): ", type(endWorkTime))
        # print(get_line_no(), "dayNight: ", dayNight, ", type(dayNight): ", type(dayNight))
        # print(get_line_no(), "workedtimes1: ", workedtimes1, ", type(workedtimes1): ", type(workedtimes1))
        # print(get_line_no(), "workedtimes2: ", workedtimes2, ", type(workedtimes2): ", type(workedtimes2))
        # print(get_line_no(), "workedtimes3: ", workedtimes3, ", type(workedtimes3): ", type(workedtimes3))
        # print(get_line_no(), "workedtimes4: ", workedtimes4, ", type(workedtimes4): ", type(workedtimes4))
        # print(get_line_no(), "workedtimes5: ", workedtimes5, ", type(workedtimes5): ", type(workedtimes5))
        # print(get_line_no(), "workedtimes6: ", workedtimes6, ", type(workedtimes6): ", type(workedtimes6))
        # print(get_line_no(), "daywork1: ", daywork1, ", type(daywork1): ", type(daywork1))
        # print(get_line_no(), "daywork2: ", daywork2, ", type(daywork2): ", type(daywork2))
        # print(get_line_no(), "daywork3: ", daywork3, ", type(daywork3): ", type(daywork3))
        # print(get_line_no(), "daywork4: ", daywork4, ", type(daywork4): ", type(daywork4))
        # print(get_line_no(), "daywork5: ", daywork5, ", type(daywork5): ", type(daywork5))
        # print(get_line_no(), "daywork6: ", daywork6, ", type(daywork6): ", type(daywork6))
        # print(get_line_no(), "workers: ", workers, ", type(workers): ", type(workers))
        # print(get_line_no(), "sessionUserId: ", sessionUserId, ", type(sessionUserId): ", type(sessionUserId))
        # print(get_line_no(), "dateCurrent: ", dateCurrent, ", type(dateCurrent): ", type(dateCurrent))
        # print(get_line_no(), "revision: ", revision, ", type(revision): ", type(revision))
        # print(get_line_no(), "workdate: ", workdate, ", type(workdate): ", type(workdate))
        # print(get_line_no(), "code: ", code, ", type(code): ", type(code))
        # print(get_line_no(), "groupsCode: ", groupsCode, ", type(groupsCode): ", type(groupsCode))
        # print(get_line_no(), "dayNight: ", dayNight, ", type(dayNight): ", type(dayNight))

        if array_sets_server is None or row_count_server < 1:
            sql = "Insert Into PRODUCTIONPLANDATE (REVISION, WORKDATE, CODE, PRODUCTIONPERFORMANCEQTIES, " \
                  "WORKEDTIMES, FROMTIME, TOTIME, MACHINE, GROUPSS, DAYNIGHT, WORKEDTIMES1, WORKEDTIMES2, " \
                  "WORKEDTIMES3, WORKEDTIMES4, WORKEDTIMES5, WORKEDTIMES6, PRODUCTIONPERFORMANCEQTIES1, " \
                  "PRODUCTIONPERFORMANCEQTIES2, PRODUCTIONPERFORMANCEQTIES3, PRODUCTIONPERFORMANCEQTIES4, " \
                  "PRODUCTIONPERFORMANCEQTIES5, PRODUCTIONPERFORMANCEQTIES6, WORKERS, USERID, MODIFIEDDATE) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s) "
            # # 4 + 8 + 5 + 3 + 5 = 25
            values = (revision, workdate, code, daywork, workedtimes, startWorkTime, endWorkTime,
                      machineCode, groupsCode, dayNight, workedtimes1, workedtimes2, workedtimes3, workedtimes4,
                      workedtimes5, workedtimes6, daywork1, daywork2, daywork3, daywork4, daywork5, daywork6,
                      workers, sessionUserId, dateCurrent)
            # sql = "Insert Into PRODUCTIONPLANDATE (REVISION, WORKDATE, CODE, PRODUCTIONPERFORMANCEQTIES, " \
            #       "WORKEDTIMES, FROMTIME, TOTIME, MACHINE, GROUPSS, DAYNIGHT, " \
            #       "WORKERS, USERID, MODIFIEDDATE) " \
            #       "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s) "
            # # 4 + 8 + 5 + 3 + 5 = 25
            # values = (revision, workdate, code, daywork, workedtimes, startWorkTime, endWorkTime,
            #           machineCode, groupsCode, dayNight,
            #           workers, sessionUserId, dateCurrent)
            # print(get_line_no(), "values: \n", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), "cursArrayWeb: ", cursArrayWeb)

        else:  # row_count_server > 0 : 이미 생산 계획 자료가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            # workdate = workdate + " 00:00:00.000"  # 2021-06-18 00:00:00.000

            sql = "Update PRODUCTIONPLANDATE Set WORKEDTIMES = %s, FROMTIME = %s, TOTIME = %s, " \
                  "WORKEDTIMES1 = %s, WORKEDTIMES2 = %s, " \
                  "WORKEDTIMES3 = %s, WORKEDTIMES4 = %s, WORKEDTIMES5 = %s, WORKEDTIMES6 = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES1 = %s, PRODUCTIONPERFORMANCEQTIES2 = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES3 = %s, PRODUCTIONPERFORMANCEQTIES4 = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES5 = %s, PRODUCTIONPERFORMANCEQTIES6 = %s, " \
                  "WORKERS = %s, USERID = %s, MODIFIEDDATE = %s " \
                  "Where REVISION = %s AND WORKDATE = %s AND CODE = %s AND GROUPSS = %s AND DAYNIGHT = %s "
            values = (workedtimes, startWorkTime, endWorkTime,
                      workedtimes1, workedtimes2, workedtimes3, workedtimes4, workedtimes5, workedtimes6,
                      daywork1, daywork2, daywork3, daywork4, daywork5, daywork6,
                      workers, sessionUserId, dateCurrent,
                      revision, workdate, code, groupsCode, dayNight)
            # sql = "Update PRODUCTIONPLANDATE Set WORKEDTIMES = %s, FROMTIME = %s, TOTIME = %s, " \
            #       "WORKERS = %s, USERID = %s, MODIFIEDDATE = %s " \
            #       "Where REVISION = %s AND WORKDATE = %s AND CODE = %s AND GROUPSS = %s AND DAYNIGHT = %s "
            # values = (workedtimes, startWorkTime, endWorkTime,
            #           workers, sessionUserId, dateCurrent,
            #           revision, workdate, code, groupsCode, dayNight)
            # print(get_line_no(), "values: \n", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), "cursArrayWeb: ", cursArrayWeb)

        rtnResult = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "[cursArrayWeb.execute(sql, values)]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rtnResult = False

    if rtnResult:
        try:
            mySqlWebDb.commit()
            # print("ProductionPlanDate: ", workdate, " :: ", revision, " :: ", code,
            #       ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 성공!!! ")
            rs = True
        except KeyboardInterrupt:
            rs = False
            mySqlWebDb.rollback()
            print(get_line_no(), "workdate: ", workdate, " :: ", revision, " :: ", code,
                  ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
    else:
        print(get_line_no(), "workdate: ", workdate, " :: ", revision, " :: ", code,
              ", startWorkTime: ", startWorkTime, ", endWorkTime: ", endWorkTime, ", 서버 저장 실패!!! ")
        rs = False
    return rs


# 2021.05.11 Create. 여기가 __initRevisionHistoryDay()와 다른 것은,
# __initRevisionHistoryDay "PRODUCTIONHISTORYDAY" 테이블을 가지고,
# "revision.생관 번호"를 기준으로, 아규먼트로 받은 "dayStr.특정 날짜"에 대해, "0"으로 초기화 해주는 것이고,
# 여기__setRevisionHistoryDaySelected() 함수는, "PRODUCTIONHISTORYDAY" 테이블을 가지고,
# "revision.생관 번호"와 "code.품번"을 기준으로, 아규먼트로 받은 "dayStr.특정 날짜"에 대해,
# "로우"가 없으면, 생성해서, "생산 계획 수량"을 직접 세팅해 주는 것이다.
def __setProductionHistoryDay(sessionUserId, revision, dateCurrent, dayStr, code, daywork, lineCode, process):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # print(get_line_no(), ", __dbMrp revision: ", revision, ", code: ", code, ", lineCode: ", lineCode, ", process: ", process)
    # PRODUCTIONHISTORYDAY.DPxx Update...
    sql = "Select CODE From PRODUCTIONHISTORYDAY " \
          "WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s Order By REVISION, CODE "
    values = (revision, code, lineCode, process)

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                # print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")
                # return False

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print(get_line_no(), "PRODUCTIONHISTORYDAY array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # print("__updateProductionDaily i:, ", i, ", monthStr: ", monthStr, ", dayStr: ", dayStr, ", code: ", code)
            # os.system("pause")
            if int(dayStr) == 1:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP1, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 2:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP2, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 3:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP3, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 4:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP4, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 5:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP5, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 6:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP6, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 7:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP7, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 8:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP8, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 9:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP9, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 10:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP10, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 11:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP11, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 12:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP12, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 13:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP13, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 14:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP14, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 15:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP15, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 16:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP16, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 17:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP17, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 18:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP18, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 19:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP19, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 20:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP20, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 21:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP21, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 22:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP22, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 23:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP23, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 24:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP24, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 25:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP25, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 26:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP26, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 27:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP27, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 28:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP28, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 29:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP29, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 30:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP30, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            if int(dayStr) == 31:
                sql = "Insert Into PRODUCTIONHISTORYDAY (REVISION, CODE, DP31, USERID, REFLECTSTOCK, LINECODE, PROCESS) " \
                      "Values (%s,%s,%s,%s,%s, %s,%s) "
            values = (revision, code, daywork, sessionUserId, 0, lineCode, process)
            # print("1 __updateProductionDaily values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print("1 __updateProductionDaily cursArrayWeb: ", cursArrayWeb)

        else:  # row_count_server > 0 : 이미 생산 계획 자료가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            if int(dayStr) == 1:
                sql = "Update PRODUCTIONHISTORYDAY Set DP1 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 2:
                sql = "Update PRODUCTIONHISTORYDAY Set DP2 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 3:
                sql = "Update PRODUCTIONHISTORYDAY Set DP3 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 4:
                sql = "Update PRODUCTIONHISTORYDAY Set DP4 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 5:
                sql = "Update PRODUCTIONHISTORYDAY Set DP5 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 6:
                sql = "Update PRODUCTIONHISTORYDAY Set DP6 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 7:
                sql = "Update PRODUCTIONHISTORYDAY Set DP7 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 8:
                sql = "Update PRODUCTIONHISTORYDAY Set DP8 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 9:
                sql = "Update PRODUCTIONHISTORYDAY Set DP9 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 10:
                sql = "Update PRODUCTIONHISTORYDAY Set DP10 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 11:
                sql = "Update PRODUCTIONHISTORYDAY Set DP11 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 12:
                sql = "Update PRODUCTIONHISTORYDAY Set DP12 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 13:
                sql = "Update PRODUCTIONHISTORYDAY Set DP13 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 14:
                sql = "Update PRODUCTIONHISTORYDAY Set DP14 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 15:
                sql = "Update PRODUCTIONHISTORYDAY Set DP15 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 16:
                sql = "Update PRODUCTIONHISTORYDAY Set DP16 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 17:
                sql = "Update PRODUCTIONHISTORYDAY Set DP17 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 18:
                sql = "Update PRODUCTIONHISTORYDAY Set DP18 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 19:
                sql = "Update PRODUCTIONHISTORYDAY Set DP19 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 20:
                sql = "Update PRODUCTIONHISTORYDAY Set DP20 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 21:
                sql = "Update PRODUCTIONHISTORYDAY Set DP21 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 22:
                sql = "Update PRODUCTIONHISTORYDAY Set DP22 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 23:
                sql = "Update PRODUCTIONHISTORYDAY Set DP23 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 24:
                sql = "Update PRODUCTIONHISTORYDAY Set DP24 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 25:
                sql = "Update PRODUCTIONHISTORYDAY Set DP25 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 26:
                sql = "Update PRODUCTIONHISTORYDAY Set DP26 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 27:
                sql = "Update PRODUCTIONHISTORYDAY Set DP27 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 28:
                sql = "Update PRODUCTIONHISTORYDAY Set DP28 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 29:
                sql = "Update PRODUCTIONHISTORYDAY Set DP29 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 30:
                sql = "Update PRODUCTIONHISTORYDAY Set DP30 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "
            if int(dayStr) == 31:
                sql = "Update PRODUCTIONHISTORYDAY Set DP31 = %s, USERID = %s WHERE REVISION = %s AND CODE = %s AND LINECODE = %s AND PROCESS = %s "

            values = (daywork, sessionUserId, revision, code, lineCode, process)
            # print(get_line_no(), "__dbMrp PRODUCTIONHISTORYDAY daywork: ", daywork)
            # print(get_line_no(), "__dbMrp PRODUCTIONHISTORYDAY revision: ", revision)
            # print(get_line_no(), "__dbMrp PRODUCTIONHISTORYDAY code: ", code)
            # print(get_line_no(), "__dbMrp PRODUCTIONHISTORYDAY lineCode: ", lineCode)

            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), "__dbMrp PRODUCTIONHISTORYDAY cursArrayWeb: ", cursArrayWeb)

        rtnResult = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), ", 경고, PRODUCTIONHISTORYDAY [callMainData]에서 치명적 에러가 발생하였습니다. "
                             "관리자에게 문의하시오!")
        rtnResult = False

    if rtnResult:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), "PRODUCTIONHISTORYDAY: ", dateCurrent, " :: ", revision, " 서버 저장 성공! ")
            rs = True
        except KeyboardInterrupt:
            rs = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", PRODUCTIONHISTORYDAY: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")
    else:
        rs = False
        print(get_line_no(), ", PRODUCTIONHISTORYDAY: ", dateCurrent, " :: ", revision, " 서버 저장 실패!!! ")

    return rs


# 2021.05.11 Create. 여기가 __setRevisionHistoryDaySelected()와 다른 것은,
# 여기서는 "PRODUCTIONHISTORYDAY" 테이블을 가지고, "revision.생관 번호"를 기준으로, 아규먼트로 받은 "dayStr.특정 날짜"에 대해,
# "0"으로 초기화 해주는 것이고,
# __setRevisionHistoryDaySelected() 함수는, "PRODUCTIONHISTORYDAY" 테이블을 가지고,
# "revision.생관 번호"와 "code.품번"을 기준으로, 아규먼트로 받은 "dayStr.특정 날짜"에 대해,
# "로우"가 없으면, 생성해서, "생산 계획 수량"을 직접 세팅해 주는 것이다.
def __initProductionHistoryDay(sessionUserId, revision, dateCurrent, dayStr):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), ", __resetProductionPlanData Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __resetProductionPlanData Database 연결을 확인하시오!")

    # print("1 __resetProductionPlanData dayStr: ", dayStr, ", monthStr: ", monthStr, ", yearStr: ", yearStr)
    # 1. ProductionHistoryDay.생산 계획 총괄 테이블의 [DPxx.해당 일자]의 모든 값을 [0]으로 초기화한다.
    sql = "Select REVISION From PRODUCTIONHISTORYDAY WHERE REVISION = %s Order By REVISION Desc "
    values = revision

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                # print(get_line_no(), ", __resetProductionPlanData Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __resetProductionPlanData Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            print(get_line_no(), ", __resetProductionPlanData array_sets_server: ")
            # print("1 __resetProductionPlanData array_sets_server: ", array_sets_server)
            # os.system("pause")

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???

            # 해당 "날짜"만 초기화한다. "전체 날짜"를 모두 초기화할 필요는 없다.
            if int(dayStr) == 1:
                sql = "Update PRODUCTIONHISTORYDAY Set DP1 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 2:
                sql = "Update PRODUCTIONHISTORYDAY Set DP2 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 3:
                sql = "Update PRODUCTIONHISTORYDAY Set DP3 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 4:
                sql = "Update PRODUCTIONHISTORYDAY Set DP4 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 5:
                sql = "Update PRODUCTIONHISTORYDAY Set DP5 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 6:
                sql = "Update PRODUCTIONHISTORYDAY Set DP6 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 7:
                sql = "Update PRODUCTIONHISTORYDAY Set DP7 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 8:
                sql = "Update PRODUCTIONHISTORYDAY Set DP8 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 9:
                sql = "Update PRODUCTIONHISTORYDAY Set DP9 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 10:
                sql = "Update PRODUCTIONHISTORYDAY Set DP10 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 11:
                sql = "Update PRODUCTIONHISTORYDAY Set DP11 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 12:
                sql = "Update PRODUCTIONHISTORYDAY Set DP12 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 13:
                sql = "Update PRODUCTIONHISTORYDAY Set DP13 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 14:
                sql = "Update PRODUCTIONHISTORYDAY Set DP14 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 15:
                sql = "Update PRODUCTIONHISTORYDAY Set DP15 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 16:
                sql = "Update PRODUCTIONHISTORYDAY Set DP16 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 17:
                sql = "Update PRODUCTIONHISTORYDAY Set DP17 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 18:
                sql = "Update PRODUCTIONHISTORYDAY Set DP18 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 19:
                sql = "Update PRODUCTIONHISTORYDAY Set DP19 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 20:
                sql = "Update PRODUCTIONHISTORYDAY Set DP20 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 21:
                sql = "Update PRODUCTIONHISTORYDAY Set DP21 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 22:
                sql = "Update PRODUCTIONHISTORYDAY Set DP22 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 23:
                sql = "Update PRODUCTIONHISTORYDAY Set DP23 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 24:
                sql = "Update PRODUCTIONHISTORYDAY Set DP24 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 25:
                sql = "Update PRODUCTIONHISTORYDAY Set DP25 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 26:
                sql = "Update PRODUCTIONHISTORYDAY Set DP26 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 27:
                sql = "Update PRODUCTIONHISTORYDAY Set DP27 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 28:
                sql = "Update PRODUCTIONHISTORYDAY Set DP28 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 29:
                sql = "Update PRODUCTIONHISTORYDAY Set DP29 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 30:
                sql = "Update PRODUCTIONHISTORYDAY Set DP30 = %s, USERID = %s WHERE REVISION = %s "
            if int(dayStr) == 31:
                sql = "Update PRODUCTIONHISTORYDAY Set DP31 = %s, USERID = %s WHERE REVISION = %s "

            values = (0, sessionUserId, revision)
            cursArrayWeb.execute(sql, values)

        rs1 = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), ", 경고, ProductionPlanData [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rs1 = False

    if rs1:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), ", ProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 성공! ")
            rs1 = True
        except KeyboardInterrupt:
            rs1 = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", ProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")
    else:
        rs1 = False

    return rs1


def __confirmProductionPlanData(sessionUserId, revision, dateCurrent, dateStartStr, dateEndStr):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    debugPath = "__dbMrp.py __confirmProductionPlanData()"

    # print(debugPath, ", dateCurrent: ", dateCurrent, ", type(dateCurrent): ", type(dateCurrent))
    # print(debugPath, ", dateStartStr: ", dateStartStr, ", type(dateStartStr): ", type(dateStartStr))
    # print(debugPath, ", dateEndStr: ", dateEndStr, ", type(dateEndStr): ", type(dateEndStr))
    # print(debugPath, ", revision: ", revision)
    # print(debugPath, ", sessionUserId: ", sessionUserId)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", ProductionPlanData Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", ProductionPlanData Database 연결을 확인하시오!")

    # print("2 ProductionPlanData dayStr: ", dayStr, ", monthStr: ", monthStr, ", yearStr: ", yearStr)
    # 2. ProductionPlanData.생산 계획 테이블은 해당 일자의 모든 [ScheduleQty] 값을 [0]으로 초기화한다.
    sql = "Select REVISION From PRODUCTIONPLANDATA WHERE REVISION = %s Order By REVISION Desc "
    values = revision

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", ProductionPlanData Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", ProductionPlanData Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("ProductionPlanData array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            pass
            # print(get_line_no(), ", ProductionPlanData array_sets_server: ")
            # 2021.05.11 Conclusion. 여기서는 자료의 존재 여부만 확인하는 것으로,
            # 자료가 존재하지 않으면, 다음 "업로드" 로직에서 자동으로 추가한다.
            # 이미 존재하면, 아래 else 문장에서, 기존 자료를 "0"으로 초기화한다.

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???

            # 해당 "날짜"만 초기화한다. "전체 날짜"를 모두 초기화할 필요는 없다.
            sql = "Update PRODUCTIONPLANDATA Set SCHEDULEQTY = %s, USERID = %s " \
                  "WHERE REVISION = %s AND SCHEDULE BETWEEN %s AND %s "
            values = (0, sessionUserId, revision, dateCurrent, dateCurrent)
            # print("2 __resetProductionPlanData values: ", values)
            cursArrayWeb.execute(sql, values)

        rs2 = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, ProductionPlanData [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rs2 = False

    if rs2:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), "ProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 성공!")
            rs2 = True
        except KeyboardInterrupt:
            rs2 = False
            mySqlWebDb.rollback()
            print(get_line_no(), "ProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")
    else:
        rs2 = False
        print(get_line_no(), ", __dbMrp.py ProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")

    return rs2


# 2021.06.20 Added. "작업 시간"을 추가하여, CS.생산 실적 정리할 때, 작업 시간을 끌고 가서 정리하게 한다.
def __confirmProductionPlanDate(sessionUserId, revision, dateCurrent, dateStartStr, dateEndStr, byYearMonthWeekDay):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    # debugPath = "__dbMrp.py __confirmProductionPlanDate()"

    # print(debugPath, ", dateCurrent: ", dateCurrent, ", type(dateCurrent): ", type(dateCurrent))
    # print(debugPath, ", dateStartStr: ", dateStartStr, ", type(dateStartStr): ", type(dateStartStr))
    # print(debugPath, ", dateEndStr: ", dateEndStr, ", type(dateEndStr): ", type(dateEndStr))
    # print(debugPath, ", revision: ", revision)
    # print(debugPath, ", sessionUserId: ", sessionUserId)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dbMrp.py Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")

    # print("2 ProductionPlanData dayStr: ", dayStr, ", monthStr: ", monthStr, ", yearStr: ", yearStr)
    # 2. ProductionPlanData.생산 계획 테이블은 해당 일자의 모든 [ScheduleQty] 값을 [0]으로 초기화한다.
    sql = "Select REVISION From PRODUCTIONPLANDATE WHERE REVISION = %s Order By REVISION Desc "
    values = revision

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dbMrp.py Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("PRODUCTIONPLANDATE array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            print(get_line_no(), ", __dbMrp.py PRODUCTIONPLANDATE row_sets_server is None!")

            # 2021.05.11 Conclusion. 여기서는 자료의 존재 여부만 확인하는 것으로,
            # 자료가 존재하지 않으면, 다음 "업로드" 로직에서 자동으로 추가한다.
            # 이미 존재하면, 아래 else 문장에서, 기존 자료를 "0"으로 초기화한다.

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???

            sql = "Update PRODUCTIONPLANDATE Set WORKEDTIMES = %s, FROMTIME = %s, TOTIME = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES1 = %s, PRODUCTIONPERFORMANCEQTIES2 = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES3 = %s, PRODUCTIONPERFORMANCEQTIES4 = %s, " \
                  "PRODUCTIONPERFORMANCEQTIES5 = %s, PRODUCTIONPERFORMANCEQTIES6 = %s, " \
                  "WORKEDTIMES1 = %s, WORKEDTIMES2 = %s, WORKEDTIMES3 = %s, " \
                  "WORKEDTIMES4 = %s, WORKEDTIMES5 = %s, WORKEDTIMES6 = %s, " \
                  "USERID = %s, MODIFIEDDATE = %s " \
                  "WHERE REVISION = %s AND WORKDATE BETWEEN %s AND %s "
            if byYearMonthWeekDay == "D":  # day
                # 해당 "날짜"만 초기화한다. "전체 기간"를 모두 초기화할 필요는 없다.
                values = (0, dateCurrent, dateCurrent, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          sessionUserId, dateCurrent, revision, dateCurrent, dateCurrent)  # 해당 날짜만 변경 *****
            elif byYearMonthWeekDay == "M":  # month
                # "전체 기간"를 모두 초기화 한다.
                values = (0, dateCurrent, dateCurrent, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          sessionUserId, dateCurrent, revision, dateStartStr, dateEndStr)
            else:
                values = (0, dateCurrent, dateCurrent, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          sessionUserId, dateCurrent, revision, dateCurrent, dateCurrent)  # 해당 날짜만 변경 *****
            # print(debugPath, ", values: ", values)

            cursArrayWeb.execute(sql, values)

        rs2 = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), ", __dbMrp.py2 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rs2 = False

    if rs2:
        try:
            mySqlWebDb.commit()
            # print("ProductionPlanDate: ", dateCurrent, " :: ", revision, " 서버 저장 성공!!! ")
            rtnRresult = True
        except KeyboardInterrupt:
            rtnRresult = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", __dbMrp.py ProductionPlanDate: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")
    else:
        rtnRresult = False

    return rtnRresult


def __confirmProductByDayPlanData(sessionUserId, revision, dateCurrent):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", _dbMrp.py Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", _dbMrp.py Database 연결을 확인하시오!")

    # print("3 __resetProductionPlanData dayStr: ", dayStr, ", monthStr: ", monthStr, ", yearStr: ", yearStr)
    # 3. ProductByDayPlanData.작업 지시 테이블은 해당 일자의 모든 [Mp,Ma,Mc,Production] 값을 [0]으로 초기화한다.
    sql = "Select REVISION From PRODUCTBYDAYPLANDATA WHERE REVISION = %s Order By REVISION Desc "
    values = revision

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", _dbMrp.py , Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", _dbMrp.py , Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("__resetProductionPlanData array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            print(get_line_no(), ", __dbMrp.py PRODUCTBYDAYPLANDATA array_sets_server: ")
            # print("3 __resetProductionPlanData array_sets_server: ", array_sets_server)
            # os.system("pause")

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???

            # 해당 "날짜"만 초기화한다. "전체 날짜"를 모두 초기화할 필요는 없다.
            # dateCurrentNext = dateCurrent.timedelta(days=1)
            # print("__resetProductionPlanData dateCurrentNext : ", dateCurrentNext)
            sql = "Update PRODUCTBYDAYPLANDATA Set MP = %s, MA = %s, MC = %s, PRODUCTION = %s, USERID = %s " \
                  "WHERE REVISION = %s AND PLANDATE BETWEEN %s AND %s "
            values = (0, 0, 0, 0, sessionUserId, revision, dateCurrent, dateCurrent)
            # print(get_line_no(), "PRODUCTBYDAYPLANDATA values: ", values)
            cursArrayWeb.execute(sql, values)

        # try:
        #     mySqlWebDb.commit()
        #     print("__resetProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 성공!!! ")
        # except KeyboardInterrupt:
        #     mySqlWebDb.rollback()
        #     print("__resetProductionPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패!!! ")

        rs3 = True

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        rs3 = False

    if rs3:
        try:
            mySqlWebDb.commit()
            # print(get_line_no(), "ProductByDayPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 성공!")
            rs3 = True
        except KeyboardInterrupt:
            rs3 = False
            mySqlWebDb.rollback()
            print(get_line_no(), "ProductByDayPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")
    else:
        rs3 = False
        print(get_line_no(), "ProductByDayPlanData: ", dateCurrent, " :: ", revision, " 서버 저장 실패! ")

    return rs3


# 1. Trade.거래처 테이블 자료 불러오기.
def __getTrade(sessionUserId):
    global CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
        mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    # 2021.05.06 Added. ***** mySqlWebDb3, cursArrayWeb3, CONNECTEDWEBAMS *****
    if CONNECTEDWEBAMS == False:
        # mySqlWebDb3, cursArrayWeb3, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME33 = connectWebAmsDB()
        mySqlWebDb3, cursArrayWeb3, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME33 = connectWebAmsMyDB()
        # print(get_line_no(), "mySqlWebDb3: ", mySqlWebDb3, "type(mySqlWebDb3):", type(mySqlWebDb3))
        # print(get_line_no(), "DBNAME33: ", DBNAME33, "type(DBNAME33):", type(DBNAME33))

        if type(mySqlWebDb3) is pymysql.connections.Connection or type(
                cursArrayWeb3) is pymysql.cursors.Cursor:
            CONNECTEDWEBAMS = True
            # print("0 __getTrade Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEBAMS = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # 1. Trade.거래처 정보 자료 불러오기. ***** connectWebAmsDB :: CONNECTEDWEBAMS *****
    sql = "Select ID, LANGUAGE1, LANGUAGE2, LANGUAGE3 From TRADE WHERE BEINUSE = 1 Order By ID "
    try:
        cursArrayWeb3.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb3.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEBAMS == False:
            # mySqlWebDb3, cursArrayWeb3, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME33 = connectWebAmsDB()
            mySqlWebDb3, cursArrayWeb3, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME33 = connectWebAmsMyDB()
            if type(mySqlWebDb3) is pymysql.connections.Connection or type(
                cursArrayWeb3) is pymysql.cursors.Cursor:
                CONNECTEDWEBAMS = True
                # print("00 __getTrade Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEBAMS = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb3.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb3.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            rtn = -1
            print(get_line_no(), "거래처 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        else:
            dfTrade = pd.DataFrame(array_sets_server)
            dfTrade.columns = ['TRADE', 'TRADE_ENG', 'TRADE_KOR', 'TRADE_LOC']
            dfTrade['TRADE'] = dfTrade['TRADE'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.

            # dfTrade.set_index('TRADE', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # 2021.05.17 Conclusion. 위와 같이 "set_index()" 처리를 하게 되면,
            # 바로 여기 문장을 실행할 때 에러가 발생한다.
            # jsonRecords = dfTrade.reset_index().to_json(orient='records')
            # 그러므로 이미 "sql" 문장에서 "ORDER BY"로 가져온 값이, 이미 "index"가 걸려 있으니까,
            # 여기서는 "set_index()" 하지 않도록 해야 한다.
            # 만약, 꼭 "set_index()"가 필요하면, 반드시 "inplace=False"로 처리해야 한다.
            dfTrade.set_index('TRADE', drop=False, inplace=False)  # drop 옵션은 반드시 False

            # print("__getTradeId dfTrade: \n", dfTrade.head(500))
            # print("__getTradeId dfTrade: \n", dfTrade.tail(20))
            # print(get_line_no(), "dfTrade: \n", dfTrade)
            # print(get_line_no(), "len(dfTrade): ", len(dfTrade))
        rtnResult = True
    except:
        rtnResult = False
        dfTrade = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, dfTrade


# 2. ReceivingOrder.수주 정보 자료 불러오기. "수주 날짜"가 아니라 "수주 번호"로 찿게 한다. "날짜"는 전월말경에 등록 가능.
def __getReceivingOrder(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3  #, \
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(get_line_no(), "mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")
    sql = "Select TRADER, RECEIVINGORDERNO FROM RECEIVINGORDER WHERE RECEIVINGORDERNO BETWEEN %s AND %s " \
          "ORDER BY RECEIVINGORDERNO Desc "
    values = (yearMonth + "0001", yearMonth + "9999")
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print(get_line_no(), "values: ", values)
        # print(get_line_no(), "array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            rtn = -2
            dfReceivingOrder = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            print(get_line_no(), "수주 정보가 없습니다. 관리자에게 문의하시오!", yearMonth)
            # os.system("pause")
        else:
            dfReceivingOrder = pd.DataFrame(array_sets_server)
            dfReceivingOrder.columns = ['TRADE', 'RECEIVING_ORDER_NO']
            dfReceivingOrder['RECEIVING_ORDER_NO'] = dfReceivingOrder['RECEIVING_ORDER_NO'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.
            # dfReceivingOrder['TRADE'] = dfReceivingOrder['TRADE'].str.strip()
            # 2021.04.14 ??? 이상하게도 자동으로 "code" 값으로 index가 되어있네... SQL 문장에서 "ORDER By Code"로 가져왔잖아...
            dfReceivingOrder.set_index('RECEIVING_ORDER_NO', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # print("__confirmReceivingOrder dfReceivingOrder: \n", dfReceivingOrder.head(500))
            # print("__confirmReceivingOrder dfReceivingOrder: \n", dfReceivingOrder.tail(20))
            # print(get_line_no(), "dfReceivingOrder: \n", dfReceivingOrder)
            # print(get_line_no(), "len(dfReceivingOrder): ", len(dfReceivingOrder))
        rtnResult = True
    except:
        rtnResult = False
        dfReceivingOrder = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "[callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, dfReceivingOrder


# 3. ReceivingOrderData.수주 상세 정보 자료 불러오기. "수주 날짜"가 아니라 "수주 번호"로 찿게 한다.
def __getReceivingOrderData(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3  #, \
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getReceivingOrderData mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select PK, CODE, RECEIVINGORDERNO, QTY FROM RECEIVINGORDERDATA WHERE RECEIVINGORDERNO " \
          "BETWEEN %s AND %s ORDER BY RECEIVINGORDERNO Desc "
    values = (yearMonth + "0001", yearMonth + "9999")
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # rtn = -3
            print(get_line_no(), "수주 상세 정보가 없습니다. 관리자에게 문의하시오!", yearMonth)
            columns = ['PK', 'CODE', 'RECEIVING_ORDER_NO', 'RECEIVING_ORDER_QTY', 'RECEIVING_ORDER_DATA_INFO']
            dfReceivingOrderData = pd.DataFrame(columns=columns)
            # print("__getReceivingOrderData 빈 df 생성 dfReceivingOrderData: ", dfReceivingOrderData)
            # print("__getReceivingOrderData 빈 df 생성 len(dfReceivingOrderData): ", len(dfReceivingOrderData))
        else:
            dfReceivingOrderData = pd.DataFrame(array_sets_server)
            dfReceivingOrderData.columns = ['PK', 'CODE', 'RECEIVING_ORDER_NO', 'RECEIVING_ORDER_QTY']
            dfReceivingOrderData['RECEIVING_ORDER_DATA_INFO'] \
                = dfReceivingOrderData['RECEIVING_ORDER_NO'] + " " + dfReceivingOrderData['CODE']
            dfReceivingOrderData['RECEIVING_ORDER_DATA_INFO'] \
                = dfReceivingOrderData['RECEIVING_ORDER_DATA_INFO'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.
            # 2021.04.14 자동으로 "CODE" 값으로 index가 되어 있음... SQL 문장에서 "ORDER By CODE"로 가져왔잖아...
            dfReceivingOrderData.set_index('RECEIVING_ORDER_DATA_INFO', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # print("__getReceivingOrderData dfReceivingOrderData: \n", dfReceivingOrderData.head(500))
            # print("__getReceivingOrderData dfReceivingOrderData: \n", dfReceivingOrderData.tail(20))
            # print("__getReceivingOrderData dfReceivingOrderData: \n", dfReceivingOrderData)
            # print("__getReceivingOrderData len(dfReceivingOrderData): ", len(dfReceivingOrderData))
        rtnResult = True
    except:
        rtnResult = False
        dfReceivingOrderData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "[callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, dfReceivingOrderData


# 4. 품목 마스터 정보 불러오기, 그 아래에는, def __getGoodsMasterInfo(dfGoodsMaster, code): 따로 있음.
def __getGoodsMaster(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getGoodsMaster mySqlWebDb: ", mySqlWebDb, "type(mySqdfGoodsMasterlWebDb):", type(mySqlWebDb))
        # print(get_line_no(), ", __dbMrp.py DBNAME3: ", DBNAME3, ", type(DBNAME3):", type(DBNAME3))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # todo: 2022.04.17 Conclusion. 언젠가 시간이 되면, 현재 사용중인 것만 부르는 것이 합리적인지 세밀히 확인하고, 그렇게 한다.
    sql = "Select CODE, STEP9, PROCESS, GOODS0, GOODS1, GOODS2, GOODS5, DESCRIPTION, COMPANYID " \
          "From GOODSMASTER Order By CODE "
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        # if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        if type(mySqlWebDb) is pymysql.connections.Connection or type(
            cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

        print(get_line_no(), "sql: ", sql)
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            rtn = -4
            print(get_line_no(), "품목 마스터 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        else:
            dfGoodsMaster = pd.DataFrame(array_sets_server)
            dfGoodsMaster.columns = ['CODE', 'STEP9', 'PROCESS', 'GOODS0', 'GOODS1', 'GOODS2', 'GOODS5', 'DESCRIPTION', 'COMPANYID']
            dfGoodsMaster['CODE'] = dfGoodsMaster['CODE'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.
            # dfGoodsMaster['code_string'] = str(dfGoodsMaster['code']).strip()  # str() 함수는 에러...
            # dfGoodsMaster['code_string'] = dfGoodsMaster['code'].strip()  # 여기는 에러고 반드시 아래와 같이 "str" 사용.
            dfGoodsMaster['CODE'] = dfGoodsMaster['CODE'].str.strip()
            # 2021.04.14 ??? 이상하게도 자동으로 "CODE" 값으로 index가 되어있네... SQL 문장에서 "ORDER By CODE"로 가져왔잖아...
            dfGoodsMaster.set_index('CODE', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # print("__getGoodsMaster dfGoodsMaster: \n", dfGoodsMaster.head(500))
            # print("__getGoodsMaster dfGoodsMaster: \n", dfGoodsMaster.tail(20))
            # print("__getGoodsMaster dfGoodsMaster: \n", dfGoodsMaster)
            # print("__getGoodsMaster len(dfGoodsMaster): ", len(dfGoodsMaster))

            # 2021.05.07 Conclusion. 여기서 "공백"을 반드시 모두 채워야 한다. 만약 어떤 컬럼 값에 "공백"이 있으면,
            # 아래와 같이 "CODE.품번"으로 검색할 때, 분명히 품번이 "존재"함에도, 찾지 못 하는, "심각한" 문제가 발생한다.
            # infoSeries = dfGoodsMaster[['STEP9', 'PROCESS', 'GOODS0', 'GOODS1', 'GOODS2', 'DESCRIPTION']]\
            #     .where(dfGoodsMaster['CODE'] == code).dropna()
            dfGoodsMaster = dfGoodsMaster.fillna(0)  # 모든 컬럼의 "NaN" 값을 먼저 [0]으로 채운 후, 타입을 변경한다.
            dfGoodsMaster = dfGoodsMaster.astype({"CODE": "str", "STEP9": "str", "PROCESS": "str"})

            # print(get_line_no(), ", __dbMrp.py dfGoodsMaster.tail(20): \n", dfGoodsMaster.tail(20))
            # # print("__getGoodsMaster dfGoodsMaster.dtypes: ", dfGoodsMaster.dtypes)
            # dfGoodsMasterStep9 = dfGoodsMaster.astype({'STEP9': str})  # 'STEP9' 컬럼을 강제로 'str' 타입으로 변경.
            # # print("1 __getGoodsMaster dfGoodsMasterStep9: \n", dfGoodsMasterStep9.head(100))
            #
            # # 특수 문자 제거한 컬럼(specification)을 추가.
            # dfGoodsMasterStep9['specification'] = dfGoodsMasterStep9['STEP9'].str.replace('[^\w]', ' ', regex=True)  #.reset_index()
            # # print("2 __getGoodsMaster dfGoodsMasterStep9: \n", dfGoodsMasterStep9.head(100))
            #
            # dfGoodsMasterStep9 = dfGoodsMasterStep9.fillna(0)  # 모든 컬럼의 "NaN" 값을 먼저 [0]으로 채운 후, 타입을 변경한다.
            # dfGoodsMasterStep9 = dfGoodsMasterStep9.astype({"CODE": "str", "STEP9": "str", "PROCESS": "str"})

            # rtn = 1  # 여기까지 문제없이 실행된 경우에만, [1]을 준다.
        rtnResult = True
    except:
        rtnResult = False
        dfGoodsMaster = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "[callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, dfGoodsMaster  #, dfGoodsMasterStep9


# 5. 2021.05.05 Created. GoodsMaster.품목 마스터 파일에서, "CODE.품번" 값으로, "품목 마스터 정보"를 얻는다.
# def __getGoodsMaster(yearMonth, sessionUserId): 이건 위에 따로 있음.
def __getGoodsMasterInfo(dfGoodsMaster, code):
    code = code.replace("-", "")
    # print("__getGoodsMasterInfo code: ", code)
    # print("__getGoodsMasterInfo len(code): ", len(code))
    # print("__getGoodsMasterInfo type(code): ", type(code))
    infoSeries = dfGoodsMaster[['STEP9', 'PROCESS', 'GOODS0', 'GOODS1', 'GOODS2', 'GOODS5', 'DESCRIPTION', 'COMPANYID']]\
        .where(dfGoodsMaster['CODE'] == str(code)).dropna()
    # 2021.05.07 Conclusion. 여기서 "공백"을 반드시 모두 채워야 한다. 만약 어떤 컬럼 값에 "공백"이 있으면,
    # 아래와 같이 "CODE.품번"으로 검색할 때, 분명히 품번이 "존재"함에도, 찾지 못 하는, "심각한" 문제가 발생한다.
    # infoSeries = dfGoodsMaster[['STEP9', 'DESCRIPTION']].where(dfGoodsMaster['CODE'] == code).dropna()
    # print("__getGoodsMasterInfo infoSeries: ", infoSeries)
    # print("__getGoodsMasterInfo type(infoSeries): ", type(infoSeries))
    # print("__getGoodsMasterInfo len(infoSeries): ", len(infoSeries))
    if len(infoSeries) > 0:
        step9 = infoSeries.values[0][0].strip()
        process = infoSeries.values[0][1].strip()
        goods0 = int(infoSeries.values[0][2])
        goods1 = int(infoSeries.values[0][3])
        goods2 = int(infoSeries.values[0][4])
        goods5 = int(infoSeries.values[0][5])
        description = int(infoSeries.values[0][6])
        companyid = int(infoSeries.values[0][7])
        # print(get_line_no(), "companyid: ", companyid, ", type(companyid): ", type(companyid))
        # process = ""
        # goods0 = 0
        # goods1 = 0
        # goods2 = 0
        # description = 0
        rs = 1
    else:
        # print("__getGoodsMasterInfo dfGoodsMaster: \n", dfGoodsMaster)
        # print("__getGoodsMasterInfo code: ", code)
        # print("__getGoodsMasterInfo len(code): ", len(code))
        # print("__getGoodsMasterInfo type(code): ", type(code))
        step9 = ""
        process = ""
        goods0 = 0
        goods1 = 0
        goods2 = 0
        goods5 = 0
        description = 0
        companyid = 0
        rs = -1

    return rs, step9, process, goods0, goods1, goods2, description, companyid


# 5. 2022.04.17 Created. GoodsMaster.품목 마스터 파일에서, 북경 조이 생산 일보 엑셀표상 'D열.CODE' 값과 'F열.工程名' 값으로,
# "CODE.품번" 정보를 얻는다.
def __getGoodsMasterCodeInfo(dfGoodsMaster, goods5, process):
    # goods5 = goods5.replace("-", "")
    print(get_line_no(), "dfGoodsMaster: \n", dfGoodsMaster)
    # print(get_line_no(), "dfGoodsMaster.tail(20): \n", dfGoodsMaster.tail(20))
    print(get_line_no(), "goods5: ", goods5, type(goods5))
    print(get_line_no(), "process: ", process, type(process))
    infoSeries = \
        dfGoodsMaster[['CODE', 'STEP9', 'PROCESS', 'GOODS0', 'GOODS1', 'GOODS2', 'GOODS5', 'DESCRIPTION']].where(
            (dfGoodsMaster['GOODS5'] == goods5) & (dfGoodsMaster['PROCESS'] == process)).dropna()
    # 2021.05.07 Conclusion. 여기서 "공백"을 반드시 모두 채워야 한다. 만약 어떤 컬럼 값에 "공백"이 있으면,
    # 아래와 같이 "CODE.품번"으로 검색할 때, 분명히 품번이 "존재"함에도, 찾지 못 하는, "심각한" 문제가 발생한다.
    # infoSeries = dfGoodsMaster[['STEP9', 'DESCRIPTION']].where(dfGoodsMaster['CODE'] == code).dropna()
    # print(get_line_no(), ", infoSeries: \n", infoSeries)
    # print(get_line_no(), " type(infoSeries): ", type(infoSeries))
    # print(get_line_no(), "len(infoSeries): ", len(infoSeries))
    if len(infoSeries) > 0:
        code = str(infoSeries.values[0][0]).strip()
        step9 = infoSeries.values[0][1].strip()
        process = infoSeries.values[0][2].strip()
        goods0 = int(infoSeries.values[0][3])
        goods1 = int(infoSeries.values[0][4])
        goods2 = int(infoSeries.values[0][5])
        goods5 = int(infoSeries.values[0][6])
        description = int(infoSeries.values[0][7])
        rs = 1
        # print(get_line_no(), ", code: ", code, ", step9: ", step9)
        # print(get_line_no(), ", process: ", process, ", description: ", description)
        # print(get_line_no(), ", goods0: ", goods0, ", goods1: ", goods1)
        # print(get_line_no(), ", goods2: ", goods2, ", goods5: ", goods5)
    else:
        print(get_line_no(), "dfGoodsMaster: \n", dfGoodsMaster)
        print(get_line_no(), "goods5: ", goods5, type(goods5))
        print(get_line_no(), "process: ", process, type(process))
        code = "0000000000"
        step9 = ""
        process = ""
        goods0 = 0
        goods1 = 0
        goods2 = 0
        goods5 = 0
        description = 0
        rs = -1
        print(get_line_no(), f"{goods5, process} 현재 품목에 대한 품번이 없습니다. 다시 확인하시오!")

    return rs, code, step9, process, goods0, goods1, goods2, goods5, description


# 1. Goods0.물품 대분류(차종) 정보 자료 불러오기.
def __getGoods0(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getGoods0 mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # 1. Goods0.차종 정보 자료 불러오기.
    # sql = "Select CODE From Machine WHERE BeInUse = 1 Order By CODE "
    sql = "Select ID, LANGUAGE1, LANGUAGE2, LANGUAGE3 From GOODS3 Order By ID "

    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            print(get_line_no(), ", Goods0.차종 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        dfGoods0 = pd.DataFrame(array_sets_server)
        dfGoods0.columns = ['GOODS0', 'GOODS0_ENG', 'GOODS0_KOR', 'GOODS0_LOC']
        # 2021.04.14 Conclusion. dfMachine 자료는 Language3을 기준으로 검색하는 관계로 index 하면 안 된다.
        dfGoods0.set_index('GOODS0', drop=False, inplace=True)  # drop 옵션은 반드시 False
        # print("__getGoods0 dfGoods0: \n", dfGoods0.head(20))
    except:
        CONNECTEDWEB = False
        dfGoods0 = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return CONNECTEDWEB, dfGoods0


# 2. Machine.작업반(설비) 정보 자료 불러오기.
def __getMachine(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3  # , \
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getMachine mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", Database 연결을 확인하시오!")

    # 2. Machine.설비 정보 자료 불러오기.
    sql = "Select CODE, LANGUAGE1, LANGUAGE2, LANGUAGE3, LINECODE From MACHINE WHERE BEINUSE = 1 Order By CODE "
    # sql = "Select CODE, LANGUAGE1, LANGUAGE2, LANGUAGE3, LINECODE From MACHINE Order By CODE "

    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            print(get_line_no(), ", 설비 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        dfMachine = pd.DataFrame(array_sets_server)
        dfMachine.columns = ['MACHINE', 'MACHINE_ENG', 'MACHINE_KOR', 'MACHINE_LOC', 'LINE_CODE']
        # dfMachine = dfMachine.astype({'MACHINE_ENG': str, 'MACHINE_KOR': str, 'MACHINE_LOC': str})
        # 2021.04.14 Conclusion. dfMachine 자료는 Language3을 기준으로 검색하는 관계로 index 하면 안 된다.
        # dfMachine.set_index('machine', drop=False, inplace=True)  # drop 옵션은 반드시 False
        # print(get_line_no(), ", __dbMrp.py dfMachine.tail(35): \n", dfMachine.tail(35))
    except:
        CONNECTEDWEB = False
        dfMachine = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return CONNECTEDWEB, dfMachine


# 2021.05.05 Created. Trade.거래처 테이블에서, "tradeCode.거래처 코드" 값으로, "거래처 정보"를 얻는다.
def __getTradeInfo(dfTrade, tradeId):
    # print("__getTradeInfo dfTrade: \n", dfTrade)
    # print("__getTradeInfo type(dfTrade): ", type(dfTrade))
    # print("__getTradeInfo len(dfTrade): ", len(dfTrade))

    # print("__getTradeInfo tradeId: ", tradeId, ", type(tradeId): ", type(tradeId))

    # dfTrade.columns = ['TRADE', 'trade_eng', 'trade_kor', 'trade_loc']
    infoSeries = dfTrade[['TRADE', 'TRADE_ENG', 'TRADE_KOR', 'TRADE_LOC']]\
        .where(dfTrade['TRADE'] == str(tradeId)).dropna()  # "tradeId" 타입이 "int"이면, 반드시 "str"로 찾아야 되네...
    # print("__getTradeInfo infoSeries: ", infoSeries)
    # print("__getTradeInfo type(infoSeries): ", type(infoSeries))
    # print("__getTradeInfo len(infoSeries): ", len(infoSeries))
    if len(infoSeries) > 0:
        tradeId = int(infoSeries.values[0][0])
        tradeEng = infoSeries.values[0][1].strip()
        tradeKor = infoSeries.values[0][2].strip()
        tradeLoc = infoSeries.values[0][3].strip()
        rs = 1
    else:
        tradeId = ""
        tradeEng = ""
        tradeKor = 0
        tradeLoc = 0
        rs = -1

    # print("__getTradeInfo rs: ", rs, ", tradeId: ", tradeId, ", tradeKor: ", tradeKor)

    return rs, tradeId, tradeEng, tradeKor, tradeLoc


# StockWarehouseLot.재고 정보 불러오기, 그 아래에는, def __getStockWarehouseLotInfo(dfStockWarehouseLot, code): 따로 있음.
def __getStockWarehouseLot(yearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getStockWarehouseLot mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    sql = "Select CODE, WAREHOUSE, LOTNO, BEGINNING, INCOMING, OUTGOING, UP, BEGINNINGING, INCOMINGING, OUTGOINGING " \
          "From STOCKWAREHOUSELOT Order By CODE, WAREHOUSE, LOTNO "
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            rtn = -4
            print(get_line_no(), ", __dfMrp.py 품목 마스터 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        else:
            dfStockWarehouseLot = pd.DataFrame(array_sets_server)
            dfStockWarehouseLot.columns = ['CODE', 'WAREHOUSE', 'LOTNO', 'BEGINNING', 'INCOMING', 'OUTGOING', 'UP',
                                           'BEGINNINGING', 'INCOMINGING', 'OUTGOINGING']
            dfStockWarehouseLot['CODE'] = dfStockWarehouseLot['CODE'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.
            # dfStockWarehouseLot['CODE_string'] = str(dfStockWarehouseLot['CODE']).strip()  # str() 함수는 에러...
            # dfStockWarehouseLot['CODE_string'] = dfStockWarehouseLot['CODE'].strip()  # 여기는 에러고 반드시 아래와 같이 "str" 사용.
            dfStockWarehouseLot['CODE'] = dfStockWarehouseLot['CODE'].str.strip()
            # 2021.04.14 ??? 이상하게도 자동으로 "CODE" 값으로 index가 되어있네... SQL 문장에서 "ORDER By CODE"로 가져왔잖아...
            dfStockWarehouseLot.set_index('CODE', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # print("__getStockWarehouseLot dfStockWarehouseLot: \n", dfStockWarehouseLot.head(500))
            # print("__getStockWarehouseLot dfStockWarehouseLot: \n", dfStockWarehouseLot.tail(20))
            # print("__getStockWarehouseLot dfStockWarehouseLot: \n", dfStockWarehouseLot)
            # print("__getStockWarehouseLot len(dfStockWarehouseLot): ", len(dfStockWarehouseLot))

            # 2021.05.07 Conclusion. 여기서 "공백"을 반드시 모두 채워야 한다. 만약 어떤 컬럼 값에 "공백"이 있으면,
            # 아래와 같이 "CODE.품번"으로 검색할 때, 분명히 품번이 "존재"함에도, 찾지 못 하는, "심각한" 문제가 발생한다.
            # infoSeries = dfStockWarehouseLot[['STEP9', 'PROCESS', 'GOODS0', 'GOODS1', 'GOODS2', 'DESCRIPTION']]\
            #     .where(dfStockWarehouseLot['CODE'] == code).dropna()
            dfStockWarehouseLot = dfStockWarehouseLot.fillna(0)  # 모든 컬럼의 "NaN" 값을 먼저 [0]으로 채운 후, 타입을 변경한다.
            dfStockWarehouseLot = dfStockWarehouseLot.astype({"CODE": "str", "WAREHOUSE": "str", "LOTNO": "str"})

            # # print("__getStockWarehouseLot dfStockWarehouseLot: \n", dfStockWarehouseLot.head(100))
            # # print("__getStockWarehouseLot dfStockWarehouseLot.dtypes: ", dfStockWarehouseLot.dtypes)
            # dfGoodsMasterStep9 = dfStockWarehouseLot.astype({'STEP9': str})  # 'STEP9' 컬럼을 강제로 'str' 타입으로 변경.
            # # print("1 __getStockWarehouseLot dfGoodsMasterStep9: \n", dfGoodsMasterStep9.head(100))
            #
            # # 특수 문자 제거한 컬럼(specification)을 추가.
            # dfGoodsMasterStep9['specification'] = dfGoodsMasterStep9['STEP9'].str.replace('[^\w]', ' ', regex=True)  #.reset_index()
            # # print("2 __getStockWarehouseLot dfGoodsMasterStep9: \n", dfGoodsMasterStep9.head(100))
            #
            # dfGoodsMasterStep9 = dfGoodsMasterStep9.fillna(0)  # 모든 컬럼의 "NaN" 값을 먼저 [0]으로 채운 후, 타입을 변경한다.
            # dfGoodsMasterStep9 = dfGoodsMasterStep9.astype({"CODE": "str", "STEP9": "str", "PROCESS": "str"})

            # rtn = 1  # 여기까지 문제없이 실행된 경우에만, [1]을 준다.
        rtnResult = True

    except:
        rtnResult = False
        dfStockWarehouseLot = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", 경고, __getStockWarehouseLot [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, dfStockWarehouseLot


# 2021.05.05 Created. ShippingOrderData.출하 지시 정보 테이블의 (틀정 출하 지시 번호::차수)
# 여기서는 그냥 단순하게, ShippingOrderNo::Sequence로 검색해서, 해당 자료가 있으면,
# 해당 자료의 "SHIPPEDQTY" 컬럼은 "0"으로, "SHIPPEDBAL" 컬럼도 "0"으로 초기화한다.
def __getShippingOrderDataSelected(shippingOrderNo, tradeId, sequence, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getShippingOrderDataSelected mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    sql = "Select SHIPPINGORDERNO, TRADER, SEQUENCE From SHIPPINGORDERDATA " \
          "WHERE SHIPPINGORDERNO = %s AND TRADER = %s AND SEQUENCE = %s Order By SHIPPINGORDERNO DESC "
    values = (shippingOrderNo, tradeId, sequence)
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("__getShippingOrderDataSelected array_sets_server.count() : ", row_count_server)
        # print("__getShippingOrderDataSelected values : ", values)
        if array_sets_server is None or row_count_server < 1:
            dfShippingOrderData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            print(get_line_no(), "SHIPPINGORDERDATA 정보가 없습니다!")
            print(get_line_no(), "shippingOrderNo: ", shippingOrderNo, ", tradeId: ", tradeId, " sequence: ", sequence)
        else:
            dfShippingOrderData = pd.DataFrame(array_sets_server)
            # dfShippingOrderData.columns = ['SHIPPINGORDERNO', 'SEQUENCE']
            if len(dfShippingOrderData) > 0:
                sql = "Update SHIPPINGORDERDATA Set SHIPPEDQTY = %s, SHIPPEDBAL = %s " \
                      "Where SHIPPINGORDERNO = %s AND TRADER = %s AND SEQUENCE = %s AND PERSONALID = %s"
                values = (0, 0, shippingOrderNo, tradeId, sequence, sessionUserId)
                cursArrayWeb.execute(sql, values)

                # todo: 2022.06.13 Conclusion. 아래 '커밋'과 '롤백'과 같이, 데이터베이스를 핸들링하는 것은,
                #  '행=로우=레코드'로 처리하면, 브라우져의 대기 시간을 초과하여. '에러'를 뿌리는,
                #  치명적인 시간이 소요될 수가 있으므로,
                #  모든 '행=로우'를 처리한 후에, 원시 펑션에서 반드시 '한번 만' 커밋 또는 롤백하도록 해야한다.
                # try:
                #     mySqlWebDb.commit()
                #     print(shippingOrderNo, " :: ", sequence, " 서버 저장 성공!!! __getShippingOrderDataSelected()")
                #     rtnResult = True
                # except KeyboardInterrupt:
                #     rtnResult = False
                #     mySqlWebDb.rollback()
                #     print(shippingOrderNo, " :: ", sequence, " 서버 저장 실패!!! __getShippingOrderDataSelected()")

        # print(get_line_no(), "shippingOrderNo: ", shippingOrderNo, ", tradeId: ", tradeId, ", sequence: ", sequence)
        rtnResult = True

    except:
        rtnResult = False
        dfShippingOrderData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, mySqlWebDb


# 2021.05.05 Created. Shipping.출하 정보 테이블의 (틀정 출하 번호::차수)
# 여기서는 그냥 단순하게, ShippingNo::Sequence로 검색해서, 해당 자료가 있으면,
# 해당 자료의 "IvoiceNo" 컬럼은 "공백 문자"로, "InvoiceAmount" 컬럼은 "0"으로,  "BUYER2" 컬럼은 "공백 문자"로 초기화한다.
# ===> 그런데, 여기 Shipping 테이블은 "ShippingNo" 컬럼이 "Primary Key"이므로, 굳이 여기서 초기화 하지 않아도 된다.
# def __getShippingSelected(shippingNo, tradeId, sequence, sessionUserId):


# 2021.05.05 Created. ShippingData.출하 상세 정보 테이블의 (틀정 출하 번호::차수)
# 여기서는 그냥 단순하게, ShippingNo::Sequence로 검색해서, 해당 자료가 있으면,
# 해당 자료의 "SHIPPEDQTY" 컬럼은 "0"으로, "SHIPPEDBAL" 컬럼도 "0"으로, "LOTNO" 컬럼은 "공백 문자"로 초기화한다.
def __getShippingDataSelected(shippingNo, tradeId, sequence, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3  #, \
        # mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getShippingDataSelected mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    sql = "Select SHIPPINGNO, SEQUENCE From SHIPPINGDATA " \
          "WHERE SHIPPINGNO = %s AND SEQUENCE = %s Order By SHIPPINGNO DESC "
    values = (shippingNo, sequence)  # TRADER 컬럼이 없네.
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            dfShippingData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            print("SHIPPINGDATA 정보가 없습니다!")
        else:
            dfShippingData = pd.DataFrame(array_sets_server)
            # dfShippingData.columns = ['shippingno', 'SEQUENCE']
            if len(dfShippingData) > 0:
                sql = "Update SHIPPINGDATA Set SHIPPEDQTY = %s, SHIPPEDBAL = %s, LOTNO = '' " \
                      "Where SHIPPINGNO = %s AND SEQUENCE = %s "
                values = (0, 0, shippingNo, sequence)
                cursArrayWeb.execute(sql, values)
                # todo: 2022.06.13 Conclusion. 아래 '커밋'과 '롤백'과 같이, 데이터베이스를 핸들링하는 것은,
                #  '행=로우=레코드'로 처리하면, 브라우져의 대기 시간을 초과하여. '에러'를 뿌리는,
                #  치명적인 시간이 소요될 수가 있으므로,
                #  모든 '행=로우'를 처리한 후에, 원시 펑션에서 반드시 '한번 만' 커밋 또는 롤백하도록 해야한다.
                # try:
                #     mySqlWebDb.commit()
                #     # print(shippingNo, " :: ", sequence, " 서버 저장 성공!!! __getShippingDataSelected()")
                #     rtnResult = True
                # except KeyboardInterrupt:
                #     rtnResult = False
                #     mySqlWebDb.rollback()
                #     print(shippingNo, " :: ", sequence, " 서버 저장 실패!!! __getShippingDataSelected()")
        # print(get_line_no(), "shippingNo: ", shippingNo, ", sequence: ", sequence)
        rtnResult = True

    except:
        rtnResult = False
        dfShippingData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, mySqlWebDb


# 2021.05.05 Created. ShippingOrderData.출하 지시 정보 테이블 (틀정 출하 지시 번호::차수) 등록
# ShippingOrderNo::TRADER::Sequence::Code로 검색해서, 해당 자료가 있으면, "Update", 없으면, "Insert" 한다.
# "SHIPPEDQTY", "SHIPPEDBAL"
def __setShippingOrderDataSelected(receivingOrderNo, shippingOrderNo, shippingNo, shippingDate, tradeId, code,
                                   dayNight, lotNo, sequence, shippingQty, shippedBal, unitPrice, warehouse, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getShippingOrderDataSelected mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select SHIPPINGORDERNO, TRADER, SEQUENCE, CODE From SHIPPINGORDERDATA " \
          "WHERE SHIPPINGORDERNO = %s AND TRADER = %s AND SEQUENCE = %s AND CODE = %s Order By SHIPPINGORDERNO DESC "
    values = (shippingOrderNo, tradeId, sequence, code)
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("__setShippingOrderDataSelected array_sets_server.count() : ", row_count_server)
        # print("__setShippingOrderDataSelected values : ", values)
        if array_sets_server is None or row_count_server < 1:
            # dfShippingOrderData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            # print("__setShippingOrderDataSelected 정보가 없습니다!")
            sql = "Insert Into SHIPPINGORDERDATA (SEQUENCE, RECEIVINGORDERNO, SHIPPINGORDERNO, SHIPPINGORDERDATE, " \
                  "DAYNIGHT, TRADER, CODE, UP, SHIPPEDQTY, SHIPPEDBAL, PERSONALID, LOTNO) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s) "
            values = (sequence, receivingOrderNo, shippingOrderNo, shippingDate,
                      dayNight, tradeId, code, unitPrice, shippingQty, shippedBal, sessionUserId, lotNo)
            # print("1 __setShippingOrderDataSelected values: ", values)
            result = cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print("1 __setShippingOrderDataSelected result: ", result)
        else:
            # dfShippingOrderData = pd.DataFrame(array_sets_server)
            # dfShippingOrderData.columns = ['shippingorderno', 'sequence']
            # if len(dfShippingOrderData) > 0:
            sql = "Update SHIPPINGORDERDATA Set UP = %s, SHIPPEDQTY = %s, SHIPPEDBAL = %s, LOTNO = %s " \
                  "Where SHIPPINGORDERNO = %s AND TRADER = %s AND SEQUENCE = %s AND CODE = %s AND PERSONALID = %s "
            values = (unitPrice, shippingQty, shippedBal, lotNo,
                      shippingOrderNo, tradeId, sequence, code, sessionUserId)
            # print("2 __setShippingOrderDataSelected values: ", values)
            result = cursArrayWeb.execute(sql, values)
            # print("2 __setShippingOrderDataSelected result: ", result)

        # todo: 2022.06.13 Conclusion. 아래 '커밋'과 '롤백'과 같이, 데이터베이스를 핸들링하는 것은,
        #  '행=로우=레코드'로 처리하면, 브라우져의 대기 시간을 초과하여. '에러'를 뿌리는,
        #  치명적인 시간이 소요될 수가 있으므로,
        #  모든 '행=로우'를 처리한 후에, 원시 펑션에서 반드시 '한번 만' 커밋 또는 롤백하도록 해야한다.
        # try:
        #     mySqlWebDb.commit()
        #     # print(shippingOrderNo, " :: ", sequence, " 서버 저장 성공!!! __setShippingOrderDataSelected()")
        #     rtnResult = True
        # except KeyboardInterrupt:
        #     rtnResult = False
        #     mySqlWebDb.rollback()
        #     print(shippingOrderNo, " :: ", sequence, " 서버 저장 실패!!! __setShippingOrderDataSelected()")

        # print(get_line_no(), "shippingOrderNo: ", shippingOrderNo, ", tradeId: ", tradeId, ", sequence: ", sequence)
        rtnResult = True

    except:
        rtnResult = False
        # dfShippingOrderData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, mySqlWebDb


# 2021.05.05 Created. Shipping.출하 정보 테이블 (틀정 출하 번호::차수) 등록.
# ShippingNo::BUYER2::Sequence로 검색해서, 해당 자료가 있으면, "Update", 없으면, "Insert" 한다.
# "IvoiceNo", "InvoiceAmount", "BUYER2"
# 여기서는 그냥 단순하게, ShippingNo::Sequence로 검색해서, 해당 자료가 있으면,
# 해당 자료의 "IvoiceNo" 컬럼은 "공백 문자"로, "InvoiceAmount" 컬럼은 "0"으로,  "BUYER2" 컬럼은 "공백 문자"로 초기화한다.
# ===> 그런데, 여기 Shipping 테이블은 "ShippingNo" 컬럼이 "Primary Key"이므로, 굳이 여기서 초기화 하지 않아도 된다.
def __setShippingSelected(receivingOrderNo, shippingOrderNo, shippingNo, shippingDate, tradeId, code,
                          dayNight, lotNo, sequence, shippingQty, unitPrice, warehouse, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__setShippingSelected mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select SHIPPINGNO, BUYER2, SEQUENCE From SHIPPING " \
          "WHERE SHIPPINGNO = %s AND BUYER2 = %s AND SEQUENCE = %s Order By SHIPPINGNO DESC "
    values = (shippingNo, tradeId, sequence)
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("__setShippingSelected array_sets_server.count() : ", row_count_server)
        # print("__setShippingSelected values : ", values)
        if array_sets_server is None or row_count_server < 1:
            # dfShipping = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            # rtnResult = True
            # print("__setShippingSelected 정보가 없습니다!")
            sql = "Insert Into SHIPPING (SEQUENCE, RECEIVINGORDERNO, SHIPPINGORDERNO, SHIPPINGNO, SHIPPINGDATE, " \
                  "DAYNIGHT, INVOICENO, DEPARTUREDATE, BUYER2) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s) "
            values = (sequence, receivingOrderNo, shippingOrderNo, shippingNo, shippingDate,
                      dayNight, shippingNo, shippingDate, tradeId)  # 송장 번호도 출하 번호로 한다.
            # print("1 __setShippingSelected values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print("1 __setShippingSelected cursArrayWeb: ", cursArrayWeb)
        else:
            # dfShipping = pd.DataFrame(array_sets_server)
            # dfShipping.columns = ['shippingno', 'sequence']
            # if len(dfShipping) > 0:
            sql = "Update SHIPPING Set RECEIVINGORDERNO = %s, SHIPPINGORDERNO = %s, INVOICENO = %s, " \
                  "DEPARTUREDATE = %s Where SHIPPINGNO = %s AND BUYER2 = %s AND SEQUENCE = %s "
            values = (receivingOrderNo, shippingOrderNo, shippingNo, shippingDate, shippingNo, tradeId, sequence)
            cursArrayWeb.execute(sql, values)

        # todo: 2022.06.13 Conclusion. 아래 '커밋'과 '롤백'과 같이, 데이터베이스를 핸들링하는 것은,
        #  '행=로우=레코드'로 처리하면, 브라우져의 대기 시간을 초과하여. '에러'를 뿌리는,
        #  치명적인 시간이 소요될 수가 있으므로,
        #  모든 '행=로우'를 처리한 후에, 원시 펑션에서 반드시 '한번 만' 커밋 또는 롤백하도록 해야한다.
        # try:
        #     mySqlWebDb.commit()
        #     # print(shippingNo, " :: ", sequence, " 서버 저장 성공!!! __setShippingSelected()")
        #     rtnResult = True
        # except KeyboardInterrupt:
        #     rtnResult = False
        #     mySqlWebDb.rollback()
        #     print(shippingNo, " :: ", sequence, " 서버 저장 실패!!! __setShippingSelected()")

        # print(get_line_no(), "shippingNo: ", shippingNo, ", tradeId: ", tradeId, ", sequence: ", sequence)
        rtnResult = True

    except:
        CONNECTEDWEB = False
        rtnResult = False
        # dfShipping = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, mySqlWebDb


# 2021.05.05 Created. ShippingData.출하 상세 정보 테이블 (틀정 출하 번호::차수) 등록.
# "ShippingNo::Sequence::Code::Warehouse" 로 검색해서, 해당 자료가 없으면, "Insert", 있으면, "Update" 한다.
# "PERSONALID", "Code", "ShippingNo", "Sequence", "SHIPPEDQTY", "SHIPPEDBAL", "LotNo", "Warehouse"
def __setShippingDataSelected(receivingOrderNo, shippingOrderNo, shippingNo, shippingDate, tradeId, code,
                              dayNight, lotNo, sequence, shippingQty, shippedBal, unitPrice, warehouse, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__setShippingDataSelected mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or \
                type(cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select SHIPPINGNO, SEQUENCE, CODE, WAREHOUSE, LOTNO From SHIPPINGDATA " \
          "WHERE SHIPPINGNO = %s AND SEQUENCE = %s AND CODE = %s AND WAREHOUSE = %s " \
          "Order By SHIPPINGNO, SEQUENCE, CODE, WAREHOUSE DESC "
    values = (shippingNo, sequence, code, warehouse)
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or \
                    type(cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print("__setShippingDataSelected array_sets_server.count() : ", row_count_server)
        # print("__setShippingDataSelected values : ", values)
        if array_sets_server is None or row_count_server < 1:
            # dfShippingData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            # print("__setShippingDataSelected 정보가 없습니다!")
            sql = "Insert Into SHIPPINGDATA (SEQUENCE, PERSONALID, RECEIVINGORDERNO, SHIPPINGORDERNO, " \
                  "SHIPPINGNO, SHIPPINGDATE, DAYNIGHT, CODE, SHIPPEDQTY, SHIPPEDBAL, UP, LOTNO, WAREHOUSE) " \
                  "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s) "
            values = (sequence, sessionUserId, receivingOrderNo, shippingOrderNo,
                      shippingNo, shippingDate, dayNight, code, shippingQty, shippedBal, unitPrice, lotNo, warehouse)
            # print("1 __setShippingDataSelected values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print("1 __setShippingDataSelected sql: ", sql)
        else:
            # dfShippingData = pd.DataFrame(array_sets_server)
            # dfShippingData.columns = ['shippingno', 'sequence']
            # if len(dfShippingData) > 0:
            sql = "Update SHIPPINGDATA Set PERSONALID = %s, RECEIVINGORDERNO = %s, SHIPPINGORDERNO = %s, " \
                  "SHIPPINGDATE = %s, DAYNIGHT = %s, SHIPPEDQTY = %s, SHIPPEDBAL = %s, UP = %s, LOTNO = %s " \
                  "Where SHIPPINGNO = %s AND SEQUENCE = %s AND CODE = %s AND WAREHOUSE = %s "
            values = (sessionUserId, receivingOrderNo, shippingOrderNo, shippingDate, dayNight,
                      shippingQty, shippedBal, unitPrice, lotNo, shippingNo, sequence, code, warehouse)
            # print("2 __setShippingDataSelected values: ", values)
            cursArrayWeb.execute(sql, values)
            # print("2 __setShippingDataSelected sql: ", values)
            # print("2 __setShippingDataSelected shippingQty: ", shippingQty)
            # print("2 __setShippingDataSelected unitPrice: ", unitPrice)

        # todo: 2022.06.13 Conclusion. 아래 '커밋'과 '롤백'과 같이, 데이터베이스를 핸들링하는 것은,
        #  '행=로우=레코드'로 처리하면, 브라우져의 대기 시간을 초과하여. '에러'를 뿌리는,
        #  치명적인 시간이 소요될 수가 있으므로,
        #  모든 '행=로우'를 처리한 후에, 원시 펑션에서 반드시 '한번 만' 커밋 또는 롤백하도록 해야한다.
        # try:
        #     mySqlWebDb.commit()
        #     # print(shippingNo, " :: ", sequence, " 서버 저장 성공!!! __setShippingDataSelected()")
        #     rtnResult = True
        # except KeyboardInterrupt:
        #     rtnResult = False
        #     mySqlWebDb.rollback()
        #     print(shippingNo, " :: ", sequence, " 서버 저장 실패!!! __setShippingDataSelected()")

        # print(get_line_no(), "shippingNo: ", shippingNo, ",  sequence: ", sequence, ", code: ", code)
        rtnResult = True

    except:
        rtnResult = False
        # dfShippingData = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rtnResult, mySqlWebDb


# 2021.05.05 Created. ReceivingOrder.수주 정보 테이블의 현재 년월도 자료중에서, "tradeId.거래처 코드"로 등록된
# "ReceivingOrder.수주 정보"를 얻는다. 목적은 tradeId에 맞는 "RECEIVINGORDERNO"만 리턴해 주면 된다.
# 2021.05.19 Added. 만약 없으면, 추가한다. 기준: yearMonth + "0000" : 해당 년월도 등록된 수주번호 끝 4자리 마지막 다음 번호로.
def __getReceivingOrderInfo(dfReceivingOrder, tradeId, yearMonth, sessionUserId):
    # global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
    #     mySqlWebDb3, cursArrayWeb3, DBNAME33, CONNECTEDWEBAMS
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
    # print(get_line_no(), "tradeId: ", tradeId, ", yearMonth: ", yearMonth, ", sessionUserId:, ", sessionUserId)

    dfReceivingOrder.columns = ['TRADE', 'RECEIVING_ORDER_NO']
    infoSeries = dfReceivingOrder['RECEIVING_ORDER_NO'].where(dfReceivingOrder['TRADE'] == tradeId).dropna()
    # print(get_line_no(), "infoSeries: \n", infoSeries)
    # print(get_line_no(), "type(infoSeries): ", type(infoSeries))
    # print(get_line_no(), "len(infoSeries): ", len(infoSeries))
    if len(infoSeries) > 0:
        receivingOrderNo = infoSeries.values[0].strip()
        rs = 1
    else:
        # 2021.05.19 Added. 만약 없으면, 추가한다. 기준: yearMonth + "0000" : 해당 년월도 등록된 수주번호 끝 4자리 마지막 다음 번호로.
        # sql = "Select RECEIVINGORDERNO From ReceivingOrder " \
        #       "WHERE LEFT(RECEIVINGORDERNO, 6) = %s ORDER BY RECEIVINGORDERNO Desc "
        # sql = "Select TOP 1 RECEIVINGORDERNO AS RECEIVINGORDERNOLast From ReceivingOrder " \
        #       "WHERE SUBSTRING (RECEIVINGORDERNO, 1, 6) = %s AND TRADER = %s ORDER BY RECEIVINGORDERNO Desc "

        # 2021.05.19 Conclusion. 위의 "AND TRADER = %s" 구문을 넣으면, 절대로 절대로 안 된다.
        # 여기서는 "TRADERr.거래처"와 상관 없이, 해당 "년월도"의 마지막 "수주 일련 번호" 값을 얻기 위함이기 때문이다.
        # sql = "Select TOP 1 RECEIVINGORDERNO AS receivingordernolatest From RECEIVINGORDER " \
        #       "WHERE SUBSTRING(RECEIVINGORDERNO, 1, 6) = %s ORDER BY RECEIVINGORDERNO Desc "
        sql = "Select RECEIVINGORDERNO From RECEIVINGORDER " \
              "WHERE SUBSTRING(RECEIVINGORDERNO, 1, 6) = %s ORDER BY RECEIVINGORDERNO Desc "
        values = yearMonth
        try:
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        except:  # DB 연결을 한 번 더 시도...
            if CONNECTEDWEB == False:
                mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
                BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
                if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                    CONNECTEDWEB = True
                    # print("33 __getReceivingOrderInfo Database 연결 성공!")
                else:
                    rs = -1
                    CONNECTEDWEB = False
                    print(get_line_no(), "Database 연결을 확인하시오!")
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        try:
            array_sets_server = cursArrayWeb.fetchall()
            row_count_server = len(array_sets_server)
            # print(get_line_no(), "array_sets_server : ", array_sets_server)  # [('2020110001',)]
            # print(get_line_no(), "array_sets_server.count() : ", row_count_server)

            receivingOrderDate = yearMonth[:4] + "-" + yearMonth[4:6] + "-01"
            if array_sets_server is None or row_count_server < 1:
                receivingOrderNo = yearMonth + "0001"
                # print(get_line_no(), "receivingOrderNo: ", receivingOrderNo, ", tradeId: ", tradeId)
            else:
                # todo: 2021.05.19 Conclusion. cursArrayWeb.fetchall()로 받은 "array_sets_server" 값을 읽을 때는,
                #  특별히, 반드시, 절대로 주의해야 한다. 아래와 같이 바로 "array_sets_server[0]" 이런식으로 읽으면 안 되고,
                #  ***** for 문으로 1개의 "row"를 가져와서, 거기서 "row[x]"로 읽어야 됨에 특히 주의 할 것 *****
                # receivingOrderNoLatest = array_sets_server[0]  # ('2020110001',) 값 양쪽에 (', ',) 문자가 포함되어 있다.
                # print("0 __getReceivingOrderInfo receivingOrderNoLatest: ", receivingOrderNoLatest)
                # receivingOrderNoLatest = array_sets_server["receivingOrderNoLatest"]  # 이렇게는 값을 못 가져오네...
                for row in array_sets_server:
                    receivingOrderNoLatest = row[0]
                    # print(get_line_no(), "한 번만 읽고 빠진다. receivingOrderNoLatest: ", receivingOrderNoLatest)
                    break  # 한 번만 읽고 바로 break 한다. 위에서 "Select Top 1"로 가져왔으므로.
                newSerialNo = str(int(receivingOrderNoLatest[-4:]) + 1).zfill(4)
                receivingOrderNo = receivingOrderNoLatest[:6] + newSerialNo
                # print(get_line_no(), "한 번만 읽고 빠진다. receivingOrderNo: ", receivingOrderNo,
                #       ", newSerialNo: ", newSerialNo)

            # print(get_line_no(), "tradeId: ", tradeId, ", type(tradeId): ", type(tradeId))
            sql = "Insert Into RECEIVINGORDER " \
                  "(RECEIVINGORDERNO, RECEIVINGORDERDATE, TRADER, TRADERORDERNO, USERID) Values (%s,%s,%s,%s,%s) "
            values = (receivingOrderNo, receivingOrderDate, tradeId, receivingOrderNo, sessionUserId)
            # print(get_line_no(), "values: ", values)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print(get_line_no(), "cursArrayWeb: ", cursArrayWeb)

            try:
                mySqlWebDb.commit()
                rs = 1
                # print(receivingOrderNo, " :: ", tradeId, " 서버 저장 성공!!! __getReceivingOrderInfo()")
            except KeyboardInterrupt:
                rs = -1
                mySqlWebDb.rollback()
                print(get_line_no(), ", ", receivingOrderNo, " :: ", tradeId, " 서버 저장 실패!!! ")
            # print(get_line_no(), "receivingOrderNo: ", receivingOrderNo, ", tradeId: ", tradeId)

        except:
            CONNECTEDWEB = False
            rs = -1
            receivingOrderNo = ""
            print(get_line_no(), "[callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rs, receivingOrderNo


# 2021.05.05 Created. ReceivingOrderData.수주 상세 정보 테이블의 현재 년월도 자료중에서,
# "receivingOrderNo.수주 번호 + code.품번"으로 등록된 "ReceivingOrderData.수주 상세 자료"를 검색하고,
# 없으면, "강제 등록" 한다.
# def __getReceivingOrderDataInfo(mySqlWebDb, cursArrayWeb, CONNECTEDWEB, dfReceivingOrderData, receivingOrderNo,
def __getReceivingOrderDataInfo(dfReceivingOrderData, receivingOrderNo, code, step9, shippingQtyTotal, unitPrice,
                                sessionUserId, yearMonth):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    # dfReceivingOrderData.columns = ['PK', 'CODE', 'RECEIVING_ORDER_NO', 'RECEIVING_ORDER_QTY', 'RECEIVING_ORDER_DATA_INFO']

    # print(get_line_no(), "receivingOrderNo: ", receivingOrderNo)
    # print(get_line_no(), "code: ", code)
    # print(get_line_no(), "dfReceivingOrderData: \n", dfReceivingOrderData)

    # 초기값으로 [rs = 1]을 주고, 수주 상세 자료에 해당 자료가 있으면, [rs = 1],
    # 없으면, 해당 자료를 아예 ReceivingOrderData.수주 상세 자료에 추가하고,
    # 추가에 성공하면 [rs = 1], 실패하면, [rs = -1]을 리턴한다.
    rs = 1
    receivingOrdeDataInfo = receivingOrderNo + " " + code
    # 아래 "dfReceivingOrderData" 자료는 이미 "sql"에서 "해당 월도" 자료만 불러와진 상태.
    receivingOrderDataSeries = dfReceivingOrderData['RECEIVING_ORDER_DATA_INFO'].where(
        dfReceivingOrderData['RECEIVING_ORDER_DATA_INFO'] == receivingOrdeDataInfo).dropna()
    if len(receivingOrderDataSeries) == 0:  # np.isnan(receivingOrderDataSeries):
        rs = -1
        # print("__getReceivingOrderDataInfo dfReceivingOrderData: \n", dfReceivingOrderData)
        # print("__getReceivingOrderDataInfo len(dfReceivingOrderData): ", len(dfReceivingOrderData))
        if len(dfReceivingOrderData) == 0:
            currentPk = receivingOrderNo + "0001"
        else:
            # receivingOrderNoSeries = dfReceivingOrderData['RECEIVING_ORDER_NO'].where(
            #     dfReceivingOrderData['RECEIVING_ORDER_NO'] == receivingOrderNo).dropna()
            dfReceivingOrderDataNo = dfReceivingOrderData.loc[dfReceivingOrderData['RECEIVING_ORDER_NO'] == receivingOrderNo]
            # print("__getReceivingOrderDataInfo dfReceivingOrderDataNo: \n", dfReceivingOrderDataNo)
            # print("__getReceivingOrderDataInfo len(dfReceivingOrderDataNo): ", len(dfReceivingOrderDataNo))
            if len(dfReceivingOrderDataNo) == 0:
                currentPk = receivingOrderNo + "0001"
            else:
                # print("__getReceivingOrderDataInfo ReceivingOrderNo: ", receivingOrderNo, ", code: ", code)
                maxPk = dfReceivingOrderDataNo['PK'].max()
                # print("__getReceivingOrderDataInfo maxPk: ", maxPk)
                maxSerialNo = int(maxPk[-4:])
                # print("__getReceivingOrderDataInfo maxSerialNo: ", maxSerialNo)
                currentPk = maxPk[:10] + str(maxSerialNo + 1).zfill(4)
                # print("__getReceivingOrderDataInfo currentPk: ", currentPk, ", type(currentPk): ", type(currentPk))
                # print("__getReceivingOrderDataInfo receivingOrderNo: ", receivingOrderNo, ", type(): ", type(receivingOrderNo))
                # print("__getReceivingOrderDataInfo shippingQtyTotal: ", shippingQtyTotal, ", type(): ", type(shippingQtyTotal))
                # print("__getReceivingOrderDataInfo unitPrice: ", unitPrice, ", type(unitPrice): ", type(unitPrice))
                # print("__getReceivingOrderDataInfo sessionUserId: ", sessionUserId, ", type(): ", type(sessionUserId))
                # print("__getReceivingOrderDataInfo step9: ", step9, ", type(step9): ", type(step9))

        # 2021.05.06 Conclusion. 반드시 "타입 변환"을 처리해야 에러가 발생하지 않는다.
        shippingQtyTotal = int(shippingQtyTotal)  # <class 'numpy.int64'> ===> <class 'int'>
        unitPrice = float(unitPrice)  # <class 'numpy.float64'> ===> <class 'float'>
        # print("__getReceivingOrderDataInfo shippingQtyTotal: ", shippingQtyTotal, ", type(): ", type(shippingQtyTotal))
        # print("__getReceivingOrderDataInfo unitPrice: ", unitPrice, ", type(unitPrice): ", type(unitPrice))

        sql = "Insert Into RECEIVINGORDERDATA (PK, RECEIVINGORDERNO, CODE, QTY, UP, USERID) " \
              "Values (%s,%s,%s,%s,%s, %s)"
        values = (currentPk, receivingOrderNo, code, shippingQtyTotal, unitPrice, sessionUserId)

        cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
        # print("9 __getReceivingOrderDataInfo ")

        try:
            mySqlWebDb.commit()
            rs = 1
            # print("서버에 실적 추가 성공!!! ")

            #####################################################################################################
            # 2021.05.06 Conclusion. 반드시 여기서, "신규 추가"한 자료를 다시 불러야 된다.
            CONNECTEDWEB, dfReceivingOrderData = __getReceivingOrderData(yearMonth, sessionUserId)
            #####################################################################################################

        except KeyboardInterrupt:
            rs = -1
            mySqlWebDb.rollback()
            print(get_line_no(), "DB 서버 [ReceivingOrderData.수주 상세 테이블]에 실적 추가 실패 !!! 다시 확인 하시오!!!")

    return rs, CONNECTEDWEB, dfReceivingOrderData


# 2021.05.14 Created. 납품 정보를 위한, Goods5.분류 정보 정리. "대대분류"
def __getGoods5(beInUse, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    # qrProcess = Process.objects.filter(beInUse=beInUse)
    # qrProcess = Process.objects.all().order_by('-code')  # 조립 공정이 맨 위로 오게, 내림차순(-code)으로 정렬...

    # print("__getGoods5 mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
    # print("__getGoods5 CONNECTEDWEB: ", CONNECTEDWEB, "type(CONNECTEDWEB):", type(CONNECTEDWEB))

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getGoods5 mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or \
                type(cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select ID, LANGUAGE1, LANGUAGE2, LANGUAGE3, LANGUAGE4 From GOODS5 ORDER BY LANGUAGE2 "
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or \
                    type(cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        CONNECTEDWEB = True
        sqlGoods5 = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        dfGoods5 = pd.DataFrame(sqlGoods5)  # <class 'pandas.core.frame.DataFrame'>
        # print("__getGoods5 dfSetsProcess: \n", dfSetsProcess)
        # print("_dbMrp.py __getGoods5 디버깅... 7")
        dfGoods5.columns = ['GOODS5', 'GOODS5_ENG', 'GOODS5_KOR', 'GOODS5_LOC', 'GOODS5_CHN']
        # print("__getGoods5 컬럼명 변경 후 dfSetsGoods5: \n", dfSetsGoods5)

        if LANGUAGE_NO == 1042:
        # if LANGUAGE_NO == 'korean':
            dfGoods5['GOODS5INFO'] = dfGoods5['GOODS5'].astype(str) + " " + dfGoods5['GOODS5_KOR']
        else:
            dfGoods5['GOODS5INFO'] = dfGoods5['GOODS5'].astype(str) + " " + dfGoods5['GOODS5_LOC']
        # print("__getGoods5 processinfo 추가 후 dfGoods5: \n", dfGoods5)
        # print("_dbMrp.py __getGoods5 디버깅... 8")

        goods5List = dfGoods5.values.tolist()
        # print("__getGoods5 processinfo 추가 후 리스트 goods5List: \n", goods5List)
        # print("_dbMrp.py __getGoods5 디버깅... 88")

    except:
        CONNECTEDWEB = False
        goods5List = []
        dfSetsGoods5 = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getGoods5 dfSetsProcess: \n", dfSetsProcess)
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlGoods5, dfGoods5, goods5List


# 2022.04.27 Added. 특정한 공정 코드에 대한 공정 정보 가져오기와 북경 조이 작업 일지 업로드 처리에서, "작업 위치" 값 가져오기
# // 2020.06.14 Modified. 지금까지 처리 [위치-창고]를, BOM에서 등록한 [자동 이동 창고]를 기준으로 처리하였으나,
# // 지금부터는 무조건 [창고 코드 기준.생산 위치 자기 자리]에 [재공.생산]과 [재고.입고]를 먼저 처리하고, 이후 차기 공정으로의 [재공.투입] 처리는,
# // [소형 바코드 프린터 및 스캐너]를 활용한 [물류 시스템]을 도입하여 처리한다.
# // Select MovingWarehouse Into :is_ParentWarehouse From t_Product Where Code=:ls_PaCode Using SQLCA;
# todo: ===> Select WarehouseSt Into :is_ParentWarehouse From Process Where Code=:is_Process Using SQLCA;
# 2021.05.05 Created. Process.공정 테이블에서, "process.공정 코드" 값으로, "공정 정보"를 얻는다.
def __getProcessInfo(dfSetsProcess, process):
    # process = process.replace("-", "")
    # dfSetsProcess.columns = ['PROCESS', 'PROCESS_ENG', 'PROCESS_KOR', 'PROCESS_LOC', 'PROCESS_CHN', 'COLORST']
    infoSeries = dfSetsProcess[['PROCESS', 'PROCESS_ENG', 'PROCESS_KOR', 'PROCESS_LOC', 'PROCESS_CHN',
                                'PROCESSSUPERIOR', 'WAREHOUSEST', 'COLORST']
    ].where(dfSetsProcess['PROCESS'] == process).dropna()
    #     print("infoSeries: ", infoSeries)
    #     print("type(infoSeries): ", type(infoSeries))
    #     print("len(infoSeries): ", len(infoSeries))
    if len(infoSeries) > 0:
        process = infoSeries.values[0][0].strip()
        processEng = infoSeries.values[0][1].strip()
        processKor = infoSeries.values[0][2].strip()
        processLoc = infoSeries.values[0][3].strip()
        processChn = infoSeries.values[0][4].strip()
        process_superior = infoSeries.values[0][5].strip()
        warehouse_standard = infoSeries.values[0][6].strip()
        colorSt = infoSeries.values[0][7].strip()
        rs = 1
    else:
        process = ""
        processEng = ""
        processKor = 0
        processLoc = 0
        processChn = 0
        process_superior = ""
        warehouse_standard = ""
        colorSt = 0
        rs = -1

    return rs, process, processEng, processKor, processLoc, processChn, process_superior, warehouse_standard, colorSt


# 2022.04.15 Added. 정상적이라면 __getProcess() 으로 처리되어야 하는데,
# 이것은 아래에서 Calendar.근무 일수 정보까지 담는 함수로 이미 사용하고 있어,
# 부득불 __getProcessOnly() 함수명으로, 순수 process.공정 정보 자료만 리턴하는 함수로 사용한다.
def __getProcessOnly(beInUse):
    # global msSqlServerDb, cursArrayServer, CONNECTEDWEB, COMPANY_CODE, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
    #     NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, COMPANY_CODE, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
        NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS

    # print(get_line_no(), ", __getProcess CONNECTEDWEB: ", CONNECTEDWEB)
    # print(get_line_no(), ", __getProcess COMPANY_CODE: ", COMPANY_CODE)
    # print(get_line_no(), ", __getProcess HOST3: ", HOST3)
    # print(get_line_no(), ", __getProcess DBNAME3: ", DBNAME3)

    # qrProcess = Process.objects.filter(beInUse=beInUse)
    # qrProcess = Process.objects.all().order_by('-code')  # 조립 공정이 맨 위로 오게, 내림차순(-code)으로 정렬...

    # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
    # print("__getProcess CONNECTEDWEB: ", CONNECTEDWEB, "type(CONNECTEDWEB):", type(CONNECTEDWEB))
    # print("__getProcess fromDate: ", fromDate, "toDate:", toDate)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(get_line_no(), ", __getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
        # print(get_line_no(), ", __getProcess cursArrayWeb: ", cursArrayWeb, "type(cursArrayWeb):", type(cursArrayWeb))

        # if type(mySqlWebDb) is not pymysql.connections.Connection or \
        #         type(cursArrayWeb) is not pymysql.cursors.Cursor:
        if type(mySqlWebDb) is pymysql.connections.Connection or \
                type(cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # sql = "Select CODE, Language1, Language2, Language3, Language4, ColorSt From Process ORDER BY CODE DESC "
    sql = "Select CODE, LANGUAGE1, LANGUAGE2, LANGUAGE3, LANGUAGE4, PROCESSSUPERIOR, WAREHOUSEST, COLORST " \
          "From PROCESS WHERE BEINUSE = 1 ORDER BY CODE DESC "
    try:
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        CONNECTEDWEB = True
        sqlProcess = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(get_line_no(), ", __getProcess sqlProcess: ", sqlProcess)
        dfSetsProcess = pd.DataFrame(sqlProcess)  # <class 'pandas.core.frame.DataFrame'>
        # print(get_line_no(), ", __getProcess dfSetsProcess: ", dfSetsProcess)
        dfSetsProcess.columns = ['PROCESS', 'PROCESS_ENG', 'PROCESS_KOR', 'PROCESS_LOC', 'PROCESS_CHN',
                                 'PROCESSSUPERIOR', 'WAREHOUSEST', 'COLORST']
        # print(get_line_no(), ", __getProcess 컬럼명 변경 후 LANGUAGE_NO: ", LANGUAGE_NO)

        # if LANGUAGE_NO == 1042:
        #     dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_KOR']
        # else:
        #     dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_LOC']
        # # print(get_line_no(), ", __getProcess processinfo 추가 후 dfSetsProcess: ", dfSetsProcess)

        processList = dfSetsProcess.values.tolist()
        # print(get_line_no(), ", __getProcess processinfo 추가 후 리스트 len(processList): ", len(processList))

        total_process_count = len(processList)

    except:
        CONNECTEDWEB = False
        processList = []
        total_process_count = 0
        dfSetsProcess = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getProcess dfSetsProcess: \n", dfSetsProcess)
        # print(get_line_no(), ", 경고, __getProcess [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlProcess, dfSetsProcess, processList, total_process_count


# 2023.02.06 Modified. Django ORM 방식.
def __getProcessOrm(beInUse, fromDate, toDate, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, COMPANY_CODE, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
        NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    LANGUAGE_NO = data['language']
    # sql = "Select CODE, LANGUAGE1, LANGUAGE2, LANGUAGE3, LANGUAGE4, PROCESSSUPERIOR, WAREHOUSEST, COLORST " \
    #       "From PROCESS WHERE BEINUSE = 1 ORDER BY CODE DESC "
    # sql = Process.objects.filter(beInUse=1).order_by("-code")

    # dfSetsProcess.columns = ['PROCESS', 'PROCESS_ENG', 'PROCESS_KOR', 'PROCESS_LOC', 'PROCESS_CHN',
    #                          'PROCESSSUPERIOR', 'WAREHOUSEST', 'COLORST']
    # if LANGUAGE_NO == 1042:
    #     # if LANGUAGE_NO == 'korean':
    #     dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_KOR']
    # else:
    #     dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_LOC']
    # # print(get_line_no(), ", __getProcess processinfo 추가 후 dfSetsProcess: ", dfSetsProcess)
    #

    # processList = dfSetsProcess.values.tolist()
    # # # print(get_line_no(), ", __getProcess processinfo 추가 후 리스트 len(processList): ", len(processList))
    # total_process_count = len(processList)
    #
    # # 2021.03.24 Added. 공정 정보를 가져 오면서, [CalendarCondition.근무일] 정보도 같이 가져오게 한다.
    # year = fromDate[:4]
    # month = fromDate[5:7]
    # yearBeforeLast = str(int(year) - 2)  # 2년 자료부터만 불러 오게 한다.
    # # print(get_line_no(), ", __getProcess yearBeforeLast: ", yearBeforeLast)
    # # print(get_line_no(), ", __getProcess month: ", month)
    # # print(get_line_no(), ", __getProcess CONNECTEDWEB: ", CONNECTEDWEB)
    #
    # sql = "SELECT SYEARMONTH, PROCESS, WORKINGDAYS, GT, " \
    #       "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15, " \
    #       "H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H27, H28, H29, H30, H31," \
    #       "G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, " \
    #       "G16, G17, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31 " \
    #       "FROM CALENDARCONDITION WHERE SYEARMONTH >= %s ORDER BY SYEARMONTH DESC, PROCESS DESC "
    # dfSetsWorkingDays.columns = ['YEARMONTH', 'PROCESS', 'WORKINGDAYS', 'WORKER_SUM',
    #                              'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
    #                              'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20',
    #                              'H21', 'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31',
    #                              'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
    #                              'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20',
    #                              'G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'G31']
    #
    # dfSetsWorkingDaysColumnsList = dfSetsWorkingDays.columns.values.tolist()



    # return sqlProcess, dfSetsProcess, processList, total_process_count, dfSetsWorkingDays, \
    #     NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, COMPANY_CODE


def __getProcess(beInUse, fromDate, toDate, data):
    # global msSqlServerDb, cursArrayServer, CONNECTEDWEB, COMPANY_CODE, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
    #     NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, COMPANY_CODE, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3, \
        NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS

    LANGUAGE_NO = data['language']

    # print(get_line_no(), ", __getProcess CONNECTEDWEB: ", CONNECTEDWEB)
    # print(get_line_no(), ", __getProcess COMPANY_CODE: ", COMPANY_CODE)
    # print(get_line_no(), ", __getProcess HOST3: ", HOST3)
    # print(get_line_no(), ", __getProcess DBNAME3: ", DBNAME3)

    print(get_line_no(), "LANGUAGE_NO: ", LANGUAGE_NO)

    # qrProcess = Process.objects.filter(beInUse=beInUse)
    # qrProcess = Process.objects.all().order_by('-code')  # 조립 공정이 맨 위로 오게, 내림차순(-code)으로 정렬...
    # print(get_line_no(), "qrProcess: ", qrProcess)

    # print(get_line_no(), ", mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
    # print(get_line_no(), ", CONNECTEDWEB: ", CONNECTEDWEB, "type(CONNECTEDWEB):", type(CONNECTEDWEB))
    # print(get_line_no(), ", fromDate: ", fromDate, "toDate:", toDate)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(get_line_no(), ", __getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
        # print(get_line_no(), ", __getProcess cursArrayWeb: ", cursArrayWeb, "type(cursArrayWeb):", type(cursArrayWeb))

        # if type(mySqlWebDb) is not pymysql.connections.Connection or \
        #         type(cursArrayWeb) is not pymysql.cursors.Cursor:
        if type(mySqlWebDb) is pymysql.connections.Connection or \
                type(cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # sql = "Select CODE, Language1, Language2, Language3, Language4, ColorSt From Process ORDER BY CODE DESC "
    sql = "Select CODE, LANGUAGE1, LANGUAGE2, LANGUAGE3, LANGUAGE4, PROCESSSUPERIOR, WAREHOUSEST, COLORST " \
          "From PROCESS WHERE BEINUSE = 1 ORDER BY CODE DESC "
    try:
        # print(get_line_no(), "sql: ", sql)
        cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        # if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        if type(mySqlWebDb) is pymysql.connections.Connection or type(
            cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

        try:
            # print(get_line_no(), "sql: ", sql)
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        except:
            CONNECTEDWEB = False

    try:
        CONNECTEDWEB = True
        sqlProcess = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(get_line_no(), ", __getProcess sqlProcess: ", sqlProcess)
        dfSetsProcess = pd.DataFrame(sqlProcess)  # <class 'pandas.core.frame.DataFrame'>
        # print(get_line_no(), ", __getProcess dfSetsProcess: ", dfSetsProcess)
        dfSetsProcess.columns = ['PROCESS', 'PROCESS_ENG', 'PROCESS_KOR', 'PROCESS_LOC', 'PROCESS_CHN',
                                 'PROCESSSUPERIOR', 'WAREHOUSEST', 'COLORST']
        # print(get_line_no(), ", __getProcess 컬럼명 변경 후 LANGUAGE_NO: ", LANGUAGE_NO)

        if LANGUAGE_NO == 1042:
        # if LANGUAGE_NO == 'korean':
            dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_KOR']
        else:
            dfSetsProcess['PROCESSINFO'] = dfSetsProcess['PROCESS'] + " " + dfSetsProcess['PROCESS_LOC']
        # print(get_line_no(), ", __getProcess processinfo 추가 후 dfSetsProcess: ", dfSetsProcess)

        processList = dfSetsProcess.values.tolist()
        # print(get_line_no(), ", __getProcess processinfo 추가 후 리스트 len(processList): ", len(processList))

        total_process_count = len(processList)

    except:
        CONNECTEDWEB = False
        processList = []
        total_process_count = 0
        dfSetsProcess = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getProcess dfSetsProcess: \n", dfSetsProcess)
        # print(get_line_no(), ", 경고, __getProcess [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    # return sqlProcess, dfSetsProcess, processList, total_process_count

    # 2021.03.24 Added. 공정 정보를 가져 오면서, [CalendarCondition.근무일] 정보도 같이 가져오게 한다.
    year = fromDate[:4]
    month = fromDate[5:7]
    yearBeforeLast = str(int(year) - 2)  # 2년 자료부터만 불러 오게 한다.
    # print(get_line_no(), ", __getProcess yearBeforeLast: ", yearBeforeLast)
    # print(get_line_no(), ", __getProcess month: ", month)
    # print(get_line_no(), ", __getProcess CONNECTEDWEB: ", CONNECTEDWEB)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    # sql = "SELECT sYearMonth, PROCESS, " \
    #       "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15, " \
    #       "H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H27, H28, H29, H30, H31 " \
    #       "FROM CalendarCondition WHERE sYearMonth >= %s ORDER BY sYearMonth DESC, PROCESS DESC "
    sql = "SELECT SYEARMONTH, PROCESS, WORKINGDAYS, GT, " \
          "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15, " \
          "H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H26, H27, H28, H29, H30, H31," \
          "G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, " \
          "G16, G17, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31 " \
          "FROM CALENDARCONDITION WHERE SYEARMONTH >= %s ORDER BY SYEARMONTH DESC, PROCESS DESC "
    try:
        cursArrayWeb.execute(sql, yearBeforeLast)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        try:
            cursArrayWeb.execute(sql, yearBeforeLast)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        except:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    try:
        CONNECTEDWEB = True
        sqlWorkingDays = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        dfSetsWorkingDays = pd.DataFrame(sqlWorkingDays)  # <class 'pandas.core.frame.DataFrame'>
        # print("__getProcess dfSetsWorkingDays: \n", dfSetsWorkingDays)
        # print("_dbMrp.py __getProcess 디버깅... 7")
        dfSetsWorkingDays.columns = ['YEARMONTH', 'PROCESS', 'WORKINGDAYS', 'WORKER_SUM',
                                     'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
                                     'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20',
                                     'H21', 'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31',
                                     'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
                                     'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20',
                                     'G21', 'G22', 'G23', 'G24', 'G25', 'G26', 'G27', 'G28', 'G29', 'G30', 'G31']

        dfSetsWorkingDaysColumnsList = dfSetsWorkingDays.columns.values.tolist()

        # 근무 일수를 "workingdays" 컬럼에 넣는다.
        # print(get_line_no(), ", dfSetsWorkingDays.tail(20): ", dfSetsWorkingDays.tail(20))
        # print(debugPath, ", 원본 type(dfSetsWorkingDays): ", type(dfSetsWorkingDays))
        # print(debugPath, ", dfSetsWorkingDays.index: ", dfSetsWorkingDays.index)
        # print(debugPath, ", 원본 len(dfSetsWorkingDays): ", len(dfSetsWorkingDays))
        # print(debugPath, ", dfSetsWorkingDays.info(): ", dfSetsWorkingDays.info())
        # print(debugPath, ", dfSetsWorkingDays.columns: ", listColumns)
        # print(debugPath, ", dfSetsWorkingDaysColumnsList: ", dfSetsWorkingDaysColumnsList)

        # df['Tenant'].replace('', np.nan, inplace=True)
        dfSetsWorkingDays['PROCESS'].replace('', np.nan, inplace=True)
        # print(get_line_no(), ", PROCESS 컬럼의 공백 문자를 np.nan으로 치환 후 dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays.tail(20))

        # df.dropna(subset=['Tenant'], inplace=True)
        dfSetsWorkingDays.dropna(subset=['PROCESS'], inplace=True)
        # print(get_line_no(), ", dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays.tail(20))
        # print(get_line_no(), ", PROCESS 컬럼 공백 문자 행 삭제 후 len(dfSetsWorkingDays): ", len(dfSetsWorkingDays))
        # print(debugPath, ", dfSetsWorkingDays.index: ", dfSetsWorkingDays.index)
        # print(debugPath, ", dfSetsWorkingDays.info(): ", dfSetsWorkingDays.info())
        # print(debugPath, ", dfSetsWorkingDays.columns: ", dfSetsWorkingDays.columns)
        # print(debugPath, ", dfSetsWorkingDaysColumnsList: ", dfSetsWorkingDaysColumnsList)
        # print(debugPath, ", dfSetsWorkingDaysColumnsList: ", dfSetsWorkingDays.columns.values.tolist())

        # 2021.07.01 Conclusion. "proceess" 컬럼 정리. ***** inplace=True ***** :: 특히 주의.
        # 특히 주의. B = A.drop_duplicates([], inplace=True) ===> A.drop_duplicates([], inplace=True)
        # dfLoadWorkSheetDaySum = dfLoadWorkSheet.drop_duplicates(['SHIPPING_DATE', 'trade_code']).reset_index()
        # dfSetsWorkingDays = dfSetsWorkingDays.drop_duplicates([['yearmonth', 'PROCESS']], inplace=True) ===> 에러...
        dfSetsWorkingDays.drop_duplicates(['YEARMONTH', 'PROCESS'], inplace=True)  # 반드시 직접 실행.
        # dfSetsWorkingDays.drop_duplicates(['yearmonth', 'PROCESS'])  # 반드시 직접 실행.
        # print(debugPath, ", dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays.tail(20))
        # print(get_line_no(), ", yearmonth+process 중복 제거 후 len(dfSetsWorkingDays): ", len(dfSetsWorkingDays))
        # print(debugPath, ", dfSetsWorkingDays.index: ", dfSetsWorkingDays.index)
        # print(debugPath, ", dfSetsWorkingDays.info(): ", dfSetsWorkingDays.info())
        # print(debugPath, ", dfSetsWorkingDaysColumnsList: ", dfSetsWorkingDaysColumnsList)
        # print(debugPath, ", dfSetsWorkingDaysColumnsList: ", dfSetsWorkingDays.columns.values.tolist())

        for i in dfSetsWorkingDays.index:
            process = dfSetsWorkingDays.at[i, "PROCESS"]
            # print(get_line_no(), ", i: ", i, ", process: ", process)
            # print(debugPath, ", i: ", i, ", type(process): ", type(process))

            workingDays = 0
            workerSum = 0
            for j in range(1, 32):
                dayTime = dfSetsWorkingDays.at[i, 'H' + str(j)]
                worker = dfSetsWorkingDays.at[i, 'G' + str(j)]
                # print(get_line_no(), ", i: ", i, ", dayTime: ", dayTime)
                # print(get_line_no(), ", j: ", j, ", type(dayTime): ", type(dayTime))
                # print(get_line_no(), ", i: ", i, ", worker: ", worker)
                # print(get_line_no(), ", j: ", j, ", type(worker): ", type(worker))
                if dayTime.astype('int64') > 0:
                    workingDays += 1
                # if worker.astype('int64') > 0:
                if worker.astype('float64') > 0:
                    workerSum += worker
            # print(debugPath, ", workingDays: ", workingDays, ", workerSum: ", workerSum)
            # os.system("pause")
            if workingDays == 0:
                workingDays = 1  # [0]으로는 나눌 수 없다.

            dfSetsWorkingDays.at[i, "WORKINGDAYS"] = workingDays
            dfSetsWorkingDays.at[i, "WORKER_SUM"] = workerSum
            # dfSetsWorkingDays.at[i, "worker_average"] \
            #     = pd.to_numeric(dfSetsWorkingDays['worker_sum']) / pd.to_numeric(dfSetsWorkingDays['workingdays']).__round__(1).astype(str)
            workerAverage = (workerSum / workingDays).__round__(1)
            dfSetsWorkingDays.at[i, "WORKER_AVERAGE"] = workerAverage
            # workerAverage = (workerSum / workingDays).__round__(1).astype(str)  # 에러 나네...
            # dfSetsWorkingDays.at[i, "worker_average"] = workerAverage

            # # 2021.07.01 Conclusion. 아래는 이미 위에서 공백 문자를 "np.nan"으로 변환 후, 모두 삭제 처리했으므로 의미 없음.
            # # 2021.06.08 Added. "process" 컬럼이 공백 문자, 즉 "Null" 값도 아니고, str 타입의 공백 문자인 경우에 "0000"으로..
            # if len(process) == 0:
            #     dfSetsWorkingDays.at[i, 'process'] = "0000"

        # # print(debugPath, ", dfSetsWorkingDays: \n", dfSetsWorkingDays)
        # dfSetsWorkingDays['PROCESS'] = dfSetsWorkingDays.process.fillna("0000")  # 틀정 컬럼의 NaN만 공 백문자로 채우기.
        # # print(debugPath, ", dfSetsWorkingDays: \n", dfSetsWorkingDays)
        #
        # # print(debugPath, ", dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays.tail(20))
        # # print(debugPath, ", processr가 [0000]인 행 제거 전 len(dfSetsWorkingDays): ", len(dfSetsWorkingDays))
        # dfSetsWorkingDays = dfSetsWorkingDays[dfSetsWorkingDays['PROCESS'] != "0000"]
        # # dfSetsWorkingDays = dfSetsWorkingDays[dfSetsWorkingDays['PROCESS'] != "0000"].reset_index()  # index 컬럼이 새로 생김에 특히 주의.
        # # dfSetsWorkingDays = dfSetsWorkingDays[dfSetsWorkingDays.process != "0000"]
        # # print(debugPath, ", processr가 [0000]인 행 제거 후 dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays.tail(20))
        # # print(debugPath, ", processr가 [0000]인 행 제거 후 len(dfSetsWorkingDays): ", len(dfSetsWorkingDays))

        # if LANGUAGE_NO == 1042:
        #     dfSetsWorkingDays['processinfo'] = dfSetsWorkingDays['process'] + " " + dfSetsWorkingDays['process_kor']
        # else:
        #     dfSetsWorkingDays['processinfo'] = dfSetsWorkingDays['process'] + " " + dfSetsWorkingDays['process_loc']
        # print("__getProcess processinfo 추가 후 dfSetsWorkingDays: \n", dfSetsWorkingDays)
        # print("_dbMrp.py __getProcess 디버깅... 8")

        workingDaysList = dfSetsWorkingDays.values.tolist()
        # print(get_line_no(), "processinfo 추가 후 리스트 workingDaysList:", workingDaysList)
        # print(get_line_no(), "processinfo 추가 후 리스트 len(workingDaysList):", len(workingDaysList))

        # 2021.06.08 Conclusion. 여기서 처리하지 말고, 꼭 필요한 곳에서만 처리하게 한다. ===> view.py.ppp_upload_worker()
        # 2021.06.08 Added. 당해 년도의 근태 자료만 따로 정리한다.
        # print(debugPath, ", 1 dfSetsWorkingDays.tail(20): \n", dfSetsWorkingDays[['yearmonth', 'process']].tail(20))
        # df = dfSetsWorkingDays[['yearmonth', 'process']]  # 대괄호 []가 2개 [[]] 인 것에 주의...
        # print(debugPath, ", 1 df.tail(20): \n", df.tail(20))
        # df['year'] = df.yearmonth.str.slice(start=0, stop=4)  # 아~~~ "202106" 값에서 "2021" 만 뽑아서 "year" 컬럼에 추가.
        # print(debugPath, ", 2 df.tail(20): \n", df.tail(20))

        # 2021.06.08 Conclusion. 여기서 처리하지 말고, 꼭 필요한 곳에서만 처리하게 한다. ===> view.py.ppp_upload_worker()
        # dfThisYearWorkingDays = dfSetsWorkingDays[dfSetsWorkingDays.yearmonth.str.slice(start=0, stop=4) == year]
        # print(debugPath, ", 2 dfThisYearWorkingDays: \n", dfThisYearWorkingDays)
        # print(debugPath, ", 2 type(dfThisYearWorkingDays): ", type(dfThisYearWorkingDays))
        # print(debugPath, ", 2 len(dfThisYearWorkingDays): ", len(dfThisYearWorkingDays))

        # dfCalendarCondition = dfSetsWorkingDays.yearmonth.str.slice(start=0, stop=4) == year
        # dfCalendarCondition = dfSetsWorkingDays[~thisYear]  # 아닌 것만... *****
        # dfCalendarCondition = dfSetsWorkingDays[thisYear]
        # print(get_line_no(), ", dfCalendarCondition.tail(20): ", dfCalendarCondition.tail(20))

    except:
        CONNECTEDWEB = False
        processList = []
        total_process_count = 0
        dfSetsProcess = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getProcess dfSetsProcess: \n", dfSetsProcess)
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlProcess, dfSetsProcess, processList, total_process_count, dfSetsWorkingDays, \
           NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, COMPANY_CODE

# 2021.06.08 Conclusion. 아래 근태 자료는 바로 위, __getProcess().dfSetsWorkingDays 데이터프레임에서,
# 2년전 자료까지 몽창 가져가서, 필요한 자료를 그때 그때 가공해서 사용하게 한다.
# 그러므로 아래 ____getCalendarCondition() 함수는 필요가 전혀 없다.
# 2021.06.08 Added. 근태 자료 가져오기.
# 엑셀 근태 자료를 업로드하려고 메뉴를 클릭하면, 먼저 기존 저장되어 있는 근태 자료를 화면에 뿌려준다.
# def __getCalendarCondition(dayInt, yearMonthCurrent, month, processCode, presentOrganization, sessionUserId):
#     global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3
#
#     debugPath = "__dbMrp.py __getCalendarCondition()"
#
#     print("\n\n\n\n\n__getCalendarCondition************************************************************************")
#     # print(debugPath, ", request: ", request)
#     # print(debugPath, ", request.content_params: ", request.content_params)
#     # print(debugPath, ", *kwargs: ", *kwargs)


# 2021.06.08 Created. 근태 자료를 업로드 하기 전에, 업로드하려고 하는 해당 기간의 기존 자료(Gxx)를 [0]으로 초기화 해야한다.
def __setCalendarConditionZero(fromYearMonth, toYearMonth, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "SELECT SYEARMONTH, PROCESS, WORKINGDAYS, GT, " \
          "G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, " \
          "G16, G17, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31 " \
          "FROM CALENDARCONDITION WHERE SYEARMONTH >= %s AND SYEARMONTH <= %s ORDER BY SYEARMONTH DESC, PROCESS DESC "
    values = (fromYearMonth, toYearMonth)

    try:
        cursArrayWeb.execute(sql, fromYearMonth, toYearMonth)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchone()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # print("month: ", month, ", dayInt: ", dayInt)
            # os.system("pause")
            rtnResult = True  # 해당 기간의 근태 자료가 없으면, 초기화 할 필요가 전혀 없다.
        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...
            # 중간에 괄호가 있으면, 에러 발생한다. ???
            sql = "Update CALENDARCONDITION Set GT = 0, GA = 0, GM = 0, GN = 0, " \
                  "G1 = 0, G2 = 0, G3 = 0, G4 = 0, G5 = 0, G6 = 0, G7 = 0, G8 = 0, G9 = 0, G10 = 0, " \
                  "G11 = 0, G12 = 0, G13 = 0, G14 = 0, G15 = 0, G16 = 0, G17 = 0, G18 = 0, G19 = 0, G20 = 0, " \
                  "G21 = 0, G22 = 0, G23 = 0, G24 = 0, G25 = 0, G26 = 0, G27 = 0, G28 = 0, G29 = 0, G30 = 0, G31 = 0 " \
                  "FROM CALENDARCONDITION WHERE SYEARMONTH >= %s AND SYEARMONTH <= %s "

            values = (fromYearMonth, toYearMonth)
            cursArrayWeb.execute(sql, values)

            try:
                mySqlWebDb.commit()
                rtnResult = True
                # print("기존 근태 자료 초기화 성공! ", fromYearMonth, " ~ ", toYearMonth)
            except KeyboardInterrupt:
                rtnResult = False
                mySqlWebDb.rollback()
                print(get_line_no(), "기존 근태 자료 초기화 실패! ", fromYearMonth, " ~ ", toYearMonth)

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

        rtnResult = False

    return rtnResult


def __setCalendarCondition(dayInt, yearMonthCurrent, month, processCode, presentOrganization, sessionUserId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

    sql = "Select SYEARMONTH, PROCESS From CALENDARCONDITION " \
          "Where SYEARMONTH = %s AND PROCESS = %s Order By SYEARMONTH Desc, PROCESS "

    values = (yearMonthCurrent, processCode)

    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), "Database 연결을 확인하시오!")

        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        # array_sets_server = cursArrayWeb.fetchone()
        # 요넘 "fetchone()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
        # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
        array_sets_server = cursArrayWeb.fetchall()

        # 2019.01.29 정리. ***** 중요 *****
        # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
        # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.
        # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
        # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
        # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
        row_count_server = len(array_sets_server)
        # print("array_sets_server.count() : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            # print("month: ", month, ", dayInt: ", dayInt)
            # os.system("pause")
            if dayInt == 1:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G1, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 2:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G2, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 3:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G3, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 4:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G4, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 5:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G5, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 6:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G6, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 7:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G7, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 8:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G8, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 9:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G9, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 10:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G10, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 11:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G11, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 12:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G12, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 13:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G13, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 14:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G14, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 15:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G15, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 16:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G16, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 17:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G17, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 18:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G18, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 19:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G19, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 20:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G20, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 21:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G21, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 22:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G22, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 23:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G23, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 24:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G24, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 25:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G25, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 26:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G26, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 27:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G27, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 28:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G28, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 29:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G29, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 30:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G30, CONFIRMID) Values (%s,%s,%s,%s,%s)"
            if dayInt == 31:
                sql = "Insert Into CALENDARCONDITION (SYEARMONTH,SMONTH, PROCESS, G31, CONFIRMID) Values (%s,%s,%s,%s,%s)"

            values = (yearMonthCurrent, month, processCode, presentOrganization, sessionUserId)
            cursArrayWeb.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
            # print("values: ", values)
            # print("cursArrayWeb: ", cursArrayWeb)

            # try:
            #     mySqlWebDb.commit()
            #     print("자료 추가 성공!!!")
            #     os.system("pause")
            # except KeyboardInterrupt:
            #     mySqlWebDb.rollback()
            #     print("자료 추가 실패 !!! 다시 확인 하시오!!!")

        else:  # row_count_server > 0 : 이미 생산 실적 번호가 있으면...

            # 중간에 괄호가 있으면, 에러 발생한다. ???
            if dayInt == 1:
                sql = "Update CALENDARCONDITION Set G1 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 2:
                sql = "Update CALENDARCONDITION Set G2 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 3:
                sql = "Update CALENDARCONDITION Set G3 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 4:
                sql = "Update CALENDARCONDITION Set G4 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 5:
                sql = "Update CALENDARCONDITION Set G5 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 6:
                sql = "Update CALENDARCONDITION Set G6 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 7:
                sql = "Update CALENDARCONDITION Set G7 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 8:
                sql = "Update CALENDARCONDITION Set G8 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 9:
                sql = "Update CALENDARCONDITION Set G9 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 10:
                sql = "Update CALENDARCONDITION Set G10 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 11:
                sql = "Update CALENDARCONDITION Set G11 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 12:
                sql = "Update CALENDARCONDITION Set G12 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 13:
                sql = "Update CALENDARCONDITION Set G13 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 14:
                sql = "Update CALENDARCONDITION Set G14 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 15:
                sql = "Update CALENDARCONDITION Set G15 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 16:
                sql = "Update CALENDARCONDITION Set G16 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 17:
                sql = "Update CALENDARCONDITION Set G17 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 18:
                sql = "Update CALENDARCONDITION Set G18 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 19:
                sql = "Update CALENDARCONDITION Set G19 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 20:
                sql = "Update CALENDARCONDITION Set G20 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 21:
                sql = "Update CALENDARCONDITION Set G21 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 22:
                sql = "Update CALENDARCONDITION Set G22 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 23:
                sql = "Update CALENDARCONDITION Set G23 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 24:
                sql = "Update CALENDARCONDITION Set G24 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 25:
                sql = "Update CALENDARCONDITION Set G25 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 26:
                sql = "Update CALENDARCONDITION Set G26 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 27:
                sql = "Update CALENDARCONDITION Set G27 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 28:
                sql = "Update CALENDARCONDITION Set G28 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 29:
                sql = "Update CALENDARCONDITION Set G29 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 30:
                sql = "Update CALENDARCONDITION Set G30 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"
            if dayInt == 31:
                sql = "Update CALENDARCONDITION Set G31 = %s, CONFIRMID = %s Where SYEARMONTH = %s AND PROCESS = %s"

            values = (presentOrganization, sessionUserId, yearMonthCurrent, processCode)
            cursArrayWeb.execute(sql, values)

            # try:
            #     mySqlWebDb.commit()
            #     print(yearMonthCurrent, " :: ", processCode, " 변경 성공!!! ")
            # except KeyboardInterrupt:
            #     mySqlWebDb.rollback()
            #     print(yearMonthCurrent, " :: ", processCode, " 변경 실패!!! ")

        try:
            mySqlWebDb.commit()
            rtnResult = True
            # print(yearMonthCurrent, " :: ", processCode, " 서버 저장 성공!!! ")
        except KeyboardInterrupt:
            rtnResult = False
            mySqlWebDb.rollback()
            print(get_line_no(), ", ", yearMonthCurrent, " :: ", processCode, " 서버 저장 실패!!! ")

    except:
        CONNECTEDWEB = False
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

        rtnResult = False

    return rtnResult, CONNECTEDWEB


# 2022.04.15 Added. EMP.사원 정보
def __getEmp(beInUse):
    global mySqlWebDb2, cursArrayWeb2, CONNECTEDWEBWMS, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME32

    CONNECTEDWEBWMS = False
    if CONNECTEDWEBWMS == False:
        # mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsDB()  # DBNAME32 임에 주의...
        mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()  # DBNAME32 임에 주의...
        # print(get_line_no(), ", mySqlWebDb: ", mySqlWebDb2, ", type(mySqlWebDb):", type(mySqlWebDb2))
        # print(get_line_no(), ", cursArrayWeb: ", cursArrayWeb2, ", type(cursArrayWeb):", type(cursArrayWeb2))
        if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
            CONNECTEDWEBWMS = True
            # print(get_line_no(), f"웹 컴퓨터 {HOST3} {DBNAME32} Database 연결 성공!")
        else:
            CONNECTEDWEBWMS = False
            print(get_line_no(), f"웹 컴퓨터 {HOST3} {DBNAME32} Database 연결을 확인하시오!")
            existYesNoUserId = False
            dfEmpInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            print(get_line_no(), f"경고, {HOST3} {DBNAME32}[callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")
            empInfoList = []
            return existYesNoUserId, dfEmpInfo, empInfoList

    sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP ORDER BY ID "  # BEINUSE 컬럼이 없네.
    # sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP Where BEINUSE = %s ORDER BY ID "  # BEINUSE 컬럼이 없네.
    # values = (beInUse)
    try:
        # print(get_line_no(), ", __dbMrp.py sql: ", sql)
        cursArrayWeb2.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEBWMS == False:
            # mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsDB()
            mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()
            if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
                CONNECTEDWEBWMS = True
                # print(get_line_no(), f"{HOST3} {DBNAME32} Database 연결 성공!")
            else:
                CONNECTEDWEBWMS = False
                print(get_line_no(), f"{HOST3} {DBNAME32} Database 연결을 확인하시오!")
                existYesNoUserId = False
                dfEmpInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
                print(get_line_no(), f"경고, {HOST3} {DBNAME32} [callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")
                empInfoList = []
                return existYesNoUserId, dfEmpInfo, empInfoList

        cursArrayWeb2.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        CONNECTEDWEBWMS = True
        # print(get_line_no(), ", __dbMrp.py CONNECTEDWEBWMS: ", CONNECTEDWEBWMS)
        sqlEmpInfo = cursArrayWeb2.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(get_line_no(), ", __dbMrp.py sqlEmpInfo: ", sqlEmpInfo)
        # print(get_line_no(), ", __dbMrp.py len(sqlEmpInfo): ", len(sqlEmpInfo))
        dfEmpInfo = pd.DataFrame(sqlEmpInfo)  # <class 'pandas.core.frame.DataFrame'>
        # print(get_line_no(), ", __dbMrp.py dfEmpInfo: ", dfEmpInfo)
        # print(get_line_no(), ", __dbMrp.py len(dfEmpInfo): ", len(dfEmpInfo))
        dfEmpInfo.columns = ['EMPNO', 'USERID', 'NAME_KOR', 'NAME_LOC']
        # print(get_line_no(), ", __dbMrp.py 컬럼명 변경 후 dfEmpInfo.tail(20): \n", dfEmpInfo.tail(20))

        # # print(get_line_no(), ", __dfMrp.py LANGUAGE_NO: ", LANGUAGE_NO)
        # if LANGUAGE_NO == 1042:
        #     dfEmpInfo['USERINFO'] = dfEmpInfo['EMPNO'] + " " + dfEmpInfo['NAME_KOR']
        # else:
        #     dfEmpInfo['USERINFO'] = dfEmpInfo['EMPNO'] + " " + dfEmpInfo['NAME_LOC']
        # # print("__getUserIdPassword processinfo 추가 후 dfEmpInfo: \n", dfEmpInfo)

        empInfoList = dfEmpInfo.values.tolist()
        # print("__getUserIdPassword processinfo 추가 후 리스트 empInfoList: \n", empInfoList)
        # print(get_line_no(), ", _dbMrp.py len(empInfoList): ", len(empInfoList))

        existYesNoUserId = True

    except:
        existYesNoUserId = False
        CONNECTEDWEBWMS = False
        empInfoList = []
        dfEmpInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getEmp dfEmpInfo: \n", dfEmpInfo)
        print(get_line_no(), f"경고, {HOST3} {DBNAME32}[callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")

    return existYesNoUserId, dfEmpInfo, empInfoList


def __getUserIdPassword(userId, password, data):
    global mySqlWebDb2, cursArrayWeb2, CONNECTEDWEBWMS, NIGHT_CLOSING_HHMMSS

    LANGUAGE_NO = data['language']

    # qrProcess = Process.objects.filter(beInUse=beInUse)
    # qrProcess = Process.objects.all().order_by('-code')  # 조립 공정이 맨 위로 오게, 내림차순(-code)으로 정렬...

    print(get_line_no(), ", userId: ", userId, "type(userId):", type(userId))
    print(get_line_no(), ", password: ", password, "type(password):", type(password))

    CONNECTEDWEBWMS = False
    if CONNECTEDWEBWMS == False:
        # mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsDB()  # DBNAME32 임에 주의...
        mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()  # DBNAME32 임에 주의...
        # print(get_line_no(), ", mySqlWebDb: ", mySqlWebDb2, ", type(mySqlWebDb):", type(mySqlWebDb2))
        # print(get_line_no(), ", cursArrayWeb: ", cursArrayWeb2, ", type(cursArrayWeb):", type(cursArrayWeb2))
        if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
            CONNECTEDWEBWMS = True
            print(get_line_no(), f"웹 컴퓨터 {HOST3} {DBNAME32} Database 연결 성공!")
        else:
            CONNECTEDWEBWMS = False
            print(get_line_no(), f"웹 컴퓨터 {HOST3} {DBNAME32} Database 연결을 확인하시오!")
            existYesNoUserId = False
            dfSetsUserInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            print(get_line_no(), f"경고, {HOST3} {DBNAME32}[callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")
            return existYesNoUserId

    # sql = "Select empno, id, name2, name3 From t_emp Where id = %s AND password = %s ORDER BY id "
    # sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP Where ID = %s AND PASSWORD = %s ORDER BY ID "
    sql = "Select EMPNO, ID, NAME2, NAME3 From T_EMP Where ID = %s ORDER BY ID "  # 2022.04.08 Conclusion. password 불필
    # sql = "Select empno, id, name2, name3 From t_emp Where id = 'rwkang@naver.com' AND password = 'qq' ORDER BY id "
    # values = (userId, password)
    values = (userId)
    try:
        # print(get_line_no(), ", __dbMrp.py sql: ", sql)
        # print(get_line_no(), ", __dbMrp.py userId: ", userId)
        # print(get_line_no(), ", __dbMrp.py password: ", password)
        cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # cursArrayWeb2.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEBWMS == False:
            # mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsDB()
            mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()
            if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
                CONNECTEDWEBWMS = True
                print(get_line_no(), f"{HOST3} {DBNAME32} Database 연결 성공!")
            else:
                CONNECTEDWEBWMS = False
                print(get_line_no(), f"{HOST3} {DBNAME32} Database 연결을 확인하시오!")
                existYesNoUserId = False
                dfSetsUserInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
                print(get_line_no(), f"경고, {HOST3} {DBNAME32} [callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")
                return existYesNoUserId

        cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # cursArrayWeb2.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        CONNECTEDWEBWMS = True
        # print(get_line_no(), ", __dbMrp.py CONNECTEDWEBWMS: ", CONNECTEDWEBWMS)
        sqlUserInfo = cursArrayWeb2.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(get_line_no(), ", __dbMrp.py sqlUserInfo: ", sqlUserInfo)
        # print(get_line_no(), ", __dbMrp.py len(sqlUserInfo): ", len(sqlUserInfo))
        dfSetsUserInfo = pd.DataFrame(sqlUserInfo)  # <class 'pandas.core.frame.DataFrame'>
        # print(get_line_no(), ", __dbMrp.py dfSetsUserInfo: ", dfSetsUserInfo)
        # print(get_line_no(), ", __dbMrp.py len(dfSetsUserInfo): ", len(dfSetsUserInfo))
        # print("_dbMrp.py __getUserIdPassword 디버깅... 7")
        dfSetsUserInfo.columns = ['EMPNO', 'USERID', 'NAME_KOR', 'NAME_LOC']
        # print("__getUserIdPassword 컬럼명 변경 후 dfSetsUserInfo: \n", dfSetsUserInfo)

        # print(get_line_no(), ", __dfMrp.py LANGUAGE_NO: ", LANGUAGE_NO)
        if LANGUAGE_NO == 1042:
        # if LANGUAGE_NO == 'korean':
            dfSetsUserInfo['USERINFO'] = dfSetsUserInfo['EMPNO'] + " " + dfSetsUserInfo['NAME_KOR']
        else:
            dfSetsUserInfo['USERINFO'] = dfSetsUserInfo['EMPNO'] + " " + dfSetsUserInfo['NAME_LOC']
        # print("__getUserIdPassword processinfo 추가 후 dfSetsUserInfo: \n", dfSetsUserInfo)
        # print("_dbMrp.py __getUserIdPassword 디버깅... 8")

        userInfoList = dfSetsUserInfo.values.tolist()
        # print("__getUserIdPassword processinfo 추가 후 리스트 userInfoList: \n", userInfoList)
        # print(get_line_no(), ", _dbMrp.py len(userInfoList): ", len(userInfoList))

        existYesNoUserId = True

    except:
        existYesNoUserId = False
        CONNECTEDWEBWMS = False
        userInfoList = []
        dfSetsUserInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getUserIdPassword dfSetsUserInfo: \n", dfSetsUserInfo)
        print(get_line_no(), f"경고, {HOST3} {DBNAME32}[callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")

    return existYesNoUserId


def __setPasswordNew(userId, passwordNew):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEBWMS, NIGHT_CLOSING_HHMMSS
    # print(get_line_no(), ", __dbMrp.py userId: ", userId, "passwordNew: ", passwordNew)

    CONNECTEDWEBWMS = False
    if CONNECTEDWEBWMS == False:
        # mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsDB()  # DBNAME32 임에 주의...
        mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()  # DBNAME32 임에 주의...
        # print("__getUserIdPassword mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
        if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
            CONNECTEDWEBWMS = True
            print(get_line_no(), ", __dbMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEBWMS = False
            print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")

    sql = "UPDATE T_EMP SET PASSWORD = %s Where ID = %s "
    values = (passwordNew, userId)

    try:
        cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEBWMS == False:
            mySqlWebDb2, cursArrayWeb2, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME32 = connectWebWmsMyDB()
            if type(mySqlWebDb2) is pymysql.connections.Connection or type(
                cursArrayWeb2) is pymysql.cursors.Cursor:
                CONNECTEDWEBWMS = True
                print(get_line_no(), ", __dbMrp.py Database 연결 성공!")
            else:
                CONNECTEDWEBWMS = False
                print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")

        cursArrayWeb2.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:

        # print("cursArrayWeb2.rowcount: ", cursArrayWeb2.rowcount)
        if cursArrayWeb2.rowcount > 0:
            mySqlWebDb2.commit()
            CONNECTEDWEBWMS = True
            successOk = True
            print(get_line_no(), ", __dbMrp.py Database 저장 성공!!!")
        else:
            mySqlWebDb2.rollback()
            print(get_line_no(), ", __dbMrp.py Database 저장 실패!!!")
            CONNECTEDWEBWMS = False
            successOk = False

        # sqlUserInfo = cursArrayWeb2.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("__getUserIdPassword dfSetsUserInfo: \n", dfSetsUserInfo)
        # print("_dbMrp.py __getUserIdPassword 디버깅... 7")

        # my_cursor = my_connect.cursor() #
        # my_cursor.execute("UPDATE student SET class='Five' Where class='Four'")
        # my_connect.commit()
        # print("Rows updated = ",my_cursor.rowcount)
        # Output is here
        # Rows updated = 9

    except:
        successOk = False
        CONNECTEDWEBWMS = False
        userInfoList = []
        dfSetsUserInfo = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # print("경고, __getUserIdPassword dfSetsUserInfo: \n", dfSetsUserInfo)
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서, 해당 [ID]를 찾지 못 했습니다. 관리자에게 문의하시오!")

    return successOk


def __getGatheringData(byYearMonthWeekDay, fromDate, toDate, processCode, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    # print(get_line_no(), ", _dbMrp.py byYearMonthWeekDay: ", byYearMonthWeekDay)

    if byYearMonthWeekDay == "D":
        year = fromDate[:4]
        month = fromDate[5:7]
        day = fromDate[-2:]
        # serial = "0001"  # 사업 계획 Revision은 필요 없고, 그냥 [달]을 4자리로 하여 처리...
        revision = year + "00" + month
        # print(get_line_no(), ", _dbMrp.py __getGatheringData year: ", year)
        # print(get_line_no(), ", _dbMrp.py __getGatheringData month: ", month)
        # print(get_line_no(), ", _dbMrp.py __getGatheringData day: ", day)

        # 해당 월도의 마지막 날짜를 찾는다.
        maxDate = __getMaxDate(year, month)
        # print(get_line_no(), ", __getGatheringData 55 maxDate: ", maxDate)

        # 검색 날짜 + 1
        # import datetime
        # fromDateStart = datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")  # 이게 안 되네...

        # todo: 2022.04.28 Conclusion. 처음에 "import datetime as dt"로 새로 define 하였다.
        #   안 되면, 이것도 참조: workdate = datetime.strptime(workdate, datetime_format).date()  # 이것은 "date" 형식.
        # fromDateStart = datetime.datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")  # <class 'datetime.datetime'>
        fromDateStart = dt.datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")  # <class 'datetime.datetime'>

        fromDateEnd = fromDateStart + timedelta(days=1)
        # print(get_line_no(), ", __getGatheringData fromDateStart: ", fromDateStart)
        # print(get_line_no(), ", __getGatheringData fromDateEnd: ", fromDateEnd)
        fromDateStartString = fromDateStart.strftime("%Y-%m-%d")
        fromDateEndString = fromDateEnd.strftime("%Y-%m-%d")
        # print("2 __getGatheringData fromDateStartString: ", fromDateStartString)
        # print("2 __getGatheringData type(fromDateStartString): ", type(fromDateStartString))
        # print("2 __getGatheringData fromDateEndString: ", fromDateEndString)
        # print("2 __getGatheringData type(fromDateEndString): ", type(fromDateEndString))

        # fromDateStartString = "2021-03-20"
        # fromDateEndString = "2021-03-21"
        # processCode = "2080"

    elif byYearMonthWeekDay == "M":
        fromDateStartString = fromDate

        # 1. 여기는 [순수 실시간 실적 수집 자료]만을 불러와서, 선택 기간에 대해 [날짜별]로 뿌려 주는 것이므로,
        #    [수집 자료 로우]가 엄청 많기 때문에, 여기서 강제로 [fromDate]를 기준으로 [1개월간]만의 자료로 가공한다.
        # 3. x축으로는 [날짜]를 표시한다.
        year = fromDate[:4]
        month = fromDate[5:7]
        # print("ppp_machine year: ", year)
        # print("ppp_machine month: ", month)
        maxDate = __getMaxDate(year, month)
        # print("ppp_machine maxDate: ", maxDate)

        toDate = year + "-" + month + "-" + maxDate
        # print("ppp_machine toDate: ", toDate)

        fromDateEndString = toDate

    elif byYearMonthWeekDay == "Y":
        pass
    elif byYearMonthWeekDay == "W":
        pass

    # print("_dbMrp.py __getGatheringData fromDate: ", fromDate, ", toDate: ", toDate, ", processCode: ", processCode)

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProductionCurrent mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dbMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")

    if str(processCode).lower() == 'all' or str(processCode) == '0000':
        # print("1 __getGatheringData() Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")

        # 0. Gathering_No: 작업 번호: 생산 번호 + 일련 번호: 210301 PSC001 25 1 8000031313 0011
        # 1. Facilities: 설비 번호: 최초 설비 대장 등록 번호
        # 2. Work_date: 작업 날짜, 시각: 시:분:초
        # 3. Code: 품번
        # 4. Specification: 제품 규격
        # 5. Process: 공정 코드: 4자리
        # 6. Groups: 작업 그룹 코드: 4자리
        # 7. Line_Code: 라인 코드: 숫자형
        # 8. DayNight: 주야 구분 코드: 1자리 문자형
        # 9. Ok_Ng: 양품 불량품 구분 코드: 1자리 문자형: 1: 양품, 0: 불량품
        # 10. Daywork: 생산 수량
        # 11. Goodness: 양품 수량
        # 12. Badness: 불량 수량

        # dfSets.columns = ['gatheringno', 'facilities', 'work_date', 'code', 'STEP9',
        #                   'process', 'MACHINE, 'groups', 'LINE_CODE', 'day_night',
        #                   'ok_ng', 'daywork', 'goodness', 'badness', 'MACHINE_kor', 'MACHINE_loc']

        values = (fromDateStartString, fromDateEndString)
        # 아래는 최초 MACHINE.CODE 조인.
        # sql = "SELECT ga.Gathering_No, ga.Facilities, ga.Work_date, ga.CODE, ga.Specification, " \
        #       "ga.Process, ga.MACHINE, ga.Groups, ga.Line_CODE, ga.Day_Night, " \
        #       "ga.Ok_Ng, ga.Daywork, ga.Goodness, ga.Badness, mc.Language2, mc.Language3 " \
        #       "FROM Gathering_Data AS ga INNER JOIN MACHINE AS mc ON ga.MACHINE = mc.CODE " \
        #       "WHERE ga.Work_date BETWEEN %s AND %s ORDER BY ga.work_date DESC "
        # 2021.03.21 Conclusion. 2021년을 넘어 오면서, [MACHINE.CODE] 값을 [2]자리에서, [3]자리로 변경한 관계로,
        #           ===> [MACHINE.CODE]로 INNER JOIN할 경우, 2020년도 자료 조회가 불가능하다.
        # sql = "SELECT ga.Gathering_No, ga.Facilities, ga.Work_date, ga.CODE, ga.Specification, " \
        #       "ga.Process, ga.MACHINE, ga.Groups, ga.Line_CODE, ga.Day_Night, " \
        #       "ga.Ok_Ng, ga.Daywork, ga.Goodness, ga.Badness, gr.Language2, gr.Language3 " \
        #       "FROM Gathering_Data AS ga INNER JOIN Groups AS gr ON ga.Groups = gr.CODE " \
        #       "WHERE ga.Work_date BETWEEN %s AND %s ORDER BY ga.work_date DESC "
        # 아래는 Groups.CODE 조인, t_Procuct.StandardTime 추가.
        sql = "SELECT ga.GATHERING_NO, ga.FACILITIES, ga.WORK_DATE, ga.CODE, ga.SPECIFICATION, " \
              "ga.PROCESS, ga.MACHINE, ga.GROUPSS, ga.LINE_CODE, ga.DAY_NIGHT, " \
              "ga.OK_NG, ga.DAYWORK, ga.GOODNESS, ga.BADNESS, gr.LANGUAGE2, gr.LANGUAGE3, pd.STANDARDTIME, pd.CODETWINS " \
              "FROM GATHERING_DATA AS ga INNER JOIN GROUPSS AS gr ON ga.GROUPSS = gr.CODE " \
              "INNER JOIN T_PRODUCT AS pd ON ga.CODE = pd.CODE " \
              "WHERE ga.WORK_DATE BETWEEN %s AND %s ORDER BY ga.WORK_DATE DESC "
        # 2021.03.24 Found. [ga.Line_CODE] 원본은 [MACHINE.LINECODE]이며, 향후 검토 대상. 현재는 그냥 간다...
    else:
        print(get_line_no(), "processCode: ", processCode, "에 대한 자료만 필터합니다.")
        values = (fromDateStartString, fromDateEndString, processCode)
        # 아래는 Groups.Code 조인, t_Procuct.StandardTime 추가.
        # sql = "SELECT ga.Gathering_No, ga.Facilities, ga.Work_date, ga.CODE, ga.Specification, " \
        #       "ga.Process, ga.MACHINE, ga.Groups, ga.Line_CODE, ga.Day_Night, " \
        #       "ga.Ok_Ng, ga.Daywork, ga.Goodness, ga.Badness, gr.Language2, gr.Language3, pd.StandardTime, pd.CODETwins " \
        #       "FROM Gathering_Data AS ga INNER JOIN Groups AS gr ON ga.Groups = gr.CODE " \
        #       "INNER JOIN t_Product AS pd ON ga.CODE = pd.CODE " \
        #       "WHERE (ga.Work_date BETWEEN %s AND %s) AND ga.Process = %s ORDER BY ga.work_date DESC "
        # 2022.03.29 Edited. Groups ===> Groupss ∵)MSSQL ===> MySql
        sql = "SELECT ga.GATHERING_NO, ga.FACILITIES, ga.WORK_DATE, ga.CODE, ga.SPECIFICATION, " \
              "ga.PROCESS, ga.MACHINE, ga.GROUPSS, ga.LINE_CODE, ga.DAY_NIGHT, " \
              "ga.OK_NG, ga.DAYWORK, ga.GOODNESS, ga.BADNESS, gr.LANGUAGE2, gr.LANGUAGE3, pd.STANDARDTIME, pd.CODETWINS " \
              "FROM GATHERING_DATA AS ga INNER JOIN GROUPSS AS gr ON ga.GROUPSS = gr.CODE " \
              "INNER JOIN T_PRODUCT AS pd ON ga.CODE = pd.CODE " \
              "WHERE (ga.WORK_DATE BETWEEN %s AND %s) AND ga.PROCESS = %s ORDER BY ga.WORK_DATE DESC "
        # 아래는 Groups.CODE 조인.
        # sql = "SELECT ga.Gathering_No, ga.Facilities, ga.Work_date, ga.CODE, ga.Specification, " \
        #       "ga.Process, ga.MACHINE, ga.Groups, ga.Line_CODE, ga.Day_Night, " \
        #       "ga.Ok_Ng, ga.Daywork, ga.Goodness, ga.Badness, gr.Language2, gr.Language3 " \
        #       "FROM Gathering_Data AS ga INNER JOIN Groups AS gr ON ga.Groups = gr.CODE " \
        #       "WHERE ga.Work_date BETWEEN %s AND %s AND ga.Process = %s ORDER BY ga.work_date DESC "
        # 아래는 최초 MACHINE.CODE 조인.
        # sql = "SELECT ga.Gathering_No, ga.Facilities, ga.Work_date, ga.CODE, ga.Specification, " \
        #       "ga.Process, ga.MACHINE, ga.Groups, ga.Line_CODE, ga.Day_Night, " \
        #       "ga.Ok_Ng, ga.Daywork, ga.Goodness, ga.Badness, mc.Language2, mc.Language3 " \
        #       "FROM Gathering_Data AS ga INNER JOIN MACHINE AS mc ON ga.MACHINE = mc.CODE " \
        #       "WHERE ga.Work_date BETWEEN %s AND %s AND ga.Process = %s ORDER BY ga.work_date DESC "

    # print(get_line_no(), "sql: ", sql)
    print(get_line_no(), "values: ", values)

    try:
        # print("===========================================================================================")
        # print("__getProductionCurrent views.cursArrayWeb() 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...", values)
        # print("===========================================================================================")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    except:  # DB 연결을 한 번 더 시도...
        # if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        if type(mySqlWebDb) is pymysql.connections.Connection or type(
            cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), "Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), "Database 연결을 확인하시오!")

        # print(get_line_no(), "values: ", values)
        if values == '':
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의... cursArrayWeb.execute(sql, from_date, to_date)
        else:
            # print(get_line_no(), ", _dbMrp.py __getGatheringData sql: ", sql)
            # print(get_line_no(), ", _dbMrp.py __getGatheringData values: ", values)
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의.. cursArrayWeb.execute(sql, from_date, to_date)
        # print("_dbMrp.py __getGatheringData 디버깅... 2-1")

    try:
        CONNECTEDWEB = True

        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("_dbMrp.py __getGatheringData sqlQuerySets: \n", sqlQuerySets)
        # print("_dbMrp.py __getGatheringData type(sqlQuerySets): ", type(sqlQuerySets))
        # print(get_line_no(), ", __dbMrp.py len(sqlQuerySets): ", len(sqlQuerySets))

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print("_dbMrp.py __getGatheringData dfSets: \n", dfSets)
        # print("_dbMrp.py __getGatheringData type(dfSets): ", type(dfSets))
        # print(get_line_no(), ", __dbMrp.py len(dfSets): ", len(dfSets))

        # 2021.02.06 Added. 빈 dfSets 확인.
        # if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
        #     print("__getGatheringData 조건에 맞는 자료가 없습니다. 다시 확인하시오!")
        # else:
        #     # 2021.02.21 Conclusion. ProductionActual.Mp 컬럼인 생산 능력 수량 ['volumn'] 값은, DataFrame에서 추가한다.
        #     # 아니다... 여기서 가져오고, [DataFrame]에서는 그 값을 정리만 한다.
        dfSets.columns = ['GATHERINGNO', 'FACILITIES', 'WORK_DATE', 'CODE', 'STEP9', 'PROCESS', 'MACHINE',
                          'GROUPSS', 'LINE_CODE', 'DAY_NIGHT',
                          'OK_NG', 'DAYWORK', 'GOODNESS', 'BADNESS', 'MACHINE_KOR', 'MACHINE_LOC', 'STANDARDTIME', 'CODETWINS']
        # print("__getGatheringData 컬럼명 변경 후 dfSets: \n", dfSets)
        # print("__getGatheringData 컬럼명 변경 후 type(dfSets): ", type(dfSets))
        # print(get_line_no(), ", __dbMrp.py 컬럼명 변경 후 len(dfSets): ", len(dfSets))

        # 2021.03.20 Added. 작업 시간 분리 후 컬럼 추가: 이것은 반드시, 날짜를 문자형으로 변경 전, [날짜형]일 때, 처리해야 한다.
        # dfSets['work_year'] = dfSets['work_date'].dt.year
        # dfSets['work_month'] = dfSets['work_date'].dt.month
        # dfSets['work_day'] = dfSets['work_date'].dt.day
        dfSets['WORK_HOUR'] = dfSets['WORK_DATE'].dt.hour
        # dfSets['work_minute'] = dfSets['work_date'].dt.minute
        # dfSets['work_second'] = dfSets['work_date'].dt.second
        # print("2 __getGatheringData::dfSets: \n", dfSets)
        # print("2 __getGatheringData::type(dfSets): ", type(dfSets))
        # print(get_line_no(), ", __dbMrp.py len(dfSets): ", len(dfSets))

        # 2021.01.31 Added. workdate.작업일자 컬럼은 TimeStamp.시간 정보는 전혀 필요가 없기에, [문자형 타입]으로 변환...
        dfSets['WORK_DATE'] = dfSets['WORK_DATE'].astype(str)
        # print("1 __getGatheringData::dfSets: \n", dfSets)
        # print("1 __getGatheringData::type(dfSets): ", type(dfSets))
        # print(get_line_no(), ", __dbMrp.py  len(dfSets): ", len(dfSets))

        # 2021.03.23 Added. 실시간 자료에서는 시간이 정확하게 등록되어 있으므로, 날짜로만 그룹화하기 위해, 시간 데이터 빼내기...
        # dfSets['workdate'] = dfSets['work_date'].astype(str).str[:10]
        dfSets['WORKDATE'] = dfSets['WORK_DATE'].str[:10]
        # print("11 __getGatheringData::dfSets: \n", dfSets)
        # print("11 __getGatheringData::type(dfSets): ", type(dfSets))
        # print(get_line_no(), ", __dbMrp.py len(dfSets): ", len(dfSets))

        # dfSets['LINE_CODE'] = dfSets['LINE_CODE'].astype(str).str.zfill(2)    # 15.60 ms per loop
        # dfSets['LINE_CODE'] = dfSets['LINE_CODE'].map(lambda x: f'{x:0>2}')   #  5.46 ms per loop
        # dfSets['LINE_CODE'] = dfSets['LINE_CODE'].map('{:0>2}'.format)        #  4.06 ms per loop
        # print("7 __getGatheringData::dfSets: \n", dfSets)
        # print("7 __getGatheringData::type(dfSets): ", type(dfSets))
        # print("7 __getGatheringData::len(dfSets): ", len(dfSets))

        if LANGUAGE_NO == 1042:
        # if LANGUAGE_NO == 'korean':
            # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].astype(str) + " " + dfSets['MACHINE_kor']
            # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].map(lambda x: f'{x:0>2}') + " " + dfSets['MACHINE_kor']
            dfSets['MACHINEINFO'] = dfSets['LINE_CODE'].map('{:0>2}'.format) + " " + dfSets['MACHINE_KOR']
        else:
            # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].astype(str) + " " + dfSets['MACHINE_loc']
            # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].map(lambda x: f'{x:0>2}') + " " + dfSets['MACHINE_loc']
            dfSets['MACHINEINFO'] = dfSets['LINE_CODE'].map('{:0>2}'.format) + " " + dfSets['MACHINE_LOC']
        # print("8 __getGatheringData MACHINEinfo 추가 후 dfSets: \n", dfSets)
        # print("8 _dbMrp.py __getGatheringData 디버깅... 8")

        # dfSets['CODEspec'] = dfSets['CODE'] + " " + dfSets['STEP9']
        # print("9 __getGatheringData CODEspec 추가 후 dfSets: \n", dfSets)
        # print(get_line_no(), ", __dbMrp.py len(dfSets): ", len(dfSets))

    except:
        CONNECTEDWEB = False
        # dfSets = pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])
        # dfSets = pd.DataFrame(index=range(0, 0), columns=['INDEX', 'NUMBER'])
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])  # 필수 컬럼 세팅...
        # print("경고, __getGatheringData dfSets: \n", dfSets)
        print(get_line_no(), ", __dbMrp.py [callMainData]에서, 실시간 생산 실적 수집 자료가 전혀 없습니다."
                             " 관리자에게 문의하시오!")

    return sqlQuerySets, dfSets, fromDateStartString, fromDateEndString, NIGHT_CLOSING_HHMMSS


def __getProductionCurrent(fromDate, toDate, processCode, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    year = fromDate[:4]
    month = fromDate[5:7]
    # serial = "0001"  # 사업 계획 Revision은 필요 없고, 그냥 [달]을 4자리로 하여 처리...
    revision = year + "00" + month
    # print("_dbMrp.py     # print("_dbMrp.py __getProductionCurrent month: ", month) revision: ", revision)

    # 해당 월도의 마지막 날짜를 찾는다.
    maxDate = __getMaxDate(year, month)
    # print("__getProductionCurrent 55 maxDate: ", maxDate)

    # [ppp_current.생산 진도 관리]는 반드시 1개월 단위로만 관리해야 하므로, 기간의 종료 날짜를 이번달 말일로 새로 넣어준다.
    # toDate = datetime.strptime(year + "-" + month + "-" + maxDate, "%Y-%m-%d")  # <class 'datetime.datetime'>
    toDate = year + "-" + month + "-" + maxDate  # <str>
    # print("__getProductionCurrent 555 fromDate: ", fromDate)
    # print("__getProductionCurrent 555 toDate: ", toDate)
    # print("__getProductionCurrent 555 type(fromDate): ", type(fromDate))
    # print("__getProductionCurrent 555 type(toDate): ", type(toDate))

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getProductionCurrent mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    if str(processCode).lower() == 'all' or str(processCode) == '0000':
        # print("1 __getProductionCurrent() Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")

        # 1. fo.Revision: 관리 번호
        # 2. fo.Code: 제품 코드
        # mc.Language2: 설비명 korea
        # mc.Language3: 설비명 local
        # fo.Duduction: 근무 일수: 해당 월 + 해당 공정
        # 3. fo.Coefficient: Cycle Time (초)
        # 4. fo.PoBal: 소요 일수
        # fo.Minimum: 소요 시간
        # fo.Tmp: UPH
        # 5. ma.Goods2: 구분: 용접이면, 1.로타리, 2.반자동, 3.고주파, 4.수동, 조립이면, 1.?, 2.?
        # fo.WorkBaseDay: UPD
        # 6. fo.Stock: 월초 재고: 월말 재고 조사 수량을 차월초 재고로 등록...
        # 7. fo.Dpt: 생산 계획 합
        # 8. fo.Dst: 생산 계획 잔량 합
        # 9. fo.Nmt: 달성률
        # 10. fo.Nst: 현재 재고
        # fo.ClassMonth: 생산 라인 코드 3자리: String, (LINECODE.라인 번호는 중복이 있어 사용 불가)
        # 11. fo.Dm01 - Dm31: 생산 실적 수량
        # 12. fo.Nf01 - Nf31: 생산 실적 누계 수량

        # dfSets.columns = ['revision', 'CODE', 'STEP9', 'ct', 'needsday',
        #               'division', 'stockfirst', 'dpt', 'dft', 'dmt', 'dst', 'npt', 'nft', 'nst',
        #               'MACHINE', 'MACHINE_kor', 'MACHINE_loc', 'PROCESS', 'PROCESS_kor', 'PROCESS_loc']
        #
        # values = (revision)
        # sql = "Select fo.Revision, fo.CODE, ma.STEP9, fo.Coefficient, fo.PoBal, " \
        #       "ma.Goods2, fo.Stock, fo.Dpt, fo.Dft, fo.Dmt, fo.Dst, fo.Npt, fo.Nft, fo.Nst, " \
        #       "fo.ClassMonth, mc.Language2, mc.Language3, ma.PROCESS, pr.Language2, pr.Language3, " \
        #       "fo.Dm1, fo.Dm2, fo.Dm3, fo.Dm4, fo.Dm5, fo.Dm6, fo.Dm7, fo.Dm8, fo.Dm9, fo.Dm10, " \
        #       "fo.Dm11, fo.Dm12, fo.Dm13, fo.Dm14, fo.Dm15, fo.Dm16, fo.Dm17, fo.Dm18, fo.Dm19, fo.Dm20, " \
        #       "fo.Dm21, fo.Dm22, fo.Dm23, fo.Dm24, fo.Dm25, fo.Dm26, fo.Dm27, fo.Dm28, fo.Dm29, fo.Dm30, fo.Dm31, " \
        #       "fo.Nf1, fo.Nf2, fo.Nf3, fo.Nf4, fo.Nf5, fo.Nf6, fo.Nf7, fo.Nf8, fo.Nf9, fo.Nf10, " \
        #       "fo.Nf11, fo.Nf12, fo.Nf13, fo.Nf14, fo.Nf15, fo.Nf16, fo.Nf17, fo.Nf18, fo.Nf19, fo.Nf20, " \
        #       " fo.Nf21, fo.Nf22, fo.Nf23, fo.Nf24, fo.Nf25, fo.Nf26, fo.Nf27, fo.Nf28, fo.Nf29, fo.Nf30, fo.Nf31 " \
        #       "From ForecastHistoryDay AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
        #       "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE  INNER JOIN MACHINE AS mc ON fo.ClassMonth = mc.CODE " \
        #       "WHERE fo.Revision = %s " \
        #       "ORDER BY fo.Revision Desc, ma.PROCESS Desc, fo.ClassMonth, ma.STEP9 "

        # 2021.032.08 Conclusion. 위의 방식은 문제가 좀 있다. 생산 실적 등록을 완료하였음에도,
        # 생산 능력에서 [실적 자료] 버튼을 클릭하지 않으면, ForecastHistoryDay.NFxx 컬럼이 정리가 안 되어,
        # [생산 진도 관리]를 볼 수가 없다.
        # 그러므로 ProductionActual.생산 실적 자료를 직접 가져와서 처리한다.
        values = (fromDate, toDate)
        sql = "Select pa.WORKDATE, pa.PRODUCTIONACTUALNO, pa.CODE, ma.STEP9, pa.GOODNESS, pa.BADNESS, pa.MP pa.AP, pd.CODETWINS, " \
              "ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, pa.MACHINE, pa.GROUPSS, pa.WORKFROM, pa.WORKTO, pd.STANDARDTIME " \
              "From PRODUCTIONACTUAL AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE AND pa.GOODNESS <> 0 " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE INNER JOIN T_PRODUCT AS pd ON ma.CODE = pd.CODE " \
              "WHERE pa.WORKDATE BETWEEN %s AND %s ORDER BY pa.WORKDATE DESC "
    else:
        # print("__getProductionCurrent processCode: ", processCode, "에 대한 자료만 필터합니다.")
        values = (fromDate, toDate, processCode)
        sql = "Select pa.WORKDATE, pa.PRODUCTIONACTUALNO, pa.CODE, ma.STEP9, pa.GOODNESS, pa.BADNESS, pa.MP, pa.AP, pd.CODETWINS," \
              "ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, pa.MACHINE, pa.GROUPSS, pa.WORKFROM, pa.WORKTO, pd.STANDARDTIME " \
              "From PRODUCTIONACTUAL AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE AND pa.GOODNESS <> 0 " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE INNER JOIN T_PRODUCT AS pd ON ma.CODE = pd.CODE " \
              "WHERE pa.WORKDATE BETWEEN %s AND %s AND ma.PROCESS = %s ORDER BY pa.WORKDATE DESC "

        # values = (revision, processCode)
        # sql = "Select fo.Revision, fo.CODE, ma.STEP9, fo.Coefficient, fo.PoBal, " \
        #       "ma.Goods2, fo.Stock, fo.Dpt, fo.Dft, fo.Dmt, fo.Dst, fo.Npt, fo.Nft, fo.Nst, " \
        #       "fo.ClassMonth, mc.Language2, mc.Language3, ma.Process, pr.Language2, pr.Language3, " \
        #       "fo.Dm1, fo.Dm2, fo.Dm3, fo.Dm4, fo.Dm5, fo.Dm6, fo.Dm7, fo.Dm8, fo.Dm9, fo.Dm10, " \
        #       "fo.Dm11, fo.Dm12, fo.Dm13, fo.Dm14, fo.Dm15, fo.Dm16, fo.Dm17, fo.Dm18, fo.Dm19, fo.Dm20, " \
        #       "fo.Dm21, fo.Dm22, fo.Dm23, fo.Dm24, fo.Dm25, fo.Dm26, fo.Dm27, fo.Dm28, fo.Dm29, fo.Dm30, fo.Dm31, " \
        #       "fo.Nf1, fo.Nf2, fo.Nf3, fo.Nf4, fo.Nf5, fo.Nf6, fo.Nf7, fo.Nf8, fo.Nf9, fo.Nf10, " \
        #       "fo.Nf11, fo.Nf12, fo.Nf13, fo.Nf14, fo.Nf15, fo.Nf16, fo.Nf17, fo.Nf18, fo.Nf19, fo.Nf20, " \
        #       " fo.Nf21, fo.Nf22, fo.Nf23, fo.Nf24, fo.Nf25, fo.Nf26, fo.Nf27, fo.Nf28, fo.Nf29, fo.Nf30, fo.Nf31 " \
        #       "From ForecastHistoryDay AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
        #       "INNER JOIN Process AS pr ON ma.Process = pr.CODE  INNER JOIN MACHINE AS mc ON fo.ClassMonth = mc.CODE " \
        #       "WHERE fo.Revision = %s AND ma.Process = %s " \
        #       "ORDER BY fo.Revision Desc, ma.Process Desc, fo.ClassMonth, ma.STEP9 "

    try:
        # print("===========================================================================================")
        # print("__getProductionCurrent views.cursArrayWeb() 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...", values)
        # print("===========================================================================================")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

        # print("_dbMrp.py __getProductionCurrent 디버깅... 1-1")
        if values == '':
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        else:
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # print("_dbMrp.py __getProductionCurrent 디버깅... 2-1")

    try:
        CONNECTEDWEB = True
        # print("_dbMrp.py __getProductionCurrent 디버깅... 3")

        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("_dbMrp.py __getProductionCurrent sqlQuerySets: \n", sqlQuerySets)
        # print("_dbMrp.py __getProductionCurrent type(sqlQuerySets): ", type(sqlQuerySets))
        # print("_dbMrp.py __getProductionCurrent len(sqlQuerySets): ", len(sqlQuerySets))
        # print("_dbMrp.py __getProductionCurrent 디버깅... 4")

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print("_dbMrp.py __getProductionCurrent dfSets: \n", dfSets)
        # print("_dbMrp.py __getProductionCurrent type(dfSets): ", type(dfSets))
        # print("_dbMrp.py __getProductionCurrent len(dfSets): ", len(dfSets))
        # print("_dbMrp.py __getProductionCurrent 디버깅... 6")

        # 2021.02.06 Added. 빈 dfSets 확인.
        # if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
        #     print("__getProductionCurrent 조건에 맞는 자료가 없습니다. 다시 확인하시오!")
        # else:
        #     # 2021.02.21 Conclusion. ProductionActual.Mp 컬럼인 생산 능력 수량 ['volumn'] 값은, DataFrame에서 추가한다.
        #     # 아니다... 여기서 가져오고, [DataFrame]에서는 그 값을 정리만 한다.
        dfSets.columns = ['WORKDATE', 'PRODUCTIONACTUALNO', 'CODE', 'STEP9', 'GOODNESS', 'BADNESS', 'VOLUME',
                          'SCHEDULE', 'CODETWINS',
                          'PROCESS', 'PROCESS_KOR', 'PROCESS_LOC', 'MACHINE', 'GROUPSS', 'WORKFROM', 'WORKTO',
                          'STANDARDTIME']
        # print("__getProductionCurrent 컬럼명 변경 후 dfSets: \n", dfSets)

        # 2021.01.31 Added. WORKDATE.작업일자 컬럼은 TimeStamp.시간 정보는 전혀 필요가 없기에, [문자형 타입]으로 변환...
        dfSets['WORKDATE'] = dfSets['WORKDATE'].astype(str)
        # print("__getProductionCurrent::type(dfSets): ", type(dfSets))
        # print("__getProductionCurrent::len(dfSets): ", len(dfSets))
        # print("__getProductionCurrent::dfSets: \n", dfSets)

        # print("_dbMrp.py __getProductionCurrent 디버깅... 7")
        # dfSets['CODEspec'] = dfSets['CODE'] + " " + dfSets['STEP9']
        # print("__getProductionCurrent CODEspec 추가 후 dfSets: \n", dfSets)
        # print("_dbMrp.py __getProductionCurrent 디버깅... 8")

        if LANGUAGE_NO == 1042:
        # if LANGUAGE_NO == 'korean':
            dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_KOR']
        else:
            dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_LOC']
        # print("__getProductionCurrent processinfo 추가 후 dfSets: \n", dfSets)
        # print("_dbMrp.py __getProductionCurrent 디버깅... 8")

        # if len(dfSets) > 0:
        #     if ProcessCode == 'all':
        #         processInfoCurrent = 'ALL'
        #     else:
        #         processInfoCurrent = dfSets.at[0, 'processinfo']
        # print("__getProductionCurrent processInfoCurrent 추가 후 processInfoCurrent: \n", processInfoCurrent)

    except:
        CONNECTEDWEB = False
        # dfSets = pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])
        # dfSets = pd.DataFrame(index=range(0, 0), columns=['INDEX', 'NUMBER'])
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py 경고, dfSets: \n", dfSets)
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlQuerySets, dfSets, toDate


# 2021.05.14 Created. 납품 자료.
def __getShippingData(fromDate, toDate, classId, tradeId):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    # debugPath = "_dbMrp.py __getShippingData()"

    # print(debugPath, ", type(fromDate): ", type(fromDate))
    # print(debugPath, ", fromDate: ", fromDate)
    # print(debugPath, ", toDate: ", toDate)
    # print(debugPath, ", 0 classId: ", classId)
    # print(debugPath, ", 0 tradeId: ", tradeId)
    # print(debugPath, ", timezone.now(): ", timezone.now())

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(debugPath, ", mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print(debugPath, ", Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            # print(debugPath, ", Database 연결을 확인하시오!")

    # 2021.03.21 Conclusion. 컬럼 정리.
    if classId == 0:
        if tradeId == 0:
            # print(debugPath, ", 11 Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")
            # fromDate = "2020-11-01"  # for Debugging...
            values = (fromDate, toDate)
            # 2021.05.14 Conclusion. "Shipping.BUYER2.거래처명"음 "DB"가 다른 관계로, 나중에 따로 붙힌다.
            sql = "Select sd.SHIPPINGDATE, sd.RECEIVINGORDERNO, sd.SHIPPINGORDERNO, sd.SHIPPINGNO, sd.CODE, " \
                  "sd.SHIPPEDQTY, sd.UP, sd.LOTNO, sd.WAREHOUSE, ma.STEP9, ma.GOODS0, ma.GOODS1, ma.GOODS5, " \
                  "ma.DESCRIPTION, sh.BUYER2 " \
                  "From SHIPPINGDATA AS sd INNER JOIN GOODSMASTER AS ma ON sd.CODE = ma.CODE " \
                  "INNER JOIN SHIPPING AS sh ON sh.SHIPPINGNO = sd.SHIPPINGNO " \
                  "WHERE sd.SHIPPINGDATE BETWEEN %s AND %s AND sd.SHIPPEDQTY <> 0 " \
                  "ORDER BY sd.SHIPPINGNO DESC, sd.SHIPPINGDATE DESC "

            # "INNER JOIN Goods5 AS g5 ON ma.Goods5 = g5.Id " \ # 2021.05.15 Conclusion. 여긴 미묘한 문제가 있다.
            # 현재 "GOODSMASTER.Goods5" 컬럼을 "874" 또는 "374" 등으로 즉, 제품의 분류 컬럼으로 사용하기로 했지만,
            # "GOODSMASTER.Goods5" 컬럼이 모든 값이 들어 있는 것도 아니고,
            # 또한 "GOODSMASTER.Goods5" 값이 비어 있더라도, 비어 있는 대로, 여기서 중요한 "납품" 정보를 뿌려 주는 것이 목적이므로,
            # "Goods5" 컬럼을 "키"로 "INNER JOIN"하게 되면 절대로 안 되는 것이다. 조인이 안 되는 품목은 아예 뿌려지질 않기 때문에.
            # 그러므로 "Goods5.Language" 정보는 필요할 때 따로 불러서, 컬럼을 추가해 주는 방법으로 처리해야 한다.
        else:
            values = (fromDate, toDate, tradeId)
            # 2021.05.14 Conclusion. "Shipping.BUYER2.거래처명"음 "DB"가 다른 관계로, 나중에 따로 붙힌다.
            sql = "Select sd.SHIPPINGDATE, sd.RECEIVINGORDERNO, sd.SHIPPINGORDERNO, sd.SHIPPINGNO, sd.CODE, " \
                  "sd.SHIPPEDQTY, sd.UP, sd.LOTNO, sd.WAREHOUSE, ma.STEP9, ma.GOODS0, ma.GOODS1, ma.GOODS5, " \
                  "ma.DESCRIPTION, sh.BUYER2 " \
                  "From SHIPPINGDATA AS sd INNER JOIN GOODSMASTER AS ma ON sd.CODE = ma.CODE " \
                  "INNER JOIN SHIPPING AS sh ON sh.SHIPPINGNO = sd.SHIPPINGNO " \
                  "WHERE sd.SHIPPINGDATE BETWEEN %s AND %s AND sd.SHIPPEDQTY <> 0 AND sh.BUYER2 = %s " \
                  "ORDER BY sd.SHIPPINGNO DESC, sd.SHIPPINGDATE DESC "

    else:
        if tradeId == 0:
            values = (fromDate, toDate, classId)
            sql = "Select sd.SHIPPINGDATE, sd.RECEIVINGORDERNO, sd.SHIPPINGORDERNO, sd.SHIPPINGNO, sd.CODE, " \
                  "sd.SHIPPEDQTY, sd.UP, sd.LOTNO, sd.WAREHOUSE, ma.STEP9, ma.GOODS0, ma.GOODS1, ma.GOODS5, " \
                  "ma.DESCRIPTION, sh.BUYER2 " \
                  "From SHIPPINGDATA AS sd INNER JOIN GOODSMASTER AS ma ON sd.CODE = ma.CODE " \
                  "INNER JOIN SHIPPING AS sh ON sh.SHIPPINGNO = sd.SHIPPINGNO " \
                  "WHERE sd.SHIPPINGDATE BETWEEN %s AND %s AND sh.BUYER2 = %s AND sd.SHIPPEDQTY <> 0 " \
                  "ORDER BY sd.SHIPPINGNO DESC, sd.SHIPPINGDATE DESC "
        else:
            values = (fromDate, toDate, classId, tradeId)
            sql = "Select sd.SHIPPINGDATE, sd.RECEIVINGORDERNO, sd.SHIPPINGORDERNO, sd.SHIPPINGNO, sd.CODE, " \
                  "sd.SHIPPEDQTY, sd.UP, sd.LOTNO, sd.WAREHOUSE, ma.STEP9, ma.GOODS0, ma.GOODS1, ma.GOODS5, " \
                  "ma.DESCRIPTION, sh.BUYER2 " \
                  "From SHIPPINGDATA AS sd INNER JOIN GOODSMASTER AS ma ON sd.CODE = ma.CODE " \
                  "INNER JOIN SHIPPING AS sh ON sh.SHIPPINGNO = sd.SHIPPINGNO " \
                  "WHERE sd.SHIPPINGDATE BETWEEN %s AND %s AND ma.GOODS5 = %s AND sh.BUYER2 = %s AND sd.SHIPPEDQTY <> 0 " \
                  "ORDER BY sd.SHIPPINGNO DESC, sd.SHIPPINGDATE DESC "

        # "INNER JOIN Goods5 AS g5 ON ma.Goods5 = g5.Id " \ # 2021.05.15 Conclusion. 여긴 미묘한 문제가 있다.

    # dfSets.columns = ['SHIPPINGDATE', 'receivingorderno', 'shkppingorderno', 'SHIPPINGNO', 'CODE',
    #                   'SHIPPEDQTY', 'UP', 'LOTNO', 'WAREHOUSE', 'STEP9', 'GOODS0', 'GOODS1', 'class_id',
    #                   'DESCRIPTION', 'TRADE']
    # print(debugPath, ", 디버깅... 2-1 sql: ", sql)
    # print(debugPath, ", 디버깅... 2-1 values: ", values)
    try:
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
            # print(debugPath, ", 디버깅... 2-1")

    try:
        CONNECTEDWEB = True
        # print(debugPath, ", 디버깅... 3")
        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(debugPath, ", 디버깅... 4")
        # print(debugPath, ", sqlQuerySets: ", sqlQuerySets)
        # print(debugPath, ", type(sqlQuerySets): ", type(sqlQuerySets))
        # print(debugPath, ", len(sqlQuerySets): ", len(sqlQuerySets))

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print(debugPath, ", dfSets: \n", dfSets)
        # print(debugPath, ", type(dfSets): ", type(dfSets))
        # print(debugPath, ", len(dfSets): ", len(dfSets))

        # 2021.02.06 Added. 빈 dfSets 확인.
        if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
            print(get_line_no(), ", 조건에 맞는 자료가 없습니다. 다시 확인하시오!")
        else:
            dfSets.columns = ['SHIPPING_DATE', 'RECEIVING_ORDER_NO', 'SHIPPING_ORDER_NO', 'SHIPPING_NO', 'CODE',
                              'SHIPPED_QTY', 'UP', 'LOTNO', 'WAREHOUSE', 'STEP9', 'GOODS0', 'GOODS1', 'GOODS5',
                              'DESCRIPTION', 'TRADE']
            dfSets['SHIPPING_DATE'] = dfSets['SHIPPING_DATE'].astype(str)
            # print(debugPath, ", type(dfSets): ", type(dfSets))
            # print(debugPath, ", len(dfSets): ", len(dfSets))
            # print(debugPath, ", dfSets: \n", dfSets)

            # if LANGUAGE_NO == 1042:
            #     dfSets['classinfo'] = dfSets['class_id'] + " " + dfSets['class_kor']
            # else:
            #     dfSets['classinfo'] = dfSets['class_id'] + " " + dfSets['class_loc']
            # print(debugPath, ", processinfo 추가 후 dfSets: \n", dfSets)
            # print(debugPath, ", 디버깅... 8")
    except:
        CONNECTEDWEB = False
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlQuerySets, dfSets, NIGHT_CLOSING_HHMMSS

# todo: 2022.04.29 Added. 북경 조이 생산 현황은 "전체 공정 제품 수"가 많지 않은 관계로, "processCode.공정코드" 값을 "0000"으로
#  주어, "전체 공정 전체 품목"을 뿌려 줄 수 있게 한다.
def __getProductionPerformance(fromDate, toDate, processCode, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    # debugPath = "db_Mrp.py __getProductionPerformance()"

    # print(debugPath, ", type(fromDate): ", type(fromDate))
    print(get_line_no(), ", fromDate: ", fromDate)
    print(get_line_no(), ", toDate: ", toDate)
    print(get_line_no(), "processCode: ", processCode)
    print(get_line_no(), "HOST3: ", HOST3)
    print(get_line_no(), "DBNAME3: ", DBNAME3)
    # print(debugPath, ", timezone.now(): ", timezone.now())

    # 2021.02.18 Conclusion. 아래는 다음과 같은 에러가 발생한다. [workdate_lte] 요기 때문...
    # RuntimeWarning: DateTimeField ProductionActual.workdate received a naive datetime (2020-12-31 08:00:00) while time zone support is acti
    # ve.   RuntimeWarning)
    # qrProductionPerformance = ProductionActual.objects\
    #     .values('workdate', 'productionactualno', 'code', 'goodness', 'badness', 'daywork')\
    #     .filter(workdate_lte=fromDateDate, workdate__gte=toDateDate)

    if CONNECTEDWEB == False:
        # 2021.03.01 Conclusion. WEB DB 웹 Database 또한 [MS SQL]로 최종 결정되었다.
        # mySqlLocalDb, cursArray, cursDict, \
        # COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, BOUNCE_TIME, SLEEP_TIME, \
        # TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS, \
        # FORPRODUCINGORDERDATA, PROCESS, GROUPS, DESCRIPTION_TEXT, LINE_CODE, \
        # WORK_DATE, DAY_NIGHT, GOODS, CODE, CAVITY, GOODSRIGHT, CODERIGHT, CAVITYRIGHT, TO_WAREHOUSE, \
        # FACODE, PRODUCTSELECTION, PLCBIT, FRONTJISNO, TRADE, UI, BAUDRATE = connectWebMyDB()
        # if mySqlLocalDb:

        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(debugPath, ", mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            # print("3 __getProductionPerformance Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            # print("3 __getProductionPerformance Database 연결을 확인하시오!")
        # print(debugPath, ", mySqlLocalDb: ", mySqlLocalDb, "type(mySqlLocalDb):", type(mySqlLocalDb))
        # print(debugPath, ", cursArray: ", cursArray, "type(cursArray):", type(cursArray))
        # print(debugPath, ", cursDict: ", cursDict, "type(cursDict):", type(cursDict))
        # print(debugPath, ", HOST3: ", HOST3, "type(HOST3):", type(HOST3))
        # print(debugPath, ", USER3: ", USER3, "type(USER3):", type(USER3))
        # print(debugPath, ", DBNAME3: ", DBNAME3, "type(DBNAME3):", type(DBNAME3))

    # 2021.02.21 Added. 자료를 가져오기 전에, 먼저 [Mp.작업 시간]을 찍어준다. [Mp] 컬럼은 임시로 사용한다.
    # 아니다... 그냥 [DataFrame]에서 처리하자...
    # sql = "UPDATE ProductionActual Set Mp = WorkTo - WorkFrom WHERE WorkDate BETWEEN %s AND %s ORDER BY WorkDate DESC "

    # 2021.03.21 Conclusion. 컬럼 정리.
    # 1. [pa.Ap = 생산 계획 수량] : 나중에 사용할 컬럼
    # 2. [pa.Mp = 생산 능력 수량] 컬럼은 [pa.WorkTo], [pa.WorkFrom], [t_Product.StandardTime] 컬럼으로 계산하여,
    #    [pandas.DataFrame]에서 [pa.Mp=volume] 컬럼에 정리.
    print(get_line_no(), "processCode: ", processCode)
    if str(processCode).lower() == 'all' or str(processCode) == '0000':
        # print("1 __getProductionPerformance() Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")
        values = (fromDate, toDate)
        # 2021.03.01 Conclusion. WEB DB 웹 Database 또한 [MS SQL]로 최종 결정되었다.
        # sql = "Select pa.WorkDate, pa.ProductionActualNo, pa.Code, ma.STEP9, pa.Goodness, pa.Badness, pa.Mp, pa.Ap, pd.CodeTwins, " \
        #       "ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, pa.WorkFrom, pa.WorkTo, pd.StandardTime "\
        #       "From ProductionActual AS pa LEFT JOIN GOODSMASTER AS ma ON TRIM(pa.Code) = TRIM(ma.Code) " \
        #       "LEFT JOIN t_Product AS pd ON TRIM(ma.Code) = TRIM(pd.Code) " \
        #       "LEFT JOIN Process AS pr ON TRIM(ma.Process) = TRIM(pr.Code) " \
        #       "WHERE (pa.Goodness > 0 AND (pa.WorkDate BETWEEN %s AND %s)) ORDER BY pa.WorkDate DESC "
        # sql = "Select pa.WorkDate, pa.ProductionActualNo, pa.CODE, ma.STEP9, pa.Goodness, pa.Badness, " \
        #       "pa.Mp, pa.Ap, pd.CODETwins, ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, " \
        #       "mc.LINECODE, gr.Language2, gr.Language3, pa.WorkFrom, pa.WorkTo, pd.StandardTime " \
        #       "From ProductionActual AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
        #       "INNER JOIN Process AS pr ON ma.Process = pr.CODE INNER JOIN t_Product AS pd ON ma.CODE = pd.CODE " \
        #       "INNER JOIN Groups AS gr ON pa.Groups = gr.CODE " \
        #       "INNER JOIN MACHINE AS mc ON mc.CODE = gr.PaCODE " \
        #       "WHERE pa.WorkDate BETWEEN %s AND %s AND pa.Goodness <> 0 ORDER BY pa.WorkDate DESC "
        sql = "Select pa.WORKDATE, pa.PRODUCTIONACTUALNO, pa.CODE, ma.STEP9, pa.GOODNESS, pa.BADNESS, " \
              "pa.MP, pa.AP, pd.CODETWINS, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, pa.MACHINE, pa.GROUPSS, " \
              "mc.LINECODE, mc.LANGUAGE2, mc.LANGUAGE3, pa.WORKFROM, pa.WORKTO, pd.STANDARDTIME, pd.STANDARDWORKER " \
              "From PRODUCTIONACTUAL AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE INNER JOIN T_PRODUCT AS pd ON ma.CODE = pd.CODE " \
              "INNER JOIN MACHINE AS mc ON pa.MACHINE = mc.CODE " \
              "WHERE pa.WORKDATE BETWEEN %s AND %s AND pa.GOODNESS <> 0 ORDER BY pa.WORKDATE DESC "
        print(get_line_no(), "sql: ", sql)
    else:
        # dfSets.columns = ['WORKDATE', 'productionactualno', 'CODE', 'STEP9', 'goodness', 'badness',
        #                   'volume', 'schedule', 'CODEtwins', 'process', 'process_kor', 'process_loc', 'MACHINE',
        #                   'groups',
        #                   'LINE_CODE', 'MACHINE_kor', 'MACHINE_loc', 'workfrom', 'workto', 'standardtime']
        # print(debugPath, ", processCode: ", processCode, "에 대한 자료만 필터합니다.")
        values = (fromDate, toDate, processCode)
        # 2021.03.01 Conclusion. WEB DB 웹 Database 또한 [MS SQL]로 최종 결정되었다.
        sql = "Select pa.WORKDATE, pa.PRODUCTIONACTUALNO, pa.CODE, ma.STEP9, pa.GOODNESS, pa.BADNESS, " \
              "pa.MP, pa.AP, pd.CODETWINS, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, pa.MACHINE, pa.GROUPSS, " \
              "mc.LINECODE, mc.LANGUAGE2, mc.LANGUAGE3, pa.WORKFROM, pa.WORKTO, pd.STANDARDTIME, pd.STANDARDWORKER " \
              "From PRODUCTIONACTUAL AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE INNER JOIN T_PRODUCT AS pd ON ma.CODE = pd.CODE " \
              "INNER JOIN MACHINE AS mc ON pa.MACHINE = mc.CODE " \
              "WHERE pa.WORKDATE BETWEEN %s AND %s AND ma.PROCESS = %s AND pa.GOODNESS <> 0 ORDER BY pa.WORKDATE DESC "

        # sql = "Select pa.WORKDATE, pa.ProductionActualNo, pa.CODE, ma.STEP9, pa.Goodness, pa.Badness, " \
        #       "pa.Mp, pa.Ap, pd.CODETwins, ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, " \
        #       "gr.CODE, gr.Language2, gr.Language3, pa.WorkFrom, pa.WorkTo, pd.StandardTime " \
        #       "From ProductionActual AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
        #       "INNER JOIN Process AS pr ON ma.Process = pr.CODE INNER JOIN t_Product AS pd ON ma.CODE = pd.CODE " \
        #       "INNER JOIN Groups AS gr ON pa.Groups = gr.CODE " \
        #       "WHERE pa.WORKDATE BETWEEN %s AND %s AND ma.Process = %s AND pa.Goodness <> 0 ORDER BY pa.WORKDATE DESC "
        # sql = "Select pa.WORKDATE, pa.ProductionActualNo, pa.CODE, ma.STEP9, pa.Goodness, pa.Badness, " \
        #       "pa.Mp, pa.Ap, pd.CODETwins, ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, " \
        #       "mc.LINECODE, gr.Language2, gr.Language3, pa.WorkFrom, pa.WorkTo, pd.StandardTime " \
        #       "From ProductionActual AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
        #       "INNER JOIN Process AS pr ON ma.Process = pr.CODE INNER JOIN t_Product AS pd ON ma.CODE = pd.CODE " \
        #       "INNER JOIN Groups AS gr ON pa.Groups = gr.CODE " \
        #       "INNER JOIN MACHINE AS mc ON mc.CODE = gr.PaCODE " \
        #       "WHERE pa.WORKDATE BETWEEN %s AND %s AND ma.Process = %s AND pa.Goodness <> 0 ORDER BY pa.WORKDATE DESC "

        # sql = "Select pa.WORKDATE, pa.ProductionActualNo, pa.CODE, ma.STEP9, pa.Goodness, pa.Badness, pa.Mp, pa.Ap, pd.CODETwins, " \
        #       "ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, pa.WorkFrom, pa.WorkTo, pd.StandardTime "\
        #       "From ProductionActual AS pa LEFT JOIN GOODSMASTER AS ma ON TRIM(pa.CODE) = TRIM(ma.CODE) " \
        #       "LEFT JOIN t_Product AS pd ON TRIM(ma.CODE) = TRIM(pd.CODE) " \
        #       "LEFT JOIN Process AS pr ON TRIM(ma.Process) = TRIM(pr.CODE) " \
        #       "WHERE (pa.Goodness > 0 AND (pa.WORKDATE BETWEEN %s AND %s) AND LEFT(ma.Process,4) = %s) ORDER BY pa.WORKDATE DESC "
        # sql = "Select pa.WORKDATE, pa.ProductionActualNo, pa.CODE, ma.STEP9, pa.Goodness, pa.Badness, " \
        #       "pa.Mp, pa.Ap, pd.CODETwins, ma.Process, pr.Language2, pr.Language3, pa.MACHINE, pa.Groups, " \
        #       "mc.LINECODE, mc.Language2, mc.Language3, pa.WorkFrom, pa.WorkTo, pd.StandardTime " \
        #       "From ProductionActual AS pa INNER JOIN GOODSMASTER AS ma ON pa.CODE = ma.CODE " \
        #       "INNER JOIN Process AS pr ON ma.Process = pr.CODE INNER JOIN t_Product AS pd ON ma.CODE = pd.CODE " \
        #       "INNER JOIN Groups AS gr ON pa.Groups = gr.CODE " \
        #       "INNER JOIN MACHINE AS mc ON pa.MACHINE = mc.CODE " \
        #       "WHERE pa.WORKDATE BETWEEN %s AND %s AND ma.Process = %s AND pa.Goodness <> 0 ORDER BY pa.WORKDATE DESC "

    try:
        # print(debugPath, ", 디버깅... 1")
        # print("===========================================================================================")
        # print("sql: \n", sql)
        # print("values: ", values)
        # print(debugPath, ", views.cursArrayWeb() 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...", values)
        # print("===========================================================================================")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # print(debugPath, ", 디버깅... 2")
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dbMrp.pr Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dbMrp.py Database 연결을 확인하시오!")
            # print(debugPath, ", mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))
            # print(debugPath, ", cursArray: ", cursArrayWeb, "type(cursArrayWeb):", type(cursArrayWeb))
            # print(debugPath, ", cursDict: ", cursDict, "type(cursDict):", type(cursDict))
            # print(debugPath, ", HOST3: ", HOST3, "type(HOST3):", type(HOST3))
            # print(debugPath, ", USER3: ", USER3, "type(USER3):", type(USER3))
            # print(debugPath, ", DBNAME3: ", DBNAME3, "type(DBNAME3):", type(DBNAME3))

        # print("sql: \n", sql)
        # print(debugPath, ", values: ", values)
        if values == '':
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        else:
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)

    try:
        CONNECTEDWEB = True
        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("sqlQuerySets: ", sqlQuerySets)
        # print("type(sqlQuerySets): ", type(sqlQuerySets))  # <class 'list'>
        # print(get_line_no(), ", len(sqlQuerySets): ", len(sqlQuerySets))

        # for i, data in enumerate(sqlQuerySets):
        #     if i == 11314:
        #         print("i: ", i, ", data: ", data)

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print(debugPath, ", dfSets: \n", dfSets)
        # print(debugPath, ", type(dfSets): ", type(dfSets))
        print(get_line_no(), ", __dbMrp len(dfSets): ", len(dfSets))

        # 2021.02.06 Added. 빈 dfSets 확인.
        if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
            print(get_line_no(), f", __dbMrp 조건에 맞는 자료가 없습니다. 먼저 BOM 등록을 확인하고, 다시 진행하시오!")
            # print(get_line_no(), f", __dbMrp 조건에 맞는 자료가 없습니다. 먼저 현 제품({})에 대한 BOM 등록을 확인하고, 다시 진행하시오!")
        else:
            # 2021.02.21 Conclusion. ProductionActual.Mp 컬럼인 생산 능력 수량 ['volumn'] 값은, DataFrame에서 추가한다.
            # 아니다... 여기서 가져오고, [DataFrame]에서는 그 값을 정리만 한다.
            dfSets.columns = ['WORKDATE', 'PRODUCTIONACTUALNO', 'CODE', 'STEP9', 'GOODNESS', 'BADNESS',
                              'VOLUME', 'SCHEDULE', 'CODETWINS', 'PROCESS', 'PROCESS_KOR', 'PROCESS_LOC', 'MACHINE',
                              'GROUPSS', 'LINE_CODE', 'MACHINE_KOR', 'MACHINE_LOC', 'WORKFROM', 'WORKTO','STANDARDTIME',
                              'STANDARDWORKER']
            # dfSets.columns = ['WORKDATE', 'productionactualno', 'CODE', 'STEP9', 'goodness', 'badness', 'schedule',
            #               'process', 'process_kor', 'process_loc', 'MACHINE', 'groups', 'workfrom', 'workto', 'standardtime']
            # print("컬럼명 변경 후 dfSets: \n", dfSets)

            # 2021.01.31 Added. WORKDATE.작업일자 컬럼은 TimeStamp.시간 정보는 전혀 필요가 없기에, [문자형 타입]으로 변환...
            dfSets['WORKDATE'] = dfSets['WORKDATE'].astype(str)
            # print(debugPath, ",::type(dfSets): ", type(dfSets))
            # print(debugPath, ",::len(dfSets): ", len(dfSets))
            # print(debugPath, ",::dfSets: \n", dfSets)

            # dfSets['CODEspec'] = dfSets['CODE'] + " " + dfSets['STEP9']
            # print(debugPath, ", CODEspec 추가 후 dfSets: \n", dfSets)

            if LANGUAGE_NO == 1042:
            # if LANGUAGE_NO == 'korean':
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_KOR']
            else:
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_LOC']
            # print(debugPath, ", processinfo 추가 후 dfSets: \n", dfSets)

            if LANGUAGE_NO == 1042:
            # if LANGUAGE_NO == 'korean':
                # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].astype(str) + " " + dfSets['MACHINE_kor']
                # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].map(lambda x: f'{x:0>2}') + " " + dfSets['MACHINE_kor']
                dfSets['MACHINEINFO'] = dfSets['LINE_CODE'].map('{:0>2}'.format) + " " + dfSets['MACHINE_KOR']
            else:
                # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].astype(str) + " " + dfSets['MACHINE_loc']
                # dfSets['MACHINEinfo'] = dfSets['LINE_CODE'].map(lambda x: f'{x:0>2}') + " " + dfSets['MACHINE_loc']
                dfSets['MACHINEINFO'] = dfSets['LINE_CODE'].map('{:0>2}'.format) + " " + dfSets['MACHINE_LOC']

            # if len(dfSets) > 0:
            #     if ProcessCode == 'all':
            #         processInfoCurrent = 'ALL'
            #     else:
            #         processInfoCurrent = dfSets.at[0, 'processinfo']
            # print(debugPath, ", processInfoCurrent 추가 후 processInfoCurrent: \n", processInfoCurrent)

    except:
        CONNECTEDWEB = False
        # # [dfSets = pd.DataFrame()] 이 문장을 실행하지 않더라도,
        # # 아래 [if dfSets is None and isinstance(dfSets, pd.DataFrame) and not dfSets.empty] 여기서 걸러진다.
        # # 그렇지만, 프로그램 오류 없이 걸러지기 위해, retrun 값 [dfSets] 변수는 정의해 준다.
        # dfSets = ""
        # dfSets = pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # dfSets = pd.DataFrame(index=range(0, 0), columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")
        # print("경고 dfSets: \n", dfSets)

    return sqlQuerySets, dfSets, NIGHT_CLOSING_HHMMSS


def __getProductionCapacity(fromDate, toDate, processCode, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    debugPath = "__dbMrp.py __getProductionCapacity()"

    # print(debugPath, ", type(fromDate): ", type(fromDate))
    # print(debugPath, ", fromDate: ", fromDate)
    # print(debugPath, ", toDate: ", toDate)
    # print(debugPath, ", ProcessCode: ", ProcessCode)
    # print(debugPath, ", timezone.now(): ", timezone.now())

    year = fromDate[:4]
    month = fromDate[5:7]
    # serial = "0001"  # 사업 계획 Revision은 필요 없고, 그냥 [달]을 4자리로 하여 처리...
    revision = year + "00" + month
    # print(debugPath, ", year: ", year)
    # print(debugPath, ", month: ", month)
    # print(debugPath, ", revision: ", revision)

    # 해당 월도의 마지막 날짜를 찾는다.
    maxDate = __getMaxDate(year, month)
    # print("__getProductionCapacity 55 maxDate: ", maxDate)

    # [ppp_current.생산 Capa 관리]는 반드시 1개월 단위로만 관리해야 하므로, 기간의 종료 날짜를 이번달 말일로 새로 넣어준다.
    # toDate = datetime.strptime(year + "-" + month + "-" + maxDate, "%Y-%m-%d")
    toDate = year + "-" + month + "-" + maxDate

    # 2021.03.20 Added. ***** Release No. 즉 ReflectStock 값은 항상 [1]번만 사용하게 한다. *****
    release = 1

    # // 2020.04.28 Added. [생관 번호]가 바뀌면, 당연히 그 생관 번호에 맞는 [최종 백업 번호]까지, [ddlb_33]에 뿌려 줘야 한다.
    # // 2020.04.09 Added. ii_BackupNo 얻기. 가장 마지막 백업 번호 얻기.
    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(" mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    # 2021.03.21 Conclusion. [CS ERP 생산 능력 분석 메뉴]에서 [사업 번호.Revision]에 대한 [릴리스 번호.BackupNo] 관리는,
    #           ===> [월도] 기준으로 관리한다. 절대 [공정별]로 관리하는 것이 아니라, [월도]별로 전체 공정이 모두 해당된다.
    #           ===> 즉, ForecastHistoryDay 자료에, [조립 공정]에 대한 자료는 BackupNo.ReflectStock 값이, [3]까지 있고,
    #           ===> [용접 공정]은 [1]까지 되어 있다 할 지라도,
    #           ===> 여기 [WEB ERP]에서 [용접 공정]의 [BackupNo]는 [3]을 가져와서,
    #           ===> ForecastHistoryDay.ReflectStock 값이 [3]인 [용접 공정]의 자료를 가져와야 한다. 그러면,
    #           ===> 그러면, 당연히 용접 공정 [3]에 대한 자료가 없을 것이다.
    #           ===> 그러면, CS ERP에서 용접 공정을 처리하게 되는데, [자동으로] 용접 공정이 [3]으로 세팅되면서 저장된다.
    #           ===> 왜냐하면, [조립 공정]의 BackupNo 값이 이미 [3]이 있기 때문이다.

    # 이렇게 [공정별]로 값을 찾으면 절대 안 된다.
    # values = (revision, ProcessCode)
    # sql = "Select Revision, Process, BackupNo From WorkBaseByGoods0 " \
    #       "Where Revision = %s And Process = %s Order By Revision Desc, Process Desc, BackupNo Desc "

    # 이렇게 [사업 번호별] 즉, [월도]로 값을 찾아야 한다.
    values = (revision)
    sql = "Select REVISION, PROCESS, BACKUPNO From WORKBASEBYGOODS0 " \
          "Where REVISION = %s Order By REVISION Desc, BACKUPNO Desc "
    try:
        cursArrayWeb.execute(sql, values)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
            else:
                CONNECTEDWEB = False
            cursArrayWeb.execute(sql, values)
    try:
        sqlQueryBackupNo = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        if len(sqlQueryBackupNo) == 0:
            print(get_line_no(), ", __dbMrp.py 저장된 백업 번호가 없어, [0]번을 사용합니다.")
            release = 0
        else:
            # print("0 origin _dbMrp.py __getProductionCapacity sqlQueryBackupNo: \n", sqlQueryBackupNo)
            # print("0 origin _dbMrp.py __getProductionCapacity type(sqlQueryBackupNo): ", type(sqlQueryBackupNo))
            # print("0 origin _dbMrp.py __getProductionCapacity len(sqlQueryBackupNo): ", len(sqlQueryBackupNo))
            for row in sqlQueryBackupNo:
                # print("sqlQueryBackupNo  row: ", row)
                release = int(row[2])
                break
        # print("Current Release Backup No.: ", release)
        # print("Current Release Backup No. type(release): ", type(release))
    except:
        release = 0

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(" mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    if str(processCode).lower() == 'all' or str(processCode) == '0000':
        # print("1 __getProductionCapacity() Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")

        # mc.Language2: 설비명 korea
        # mc.Language3: 설비명 local
        # fo.Duduction: 근무 일수: 해당 월 + 해당 공정
        # fo.Coefficient: Cycle Time (초)
        # fo.PoBal: 소요 일수
        # fo.Minimum: 소요 시간
        # fo.Tmp: UPH
        # fo.ClassMonth: 생산 라인 코드 3자리: String, (LINECODE.라인 번호는 중복이 있어 사용 불가)
        # ma.Good2: 구분: 용접이면, 1.로타리, 2.반자동, 3.고주파, 4.수동
        # fo.WorkBaseDay: UPD
        # fo.Stock: 월초 재고: 월말 재고 조사 수량을 차월초 재고로 등록...
        # fo.Dpt: 생산 계획 합
        # fo.Dst: 생산 계획 잔량 합
        # fo.Nmt: 달성률
        # fo.Nst: 현재 재고

        values = (revision, release)  # Release No. 즉 ReflectStock 값 사용.
        # values = (revision)  # Release No. 즉 ReflectStock 값 사용.
        sql = "Select fo.REVISION, fo.CODE, ma.STEP9, fo.DEDUCTION, fo.COEFFICIENT, fo.POBAL, fo.MINIMUM, fo.TMP, " \
              "ma.GOODS2, fo.WORKBASEDAY, fo.STOCK, fo.DPT, fo.DFT, fo.DMT, fo.DST, fo.NPT, fo.NFT, fo.NST, " \
              "fo.CLASSMONTH, mc.LANGUAGE2, mc.LANGUAGE3, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, fo.REFLECTSTOCK " \
              "From FORECASTHISTORYDAY AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE  INNER JOIN MACHINE AS mc ON fo.CLASSMONTH = mc.CODE " \
              "WHERE fo.REVISION = %s AND fo.DPT <> 0 AND fo.REFLECTSTOCK = %s " \
              "ORDER BY fo.REVISION Desc, ma.PROCESS Desc, fo.CLASSMONTH, ma.STEP9 "
    else:
        values = (revision, processCode, release)  # Release No. 즉 ReflectStock 값 사용.
        # values = (revision, processCode)  # Release No. 즉 ReflectStock 값 사용.
        sql = "Select fo.REVISION, fo.CODE, ma.STEP9, fo.DEDUCTION, fo.COEFFICIENT, fo.POBAL, fo.MINIMUM, fo.TMP, " \
              "ma.GOODS2, fo.WORKBASEDAY, fo.STOCK, fo.DPT, fo.DFT, fo.DMT, fo.DST, fo.NPT, fo.NFT, fo.NST, " \
              "fo.CLASSMONTH, mc.LANGUAGE2, mc.LANGUAGE3, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, fo.REFLECTSTOCK " \
              "From FORECASTHISTORYDAY AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE  INNER JOIN MACHINE AS mc ON fo.CLASSMONTH = mc.CODE " \
              "WHERE fo.REVISION = %s AND ma.PROCESS = %s AND fo.DPT <> 0 AND fo.REFLECTSTOCK = %s " \
              "ORDER BY fo.REVISION Desc, ma.PROCESS Desc, fo.CLASSMONTH, ma.STEP9 "
    try:
        # print("===========================================================================================")
        # print("__getProductionCapacity views.cursArrayWeb() 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...", values)
        # print("===========================================================================================")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

        # print(debugPath, ", 디버깅... 1-1")
        if values == '':
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        else:
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # print(debugPath, ", 디버깅... 2-1")

    try:
        CONNECTEDWEB = True
        # print(debugPath, ", 디버깅... 3")
        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print("0 origin _dbMrp.py __getProductionCapacity sqlQuerySets: \n", sqlQuerySets)
        # print("0 origin _dbMrp.py __getProductionCapacity type(sqlQuerySets): ", type(sqlQuerySets))
        # print("0 origin _dbMrp.py __getProductionCapacity len(sqlQuerySets): ", len(sqlQuerySets))
        # print("0 origin _dbMrp.py __getProductionCapacity 디버깅... 6")

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print("origin _dbMrp.py __getProductionCapacity dfSets: \n", dfSets)
        # print("origin _dbMrp.py __getProductionCapacity type(dfSets): ", type(dfSets))
        # print("origin _dbMrp.py __getProductionCapacity len(dfSets): ", len(dfSets))
        # print("origin _dbMrp.py __getProductionCapacity 디버깅... 6")

        # 2021.02.06 Added. 빈 df 확인.
        if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
            print(get_line_no(), ", __dfMrp.py 조건에 맞는 자료가 없습니다. 다시 확인하시오!")
        else:
            # dfSets.columns = ['REVISION', 'CODE', 'STEP9', 'workingdays', 'ct', 'needsday', 'needshour', 'uph',
            #                   'division', 'upd', 'stockfirst', 'dpt', 'dft', 'dmt', 'dst', 'nptqty', 'nftqty', 'nstqty',
            #                   'MACHINE', 'MACHINE_kor', 'MACHINE_loc', 'process', 'process_kor', 'process_loc', 'release']
            dfSets.columns = ['REVISION', 'CODE', 'STEP9', 'WORKINGDAYS', 'CT', 'NEEDSDAY', 'NEEDSHOUR', 'UPH',
                              'DIVISION', 'UPD', 'STOCKFIRST', 'DPT', 'DFT', 'DMT', 'DST', 'NPTQTY', 'NFTQTY', 'NSTQTY',
                              'MACHINE', 'MACHINE_KOR', 'MACHINE_LOC', 'PROCESS', 'PROCESS_KOR', 'PROCESS_LOT', 'RELEASE']
            # print("컬럼명 변경 후 __getProductionCapacity dfSets: \n", dfSets)
            # print(debugPath, ", 디버깅... 7")

            if LANGUAGE_NO == 1042:
            # if LANGUAGE_NO == 'korean':
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_KOR']
            else:
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_LOT']
            # print("__getProductionCapacity processinfo 추가 후 dfSets: \n", dfSets)
            # print(debugPath, ", 디버깅... 8")

    except:
        CONNECTEDWEB = False
        # dfSets = pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # dfSets = pd.DataFrame(index=range(0, 0), columns=['INDEX', 'NUMBER'])
        print(get_line_no(), ", __dfMrp.py 경고, dfSets: \n", dfSets)
        print(get_line_no(), ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlQuerySets, dfSets, revision, toDate


# 2021.04.29 Added. 수주 수량 대비 생산 능력 분석
def __getReceivingOrderCapacity(fromDate, toDate, processCode, data):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    LANGUAGE_NO = data['language']

    debugPath = "__dbMrp.py __getReceivingOrderCapacity()"

    year = fromDate[:4]
    month = fromDate[5:7]
    # serial = "0001"  # 사업 계획 Revision은 필요 없고, 그냥 [달]을 4자리로 하여 처리...
    revision = year + "00" + month
    # print(debugPath, ", year: ", year)
    # print(debugPath, ", month: ", month)
    # print(debugPath, ", revision: ", revision)
    # print(debugPath, ", ProcessCode: ", ProcessCode)

    # 해당 월도의 마지막 날짜를 찾는다.
    maxDate = __getMaxDate(year, month)
    # print(debugPath, ", 55 maxDate: ", maxDate)

    # [Capa 관리]는 반드시 1개월 단위로만 관리해야 하므로, 기간의 종료 날짜를 이번달 말일로 새로 넣어준다.
    # toDate = datetime.strptime(year + "-" + month + "-" + maxDate, "%Y-%m-%d")
    toDate = year + "-" + month + "-" + maxDate

    # 2021.03.20 Added. ***** Release No. 즉 ReflectStock 값은 항상 [1]번만 사용하게 한다. *****
    release = 1

    # // 2020.04.28 Added. [생관 번호]가 바뀌면, 당연히 그 생관 번호에 맞는 [최종 백업 번호]까지, [ddlb_33]에 뿌려 줘야 한다.
    # // 2020.04.09 Added. ii_BackupNo 얻기. 가장 마지막 백업 번호 얻기.
    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(" mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(debugPath, ", __dfMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(debugPath, ", __dfMrp.py Database 연결을 확인하시오!")

    # 2021.03.21 Conclusion. [CS ERP 생산 능력 분석 메뉴]에서 [사업 번호.Revision]에 대한 [릴리스 번호.BackupNo] 관리는,
    #           ===> [월도] 기준으로 관리한다. 절대 [공정별]로 관리하는 것이 아니라, [월도]별로 전체 공정이 모두 해당된다.
    #           ===> 즉, ForecastHistoryDay 자료에, [조립 공정]에 대한 자료는 BackupNo.ReflectStock 값이, [3]까지 있고,
    #           ===> [용접 공정]은 [1]까지 되어 있다 할 지라도,
    #           ===> 여기 [WEB ERP]에서 [용접 공정]의 [BackupNo]는 [3]을 가져와서,
    #           ===> ForecastHistoryDay.ReflectStock 값이 [3]인 [용접 공정]의 자료를 가져와야 한다. 그러면,
    #           ===> 그러면, 당연히 용접 공정 [3]에 대한 자료가 없을 것이다.
    #           ===> 그러면, CS ERP에서 용접 공정을 처리하게 되는데, [자동으로] 용접 공정이 [3]으로 세팅되면서 저장된다.
    #           ===> 왜냐하면, [조립 공정]의 BackupNo 값이 이미 [3]이 있기 때문이다.

    # 이렇게 [공정별]로 값을 찾으면 절대 안 된다.
    # values = (revision, ProcessCode)
    # sql = "Select Revision, Process, BackupNo From WorkBaseByGoods0 " \
    #       "Where Revision = %s And Process = %s Order By Revision Desc, Process Desc, BackupNo Desc "

    # 이렇게 [사업 번호별] 즉, [월도]로 값을 찾아야 한다.
    values = (revision)
    sql = "Select REVISION, PROCESS, BACKUPNO From WORKBASEBYGOODS0 " \
          "Where REVISION = %s Order By REVISION Desc, BACKUPNO Desc "
    try:
        cursArrayWeb.execute(sql, values)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
            else:
                CONNECTEDWEB = False
            cursArrayWeb.execute(sql, values)
    try:
        sqlQueryBackupNo = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        if len(sqlQueryBackupNo) == 0:
            print(debugPath, ", __dfMrp.py 저장된 백업 번호가 없어, [0]번을 사용합니다.")
            release = 0
        else:
            # print("debugPath, ", sqlQueryBackupNo: \n", sqlQueryBackupNo)
            # print("debugPath, ", type(sqlQueryBackupNo): ", type(sqlQueryBackupNo))
            # print("debugPath, ", len(sqlQueryBackupNo): ", len(sqlQueryBackupNo))
            for row in sqlQueryBackupNo:
                # print("sqlQueryBackupNo  row: ", row)
                release = int(row[2])
                break
        # print(debugPath, ", Current Release Backup No.: ", release)
        # print(debugPath, ", Current Release Backup No. type(release): ", type(release))
    except:
        release = 0

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print(" mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

    if str(processCode).lower() == 'all' or str(processCode) == '0000':
        # print("1 __getProductionCapacity() Database 선택한 공정 코드가 없습니다. 전체 공정 자료를 뿌려줍니다.")

        # mc.Language2: 설비명 korea
        # mc.Language3: 설비명 local
        # fo.Duduction: 근무 일수: 해당 월 + 해당 공정
        # fo.Coefficient: Cycle Time (초)
        # fo.PoBal: 소요 일수
        # fo.Minimum: 소요 시간
        # fo.Tmp: UPH
        # fo.ClassMonth: 생산 라인 코드 3자리: String, (LINECODE.라인 번호는 중복이 있어 사용 불가)
        # ma.Good2: 구분: 용접이면, 1.로타리, 2.반자동, 3.고주파, 4.수동
        # fo.WorkBaseDay: UPD
        # fo.Stock: 월초 재고: 월말 재고 조사 수량을 차월초 재고로 등록...
        # fo.Dpt: 생산 계획 합
        # fo.Dst: 생산 계획 잔량 합
        # fo.Nmt: 달성률
        # fo.Nst: 현재 재고

        values = (revision, release)  # Release No. 즉 ReflectStock 값 사용.
        # values = (revision)  # Release No. 즉 ReflectStock 값 사용.
        sql = "Select fo.REVISION, fo.CODE, ma.STEP9, fo.DEDUCTION, fo.COEFFICIENT, fo.POBAL, fo.MINIMUM, fo.TMP, " \
              "ma.GOODS2, fo.WORKBASEDAY, fo.STOCK, fo.DPT, fo.DFT, fo.DMT, fo.DST, fo.NPT, fo.NFT, fo.NST, " \
              "fo.CLASSMONTH, mc.LANGUAGE2, mc.LANGUAGE3, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, fo.REFLECTSTOCK " \
              "From MASTERPLANHISTORYDAY AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE  INNER JOIN MACHINE AS mc ON fo.ClassMonth = mc.CODE " \
              "WHERE fo.REVISION = %s AND fo.DFT <> 0 AND fo.REFLECTSTOCK = %s " \
              "ORDER BY fo.REVISION Desc, ma.PROCESS Desc, fo.CLASSMONTH, ma.STEP9 "
    else:
        # print(debugPath, ", revision: ", revision)
        # print(debugPath, ", ProcessCode: ", ProcessCode)
        # print(debugPath, ", release: ", release)
        values = (revision, processCode, release)  # Release No. 즉 ReflectStock 값 사용.
        # values = (revision, processCode)  # Release No. 즉 ReflectStock 값 사용.
        sql = "Select fo.REVISION, fo.CODE, ma.STEP9, fo.DEDUCTION, fo.COEFFICIENT, fo.POBAL, fo.MINIMUM, fo.TMP, " \
              "ma.GOODS2, fo.WORKBASEDAY, fo.STOCK, fo.DPT, fo.DFT, fo.DMT, fo.DST, fo.NPT, fo.NFT, fo.NST, " \
              "fo.CLASSMONTH, mc.LANGUAGE2, mc.LANGUAGE3, ma.PROCESS, pr.LANGUAGE2, pr.LANGUAGE3, fo.REFLECTSTOCK " \
              "From MASTERPLANHISTORYDAY AS fo INNER JOIN GOODSMASTER AS ma ON fo.CODE = ma.CODE " \
              "INNER JOIN PROCESS AS pr ON ma.PROCESS = pr.CODE INNER JOIN MACHINE AS mc ON fo.ClassMoCLASSMONTHnth = mc.CODE " \
              "WHERE fo.REVISION = %s AND ma.PROCESS = %s AND fo.DFT <> 0 AND fo.REFLECTSTOCK = %s " \
              "ORDER BY fo.REVISION Desc, ma.PROCESS Desc, fo.CLASSMONTH, ma.STEP9 "
    try:
        # print("===========================================================================================")
        # print(debugPath, ", 접속을 시도합니다. 시간이 오래 걸릴수도 있습니다 잠시만 기다려 주세요...", values)
        # print("===========================================================================================")
        cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", __dfMrp.py Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", __dfMrp.py Database 연결을 확인하시오!")

        # print(debugPath, ", 디버깅... 1-1")
        if values == '':
            cursArrayWeb.execute(sql)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        else:
            cursArrayWeb.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql, from_date, to_date)
        # print(debugPath, ", 디버깅... 2-1")

    try:
        CONNECTEDWEB = True
        # print(debugPath, ", 디버깅... 3")
        sqlQuerySets = cursArrayWeb.fetchall()  # Dictionary based cursor, 선택한 "로우"가 1개 이상일 때.
        # print(debugPath, ", sqlQuerySets: \n", sqlQuerySets)
        # print(debugPath, ", type(sqlQuerySets): ", type(sqlQuerySets))
        # print(debugPath, ", len(sqlQuerySets): ", len(sqlQuerySets))
        # print(debugPath, ", 디버깅... 6")

        dfSets = pd.DataFrame(sqlQuerySets)  # <class 'pandas.core.frame.DataFrame'>
        # print(debugPath, ", dfSets: \n", dfSets)
        # print(debugPath, ", type(dfSets): ", type(dfSets))
        # print(debugPath, ", len(dfSets): ", len(dfSets))
        # print(debugPath, ", 디버깅... 6")

        # 2021.02.06 Added. 빈 df 확인.
        if len(dfSets) == 0:  # len(dfSets.index) == 0: 또는 dfSets.shape[0] == 0: 같은 구문이다.
            print(debugPath, ", __dfMrp.py 조건에 맞는 자료가 없습니다. 다시 확인하시오!")
        else:
            dfSets.columns = ['REVISION', 'CODE', 'STEP9', 'WORKINGDAYS', 'CT', 'NEEDSDAY', 'NEEDSHOUR', 'UPH',
                              'DIVISION', 'UPD', 'STOCKFIRST', 'DPT', 'DFT', 'DMT', 'DST', 'NPTQTY', 'NFTQTY', 'NSTQTY',
                              'MACHINE', 'MACHINE_KOR', 'MACHINE_LOC', 'PROCESS', 'PROCESS_KOR', 'PROCESS_LOC', 'RELEASE']
            # print("컬럼명 변경 후 __getProductionCapacity dfSets: \n", dfSets)
            # print(debugPath, ", 디버깅... 7")

            if LANGUAGE_NO == 1042:
            # if LANGUAGE_NO == 'korean':
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_KOR']
            else:
                dfSets['PROCESSINFO'] = dfSets['PROCESS'] + " " + dfSets['PROCESS_LOC']
            # print(debugPath, ", PROCESSinfo 추가 후 dfSets: \n", dfSets)
            # print(debugPath, ", 디버깅... 8")

    except:
        CONNECTEDWEB = False
        # dfSets = pd.DataFrame(np.nan, index=[0, 1, 2, 3], columns=['A'])
        dfSets = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        # dfSets = pd.DataFrame(index=range(0, 0), columns=['INDEX', 'NUMBER'])
        print(debugPath, ", __dfMrp.py 경고, dfSets: \n", dfSets)
        print(debugPath, ", __dfMrp.py 경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return sqlQuerySets, dfSets, revision, toDate


# 2022.04.27 Added. 북경 조이 작업 일지 업로드 처리에서, "ProductionActual.생산 실적"을 자동 등록 처리할 때,
# "t_Material.Required.소요량" 값을 가져 와서, "ProductionActual.RequiredStandard" 컬럼에 넣어 준다. 의미가 있는지는 모르겠다.
def __getRequired(code):
    global mySqlWebDb, cursArrayWeb, CONNECTEDWEB, NIGHT_CLOSING_HHMMSS, HOST3, DBNAME3

    m_code = ""
    required = 0
    tolerance = 0

    if CONNECTEDWEB == False:
        mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
        # print("__getRequired mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(mySqlWebDb) is pymysql.connections.Connection or type(
                cursArrayWeb) is pymysql.cursors.Cursor:
            CONNECTEDWEB = True
            print(get_line_no(), ", Database 연결 성공!")
        else:
            CONNECTEDWEB = False
            print(get_line_no(), ", Database 연결을 확인하시오!")

    sql ="Select M_CODE, REQUIRED, TOLERANCE From T_MATERIAL Where P_CODE = %s Order By P_CODE "

    try:
        cursArrayWeb.execute(sql, code)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDWEB == False:
            mySqlWebDb, cursArrayWeb, COMPANY_CODE, HOST3, USER3, PASS3, DBNAME3, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectWebMyDB()
            if type(mySqlWebDb) is pymysql.connections.Connection or type(
                    cursArrayWeb) is pymysql.cursors.Cursor:
                CONNECTEDWEB = True
                print(get_line_no(), ", Database 연결 성공!")
            else:
                CONNECTEDWEB = False
                print(get_line_no(), ", Database 연결을 확인하시오!")
            cursArrayWeb.execute(sql, code)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = cursArrayWeb.fetchall()
        row_count_server = len(array_sets_server)
        # print(get_line_no(), "T_MATERIAL len(array_sets_server) : ", row_count_server)
        if array_sets_server is None or row_count_server < 1:
            m_code = ""
            required = 0
            tolerance = 0
            print(get_line_no(), f"현재 제품({code})에 대한 BOM 자식 구성 정보가 없습니다. 관리자에게 문의하시오!")
        else:
            dfRequired = pd.DataFrame(array_sets_server)
            dfRequired.columns = ['M_CODE', 'REQUIRED', 'TOLERANCE']
            # print(get_line_no(), ", __dbMrp dfRequired: \n", dfRequired)
            m_code = dfRequired[1, 'M_CODE']
            required = dfRequired[1, 'REQUIRED']
            tolerance = dfRequired[1, 'TOLERANCE']
    except:
        m_code = ""
        required = 0
        tolerance = 0
        print(get_line_no(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return m_code, required, tolerance


# 2022.04.27 Added. 작업 지시 번호 제작.
def __makingProducingOrderNo(workdate, COMPANY_CODE, lineCode, dayNight, code):
    day_2s = str(workdate.day).zfill(2)
    month_2s = str(workdate.month).zfill(2)
    year_2s = str(workdate.year)[-2:].zfill(2)
    # print(get_line_no(), ", __dbMrp day_2s:", day_2s, ", month_2s: ", month_2s, ", year_2s: ", year_2s)

    producing_order_no = year_2s + month_2s + day_2s + COMPANY_CODE[:6] + str(lineCode).zfill(2) + dayNight + code
    # print(get_line_no(), ", __dbMrp producing_order_no: ", producing_order_no)

    return producing_order_no

# def goodsmasters(request):
#     global process_code_selected
#     goodsmasters = GoodsMaster.objects.all()
#
#     print("goodsmasters process_code: ", processCode)
#     # if process_code_selected is None or len(process_code_selected) == 0:  # 이것도 에러...
#     if "process_code_selected" not in globals():  # 로컬 변수일 경우에는, [not in locals()]
#         process_code_selected = processCode
#         print("goodsmasters process_code_selected: ", process_code_selected)
#
#     goodsmasters = GoodsMaster.objects.all().filter(process=process_code_selected)
#
#     # return HttpResponse('Products page')  # [127.0.0.1:8000/about]으로 연결 시, 바로 뿌려준다. ===> 아래 : path('about/', contact),
#     # return render(request, 'accounts/products.html')
#     return render(request, 'ppp/goodsmasters.html', {'goodsmasters': goodsmasters})
#
#
# def customers(request):
#     # return HttpResponse('Customer page')  # [127.0.0.1:8000/about]으로 연결 시, 바로 뿌려준다. ===> 아래 : path('about/', contact),
#     return render(request, 'ppp/customer.html')
#
#
# # ***** 엄청 중요 ***** # 원래 위와 같은 [class]에서, 사용자가 customer.html 뿌려진 화면에서, 특정 customer를 클릭했을 때, 특정한 customer만 화면에 뿌려주는 방법...
# def customer(request, pk):
#     customer = Customer.objects.get(id=pk)  # urls.py : path('customer/<str:pk>/', views.customer), 이쪽과 연동...
#
#     # ***** 여기서 또한 엄청 중요한 것은, ***** : customer.html 화면의 아래 부분에, Order 정보를 뿌려 주는 화면이 있으므로,
#     # customer를 클릭하면, 해당 customer가 주문한 order 정보를 같이 가져다가, Order 정보 부분에 뿌려줘야 한다.
#     orders = customer.order_set.all()
#     # 또한, 같은 화면 customer.html에서, Total Orders 수량을 찍어줘야 하므로,
#     order_count = 1  #orders.count()
#
#     context = {'customer': customer, 'orders': orders, 'order_count': order_count}
#
#     # return HttpResponse('Customer page')  # [127.0.0.1:8000/about]으로 연결 시, 바로 뿌려준다. ===> 아래 : path('about/', contact),
#     # return render(request, 'accounts/customer.html')
#     return render(request, 'ppp/customer.html', context)



# 2021.03.23 SQL 사용 예제

# rowcount : Rows affected by Query
# plus2net.com offers FREE online classes on Basics of Python for selected few visitors.
# Read more on course content , Details about the Program.
# We can get number of rows affected by the query by using rowcount. We will use one SELECT query here. ( What is a SELECT query ? )
# We defined my_cursor as connection object.
# Here is the code to create connection object
# import mysql.connector
#
# my_connect = mysql.connector.connect(
#   host="localhost",
#   user="userid",
#   passwd="password",
#   database="database_name"
# )
# ####### end of connection ####

# my_cursor = my_connect.cursor()
# Using my_cusor we will manage our database.
# my_cursor = my_connect.cursor(buffered=True) # my_connect is the connection
# my_cursor.execute("SELECT * FROM  student Where class='Five'")
# print("Rows returned = ",my_cursor.rowcount)
# Output is here
# Rows returned =  11

# buffered=True
# We have used my_cursor as buffered cursor.
# my_cursor = my_connect.cursor(buffered=True)
# This type cursor fetches rows and buffers them after getting output from MySQL database. We can use such cursor as iterator. There is no point in using buffered cursor for single fetching of rows.
#
# If we don’t use buffered cursor then we will get -1 as output from rowcount
# my_cursor = my_connect.cursor(buffered=False) # my_connect is the connection
# my_cursor.execute("SELECT * FROM  student Where class='Five'")
# print("Rows returned = ",my_cursor.rowcount)
# Output
# Rows returned =  -1

# Here is an update query to change the records. ( What is an UPDATE query ?)
# my_cursor = my_connect.cursor() #
# my_cursor.execute("UPDATE student SET class='Five' Where class='Four'")
# my_connect.commit()
# print("Rows updated = ",my_cursor.rowcount)
# Output is here
# Rows updated = 9

# Let us use one DELETE query ( What is a DELETE Query ? )
# my_cursor = my_connect.cursor() # Cursor
# my_cursor.execute("DELETE FROM student Where class='Five'")
# print("Rows Deleted = ",my_cursor.rowcount)
# my_connect.commit()
# Output is here
# Rows Deleted = 11

# By using INSERT query ( What is an INSERT Query ? )
# my_cursor = my_connect.cursor() # Cursor
# my_cursor.execute("INSERT INTO  `my_tutorial`.`student` (`id` ,`name` ,`class` ,`mark` ,`sex`) \
#                   VALUES ('36',  'King',  'Five',  '45',  'male')")
# print("Rows Added  = ",my_cursor.rowcount)
# my_connect.commit()
# Output is here
# Rows Added  = 1


# @csrf_exempt
# def sudoku(request):
#     context = {}
#     return render(request, 'ppp/index_sudoku.html', context)


# 출처: https://cholol.tistory.com/454 [IT, I Think ]
# ▷ 일별, 월별 데이터 뽑기
# 이제 로그데이터를 바탕으로 통계 페이지를 만들 예정입니다. 가장 간단하게 일별 통계를 먼저 만들껀데...
# dJango에서 쿼리 셋으로 날짜별 count를 출력할 수 있을지 모르겠네요. 일단 구글링 꼬~
# 구글링 결과 annotate를 사용해서 group by 효과를 볼 수 있는 쿼리 셋을 만들 수 있다고 합니다. 대략적으로 아래와 같이 만들면...

# # adminpage/views.py
# from django.db.models.functions import TruncMonth, TruncDate
#
#
# # def statisticslogs(request):
# #     stat_type = request.GET.get('stat_type')
# #     if stat_type == 'M':
# #         stats = Log.objects \
# #             .annotate(stat_date=TruncMonth('log_date')) \
# #             .values('stat_date') \
# #             .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
# #         else:
# #             stats = Log.objects \
# #                 .annotate(stat_date=TruncDate('log_date')) \
# #                 .values('stat_date') \
# #                 .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
# #
# #     context = {'stats': stats}
# #     return render(request, 'adminpage/statistics_logs.html', context)
#
# # 위에서는 [datetimepicker]이고, 아래는 [datepicker] 임에 유의...
#
#
# def statisticslogs(request):
#     stat_type = request.GET.get('stat_type')
#     stat_gbn = request.GET.get('optionRadios')
#     to_date = request.GET.get('to_date')
#     from_date = request.GET.get('from_date')
#     if stat_type == 'M':
#         if stat_gbn == 'period':
#             stats = Log.objects \
#                 .filter(log_date__range=[from_date, to_date]) \
#                 .annotate(stat_date=TruncMonth('log_date')) \
#                 .values('stat_date') \
#                 .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
#         else:
#             stats = Log.objects \
#                 .annotate(stat_date=TruncMonth('log_date')) \
#                 .values('stat_date') \
#                 .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
#     else:
#         if stat_gbn == 'period':
#             stats = Log.objects \
#                 .filter(log_date__range=[from_date, to_date])\
#                 .annotate(stat_date=TruncDate('log_date')) \
#                 .values('stat_date') \
#                 .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
#         else:
#             stats = Log.objects \
#                 .annotate(stat_date=TruncDate('log_date')) \
#                 .values('stat_date') \
#                 .annotate(stat_count=Count('log_userid')).values('stat_date', 'stat_count')
#         context = {'stats': stats, 'stat_type': stat_type, 'optionRadios': stat_gbn, 'to_date': to_date, 'from_date': from_date}
#         return render(request, 'adminpage/statistics_logs.html', context)
#
#
# class ListSubjects(ListView):
#     template_name = 'home_teacher.html'
#     model = Student
#
#     def get(self, request, *args, **kwargs):
#         name = request.GET['name']
#         student_subjects = Student.objects.get(name=name)
#         subjects = student_subjects.subject_student.all()
#         data = serializers.serialize('json', subjects, fields=('name', 'number_credits'))
#         return HttpResponse(data, content_type='application/json')

