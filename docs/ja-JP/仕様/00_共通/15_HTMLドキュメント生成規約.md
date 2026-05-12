<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlDocumentGeneration
lang: ja-JP
canonical_title: HTMLドキュメント生成規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTMLドキュメント生成規約

# HTMLドキュメント生成規約

本書は、HLDocS において Markdown 正本から HTML ドキュメントを生成する際の基本規約を定義する。

HTML ドキュメントは、Markdown 正本を置き換えるものではなく、人間向け閲覧・説明・検査を目的として生成される Operational Representation である。

本書は、「HLDocS 前提条件」という仕様が参照可能である場合にのみ適用される。

- 「HLDocS 前提条件」が入力として与えられていない場合、または当該仕様に基づく適用可否が確定していない場合、本書に基づく判断・生成・再作成・工程実行を行ってはならない。
- この場合、許可されるのは、提示された文書の受理および存在確認、ならびに前提条件が未参照または未確定である旨の通知のみとする。
- 「HLDocS 前提条件」が入力文書一覧に含まれない場合、生成・再作成・成果物提示を一切行ってはならない。

---

## 1. 基本方針

HLDocS における HTML ドキュメントは、Markdown 正本から生成される read-only Operational Representation とする。

Markdown 正本が canonical であり、HTML ドキュメントは generated output である。

HTML ドキュメントを編集正本として扱ってはならない（MUST NOT）。

HTML ドキュメントから Markdown 正本を逆生成してはならない（MUST NOT）。

---

## 2. 適用範囲

本規約は、Markdown 正本から HTML ドキュメントを生成する範囲までを定義する。

HTML ドキュメントの公開・配信・ホスティングは、本規約の直接範囲外とする。

公開処理は、公開先ごとの公開ツールまたは公開先アダプタで扱う。

GitHub Pages は、公開ツールまたは公開先アダプタの一実装例として扱う。

---

## 3. HTML ドキュメントの配置

HLDocS リポジトリ内で HTML 生成結果を管理する場合、既定の配置候補は以下とする。

```text
docs/ja-JP/HTMLドキュメント
```

このディレクトリは、HTML 生成結果を格納する generated artifact 領域であり、Markdown 正本領域ではない。

HTML 仕様および HTML テンプレートは、独立した正本カテゴリとして扱わず、共通仕様・template・prompt 系に吸収する。

---

## 4. 想定用途

HTML ドキュメント生成は、少なくとも以下の用途を想定する。

### 4.1 全体像把握

仕様全体の構成図、仕様間の関係図、概念図など、概要レベルで人間が把握できる情報を生成する。

### 4.2 入門用説明資料

初学者・利用者向けに、HLDocS の考え方や利用方法を説明する資料を生成する。

### 4.3 API仕様・テスト仕様・使用方法の整理

API 仕様、テスト仕様、使用方法を、人間が見やすく整理された形で表示する。

### 4.4 検査成績表

テスト結果を検査成績表として見やすく整理する。

### 4.5 Traceability 可視化

仕様・テスト仕様・コード・テストコードの Traceability 関係を辿れる形で表示する。

### 4.6 差分・変更履歴の閲覧

restructuring・migration・再作成・patch 等による変更内容を、人間が把握しやすい形で表示する。

### 4.7 レビュー支援

仕様レビュー・テストレビュー・コードレビューを支援する表示を生成する。

---

## 5. Markdown 正本へのリンク

HTML ドキュメントは、必要に応じて Markdown 正本へ遷移できなければならない（MUST）。

HTML ドキュメントは、少なくとも以下のリンクを持つことが望ましい（SHOULD）。

- 元 Markdown ファイルへのリンク
- 該当 `doc_id` への対応情報
- 可能であれば該当 `sec_id` へのリンク
- 関連仕様へのリンク
- 関連テスト仕様へのリンク
- 関連コード・テストコードへのリンク

HTML 上のリンク表示名には、物理ファイル名・物理パス・並び順制御番号を表示してはならない（MUST NOT）。

リンク表示名は、表示名リンク規約に従わなければならない（MUST）。

---

## 6. HTML 生成プロファイル

HTML 生成は、常に全量生成を行うのではなく、生成範囲を profile として選択可能にする。

想定する profile は以下とする。

- `overview`
- `reference`
- `traceability`
- `test-report`
- `full`

未指定時の既定 profile は `overview` とする。

LLM は、指定されていない profile のページ種別を推測で追加生成してはならない（MUST NOT）。

---

## 7. profile 定義

### 7.1 overview

`overview` は、仕様全体像・概念図・入門説明・最小限の HTML ドキュメント間リンクを生成対象とする。

### 7.2 reference

`reference` は、仕様本文、API仕様、使用方法、テスト仕様などの参照用ページを生成対象とする。

### 7.3 traceability

`traceability` は、spec / testspec / code / testcode の関係表示を生成対象とする。

### 7.4 test-report

`test-report` は、テスト結果、検査成績表、証跡表示を生成対象とする。

### 7.5 full

`full` は、定義済み profile の全出力を生成対象とする。

---

## 8. 未生成ページの扱い

指定 profile に含まれないページ種別は生成しない。

未生成ページへのリンクを生成してはならない（MUST NOT）。

必要に応じて、HTML 上に `not generated` と表示してよい（MAY）。

利用者は、`+` / `-` 指示により、profile またはページ種別を調整し、再生成できる。

---

## 9. HTML Site Manifest

HTML ドキュメント間リンク管理のため、HTML Site Manifest を生成しなければならない（MUST）。

HTML Site Manifest は、少なくとも以下を保持する。

- 生成対象ページ一覧
- source markdown
- `doc_id`
- `sec_id`
- 出力 HTML パス
- profile 種別
- 内部リンク可否
- stale 状態

HTML ドキュメント間リンクは、Manifest に存在するページのみを対象としなければならない（MUST）。

Manifest に存在しないページへリンクしてはならない（MUST NOT）。

---

## 10. stale representation

HTML ドキュメントは、生成元 Markdown 正本の変更に追従できていない場合、stale representation として扱う。

stale representation は、Canonical Specification と等価であるとみなしてはならない（MUST NOT）。

HTML ドキュメントは、必要に応じて stale 状態を表示しなければならない（MUST）。

---

## 11. 出力形式

初期段階では、HTML ドキュメントは静的 HTML として生成する。

軽量 JavaScript を含めてもよいが、HTML ドキュメントの canonical 性を主張してはならない（MUST NOT）。

HTML ドキュメントの表示補助として、図・表・ナビゲーション・フィルタを生成してよい（MAY）。

---

## 12. 非目標

本規約は、以下を目的としない。

- HTML を正本として扱うこと
- HTML 側で仕様を編集すること
- HTML から Markdown を逆生成すること
- 公開先ごとのデプロイ手順を定義すること
- GitHub Pages 固有の設定を共通仕様として固定すること
- 完全な Web アプリケーションを定義すること

---

## 13. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- HTML 出力単位
- HTML 出力先ディレクトリ構成
- `doc_id` / `sec_id` の HTML 埋め込み方法
- Markdown 正本へのリンク形式
- Traceability 表示形式
- 検査成績表フォーマット
- HTML Site Manifest の形式
- 公開ツール・公開先アダプタとの関係

---

[目次](../../目次.md) > 仕様 > 共通 > HTMLドキュメント生成規約
