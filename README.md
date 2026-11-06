# yucs 教學入口

[開啟教學入口](https://yuyu881.github.io/teaching/)

每個科目與教材卡片都在 `catalog.json` 維護。調整同一科目的卡片順序時，移動該科目 `materials` 陣列中的項目。新增教材時填寫顯示名稱、簡介及已公開的 GitHub Pages 網址。

桌面每列四張等大的卡片。平板改為兩欄，手機改為單欄。科目切換由頁面處理，教材卡片會隨所選科目更新。

GitHub Actions 會在每次建置時設定 `DEPLOYED_AT`，再以 `build.py` 產生公開頁面。頁尾時間換算為 Asia/Taipei，重新整理頁面不會改變。
