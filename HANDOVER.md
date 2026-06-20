# X光擺位 3D 模擬器 — 交接文件

> 最後更新:2026-06-20(補回 sw34-40 紀錄 + §6 新 view 製作 SOP;線上 build = sw40)

## sw34-47:骨盆群 + Stenvers 定版 + Dunn(90/45)+ 陰影控制 + pose 片段鈕(2026-06-15~20)
- **sw47 新 `dunn-45`(Modified Dunn)preset**:= 標準 dunn-view 只把髖屈 90→45(`leg.x 45`),其餘全同(外展 20、交疊手臂、tube/CR/SID、surfaceField0、beamShadow1)。SOP 來源 positions.json dunn-view variants(髖屈 45°,無法達 90° 時採此)。骨盆不動 → CR/tube 同 dunn-view。**髖屈 45° < 55° 在 disfigure 穩定區,腿不糊**(比 Dunn 90 乾淨)。起始姿勢,待使用者微調膝/足角度。
- **sw46 「🙆 雙手交疊」pose 片段鈕**:一鍵把雙臂套成屈肘交疊胸前(只動手臂全部可動軸,不碰腿/軀幹/球管),做骨盆等 view 時快速套手。機制 = `ARM_POSES.fold` 字典 + `applyArmPose(name)`(setJoint 每軸 → applyAll → syncSliders)。**要加新 pose 片段就往 `ARM_POSES` 加一筆 + 一顆鈕。** 值來源 = pelvis-frog/dunn 定版手臂。
- **sw44-45 dunn-view 定版**:sw44 `surfaceField 0`(檯面光野關);sw45 雙臂改交疊胸前(沿用 pelvis-frog 手臂數據)。複製數值原封回填。
- 🔑 **sw43 根除「第二道淡影」(綠色假腿影)**:disfigure 內建世界光 `light`(我們壓到 0.25)+ `cameraLight` 原本 **castShadow 沒關** → 它們在世界座標固定不動,各投一道淡影。Dunn 抬腿時這道固定淡影看起來像「第二雙伸直的腿」(綠),且**不受 `shadowLift` 影響**(shadowLift 只動 ROOMG 內的 `sun`)——使用者精準回報「陰影光角動的是紅、淡綠不變」才定位到。**解法**:`light.castShadow=false; cameraLight.castShadow=false`([index.html:351](index.html))→ 全場只剩 `sun` 一道可控影。⚠️ 教訓:任何 fill/ambient 性質的光都要 `castShadow=false`,只留主光投影,否則多重淡影疊加很難 debug。
- **sw42 陰影控制滑桿**(UI「光線」群):①「**陰影濃度**」→ `sun.shadow.intensity`(0=無影 1=全黑,預設 0.4)。②「**陰影光角(臥位)**」→ `S.tube.shadowLift`(per-view,-12~12)。⚠️ `shadow.radius` 柔邊在 WebGPU **無效**(已移除)——所以 sw41 只把綠條變淡、形狀沒柔化(使用者回報「綠色沒變」)。真正消綠條靠 `shadowLift`:把 sun 往房間 z(檯面法線)推,beamShadow 的直射掠射→斜射,抬腿長影收短。`shadowLift` 放在 `S.tube` 內(applyPreset `Object.assign(S.tube,p.tube)` 自動帶;已加 `S.tube.shadowLift=0` 歸零行)。**使用者要自己拉滑桿定值再回填 preset。**
- **sw41 全域陰影柔化**:`sun.shadow.intensity 0.4`(WebGPU 有吃)。場景只有一盞硬 `sun` 投影、無補光 → 硬黑影。Dunn 因 sw40 `beamShadow` 把 sun 變近乎掠射檯面,抬起的腿被拖出又長又硬的條狀影(像第二雙伸直的腿)。降濃度讓紅(彎腿影)變淡;綠(掠射長條)的形狀要靠 sw42 `shadowLift` 改光角才收得掉。
- **sw34-35 `pelvis-frog`(骨盆蛙式)**:新 view,仰臥蛙腿。**使用者定版**:雙臂屈肘交疊胸前 + 雙腿蛙腿(髖屈 `leg.x 27`、外旋 `thigh.y 45`、外展 `leg.z 40`、膝屈 `knee.x 92`、足內翻併攏 `ankle.x 35/ankle.z -20`)、`fig.z 0.88`、`surfaceField:1`。SOP(reviewed):兩 ASIS 等高不旋轉、CR 垂直對恥骨聯合上 2.5cm、SID 102。⚠️ 外傷/疑髖骨折禁蛙位。
- **sw36 `pelvis-in-let` / `pelvis-out-let`(骨盆入口/出口位)**:新 2 views,首次用 **真・CR 角度 `crTilt`** 而非機身假斜。腿直、雙足內旋 15°(`thigh.y -15` 同號)、骨盆不旋轉。
  - 🔑 **crTilt 符號慣例(臥位)**:**正 = 向腳側 caudad、負 = 向頭側 cephalad**。Inlet `crTilt +40`(向腳,對 ASIS 中央,看骨盆環前後位移);Outlet `crTilt -30`(向頭,對恥骨聯合下,看恥骨上下支;男 20-35/女 30-45)。SID 102。
  - ⚠️ 鍵名刻意寫 `pelvis-in-let`/`pelvis-out-let`(夾 `-` 切開),不是 `pelvis-inlet`——grep 找不到時注意。
