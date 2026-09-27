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

本書は、HLDocSにおけるWorkflowの共通構造、責務および実行状態を定義する。

## 2. Workflow

Workflowは、Workを進行させる処理単位である。  
WorkflowはStateにより利用可能範囲を制約され、Workflow Planによって実行予定を管理される。

同時にACTIVEとなるWorkflowは一つのWorkにつき最大1件とする（MUST）。

## 3. 実行状態

Workflow Plan内のWorkflowは少なくとも次の状態を持つ。

- PENDING
- ACTIVE
- SUSPENDED
- COMPLETED
- SKIPPED

COMPLETEDとSKIPPEDを同一の意味として扱ってはならない（MUST NOT）。

## 4. 開始

Workflowを開始するには、少なくとも次を満たさなければならない（MUST）。

- Current Stateのavailable_workflowsに登録されている。
- 現在のWorkflow Planに含まれている。
- 状態がPENDINGである。
- 他のActive Workflowが存在しない。
- Workflow固有の開始条件を満たす。
- 必要なRestriction Setを適用できる。

Coreは条件を検証した後、WorkflowをACTIVEへ変更する。

## 5. 責務

Workflowは次を担当する。

- Workflow目的の達成に必要な処理進行
- 必要なSubFlowの選択および順序
- Workflow固有Restriction Setの宣言
- Issueの発見および影響分析
- Workflow終了条件の判定
- 必要なState遷移候補の要求

利用者との直接対話はInteractionを介さなければならない（MUST）。

## 6. 完了

Workflow終了条件を満たした場合、WorkflowはCoreへ完了要求を行う。

Coreは終了条件、Execution ContextおよびRestriction Contextを検証した後、ACTIVEからCOMPLETEDへの変更を適用する。

Workflow完了をIssue解決またはWork完了として扱ってはならない（MUST NOT）。

## 7. Workflow Plan

Stateのdefault_workflow_planから生成されたPlanは、当該実行の承認済み初期Planとして扱う。

Plan内の次のPENDING Workflowは、開始条件を満たす場合に開始してよい（MAY）。

Plan外Workflowを必要とする場合は、Workflow候補の発見とPlan変更を分離しなければならない（MUST）。  
Workflowの追加、削除、並べ替えまたはSKIPPED化は、利用者の明示的な指示または承認なしに確定してはならない（MUST NOT）。

## 8. State遷移

WorkflowはState遷移候補を提示または遷移要求の契機を生成できるが、自らCurrent Stateを変更してはならない（MUST NOT）。

State遷移候補の選択が必要な場合はState選択ルールに従う。  
遷移可否はState Machineが判断し、変更適用はCoreが行う。

---

[目次](../../目次.md) > 仕様 > Workflow > Workflow仕様
