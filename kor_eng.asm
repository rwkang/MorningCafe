; 2025.02.28 03:59 마지막 성공 후 수정 프롬프트 : Grog 3 연결되면, 질문... Free로... Claude 3.7 Sonnet Normal 버전.
; 이번엔 성공했는데, 첨부와 같이 윈도우가 너무 크게 나오는데, 이것을 가로x세로 1Cm 크기로 수정해 주고, 또 중요한 것은, Red가 "한글" 이면, "한/영" 토글 키를 눌러서 "영문" 상태로 변경되면, Green 으로 변경되고, 다시 "한/영" 토글 키를 눌러서 "한글" 상태가 되면, 그때 Red로 변경되도록 해줘.
지금은 "한/영" 토글키를 누르면, "한글"과 "영어"에 상관 없이 잠깐 Green으로 깜빡했다가, 바로 Red 상태로 되돌아 가네, 그럼 현재 키보드 상태가 "한글" 인지 "영어" 인지 알수가 없잖아?
현재 키보드 상태가 한글이면 Red, 영문이면 Green 이렇게 되도록, 소스를 한번더 수정해줘


section .data
    className db "KeyboardLEDClass", 0
    windowTitle db "Keyboard LED", 0
    errorMsg db "Error creating window", 0
    successMsg db "Window created successfully", 0
    regErrorMsg db "Error registering window class", 0
    debugFmt db "Value: %d", 0
    debugTitle db "Debug", 0

section .bss
    msg resb 48        ; MSG 구조체
    wc resb 80         ; WNDCLASSEX 구조체
    ps resb 72         ; PAINTSTRUCT 구조체
    rect resb 16       ; RECT 구조체
    hwnd resq 1        ; HWND
    hInstance resq 1   ; 인스턴스 핸들
    debugValue resd 1  ; 디버그 값 저장용

section .text
    ; 윈도우 메시지 상수
    %define WM_PAINT 0x000F
    %define WM_DESTROY 0x0002
    %define WM_TIMER 0x0113
    %define WM_CREATE 0x0001

    ; 키보드 상수
    %define VK_HANGUL 0x15

    ; 색상 상수 (BGR 형식)
    %define RGB_GREEN 0x0000FF00
    %define RGB_RED 0x000000FF

    ; 윈도우 스타일 상수
    %define WS_OVERLAPPEDWINDOW 0x00CF0000
    %define WS_VISIBLE 0x10000000
    %define CS_HREDRAW 0x0002
    %define CS_VREDRAW 0x0001
    %define SW_SHOW 5

    ; IDT for timer
    %define IDT_TIMER1 1

    ; MessageBox 상수
    %define MB_OK 0
    %define MB_ICONINFORMATION 0x00000040

    extern GetMessageA, TranslateMessage, DispatchMessageA
    extern CreateWindowExA, ShowWindow, UpdateWindow, DefWindowProcA
    extern GetAsyncKeyState, FillRect, BeginPaint, EndPaint
    extern GetClientRect, PostQuitMessage, SetTimer, KillTimer
    extern RegisterClassExA, CreateSolidBrush, DeleteObject
    extern GetModuleHandleA, LoadIconA, LoadCursorA, GetDesktopWindow
    extern MessageBoxA, ExitProcess, InvalidateRect
    extern wsprintfA

    ; 진입점 (중요: 링커에 따라 main 또는 WinMain 모두 사용)
    global main
    global WinMain
    global WndProc

