<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260928-000000Z-STIR
lang: ja-JP
canonical_title: 情報参照State
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State > 情報参照State

# 情報参照State

## 1. 目的

情報参照Stateは、HLDocSが参照可能な正本および関連情報を読み取り、利用者の問い合わせへ回答するための実行環境を定義する。

## 2. State定義

- State: 情報参照
- plan_owner: WORK
- work_acceptance:
  - 情報の参照、確認、説明または分析を目的とし、正本の変更を要求しないWork
- available_workflows:
  - 情報参照
- default_workflow_plan:
  1. 情報参照
- restriction_sets: 現時点では追加定義なし

## 3. 境界

本Stateでは、参照対象の変更をWorkの目的として実行してはならない（MUST NOT）。

参照の結果として変更が必要と判明しても、それだけを根拠として変更処理へ移行してはならない（MUST NOT）。

## 4. Workとの関係

本StateのWorkflow PlanはOwner=WORKとし、対象Work IDを関連付ける。

Work Purposeがwork_acceptanceに適合しない場合、本Stateを候補としてはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State > 情報参照State
