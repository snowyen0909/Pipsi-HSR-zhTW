from pathlib import Path
import argparse, shutil

TRANSLATE = {
    "menu.cpp": {
        '"Adventure"': '"探索"',
        '"Battle"': '"戰鬥"',
        '"Visuals"': '"視覺"',
        '"Misc"': '"其他"'
    },
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
    ap = argparse.ArgumentParser(description="Pipsi-HSR Traditional Chinese localization patch")
    ap.add_argument("repo", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()

    if not (repo / "Pipsi-HSR.sln").exists():
        raise SystemExit("Pipsi-HSR.sln not found")

    backup = repo / "_zh_tw_backup"
    backup.mkdir(exist_ok=True)

    # Compatibility fix for current AnimeSDK dump.
    battle_speed = repo / "battle_speed_changer.cpp"
    if battle_speed.exists():
        text = battle_speed.read_text(encoding="utf-8")
        if "_this->Field_2_4" in text:
            if not (backup / "battle_speed_changer.cpp").exists():
                shutil.copy2(battle_speed, backup / "battle_speed_changer.cpp")
            text = text.replace("_this->Field_2_4", "_this")
            battle_speed.write_text(text, encoding="utf-8")
            print("patched AnimeSDK compatibility")

    # Only translate visible strings. Keep the original UI/layout and input logic.
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

    # Load a Windows CJK font so Traditional Chinese glyphs render correctly.
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
            print("added Traditional Chinese font support")

if __name__ == "__main__":
    main()