- **sw37-38 `skull-stenvers` 改真斜 + 使用者定版**:① sw37 把 stenvers 從「機身視覺斜 `bodyTilt`」改成 **真・`crTilt -10`**(光束真的朝頭傾,十字往枕部移;SOP 本就是 cephalad,使用者選真斜)。② sw38 使用者定版:`head.x 4 / head.y 45(面轉對側)/ chest.x 2`、雙臂上抬近頭微屈肘(`arm.z -90, x -15, y -32, elbow.y 10`)、`fig.z 0.81`、`tube.x 0.02 z 0.57 h 1.74`、`crTilt -10`、光野 20×19、`surfaceField:0`(光野只畫頭上)。**注意**:`skull-stenvers-arcelin`(仰臥替代)仍用舊的 `bodyTilt:12`(機身假斜),沒跟著改 crTilt。
- **sw39 `dunn-view`(髖 Dunn 位)**:新 view,仰臥髖屈 90° + 外展 20°(`leg.x 90, leg.z 20, knee.x 90` 同號)、CR 垂直對 ASIS–恥骨聯合中點、SID 100。modified Dunn = 髖屈 45°(disfigure 髖屈 55-90° 會糊,糊就降到 ~50)。
- **sw40 `dunn-view` 加 `beamShadow:1`**:蛙腿抬高擋斜射 sun → 腿間積硬黑影 + 長斜影。CR 垂直(pitch 0)→ beamShadow 對齊光束 = 正上方打光,影子收到身體正下方。對照圖 `shots/dunn_before|after|foot.png`。**同類修法**:任何「抬腿/抬手 + 仰臥垂直 CR」view 若腿/臂間積黑影,優先加 `beamShadow:1`。

## sw27-33:Styloid(莖突)view + 新機制
- **新 view `styloid`**(莖突,俯臥側位;SOP 見 `Xray/positions.json` styloid-temporal-styloid-process):俯臥、頭轉近側位(head.y~68)、左臂屈肘上抬手貼桌近頭、CR 朝頭傾 10°、對患側 EAM 下後。**使用者定版數值已寫進 preset**(sw33,tube x0.05/z0.55,crTilt -10)。
- **臥位真・CR 朝頭傾 `crTilt`**(sw30):`tubeHead.rotation.z`(臥位=沿身體縱軸傾 cephalad/caudad,光束+機身一起轉,十字/光野跟著走;也加進 SID dir Euler)。**為什麼不是 pitch**:臥位(轉房間)下 pitch 變成水平擺動、不是朝頭。UI「CR 朝頭傾(臥位)」。站位 preset crTilt 0 不受影響。
- **張口示意 `uMouthOpen`**(sw29):disfigure 無下顎關節 → 用臉部模型空間口部深色橢圓貼花近似張口(會跟頭轉/變形)。per-preset `mouthOpen` 旗標(styloid=1)+ `?mouth=1/2`(2=亮色探位)。座標 model (x0,y1.60,z0.092)。
- **皮膚樣式預設**(sw27):`uSkinMode` 預設改 2(陶土暖影)。
- 診斷 URL 再加 `tubex/tubez/tubeh`(球管位置覆寫)。
- ⚠️ **擺姿勢教訓**(見 memory feedback-paste-values-verbatim):使用者貼 📋 數值 → 原封不動寫回,別自作主張改 pose。手調姿勢使用者整體判斷一定比 Claude 單規則+靜態截圖好。

