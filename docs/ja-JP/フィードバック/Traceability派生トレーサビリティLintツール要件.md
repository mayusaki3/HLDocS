<!-- FILE: docs/ja-JP/仕様/共通/Traceability派生トレーサビリティLintツール要件.md -->

<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260126-010000Z-7K3P
lang: ja-JP
canonical_title: Traceability 派生トレーサビリティ lint ツール要件（Node）
document_type: spec
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../目次.md) > 仕様 > 共通 > Traceability派生トレーサビリティLintツール要件

# Traceability 派生トレーサビリティ lint ツール要件（Node）

---

## 1. Purpose（目的）

本書は、Traceability 規約における **派生トレーサビリティ（minutes / note ⇔ spec）** を対象に、  
参照の健全性を **静的に検査・集計・整形**する Node ツール（以下 lint ツール）の要件を定義する。

---

## 2. Scope（対象）

### 2.1 対象 document_type

- minutes
- note
- spec

### 2.2 対象記法

- minutes / note 側アンカー
  - `<!-- hldocs:ref_id=ref_<random> -->`
- spec 側参照
  - `<!-- hldocs:ref=<doc_id>#ref_<random> hldocs:rel=<rel> -->`
  - `<rel>` は `rationale` / `derivation`

### 2.3 非対象

- testspec 起点の検証トレーサビリティ（`doc_id#sec_id`）
- 実装コード側 `@hldocs.ref`（検証トレーサビリティ）

---

## 3. 入力・出力

### 3.1 入力

- リポジトリルート（パス）
- 解析対象パス（複数可）
- 解析対象ファイル拡張子（既定：`.md`）

### 3.2 出力（モード）

- `lint`：規約違反（NG）／警告（WARN）／情報（INFO）のレポート出力
- `report`：集計レポート（JSON / Markdown）
- `fix`（任意）：安全に機械整形可能な範囲のみ自動整形

---

## 4. 機能要件

### 4.1 minutes / note の ref_id インデックス生成（MUST）

minutes / note ファイルを走査し、以下を抽出する。

- doc_id（LLM-MANAGED の doc_id）
- ref_id（`hldocs:ref_id=...`）
- ref_id の出現位置（行番号・周辺テキスト抜粋）
- ファイルパス

出力例（JSON 概念）：

- `refIndex[doc_id][ref_id] = { path, line, context }`

### 4.2 spec の派生参照抽出（MUST）

spec ファイルを走査し、以下を抽出する。

- spec doc_id
- `hldocs:ref` の参照先（`<doc_id>#<ref_id>`）
- `hldocs:rel`（`rationale` / `derivation`）
- 出現位置（行番号・周辺テキスト抜粋）
- ファイルパス

### 4.3 整合性検査（MUST）

#### 4.3.1 NG（失敗）条件（MUST）

- minutes / note 内で `ref_id` が重複（同一 doc_id 内で同一 ref_id が複数箇所に出現）
- spec 側 `hldocs:ref` が形式不正（`doc_id#ref_<random>` 以外）
- spec 側 `hldocs:rel` が欠落、または値域外（`rationale` / `derivation` 以外）
- spec 側参照先 doc_id が minutes / note インデックスに存在しない（参照先文書不明）
- spec 側参照先 ref_id が参照先 doc_id に存在しない（broken ref）

#### 4.3.2 WARN（警告）条件（MAY）

- 同一 spec（同一 spec doc_id）内で、同一 `doc_id#ref_id` に対して `hldocs:rel` が混在
  - 例：同一参照を `rationale` と `derivation` の両方で参照している
- 参照されていない ref_id（孤立アンカー）
- 同一 ref_id が多数の spec から参照されている（閾値は設定可能）

#### 4.3.3 INFO（情報）条件（MAY）

- `hldocs:ref_id` の総数、参照数、孤立数
- spec ごとの参照数、参照先分布

### 4.4 レポート生成（MUST）

#### 4.4.1 参照一覧（MUST）

- spec → (minutes/note doc_id, ref_id, rel) の一覧
- minutes/note doc_id → ref_id → 参照元 spec 一覧

#### 4.4.2 出力形式（MUST）

- JSON（機械処理用）
- Markdown（人間確認用）

### 4.5 fix（自動整形）モード（任意・MAY）

自動修正は「意味に影響しない整形」に限定する。

許可例：

- 同一行内の HTML コメント属性順を正規化
  - `hldocs:ref=... hldocs:rel=...` の順序固定

禁止例：

- ref_id の追加・削除
- rel の変更
- 参照の追加・削除

---

## 5. 非機能要件

### 5.1 実装言語・実行（MUST）

- Node.js（LTS）
- CLI で実行可能

### 5.2 依存（SHOULD）

- 解析は Markdown AST でなくてもよい（HTML コメント抽出が主目的）
- ただし、行番号・周辺文脈抽出のため、行ベース解析を必須とする

### 5.3 性能（SHOULD）

- 数千ファイル規模で実行可能（線形走査）
- インクリメンタル（変更ファイルのみ）を将来拡張として許容

---

## 6. CLI インターフェース要件（例）

- `hldocs-trace-lint lint --root <path> --paths <glob...>`
- `hldocs-trace-lint report --format json|md --out <file>`
- `hldocs-trace-lint fix --dry-run`

---

[目次](../../目次.md) > 仕様 > 共通 > Traceability派生トレーサビリティLintツール要件
