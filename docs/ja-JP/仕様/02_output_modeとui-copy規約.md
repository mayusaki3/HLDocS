<!--
HLDocS:LLM-MANAGED
doc_id: HLDOCS.SPEC.OUTPUT-MODE
lang: ja-JP
canonical_title: output_modeとui-copy規約
document_type: spec
output_mode: canonical-md
transport: none
-->

HLDocS ドキュメント目次 > 仕様 > output_modeとui-copy規約

# output_modeとui-copy規約

## 1. 目的

- LLM 出力の回収失敗を防ぐ
- 再生成による計算資産の無駄を抑制する
- UI・API の両利用形態に対応する

---

## 2. output_mode

### canonical-md

- 正規 Markdown として保存されることを前提とする
- ファイル生成・UI コピーの双方に対応

### ui-copy（推奨）

- UI 上で全文をコピー可能な形で出力する
- デフォルトの利用形態とする

---

## 3. ui-copy 規約

- 出力全体を Markdown としてそのままコピー可能であること
- セッション切れによるファイル回収失敗を回避できる
- 原則として ui-copy を優先する

---

## 4. 例外（file-only）

- 自己言及により ui-copy が破綻する文書
- 例：`<HL-FENCE>` の説明文書
- この場合のみ、ファイルダウンロードを許容する

---

## 5. doc_id との関係

- output_mode の変更は doc_id に影響しない
- doc_id は出力形式と独立して管理される

---

HLDocS ドキュメント目次 > 仕様 > output_modeとui-copy規約
