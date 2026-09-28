<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-WORK
lang: ja-JP
canonical_title: Work仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Work > Work仕様

# Work(作業)仕様

## 1. 目的

本書は、HLDocSにおける利用者単位の作業であるWorkの生成、継続、切替および完了を定義する。

## 2. Work定義

WorkはWork ID、Purpose、Status、Issuesを保持する。  
StatusはACTIVE、SUSPENDED、COMPLETEDとする。

同時にACTIVEとなるWorkは最大1件とする（MUST）。  
COMPLETEDとなったWorkを直接ACTIVEへ戻してはならない（MUST NOT）。

## 3. Work Candidate

NEW_WORK_REQUESTを受けた時点では、Workを直ちにExecution Contextへ確定生成せず、まずWork Candidate(作業候補)を構成する。

Work Candidate(作業候補)は少なくとも次を持つ。

- Purpose
- Source User Input
- 必要に応じてWork ID生成に必要な情報

Work CandidateはWorkではなく、ACTIVE/SUSPENDED/COMPLETEDのStatusを持たない。  
Work CandidateをCurrent Workとして扱ってはならない（MUST NOT）。

## 4. Work生成

Interactionが利用者入力をNEW_WORK_REQUESTとして一意に分類した場合、Work CandidateをState選択へ渡してよい（MAY）。

Work Candidateについて処理可能なStateがUNIQUEであり、State Machine上の遷移が可能で、State進入準備を完了できる場合、CoreはWorkを生成してACTIVEとし、State遷移と整合した一つのコミットとして適用してよい（MAY）。

Purposeを確定するために作業範囲を推測で拡張してはならない（MUST NOT）。

## 5. State選択が確定しない場合

State選択結果がMULTIPLE、NONEまたはUNKNOWNの場合、Work CandidateをACTIVE Workとして確定してはならない（MUST NOT）。

- MULTIPLE: 必要ならInteractionのDecision Requestで利用者選択を取得する。
- UNKNOWN: 必要な追加情報を取得する。
- NONE: 現在処理可能なStateがないことをInteractionから通知する。

Decision Responseや追加情報によりUNIQUEへ変化した場合は、同じWork Candidateを再評価してよい（MAY）。

候補処理を中止する場合、Work Candidateを破棄してよい。Work履歴としてCOMPLETED等を生成する必要はない。

## 6. Work Context

Work Contextは確定済みWorkのWork固有情報を保持する。

Workflow Plan、Active Workflow、Suspended WorkflowおよびCurrent Stateの正本はExecution Contextに保持する。

SUSPENDED Workには再開に必要な実行情報を関連付けて保存し、再開時に再検証する。

## 7. WorkとWorkflow Plan

利用者Workを処理するWorkflow PlanはOwner=WORKとし、対象Work IDを関連付ける。

SYSTEM Workflow PlanをWorkへ仮所属させてはならない（MUST NOT）。

## 8. Work継続・切替

現在Workへの継続指示によって新規Workを生成してはならない（MUST NOT）。

別Workへ切り替える場合は利用者の明示的な指示または承認を必要とする（MUST）。

## 9. Work完了

Workは、対象Plan完了、Active/Suspended Workflowなし、Work完了をBLOCKするIssue Policyなし、完了を保留するDecision Requestなしの場合に完了候補としてよい（MAY）。

残存IssueがあってもPolicyおよび利用者判断に従いCOMPLETEDとしてよい（MAY）。  
Work完了によってIssueを自動的にRESOLVED/CLOSEDへ変更してはならない（MUST NOT）。

COMPLETED後はCurrent Workから解除し、Work Contextsに履歴として保持してよい（MAY）。

---

[目次](../../目次.md) > 仕様 > Work > Work仕様
