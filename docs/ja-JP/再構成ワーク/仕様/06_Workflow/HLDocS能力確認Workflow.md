<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-WFCP
lang: ja-JP
canonical_title: HLDocS能力確認Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > HLDocS能力確認Workflow

# HLDocS能力確認Workflow

## 1. 目的

本Workflowは、現在のHLDocSで利用可能な能力を検証し、その結果を利用者へ通知する。

## 2. 開始条件

次をすべて満たす場合に開始できる。

- Current Stateが能力確認Stateである。
- 能力確認Stateのavailable_workflowsに本Workflowが登録されている。
- 現在のWorkflow Planに本WorkflowがPENDINGとして存在する。
- 他のActive Workflowが存在しない。

## 3. 能力の扱い

能力とは、利用者がHLDocSに依頼可能な作業機能をいう。

登録された仕様要素そのものを能力として列挙してはならない（MUST NOT）。

例:

- 「Git Tool」ではなく「Gitを利用したソースコード更新」
- 「検証SubFlow」ではなく「仕様に基づく検証」

## 4. 検証

能力を利用可能と判定する場合は、その能力を成立させるために必要な登録情報を確認しなければならない（MUST）。

必要に応じて、次を確認する。

- 必要なStateが登録されている。
- 必要なWorkflowが登録されている。
- 必要なWorkflow仕様を参照できる。
- 必要なSubFlowが登録され、参照できる。
- 必要なToolまたは能力提供手段を利用できる。
- 必要なRestriction Setを取得・適用できる。
- 現在の実行環境で開始不能となる既知条件がない。

登録されていることだけを利用可能の根拠としてはならない（MUST NOT）。

能力確認のために、すべての個別仕様を無条件に一括読込してはならない（MUST NOT）。

## 5. 判定

各能力は少なくとも次のいずれかとして扱う。

- AVAILABLE: 必要条件を確認でき、利用可能。
- UNAVAILABLE: 能力は定義されているが、必要条件を満たさない。
- UNKNOWN: 利用可能性を安全に確認できない。

未登録の能力を、存在する能力としてNOT_REGISTERED一覧へ網羅的に推測してはならない（MUST NOT）。

## 6. 通知

検証結果はInteractionを通じて利用者へ通知する。

少なくともAVAILABLEな能力を利用者が認識できるようにする。  
UNAVAILABLEまたはUNKNOWNが存在する場合は、必要に応じて理由を添えて通知する。

AVAILABLEな能力が一つも存在しない場合も正常な検証結果として扱い、次の趣旨を通知する。

「現在利用可能な機能はありません。」

能力が存在しないことをHLDocSシステム起動失敗として扱ってはならない（MUST NOT）。

## 7. 終了条件

能力検証およびInteractionへの結果通知が完了した場合、本Workflowの終了条件を満たす。

終了条件を満たした場合、Workflow完了要求を行う。

Workflow Plan内の全WorkflowがCOMPLETEDまたはSKIPPEDとなった後、能力確認Stateから待機Stateへの遷移候補を提示する。

---

[目次](../../目次.md) > 仕様 > Workflow > HLDocS能力確認Workflow
