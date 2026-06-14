# X光擺位 3D 模擬器 — 交接文件

> 最後更新:2026-06-14(Caldwell view + 示意圖風格化)

## 1. 這專案在做什麼

放射擺位教學網站(`femhmedimage.org` 放射技術指引,本機 `..\Xray\`)需要大量擺位示意照。真人拍攝有隱私 / 尷尬部位 / 找不到模特兒的痛點(127 筆中 47 筆缺照,多為骨盆 / 髖 / 腹部 / 胸部 / 嬰兒)。本工具用 three.js + disfigure(平滑人偶,MIT)在瀏覽器模擬 X 光攝影室與可擺姿勢人偶,截圖 PNG 給主站用。

## 2. 現在進度到哪

- ✅ MVP 完成:攝影室、立式攝影架(板高可調)、攝影檯 + 檯面偵檢板、天吊球管(x/z/高/俯仰/旋轉)、光野錐 + 十字 + spotlight 投影、定位雷射線、SID 即時讀數
- ✅ 人偶:mannequin.js Female,50 個滑桿(全身位置 + 頭頸/軀幹/四肢關節)
- ✅ 場景 preset 2 個:cspine-lateral(立位,SID 180)、ankle-ap(檯上坐姿,SID 100)
- ✅ 截圖 PNG / 匯出匯入設定 JSON / 白底切換
- ✅ 美術 pass:示範圖風格(灰肢體 + 藍衣人偶、粉紅雷射、灰藍場景、柔光)
- ✅ 設備細節 pass:膠囊形球管殼 + 圓角準直儀 + 把手 + 接頭(yoke 掛 rig 不隨俯仰轉)、拱頂壁架殼(ExtrudeGeometry)、圓邊檯面(RoundedBoxGeometry)
- ✅ **disfigure 平滑人偶實驗版 `disfigure.html`**(2026-06-12 spike 成功):無縫平滑身體 + **原生腳趾/手指**,MIT 授權,質感 = 使用者的 3D 擺位示範圖
- ✅ **index.html 已全面遷移到 disfigure 引擎**(2026-06-13):完整滑桿 UI(54 個,含 disfigure 關節路徑 head/chest/waist/arm/elbow/wrist/leg/knee/ankle/foot 的 x/y/z)+ 雷射 gap/skin + 體表十字(含 flat 模式給仰臥)+ 手指 path 走 JSON 匯出入。男性人偶 Man(1.73)
- ✅ **使用者已定稿 2 個缺照 view**(2026-06-14):
  - **pelvis-ap**(仰臥):雙腿內旋 18°(thigh.y 同號)、CR 對 ASIS 下 5cm、SID 102、光野 35×43;使用者選低側斜構圖
  - **skull-stenvers**(俯臥)+ **skull-stenvers-arcelin**(仰臥替代):面轉對側 head.y 45、CR 入點顳/耳(使用者調 tube x=-0.12,z=0.57)、SID 100、光野 20×19、球管機身視覺斜 12°(與光束解耦)、檯面光野關閉(surfaceField:0)。**官方參考圖 `samples/stenvers_final.png` = 使用者最終截圖**
  - **skull-caldwells**(直立 PA,2026-06-14):面向壁架 rotY 180、**點頭 head.x 15°**(下巴內收、前額朝板)、fig z=-1.55 貼板、球管 **h=1.76 真斜 8° caudad(pitch 82)**、SID 100、光野 20×24。**示意圖風格**:`showCross:0` + `surfaceField:0` + 側面 profile 相機(對照 `..\Xray\caldwell view示意圖.png`)。CR 真斜(非假機身斜),想要完整 SOP 15° 把 pitch 調 75
  - **cspine-swimmers**(立位側位,2026-06-14):rotY 90 側位(矢狀面平行板)、**近板側(左)手臂 l_arm.z 100 高舉過頭、遠側 r_arm.z -72 下壓**(分開兩肩露 C7-T1)、head.x -12 下顎抬、fig z=-1.42、球管 z=-0.64 h=1.44 pitch 90 對 C7-T1、**SID 102**、光野 16×30 窄高。Twining 法。**這個 view 要十字+光野框畫在皮膚上**(showCross 1、surfaceField 0 板上不畫)。⚠️ 光野沿光束打到所有表面(手、板)→ 用 `paintGate {z, r, followBeam:1}` 範圍閘(球體+**facing 朝向閘**:`normalWorld·toFocal` 只畫朝球管的面,不繞到背板側/另一側),只在球管軸附近(頸 C7-T1)畫、排除舉起的手;followBeam=中心跟著 tube.x/h 自動移。r 要夠小(0.14)才不碰到旁邊手臂。光束 x 要對準頸部(=fig.x)否則只擦到邊緣很淡。**陰影**:預設 sun 從上方斜下打,高的手影會落到頭高度(錯)→ 用 `beamShadow:1` 讓 sun 對齊光束方向(水平),頭影在頭高、手影投到板頂以上。directional light 在無限遠擺不到球管出口,球管會擋光投自身陰影 → **球管整組 `tubeRig.traverse castShadow=false`**(球管陰影不重要),只留人偶投影。⚠️ **applyPreset 只複製白名單欄位**(fig/tube/ws/det/room/occl/surfaceField/showCross/paintGate/beamShadow)——加新的 per-preset 自訂欄位一定要在 applyPreset 補一行複製到 S,否則靠殘留狀態僥倖、fresh load 會失效。⚠️ 截圖時 embedded preview canvas 會變 1px → 先 `renderer.setSize(960,720,false)+camera.aspect` 再拍(真實瀏覽器正常)
  - **waters-view**(直立 PA 頭後仰,2026-06-14):面向壁架 rotY 180、**軀幹前傾分散 chest.x 6 + waist.x 9**(臉到板而胸口不陷,見下「臉貼板」坑)+ **頭微後仰 head.x -4**(下巴上抬、鼻尖離板≈1cm,SOP OML 37°/MML 垂直板)、fig z=-1.52、球管 **h=1.52 pitch 90 垂直入射 acanthion(鼻基)**、SID 100。與 Caldwell 共用示意圖風格(showCross/surfaceField 0、側面 profile)。防雷:仰角過大/不足是最常見不良片(使用者於工具內調定:胸彎6/腰彎9/點頭-4)
- ⏳ 待辦:批次產「已 reviewed 缺照」其餘 view → 47 筆全補。臥位/頭顱姿勢 workaround 已記錄(見下)
- **2026-06-14 全域風格化**:① 膚色基底改暖色淺咖啡 `#c9b29a`(原 `#bfc4cb`,影響所有 view);② 病人服上衣下緣延伸到與短褲相接(torsoBand 下緣 0.70-0.80),腰部不再露膚 = 連續一件式;③ 新增 `uShowCross` uniform + per-preset `showCross` 旗標(0=只留柔光罩不畫十字),示意圖風格用

## 3. 架構速覽

- 單檔 `index.html`(~870 行),無 build step;importmap 載 three@0.184(WebGPU)+ disfigure(CDN gh)。舊 mannequin.js + three 0.170 版見 git 歷史
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
- **WebGPU SpotLight 陰影不生效**(three 0.184 + 此渲染路徑):「紅色光源+狹縫」做雷射投影行不通,遮光板擋不住光。定位雷射改用視覺等效法:牆線拆 L/R 兩段留身體陰影缺口 + per-preset 體表紅線段(`laser: {gapFrom, gapTo, skin}`)。準直儀十字遮光條的十字陰影同理可能無效(spot shadow),光野亮區是有的
- **準直儀光野 spotlight 照在人偶身上要夠亮**:intensity 120+、penumbra 0.22,不然只看得到牆上的亮斑
- 🔑 **THREE.SpotLight 預設 position=(0,1,0) 不是原點**:掛進 beamGroup 後光源比準直儀高 1m,光池變大變淡。一定要 `spot.position.set(0,0,0)`(2026-06-13 抓到,新舊兩版都中過)
- ~~仰臥 rotZ=90 姿勢參數速查~~(**已棄用**,被「轉房間」架構取代,留作歷史:rotZ 旋轉人偶會讓左臂 -115 才平貼、leg.y 扭爆等;rotY+rotZ 組合會讓人偶整個散掉)
- 🔑🔑 **臥位的正解:「人不動,轉房間」(2026-06-13 重構)**:人偶永遠站立(關節語意 100% 正常),臥位 view 設 `room: {lie:1, ox, oy, oz}` 讓 ROOMG(房間+設備+雷射全在裡面)旋轉 90 度 + 相機 up 軸跟轉 → 圖面上人躺在檯上
  - LIE_M 基底:room x→world -y(體軸沿檯)、room y→world +z(檯面法線=肚皮朝向)、room z→world -x
  - 座標換算:world_x = -z_room + ox / world_y = -x_room + oy / world_z = y_room + oz
  - 模板:fig `{x:0, z:0.87, y:0, rotY:0}`(站立,背貼檯面),room `{lie:1, ox:0.55, oy:1.47, oz:0}` → 頭朝room -x、骨盆在 room x≈0.55、踝在 ≈1.38
  - 相機 preset 一律寫房間座標,applyPreset 自動 localToWorld + up 軸切換
  - SID 改在房間座標解析計算(S 的數值 + Euler YXZ),不依賴 world position
  - 內建 sun(DirectionalLight)放在 ROOMG 內隨房間轉,disfigure 的世界光壓到 0.35 → 臥位圖光影方向仍自然
  - 站立姿勢的足內旋 `leg.y ±12`、雙臂 `arm.z -72` 全部正常可用
- **spotlight 光野強度:預設 30**(UI 有「光線」滑桿群可調主光/環境光/光野;120 在 SID 75cm 會過曝)
- **病人服 = TSL colorNode 高度帶**(模型空間 y,disfigure rest=T-pose):上衣 torsoBand y 0.70-1.60(下緣已降到接短褲)× sideIn |x|<0.34 × 圓領口挖空;短袖 sleeve(armX |x| 0.28-0.37 沿手臂 = 收到 proximal humerus 1/3;橫截面用**徑向** armR²=(y-1.46)²+z² 圓管不要用水平 y 帶。**🔑 手臂 rest 中心線實測在 (y≈1.46, z≈-0.08),手臂 z 全為負(-0.14~-0.03)**(用 scene.traverse 找 12089 頂點的 body mesh、對 |x|0.26-0.6 分箱量 cy/cz 得到)。所以圓管 armR2 要 `(y-1.46)²+(z+0.08)²`、前後分界 zFrac 要 `smoothstep(-0.12,-0.04,z)` 都以 -0.08 為中心 —— 若用 z=0 圓管只罩到前緣、後側漏掉、前後滑桿都只動到前面(踩過)。前後外緣 |x| 截斷各一 uniform(`uSleeveFront`/`uSleeveBack`)依 zFrac 內插。**UI「病人服(袖長)」兩條滑桿**可即時調,調好回填預設值);短褲 y 0.66-1.08 全寬;點點花紋 sin 網格。gown 色 `#7791ba`、膚色 `#c9b29a`。disfigure 的 `dress()` 在此版是 silent no-op 別浪費時間
- 🔑 **雷射/十字/光野「畫在皮膚上」(TSL,2026-06-13)**:同一個 colorNode 接著做三層 — ① 光野亮區:positionWorld 經 `uBeamInv`(beamGroup.matrixWorld 逆矩陣 uniform)轉光束局部座標,錐內(線性放大的 field 範圍)加暖色;② 十字:光束局部 |x|或|z| < 3.5mm 變暗;③ 雷射:`|positionWorld.y - uLaserY| < 4.2mm` 且 `normalWorld.z > -0.1`(只畫面向雷射源的表面)染紅。**任何視角都貼著身體輪廓**,完全取代會浮空的貼片(crossSkin/laserSkin 已刪),十字也不再需要逐 preset 手動標位。uniform 在 applyAll 末端更新(記得 `beamGroup.updateWorldMatrix` 後再 invert)。牆上雷射線仍是 L/R 兩段幾何(平面上貼片不會穿幫),gap 機制保留
- **光野視覺規格(對照 Skull AP 實拍)**:柔邊「矩形」暖光 + 寬 ~15mm 軟邊十字陰影。承光面(牆/板/檯/偵檢板)用 `beamLambert()`(MeshLambertNodeMaterial + 共用 beamPaint TSL 鏈)。**spotlight 預設 0**(只當氛圍光,由滑桿開)。⚠️ 半透明光錐 DoubleSide 多層疊加會變白盤 → FrontSide + opacity 0.07
- **標準視角按鈕**(斜45/正面/側面/正上)方向用房間座標經 ROOMG 轉換,臥位也正確;正上方刻意偏斜 (0.45,1,0.45) 避開球管;臥位時「側面」≈ 從腳底看(房間座標語意),要更名再說
- **視角滑桿**(水平角/垂直角/距離):球面角繞 controls.target,房間座標;滑鼠 orbit 後經 controls change 事件回寫滑桿
- **定位雷射已整組移除**(2026-06-13 使用者決定):視覺主角 = 方形光野+十字。git 歷史有完整實作(牆線 gap + shader 皮膚紅線)要復活就 revert
- 🔑 **disfigure 關節「軸位圖」(實測,鎖死軸寫入會被靜默吃掉,getJoint 讀回 0)**:
  - leg: x屈髖 z外展(**y 鎖死**)/ **thigh: 只有 y**(大腿內外旋)/ knee: x z / **shin: 只有 y**(小腿旋轉)/ ankle: x z / foot: x
  - arm: x y z 全活 / **elbow: 只有 y**(屈肘)/ **forearm: 只有 x**(旋前旋後)/ wrist: y z(x 鎖死)
  - head/chest/waist/torso: 全活。新增滑桿前先 `figure[part][axis]=33` 寫入讀回驗證
  - **左右關節內建鏡像:對稱動作用「同號」**(兩腿內旋 = l_thigh.y 與 r_thigh.y 都 -18;雙臂垂放 = 都 -72)。不要像一般骨架那樣左右反號
- 🔑🔑 **人偶完全不吃場景燈**(2026-06-14 證實):任何 AmbientLight / DirectionalLight / cameraLight 改 intensity 對人偶零效果(變形綁在材質內,材質不能換)。俯臥/側臥時背光面會全黑。**解法:material.emissiveNode = colorNode × wrap-diffuse 自照亮**(`shade = (normalWorld·Ldir·0.5+0.5)·0.5+0.42`,Ldir≈(0.3,0.85,0.45))→ 任何體位都明亮、又有立體感。改 emissiveNode 後站姿/仰臥/俯臥全部一致變好。**別再花時間調燈去救人偶亮度**
- **俯臥(prone)= 仰臥 preset 把 fig.rotY 設 180**(臉朝下);頭轉 = head.y;Stenver's/Arcelin 已用此法。scene.background 改色無效(disfigure World 自管 clear)
- 🔑 **「臉貼板」類直立頭顱 view 的胸口陷板問題(2026-06-14)**:挺直站面對立架時**胸廓比臉更前凸**,硬把臉推到板會讓胸口陷入板內。**解法 = 軀幹前傾 `waist.x +10~14°`(骨盆後、上身靠向立架)+ 人偶 z 後移留前傾空間 + 補調 head.x**(前傾會把頭一起帶前,要多給後仰/點頭補回 SOP 頭角)。因為頭在腰樞紐上方比胸口高 → 前傾每度頭前移 > 胸口,臉先到板而胸口留後方傾斜。Waters 已用(waist.x 10、head.x -26)。Caldwell 同理(前額貼板)可加。**waist.x 正=前傾、負=後仰**
- ⚠️ **WebGPU 截圖偶爾回傳舊幀**:reload 後第一次要等 ~4s,且 renderOnce 連呼 3 次中間 sleep 50ms 才穩;懷疑卡幀就 location.reload()

## 5. 接手者 cheatsheet

- 本機跑:`python -m http.server 8765 --directory .`;preview launch config 在 `..\Xray\.claude\launch.json`(名稱 sim3d)
- 截圖管道:背景跑 `python tools/shot_server.py 8766` → preview_eval 裡 render + POST → `shots/*.png` 直接 Read
- 加 preset:複製 `PRESETS` 一筆,joints 用路徑語法;先在 console 用 `__sim.setJoint()` / `__sim.S` 調好再回填
- 主站缺照清單:見 `..\Xray\positions.json`(47 筆 `images.positioning_photo` 為空者);出圖優先序:已 reviewed 10 筆 → 骨盆/髖/腹部隱私群 → 其餘
- 部署:push main → GitHub Pages(repo Settings → Pages 啟用 main / root)
