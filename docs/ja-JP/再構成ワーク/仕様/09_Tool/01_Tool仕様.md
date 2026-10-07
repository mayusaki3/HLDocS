<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261007-000000Z-TOOL
lang: ja-JP
canonical_title: Tool仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Tool > Tool仕様

# Tool(ツール)仕様

## 1. 目的

本書は、HLDocSにおけるTool(ツール)の責務と、Capability Provider(能力提供手段)との境界を定義する。

Toolは、LLM実行環境またはHLDocSが利用できる具体的な操作インターフェースである。

ToolそのものをCapability(能力)として扱ってはならない（MUST NOT）。

## 2. 基本構造

Execution Capability(実行能力)とToolの関係は次とする。

```text
Execution Capability
        ↓ provided_by
Capability Provider Reference
        ↓ runtime match / defined tool
Tool
```

Execution Capabilityは「何を実行できるか」を表す。

Capability Providerは「そのExecution Capabilityをどの実行手段によって実現できるか」を表す。

Toolは「実際に呼び出せる操作インターフェース」を表す。

Tool名、Connector名、MCP名、関数名、製品名その他の実装上の識別子をExecution Capabilityそのものとしてはならない（MUST NOT）。

## 3. Toolの種類

HLDocSは少なくとも次のToolを扱える。

### 3.1 Environment Tool(実行環境ツール)

現在のLLM実行環境から提供されるTool、Connector、API操作その他の実行インターフェース。

Environment ToolはHLDocSの個別Tool仕様へ登録されていなくてもよい。

利用可能性はCapability Provider仕様のProvider Referenceによって現在の実行環境と意味照合する。

### 3.2 HLDocS Tool(HLDocSツール)

HLDocSが個別仕様として定義するTool。

HLDocS Toolは、実行環境が直接提供しない操作を補う場合、またはHLDocS固有の入力、出力、実行条件その他のインターフェースを定義する必要がある場合に定義してよい（MAY）。

HLDocS Toolを定義したことだけを理由として、そのToolを現在実行可能として扱ってはならない（MUST NOT）。

## 4. Toolの責務

Toolは、必要に応じて次を提供する。

- 入力
- 出力
- 実行条件
- 実行時制約
- 実行結果
- 実行時エラーまたは外部状態

Toolは処理の意味上の目的、Workflow進行またはState遷移を決定する主体ではない。

Toolの実行結果は、呼出元またはCore(中核)が後続判断に利用できる事実または結果として返す。

## 5. Toolが行ってはならないこと

Toolは次を行ってはならない（MUST NOT）。

- Work(作業)を生成、変更または完了する。
- State(状態)を選択または遷移する。
- Workflow Plan(ワークフロー計画)を生成または変更する。
- Workflow(ワークフロー)またはSubFlow(サブフロー)を選択、開始、完了または中断する。
- Restriction Set(制限セット)を選択、解除または緩和する。
- Capability Context(能力コンテキスト)の判定結果を自ら確定する。
- 利用者意図を独自に解釈して要求範囲を拡張する。
- 利用者とのHLDocS上の対話制御を担当する。

Toolは、呼出時に与えられた入力と実行環境が許す範囲で操作を実施する。

## 6. Capability Providerとの境界

Capability ProviderはToolそのものの別名ではない。

一つのExecution Capabilityを複数Toolが提供してよい（MAY）。

一つのToolが複数Execution CapabilityのProvider条件を満たしてよい（MAY）。

```text
Execution Capability A ─┐
                        ├→ Tool X
Execution Capability B ─┘

Execution Capability A ─→ Tool X
                       └→ Tool Y
```

したがって、Tool一覧とCapability登録簿を同一の登録簿としてはならない（MUST NOT）。

Environment Toolについて、現在の具体的Tool名をHLDocS正本へ恒久的に書き戻すことを要求しない。

## 7. Tool選択

Tool選択は、対象Execution CapabilityのProvider Referenceに適合する現在利用可能なTool候補から行う。

特定Toolの固定優先順位をCapabilityの利用可能性と同一視してはならない（MUST NOT）。

Tool候補の選択では、少なくとも次を考慮できる。

- Provider Referenceへの適合
- 現在の利用可能性
- 対象範囲
- 実行条件
- Restriction Context(制限コンテキスト)
- 外部サービスの一時的制限
- 呼出元が必要とする入出力

優先Toolが失敗した場合も、Execution Capability自体を直ちにUNAVAILABLEとしてはならない（MUST NOT）。Capability Provider仕様およびCapability Context仕様に従って代替Providerを評価する。

## 8. Tool実行

Toolを実行する前に、Coreは少なくとも次を確認しなければならない（MUST）。

- 必要なExecution Capabilityが現在利用可能であること。
- 選択Toolが対象Provider Referenceに適合すること。
- 現在のRestriction Contextで対象操作が許容されること。
- 対象範囲が確定していること。
- 必要な利用者承認またはその他の実行条件が成立していること。

副作用を伴うTool実行では、実行直前の状態でこれらを再確認しなければならない（MUST）。

Toolを変更してRestrictionを回避してはならない（MUST NOT）。

## 9. Execution Attempt

Toolの一回の実行結果はExecution Attempt(実行試行)として扱える。

Tool実行失敗とExecution Capabilityの利用不能を同一視してはならない（MUST NOT）。

一時的エラー、利用制限、Provider不適合、恒常的利用不能、原因不明その他の分類はCapability Context仕様に従う。

Tool自身が返していない原因、retry-afterまたは恒常性を推測して確定してはならない（MUST NOT）。

## 10. HLDocS Tool個別仕様

HLDocS Toolを定義する場合、個別仕様は少なくとも次を識別できなければならない（MUST）。

- tool: Tool識別子または名称
- purpose: Toolの目的
- input: 入力
- output: 出力
- execution_conditions: 実行条件
- constraints: 実行時制約

必要に応じてエラーまたは外部状態の返却形式を定義してよい（MAY）。

個別Tool仕様は、そのToolがどのPractical Capabilityから利用されるかを逆参照一覧として保持する必要はない。

## 11. 呼出関係

基本的な呼出方向は次とする。

```text
Workflow
   ↓
SubFlow
   ↓ requires
Execution Capability
   ↓ Provider selection
Tool
```

WorkflowからToolを直接呼び出すことを共通仕様で全面禁止しない。ただし、再利用可能な意味処理として分離できる場合はSubFlowへ分離する。

ToolからTool、SubFlow、Workflow、Stateその他の上位HLDocS実行層を選択または呼び出す構造を基本モデルとしてはならない（MUST NOT）。

## 12. 登録

Environment Toolの網羅的なTool登録簿をHLDocS側へ作成することを要求しない。

HLDocS Toolが複数定義され、発見機構が必要になった場合はHLDocS Tool登録簿を設けてよい（MAY）。

Tool登録簿を作成する場合も、Execution CapabilityとProvider Referenceを介さず、Tool登録だけを根拠として能力AVAILABLEを判定してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Tool > Tool仕様
