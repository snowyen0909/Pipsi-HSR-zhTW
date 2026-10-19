from pathlib import Path
import argparse, shutil

MENU_CPP = r'''#include "pch.h"
#include "menu.h"
#include "imgui_impl_win32.h"
#include "cheat.h"
#include "d3d11_overlay.h"

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

namespace Menu
{
    static BOOL OnWndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
    {
        if (hIl2Cpp)
        {
            Input::UpdateKeyState(uMsg, wParam, lParam);

            if (Input::IsKeyToggled(Options.MenuKey))
            {
                if (ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam))
                    return FALSE;

                switch (uMsg)
                {
                case WM_MOVE: case WM_SIZE: case WM_ACTIVATE: case WM_SETFOCUS:
                case WM_KILLFOCUS: case WM_PAINT: case WM_ERASEBKGND:
                case WM_ACTIVATEAPP: case WM_GETMINMAXINFO:
                case WM_WINDOWPOSCHANGING: case WM_WINDOWPOSCHANGED:
                case WM_NCCALCSIZE: case WM_NCHITTEST: case WM_NCPAINT:
                case WM_NCACTIVATE: case WM_SIZING: case WM_MOVING:
                    break;
                default:
                    return FALSE;
                }
            }
        }
        return TRUE;
    }

    static void ApplyTheme()
    {
        ImGuiStyle& s = ImGui::GetStyle();
        s.WindowPadding = ImVec2(14, 14);
        s.FramePadding = ImVec2(12, 8);
        s.ItemSpacing = ImVec2(10, 10);
        s.ItemInnerSpacing = ImVec2(8, 6);
        s.WindowRounding = 14.0f;
        s.ChildRounding = 12.0f;
        s.FrameRounding = 8.0f;
        s.PopupRounding = 10.0f;
        s.ScrollbarRounding = 8.0f;
        s.GrabRounding = 8.0f;
        s.WindowBorderSize = 1.0f;
        s.ChildBorderSize = 1.0f;
        s.FrameBorderSize = 1.0f;

        ImVec4* c = s.Colors;
        c[ImGuiCol_Text] = ImVec4(0.91f,0.94f,1.00f,1.00f);
        c[ImGuiCol_TextDisabled] = ImVec4(0.49f,0.56f,0.68f,1.00f);
        c[ImGuiCol_WindowBg] = ImVec4(0.035f,0.055f,0.095f,0.97f);
        c[ImGuiCol_ChildBg] = ImVec4(0.050f,0.075f,0.125f,0.96f);
        c[ImGuiCol_PopupBg] = ImVec4(0.040f,0.060f,0.105f,0.98f);
        c[ImGuiCol_Border] = ImVec4(0.22f,0.32f,0.49f,0.85f);
        c[ImGuiCol_FrameBg] = ImVec4(0.075f,0.105f,0.165f,1.00f);
        c[ImGuiCol_FrameBgHovered] = ImVec4(0.10f,0.17f,0.29f,1.00f);
        c[ImGuiCol_FrameBgActive] = ImVec4(0.12f,0.22f,0.38f,1.00f);
        c[ImGuiCol_CheckMark] = ImVec4(0.34f,0.70f,1.00f,1.00f);
        c[ImGuiCol_SliderGrab] = ImVec4(0.35f,0.68f,1.00f,1.00f);
        c[ImGuiCol_SliderGrabActive] = ImVec4(0.72f,0.84f,1.00f,1.00f);
        c[ImGuiCol_Button] = ImVec4(0.075f,0.125f,0.220f,1.00f);
        c[ImGuiCol_ButtonHovered] = ImVec4(0.12f,0.24f,0.43f,1.00f);
        c[ImGuiCol_ButtonActive] = ImVec4(0.16f,0.31f,0.53f,1.00f);
        c[ImGuiCol_Header] = ImVec4(0.10f,0.22f,0.40f,0.85f);
        c[ImGuiCol_HeaderHovered] = ImVec4(0.14f,0.32f,0.57f,0.95f);
        c[ImGuiCol_HeaderActive] = ImVec4(0.16f,0.38f,0.68f,1.00f);
        c[ImGuiCol_Separator] = ImVec4(0.24f,0.34f,0.51f,0.70f);
    }

    static void BeforeFrame() { Cheat::BeforeFrame(); }

    static const char* Tabs[] = { "戰鬥", "探索", "視覺", "其他" };
    static const char* Descs[] =
    {
        "調整戰鬥相關功能與速度。",
        "探索、移動與世界互動功能。",
        "畫面、相機與顯示功能。",
        "設定、FPS 與其他工具。"
    };

    static int CurrentTab = 0;
    static bool ThemeApplied = false;

    static void OnFrame()
    {
        if (!hIl2Cpp)
            return;

        if (!ThemeApplied)
        {
            ApplyTheme();
            ThemeApplied = true;
        }

        if (Input::IsKeyToggled(Options.MenuKey))
        {
            ImGui::SetNextWindowSize(ImVec2(1000, 650), ImGuiCond_FirstUseEver);
            ImGui::SetNextWindowSizeConstraints(ImVec2(820, 520), ImVec2(1500, 1000));

            if (ImGui::Begin("PIPSI // HSR##MainWindow", NULL,
                ImGuiWindowFlags_NoCollapse | ImGuiWindowFlags_NoSavedSettings))
            {
                ImGui::PushStyleColor(ImGuiCol_ChildBg, ImVec4(0.025f,0.045f,0.080f,0.98f));
                if (ImGui::BeginChild("##Sidebar", ImVec2(185, 0), ImGuiChildFlags_Borders))
                {
                    ImGui::TextColored(ImVec4(0.91f,0.94f,1.00f,1.0f), "PIPSI // HSR");
                    ImGui::TextDisabled("繁體中文 UI");
                    ImGui::Separator();
                    ImGui::Dummy(ImVec2(0, 8));

                    for (int i = 0; i < IM_ARRAYSIZE(Tabs); ++i)
                    {
                        if (CurrentTab == i)
                        {
                            ImGui::PushStyleColor(ImGuiCol_Header, ImVec4(0.12f,0.29f,0.53f,0.95f));
                            ImGui::PushStyleColor(ImGuiCol_HeaderHovered, ImVec4(0.14f,0.34f,0.62f,1.0f));
                        }

                        if (ImGui::Selectable(Tabs[i], CurrentTab == i, 0, ImVec2(0, 44)))
                            CurrentTab = i;

                        if (CurrentTab == i)
                            ImGui::PopStyleColor(2);
                    }

                    ImGui::Separator();
                    ImGui::TextDisabled("快捷鍵");
                    ImGui::Text("INSERT");
                    ImGui::SameLine();
                    ImGui::TextDisabled("顯示 / 隱藏");
                }
                ImGui::EndChild();
                ImGui::PopStyleColor();

                ImGui::SameLine();

                if (ImGui::BeginChild("##Content", ImVec2(0, 0)))
                {
                    ImGui::TextColored(ImVec4(0.83f,0.73f,0.49f,1.0f), "%s", Tabs[CurrentTab]);
                    ImGui::SameLine();
                    ImGui::TextDisabled(" / PIPSI HSR");
                    ImGui::TextDisabled("%s", Descs[CurrentTab]);
                    ImGui::Separator();
                    ImGui::Dummy(ImVec2(0, 4));

                    switch (CurrentTab)
                    {
                    case 0: Cheat::MenuBattle(); break;
                    case 1: Cheat::MenuAdventure(); break;
                    case 2: Cheat::MenuVisuals(); break;
                    case 3: Cheat::MenuMisc(); break;
                    }
                }
                ImGui::EndChild();
            }
            ImGui::End();
        }

        Cheat::OnFrame();
    }

    bool Setup()
    {
        if (!D3D11_Overlay::Setup(OnWndProc, BeforeFrame, OnFrame))
            return FALSE;
        if (!Cheat::Setup())
            return FALSE;
        return TRUE;
    }
}
'''