main:
WinMain:
    ; 스택 정렬을 위한 준비
    push rbp
    mov rbp, rsp
    sub rsp, 64              ; 충분한 스택 공간 확보

    ; 인스턴스 핸들 가져오기
    xor rcx, rcx              ; NULL
    call GetModuleHandleA
    test rax, rax             ; 핸들 확인
    jz exit_program           ; 실패시 종료

    mov [rel hInstance], rax  ; 인스턴스 핸들 저장

    ; WNDCLASSEX 구조체 초기화
    lea rcx, [rel wc]
    mov dword [rcx], 80      ; cbSize = sizeof(WNDCLASSEX)
    mov dword [rcx+4], CS_HREDRAW | CS_VREDRAW  ; style

    ; WndProc 설정
    lea rdx, [rel WndProc]
    mov [rcx+8], rdx         ; lpfnWndProc

    mov dword [rcx+16], 0    ; cbClsExtra
    mov dword [rcx+20], 0    ; cbWndExtra

    mov rdx, [rel hInstance]
    mov [rcx+24], rdx        ; hInstance

    ; 시스템 아이콘 사용
    xor rcx, rcx             ; NULL
    mov rdx, 32512           ; IDI_APPLICATION
    call LoadIconA

    lea rcx, [rel wc]
    mov [rcx+32], rax        ; hIcon

    ; 기본 커서 로드
    xor rcx, rcx             ; NULL
    mov rdx, 32512           ; IDC_ARROW
    call LoadCursorA

    lea rcx, [rel wc]
    mov [rcx+40], rax        ; hCursor

    ; 배경색 - 기본 윈도우 색
    mov qword [rcx+48], 6    ; hbrBackground = COLOR_WINDOW + 1
    mov qword [rcx+56], 0    ; lpszMenuName

    lea rdx, [rel className]
    mov [rcx+64], rdx        ; lpszClassName

    mov qword [rcx+72], 0    ; hIconSm

    ; 윈도우 클래스 등록
    lea rcx, [rel wc]
    call RegisterClassExA

    ; 등록 결과 체크
    test rax, rax
    jz reg_error             ; 등록 실패시 에러

    ; 실제 값 사용
    mov r14d, 300            ; 너비
    mov r15d, 150            ; 높이

    ; 윈도우 생성
    xor rcx, rcx              ; dwExStyle = 0
    lea rdx, [rel className]  ; lpClassName
    lea r8, [rel windowTitle] ; lpWindowName
    mov r9d, WS_OVERLAPPEDWINDOW | WS_VISIBLE ; 스타일

    sub rsp, 64               ; 파라미터를 위한 스택 공간 확보 (Win64 호출 규약)
    mov qword [rsp+32], 0     ; lpParam
    mov rax, [rel hInstance]
    mov qword [rsp+24], rax   ; hInstance
    mov qword [rsp+16], 0     ; hMenu
    mov qword [rsp+8], 0      ; hWndParent
    mov dword [rsp+4], r15d   ; nHeight
    mov dword [rsp], r14d     ; nWidth
    mov qword [rsp+48], 100   ; Y
    mov qword [rsp+40], 100   ; X

    call CreateWindowExA
    add rsp, 64               ; 스택 복원

    ; 윈도우 핸들 저장 및 확인
    mov [rel hwnd], rax
    test rax, rax
    jz error_exit            ; 윈도우 생성 실패시 에러

    ; 윈도우 표시
    mov rcx, rax             ; hWnd
    mov rdx, SW_SHOW         ; nCmdShow
    call ShowWindow

    ; 윈도우 업데이트
    mov rcx, [rel hwnd]
    call UpdateWindow

    ; 타이머 설정 (500ms 간격)
    mov rcx, [rel hwnd]      ; hWnd
    mov rdx, IDT_TIMER1      ; nIDEvent
    mov r8, 500              ; uElapse (500ms)
    xor r9, r9               ; lpTimerFunc (NULL)
    call SetTimer

    ; 성공 메시지 표시
    xor rcx, rcx             ; hWnd
    lea rdx, [rel successMsg]; lpText
    lea r8, [rel windowTitle]; lpCaption
    mov r9d, MB_OK | MB_ICONINFORMATION ; uType
    call MessageBoxA

    ; 윈도우 강제 업데이트
    mov rcx, [rel hwnd]      ; hWnd
    xor rdx, rdx             ; lpRect (NULL)
    mov r8, 1                ; bErase
    call InvalidateRect

    ; 메시지 루프
