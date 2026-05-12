<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlOutputUnit
lang: ja-JP
canonical_title: HTML出力単位規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTML出力単位規約

# HTML出力単位規約

## 1. 目的

本書は、HLDocS における HTML ドキュメント生成時の出力単位を定義する。

本規約は、以下を安定化することを目的とする。

- HTML ページ粒度
- profile 別生成範囲
- HTML ドキュメント間リンク
- restructuring / migration
- Traceability 可視化
- generated artifact 管理

---

## 2. 基本方針

HTML ドキュメントは、論理単位ごとに生成しなければならない（MUST）。

物理ファイル単位のみを基準として HTML 出力単位を決定してはならない（MUST NOT）。

HTML 出力単位は、以下を基準として決定する。

- document_type
- profile
- logical structure
- Traceability 関係
- review / navigation 用途

---

## 3. HTML 出力単位

HTML 出力単位は、少なくとも以下を想定する。

### 3.1 Overview Page

仕様全体像・構成図・概念図・入門説明を表示するページ。

主に `overview` profile に属する。

---

### 3.2 Document Page

Markdown 1文書に対応する閲覧ページ。

主に `reference` profile に属する。

Document Page は、Markdown 正本との対応関係を保持しなければならない（MUST）。

---

### 3.3 Section Page

必要に応じて、`sec_id` 単位で分離されたページを生成してよい（MAY）。

Section Page は、review・Traceability・大型仕様分割用途を想定する。

---

### 3.4 Traceability Page

spec / testspec / code / testcode 関係を表示するページ。

主に `traceability` profile に属する。

---

### 3.5 Test Report Page

検査成績表・テスト結果・証跡を表示するページ。

主に `test-report` profile に属する。

---

### 3.6 Index Page

HTML ドキュメント一覧および navigation を提供するページ。

---

## 4. Overview Page

Overview Page は、少なくとも以下を表示してよい（MAY）。

- 構成図
- 概念図
- document_type 関係
- Traceability 概要
- overview navigation
- preview 状態警告
- stale representation 警告

Overview Page は、Markdown 正本の完全表示を目的としない。

---

## 5. Document Page

Document Page は、Markdown 正本に最も近い HTML 表現とする。

Document Page は、少なくとも以下を保持しなければならない（MUST）。

- canonical_title
- doc_id
- sec_id
- Markdown 正本リンク
- related links

Document Page は、Markdown 正本そのものとして扱ってはならない（MUST NOT）。

---

## 6. Section Page

Section Page は、必要に応じて生成してよい（MAY）。

Section Page を生成する場合、少なくとも以下を保持しなければならない（MUST）。

- source Document Page
- doc_id
- sec_id
- reverse navigation

Section Page は、単独 canonical specification とみなしてはならない（MUST NOT）。

---

## 7. Traceability Page

Traceability Page は、少なくとも以下を表示してよい（MAY）。

```text
spec
↓
testspec
↓
code
↓
testcode
```

また、以下を表示してよい（MAY）。

- reverse traceability
- orphan relation
- missing relation
- coverage state
- stale relation

---

## 8. Test Report Page

Test Report Page は、少なくとも以下を表示してよい（MAY）。

- PASS / FAIL
- test_id
- evidence
- environment
- logs
- screenshots
- related spec
- related testspec
- related code

Test Report Page は、検査成績表用途を想定する。

---

## 9. Index Page

Index Page は、HTML ドキュメント navigation を提供する。

Index Page は、少なくとも以下を保持してよい（MAY）。

- profile navigation
- document_type navigation
- generated page list
- stale page list
- preview warning

---

## 10. profile 関係

HTML 出力単位は、profile により生成有無が変化してよい（MAY）。

例：

- `overview`
  - Overview Page
  - 最小限 navigation

- `reference`
  - Document Page
  - Index Page

- `traceability`
  - Traceability Page

- `test-report`
  - Test Report Page

- `full`
  - 全ページ種別

---

## 11. Link 解決

HTML ドキュメント間リンクは、HTML Site Manifest に基づいて解決しなければならない（MUST）。

Manifest に存在しないページへリンクしてはならない（MUST NOT）。

未生成ページは、必要に応じて `not generated` と表示してよい（MAY）。

---

## 12. restructuring / migration

HTML 出力単位は、restructuring / migration によって変更されてよい（MAY）。

ただし、以下を保持しなければならない（MUST）。

- migration relation
- reverse navigation
- stale state

---

## 13. 非目標

本規約は、以下を目的としない。

- HTML CMS
- DB サーバ
- 動的 SPA
- GitHub Pages 固定
- 完全な UI framework

---

## 14. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- page_id 命名規則
- sec_id page split 規則
- reverse navigation format
- page hierarchy
- overview graph format
- report page format
- Traceability graph format
- stale visualization format

---

[目次](../../目次.md) > 仕様 > 共通 > HTML出力単位規約
