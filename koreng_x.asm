section .data
    className db "LangIndicatorClass", 0
    title db "", 0  ; 타이틀 바 제거

section .bss
    msg resb 48     ; MSG 구조체
    wc resb 80      ; WNDCLASSEX 구조체
    ps resb 72      ; PAINTSTRUCT 구조체
    rect resb 16    ; RECT 구조체
    hwnd resq 1     ; 창 핸들
    hInst resq 1    ; 인스턴스 핸들
    isHangul resd 1 ; 한글 상태 (0=영문, 1=한글)

section .text
    %define WM_PAINT 0x000F
    %define WM_DESTROY 0x0002
    %define WM_TIMER 0x0113
    %define WM_KEYDOWN 0x0100
    %define WM_SYSKEYDOWN 0x0104
    %define WM_NCHITTEST 0x0084
    %define WM_LBUTTONDOWN 0x0201
    %define VK_HANGUL 0x15
    %define RGB_GREEN 0x0000FF00  ; 영문: 초록
    %define RGB_RED 0x000000FF    ; 한글: 빨강
    %define WS_POPUP 0x80000000
    %define WS_VISIBLE 0x10000000
    %define WS_EX_TOPMOST 0x00000008
    %define WS_EX_TOOLWINDOW 0x00000080
    %define CS_HREDRAW 0x0002
    %define CS_VREDRAW 0x0001
    %define SW_SHOW 5
    %define IDT_TIMER1 1
    %define HTCAPTION 2

    extern GetMessageA, TranslateMessage, DispatchMessageA
    extern CreateWindowExA, ShowWindow, UpdateWindow, DefWindowProcA
    extern FillRect, BeginPaint, EndPaint, GetClientRect, PostQuitMessage
    extern SetTimer, KillTimer, RegisterClassExA, CreateSolidBrush, DeleteObject
    extern GetModuleHandleA, GetKeyboardLayout, GetForegroundWindow, GetWindowThreadProcessId
    extern InvalidateRect, ExitProcess, ReleaseCapture

    global main
    global WndProc

main:
    push rbp
    mov rbp, rsp
    sub rsp, 32

    ; 초기 상태
    mov dword [rel isHangul], 0  ; 영문 모드

    ; 인스턴스 핸들
    xor rcx, rcx
    call GetModuleHandleA
    test rax, rax
    jz .exit
    mov [rel hInst], rax

    ; WNDCLASSEX 설정 (최소화)
    lea rcx, [rel wc]
    mov dword [rcx], 80
    mov dword [rcx+4], CS_HREDRAW | CS_VREDRAW
    lea rdx, [rel WndProc]
    mov [rcx+8], rdx
    mov [rcx+24], rax
    lea rdx, [rel className]
    mov [rcx+64], rdx

    ; 클래스 등록
    call RegisterClassExA
    test rax, rax
    jz .exit

    ; 창 생성 (75x75, 최상단, 드래그 가능, 테두리/타이틀 없음)
    mov rcx, WS_EX_TOPMOST | WS_EX_TOOLWINDOW
    lea rdx, [rel className]
    lea r8, [rel title]
    mov r9d, WS_POPUP | WS_VISIBLE
    sub rsp, 64
    mov qword [rsp+32], 100  ; 초기 X (작업 표시줄 아래로 설정 가능)
    mov qword [rsp+40], 100  ; 초기 Y (작업 표시줄 아래로 설정 가능)
    mov dword [rsp+48], 75   ; 너비
    mov dword [rsp+56], 75   ; 높이
    mov rax, [rel hInst]
    mov [rsp+64], rax
    call CreateWindowExA
    add rsp, 64
    mov [rel hwnd], rax
    test rax, rax
    jz .exit

    ; 창 표시
    mov rcx, rax
    mov rdx, SW_SHOW
    call ShowWindow
    mov rcx, [rel hwnd]
    call UpdateWindow

    ; 타이머 설정 (100ms)
    mov rcx, [rel hwnd]
    mov rdx, IDT_TIMER1
    mov r8, 100
    xor r9, r9
    call SetTimer

    ; 메시지 루프
.loop:
    lea rcx, [rel msg]
    xor rdx, rdx
    xor r8, r8
    xor r9, r9
    call GetMessageA
    test rax, rax
    jle .exit
    lea rcx, [rel msg]
    call TranslateMessage
    lea rcx, [rel msg]
    call DispatchMessageA
    jmp .loop

.exit:
    xor rcx, rcx
    call ExitProcess

WndProc:
    push rbp
    mov rbp, rsp
    sub rsp, 80

    cmp rdx, WM_PAINT
    je .paint
    cmp rdx, WM_DESTROY
    je .destroy
    cmp rdx, WM_TIMER
    je .timer
    cmp rdx, WM_KEYDOWN
    je .keydown
    cmp rdx, WM_SYSKEYDOWN
    je .keydown
    cmp rdx, WM_NCHITTEST
    je .nchittest
    cmp rdx, WM_LBUTTONDOWN
    je .lbuttondown

    call DefWindowProcA
    jmp .end

.paint:
    mov [rsp+32], rcx
    lea rdx, [rel ps]
    call BeginPaint
    mov rbx, rax
    mov rcx, [rsp+32]
    lea rdx, [rel rect]
    call GetClientRect
    mov eax, [rel isHangul]
    test eax, eax
    jnz .korean
    mov ecx, RGB_GREEN  ; 영문: 초록
    jmp .brush
.korean:
    mov ecx, RGB_RED    ; 한글: 빨강
.brush:
    call CreateSolidBrush
    mov r15, rax
    mov rcx, rbx
    lea rdx, [rel rect]
    mov r8, r15
    call FillRect
    mov rcx, r15
    call DeleteObject
    mov rcx, [rsp+32]
    lea rdx, [rel ps]
    call EndPaint
    xor rax, rax
    jmp .end

.timer:
    mov [rsp+32], rcx
    call GetForegroundWindow
    test rax, rax
    jz .default_layout
    mov rcx, rax
    xor rdx, rdx
    call GetWindowThreadProcessId
    mov rcx, rax
    call GetKeyboardLayout
    jmp .check_layout
.default_layout:
    xor rcx, rcx
    call GetKeyboardLayout
.check_layout:
    and rax, 0xFFFF
    cmp rax, 0x0412  ; 한국어
    sete al
    mov [rel isHangul], al
    mov rcx, [rsp+32]
    xor rdx, rdx
    mov r8, 1
    call InvalidateRect
    xor rax, rax
    jmp .end

.keydown:
    cmp r8d, VK_HANGUL
    jne .end
    call GetForegroundWindow
    test rax, rax
    jz .default_layout_key
    mov rcx, rax
    xor rdx, rdx
    call GetWindowThreadProcessId
    mov rcx, rax
    call GetKeyboardLayout
    jmp .check_layout_key
.default_layout_key:
    xor rcx, rcx
    call GetKeyboardLayout
.check_layout_key:
    and rax, 0xFFFF
    cmp rax, 0x0412
    sete al
    mov [rel isHangul], al
    mov rcx, [rsp+32]
    xor rdx, rdx
    mov r8, 1
    call InvalidateRect
    xor rax, rax
    jmp .end

.nchittest:
    mov rax, HTCAPTION
    jmp .end

.lbuttondown:
    mov [rsp+32], rcx
    call ReleaseCapture
    mov rcx, [rsp+32]
    mov rdx, 0xF012  ; SC_DRAGMOVE
    xor r8, r8
    xor r9, r9
    call DefWindowProcA
    xor rax, rax
    jmp .end

.destroy:
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