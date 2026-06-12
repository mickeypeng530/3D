# X光擺位 3D 模擬器 — 交接文件

> 最後更新:2026-06-12(MVP 完成)

## 1. 這專案在做什麼

放射擺位教學網站(`femhmedimage.org` 放射技術指引,本機 `..\Xray\`)需要大量擺位示意照。真人拍攝有隱私 / 尷尬部位 / 找不到模特兒的痛點(127 筆中 47 筆缺照,多為骨盆 / 髖 / 腹部 / 胸部 / 嬰兒)。本工具用 three.js + mannequin.js 在瀏覽器模擬 X 光攝影室與可擺姿勢人偶,截圖 PNG 給主站用。

## 2. 現在進度到哪

- ✅ MVP 完成:攝影室、立式攝影架(板高可調)、攝影檯 + 檯面偵檢板、天吊球管(x/z/高/俯仰/旋轉)、光野錐 + 十字 + spotlight 投影、定位雷射線、SID 即時讀數
- ✅ 人偶:mannequin.js Female,50 個滑桿(全身位置 + 頭頸/軀幹/四肢關節)
- ✅ 場景 preset 2 個:cspine-lateral(立位,SID 180)、ankle-ap(檯上坐姿,SID 100)
- ✅ 截圖 PNG / 匯出匯入設定 JSON / 白底切換
- ⏳ 待辦:更多 preset(目標:主站 47 筆缺照 view)、男性 / 兒童人偶切換、姿勢直接拖曳(目前只有滑桿)、preset 存進 localStorage 或檔案庫

## 3. 架構速覽

- 單檔 `index.html`(~600 行),無 build step;importmap 載 three@0.170 + mannequin-js@5(CDN)
- 場景單位 = 公尺(啟動時量人偶 bbox 校正 `M` 比例;`mm(公尺)` 轉世界單位;地面 `GL = getGroundLevel()`)
- 座標:後牆 z=-1.9(壁架板面 z=-1.78)、左牆 x=-2.2、攝影檯心 (0.75, 0.55)、檯面高 0.74
- 球管:`tubeRig`(x/z + yaw)→ `tubeHead`(高度 + pitch;pitch 0=朝下、90=朝後牆)→ `beamGroup`(光束沿局部 -Y)
- 狀態都在 `S` 物件;`applyAll()` 套用;preset 在 `PRESETS`;關節用 `"part.prop"` 路徑(如 `r_ankle.bend`)
- `window.__sim` 暴露 debug 介面(console 調參 / 自動截圖用)

## 4. 常見坑 / 防雷

- **嵌入式 preview 初始視窗 0x0** → createStage 後要 `fitViewport()` 強制 resize(已內建)
- **figure.position.y 是髖根節點不是腳底**:站立時 feet=GL、pos.y≈0.16;坐檯面(0.74m)只要 y 偏移 ≈ -0.03,不是 +0.74
- **mannequin turn=0 面向 +x**;側位(肩貼後牆板)用 turn 0/180,AP 面向球管(+z)用 -90
- **SID 從 tubeHead(焦點)起算**,光束視覺長度從準直儀出口(focal -0.24m)起算,別混用
- **preview_screenshot 工具會 timeout**:用 `tools/shot_server.py`(port 8766)+ `__sim.renderer.render + toDataURL + fetch POST` 自製截圖管道
- 全形標點字面值在本機檔案會被收斂成半形 → UI 文案避免依賴全形標點(同 Xray 專案鐵則)

## 5. 接手者 cheatsheet

- 本機跑:`python -m http.server 8765 --directory .`;preview launch config 在 `..\Xray\.claude\launch.json`(名稱 sim3d)
- 截圖管道:背景跑 `python tools/shot_server.py 8766` → preview_eval 裡 render + POST → `shots/*.png` 直接 Read
- 加 preset:複製 `PRESETS` 一筆,joints 用路徑語法;先在 console 用 `__sim.setJoint()` / `__sim.S` 調好再回填
- 主站缺照清單:見 `..\Xray\positions.json`(47 筆 `images.positioning_photo` 為空者);出圖優先序:已 reviewed 10 筆 → 骨盆/髖/腹部隱私群 → 其餘
- 部署:push main → GitHub Pages(repo Settings → Pages 啟用 main / root)
