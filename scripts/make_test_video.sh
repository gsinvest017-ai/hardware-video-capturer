#!/usr/bin/env bash
# 產生 1920x1080 @ 30fps 的測試影片，30 秒，模擬擷取棒輸入
set -euo pipefail
OUT="${1:-samples/test.mp4}"
DUR="${DUR:-30}"
mkdir -p "$(dirname "$OUT")"
ffmpeg -y \
  -f lavfi -i "testsrc=size=1920x1080:rate=30" \
  -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
  -t "$DUR" \
  -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -shortest \
  "$OUT"
echo "wrote $OUT"
