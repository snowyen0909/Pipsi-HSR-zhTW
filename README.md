# Pipsi-HSR 繁中 UI 雲端編譯

這個 Repository 會使用 GitHub Actions 的 Windows runner 自動編譯，所以你的電腦不用安裝 Visual Studio / C++。

## 怎麼開始

1. 點上方 **Actions**
2. 左側選 **Build Pipsi-HSR zh-TW UI**
3. 點 **Run workflow**
4. 等待綠色勾勾

## 下載成品

完成後點進那次執行，在頁面下方 **Artifacts** 下載：

`Pipsi-HSR-zh-TW-UI-ready`

解壓後會得到：
- `Cheat.dll`
- `README.txt`
- `SHA256.txt`

把新的 `Cheat.dll` 放回原本 `GlobalSR` 資料夾，建議先把舊版改名成 `Cheat.original.dll` 備份。

## 自動流程

```text
下載 Pipsi-HSR 原始碼
→ 套用繁體中文 UI Redesign
→ MSVC Release / x64 編譯
→ 上傳 Cheat.dll Artifact
```

目前 UI 方向：
- 深藍玻璃介面
- 金色點綴
- 左側導航
- 戰鬥 / 探索 / 視覺 / 其他
- 卡片式功能區
- 繁體中文
