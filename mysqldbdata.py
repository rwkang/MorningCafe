# 2021.05.08 Created. 시스템 옵티마이징, MRP.물적 자원 관리 관련 DB.데이터베이스 테이블 핸들링 함수 모음
#####################################################################################################################
# 2021.05.06 Conclusion. 모든 테이블의 자료를 불러오는 것을, "테이블 단위"로 함수를 만들어 사용한다.
#####################################################################################################################
import time

# import datetime as dt  # todo: 엄청 중요 ***** 위의 from datetime import datetime 모듈과 구분하기 위해, 반드시 "dt"로 사용.

from mysqldb import *
import pandas as pd

# todo: main.py 파일을 제외한 나머지 파일에서는, 가능하면, 글로벌(대문자) 변수를, [파라미터]로 전달하여 사용하도록 한다. 메모리 문제 등.

# MorningCafeIdeaScene 테이블에서, 오늘 날짜의 데이터 가져오기.
# todo: directory : 20250217, code_idea: 20250217i, title: 아래, content: 아래,
#  code_scene: 20250217ij, scene: 아래, scenario: 아래,
#  image_name: 20250217ij0.png, video_name: 20250217ij0.mp4, music_name: 20250217ij0.
def __getTodayData(CONNECTEDLOCAL, param, code_idea, code_scene):

    if not CONNECTEDLOCAL: # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    # print(get_info(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)
    print(get_info(), "CURSDICTLOCAL: ", CURSDICTLOCAL)
    print(get_info(), "STR_YMD: ", STR_YMD)

    # 0. param 자료 확인. [Order By ASC] 임에 주의.
    if param == "DIRECTORY":
        sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, " \
              "IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
              "From MORNING_CAFE_SCENE Where DIRECTORY = %s Order By CODE_SCENE ASC "
        values = (STR_YMD,)  # todo: 튜플로 만들어야 함
    elif param == "IDEA":
        sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, " \
              "IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
              "From MORNING_CAFE_SCENE Where CODE_IDEA = %s Order By CODE_SCENE ASC "
        values = (code_idea,)  # todo: 튜플로 만들어야 함
    elif param == "SCENE":
        sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, " \
              "IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
              "From MORNING_CAFE_SCENE Where CODE_SCENE = %s Order By CODE_SCENE ASC "
        values = (code_scene,)  # todo: 튜플로 만들어야 함

    try:
        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or \
                    type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                # print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")

        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)

    try:
        array_sets_server = CURSARRAYLOCAL.fetchall()
        row_count_server = len(array_sets_server)
        print(get_info(), "row_count_server: ", row_count_server)
        if array_sets_server is None:
            print(get_info(), "array_sets_server is None")

        if row_count_server < 1:
            print(get_info(), "row_count_server: ", row_count_server)

        if array_sets_server is None or row_count_server < 1:
            rtn = -1
            dfScene = pd.DataFrame(columns=['INDEX', 'NUMBER'])
            # print(get_info(), "오늘 scene 정보가 없습니다. 관리자에게 문의하시오!")
            # os.system("pause")
        else:
            dfScene = pd.DataFrame(array_sets_server)
            dfScene.columns = ['DIRECTORY', 'CODE_IDEA', 'TITLE', 'CONTENT', 'CODE_SCENE',
                               'SCENE', 'SCENARIO', 'VIDEO_PROMPT', 'IMAGE_NAME', 'VIDEO_NAME', 'MUSIC_NAME']
            dfScene['CODE_SCENE'] = dfScene['CODE_SCENE'].astype(str)  # 반드시 String 타입으로 세팅해 주어야 한다.

            # dfTrade.set_index('TRADE', drop=False, inplace=True)  # drop 옵션은 반드시 False
            # 2021.05.17 Conclusion. 위와 같이 "set_index()" 처리를 하게 되면,
            # 바로 여기 문장을 실행할 때 에러가 발생한다.
            # jsonRecords = dfTrade.reset_index().to_json(orient='records')
            # 그러므로 이미 "sql" 문장에서 "ORDER BY"로 가져온 값이, 이미 "index"가 걸려 있으니까,
            # 여기서는 "set_index()" 하지 않도록 해야 한다.
            # 만약, 꼭 "set_index()"가 필요하면, 반드시 "inplace=False"로 처리해야 한다.
            dfScene.set_index('CODE_SCENE', drop=False, inplace=False)  # drop 옵션은 반드시 False

            # print(get_info(), "dfScene: \n", dfScene.head(500))
            # print(get_info(), "dfScene: \n", dfScene.tail(20))
            # print(get_info(), "dfScene: \n", dfScene)
            print(get_info(), "len(dfScene): ", len(dfScene))
        rs = True
    except:
        rs = False
        dfScene = pd.DataFrame(columns=['INDEX', 'NUMBER'])
        print(get_info(), "경고, [callMainData]에서 치명적 에러가 발생하였습니다. 관리자에게 문의하시오!")

    return rs, dfScene

