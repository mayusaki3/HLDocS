<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-WF01
lang: ja-JP
canonical_title: Workflow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Workflow仕様

# Workflow(ワークフロー)仕様

## 1. 目的

本書は、HLDocSにおけるWorkflowおよびWorkflow Planの共通構造、責務、実行状態を定義する。

## 2. Workflow

Workflow(ワークフロー)はHLDocSの処理を進行させる実行単位である。  
SYSTEM処理と利用者Work処理はWorkflow PlanのOwnerによって区別する。

同時にACTIVEとなるWorkflowはExecution Context上で最大1件とする（MUST）。

## 3. Workflow Plan

Workflow Plan(ワークフロー計画)は現在実行するWorkflow列の実行インスタンスであり、Execution Contextに保持する。

OwnerはSYSTEMまたはWORKとする。  
Owner=WORKの場合はWork IDを保持する。Owner=SYSTEMの場合はWork IDを要求してはならない（MUST NOT）。

## 4. 実行状態

WorkflowはPENDING、ACTIVE、SUSPENDED、COMPLETED、SKIPPEDを持つ。

Planは、Plan内の全WorkflowがCOMPLETEDまたはSKIPPEDであり、Active/Suspended Workflowが存在しない場合に完了とする。

COMPLETEDとSKIPPEDを同一の意味として扱ってはならない（MUST NOT）。

## 5. Plan生成

Stateへ進入し、対応するCurrent Workflow Planが存在せず、default_workflow_planが定義されている場合、Coreはdefault_workflow_planからPlanを生成してよい（MAY）。

SYSTEM用StateではOwner=SYSTEM、利用者Work用StateではOwner=WORKとする。

## 6. Workflow開始

Workflow開始には、Current Stateのavailable_workflows登録、Current Plan所属、PENDING、他Active Workflowなし、開始条件成立、Restriction適用可能をすべて満たさなければならない（MUST）。

Coreは検証後、WorkflowをACTIVEへ変更する。

## 7. Workflowの責務

Workflowは目的達成に必要な処理進行、SubFlow選択・順序、Restriction Set宣言、Issue発見・影響分析、終了条件判定、State遷移候補要求を担当する。

利用者との直接対話はInteractionを介さなければならない（MUST）。

## 8. Workflow完了

Workflowは終了条件成立時にCoreへ完了要求を行う。  
Coreは検証後、ACTIVEからCOMPLETEDへの変更を適用する。

Workflow完了をIssue解決、Work完了またはState遷移完了として扱ってはならない（MUST NOT）。

## 9. Plan終了と解除

Current Workflow Planが完了しただけでは直ちに履歴を失ってはならない（MUST NOT）。

Plan完了を条件とするWork完了またはState遷移の検証が終了した後、CoreはCurrent Workflow PlanをExecution Contextの現在実行位置から解除してよい（MAY）。

必要な場合、完了Planは履歴またはWork再現情報として保存してよい（MAY）。

新しいStateのPlanを生成する前に、前Stateの完了済みPlanがCurrent Workflow Planとして残存していてはならない（MUST NOT）。

## 10. Plan変更

Plan外Workflowを必要とする場合は、Workflow候補の発見とPlan変更を分離する（MUST）。

Owner=WORKのPlanについて、追加、削除、並べ替え、SKIPPED化は利用者の明示的な指示または承認なしに確定してはならない（MUST NOT）。

Owner=SYSTEMのPlanは対応仕様に明示された規則なしに変更してはならない（MUST NOT）。

Workflow Re-run(ワークフロー再実行)は、Current Workflow Plan(ワークフロー計画)に既に存在するWorkflowを再度実行する実行制御であり、Workflowの追加、削除または順序変更を伴わない限りPlan構成変更として扱わない。

完了済みWorkflowを再実行する場合、通常の状態遷移として暗黙に`COMPLETED(完了)`から`PENDING(未実行)`へ戻してはならない（MUST NOT）。Core(中核)がRe-run要求を検証し、再実行可能な場合に対象Workflowを再実行可能状態へ戻す。

Re-run時に別Workflowが`ACTIVE(実行中)`である場合、同時ACTIVE最大1件の規則を満たすため、必要に応じて現在のWorkflowを`SUSPENDED(中断中)`としてから再実行対象を開始する。

Owner=`WORK`のPlanで、現在の利用者要求の遂行に必要な再調査・再検証等が既存Workflow仕様から明確に要求される場合、その仕様に従うRe-runはPlan構成変更の利用者承認を別途要求しない。ただし、Work Purposeの拡張、追加変更、または新たな利用者判断を伴う場合は該当する承認規則に従わなければならない（MUST）。

## 11. Workflow Re-run

Re-run要求は少なくとも対象Workflow、再実行理由および再実行後に復帰すべき処理を識別できなければならない（MUST）。

Re-runは過去のArtifact(作業成果物)を最新状態として保証しない。再実行Workflowは必要な対象状態を再取得し、Artifactを更新しなければならない（MUST）。

## 12. State遷移

WorkflowはState遷移候補を提示できるが、自らCurrent Stateを変更してはならない（MUST NOT）。

遷移可否はState Machineが判断し、変更適用はCoreが行う。

---

[目次](../../目次.md) > 仕様 > Workflow > Workflow仕様