msg_loop:
    lea rcx, [rel msg]       ; lpMsg
    xor rdx, rdx             ; hWnd
    xor r8, r8               ; wMsgFilterMin
    xor r9, r9               ; wMsgFilterMax
    call GetMessageA

    ; 종료 메시지 확인
    cmp rax, 0
    jle exit_program         ; 0 이하면 종료

    lea rcx, [rel msg]
    call TranslateMessage

    lea rcx, [rel msg]
    call DispatchMessageA

    jmp msg_loop

reg_error:
    ; 클래스 등록 에러 메시지
    xor rcx, rcx             ; hWnd
    lea rdx, [rel regErrorMsg] ; lpText
    lea r8, [rel windowTitle] ; lpCaption
    mov r9d, MB_OK | MB_ICONINFORMATION ; uType
    call MessageBoxA
    jmp exit_program

error_exit:
    ; 윈도우 생성 에러 메시지
    xor rcx, rcx             ; hWnd
    lea rdx, [rel errorMsg]  ; lpText
    lea r8, [rel windowTitle]; lpCaption
    mov r9d, MB_OK | MB_ICONINFORMATION ; uType
    call MessageBoxA

exit_program:
    ; 프로그램 종료
    mov rcx, 0               ; exit code
    call ExitProcess

; 윈도우 프로시저
WndProc:
    ; 함수 프롤로그
    push rbp
    mov rbp, rsp
    sub rsp, 80              ; shadow space + 지역 변수

    ; 파라미터: rcx = hWnd, rdx = uMsg, r8 = wParam, r9 = lParam

    ; 메시지 타입에 따라 처리
    cmp rdx, WM_CREATE
    je .WM_CREATE
    cmp rdx, WM_PAINT
    je .WM_PAINT
    cmp rdx, WM_TIMER
    je .WM_TIMER
    cmp rdx, WM_DESTROY
    je .WM_DESTROY

    ; 기본 윈도우 프로시저 호출
    call DefWindowProcA
    jmp .end

.WM_CREATE:
    ; 윈도우 생성 시 추가 초기화가 필요하면 여기서 수행
    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.WM_PAINT:
    ; 윈도우 그리기 준비
    mov [rsp+32], rcx        ; hWnd 저장 (첫 번째 매개변수)
    lea rdx, [rel ps]        ; lpPaint
    call BeginPaint
    mov rbx, rax             ; HDC 저장

    ; 클라이언트 영역 가져오기
    mov rcx, [rsp+32]        ; hWnd 불러오기
    lea rdx, [rel rect]      ; lpRect
    call GetClientRect

    ; 한/영 키 상태 확인
    mov rcx, VK_HANGUL
    call GetAsyncKeyState

    ; 상태에 따라 브러시 색상 결정
    test ax, 1               ; 토글 상태 확인 (최하위 비트)
    jnz .korean_mode

    ; 영문 모드 - 빨간색
    mov ecx, RGB_RED
    jmp .create_brush

.korean_mode:
    ; 한글 모드 - 초록색
    mov ecx, RGB_GREEN

.create_brush:
    call CreateSolidBrush
    mov r15, rax             ; 브러시 핸들 저장

    ; 사각형 채우기
    mov rcx, rbx             ; hdc
    lea rdx, [rel rect]      ; lprc
    mov r8, r15              ; hbr
    call FillRect

    ; 브러시 삭제
    mov rcx, r15
    call DeleteObject

    ; 그리기 종료
    mov rcx, [rsp+32]        ; hWnd
    lea rdx, [rel ps]        ; lpPaint
    call EndPaint

    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.WM_TIMER:
    ; 타이머 이벤트 - 윈도우 갱신
    mov [rsp+32], rcx        ; hWnd 저장
    xor rdx, rdx             ; lpRect (NULL)
    mov r8, 1                ; bErase
    call InvalidateRect

    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.WM_DESTROY:
    ; 타이머 제거
    mov [rsp+32], rcx        ; hWnd 저장
    mov rdx, IDT_TIMER1      ; nIDEvent
    call KillTimer

    ; 종료 메시지 전송
    xor rcx, rcx             ; nExitCode
    call PostQuitMessage

    xor rax, rax             ; 0 반환 (성공)

.end:
    ; 함수 에필로그
    add rsp, 80
    pop rbp
    ret
