<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-HL01
lang: ja-JP
canonical_title: HLDocSとは
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > HLDocSとは

# HLDocSとは

## 1. HLDocSとは何か

HLDocSは、LLMが作業対象正本を根拠として、ドキュメントおよびソースコードの生成・更新・検証を行うための共通仕様である。  
HLDocSは、作業手順、参照方法、成果物管理および実行モデルを定義し、再現性と検証性を備えたLLMによる作業を実現する。  
HLDocSは、仕様作成のための技術検証について、検証ドキュメントおよび検証コードの生成・更新・検証結果の整理も対象とする。

## 2. 目的

HLDocSは、次を目的とする。

- 作業対象正本を根拠として作業する。
- 推測や記憶への過度な依存を抑制する。
- Work(作業)、State(状態)、Workflow(ワークフロー)、SubFlow(サブフロー)およびTool(ツール)の責務を分離して作業を制御する。
- 現在の処理に必要な仕様のみを参照し、LLMが保持するコンテキストを抑制する。
- 再現可能かつ検証可能な成果物を生成する。
- 利用者の判断を必要とする変更を、LLMが独断で確定しない。

## 3. 基本構成

HLDocSは、少なくとも次の責務領域によって構成する。

- Core(中核)
- State Machine(状態遷移機構)
- State(状態)
- Work(作業)
- 選択ルール
- Workflow(ワークフロー)
- SubFlow(サブフロー)
- Capability(能力)
- Tool(ツール)
- Restriction Set(制限セット)
- Interaction(対話窓口)

各責務領域は、実行時に常にすべての詳細仕様を参照することを要求しない。  
現在の処理に必要な仕様を必要な時点で参照しなければならない（MUST）。

## 4. 正本

### 4.1 HLDocS仕様/規約（正本）

HLDocS仕様/規約とは、HLDocS自体を構成する仕様群である。  
HLDocS仕様/規約に対し正本という場合、それが現在採用されているHLDocS仕様であることを示す。

### 4.2 作業対象正本

作業対象正本とは、利用者が作業対象の正本として指定した仕様、文書、ソースコードまたはリポジトリ上の成果物である。  
HLDocS仕様/規約（正本）と作業対象正本を混同してはならない（MUST NOT）。

## 5. 実行モデル

HLDocSは、Core(中核)の起動後にState Machine(状態遷移機構)へ制御を移譲して通常運転を開始する。

通常運転では、Work(作業)を利用者から見た作業単位として扱い、WorkはState Machine(状態遷移機構)上のState(状態)を移動しながらWorkflow Plan(ワークフロー計画)に従って処理される。  
Workflow(ワークフロー)は作業進行、SubFlow(サブフロー)は再利用可能な単一目的処理、Capability(能力)は実現可能な能力、Tool(ツール)は具体的な操作インターフェースを担当する。  
利用者との入出力はInteraction(対話窓口)を介して行う。

## 6. Core

Core(中核)は、HLDocSの整合性を維持するための共通実行機構である。  
Coreは、システム起動、Execution Context(実行コンテキスト)の管理、変更適用、制限制御、登録要素参照およびState Machine(状態遷移機構)へ移譲できない場合の復旧への移行を担当する。

Coreは、通常作業における次のWorkflowを決定してはならない（MUST NOT）。  
Coreは、WorkflowまたはSubFlowの処理内容を決定してはならない（MUST NOT）。

## 7. Coreの補助記憶

Coreは、HLDocS実行中の作業継続および復元を補助する一時記憶領域としてLLM_WORKSPACEを利用できる。  
LLM_WORKSPACEは独立した実行責務領域ではなく、Coreが利用する補助機構として扱う。詳細はCore仕様に従う。

## 8. 起動

HLDocS開始時は、「HLDocSシステム起動条件」に従ってCoreを起動する。  
起動条件が成立するまでは、通常のState、Workflow、SubFlowまたはToolに基づく作業を開始してはならない（MUST NOT）。

Core起動後はState Machineへの制御移譲を試行する。  
移譲に成功した場合は通常運転を開始する。  
移譲に失敗した場合は、Coreの復旧機構によって安全な復旧処理を行わなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > Core > HLDocSとは
