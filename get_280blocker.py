name: Update 280blocker Filter

on:
  schedule:
    # 毎日 午前10:00 JST（= 01:00 UTC）
    - cron: '0 1 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-filter:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Fetch via Cloudflare Worker
        run: |
          # Worker 経由で最新フィルタを取得
          # run_id をクエリにつけてキャッシュをバイパス（任意）
          curl -fsSL "https://block.shigelon.workers.dev/latest?run=${{ github.run_id }}" -o adguard.txt

      - name: Check for changes
        id: diff
        run: |
          if [[ -n "$(git status --porcelain adguard.txt)" ]]; then
            echo "changed=true" >> "$GITHUB_OUTPUT"
          else
            echo "changed=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Commit and push
        if: steps.diff.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add adguard.txt
          git commit -m "Update 280blocker filter (via Cloudflare Worker)"
          git push
