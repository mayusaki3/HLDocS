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
- plan_owner
- work_acceptance
- available_workflows
- default_workflow_plan
- system_plan_changes
- restriction_sets

Stateは処理を実行する主体ではない。

## 3. plan_owner

plan_ownerは、当該Stateでdefault_workflow_planから生成するWorkflow Plan(ワークフロー計画)のOwnerを宣言する。

- SYSTEM: HLDocS自身の通常運転処理
- WORK: 利用者Work(作業)に属する処理

plan_ownerがWORKの場合、対象Work IDをWorkflow Planへ関連付ける。plan_ownerがSYSTEMの場合、Plan所有のためだけにWorkを生成してはならない（MUST NOT）。

default_workflow_planを持たないStateではplan_ownerを省略してよい（MAY）。

## 4. work_acceptance

work_acceptanceは、当該Stateが処理対象として受け入れられるWorkまたはWork Candidate(作業候補)の範囲を宣言する。

利用者Workを処理するStateは、State選択に必要な範囲でwork_acceptanceを定義しなければならない（MUST）。

work_acceptanceはState選択の候補抽出根拠であり、State遷移許可そのものではない。

SYSTEM専用StateまたはWorkを処理しないStateではwork_acceptanceを省略してよい（MAY）。

## 5. available_workflows

available_workflowsは、当該Stateで利用可能なWorkflowを定義する。

当該StateでWorkflowを開始する場合、そのWorkflowはavailable_workflowsに登録されていなければならない（MUST）。

available_workflowsへの登録は、そのWorkflowが現在のWorkflow Planに含まれること、または直ちに実行してよいことを意味しない。

## 6. default_workflow_plan

default_workflow_planは、当該Stateで新たにWorkflow Planを生成する場合の標準構成を宣言する。

default_workflow_planは任意とする。  
default_workflow_planが存在しないStateへ進入したことだけを理由としてWorkflowを開始してはならない（MUST NOT）。

default_workflow_planから生成されたWorkflow PlanはExecution Contextに属する実行インスタンスであり、State定義そのものではない。

実行中のWorkflow Planを変更してもStateのdefault_workflow_planを変更してはならない（MUST NOT）。

plan_ownerがSYSTEMであり、実行中Planの構成変更を許可する必要があるStateは、`system_plan_changes`として許可する変更条件と変更内容を宣言できる（MAY）。

`system_plan_changes`が未定義の場合、そのStateのSYSTEM Planについて追加、削除、並べ替えまたはSKIPPED化を許可してはならない（MUST NOT）。

plan_ownerがWORKの場合、`system_plan_changes`をPlan変更承認の代替として使用してはならない（MUST NOT）。

State進入時にCurrent Workflow Planが存在する場合、Core(中核)はそのPlanが当該State、plan_ownerおよび対象Workとの関係で再利用可能か検証しなければならない（MUST）。

再利用可能と確認できない既存Planを暗黙に復元してはならない（MUST NOT）。

同一目的の有効なCurrent Workflow Planが既に存在する場合、default_workflow_planから重複Planを生成してはならない（MUST NOT）。

## 7. restriction_sets

restriction_setsは、当該Stateで適用するRestriction Setを宣言する。

宣言されたRestriction SetはState進入時にCoreによって取得、検証および適用されなければならない（MUST）。

宣言されたRestriction Setを適用できない場合、当該Stateで通常処理を開始してはならない（MUST NOT）。

## 8. Stateが行ってはならないこと

Stateは次を行ってはならない（MUST NOT）。

- 自らState遷移する。
- State遷移可否を決定する。
- Workflowを選択または開始する。
- Workflow Planを実行時に変更する。
- Restriction Setを適用または解除する。
- 利用者と直接対話する。
- Toolを実行する。

## 9. State Machineとの境界

Stateは自身の実行環境を定義する。  
State間の遷移関係、Initial Stateおよび遷移可否はState Machineが定義する。

State個別仕様にState間の遷移関係を重複して定義してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State > State仕様