## sw19:swimmer 光影對齊 `Xray/Swimer view示範.jpeg`

## sw19:swimmer 光影對齊 `Xray/Swimer view示範.jpeg`
**參考圖鐵則**:X 光板(bucky)上**只有身體的柔影**,沒有亮光野矩形、沒有投影十字;光野+十字**只畫在皮膚上**。
- **承光面分流**(beamPaint 用 `if(onSurface)` 編譯期分支):
  - 承光面(板/牆/檯,sw20):一塊柔和**光野**(`fieldLit·uPlateField` 微亮 + 微暖)+ 身體**柔影**(`shadow·uPlateShadow`),**但不畫投影十字**。`fieldLit = fieldMask·lit·surfGate`、`shadow = fieldMask·(1-lit)·surfGate`。預設 `uPlateField 0.35`、`uPlateShadow 0.5`;UI「板上光野」「板上影濃」可調(0 = 關)。
  - 身體皮膚:光野亮區 + 暖調 + 十字(`bodyGate` 橢球只罩後頸/肩、排除舉起手臂)。
  - 演進:sw18 誤把**亮光野矩形+投影十字**全投到板上 → 打槍;sw19 改「板上只剩柔影」→ 使用者說「範例圖影子後面要有一塊光野」;sw20 = 板上「柔光野+柔影、無十字」。`surfaceField` 旗標仍是承光面著色總開關(swimmer=1)。
  - **sw21**:① 板上光野改用**乾淨矩形 `nearFade·inX·inZ`(不套 farFade)**——farFade 沿光束距離切、打在斜板面上會切出對角線 → 角落黑三角;拿掉就乾淨。② 加**光野框線** `uPlateFrame`(矩形內緣一圈、UI「板上框線」)。③ 皮膚十字改**混向柔灰 `#808080`**(不再單純壓暗),近示範圖灰色定位線。UI 新增「板上光野/板上影濃/板上框線/十字線寬」四條微調滑桿。
  - 診斷 URL 參數再加 `tx/ty/tz`(相機 target 覆寫,對準板面除錯用)。
  - **sw26**:**皮膚樣式比較鈕**(🧑 皮膚樣式)——`uSkinMode` 0=原本/1=陶土軟陰影/2=陶土暖影,只改 `emissiveNode` 自照亮(膚色不變),uniform 即時切換、`?skin=` URL 參數、列入 PERSIST_UNIFORMS。差異刻意溫和。想更明顯就加大 `shade1/shade2` 參數或 `warmShadow`。
  - **sw25**:**十字 = 光野中央定位線,線延伸到光野邊緣**(垂直↓肩、水平→後頸)。修正:十字**與光野共用同一個 fm**(不再用小十字閘);排除舉起的手臂改靠**範圍閘形狀**——把閘的前後半徑拆出 `uPaintRZ`(窄)→板側 -z 的手臂落在閘外。`paintGate` 變 `{z,r,ry,rz}`,swimmer `{z:-1.37, r:0.13, ry:0.22, rz:0.08}`。UI:閘 水平r(後頸寬)/垂直ry(到肩)/前後rz(排手臂)。移除 sw24 的十字長/寬範圍滑桿與 uCrossRX/RY。
  - **sw24**:① 十字垂直線被小閘截斷(使用者要它往下延伸到斜方肌)→ 十字閘改**細長柱狀橢球**(`uCrossRX` 窄 0.06 不繞頸/不上手臂、`uCrossRY` 長 0.24 往下延伸);UI「十字長/十字寬範圍」。② **控制面板收合/還原**(`—` 收合、浮動 `☰ 面板` 還原)。③ **「存到此 view / 還原此 view」**:把目前 S+關節+uniforms 存到 `localStorage["ovr_<preset>"]`,`applyPreset` 末端 `loadOverride()` 自動套用(正式站無法寫回原始碼,用 localStorage 讓微調持久;滿意後仍要 📋 複製數值由 Claude 回填 PRESETS 原始碼才會跨裝置/永久)。`PERSIST_UNIFORMS` 列出會被存的 uniform。
  - **sw23**:十字線跑到「左頸+左臂」根因——光野閘為了肩部光放大(r0.13/ry0.20),但**十字與光野共用同一大閘**→十字垂直面沿整個閘高繞頸側/上手臂。**修:十字改用自己的小閘**(`crossGate = smoothstep(uCrossGate, uCrossGate-0.15, pgd)`,只取橢球內側),光野維持大閘。UI 加「十字範圍」滑桿(`uCrossGate` 預設 0.55)。預設值寫入:袖長 0.28/0.28、十字線寬 16mm(`uCrossW 0.008`)。
  - **sw22**:修掉「光野左上角黑色三角形」(使用者圈圖確認在後腦陰影處)。真因:板上光野亮度被 occl 橢球挖洞(`fieldLit·lit` + occl 陰影項),粗橢球硬邊在角落切出三角(陰影算兩次)。**改:板上光野均勻打滿矩形**(不用 occl 挖洞),身體陰影**只**靠場景 sun 的柔和 profile 投影。移除 `uPlateShadow` uniform + 「板上影濃」滑桿。板影濃淡改由 `sun.intensity`/陰影本身決定。
