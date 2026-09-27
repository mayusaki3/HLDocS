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

## 2. Work定義

WorkはWork ID、Purpose、Status、Issuesを保持する。  
StatusはACTIVE、SUSPENDED、COMPLETEDとする。

同時にACTIVEとなるWorkは最大1件とする（MUST）。  
COMPLETEDとなったWorkを直接ACTIVEへ戻してはならない（MUST NOT）。

## 3. Work Context

Work ContextはWork固有情報を保持する。

Workflow Plan、Active Workflow、Suspended WorkflowおよびCurrent Stateの正本はExecution Contextに保持し、Work Contextへ重複して正本を保持してはならない（MUST NOT）。

SUSPENDED Workには再開に必要な実行情報を関連付けて保存できなければならない（MUST）。  
保存情報は再開時に再検証する。

## 4. Work生成

Current Workが存在しない状態で、Interactionが利用者入力をNEW_WORK_REQUESTとして一意に分類した場合、InteractionはCoreへWork生成要求を送ってよい（MAY）。

Coreは要求を検証し、他のACTIVE Workが存在しない場合にWorkを生成してCurrent WorkとしてACTIVEにできる。

Work生成要求にはWork ID生成に必要な情報、Purpose、Status=ACTIVE、生成根拠となる利用者入力を関連付ける。

Purposeを確定するために作業範囲を推測で拡張してはならない（MUST NOT）。

## 5. WorkとWorkflow Plan

利用者Workを処理するWorkflow PlanはOwner=WORKとし、対象Work IDを関連付ける。

SYSTEM Workflow PlanをWorkへ仮所属させてはならない（MUST NOT）。

## 6. Work開始とState

Work生成と処理対象Stateの選択は別の意味判断とする（MUST）。

Work生成後、現在StateでWorkを処理できない場合はState選択ルールを使用し、State Machineによる遷移可否判定を経なければならない（MUST）。

ただし、必要なWork生成、State選択、State遷移およびState進入準備がすべて検証済みの場合、CoreはExecution Contextに不整合な中間状態を公開しないため、関連変更を一つの整合したコミットとして適用してよい（MAY）。

## 7. Work継続・切替

現在Workへの継続指示によって新規Workを生成してはならない（MUST NOT）。

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

WorkをCOMPLETEDへ変更した後、Current Workから解除する。  
完了済みWorkはWork Contextsに履歴として保持してよい（MAY）。

---

[目次](../../目次.md) > 仕様 > Work > Work仕様