IMGUI_USER_H = r'''#pragma once
#include <windows.h>

namespace ImGui
{
    void BeginGroupPanel(const char* label, const ImVec2& size = ImVec2(-FLT_MIN, 0.0f));
    void EndGroupPanel();
    void Hotkey(const char* label, unsigned char* p_key, bool* p_held = NULL);
    void SmallHotkey(const char* label, unsigned char* p_key, bool* p_held = NULL);
}
'''

IMGUI_USER_CPP = r'''#include "pch.h"
#include "imgui_user.h"
#include "imgui_internal.h"

namespace ImGui
{
    void BeginGroupPanel(const char* label, const ImVec2& size)
    {
        ImGui::PushID(label);
        ImVec2 s = size;
        if (s.x < 0.0f) s.x = 0.0f;
        if (s.y < 0.0f) s.y = 0.0f;

        ImGui::PushStyleColor(ImGuiCol_ChildBg, ImVec4(0.055f,0.082f,0.135f,0.94f));
        ImGui::PushStyleColor(ImGuiCol_Border, ImVec4(0.21f,0.33f,0.52f,0.88f));
        ImGui::PushStyleVar(ImGuiStyleVar_ChildRounding, 11.0f);
        ImGui::PushStyleVar(ImGuiStyleVar_ChildBorderSize, 1.0f);
        ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(14,12));

        ImGui::BeginChild("##Card", s, ImGuiChildFlags_Borders | ImGuiChildFlags_AutoResizeY);
        ImGui::TextColored(ImVec4(0.87f,0.77f,0.55f,1.0f), "%s", label);
        ImGui::Separator();
    }

    void EndGroupPanel()
    {
        ImGui::Dummy(ImVec2(0,3));
        ImGui::EndChild();
        ImGui::PopStyleVar(3);
        ImGui::PopStyleColor(2);
        ImGui::PopID();
        ImGui::Dummy(ImVec2(0,4));
    }

    static const char* KeyText(unsigned char key)
    {
        if (key == 0x00) return "未設定";
        if (key == 0xFF) return "...";
        const char* name = Input::GetKeyName(key);
        return name ? name : "未知";
    }

    void Hotkey(const char* label, unsigned char* p_key, bool* p_held)
    {
        ImGui::PushID(label);
        unsigned char key = *p_key;

        if (key == 0xFF)
        {
            unsigned char last = Input::GetLastKeyDown();
            if (last == VK_ESCAPE) *p_key = 0x00;
            else if (last != 0x00) *p_key = last;
        }

        if (ImGui::Button(KeyText(key), ImVec2(90,0)))
        {
            *p_key = 0xFF;
            Input::ClearLastKeyDown();
        }

        if (key != 0x00 && key != 0xFF && p_held)
        {
            ImGui::SameLine();
            if (ImGui::Button(*p_held ? "按住" : "切換"))
                *p_held = !*p_held;
        }
        ImGui::PopID();
    }

    void SmallHotkey(const char* label, unsigned char* p_key, bool* p_held)
    {
        ImGui::PushID(label);
        unsigned char key = *p_key;

        if (key == 0xFF)
        {
            unsigned char last = Input::GetLastKeyDown();
            if (last == VK_ESCAPE) *p_key = 0x00;
            else if (last != 0x00) *p_key = last;
        }

        if (ImGui::SmallButton(KeyText(key)))
        {
            *p_key = 0xFF;
            Input::ClearLastKeyDown();
        }

        if (key != 0x00 && key != 0xFF && p_held)
        {
            ImGui::SameLine();
            if (ImGui::SmallButton(*p_held ? "按住" : "切換"))
                *p_held = !*p_held;
        }
        ImGui::PopID();
    }
}
'''

