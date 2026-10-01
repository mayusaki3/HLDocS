<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-STCP
lang: ja-JP
canonical_title: 能力確認State
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State > 能力確認State

# 能力確認State

## 1. 目的

能力確認Stateは、現在のHLDocSで利用可能な能力を検証し、その結果を利用者へ通知するための実行環境を定義する。

能力確認Stateは、HLDocSの起動そのものを担当しない。

## 2. State定義

- State: 能力確認
- plan_owner: SYSTEM
- available_workflows:
  - HLDocS能力確認
- default_workflow_plan:
  1. HLDocS能力確認
- system_plan_changes: なし
- restriction_sets: 現時点では追加定義なし

Core基本制限は能力確認Stateでも常時適用する。

## 3. 進入

能力確認StateはState MachineのInitial Stateとして使用できる。

能力確認Stateへ進入し、対応するSYSTEM Workflow Planが存在しない場合は、default_workflow_planからOwner=SYSTEMの実行用Workflow Planを生成する。

能力確認のためだけにWorkを生成してはならない（MUST NOT）。

## 4. 能力確認

能力確認State自身は能力検証を実行しない。  
能力検証はHLDocS能力確認Workflowが行う。

Stateへ登録されていることだけを理由として、能力を利用可能と通知してはならない（MUST NOT）。

## 5. 終了

SYSTEM Workflow Planが完了した場合、待機StateへのState遷移を要求できる状態となる。

State自身が遷移を実行してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State > 能力確認State
