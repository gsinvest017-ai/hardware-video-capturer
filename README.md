# Hardware Video Capturer

USB HDMI 擷取棒 + HDMI dummy plug 方案的影像擷取與處理 pipeline。
來源可抽換：開發階段用測試影片，硬體到貨後改用 `/dev/video0`。

## 專案結構

```
hardware-video-capturer/
├── capture.py                  # 入口，CAPTURE_SRC 切換來源
├── requirements.txt
├── scripts/
│   └── make_test_video.sh      # ffmpeg 產測試影片
├── samples/                    # 測試影片放這
└── .gitignore
```

## 安裝（WSL Ubuntu）

### 1. 安裝系統工具

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv v4l-utils ffmpeg
```

### 2. 建立虛擬環境並安裝套件

```bash
cd ~/hardware-video-capturer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 產生測試影片（1920x1080 @ 30fps，30 秒）

```bash
bash scripts/make_test_video.sh
# 輸出：samples/test.mp4
```

長度可調：`DUR=10 bash scripts/make_test_video.sh`

## 執行

預設讀 `samples/test.mp4`，存成 `out.mp4`：

```bash
SAVE=out.mp4 .venv/bin/python capture.py
```

> 本專案使用 **opencv-python-headless**，**不開視窗**，避免 WSL 上 OpenCV 內建 Qt 的相容性問題。要看畫面請用下面的方式。

## 看畫面

存檔後用 `ffplay` 或 Windows 的播放器：

```bash
ffplay out.mp4                     # WSL 內播放（需要 WSLg）
explorer.exe .                     # 在 Windows 檔案總管打開資料夾後雙擊
```

## 環境變數

| 變數 | 預設 | 說明 |
|---|---|---|
| `CAPTURE_SRC` | `samples/test.mp4` | 影片檔路徑或 `/dev/videoN` 的 N（例如 `0`） |
| `SAVE` | （空） | 設成輸出路徑就把處理後畫面存成檔（例如 `out.mp4`） |
| `MAX_FRAMES` | `0` | 處理幾幀後停止，`0` 表示讀到結束 |

範例：

```bash
# 換影片來源（讀 Windows 端的檔案）
CAPTURE_SRC=/mnt/c/Users/User/Videos/foo.mp4 SAVE=out.mp4 .venv/bin/python capture.py

# 只跑前 60 幀做快速驗證
MAX_FRAMES=60 SAVE=out.mp4 .venv/bin/python capture.py
```

## 擷取棒到貨後

### 1. Windows 端：用 usbipd-win 把 USB 擷取棒轉發到 WSL

PowerShell（系統管理員）：

```powershell
winget install --interactive --exact dorssel.usbipd-win
usbipd list                          # 找到擷取棒的 BUSID（例如 2-3）
usbipd bind --busid 2-3              # 第一次要 bind
usbipd attach --wsl --busid 2-3      # 轉發到 WSL
```

### 2. WSL 端確認裝置

```bash
lsusb                                          # 應看到擷取棒
ls /dev/video*                                 # 應有 /dev/video0
v4l2-ctl --device=/dev/video0 --list-formats-ext
```

### 3. 換來源跑

```bash
CAPTURE_SRC=0 SAVE=out.mp4 .venv/bin/python capture.py
```

## 後續開發

接 YOLO / SAM / 去背等處理只要改 `capture.py` 的 `process()` 函式，
其他流程（讀來源、顯示、存檔）都不用動。

```python
def process(frame):
    # 在這裡做模型推論 / 後處理
    return frame
```