TRANSLATE = {
    "battle_speed_changer.cpp": {
        '"Battle Speed Changer"':'"戰鬥速度"', '"Enable"':'"啟用"', '"Speed"':'"速度"'
    },
    "config.cpp": {
        '"Config"':'"設定檔"', '"Save"':'"儲存"', '"Load"':'"載入"', '"Reset"':'"重設"'
    },
    "dumb_enemies.cpp": {
        '"Dumb Enemies"':'"木樁敵人"', '"Enable"':'"啟用"'
    },
    "fov_changer.cpp": {
        '"FOV Changer"':'"視野調整 (FOV)"', '"Enable"':'"啟用"', '"Value"':'"視野角度"'
    },
    "fps_indicator.cpp": {
        '"FPS Indicator"':'"FPS 顯示"', '"Enable"':'"啟用"', '"FPS: %.0f"':'"FPS：%.0f"'
    },
    "fps_unlocker.cpp": {
        '"FPS Unlocker"':'"FPS 解鎖"', '"Enable"':'"啟用"', '"FPS Limit"':'"FPS 上限"'
    },
    "free_camera.cpp": {
        '"Free Camera"':'"自由相機"', '"Enable"':'"啟用"', '"Speed"':'"移動速度"',
        '"Mouse Sensitivity"':'"滑鼠靈敏度"', '"Move Forward:"':'"向前："',
        '"Move Backward:"':'"向後："', '"Move Right:"':'"向右："',
        '"Move Left:"':'"向左："', '"Move Up:"':'"向上："',
        '"Move Down:"':'"向下："', '"Boost:"':'"加速："'
    },
    "global_speed_changer.cpp": {
        '"Global Speed Changer"':'"全域速度"', '"Enable"':'"啟用"', '"Speed"':'"速度"'
    },
    "hide_ui.cpp": {
        '"Hide UI"':'"隱藏介面"', '"Enable"':'"啟用"'
    },
    "menu_settings.cpp": {
        '"Menu Settings"':'"介面設定"', '"Menu Key:"':'"選單快捷鍵："',
        '"Custom Menu Scale"':'"自訂介面縮放"', '"Value"':'"縮放比例"'
    },
    "noclip.cpp": {
        '"Noclip"':'"無視地形"', '"Enable"':'"啟用"',
        '"Speed"':'"移動速度"', '"Use Camera Direction"':'"使用鏡頭方向"'
    },
    "peeking.cpp": {
        '"Peeking"':'"防止角色虛化"', '"Enable"':'"啟用"'
    }
}

