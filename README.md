# Pipsi-HSR 繁體中文在地化分支

本專案專注於 **繁體中文化** 維護，完整保留原版介面排版、選單架構與按鍵操作邏輯，不再套用先前的深藍玻璃自訂 UI。

---

## 雲端自動編譯 (GitHub Actions)

1. 前往倉庫上方的 **Actions** 分頁。
2. 在左側清單選擇 **Build Pipsi-HSR zh-TW UI**。
3. 點擊右側的 **Run workflow**。
4. 等待編譯完成（出現綠色勾勾圖示）。

編譯完成後，進入該次工作流程頁面的 **Artifacts** 區塊下載：

`Pipsi-HSR-zh-TW-UI-ready`

### 封裝內容物
- `Cheat.dll`
- `README.txt`
- `SHA256.txt`

### 安裝方式
將解壓縮得到的 `Cheat.dll` 覆蓋至原本的 `GlobalSR` 資料夾即可。  
> ⚠️ **建議**：替換前請先手動備份原版 DLL 檔案。

---

## 修改項目說明

- **保留原生操作**：維持原版 UI 排版、ImGui 元件架構與 `INSERT` 鍵選單喚醒邏輯。
- **繁體中文在地化**：全域功能名稱、各項設定與操作說明中文化。
- **字型相容性處理**：整合 Windows 原生中文字型載入，避免介面出現字元遺失或方框。
- **基礎編譯修正**：僅保留建置必要的 AnimeSDK 相容性修正代碼。

---

## 鳴謝與致敬 (Credits)

- 本專案基於 [Z4ee/Pipsi-HSR](https://github.com/Z4ee/Pipsi-HSR) 進行繁體中文化維護。
- 特別感謝原作者 **Z4ee** 的開源貢獻。

## 授權條款 (License)

本專案遵循 [MIT 授權條款](LICENSE) 進行分發與修改。
