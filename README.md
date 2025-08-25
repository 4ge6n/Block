# 280blocker 自動更新（AdGuard Pro 用 固定URL）

このリポジトリは GitHub Actions を用いて、毎月更新される 280blocker の AdGuard 形式フィルタを
`adguard.txt` に自動反映します。**固定の Raw URL** を AdGuard Pro (iOS) のカスタムフィルタに登録しておけば、毎月自動で最新化されます。

---

## 使い方

1. この3ファイルをリポジトリ直下に配置してコミット・プッシュ
   - `get_280blocker.py`
   - `.github/workflows/update-filter.yml`（フォルダ込み）
2. Actions タブでワークフローを有効化（初回は `Run workflow` で手動実行推奨）
3. 生成される `adguard.txt` の Raw URL を AdGuard Pro に登録  
   例: `https://raw.githubusercontent.com/<yourname>/<yourrepo>/main/adguard.txt`

## 仕様

- 取得元: `https://280blocker.net/files/280blocker_domain_ag_YYYYMM.txt`
- タイムゾーン: JST 基準で `YYYYMM` を判定（GitHub Actions は UTC 実行）
- フォールバック: 直近3ヶ月分まで 404 対策で遡って取得
- スケジュール: 毎月1日の **JST 12:05**（UTC 03:05）に自動実行
- 内容不変ならコミットを行いません

## 手動実行

```bash
pip install requests
python get_280blocker.py
# adguard.txt が作成/更新されます
```

## AdGuard Pro 設定

- アプリの「フィルタ」→「カスタム」→「フィルタを追加」で上記 Raw URL を登録してください。
- AdGuard 側の更新間隔に従って自動取得されます。

---

### 注意
- 280blocker の配布ポリシーや URL 構成が変わった場合はスクリプトの修正が必要です。
- このリポジトリは個人利用を想定しています。ご利用は自己責任でお願いします。
