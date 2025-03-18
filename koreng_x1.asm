section .data
    className db "KeyboardLEDClass", 0
    colorClassName db "ColorWindowClass", 0
    windowTitle db "Keyboard LED", 0
    colorTitle db "Color Window", 0
    errorMsg db "Error creating window", 0
    successMsg db "Window created successfully", 0
    regErrorMsg db "Error registering window class", 0
    debugFmt db "Value: %d", 0
    debugTitle db "Debug", 0

section .bss
    msg resb 48        ; MSG 구조체
    wc resb 80         ; WNDCLASSEX 구조체
    cwc resb 80        ; 색상 윈도우용 WNDCLASSEX 구조체
    ps resb 72         ; PAINTSTRUCT 구조체
    rect resb 16       ; RECT 구조체
    hwnd resq 1        ; HWND (메인 윈도우 핸들)
    colorHwnd resq 1   ; 색상 윈도우 핸들
    hInstance resq 1   ; 인스턴스 핸들
    debugValue resd 1  ; 디버그 값 저장용
    isHangulMode resd 1 ; 한글 모드 상태 저장 (0=영문, 1=한글)

section .text
    ; 윈도우 메시지 상수
    %define WM_PAINT 0x000F
    %define WM_DESTROY 0x0002
    %define WM_CLOSE 0x0010
    %define WM_TIMER 0x0113
    %define WM_CREATE 0x0001
    %define WM_KEYDOWN 0x0100
    %define WM_KEYUP 0x0101
    %define WM_SYSKEYDOWN 0x0104
    %define WM_SYSKEYUP 0x0105

    ; 키보드 상수
    %define VK_HANGUL 0x15
    %define VK_HANGEUL 0x15  ; 동일한 값

    ; 색상 상수 (BGR 형식)
    %define RGB_GREEN 0x0000FF00
    %define RGB_RED 0x000000FF

    ; 윈도우 스타일 상수
    %define WS_POPUP 0x80000000
    %define WS_VISIBLE 0x10000000
    %define WS_BORDER 0x00800000
    %define WS_THICKFRAME 0x00040000
    %define WS_CAPTION 0x00C00000
    %define WS_SYSMENU 0x00080000
    %define WS_EX_TOPMOST 0x00000008
    %define WS_OVERLAPPED 0x00000000
    %define WS_DISABLED 0x08000000
    %define WS_EX_TOOLWINDOW 0x00000080
    %define CS_HREDRAW 0x0002
    %define CS_VREDRAW 0x0001
    %define SW_SHOW 5
    %define SW_HIDE 0
    %define SW_SHOWMINNOACTIVE 7

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
    extern MessageBoxA, ExitProcess, InvalidateRect, SendMessageA
    extern wsprintfA, GetKeyboardLayout, GetKeyState

    ; 진입점 (중요: 링커에 따라 main 또는 WinMain 모두 사용)
    global main
    global WinMain
    global WndProc
    global ColorWndProc

