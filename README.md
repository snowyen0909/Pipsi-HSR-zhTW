# Pipsi-HSR 繁體中文化

這個 Repository 現在只做 **繁體中文化**，不再修改原本 UI 版面、選單結構或按鍵邏輯。

## 雲端編譯

1. 點上方 **Actions**
2. 左邊選 **Build Pipsi-HSR zh-TW UI**
3. 點 **Run workflow**
4. 等待綠色勾勾

完成後，在該次執行頁面的 **Artifacts** 下載：

`Pipsi-HSR-zh-TW-UI-ready`

裡面會有：
- `Cheat.dll`
- `README.txt`
- `SHA256.txt`

把新的 `Cheat.dll` 替換到原本的 `GlobalSR` 資料夾即可。建議先備份原版 DLL。

## 目前只做這些修改

- 原版 UI 版面完全保留
- 原版 INSERT 選單按鍵邏輯保留
- 原版 ImGui 元件保留
- 將功能名稱與常用操作文字翻成繁體中文
- 加入 Windows 中文字型載入，避免中文變成方框
- 保留必要的 AnimeSDK 編譯相容修正

不再套用之前的深藍玻璃新版 UI。
