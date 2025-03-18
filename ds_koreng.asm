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
    currentColor resd 1 ; 현재 색상 저장용

section .text
    %define WM_PAINT 0x000F
    %define WM_DESTROY 0x0002
    %define WM_TIMER 0x0113
    %define WM_CREATE 0x0001
    %define VK_HANGUL 0x15
    %define RGB_GREEN 0x0000FF00
    %define RGB_RED 0x000000FF
    %define WS_OVERLAPPEDWINDOW 0x00CF0000
    %define WS_VISIBLE 0x10000000
    %define CS_HREDRAW 0x0002
    %define CS_VREDRAW 0x0001
    %define SW_SHOW 5
    %define IDT_TIMER1 1
    %define MB_OK 0
    %define MB_ICONINFORMATION 0x00000040

    extern GetMessageA, TranslateMessage, DispatchMessageA
    extern CreateWindowExA, ShowWindow, UpdateWindow, DefWindowProcA
    extern GetAsyncKeyState, FillRect, BeginPaint, EndPaint
    extern GetClientRect, PostQuitMessage, SetTimer, KillTimer
    extern RegisterClassExA, CreateSolidBrush, DeleteObject
    extern GetModuleHandleA, LoadIconA, LoadCursorA
    extern MessageBoxA, ExitProcess, InvalidateRect

    global main
    global WinMain
    global WndProc

main:
WinMain:
    push rbp
    mov rbp, rsp
    sub rsp, 64              ; 충분한 스택 공간 확보

    xor rcx, rcx              ; NULL
    call GetModuleHandleA
    test rax, rax
    jz exit_program

    mov [rel hInstance], rax

    lea rcx, [rel wc]
    mov dword [rcx], 80
    mov dword [rcx+4], CS_HREDRAW | CS_VREDRAW

    lea rdx, [rel WndProc]
    mov [rcx+8], rdx
    mov dword [rcx+16], 0
    mov dword [rcx+20], 0

    mov rdx, [rel hInstance]
    mov [rcx+24], rdx

    xor rcx, rcx
    mov rdx, 32512
    call LoadIconA
    lea rcx, [rel wc]
    mov [rcx+32], rax

    xor rcx, rcx
    mov rdx, 32512
    call LoadCursorA
    lea rcx, [rel wc]
    mov [rcx+40], rax

    mov qword [rcx+48], 6
    mov qword [rcx+56], 0
    lea rdx, [rel className]
    mov [rcx+64], rdx
    mov qword [rcx+72], 0

    lea rcx, [rel wc]
    call RegisterClassExA
    test rax, rax
    jz reg_error

    ; 가로 및 세로 크기를 2cm로 변경
    mov r14d, 76             ; 너비 (약 2cm, 1cm ≈ 38픽셀)
    mov r15d, 76             ; 높이 (약 2cm)

    xor rcx, rcx
    lea rdx, [rel className]
    lea r8, [rel windowTitle]
    mov r9d, WS_OVERLAPPEDWINDOW | WS_VISIBLE

    sub rsp, 64
    mov qword [rsp+32], 0
    mov rax, [rel hInstance]
    mov qword [rsp+24], rax
    mov qword [rsp+16], 0
    mov qword [rsp+8], 0
    mov dword [rsp+4], r15d
    mov dword [rsp], r14d
    mov qword [rsp+48], 100
    mov qword [rsp+40], 100

    call CreateWindowExA
    add rsp, 64

    mov [rel hwnd], rax
    test rax, rax
    jz error_exit

    mov rcx, rax
    mov rdx, SW_SHOW
    call ShowWindow

    mov rcx, [rel hwnd]
    call UpdateWindow

    mov rcx, [rel hwnd]
    mov rdx, IDT_TIMER1
    mov r8, 500
    xor r9, r9
    call SetTimer

    xor rcx, rcx
    lea rdx, [rel successMsg]
    lea r8, [rel windowTitle]
    mov r9d, MB_OK | MB_ICONINFORMATION
    call MessageBoxA

    mov rcx, [rel hwnd]
    xor rdx, rdx
    mov r8, 1
    call InvalidateRect

msg_loop:
    lea rcx, [rel msg]
    xor rdx, rdx
    xor r8, r8
    xor r9, r9
    call GetMessageA
    cmp rax, 0
    jle exit_program

    lea rcx, [rel msg]
    call TranslateMessage

    lea rcx, [rel msg]
    call DispatchMessageA
    jmp msg_loop

reg_error:
    xor rcx, rcx
    lea rdx, [rel regErrorMsg]
    lea r8, [rel windowTitle]
    mov r9d, MB_OK | MB_ICONINFORMATION
    call MessageBoxA
    jmp exit_program

error_exit:
    xor rcx, rcx
    lea rdx, [rel errorMsg]
    lea r8, [rel windowTitle]
    mov r9d, MB_OK | MB_ICONINFORMATION
    call MessageBoxA

exit_program:
    mov rcx, 0
    call ExitProcess

WndProc:
    push rbp
    mov rbp, rsp
    sub rsp, 80               ; shadow space + 지역 변수

    cmp rdx, WM_CREATE
    je .WM_CREATE
    cmp rdx, WM_PAINT
    je .WM_PAINT
    cmp rdx, WM_TIMER
    je .WM_TIMER
    cmp rdx, WM_DESTROY
    je .WM_DESTROY

    call DefWindowProcA
    jmp .end

.WM_CREATE:
    xor rax, rax
    ; 초기 바탕색은 초록색으로 설정
    mov dword [rel currentColor], RGB_GREEN
    jmp .end

.WM_PAINT:
    mov [rsp+32], rcx
    lea rdx, [rel ps]
    call BeginPaint
    mov rbx, rax             ; HDC 저장

    mov rcx, [rsp+32]
    lea rdx, [rel rect]
    call GetClientRect

    ; 현재 키보드 언어 상태 확인
    mov rcx, VK_HANGUL
    call GetAsyncKeyState
    test ax, 1               ; 한/영 키의 상태 확인

    jz .check_english_mode    ; 한글이 아닐 경우 영어 모드 체크

.korean_mode:
    ; 한글 모드 - 빨간색
    mov ecx, RGB_RED
    mov dword [rel currentColor], RGB_RED ; 현재 색상을 빨간색으로 설정
    jmp .create_brush

.check_english_mode:
    ; 영어 모드 - 초록색
    mov ecx, RGB_GREEN
    mov dword [rel currentColor], RGB_GREEN ; 현재 색상을 초록색으로 설정

.create_brush:
    call CreateSolidBrush
    mov r15, rax             ; 브러시 핸들 저장

    ; 사각형 채우기
    mov rcx, rbx
    lea rdx, [rel rect]
    mov r8, r15
    call FillRect

    ; 브러시 삭제
    mov rcx, r15
    call DeleteObject

    ; 페인팅 종료
    mov rcx, [rsp+32]
    lea rdx, [rel ps]
    call EndPaint

    xor rax, rax
    jmp .end

.WM_TIMER:
    mov [rsp+32], rcx
    xor rdx, rdx
    mov r8, 1
    call InvalidateRect
    xor rax, rax
    jmp .end

.WM_DESTROY:
    mov [rsp+32], rcx
    mov rdx, IDT_TIMER1
    call KillTimer
    xor rcx, rcx
    call PostQuitMessage
    xor rax, rax

.end:
    add rsp, 80
    pop rbp
    ret
