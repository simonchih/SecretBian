# Secret Council — Secret Trump × 神祕阿扁

兩個原版 Pygame 遊戲已整合至本專案。`game_trump.py` 與 `game_bian.py` 保留各自的遊戲流程及 AI；正式遊戲以獨立程序啟動，隔離對局狀態。所有程式、圖片與字型均位於本專案，不再依賴舊版資料夾。

## 啟動

需要 Python 3.10 以上。Windows 可直接雙擊 `start.bat`；本機已準備好 `.venv`。

其他環境首次安裝及啟動：

```sh
python -m pip install -r requirements.txt
python main.py
```

主選單依序提供：

1. **Secret Trump Version** — 進入原本 SecretTrump 主程式。
2. **Tutorial for Trump** — 全英文互動教學。
3. **阿扁版** — 進入原本 SecretBian 主程式。
4. **阿扁版遊戲教學** — 全繁體中文互動教學。

主選單支援滑鼠、上下方向鍵、Enter 與空白鍵。教學使用滑鼠操作；Esc 返回選單。正式遊戲可按 Esc 或左上角按鈕返回選單（目前對局不保留）；關閉遊戲視窗也返回選單。主選單按 Esc 則退出程式。

也可直接執行 `python game_trump.py` 或 `python game_bian.py`，素材路徑不依賴工作目錄。正式遊戲維持原版以滑鼠點選箭頭、投票按鈕、政策牌及中央繼續按鈕的操作。

## 教學與規則

每個版本包含十個練習：翻牌、身分資訊、合法提名、投票、三次破局、總統棄牌、院長棄牌、權力、特殊提名、勝利條件。答錯有提示，完成操作才可前進；可回上一步或重試。總統留下的兩張牌會實際傳到院長步驟。這是獨立的固定情境練習，不影響正式對局。

原始規則已保存至 `docs/bian-rules.txt` 與 `docs/trump-rules.txt`，保留本遊戲與 Secret Hitler 不同的規則：

- 十人：六位藍營／民主黨、三位一般綠營／共和黨，以及一位扁維拉／D.T.。
- 五項藍方政策或殺死特殊角色，藍方獲勝；六項另一方政策，另一方獲勝。
- 第三、第五項綠營／共和黨政策有暗殺權；第四項有私人黨派調查權。
- 四項綠營／共和黨政策後，特殊角色獲提名為院長／chancellor 就直接獲勝，不需要投票。
- 三次破局強制頒布政策，不發動總統權力。

## 美術與程式

- `assets/entrance.png`：以內建 imagegen 產生的政治懸疑桌遊封面。生成提示詞見 `assets/ART_DIRECTION.md`。
- `visual.py`：統一字型、配色、向量式圖示與面板。執行 `python visual.py` 可重新輸出兩版本所有使用中的 PNG 美術。
- `assets/trump/`、`assets/bian/`：新版背景、陣營政策、特殊角色、調查、暗殺、死亡、箭頭及投票按鈕，共二十張 PNG。
- `assets/fonts/wqy-zenhei.ttf`：兩版共用的中文字型，僅保留一份。
- `game_trump.py`、`game_bian.py`：兩個正式遊戲入口。
- `policy_animation.py`：兩版共用的政策動畫與政策軌座標。
- `game_skin.py`：原遊戲的視覺整合、階段提示與柔和切換光框。原有政策淡入改為每秒六十格下約半秒完成，移除背景執行緒繪圖；字型會快取。
- 兩版皆修正原本停留在勝利畫面時，每次重畫都增加勝場的問題；現在每局僅計算一次。
- `tutorial.py`：雙語互動教學狀態及畫面。
- `main.py`：四選項入口與子程序管理。遊戲離開後重新建立主選單畫面。

舊版資料夾、未使用的舊圖片、舊 py2exe 設定及一次性遷移工具已移除。本專案提供 Python 啟動方式，未製作 exe。

## 驗證

```sh
python -m unittest discover -s tests -v
python tests/smoke_game.py Trump
python tests/smoke_game.py Bian
python tests/render_previews.py
python tests/smoke_startup.py
python tests/smoke_startup.py --native
```

測試使用 SDL 無視窗模式，驗證教學 gating、錯誤答案、所有棄牌組合、重試及文字排版。每個遊戲 smoke test 以模擬滑鼠完成五局並驗證 Esc 返回；不代表所有隨機 AI 局面都已窮盡。`artifacts/` 提供選單、教學及遊戲的實際 Pygame 渲染預覽。

`smoke_startup.py` 從其他工作目錄啟動入口，實際建立兩個遊戲子程序，並依序操作四個選項與返回選單。加上 `--native` 會短暫開啟真實遊戲視窗，驗證 SDL 顯示模式。
