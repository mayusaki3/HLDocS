<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlSiteManifest
lang: ja-JP
canonical_title: HTML Site Manifest規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTML Site Manifest規約

# HTML Site Manifest規約

## 1. 目的

本書は、HLDocS における HTML ドキュメント生成結果の論理管理方法を定義する。

HTML Site Manifest は、以下を安定化することを目的とする。

- HTML ドキュメント間リンク
- profile 別部分生成
- stale representation 判定
- restructuring / migration
- Traceability 可視化
- generated output 管理

---

## 2. 基本方針

HTML Site Manifest は、HTML ドキュメント生成結果を管理する generated metadata とする。

Manifest は canonical specification ではない。

Markdown 正本が canonical であり、Manifest は generated operational metadata として扱う。

Manifest を編集正本として扱ってはならない（MUST NOT）。

Manifest から Markdown 正本を逆生成してはならない（MUST NOT）。

---

## 3. Manifest の役割

Manifest は、少なくとも以下を管理する。

- 生成対象 HTML 一覧
- source markdown
- profile
- 内部リンク解決
- stale 状態
- Traceability 関係
- restructuring / migration 関係

Manifest は、HTML ドキュメント間リンクの唯一の論理根拠として扱わなければならない（MUST）。

---

## 4. Manifest 必須項目

Manifest は、少なくとも以下を保持しなければならない（MUST）。

### 4.1 page_id

HTML ページ識別子。

### 4.2 profile

対象 profile。

例：

```text
overview
reference
traceability
test-report
full
```

### 4.3 source_markdown

生成元 Markdown 正本。

### 4.4 canonical_title

表示用 canonical title。

### 4.5 doc_id

対応する `doc_id`。

### 4.6 sec_id

対応する `sec_id` 一覧。

### 4.7 output_html_path

出力 HTML パス。

### 4.8 generated_at

生成日時。

### 4.9 source_hash

生成元 Markdown hash。

### 4.10 stale

stale representation 状態。

### 4.11 link_targets

リンク可能対象 page_id 一覧。

---

## 5. Link 解決規則

HTML ドキュメント間リンクは、Manifest に存在するページのみを対象としなければならない（MUST）。

Manifest に存在しないページへリンクしてはならない（MUST NOT）。

LLM は、未生成ページを推測補完してリンク生成してはならない（MUST NOT）。

---

## 6. stale representation

以下の場合、HTML ドキュメントは stale representation として扱う。

- source_hash 不一致
- source markdown 更新後未再生成
- migration 後未更新
- restructuring 後未更新

stale representation は、Canonical Specification と等価であるとみなしてはならない（MUST NOT）。

Manifest は、stale 状態を保持しなければならない（MUST）。

---

## 7. profile 関係

Manifest は、各 HTML ページがどの profile に属するかを保持しなければならない（MUST）。

1ページが複数 profile に属してもよい（MAY）。

---

## 8. restructuring / migration

Manifest は、restructuring / migration 関係を保持してよい（MAY）。

例：

```text
old_page_id
↓
new_page_id
```

```text
old_sec_id
↓
new_sec_id
```

など。

---

## 9. Traceability 関係

Manifest は、少なくとも以下の Traceability 関係を保持してよい（MAY）。

```text
spec
↓
testspec
↓
code
↓
testcode
```

Manifest は、reverse traceability を保持してよい（MAY）。

---

## 10. 非目標

本規約は、以下を目的としない。

- CMS
- DB サーバ
- 動的検索サーバ
- GitHub Pages 固定
- 完全な Web アプリケーション

---

## 11. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- Manifest JSON 形式
- page_id 形式
- source_hash 算出方法
- stale 判定アルゴリズム
- migration relation format
- reverse link format
- profile inheritance

---

[目次](../../目次.md) > 仕様 > 共通 > HTML Site Manifest規約
