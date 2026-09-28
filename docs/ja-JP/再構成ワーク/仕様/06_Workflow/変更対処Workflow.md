<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-080000Z-WFCA
lang: ja-JP
canonical_title: 変更対処Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 変更対処Workflow

# 変更対処Workflow(ワークフロー)

## 1. 目的

変更調査Workflow(ワークフロー)が生成したTarget List(対処対象リスト)に従って、許可された変更を実施する。

## 2. 開始条件

- Current Stateが変更Stateである。
- 本WorkflowがCurrent Workflow Plan内で`PENDING(未実行)`である。
- 変更調査Workflowが`COMPLETED(完了)`である。
- 対象WorkのWork Context(作業コンテキスト)からArtifact Type=`TARGET_LIST`のTarget Listを参照できる。
- 対処に必要なRestriction Context(制限コンテキスト)を適用できる。

## 3. 処理

1. Target Listの各項目について最新の対象状態を確認する。
2. 調査時点から状態が変化している場合は、そのまま対処せず再評価する。
3. 対処可能かつ必要な承認根拠を満たす項目だけを処理する。
4. Core(中核)の検証を経て必要なTool(ツール)または能力提供手段を実行する。
5. 各項目の実行結果をTarget Listに対応付けたArtifact(作業成果物)として記録する。

## 4. 制限

Target Listに存在しない変更を暗黙に追加してはならない（MUST NOT）。

Target Listの内容と実体が不一致の場合、調査結果を正しいものとして強制適用してはならない（MUST NOT）。

対処不能、失敗または追加判断が必要な項目を成功として扱ってはならない（MUST NOT）。

## 5. 終了

Target Listの対処対象について、実行結果または実行不能理由を確定できた場合にWorkflow完了要求を行う。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更対処Workflow