# MorningCafeIdeaScene 테이블에, 오늘 날짜의 데이터 todo: [무조건] Insert 하기.
# todo: directory : 20250217, code_idea: 20250217i, title: 아래, content: 아래,
#  code_scene: 20250217ij, scene: 아래, scenario: 아래,
#  image_name: 20250217ij0.png, video_name: 20250217ij0.mp4, music_name: 20250217ij0.
def __insertCurrentRow1(CONNECTEDLOCAL, title, content, scene, scenario, video_prompt, code_idea_current, code_scene_current):

    user_id = "RWKANG"

    if not CONNECTEDLOCAL: # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    # print(get_info(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)
    print(get_info(), "CURSDICTLOCAL: ", CURSDICTLOCAL)
    print(get_info(), "STR_YMD: ", STR_YMD)
    print(get_info(), "code_idea_current: ", code_idea_current)
    print(get_info(), "code_scene_current: ", code_scene_current)

    # while True: # todo: code_scene_current 값이 기존 자료에 있는지 확인하는 것은, 반드시 _getTodataData()에서 처리하게 한다.
    # 0. code_scene 체크.
    sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, " \
          "IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
          "From MORNING_CAFE_SCENE Where CODE_IDEA = %s Order By CODE_SCENE ASC "
    values = (code_idea_current,)  # todo: 튜플로 만들어야 함

    rsSelect = False
    try:
        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or \
                    type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")
        try:
            CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        except pymysql.MySQLError as e:
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            print(get_info(), "Error: ", str(e))
        else:
            rsSelect = True
            print(get_info(), "Successfully Selected: ", values, ", 여기서는 단지 검색이 가능하였다는 의미 임.")


    # array_sets_server = cursArrayWeb.fetchone()
    # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
    # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
    array_sets_server = CURSARRAYLOCAL.fetchall()
    row_count_server = len(array_sets_server)
    print(get_info(), "array_sets_server: ", row_count_server)
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "array_sets_server.count(): ", row_count_server, ", values: ", values)

    # todo: 2025.02.17 Conclusion. 기존 자료 갯수가 5개가 아니면, 기존 자료 먼저 삭제 루틴은, 반드시 main()에서 처리해야 한다. .
    print(get_info(), "여기서는 무조건 1개 로우를 [Insert] 한다: ", row_count_server)

    # 2019.01.29 정리. ***** 중요 *****
    # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
    # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
    # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
    # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
    # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []

    # rsInsert = True
    # if rsSelect:  # 기존 자료 없으면,
    #     if row_count_server > 0:
    #         print(get_info(), "row_count_server : ", row_count_server)
    #         rsInsert = False

    # if array_sets_server is None:
    #     print(get_info(), "array_sets_server is None")
    # if row_count_server < 1:
    #     print(get_info(), "row_count_server : ", row_count_server)
    # if array_sets_server is None or row_count_server < 1:
    #     print(get_info(), "row_count_server: ", row_count_server)

    print(get_info(), "STR_YMD: ", STR_YMD)
    print(get_info(), "code_idea_current: ", code_idea_current)
    print(get_info(), "title: ", title)
    print(get_info(), "content: ", content)
    print(get_info(), "code_scene_current: ", code_scene_current)
    print(get_info(), "scene: ", scene)
    print(get_info(), "scenario: ", scenario)
    print(get_info(), "video_prompt: ", video_prompt)
    print(get_info(), "user_id: ", user_id)

    # os.system("pause")
    sql = "Insert Into MORNING_CAFE_SCENE " \
          "(DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, USER_ID) " \
          "Values (%s,%s,%s,%s,%s, %s,%s,%s,%s)"
    values = (STR_YMD, code_idea_current, title, content, code_scene_current, scene, scenario, video_prompt, user_id)
    rsInsert = False
    try:
        CURSARRAYLOCAL.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
    except pymysql.MySQLError as e:
        print(get_info(), "MySQL 오류: ", str(e))
    except Exception as e:
        print(get_info(), "일반 오류: ", str(e))
    else:
        rsInsert = True
        print(get_info(), "데이터 추가 성공: ", values)
    print(get_info(), "values: ", values)
    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    rsInsertCommit = False
    if not rsInsert:
        rsInsertCommit = False
    else:
        try:
            MYSQLLOCALDB.commit()
            print(get_info(), "CODE_SCENE: ", code_scene_current, " 서버 commit 성공!")
            rsInsertCommit = True
        except pymysql.MySQLError as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "Error: ", str(e))
        except KeyboardInterrupt as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "KeyboardInterrupt Error: ", str(e), " DB rollback...")
            print(get_info(), "CODE_SCENE: ", code_scene_current, " 서버 저장 실패!")

    return rsInsertCommit


