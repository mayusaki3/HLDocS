<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-CORE
lang: ja-JP
canonical_title: Core仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Core仕様

# Core(中核)仕様

## 1. 目的

本書は、HLDocS Core(中核)の責務と、通常運転および復旧に共通する実行制御を定義する。

## 2. Coreの責務

Coreは次を担当する。

- HLDocSシステム起動制御
- Execution Contextの正本管理
- Execution Contextに対する変更要求の検証および適用
- Restriction Context(制限コンテキスト)の構築および強制
- 登録済み仕様要素の参照機構
- State Machineへの制御移譲
- State Machineへ移譲できない場合の復旧制御

Coreは、作業の意味上の処理内容を決定する機構ではない。

## 3. Coreが行ってはならないこと

Coreは次を行ってはならない（MUST NOT）。

- 通常作業で利用するWorkflowを意味判断によって選択する。
- Workflow PlanへWorkflowを独断で追加、削除または並べ替える。
- WorkflowまたはSubFlowの処理内容を決定する。
- State Machineに代わって通常のState遷移可否を決定する。
- 個別Restriction Setの内容を独断で変更する。
- 制限確認を迂回して処理を実行する。

## 4. Execution Context

Coreは、実行状態をExecution Contextとして管理しなければならない（MUST）。

Execution Context(実行コンテキスト)は、少なくとも次を表現できなければならない（MUST）。

- Current State
- Current Workflow Plan
- Active Workflow
- Suspended Workflow
- Current Work
- Work Contexts
- Capability Context

Current Workflow PlanはWorkの有無に依存しない現在の実行Planとする。

Current Workflow PlanはOwnerを持たなければならない（MUST）。  
Ownerは少なくとも次を区別する。

- SYSTEM: HLDocS自身の通常運転処理
- WORK: 利用者Workに属する処理

OwnerがWORKの場合は、対応するWork IDを一意に関連付けなければならない（MUST）。  
OwnerがSYSTEMの場合は、存在しないWorkを生成してPlanの所有者としてはならない（MUST NOT）。

Work Context(作業コンテキスト)は少なくともWork ID、Purpose、Status、Issuesおよび任意のArtifacts(作業成果物)を保持できる。

ArtifactsはWork固有の中間成果物または結果であり、作業対象正本またはExecution Context(実行コンテキスト)の確定実行状態を代替しない。

Work Statusは、少なくとも次を扱う。

- ACTIVE
- SUSPENDED
- COMPLETED

同時にACTIVEとなるWorkは最大1件とする（MUST）。

同時に`ACTIVE(実行中)`となるWorkflowは最大1件とする（MUST）。`SUSPENDED(中断中)` Workflowが存在していても別WorkflowをACTIVEにできるが、その組み合わせが対応Workflow仕様で許可され、復帰先を一意に管理できなければならない（MUST）。

Workflow Planの実行状態とIssueの状態を同一の状態として扱ってはならない（MUST NOT）。

Capability Context(能力コンテキスト)は登録済みCapabilityについて現在の実行環境で確認した利用可能性を保持する。詳細はCapability Context仕様に従う。

Capability Contextの`AVAILABLE`を、現在の処理における実行許可またはRestriction Contextの代替として扱ってはならない（MUST NOT）。

## 5. Execution Contextの変更

State Machine、選択ルール、Workflowその他のSubsystemは、Execution Contextを直接変更してはならない（MUST NOT）。  
Execution Contextを変更する場合は、Coreへ変更要求を行わなければならない（MUST）。

Coreは変更要求について、少なくとも次を確認しなければならない（MUST）。

- 現在のExecution Contextとの整合性
- 要求元が当該変更を要求できること
- 有効なRestriction Contextに違反しないこと
- 利用者承認を必要とする変更では、必要な承認根拠が存在すること

Workflow(ワークフロー)がWork Context内のArtifactを生成または更新する場合もExecution Context変更要求として扱い、Coreが対象Work、要求元および変更内容を検証して適用しなければならない（MUST）。

## 6. Workflow Plan変更

Stateのdefault_workflow_planから新規Planを生成する場合、そのState仕様で定義されたPlanを初期Planとして生成してよい（MAY）。

承認済みまたはState仕様により確定したWorkflow Plan内の通常の実行状態遷移は、各仕様の条件を満たす場合に適用してよい（MAY）。

実行中Planに対する次の変更は、利用者WorkをOwnerとする場合、利用者による明示的な指示または承認なしに確定してはならない（MUST NOT）。

- Workflowの追加
- Workflowの削除
- Workflow順序の変更
- WorkflowのSKIPPED化

SYSTEM Planの変更は、対応するStateまたはシステム仕様に明示された規則なしに確定してはならない（MUST NOT）。

SYSTEM Plan変更では利用者承認を一般的な代替根拠としてはならない（MUST NOT）。Coreは、変更対象、変更内容、仕様上の許可根拠および現在の変更条件を検証しなければならない（MUST）。

SYSTEM Planの変更規則が定義されていない場合、CoreはPlan構成を維持する。処理を継続できない場合も、Coreが未定義のPlan変更を生成して回避してはならない（MUST NOT）。

SYSTEM Plan変更によってWork(作業)を暗黙に生成または変更してはならない（MUST NOT）。

既存Plan内WorkflowのRe-run(再実行)およびRe-run Sequence(再実行列)はPlan構成変更として扱わない。CoreはRe-run要求について、対象WorkflowがCurrent Planに存在すること、再実行理由が対応仕様に適合すること、同時ACTIVE制約およびRestriction Context(制限コンテキスト)を満たすことを検証しなければならない（MUST）。

Re-run Sequenceでは、Coreは一つのSUSPENDED Workflowをreturn_toとして保持し、Sequence内Workflowを順番に再実行する。Sequenceの中間Workflowを新たなSUSPENDED復帰先として積み重ねてはならない（MUST NOT）。

## 7. Restriction Context

Coreは、常時適用する安全側の基本制御を保持しなければならない（MUST）。

通常運転では、現在の実行位置に応じてState、Workflow、SubFlowのRestriction Setを必要な範囲で読み込み、Restriction Contextを構築する。

下位のRestriction Setは上位の制限を緩和してはならない（MUST NOT）。  
必要なRestriction Setを取得または解釈できない場合は、制限なしとして処理を継続してはならない（MUST NOT）。

## 8. State Machineへの移譲

Coreは起動後、State Machine仕様を必要な範囲で参照し、制御移譲を試行する。

移譲成功後は、通常のState遷移判断をState Machineへ委ねなければならない（MUST）。  
CoreはState Machineが許可した遷移要求について、Execution ContextおよびRestriction Context上の整合性を確認した後にCurrent Stateへ適用する。

## 9. 復旧

State Machineへの移譲に失敗した場合、Coreは通常運転を開始してはならない（MUST NOT）。  
復旧処理の詳細はCore復旧仕様に従う。

## 10. Interactionとの関係

Coreは利用者との自然言語対話を直接担当しない。  
利用者への情報提示および判断要求はInteractionを介して行う。

Coreは、利用者承認を必要とする変更について、Interaction等から得られた承認根拠を検証してから適用しなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > Core > Core仕様