main:
WinMain:
    ; 스택 정렬을 위한 준비
    push rbp
    mov rbp, rsp
    sub rsp, 64              ; 충분한 스택 공간 확보

    ; 초기 한글 모드 상태 설정
    mov dword [rel isHangulMode], 0  ; 기본값은 영문 모드 (0)

    ; 인스턴스 핸들 가져오기
    xor rcx, rcx              ; NULL
    call GetModuleHandleA
    test rax, rax             ; 핸들 확인
    jz exit_program           ; 실패시 종료

    mov [rel hInstance], rax  ; 인스턴스 핸들 저장

    ; WNDCLASSEX 구조체 초기화 (메인 윈도우용)
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

    ; WNDCLASSEX 구조체 초기화 (색상 윈도우용)
    lea rcx, [rel cwc]
    mov dword [rcx], 80      ; cbSize = sizeof(WNDCLASSEX)
    mov dword [rcx+4], CS_HREDRAW | CS_VREDRAW  ; style

    ; ColorWndProc 설정
    lea rdx, [rel ColorWndProc]
    mov [rcx+8], rdx         ; lpfnWndProc

    mov dword [rcx+16], 0    ; cbClsExtra
    mov dword [rcx+20], 0    ; cbWndExtra

    mov rdx, [rel hInstance]
    mov [rcx+24], rdx        ; hInstance

    ; 시스템 아이콘 사용
    xor rcx, rcx             ; NULL
    mov rdx, 32512           ; IDI_APPLICATION
    call LoadIconA

    lea rcx, [rel cwc]
    mov [rcx+32], rax        ; hIcon

    ; 기본 커서 로드
    xor rcx, rcx             ; NULL
    mov rdx, 32512           ; IDC_ARROW
    call LoadCursorA

    lea rcx, [rel cwc]
    mov [rcx+40], rax        ; hCursor

    ; 배경색 - 기본 윈도우 색
    mov qword [rcx+48], 6    ; hbrBackground = COLOR_WINDOW + 1
    mov qword [rcx+56], 0    ; lpszMenuName

    lea rdx, [rel colorClassName]
    mov [rcx+64], rdx        ; lpszClassName

    mov qword [rcx+72], 0    ; hIconSm

    ; 색상 윈도우 클래스 등록
    lea rcx, [rel cwc]
    call RegisterClassExA

    ; 등록 결과 체크
    test rax, rax
    jz reg_error             ; 등록 실패시 에러

    ; 윈도우 크기 (약 75픽셀)
    mov r14d, 75             ; 너비 (2cm 약 75픽셀)
    mov r15d, 75             ; 높이 (2cm 약 75픽셀)

    ; 메인 윈도우 생성 - 완전히 보이지 않게 스타일 설정
    mov rcx, WS_EX_TOOLWINDOW ; dwExStyle = 툴 윈도우 (작업 표시줄에 표시 안됨)
    lea rdx, [rel className]  ; lpClassName
    lea r8, [rel windowTitle] ; lpWindowName
    mov r9d, WS_OVERLAPPED | WS_DISABLED ; 기본 스타일만 (보이지 않음)

    sub rsp, 64               ; 파라미터를 위한 스택 공간 확보
    mov qword [rsp+32], 0     ; lpParam
    mov rax, [rel hInstance]
    mov qword [rsp+24], rax   ; hInstance
    mov qword [rsp+16], 0     ; hMenu
    mov qword [rsp+8], 0      ; hWndParent
    mov dword [rsp+4], 1      ; nHeight (최소 크기)
    mov dword [rsp], 1        ; nWidth (최소 크기)
    mov qword [rsp+48], -10000 ; Y (화면 밖으로 멀리)
    mov qword [rsp+40], -10000 ; X (화면 밖으로 멀리)

    call CreateWindowExA
    add rsp, 64               ; 스택 복원

    ; 윈도우 핸들 저장 및 확인
    mov [rel hwnd], rax
    test rax, rax
    jz error_exit            ; 윈도우 생성 실패시 에러

    ; 메인 윈도우를 숨김
    mov rcx, [rel hwnd]
    mov rdx, SW_HIDE
    call ShowWindow

    ; 색상 윈도우 생성 (2번 창)
    mov rcx, WS_EX_TOPMOST   ; dwExStyle = 항상 위에 표시
    lea rdx, [rel colorClassName]  ; lpClassName
    lea r8, [rel colorTitle] ; lpWindowName
    mov r9d, WS_POPUP | WS_VISIBLE | WS_BORDER | WS_THICKFRAME ; 드래그 가능

    sub rsp, 64               ; 파라미터를 위한 스택 공간 확보
    mov qword [rsp+32], 0     ; lpParam
    mov rax, [rel hInstance]
    mov qword [rsp+24], rax   ; hInstance
    mov qword [rsp+16], 0     ; hMenu
    mov qword [rsp+8], 0      ; hWndParent
    mov dword [rsp+4], r15d   ; nHeight
    mov dword [rsp], r14d     ; nWidth
    mov qword [rsp+48], 200   ; Y - 다른 위치에 표시
    mov qword [rsp+40], 200   ; X - 다른 위치에 표시

    call CreateWindowExA
    add rsp, 64               ; 스택 복원

    ; 색상 윈도우 핸들 저장
    mov [rel colorHwnd], rax
    test rax, rax
    jz error_exit            ; 윈도우 생성 실패시 에러

    ; 색상 윈도우 표시
    mov rcx, rax             ; hWnd
    mov rdx, SW_SHOW         ; nCmdShow
    call ShowWindow

    ; 색상 윈도우 업데이트
    mov rcx, [rel colorHwnd]
    call UpdateWindow

    ; 타이머 설정 (색상 윈도우용)
    mov rcx, [rel colorHwnd]  ; hWnd
    mov rdx, IDT_TIMER1      ; nIDEvent
    mov r8, 100              ; uElapse (100ms)
    xor r9, r9               ; lpTimerFunc (NULL)
    call SetTimer

    ; 성공 메시지 표시 (4번 창)
    xor rcx, rcx             ; hWnd = NULL (최상위 윈도우 중앙에 표시)
    lea rdx, [rel successMsg]; lpText
    lea r8, [rel windowTitle]; lpCaption
    mov r9d, MB_OK | MB_ICONINFORMATION ; uType
    call MessageBoxA

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