- **肩部光**:`paintGate {z:-1.37, r:0.13, ry:0.20}`(涵蓋後頸+肩),`r` 窄到排除手臂(在 -z 板側)。
- **十字線寬可調**:`uCrossW`(半寬 m,預設 0.011);UI「十字線寬 (mm)」1-30mm。
- 使用者微調值:`tube {x:-0.94, h:1.5, pitch:88, fieldW:0.16, fieldH:0.38}`、SID 102。十字耳後位置/肩範圍仍可滑桿微調。

## ⚠️ 著色機制重大修正(sw17,推翻 sw14-16 的 facing 路線)
**結論:facing(用法線·朝球管 判斷正反面)是錯的路線,已整段移除。** 十字/光野本來就該畫在
**球管入射側的後頸(耳後)**——那面就是要顯示光線的地方;facing 卻把「沒朝球管的面」關掉,反而
①把該顯示的後頸光線砍掉、②連帶把 cspine(無閘 view)原本正常的後頸光線也弄不見。使用者明確回報:
「後頸光線沒辦法呈現;cspine 原本沒問題、被你改壞」。
**正解 = 純『空間橢球閘』**:`fm = fieldMask·lit·surfGate·gateRegion`,`gateRegion = mix(1, smoothstep(1.10,0.92,pgd), uPaintGateOn)`,
`pgd` 是把表面點對 `uPaintC`(中心)、`uPaintR`(x/z 半徑)、`uPaintRY`(y 半徑)做橢球正規化的距離。
- **只靠位置決定畫在哪**:把橢球擺在後頸(z 偏球管側),橢球夠小就只罩到該處 → 不穿到對側、不沾手臂、後頸光線正常。
- **gate 關閉的 view(cspine-lateral)**:gateRegion=1 → 維持原本「光束打到哪畫到哪(含後頸)」,**= 使用者說的原本正確行為**。
- swimmer 預設:`tube {x:-0.85, h:1.52}`、`paintGate {z:-1.37, r:0.09, ry:0.11}`。**十字確切高度(耳後約 2cm)請用「焦點高」+「閘 深度Z」滑桿微調**(中心跟球管 x/高,深度獨立)。

## 🆕 重大:headless Chrome 可直接截 WebGPU 圖(接手者必讀)
**以前**只能靠使用者線上回報、瞎猜。**現在**本機 headless Chrome 能直接 render WebGPU 出圖,Claude 可自己看畫面除錯。
- 開 server:`python -m http.server 8765`(背景)。
- 截圖一張:
  `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --enable-unsafe-webgpu --enable-features=Vulkan --window-size=760,760 --virtual-time-budget=14000 "--screenshot=<絕對路徑>.png" "http://localhost:8765/index.html?p=cspine-swimmers&hud=0&az=50&el=6&dist=1.5"`