def __delTodayData(CONNECTEDLOCAL, param, code_idea, code_scene):
    if not CONNECTEDLOCAL:  # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    # print(get_info(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)
    print(get_info(), "CURSDICTLOCAL: ", CURSDICTLOCAL)
    print(get_info(), "STR_YMD: ", STR_YMD)
    print(get_info(), "code_idea: ", code_idea)
    print(get_info(), "code_scene: ", code_scene)
    print(get_info(), "param: ", param)

    # 0. param 자료 확인.
    if param == "DIRECTORY":
        sql = "Delete From MORNING_CAFE_SCENE Where DIRECTORY = %s Order By CODE_SCENE ASC "
        values = (STR_YMD,)  # todo: 튜플로 만들어야 함
    elif param == "IDEA":
        sql = "Delete From MORNING_CAFE_SCENE Where CODE_IDEA = %s Order By CODE_SCENE ASC "
        values = (code_idea,)  # todo: 튜플로 만들어야 함
    elif param == "SCENE":
        sql = "Delete From MORNING_CAFE_SCENE Where CODE_IDEA = %s Order By CODE_SCENE ASC "
        values = (code_scene,)  # todo: 튜플로 만들어야 함

    try:
        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except pymysql.MySQLError as e:  # DB 연결을 한 번 더 시도...
        print(get_info(), "MySQL Error: ", str(e))
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
                BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or \
                    type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")

            rsDeleteTodayData = False
            try:
                CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
            except pymysql.MySQLError as e:
                print(get_info(), "MySQL Error: ", str(e))
            except Exception as e:
                print(get_info(), "Error: ", str(e))
            else:
                rsDeleteTodayData = True
                print(get_info(), "Successfully Deleted: ", values)

                #  todo: image, video, music 파일을 체크하여, 반드시 삭제 해야 한다. ===> 프롬프트 내용과 image 파일 정체성 일치.
                rsDeleteFile = __delFile(code_scene)
                if not rsDeleteFile:
                    rsDeleteTodayData = False
                    print(get_info(), "Image, Video, Musin 파일 삭제에 실패하였습니다. 파일 삭제 권한 등 다시 확인하시오!")

    except Exception as e:
        print(get_info(), "Error: ", str(e))
    else:
        rsDeleteTodayData = True
        print(get_info(), "Successfully Deleted: ", values)

        #  todo: image, video, music 파일을 체크하여, 반드시 삭제 해야 한다. ===> 프롬프트 내용과 image 파일 정체성 일치.
        rsDeleteFile = __delFile(code_scene)
        if not rsDeleteFile:
            rsDeleteTodayData = False
            print(get_info(), "Image, Video, Musin 파일 삭제에 실패하였습니다. 파일 삭제 권한 등 다시 확인하시오!")

    time.sleep(1)

    rsDeleteCommit = False
    if not rsDeleteTodayData:
        rsDeleteCommit = False
    else:
        try:
            MYSQLLOCALDB.commit()
            print(get_info(), "CODE_SCENE: ", code_scene, " 서버 commit 성공!")
            rsDeleteCommit = True
        except pymysql.MySQLError as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "Error: ", str(e))
        except KeyboardInterrupt as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "KeyboardInterrupt Error: ", str(e), " DB rollback...")
            print(get_info(), "CODE_SCENE: ", code_scene, " 서버 저장 실패!")

    time.sleep(1)
    return rsDeleteCommit



