"""
擷取入口：來源可抽換
  CAPTURE_SRC=samples/test.mp4   讀影片檔
  CAPTURE_SRC=0                  讀 /dev/video0（擷取棒到貨後）

注意：使用 opencv-python-headless，沒有 imshow。
要看畫面請用 SAVE=out.mp4 存檔後，用 ffplay/explorer 觀看。
"""
import os
import sys
import cv2


def open_source(src: str) -> cv2.VideoCapture:
    if src.isdigit():
        cap = cv2.VideoCapture(int(src), cv2.CAP_V4L2)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        return cap
    return cv2.VideoCapture(src)


def process(frame):
    # 之後在這裡接 YOLO / SAM / 去背
    return frame


def main():
    src = os.environ.get("CAPTURE_SRC", "samples/test.mp4")
    save = os.environ.get("SAVE", "")
    max_frames = int(os.environ.get("MAX_FRAMES", "0"))  # 0 = 不限

    cap = open_source(src)
    if not cap.isOpened():
        print(f"open failed: {src}", file=sys.stderr)
        sys.exit(1)

    writer = None
    if save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(save, fourcc, fps, (w, h))

    n = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            out = process(frame)
            if writer:
                writer.write(out)
            n += 1
            if n % 30 == 0:
                print(f"\rframes: {n}", end="", flush=True)
            if max_frames and n >= max_frames:
                break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if writer:
            writer.release()
        print(f"\rframes: {n}")


if __name__ == "__main__":
    main()
