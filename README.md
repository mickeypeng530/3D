# X光擺位 3D 模擬器

放射攝影擺位教學用 3D 模擬工具。在瀏覽器中模擬 X 光攝影室(球管、準直儀光野、定位雷射、立式攝影架、攝影檯、偵檢板)與可調姿勢的 3D 人偶,用來產生擺位示意圖,取代真人擺位拍照。

姊妹專案:[亞東醫院影像醫學科放射技術指引](https://femhmedimage.org)(本工具產出的截圖供該站使用)。

## 使用

直接開啟 GitHub Pages:`https://mickeypeng530.github.io/3D/`

- 滑鼠左鍵旋轉視角、右鍵平移、滾輪縮放
- 右側面板:選場景預設 → 微調關節 / 球管 / 光野 → 截圖 PNG
- 「匯出設定」會把目前姿勢 + 設備參數存成 JSON,之後可匯入重現

## 技術

- 單檔 `index.html`,無 build step,CDN 載入
- [three.js](https://threejs.org) 0.170 + [mannequin.js](https://github.com/boytchev/mannequin.js) 5.x(可擺姿勢人偶)
- 場景單位 = 公尺;SID 即時計算(焦點至偵檢板)

## 開發

```
python -m http.server 8765 --directory .
# 開 http://localhost:8765
```

`tools/shot_server.py`:開發用截圖接收 server(配合 console 的 `window.__sim` debug 介面)。

## License

GPL-3.0(因使用 mannequin.js,其授權為 GPL-3.0)