# MorningCafeIdeaScene 테이블에, 오늘 날짜의 데이터 세팅하기.
# todo: directory : 20250217, code_idea: 20250217i, title: 아래, content: 아래,
#  code_scene: 20250217ij, scene: 아래, scenario: 아래,
#  image_name: 20250217ij0.png, video_name: 20250217ij0.mp4, music_name: 20250217ij0.
# todo: 2025.02.17 Conclusion. 여기 __setTodayData() 로직은 나중에 다시 정밀 검토 해야 한다. select 후 insert, update, delete ...
def __setTodayData(CONNECTEDLOCAL, title, content, scene, scenario, code_idea_current, code_scene_current):

    user_id = "RWKANG"

    if not CONNECTEDLOCAL: # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
        BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    # print(get_info(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)
    print(get_info(), "CURSDICTLOCAL: ", CURSDICTLOCAL)
    print(get_info(), "STR_YMD: ", STR_YMD)
    print(get_info(), "code_idea_current: ", code_idea_current)
    print(get_info(), "code_scene_current: ", code_scene_current)

    # while True: # todo: code_scene_current 값이 기존 자료에 있는지 확인하는 것은, 반드시 _getTodataData()에서 처리하게 한다.
    # 0. code_scene 체크.
    sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
          "From MORNING_CAFE_SCENE Where CODE_IDEA = %s Order By CODE_SCENE ASC "
    values = (code_idea_current,)  # todo: 튜플로 만들어야 함

    try:
        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or \
                    type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")
        try:
            CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        except pymysql.MySQLError as e:
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            print(get_info(), "Error: ", str(e))
        else:
            print(get_info(), "Successfully Selected: ", values)

    # array_sets_server = cursArrayWeb.fetchone()
    # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
    # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
    array_sets_server = CURSARRAYLOCAL.fetchall()
    row_count_server = len(array_sets_server)
    print(get_info(), "array_sets_server: ", row_count_server)
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "array_sets_server.count(): ", row_count_server, ", values: ", values)

    # todo: 2025.02.17 Conclusion. 기존 자료 갯수가 5개가 아니면, 기존 자료 먼저 삭제 루틴은, 반드시 main()에서 처리해야 한다. .

    # 2019.01.29 정리. ***** 중요 *****
    # 이상하게도 서버로 실행한 "array_sets_server" 값은 해당 로우가 없으면,
    # "None"이 아니고 대괄호 "[]"로 받아 진다. 그러므로 "None"은 아니다는 결론이다.]
    # 그러므로 아래와 같이 반드시 2개 조건으로 처리해야 한다.
    # print("서버 자료 존재 여부 : array_sets_server: ", array_sets_server)  # 값이 없으면 : []
    # print("서버 자료 존재 여부 : type(array_sets_server) :", type(array_sets_server))  # 값이 없으면 : []
    rsInsert = False
    if array_sets_server is None:
        print(get_info(), "array_sets_server is None")
    if row_count_server < 1:
        print(get_info(), "row_count_server : ", row_count_server)
    if array_sets_server is None or row_count_server < 1:
        print(get_info(), "row_count_server: ", row_count_server)

        print(get_info(), "STR_YMD: ", STR_YMD)
        print(get_info(), "code_idea_current: ", code_idea_current)
        print(get_info(), "title: ", title)
        print(get_info(), "content: ", content)
        print(get_info(), "code_scene_current: ", code_scene_current)
        print(get_info(), "scene: ", scene)
        print(get_info(), "scenario: ", scenario)
        print(get_info(), "user_id: ", user_id)

        # os.system("pause")
        sql = "Insert Into MORNING_CAFE_SCENE " \
              "(DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, USER_ID) " \
              "Values (%s,%s,%s,%s,%s, %s,%s,%s)"

        values = (STR_YMD, code_idea_current, title, content, code_scene_current, scene, scenario, user_id)
        try:
            CURSARRAYLOCAL.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
        except pymysql.MySQLError as e:
            print(get_info(), "MySQL 오류: ", str(e))
        except Exception as e:
            print(get_info(), "일반 오류: ", str(e))
        else:
            rsInsert = True
            print(get_info(), "데이터 추가 성공: ", values)
        print(get_info(), "values: ", values)
        print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    # 2025.02.17 Conclusion. 아래 1개 로우만 [Update] 할 수는 없다. 1개부터 4개까지는 모두 지웠고, 5개이면, 아무 처리도 하지 않는다.
    # else:  # row_count_server > 0 : 이미 code_scene 있으면...
    #
    #     # 중간에 괄호가 있으면, 에러 발생한다. ???
    #     sql = "Update MORNING_CAFE_SCENE Set TITLE = %s, CONTENT = %s, SCENE = %s, SCENARIO = %s " \
    #           "Where code_scene = %s "
    #
    #     values = (title, content, scene, scenario, code_scene_current)
    #     try:
    #         CURSARRAYLOCAL.execute(sql, values)
    #     except pymysql.MySQLError as e:
    #         print(get_info(), "MySQL Error: ", str(e))
    #     except Exception as e:
    #         print(get_info(), "Error: ", str(e))
    #     else:
    #         print(get_info(), "Updated Complete: ", values)
    #         rs = True
    #     print(get_info(), "values: ", values)
    #     print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    if rsInsert:
        rsInsertCommit = False
        try:
            MYSQLLOCALDB.commit()
            print(get_info(), "CODE_SCENE: ", code_scene_current, " 서버 commit 성공!")
            rsInsertCommit = True
        except pymysql.MySQLError as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "Error: ", str(e))
        except KeyboardInterrupt as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "KeyboardInterrupt Error: ", str(e), " DB rollback...")
            print(get_info(), "CODE_SCENE: ", code_scene_current, " 서버 저장 실패!")

    return rsInsertCommit

