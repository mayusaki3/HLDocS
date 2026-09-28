<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-ST01
lang: ja-JP
canonical_title: State仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State > State仕様

# State(状態)仕様

## 1. 目的

本書は、HLDocSにおけるState個別仕様の共通構造および責務を定義する。

## 2. Stateの責務

State(状態)は、State Machine(状態遷移機構)上の一つの実行環境を宣言的に定義する。

State個別仕様は、少なくとも必要に応じて次を定義する。

- State識別子または名称
- Stateの目的
- available_workflows
- default_workflow_plan
- restriction_sets

Stateは処理を実行する主体ではない。

## 3. available_workflows

available_workflowsは、当該Stateで利用可能なWorkflowを定義する。

当該StateでWorkflowを開始する場合、そのWorkflowはavailable_workflowsに登録されていなければならない（MUST）。

available_workflowsへの登録は、そのWorkflowが現在のWorkflow Planに含まれること、または直ちに実行してよいことを意味しない。

## 4. default_workflow_plan

default_workflow_planは、当該Stateで新たにWorkflow Planを生成する場合の標準構成を宣言する。

default_workflow_planは任意とする。  
default_workflow_planが存在しないStateへ進入したことだけを理由としてWorkflowを開始してはならない（MUST NOT）。

default_workflow_planから生成されたWorkflow PlanはExecution Contextに属する実行インスタンスであり、State定義そのものではない。

実行中のWorkflow Planを変更してもStateのdefault_workflow_planを変更してはならない（MUST NOT）。

同一Workで当該State用の既存Workflow Planを復元すべき場合、default_workflow_planから新しいPlanを重複生成してはならない（MUST NOT）。

## 5. restriction_sets

restriction_setsは、当該Stateで適用するRestriction Setを宣言する。

宣言されたRestriction SetはState進入時にCoreによって取得、検証および適用されなければならない（MUST）。

宣言されたRestriction Setを適用できない場合、当該Stateで通常処理を開始してはならない（MUST NOT）。

## 6. Stateが行ってはならないこと

Stateは次を行ってはならない（MUST NOT）。

- 自らState遷移する。
- State遷移可否を決定する。
- Workflowを選択または開始する。
- Workflow Planを実行時に変更する。
- Restriction Setを適用または解除する。
- 利用者と直接対話する。
- Toolを実行する。

## 7. State Machineとの境界

Stateは自身の実行環境を定義する。  
State間の遷移関係、Initial Stateおよび遷移可否はState Machineが定義する。

State個別仕様にState間の遷移関係を重複して定義してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State > State仕様