; 메인 윈도우 프로시저
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
    cmp rdx, WM_DESTROY
    je .WM_DESTROY
    cmp rdx, WM_CLOSE
    je .WM_CLOSE

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

    ; 그리기 종료
    mov rcx, [rsp+32]        ; hWnd
    lea rdx, [rel ps]        ; lpPaint
    call EndPaint

    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.WM_CLOSE:
    ; 윈도우 닫기 요청 - 숨기기만 하고 종료하지 않음
    mov rcx, [rel hwnd]
    mov rdx, SW_HIDE
    call ShowWindow
    xor rax, rax             ; 처리 완료 (0 반환)
    jmp .end

.WM_DESTROY:
    ; 메인 윈도우 종료 시에는 PostQuitMessage를 호출하지 않음
    ; 색상 윈도우가 계속 실행되도록 함
    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.end:
    ; 함수 에필로그
    add rsp, 80
    pop rbp
    ret

; 색상 윈도우 프로시저
ColorWndProc:
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
    cmp rdx, WM_KEYDOWN
    je .WM_KEYDOWN
    cmp rdx, WM_SYSKEYDOWN
    je .WM_SYSKEYDOWN
    cmp rdx, 0x84           ; WM_NCHITTEST 메시지
    je .WM_NCHITTEST

    ; 기본 윈도우 프로시저 호출
    call DefWindowProcA
    jmp .end

.WM_NCHITTEST:
    mov rax, 2              ; HTCAPTION 반환 (드래그 가능)
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

    ; 현재 한글/영문 상태에 따라 색상 결정
    mov eax, dword [rel isHangulMode]
    test eax, eax
    jnz .korean_mode

    ; 영문 모드 - 초록색
    mov ecx, RGB_GREEN
    jmp .create_brush

.korean_mode:
    ; 한글 모드 - 빨간색
    mov ecx, RGB_RED

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
    ; 타이머 이벤트 - 한/영 키 상태 확인
    mov [rsp+32], rcx        ; hWnd 저장

    ; 한/영 키 상태 확인
    mov rcx, VK_HANGUL
    call GetKeyState
    and eax, 1               ; 토글 상태 확인 (최하위 비트)

    ; 현재 상태와 비교하여 변경되었는지 확인
    cmp eax, dword [rel isHangulMode]
    je .no_change

    ; 상태가 변경되었으면 업데이트
    mov dword [rel isHangulMode], eax

    ; 윈도우 갱신 요청
    mov rcx, [rsp+32]        ; hWnd
    xor rdx, rdx             ; lpRect (NULL)
    mov r8, 1                ; bErase
    call InvalidateRect

.no_change:
    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.WM_KEYDOWN:
.WM_SYSKEYDOWN:
    ; 한/영 키 누름 처리
    cmp r8d, VK_HANGUL       ; wParam이 한/영 키인지 확인
    jne .default_proc

    ; 한/영 키가 눌렸으므로 상태 토글
    mov eax, dword [rel isHangulMode]
    xor eax, 1               ; 상태 반전 (0->1, 1->0)
    mov dword [rel isHangulMode], eax

    ; 윈도우 갱신 요청
    mov [rsp+32], rcx        ; hWnd 저장
    xor rdx, rdx             ; lpRect (NULL)
    mov r8, 1                ; bErase
    call InvalidateRect

    xor rax, rax             ; 0 반환 (성공)
    jmp .end

.default_proc:
    ; 다른 키는 기본 처리
    call DefWindowProcA
    jmp .end

.WM_DESTROY:
    ; 색상 윈도우가 닫히면 프로그램 종료
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
