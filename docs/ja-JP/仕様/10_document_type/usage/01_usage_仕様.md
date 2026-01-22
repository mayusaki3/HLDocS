<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-030000Z-USG1
lang: ja-JP
canonical_title: document_type: usage 仕様
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > 仕様 > document_type > usage > 仕様

# document_type: usage 仕様

## 1. 定義

document_type: usage は、  
**人間が対象システムまたは HLDocS を利用するための具体的手順・操作方法を記述する文書**である。

usage は、利用者が「考えずに従う」ことを前提とした文書であり、  
仕様判断・設計意図・背景説明を目的としない。

---

## 2. 目的

usage 文書は、以下を目的とする。

- 利用手順を誤解なく伝えること
- 操作順・注意事項を明確化すること
- 利用者に判断・推測を要求しないこと

---

## 3. 記述対象（MUST）

usage 文書には、以下のみを記述してよい。

- 操作手順
- 入力・選択・実行の順序
- 利用時の注意点
- 利用条件・前提環境

---

## 4. 禁止事項（MUST NOT）

usage 文書では、以下を行ってはならない。

- 要件・仕様の定義
- 設計意図や背景説明
- 議論・検討過程の記述
- testspec 相当の検証観点の記述
- 他 document_type の内容を代替・要約すること

---

## 5. 他 document_type との関係

- usage は spec を参照してよいが、**spec を補完・変更してはならない**
- usage は minutes / note の内容を内包してはならない
- usage は traceability の必須対象ではない

---

## 6. トレーサビリティ

- usage ⇔ 他 document_type のトレーサビリティは **任意**
- usage 文書の欠落を理由に、仕様不備と判断してはならない

---

[目次](../../../目次.md) > 仕様 > document_type > usage > 仕様