- **⚠️ WebGPU 首幀偶爾全白(~3KB)**:用 loop 重試到檔案 >40KB 為止(通常 1-2 次)。`--screenshot` 路徑要 **Windows 絕對路徑**(反斜線)。
- **新增 URL 診斷參數**(startup 解析):`p=<preset>`、`hud=0`(隱藏面板)、`az/el/dist`(球面相機,繞 controls.target)、`dbg=1`(把著色遮罩 fm 染紅,一眼看出 paint 落在哪些表面——找穿透/手臂著色神器)。這些參數對正式站無害,保留。

## 0. 接手起點(先讀這段)

**線上版 build 號 `sw40`**(畫面右側讀數第一行會顯示;用來確認使用者看的是不是最新版——快取問題反覆出現;叫他無痕或 `?v=40`)。最近完成:Dunn 位腿間黑影修正(sw40 加 `beamShadow:1`)、骨盆蛙式/入口/出口位、Stenvers 真斜定版(見頂部 sw34-40 區塊)。早期 `cspine-swimmers` 皮膚十字/光野微調歷史見 §2 與下方 swNN 細節。

**目前著色模型(看 §2 swimmer 條與下方各 swNN 演進細節,這裡只給結論)**:
- **皮膚十字/光野**:用 TSL `beamPaint`,**身體**畫光野亮區+十字、**承光面(X光板)**只畫柔光野+sun 柔影(無投影十字)。`beamPaint` 用 `if(onSurface)` 編譯期分支。
- **十字 = 光野中央定位線**,與光野**共用同一範圍閘 fm**,線延伸到光野邊緣(垂直↓肩、水平→後頸)。
- **範圍閘**`paintGate {z, r, ry, rz}`(橢球,跟球管 x/高;z/r/ry/rz 滑桿可調)。**排除舉起的手臂靠閘形狀**:`rz`(前後)收窄→板側 -z 手臂落在閘外。swimmer `{z:-1.37, r:0.13, ry:0.22, rz:0.08}`。
- **facing 已廢除**(sw14-16 走過 facing 但錯,sw17 起改純空間閘;見下「著色機制重大修正」)。
- **皮膚樣式**:`uSkinMode` 0/1/2(🧑 皮膚樣式 鈕),只改自照亮、膚色不變。
- swimmer 微調值:`tube {x:-0.94, h:1.5, pitch:88, fieldW:0.16, fieldH:0.38}`、SID 102、袖長 0.28/0.28、十字線寬 16mm。**尚未存 `samples/swimmers_final.png`(待使用者拍板)**。

**常用工具(sw15-24 陸續加的)**:SID(cm)滑桿、📋 複製目前數值、💾 存到此 view/↺ 還原此 view(localStorage)、控制面板收合(— / ☰)、headless 截圖+`?dbg/skin/p/hud/az/el/dist/tx/ty/tz` 診斷參數(見下「headless」段)。

- **本機**:`python -m http.server 8765 --directory .`(或 preview launch config `sim3d`);背景跑 `python tools/shot_server.py 8766` 當截圖管道。
- **線上**:push main → GitHub Pages `https://mickeypeng530.github.io/3D/`(約 1-2 分鐘部署)。repo `github.com/mickeypeng530/3D`。本機 git 在 `C:\Users\彭嗣翔\Claude_Work\3D`(獨立 repo,**非** Xray repo)。
- **使用者習慣**:他都在 GitHub live 站看(不看本機);每次改完要他**無痕視窗**或 `?v=數字` 破快取(普通 Ctrl+Shift+R 對 Pages HTML 常破不掉)。改完務必 commit+push,並把 build 號 +1。
- **使用者偏好自己用滑桿微調**再回報數值,你再寫進 preset。不要替他決定最終角度。
- **Swimmer's 目前狀態**:側位、近板手高舉/遠手下壓/下顎抬、SID 102 都 OK;十字+光野「畫在皮膚上」的機制已大致正確(見 §2 該條的完整除錯紀錄)。最後卡在「十字只在朝球管的脖子正面、背側(左臂/左脖子)要乾淨、整段頸都要有光野不被切暗」——build sw14 用「facing 收緊到 smoothstep(0.30,0.62) + 各向異性橢球閘(r 窄/ry 高)」解掉(根因見上方 §0 sw14 段),**待使用者確認**。確認後存 `samples/swimmers_final.png` 鎖定。
- **大方向待辦**:`..\Xray\positions.json` 還有缺照要批次補(已 reviewed 的優先)。已定稿:pelvis-ap、pelvis-frog、pelvis-in-let、pelvis-out-let、dunn-view、stenvers、arcelin、caldwells、waters、styloid、(swimmers 待確認)。線上 build = **sw40**(§0 / readout)。


