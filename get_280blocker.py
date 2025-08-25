#!/usr/bin/env python3
import sys
import os
import hashlib
import datetime
from zoneinfo import ZoneInfo
import requests

print("280blockerフィルタの自動取得を開始します。")

# JST基準で現在の年月 (YYYYMM)
now_jst = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
candidates = []
# 直近の月から最大3ヶ月分をフォールバック候補に
for i in range(0, 3):
    y = (now_jst.year if now_jst.month - i > 0 else now_jst.year - 1)
    m = (now_jst.month - i) if (now_jst.month - i) > 0 else (now_jst.month - i + 12)
    candidates.append(f"{y}{m:02d}")

base_url = "https://280blocker.net/files/280blocker_domain_ag_{ym}.txt"
output_file = "adguard.txt"

session = requests.Session()
session.headers.update({
    "User-Agent": "adguard-auto-updater (+https://github.com/)"
})

latest_text = None
used_url = None
last_error = None

for ym in candidates:
    url = base_url.format(ym=ym)
    print(f"試行: {url}")
    try:
        r = session.get(url, timeout=30)
        if r.status_code == 200 and r.text.strip():
            latest_text = r.text
            used_url = url
            break
        else:
            last_error = f"HTTP {r.status_code}"
    except Exception as e:
        last_error = str(e)

if latest_text is None:
    print(f"取得に失敗しました。最後のエラー: {last_error}", file=sys.stderr)
    sys.exit(1)

# 既存と差分チェック
old = ""
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        old = f.read()

if old == latest_text:
    print("内容に変更なし（コミットは行いません）。")
    sys.exit(0)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(latest_text)

print(f"更新完了: {output_file} に保存しました。元URL: {used_url}")
sys.exit(0)
