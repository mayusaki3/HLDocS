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

WorkはWorkflowより上位の作業単位であり、Stateそのものではない。  
WorkはState Machine上のStateを移動しながら処理される。

## 2. Work定義

Workは少なくとも次を保持する。

- Work ID
- Purpose
- Status

Work Statusは次とする。

- ACTIVE
- SUSPENDED
- COMPLETED

同時にACTIVEとなるWorkは最大1件とする（MUST）。

COMPLETEDとなったWorkを直接ACTIVEへ戻してはならない（MUST NOT）。  
完了済みWorkに関連する追加作業は、新しいWorkとして開始し、必要に応じて元WorkまたはIssueを参照する。

## 3. Work Context

Workに属する実行情報はWork Contextとして管理する。

Work Contextは少なくとも次を関連付ける。

- Current State
- Workflow Plan
- Active Workflow
- Suspended Workflow
- Issues

Restriction ContextおよびInteraction ContextをWork Contextの正本として保持してはならない（MUST NOT）。

Work Contextの確定状態はExecution Contextの一部としてCoreが管理する。

## 4. Work生成

Current Workが存在しない状態で、利用者入力が新規作業要求として明確に解釈された場合、新規Work生成を要求してよい（MAY）。

Work生成要求には、少なくとも次を含めなければならない（MUST）。

- Work IDを生成するために必要な識別要求
- 利用者要求から確定できるPurpose
- Status = ACTIVE
- 生成根拠となる利用者入力

Purposeを確定するために作業範囲を推測で拡張してはならない（MUST NOT）。

CoreはWork生成要求を検証し、同時に別のACTIVE Workが存在しない場合に限り適用してよい（MAY）。

## 5. Work開始とState

Work生成と処理対象Stateの決定を同一処理として扱ってはならない（MUST NOT）。

Work生成後、現在StateでWorkを処理できない場合は、State遷移要求が必要となる。

遷移先StateはState Machineに登録され、現在Stateから到達可能でなければならない（MUST）。

WorkまたはInteractionが未定義Stateを生成してはならない（MUST NOT）。

遷移先Stateを一意に決定できない場合、利用者判断が必要なときはInteractionのDecision Requestを使用する。

## 6. Work継続

Current WorkがACTIVEの場合、現在Workに対する継続指示によって新規Workを生成してはならない（MUST NOT）。

Active Workflowが存在する場合の継続は、当該Workflowの継続として扱う。  
Active Workflowが存在せず、承認済みWorkflow Planに次のPENDING Workflowが存在する場合は、Workflow管理仕様に従う。

Decision Requestが存在する場合、「進めて」「続けて」等の入力をDecision Responseとして解釈できるかを先に確認しなければならない（MUST）。

## 7. Work切替

ACTIVE Workの実行中に別Work候補となる利用者要求を受けた場合、現在Workを暗黙に置換してはならない（MUST NOT）。

別Workへ切り替える場合は、利用者の明示的な指示または承認を必要とする（MUST）。

切替時は、現在WorkをSUSPENDEDとし、そのWork Contextを保存した後、新しいWorkをACTIVEとしてよい（MAY）。

SUSPENDED Workを再開する場合、現在の正本、State Machineおよび実体との整合性を確認しなければならない（MUST）。

## 8. Work完了

Workは、少なくとも次を満たす場合に完了候補としてよい（MAY）。

- 実行対象となるWorkflow Planが完了している。
- Active Workflowが存在しない。
- Suspended Workflowが存在しない。
- Work完了をBLOCKするIssue Policyが存在しない。
- 未処理のDecision RequestによってWork完了が保留されていない。

未解決Issueが存在することだけを理由としてWorkをCOMPLETEDにできないものとしてはならない（MUST NOT）。

残存Issueがある場合は、必要なPolicyおよび利用者判断に従い、残存Issueを保持したままWorkをCOMPLETEDとしてよい（MAY）。  
Work完了によってIssueを自動的にRESOLVEDまたはCLOSEDへ変更してはならない（MUST NOT）。

## 9. Work完了後

WorkをCOMPLETEDとした後、通常運転を待機Stateへ戻す場合は、State Machineに定義された遷移を使用しなければならない（MUST）。

Work完了とState遷移を同一の状態変更として扱ってはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Work > Work仕様
