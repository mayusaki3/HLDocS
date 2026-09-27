<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-WORK
lang: ja-JP
canonical_title: Work仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Work > Work仕様

# Work仕様

## 1. 目的

本書は、HLDocSにおける利用者単位の作業であるWorkの生成、継続、切替および完了を定義する。

WorkはWorkflowより上位の利用者作業単位であり、Stateそのものではない。

## 2. Work定義

Workは少なくとも次を保持する。

- Work ID
- Purpose
- Status
- Issues

Work StatusはACTIVE、SUSPENDED、COMPLETEDとする。

同時にACTIVEとなるWorkは最大1件とする（MUST）。

COMPLETEDとなったWorkを直接ACTIVEへ戻してはならない（MUST NOT）。

## 3. Work Context

Work ContextはWork固有情報を保持する。

Workflow Plan、Active Workflow、Suspended WorkflowおよびCurrent Stateの正本はExecution Contextに保持し、Work Contextへ重複して正本を保持してはならない（MUST NOT）。

WorkをSUSPENDEDする場合は、再開に必要な実行情報を当該Workへ関連付けて保存できなければならない（MUST）。  
保存情報は再開時の候補情報であり、現在の正本との再検証なしにそのまま復元してはならない（MUST NOT）。

## 4. Work生成

Current Workが存在しない状態で、利用者入力が新規作業要求として明確に解釈された場合、新規Work生成を要求してよい（MAY）。

Work生成要求には、Work ID、Purpose、Status=ACTIVE、および生成根拠となる利用者入力を関連付ける。

Purposeを確定するために作業範囲を推測で拡張してはならない（MUST NOT）。

## 5. WorkとWorkflow Plan

利用者Workを処理するWorkflow PlanはOwner=WORKとし、対象Work IDを関連付けなければならない（MUST）。

Workが存在しないSYSTEM Workflow PlanをWorkへ仮所属させてはならない（MUST NOT）。

ACTIVE Workが存在していても、SYSTEM PlanをそのWorkのPlanとして扱ってはならない（MUST NOT）。

## 6. Work開始とState

Work生成と処理対象Stateの決定を同一処理として扱ってはならない（MUST NOT）。

Work生成後、現在StateでWorkを処理できない場合はState選択ルールを使用し、State Machineによる遷移可否判定を経なければならない（MUST）。

## 7. Work継続・切替

Current WorkがACTIVEの場合、現在Workに対する継続指示によって新規Workを生成してはならない（MUST NOT）。

ACTIVE Workの実行中に別Work候補となる利用者要求を受けた場合、現在Workを暗黙に置換してはならない（MUST NOT）。

別Workへ切り替える場合は利用者の明示的な指示または承認を必要とする（MUST）。

## 8. Work完了

Workは少なくとも次を満たす場合に完了候補としてよい（MAY）。

- 当該WorkをOwnerとするWorkflow Planが完了している。
- 当該Workに属するActive Workflowが存在しない。
- 当該Workに属するSuspended Workflowが存在しない。
- Work完了をBLOCKするIssue Policyが存在しない。
- Work完了を保留するDecision Requestが存在しない。

残存Issueがある場合でもPolicyおよび利用者判断に従いWorkをCOMPLETEDとしてよい（MAY）。  
Work完了によってIssueを自動的にRESOLVEDまたはCLOSEDへ変更してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Work > Work仕様
