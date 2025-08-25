#!/usr/bin/env python3
import sys, os, datetime
from zoneinfo import ZoneInfo
import requests

print("280blockerフィルタの自動取得を開始します。")

# JST基準のYYYYMM
now_jst = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
candidates_ym = [f"{now_jst.year}{now_jst.month:02d}"]
# 前月・前々月もフォールバック
for i in (1, 2):
    y = now_jst.year if now_jst.month - i > 0 else now_jst.year - 1
    m = now_jst.month - i if now_jst.month - i > 0 else now_jst.month - i + 12
    candidates_ym.append(f"{y}{m:02d}")

hosts = ["280blocker.net", "www.280blocker.net"]
base_tpl = "https://{host}/files/280blocker_domain_ag_{ym}.txt"
output_file = "adguard.txt"

session = requests.Session()
session.headers.update({
    # ブラウザっぽいヘッダ
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Referer": "https://280blocker.net/",
    "Accept": "text/plain,*/*;q=0.1",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Connection": "close",
})

latest_text = None
used_url = None
last_reason = "unknown"

for ym in candidates_ym:
    for host in hosts:
        url = base_tpl.format(host=host, ym=ym)
        print(f"試行: {url}")
        try:
            r = session.get(url, timeout=30, allow_redirects=True)
            if r.status_code == 200 and r.text.strip():
                latest_text = r.text
                used_url = url
                break
            else:
                last_reason = f"HTTP {r.status_code}"
        except Exception as e:
            last_reason = f"{type(e).__name__}: {e}"
    if latest_text is not None:
        break

if latest_text is None:
    print(f"取得に失敗しました。最後のエラー: {last_reason}", file=sys.stderr)
    sys.exit(1)

# 差分チェック
old = ""
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        old = f.read()

if old == latest_text:
    print("内容に変更なし（コミットは行いません）。元URL:", used_url)
    sys.exit(0)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(latest_text)

print(f"更新完了: {output_file} に保存しました。元URL: {used_url}")