FONT_MARKER = 'ImGui::GetIO().IniFilename = NULL;'
FONT_BLOCK = r'''
        {
            ImGuiIO& io = ImGui::GetIO();
            ImFontConfig cfg;
            cfg.OversampleH = 2;
            cfg.OversampleV = 2;
            const ImWchar* ranges = io.Fonts->GetGlyphRangesChineseFull();

            const char* fonts[] =
            {
                "C:\\Windows\\Fonts\\msjh.ttc",
                "C:\\Windows\\Fonts\\msyh.ttc"
            };

            for (const char* path : fonts)
            {
                if (GetFileAttributesA(path) != INVALID_FILE_ATTRIBUTES)
                {
                    if (io.Fonts->AddFontFromFileTTF(path, 18.0f, &cfg, ranges))
                        break;
                }
            }
        }
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()

    if not (repo / "Pipsi-HSR.sln").exists():
        raise SystemExit("Pipsi-HSR.sln not found")

    backup = repo / "_ui_redesign_backup"
    backup.mkdir(exist_ok=True)

    replacements = {
        "menu.cpp": MENU_CPP,
        "imgui_user.cpp": IMGUI_USER_CPP,
        "imgui_user.h": IMGUI_USER_H,
    }

    for name, content in replacements.items():
        p = repo / name
        if p.exists() and not (backup / name).exists():
            shutil.copy2(p, backup / name)
        p.write_text(content, encoding="utf-8")
        print("replaced", name)

    for name, mapping in TRANSLATE.items():
        p = repo / name
        if not p.exists():
            continue
        if not (backup / name).exists():
            shutil.copy2(p, backup / name)
        text = p.read_text(encoding="utf-8")
        for old, new in mapping.items():
            text = text.replace(old, new)
        p.write_text(text, encoding="utf-8")
        print("translated", name)

    d3d = repo / "d3d11_overlay.cpp"
    if d3d.exists():
        if not (backup / "d3d11_overlay.cpp").exists():
            shutil.copy2(d3d, backup / "d3d11_overlay.cpp")

        text = d3d.read_text(encoding="utf-8")
        if "GetGlyphRangesChineseFull" not in text:
            if FONT_MARKER not in text:
                raise SystemExit("font insertion point not found")
            text = text.replace(FONT_MARKER, FONT_MARKER + "\n" + FONT_BLOCK, 1)
            d3d.write_text(text, encoding="utf-8")
            print("added zh-TW font")

if __name__ == "__main__":
    main()
