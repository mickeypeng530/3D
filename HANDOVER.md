# X光擺位 3D 模擬器 — 交接文件

> 最後更新:2026-06-12(MVP 完成)

## 1. 這專案在做什麼

放射擺位教學網站(`femhmedimage.org` 放射技術指引,本機 `..\Xray\`)需要大量擺位示意照。真人拍攝有隱私 / 尷尬部位 / 找不到模特兒的痛點(127 筆中 47 筆缺照,多為骨盆 / 髖 / 腹部 / 胸部 / 嬰兒)。本工具用 three.js + mannequin.js 在瀏覽器模擬 X 光攝影室與可擺姿勢人偶,截圖 PNG 給主站用。

## 2. 現在進度到哪

- ✅ MVP 完成:攝影室、立式攝影架(板高可調)、攝影檯 + 檯面偵檢板、天吊球管(x/z/高/俯仰/旋轉)、光野錐 + 十字 + spotlight 投影、定位雷射線、SID 即時讀數
- ✅ 人偶:mannequin.js Female,50 個滑桿(全身位置 + 頭頸/軀幹/四肢關節)
- ✅ 場景 preset 2 個:cspine-lateral(立位,SID 180)、ankle-ap(檯上坐姿,SID 100)
- ✅ 截圖 PNG / 匯出匯入設定 JSON / 白底切換
- ✅ 美術 pass:示範圖風格(灰肢體 + 藍衣人偶、粉紅雷射、灰藍場景、柔光)
- ✅ 設備細節 pass:膠囊形球管殼 + 圓角準直儀 + 把手 + 接頭(yoke 掛 rig 不隨俯仰轉)、拱頂壁架殼(ExtrudeGeometry)、圓邊檯面(RoundedBoxGeometry)
- ✅ **disfigure 平滑人偶實驗版 `disfigure.html`**(2026-06-12 spike 成功):無縫平滑身體 + **原生腳趾/手指**,MIT 授權,質感 = 使用者的 3D 擺位示範圖。兩個 preset(cspine-lateral 立位 / ankle-ap 仰臥)已驗證
- ⏳ 待辦:決定是否把 index.html 全面遷移到 disfigure(建議:是,UI 滑桿照搬 + 關節路徑換名)、臥位左臂軸向怪癖解法、更多 preset(目標:主站 47 筆缺照 view)、男性 / 兒童人偶切換

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

### disfigure 實驗版(disfigure.html)專屬坑
- **GLB 模型要從 gh CDN 載**:`cdn.jsdelivr.net/gh/boytchev/disfigure@main/...`;npm 包沒含 assets,woman.glb 會 404
- **改關節後必須 `figure.update()`** 才會生效(動畫迴圈死掉時尤其);關節是 `figure.l_arm.x/y/z` 度數
- **場景必須補 AmbientLight**(disfigure 預設只有方向光,人偶背光面全黑)
- **嵌入式 preview 的 rAF 不會跑**(0 次/500ms)→ World 動畫迴圈死的,自動截圖要手動 `renderer.renderAsync()`;真實瀏覽器正常
- **躺臥姿勢**:旋轉必須下在 figure 本體(包 parent Group 會被變形 shader 無視);`rotation.set(0,0,90°)` = 仰臥頭朝 -x。**根旋轉後左臂的軸語意會翻轉**(v0.x 怪癖,l_arm.z 變成指天),右臂正常 — 待解
- **`torso.x = ±90` 會讓人偶塌縮消失**,別用它放倒身體
- **`figure.frustumCulled = false`**:GPU 變形不更新 bounds,大姿勢會被誤剔除
- **髖屈 55-90 度之間不穩**(模糊變形,腿會穿檯面或翹天)→ 檯上 view 優先用仰臥,不用長坐姿

## 5. 接手者 cheatsheet

- 本機跑:`python -m http.server 8765 --directory .`;preview launch config 在 `..\Xray\.claude\launch.json`(名稱 sim3d)
- 截圖管道:背景跑 `python tools/shot_server.py 8766` → preview_eval 裡 render + POST → `shots/*.png` 直接 Read
- 加 preset:複製 `PRESETS` 一筆,joints 用路徑語法;先在 console 用 `__sim.setJoint()` / `__sim.S` 調好再回填
- 主站缺照清單:見 `..\Xray\positions.json`(47 筆 `images.positioning_photo` 為空者);出圖優先序:已 reviewed 10 筆 → 骨盆/髖/腹部隱私群 → 其餘
- 部署:push main → GitHub Pages(repo Settings → Pages 啟用 main / root)
