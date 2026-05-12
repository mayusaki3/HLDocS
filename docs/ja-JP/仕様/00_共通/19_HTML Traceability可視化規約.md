<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlTraceabilityVisualization
lang: ja-JP
canonical_title: HTML Traceability可視化規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTML Traceability可視化規約

# HTML Traceability可視化規約

## 1. 目的

本書は、HLDocS における Traceability 関係の HTML 可視化方法を定義する。

本規約は、以下を安定化することを目的とする。

- spec / testspec / code / testcode 関係可視化
- reverse traceability
- coverage 可視化
- orphan relation 検出
- restructuring / migration 可視化
- review navigation

---

## 2. 基本方針

HTML Traceability 可視化は、Markdown 正本に存在する Traceability 情報を、人間が辿りやすい形へ変換する generated operational representation とする。

Traceability HTML は canonical specification ではない。

Traceability HTML を編集正本として扱ってはならない（MUST NOT）。

Traceability HTML から Markdown 正本を逆生成してはならない（MUST NOT）。

---

## 3. 基本 Traceability 関係

少なくとも以下の関係を可視化してよい（MAY）。

```text
spec
↓
testspec
↓
code
↓
testcode
```

また、以下も表示してよい（MAY）。

- reverse traceability
- cross reference
- review relation
- migration relation
- restructuring relation

---

## 4. Traceability Page

Traceability 可視化は、少なくとも以下の単位で表示してよい（MAY）。

### 4.1 Document Traceability

document 単位の Traceability 表示。

### 4.2 sec_id Traceability

`sec_id` 単位の Traceability 表示。

### 4.3 ref_id Traceability

`ref_id` 単位の Traceability 表示。

### 4.4 Coverage Traceability

coverage 状態を含む Traceability 表示。

---

## 5. Coverage 表示

Coverage 表示では、少なくとも以下を表示してよい（MAY）。

- implemented
- tested
- untested
- orphan
- missing relation
- stale relation

Coverage 表示は、レビュー支援用途を想定する。

---

## 6. reverse traceability

Traceability HTML は、reverse traceability を表示してよい（MAY）。

例：

```text
testcode
↑
code
↑
testspec
↑
spec
```

reverse traceability は、影響範囲分析・migration・restructuring に利用してよい（MAY）。

---

## 7. orphan relation

以下を orphan relation として扱ってよい（MAY）。

- relation target 不存在
- reverse relation 不一致
- stale relation
- missing reference

orphan relation は、HTML 上で警告表示してよい（MAY）。

---

## 8. stale relation

以下を stale relation として扱ってよい（MAY）。

- source markdown 更新後未同期
- migration 後未同期
- restructuring 後未同期
- stale representation 間 relation

stale relation は、Canonical Specification と等価であるとみなしてはならない（MUST NOT）。

---

## 9. restructuring / migration

Traceability HTML は、restructuring / migration 関係を表示してよい（MAY）。

想定例：

```text
old_sec_id
↓
new_sec_id
```

```text
old_doc_id
↓
new_doc_id
```

```text
old_page_id
↓
new_page_id
```

---

## 10. review navigation

Traceability HTML は、レビュー支援 navigation を提供してよい（MAY）。

想定例：

- missing relation list
- stale relation list
- orphan relation list
- untested list
- unimplemented list
- review target list

---

## 11. Link 解決

Traceability HTML 間リンクは、HTML Site Manifest に基づいて解決しなければならない（MUST）。

Manifest に存在しないページへリンクしてはならない（MUST NOT）。

未生成ページは、必要に応じて `not generated` と表示してよい（MAY）。

---

## 12. 表示形式

Traceability 可視化では、少なくとも以下の表示形式を利用してよい（MAY）。

- graph
- matrix
- tree
- table
- reverse navigation
- dependency view

表示形式は canonical specification ではない。

---

## 13. profile 関係

Traceability 可視化は、主に以下 profile に属する。

- `traceability`
- `full`

必要に応じて `overview` に概要 graph を含めてよい（MAY）。

---

## 14. 非目標

本規約は、以下を目的としない。

- graph database
- dynamic graph server
- AI automatic inference
- relation 推測補完
- GitHub Pages 固定

LLM は、存在しない relation を推測生成してはならない（MUST NOT）。

---

## 15. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- graph format
- matrix format
- dependency notation
- orphan severity
- stale severity
- review navigation format
- cross-project traceability
- multi-repository traceability
- external adapter traceability

---

[目次](../../目次.md) > 仕様 > 共通 > HTML Traceability可視化規約
