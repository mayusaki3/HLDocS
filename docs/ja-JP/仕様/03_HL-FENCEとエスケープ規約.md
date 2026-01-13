<!--
HLDocS:LLM-MANAGED
doc_id: HLDOCS.SPEC.HL-FENCE
lang: ja-JP
canonical_title: HL-FENCEとエスケープ規約
document_type: spec
output_mode: canonical-md
transport: none
-->

HLDocS ドキュメント目次 > 仕様 > HL-FENCEとエスケープ規約

# HL-FENCEとエスケープ規約

## 1. 背景

UI コピー時、Markdown の ``` が文中に含まれると、
コピー範囲が途中で切断される問題がある。

---

## 2. HL-FENCE の定義

- `<HL-FENCE>` は ``` の代替トークンである
- ui-copy 時に使用する
- 保存後、人間が ``` に置換することを前提とする

---

## 3. 適用範囲

- ui-copy 出力時のみ使用
- canonical-md 保存後は ``` に戻す

---

## 4. 例外運用

- 本文で `<HL-FENCE>` 自体を説明する文書では ui-copy を行わない
- file-only 出力を使用する

---

HLDocS ドキュメント目次 > 仕様 > HL-FENCEとエスケープ規約