## 1. 這專案在做什麼

放射擺位教學網站(`femhmedimage.org` 放射技術指引,本機 `..\Xray\`)需要大量擺位示意照。真人拍攝有隱私 / 尷尬部位 / 找不到模特兒的痛點(127 筆中 47 筆缺照,多為骨盆 / 髖 / 腹部 / 胸部 / 嬰兒)。本工具用 three.js + disfigure(平滑人偶,MIT)在瀏覽器模擬 X 光攝影室與可擺姿勢人偶,截圖 PNG 給主站用。

## 2. 現在進度到哪

- ✅ MVP 完成:攝影室、立式攝影架(板高可調)、攝影檯 + 檯面偵檢板、天吊球管(x/z/高/俯仰/旋轉)、光野錐 + 十字 + spotlight 投影、定位雷射線、SID 即時讀數
- ✅ 人偶:disfigure **Man**(身高 1.73),全身位置 + 頭頸/軀幹/四肢關節滑桿(disfigure 軸位見 §4)
- ✅ 場景 preset(下拉選單自動生成自 `PRESETS`):cspine-lateral、cspine-swimmers、pelvis-ap、skull-stenvers、skull-stenvers-arcelin、skull-caldwells、waters-view、ankle-ap 等
- ✅ 截圖 PNG / 匯出匯入設定 JSON / 白底切換
- ✅ 美術 pass:示範圖風格(灰肢體 + 藍衣人偶、粉紅雷射、灰藍場景、柔光)
- ✅ 設備細節 pass:膠囊形球管殼 + 圓角準直儀 + 把手 + 接頭(yoke 掛 rig 不隨俯仰轉)、拱頂壁架殼(ExtrudeGeometry)、圓邊檯面(RoundedBoxGeometry)
- ✅ **disfigure 平滑人偶實驗版 `disfigure.html`**(2026-06-12 spike 成功):無縫平滑身體 + **原生腳趾/手指**,MIT 授權,質感 = 使用者的 3D 擺位示範圖
- ✅ **index.html 已全面遷移到 disfigure 引擎**(2026-06-13):完整滑桿 UI(54 個,含 disfigure 關節路徑 head/chest/waist/arm/elbow/wrist/leg/knee/ankle/foot 的 x/y/z)+ 雷射 gap/skin + 體表十字(含 flat 模式給仰臥)+ 手指 path 走 JSON 匯出入。男性人偶 Man(1.73)
- ✅ **使用者已定稿 2 個缺照 view**(2026-06-14):
  - **pelvis-ap**(仰臥):雙腿內旋 18°(thigh.y 同號)、CR 對 ASIS 下 5cm、SID 102、光野 35×43;使用者選低側斜構圖
  - **skull-stenvers**(俯臥)+ **skull-stenvers-arcelin**(仰臥替代):面轉對側 head.y 45、CR 入點顳/耳(使用者調 tube x=-0.12,z=0.57)、SID 100、光野 20×19、球管機身視覺斜 12°(與光束解耦)、檯面光野關閉(surfaceField:0)。**官方參考圖 `samples/stenvers_final.png` = 使用者最終截圖**
  - **skull-caldwells**(直立 PA,2026-06-14):面向壁架 rotY 180、**點頭 head.x 15°**(下巴內收、前額朝板)、fig z=-1.55 貼板、球管 **h=1.76 真斜 8° caudad(pitch 82)**、SID 100、光野 20×24。**示意圖風格**:`showCross:0` + `surfaceField:0` + 側面 profile 相機(對照 `..\Xray\caldwell view示意圖.png`)。CR 真斜(非假機身斜),想要完整 SOP 15° 把 pitch 調 75
  - **cspine-swimmers**(立位側位,2026-06-14):rotY 90 側位(矢狀面平行板)、**近板側(左)手臂 l_arm.z 100 高舉過頭、遠側 r_arm.z -72 下壓**(分開兩肩露 C7-T1)、head.x -12 下顎抬、fig z=-1.42、球管 z=-0.64 h=1.44 pitch 90 對 C7-T1、**SID 102**、光野 16×30 窄高。Twining 法。**這個 view 要十字+光野框畫在皮膚上**(showCross 1、surfaceField 0 板上不畫)。⚠️ 光野沿光束打到所有表面(手、板)→ 用 `paintGate {z, r, ry}` 範圍閘只在頸 C7-T1 畫。**正解(build sw14,根因見 §0)**:① facing 收緊到 `smoothstep(0.30,0.62, normalWorld·toFocal)`——十字水平線是過束軸的水平面、會橫繞垂直脖子一整圈,facing 太鬆(舊 0.22≈77°)就讓頸側也被畫成「左右都有十字」+頸側暗帶抹寬變暗;收緊只留正對球管窄錐。② 範圍閘改**各向異性橢球**(不再球形):`r` 收窄(0.12)只罩脖子粗細、`ry` 撐高(0.24)涵蓋整段頸——舊球形要 r 大才蓋頸高,卻把高舉經過頸側的手臂一起包進去 → 手臂出現十字。`pgd` 用橢球正規化距離(內部 <1)。十字平面(posB.x/z=0)會同時切過頸前後兩面,**靠 facing 擋掉背面**那一份,不是靠透明。occl 經實測與此無關(開關相同)。**光野/十字位置由「球管」決定(beam 投影),不是遮罩**——遮罩 followBeam 跟著 tube.x/h,要移光野去耳後是調「X光球管」的 焦點高/位置X;「光野範圍閘」滑桿只調 深度Z/範圍r。(曾把遮罩做成獨立位置滑桿→移遮罩光野不動、誤導,已改回 followBeam)光束 x 要對準頸部(=fig.x)否則只擦到邊緣很淡。**陰影**:預設 sun 從上方斜下打,高的手影會落到頭高度(錯)→ 用 `beamShadow:1` 讓 sun 對齊光束方向(水平),頭影在頭高、手影投到板頂以上。directional light 在無限遠擺不到球管出口,球管會擋光投自身陰影 → **球管整組 `tubeRig.traverse castShadow=false`**(球管陰影不重要),只留人偶投影。⚠️ **applyPreset 只複製白名單欄位**(fig/tube/ws/det/room/occl/surfaceField/showCross/paintGate/beamShadow)——加新的 per-preset 自訂欄位一定要在 applyPreset 補一行複製到 S,否則靠殘留狀態僥倖、fresh load 會失效。⚠️ 截圖時 embedded preview canvas 會變 1px → 先 `renderer.setSize(960,720,false)+camera.aspect` 再拍(真實瀏覽器正常)
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
- 截圖管道:背景跑 `python tools/shot_server.py 8766` → preview_eval 裡 render + POST → `shots/*.png` 直接 Read。⚠️ embedded preview canvas 常變 1px,截圖前先 `s.renderer.setSize(960,720,false); c.width=960;c.height=720; s.camera.aspect=960/720; s.camera.updateProjectionMatrix();`(真實瀏覽器正常,只影響截圖)
- 確認線上版本:畫面右側讀數第一行 `build swNN`(在 applyAll 末端 readout)。改視覺後把號碼 +1,叫使用者用無痕/`?v=` 確認看到新號
- UI 額外滑桿群:「病人服(袖長)」前/後(`uSleeveFront/Back`)、「光野範圍閘(跟著球管)」深度Z/範圍r(`S.paintGate`)、「X 光球管」位置X/Z/焦點高/俯仰/光野寬高
- 加 preset:複製 `PRESETS` 一筆,joints 用路徑語法;先在 console 用 `__sim.setJoint()` / `__sim.S` 調好再回填
- 主站缺照清單:見 `..\Xray\positions.json`(47 筆 `images.positioning_photo` 為空者);出圖優先序:已 reviewed 10 筆 → 骨盆/髖/腹部隱私群 → 其餘
- 部署:push main → GitHub Pages(repo Settings → Pages 啟用 main / root)

## 6. 新 view 製作 SOP(沒做過的 view 照這份走)

> 任何新 session 開工前先讀這段。每一步都有對應的「為什麼/坑」連回上面章節。

1. **選 view** — 從 `..\Xray\positions.json` 缺照清單挑(`images.positioning_photo` 為空者,共 47 筆;**已 reviewed 的優先**)。出圖優先序見 §5。
2. **查擺位 SOP** — 讀該 view 的擺位規範(positions.json 內文 / 主站),先定下:**體位**(站/仰臥/俯臥)、**CR 入點 + 角度**、**SID(cm)**、**光野寬高(cm)**、是否需要十字/光野畫在皮膚上。
3. **起環境** — `python -m http.server 8765 --directory .`(或 preview config `sim3d`);背景跑 `python tools/shot_server.py 8766` 當截圖管道。
4. **選基礎模板**(複製 `PRESETS` 最接近的一筆改):
   - **站位**:fig 站立、`rotY` 決定面向(0/180=側位貼板,180=面向壁架)。
   - **臥位**:`room:{lie:1, ox, oy, oz}`「人不動、轉房間」(§4 🔑🔑),人偶維持站立關節語意正常;臥位朝頭傾用 `crTilt`(§sw30)。
   - **俯臥**:仰臥 preset 把 `fig.rotY` 設 180、頭轉用 `head.y`。
5. **調 pose** — console `__sim.setJoint()`/`__sim.S` 或 UI 滑桿,設 fig 位置、關節、`tube`(x/z/h/pitch)、`crTilt`、SID、光野寬高、`surfaceField`/`showCross`。**關節務必查 §4 軸位圖**(很多軸被鎖死、左右對稱用「同號」),新增滑桿前先寫入讀回驗證。
6. **截圖檢查** — headless Chrome(§「headless」段,首幀偶爾全白要重試到 >40KB)或 preview 截圖管道(canvas 常變 1px,先 setSize 再拍)。
7. **使用者微調 → 回填** — 使用者自己用滑桿調好後 **📋 複製數值 → 原封不動寫回 PRESET**。⚠️ **絕不自作主張改 pose**(memory `feedback-paste-values-verbatim`):手調整體判斷一定優於 Claude 單規則+靜態截圖。
8. ⚠️ **applyPreset 白名單** — 若這個 view 用到**新的 per-preset 欄位**,一定要在 `applyPreset` 補一行複製到 `S`,否則 fresh load 會失效(只靠殘留狀態僥倖)。
9. **發佈** — build 號 +1(applyAll 末端 readout)→ `git commit + push main` → GitHub Pages 約 1-2 分鐘部署 → 叫使用者**無痕視窗或 `?v=<號>`** 破快取確認看到新版。
10. **出圖蓋章(finalize)** — 渲染高解析終圖(headless 大 window-size,hud=0)→ 跑 `python tools/seal_stamp.py <終圖路徑> br 0.025` → 出 `shots/sealed_<name>.png`:右下蓋 SP 作者印章(`Xray/assets/SP-seal-ink.png`)+ 底部 banner「亞東醫院影像科 · 教學用途 · AI 修飾 · <今天日期>」。**script 不上傳**(對好位置後另用 firebase-admin 上傳)。`seal_stamp.py` 吃本機檔或 view_id(view_id 會從 Firestore 抓 positioning_photo);角落 `br/bl/tr/tl`、`frac`=印章佔對角線比例。舊版純文字浮水印是 `tools/watermark.py`。
11. **定稿鎖定** — 使用者拍板後 + 回填主站 `..\Xray\positions.json` 的 `images.positioning_photo`(編輯歸屬用 "C",見 memory `reference_xray_admin_name`)。

> ⚠️ **`tools/seal_stamp.py` 目前未進 git**(內含 Firebase API key + 個人路徑,repo 為公開 GitHub Pages → 刻意不提交)。流程靠這份 HANDOVER 記錄;工具在本機 `tools/`。`shots/` 已 gitignore,`sealed_*.png` 不會被推。
