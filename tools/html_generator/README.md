# HLDocS HTML Generator PoC

## 1. 位置付け

本ディレクトリは、HLDocS 自身を対象とした HTML 生成 PoC の最小実装を格納する。

HTML は Markdown 正本を置き換えるものではなく、read-only Operational Representation として生成する。

---

## 2. 対象 profile

初期 PoC では、以下のみを対象とする。

- `overview`
- `reference`

以下は対象外とする。

- `traceability`
- `test-report`

対象外 profile は、HTML 上では `not generated` として扱う。

---

## 3. 実行方法

リポジトリルートから以下を実行する。

### 3.1 bash / Git Bash

```bash
python tools/html_generator/generate_html.py \
  --input docs/ja-JP \
  --output docs/ja-JP/HTMLドキュメント \
  --profile overview,reference
```

### 3.2 PowerShell

PowerShell では、改行継続に `^` ではなくバッククォート `` ` `` を使用する。

```powershell
python tools/html_generator/generate_html.py `
  --input docs/ja-JP `
  --output docs/ja-JP/HTMLドキュメント `
  --profile overview,reference
```

1行で実行してもよい。

```powershell
python tools/html_generator/generate_html.py --input docs/ja-JP --output docs/ja-JP/HTMLドキュメント --profile overview,reference
```

### 3.3 cmd.exe

cmd.exe では、改行継続に `^` を使用する。

```cmd
python tools/html_generator/generate_html.py ^
  --input docs/ja-JP ^
  --output docs/ja-JP/HTMLドキュメント ^
  --profile overview,reference
```

---

## 4. 生成物

以下が生成される。

```text
docs/ja-JP/HTMLドキュメント/
├── overview/
│   └── index.html
├── reference/
│   └── *.html
├── manifest/
│   └── site-manifest.json
└── index.html
```

---

## 5. テスト実行

```bash
python -m pytest tools/html_generator
```

---

## 6. 注意点

- 本実装は PoC 用であり、正式 generator ではない。
- Markdown 変換は最小実装であり、完全な Markdown 変換器ではない。
- `sec_id` は本文に存在する場合のみ抽出し、推測生成しない。
- Manifest に存在しないページへの内部リンクは生成しない。
- HTML generated artifact のファイル名・ディレクトリ名には空白を含めない。

---

## 7. 後続

PoC の検証結果は、まず `docs/ja-JP/フィードバック` に記録する。

PoC 完了後、必要な内容を HTML 系仕様へ一括反映する。
