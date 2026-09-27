<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-WF01
lang: ja-JP
canonical_title: Workflow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Workflow仕様

# Workflow仕様

## 1. 目的

本書は、HLDocSにおけるWorkflowおよびWorkflow Planの共通構造、責務、実行状態を定義する。

## 2. Workflow

Workflowは、HLDocSの処理を進行させる実行単位である。

Workflowは必ずしも利用者Workに属するとは限らない。  
SYSTEM処理と利用者Work処理は、Workflow PlanのOwnerによって区別する。

同時にACTIVEとなるWorkflowはExecution Context上で最大1件とする（MUST）。

## 3. Workflow Plan

Workflow Planは現在実行するWorkflow列の実行インスタンスであり、Execution Contextに保持する。

Workflow Planは次のOwnerを持つ。

- SYSTEM
- WORK

Owner=WORKの場合はWork IDを保持する。  
Owner=SYSTEMの場合はWork IDを要求してはならない（MUST NOT）。

## 4. 実行状態

Workflow Plan内のWorkflowは少なくともPENDING、ACTIVE、SUSPENDED、COMPLETED、SKIPPEDを持つ。

COMPLETEDとSKIPPEDを同一の意味として扱ってはならない（MUST NOT）。

## 5. Plan生成

Stateへ進入し、そのState用のCurrent Workflow Planが存在せず、default_workflow_planが定義されている場合、Coreはdefault_workflow_planからPlanを生成してよい（MAY）。

SYSTEM用StateではOwner=SYSTEMとする。  
利用者Workを処理するStateではOwner=WORKとし、Current Workを関連付ける。

同一の実行対象について既存Planを復元すべき場合、default_workflow_planから重複生成してはならない（MUST NOT）。

## 6. Workflow開始

Workflowを開始するには、少なくとも次を満たさなければならない（MUST）。

- Current Stateのavailable_workflowsに登録されている。
- Current Workflow Planに含まれている。
- 状態がPENDINGである。
- 他のActive Workflowが存在しない。
- Workflow固有の開始条件を満たす。
- 必要なRestriction Setを適用できる。

Coreは条件を検証した後、WorkflowをACTIVEへ変更する。

## 7. Workflowの責務

Workflowは、目的達成に必要な処理進行、SubFlowの選択・順序、Restriction Set宣言、Issueの発見・影響分析、終了条件判定、必要なState遷移候補の要求を担当する。

利用者との直接対話はInteractionを介さなければならない（MUST）。

## 8. Workflow完了

Workflow終了条件を満たした場合、WorkflowはCoreへ完了要求を行う。

Coreは終了条件、Execution ContextおよびRestriction Contextを検証した後、ACTIVEからCOMPLETEDへの変更を適用する。

Workflow完了をIssue解決、Work完了またはState遷移完了として扱ってはならない（MUST NOT）。

## 9. Plan変更

Plan外Workflowを必要とする場合は、Workflow候補の発見とPlan変更を分離しなければならない（MUST）。

Owner=WORKのPlanについて、Workflowの追加、削除、並べ替えまたはSKIPPED化は利用者の明示的な指示または承認なしに確定してはならない（MUST NOT）。

Owner=SYSTEMのPlanは、対応するシステム仕様またはState仕様に明示された規則なしに変更してはならない（MUST NOT）。

## 10. State遷移

WorkflowはState遷移候補を提示できるが、自らCurrent Stateを変更してはならない（MUST NOT）。

State遷移候補の選択が必要な場合はState選択ルールに従う。  
遷移可否はState Machineが判断し、変更適用はCoreが行う。

---

[目次](../../目次.md) > 仕様 > Workflow > Workflow仕様