# todo: 2025.02.20 Conclusion. wrtn에서 "Update" 구문 최적화.
def __updateData(CONNECTEDLOCAL, sql, values):

    if not CONNECTEDLOCAL:  # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    # 0. code_scene 체크.
    sql_select = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, " \
                 "CODE_SCENE, SCENE, SCENARIO, IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
                "From MORNING_CAFE_SCENE Where DIRECTORY = %s Order By CODE_SCENE ASC "
    # values = (code_scene,)  # todo: 튜플로 만들어야 함

    try:
        CURSARRAYLOCAL.execute(sql_select, values[-1]) # 마지막 변수 사용.
        array_set_server = CURSARRAYLOCAL.fetchall()
        row_count_server = len(array_set_server)
        print(get_info(), "row_count_server: ", row_count_server)

    except pymysql.MySQLError as e:
        print(get_info(), "MySQL Error: ", str(e))
        return False

    # Update 쿼리 실행
    try:
        # sql = """
        #     UPDATE MORNING_CAFE_SCENE SET LYRICS_PROMPT = %s, LYRICS = %s, MUSIC_NAME = %s
        #     WHERE DIRECTORY = %s
        # """
        CURSARRAYLOCAL.execute(sql, values)
        MYSQLLOCALDB.commit()
        print(get_info(), "Update Data 성공: ", values)
        return True
    except pymysql.MySQLError as e:
        MYSQLLOCALDB.rollback()
        print(get_info(), "MySQL Error: ", str(e))
        return False
    except Exception as e:
        MYSQLLOCALDB.rollback()
        print(get_info(), "Error: ", str(e))
        return False


