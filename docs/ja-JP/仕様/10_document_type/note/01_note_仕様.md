<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-000000Z-N0T1
lang: ja-JP
canonical_title: document_type:note 仕様
document_type: spec
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > 仕様 > document_type > note > 仕様

# document_type:note 仕様

## 1. Purpose（存在理由）

`note` は、HLDocS における **補助的 document_type** であり、  
他の document_type に明確に該当しない **未確定・検討途中の情報** を保持するための文書種別である。

## 2. Scope（対象）

- 設計途中のメモ
- 観点・論点の列挙
- 未確定な案・仮説の整理
- 後続の `spec` / `testspec` / `prompt` / `index` / `traceability` 等を作成するための前段資料

## 3. Non-goals（対象外）

- 合意済み仕様・規約の宣言（= spec）
- 操作・運用手順の確定版（= usage）
- テスト観点・期待結果の定義（= testspec）
- 生成規則・判断規則の定義（= prompt）
- 文書体系の俯瞰（= index）
- トレーサビリティ規約（= traceability）

## 4. ガード（MUST / MUST NOT）

### 4.1 MUST

- `note` は **他の document_type に該当しないことを確認した上でのみ**使用する
- 未確定・暫定であることが読み取れる記述とする
- 将来 `spec` 等に昇格可能な程度の前提・論点を保持する

### 4.2 MUST NOT

- `note` を分類不能な逃げ先として使用してはならない
- 合意済み事項を `note` に確定事項として記載してはならない
- 恒久運用する前提の文書を `note` に留め続けてはならない

## 5. 推奨構成

- 背景 / 目的
- 前提
- 論点
- 案
- 未決事項
- 次アクション（任意）

---

[目次](../../../目次.md) > 仕様 > document_type > note > 仕様
