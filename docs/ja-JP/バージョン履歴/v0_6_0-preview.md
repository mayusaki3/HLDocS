<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260605-190000Z-D9R4
lang: ja-JP
canonical_title: v0.6.0-preview バージョン履歴
document_type: note
canonical_document: true
-->

[目次](../目次.md) > バージョン履歴 > v0.6.0-preview

# v0.6.0-preview バージョン履歴

v0.5.0-preview の機能追加・運用強化版。

---

## 状態

以下は利用可能。

* HLDocS コア仕様
* Traceability 基盤
* meta/apply モード
* recreate invariant
* ChatGPT UI ベース運用
* ui_copy ベース運用
* ドキュメント参照・ナビゲーション規約
* 成果物更新運用
* LLM_WORKSPACE 運用
* GitHub 非依存運用
* 多言語 README 運用

---

## v0.6.0-preview の主な追加内容

### ドキュメント参照・ナビゲーション規約

以下を追加。

* 論理構造と物理構造の分離
* 表示名と物理名の分離
* 表示名リンク規約
* 階層リンク規約
* 目次ドキュメント運用
* 目次ドキュメント名の一意性要件

---

### 成果物更新運用

以下を追加。

* GitHub 利用時の正本取得手順
* GitHub 利用時の更新優先順位
* 全文差し替え優先運用
* 記憶ベース更新禁止
* 正本未取得時の FAIL-FAST 運用
* GitHub・添付・チャットの優先順位規定

---

### LLM_WORKSPACE

以下を追加。

* Request
* Worklog
* Handover

の運用規約。

また、

* Worklog を作業状態の正本とする
* GitHub 非依存で作業継続可能とする
* チャット移行時の運用を規定する

ことを追加した。

---

## 現時点の推奨利用方法

現時点では、prompt/template のみでの完全自己完結生成は未完成である。

そのため、現在は以下を推奨する。

1. `docs/ja-JP/仕様` を LLM に提示
2. 共通生成プロンプト・共通テンプレートを利用
3. document_type 別テンプレート・生成プロンプトを利用
4. HLDocS 規約に従って生成・検証・再構成を行う
5. 長期作業では LLM_WORKSPACE を利用する

---

## 現時点の制約

以下は継続開発中。

* prompt/template の完全自己完結生成
* HTML visualization pipeline
* specification restructuring workflow
* Traceability migration workflow
* validator integration

---

## 今後の予定

### Phase 2

* 技術検証（note）運用規約
* validator workflow
* Traceability lint
* prompt composition support
* workspace automation support

実プロジェクトで継続検証予定。

---

### Phase 3

Markdown → HTML visualization 規約を追加予定。

主目的：

* 人間向け閲覧
* Traceability 可視化
* 差分・再構成可視化
* LLM 補助 UI

Markdown canonical / HTML generated の片方向構成を前提とする。

---

### Planned v1.0

以下を目標とする。

* fully self-contained generation
* stable reconstruction workflow
* complete validation integration
* production-grade operation

---

[目次](../目次.md) > バージョン履歴 > v0.6.0-preview