# Row Data Updating.
def __updateRowData(CONNECTEDLOCAL, code_scene, image_name, video_name, music_name):

    if not CONNECTEDLOCAL:  # == False:
        MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
            BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
        # print("__getProcess mySqlWebDb: ", mySqlWebDb, "type(mySqlWebDb):", type(mySqlWebDb))

        if type(MYSQLLOCALDB) is pymysql.connections.Connection or type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
            CONNECTEDLOCAL = True
            # print(get_info(), "Database 연결 성공!")
            # os.system("pause")
        else:
            CONNECTEDLOCAL = False
            print(get_info(), "Database 연결을 확인하시오!")

    # print(get_info(), ", __dbMrp.py revision: ", revision, ", dateCurrent: ", dateCurrent,
    #       ", dateStartStr: ", dateStartStr, ", dateEndStr: ", dateEndStr)

    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)
    print(get_info(), "code_scene: ", code_scene)

    # 0. code_scene 체크.
    sql = "Select DIRECTORY, CODE_IDEA, TITLE, CONTENT, CODE_SCENE, SCENE, SCENARIO, VIDEO_PROMPT, " \
          "IMAGE_NAME, VIDEO_NAME, MUSIC_NAME " \
          "From MORNING_CAFE_SCENE Where CODE_SCENE = %s Order By CODE_SCENE ASC "
    values = (code_scene,)  # todo: 튜플로 만들어야 함

    try:
        CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
    except:  # DB 연결을 한 번 더 시도...
        if CONNECTEDLOCAL == False:
            MYSQLLOCALDB, CURSARRAYLOCAL, CURSDICTLOCAL, COMPANY_CODE, HOST1, USER1, PASS1, DBNAME1, \
                BOUNCE_TIME, SLEEP_TIME, TIME_GAP, NIGHT_CLOSING_HHMMSS, DAY_CLOSING_HHMMSS = connectLocalDB()
            if type(MYSQLLOCALDB) is pymysql.connections.Connection or \
                    type(CURSARRAYLOCAL) is pymysql.cursors.Cursor:
                CONNECTEDLOCAL = True
                print(get_info(), "Database 연결 성공!")
                # os.system("pause")
            else:
                CONNECTEDLOCAL = False
                print(get_info(), "Database 연결을 확인하시오!")
        try:
            CURSARRAYLOCAL.execute(sql, values)  # 우측은 에러 발생함에 주의. cursArrayWeb.execute(sql,from_date,to_date)
        except pymysql.MySQLError as e:
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            print(get_info(), "Error: ", str(e))
        else:
            print(get_info(), "Successfully Selected: ", values)

    # array_sets_server = cursArrayWeb.fetchone()
    # 요넘 "fetchon()" 함수는 아래 "row_count_server = len(array_sets_server)"에서 에러가 발생한다.
    # 오직 1개 이므로 의미가 "len()" 의미가 없다는 것 같다.
    array_sets_server = CURSARRAYLOCAL.fetchall()
    row_count_server = len(array_sets_server)
    print(get_info(), "array_sets_server: ", row_count_server)
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "type(array_sets_server): ", type(row_count_server))
    print(get_info(), "array_sets_server.count(): ", row_count_server, ", values: ", values)

    print(get_info(), "code_scene: ", code_scene)
    print(get_info(), "image_name: ", image_name)
    print(get_info(), "video_name: ", video_name)
    print(get_info(), "music_name: ", music_name)

    # os.system("pause")
    sql = "Update MORNING_CAFE_SCENE Set IMAGE_NAME = %s, VIDEO_NAME = %s, MUSIC_NAME = %s " \
          "Where CODE_SCENE = %s "
    values = (image_name, video_name, music_name, code_scene)

    rsUpdate = False
    try:
        CURSARRAYLOCAL.execute(sql, values)  # array_sets_server.execute() 아님에 주의.
    except pymysql.MySQLError as e:
        print(get_info(), "MySQL 오류: ", str(e))
    except Exception as e:
        print(get_info(), "일반 오류: ", str(e))
    else:
        rsUpdate = True
        print(get_info(), "Update Data 성공: ", values)
    print(get_info(), "values: ", values)
    print(get_info(), "CURSARRAYLOCAL: ", CURSARRAYLOCAL)

    rsUpdateCommit = False
    if rsUpdate:
        try:
            MYSQLLOCALDB.commit()
            rsUpdateCommit = True
            print(get_info(), "CODE_SCENE: ", code_scene, " 서버 commit 성공!")
        except pymysql.MySQLError as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "MySQL Error: ", str(e))
        except Exception as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "Error: ", str(e))
        except KeyboardInterrupt as e:
            MYSQLLOCALDB.rollback()
            print(get_info(), "KeyboardInterrupt Error: ", str(e), " DB rollback...")
            print(get_info(), "CODE_SCENE: ", code_scene, " 서버 저장 실패!")

    return rsUpdateCommit


def __delFile(code_scene):
    #  todo: image, video, music 파일을 체크하여, 반드시 삭제 해야 한다. ===> 프롬프트 내용과 image 파일 정체성 일치.
    image = code_scene + "0.png"
    video = code_scene + "0.mp4"
    music = code_scene + "0.mp3"
    # 파일 삭제
    for i in range(1, 3):
        if i == 0:
            file_name = os.path.join(PATH_YMD, image)
        elif i == 1:
            file_name = os.path.join(PATH_YMD, video)
        elif i == 2:
            file_name = os.path.join(PATH_YMD, music)

        rsDeleteFile = False
        try:
            os.remove(file_name)
            rsDeleteFile = True
            print(get_info(), f"{file_name}이 삭제 되었습니다.")
        except FileNotFoundError:
            print(get_info(), f"{file_name}이 존재하지 않습니다.")
            rsDeleteFile = True
        except PermissionError:
            print(get_info(), f"{file_name} 삭제할 권한이 없습니다.")
            break
        except Exception as e:
            print(get_info(), "Error: ", str(e))
            break

        if not rsDeleteFile: # 3개 파일 삭제 중 에러이면, 바로 시스템 종료 시켜 확인 해야 한다.
            break

        time.sleep(1) # 반드시 쉬게 한다.

    # if not rsDeleteFile: # 3개 파일 삭제 중 에러이면, 바로 시스템 종료 시켜 확인 해야 한다.

    return rsDeleteFile
