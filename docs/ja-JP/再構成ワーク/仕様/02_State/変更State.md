<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260928-191900Z-STCH
lang: ja-JP
canonical_title: 変更State
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State > 変更State

# 変更State(状態)

## 1. 目的

変更State(状態)は、利用者が明示的に要求した正本または作業対象の変更を実行するための実行環境を定義する。

## 2. State定義

- State: 変更
- plan_owner: WORK
- work_acceptance:
  - 正本または作業対象の追加、修正、削除その他の変更を明示的に目的とするWork
- available_workflows:
  - 変更調査
  - 変更対処
  - 変更検証
- default_workflow_plan:
  1. 変更調査
  2. 変更対処
  3. 変更検証
- restriction_sets: 現時点では追加定義なし

## 3. 境界

参照、確認、説明または分析だけを目的とし、変更を要求しないWorkを本Stateの候補としてはならない（MUST NOT）。

参照処理中に変更の必要性が判明したことだけを、変更要求として扱ってはならない（MUST NOT）。

変更対象、変更内容または必要な利用者承認が確定できない場合、推測して変更してはならない（MUST NOT）。

明示的な変更要求であっても、対処前に対象、現在状態、適用可否および必要な対処を調査しなければならない（MUST）。

## 4. Workとの関係

本StateのWorkflow Plan(ワークフロー計画)はOwner=`WORK`とし、対象Work IDを関連付ける。

Work Purposeがwork_acceptanceに適合しない場合、本Stateを候補としてはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State > 変更State
