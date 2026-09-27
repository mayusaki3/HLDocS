<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-STWT
lang: ja-JP
canonical_title: 待機State
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State > 待機State

# 待機State

## 1. 目的

待機Stateは、HLDocSが通常運転中であり、現在実行すべきWorkまたはWorkflowが存在しない状態を表す。

待機Stateは、利用者判断待ちを表すStateではない。

## 2. State定義

- State: 待機
- available_workflows: なし
- default_workflow_plan: なし
- restriction_sets: 現時点では追加定義なし

Core基本制限は待機Stateでも常時適用する。

## 3. 進入条件

能力確認完了後またはWork完了後に待機Stateへ進入する場合は、State Machineに当該遷移が定義されていなければならない（MUST）。

## 4. 待機中の処理

待機Stateへ進入したことだけを理由としてWorkflowを開始してはならない（MUST NOT）。

利用者入力の受付および分類はInteractionの責務とする。  
新規Work要求を受けた場合のWork生成、処理対象Stateの選択およびState遷移は、それぞれの仕様に従う。

## 5. 待機Workflow

待機Stateに常駐する「待機Workflow」は定義しない。

利用者との対話を継続するためだけにWorkflowをACTIVEとしてはならない（MUST NOT）。

## 6. Decision Requestとの関係

Active Workflowの実行中に利用者判断が必要になった場合、その判断待ちだけを理由として待機Stateへ遷移してはならない（MUST NOT）。

この場合はCurrent StateおよびActive Workflowを維持し、InteractionのDecision Requestとして扱う。

---

[目次](../../目次.md) > 仕様 > State > 待機State
