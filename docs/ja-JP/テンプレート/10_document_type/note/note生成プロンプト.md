<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-000020Z-N0T3
lang: ja-JP
canonical_title: document_type:note 生成プロンプト
document_type: prompt
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > テンプレート > document_type > note > 生成プロンプト

# document_type:note 生成プロンプト

## 0. 最上位命令（MUST）

- 出力は最終成果物のみとする。
- 思考過程・理由・検査結果を出力してはならない。
- `note` は補助的 document_type であり、他の document_type に該当する場合は生成してはならない。

## 1. note 判定（MUST）

以下に該当する場合のみ、`note` を生成してよい。

- 記述対象が未確定・暫定である。
- 合意済みの仕様・規約・手順ではない。
- 既存の `spec` / `testspec` / `index` / `traceability` / `prompt` / `usage` に明確に該当しない。

## 2. note 禁止判定（MUST NOT）

以下に該当する場合、`note` を生成してはならない。

- 合意済みルール・仕様を宣言している（spec）
- テスト観点・期待結果を定義している（testspec）
- LLM の生成・判断規則を定義している（prompt）
- 文書構造や参照関係を定義している（index / traceability）
- 操作手順の確定版を示している（usage）

## 3. 内容生成（MUST）

- 目的・前提・論点・案・未決事項を明示する。
- 未確定であることが読み取れる表現を維持する。
- 将来 `spec` 等に昇格する際に必要な前提情報を省略しない。

---

[目次](../../../目次.md) > テンプレート > document_type > note > 生成プロンプト
