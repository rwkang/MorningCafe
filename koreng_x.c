Copy
#include <windows.h>

// 함수 선언
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

// 전역 변수
int isHangulMode = 0;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 윈도우 클래스 등록
    WNDCLASSEX wc;
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc = WindowProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = "ColorWindowClass";
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc)) {
        MessageBox(NULL, "Window Registration Failed!", "Error", MB_OK);
        return 0;
    }

    // 색상 창 생성
    HWND hwndColor = CreateWindowEx(
        0,
        "ColorWindowClass",
        "Color Window",
        WS_POPUP | WS_VISIBLE | WS_BORDER,
        200, 200,
        75, 75,
        NULL, NULL, hInstance, NULL
    );

    if (hwndColor == NULL) {
        MessageBox(NULL, "Window Creation Failed!", "Error", MB_OK);
        return 0;
    }

    // 창 표시
    ShowWindow(hwndColor, nCmdShow);
    UpdateWindow(hwndColor);

    // 타이머 설정
    SetTimer(hwndColor, 1, 100, NULL);

    // 성공 메시지
    MessageBox(NULL, "Window created successfully", "Color Window", MB_OK);

    // 메시지 루프
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

// 윈도우 프로시저
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            KillTimer(hwnd, 1);
            PostQuitMessage(0);
            return 0;

        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            RECT rect;
            GetClientRect(hwnd, &rect);

            // 한글/영문 상태에 따라 색상 결정
            COLORREF color = isHangulMode ? RGB(255, 0, 0) : RGB(0, 255, 0);
            HBRUSH brush = CreateSolidBrush(color);

            FillRect(hdc, &rect, brush);
            DeleteObject(brush);

            EndPaint(hwnd, &ps);
            return 0;
        }

        case WM_TIMER:
            // 한/영 키 상태 확인
            if ((GetKeyState(VK_HANGUL) & 1) != isHangulMode) {
                isHangulMode = GetKeyState(VK_HANGUL) & 1;
                InvalidateRect(hwnd, NULL, TRUE);
            }
            return 0;

        case WM_KEYDOWN:
            if (wParam == VK_HANGUL) {
                isHangulMode = !isHangulMode;
                InvalidateRect(hwnd, NULL, TRUE);
                return 0;
            }
            break;
    }

    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}
