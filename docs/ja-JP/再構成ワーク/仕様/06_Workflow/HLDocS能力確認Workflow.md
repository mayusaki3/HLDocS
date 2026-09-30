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

HLDocSの能力は、Practical Capability(実務能力)とExecution Capability(実行能力)に分けて扱う。

### 3.1 Practical Capability(実務能力)

実務能力は、利用者から見た「どのような作業を遂行できるか」を表す。

例:

- コードを生成・修正できる。
- 仕様を調査できる。
- 仕様を変更できる。

登録されたState、Workflow、SubFlowまたはToolそのものを実務能力として列挙してはならない（MUST NOT）。

### 3.2 Execution Capability(実行能力)

実行能力は、実務能力を成立させるためにHLDocSが実際に行える操作を表す。

例:

- ファイルを参照できる。
- ファイルを書き込める。
- Gitの状態・差分を参照できる。
- Gitへ変更を書き込める。
- テストを実行できる。

Execution Capabilityは特定のTool名と同一視してはならない（MUST NOT）。一つの実行能力を複数のTool、SubFlowその他の能力提供手段が提供してよい（MAY）。

### 3.3 依存関係

Practical Capabilityは、その遂行に必要なExecution Capabilityをrequiredまたはoptionalとして関連付けてよい。

実行能力を持つことと、現在の処理でその操作を実行してよいことを同一視してはならない（MUST NOT）。実際の実行可否は有効なRestriction Context(制限コンテキスト)その他の実行条件によって別途検証する。

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

Execution Capabilityは、その能力のprovided_byに定義されたCapability Provider(能力提供手段)を現在の実行環境またはHLDocS登録情報と照合し、少なくとも一つのProviderが利用可能かを検証する。

実行環境ProviderはCapability Provider仕様の意味条件で照合し、一時的なTool名または製品名の一致だけを根拠としてはならない（MUST NOT）。

Execution Capabilityの判定は少なくともAVAILABLE、UNAVAILABLEまたはUNKNOWNを区別できるものとする。

Practical Capabilityは、必要なExecution Capabilityその他の成立条件を基に判定する。

各Practical Capabilityは少なくとも次のいずれかとして扱う。

- AVAILABLE: requiredな成立条件を満たし、想定する実務を遂行できる。
- DEGRADED: 基本的な実務は遂行できるが、optionalな実行能力の不足等により一部機能が利用できない。
- UNAVAILABLE: requiredな成立条件を満たさず、実務を遂行できない。
- UNKNOWN: 利用可能性を安全に確認できない。

DEGRADEDまたはUNAVAILABLEの場合、原因となったExecution Capabilityまたは成立条件を識別できるようにする。

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
