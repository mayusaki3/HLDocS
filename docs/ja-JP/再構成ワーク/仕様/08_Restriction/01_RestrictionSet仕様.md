<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261007-000000Z-RS01
lang: ja-JP
canonical_title: Restriction Set仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Restriction > Restriction Set仕様

# Restriction Set(制限セット)仕様

## 1. 目的

本書は、HLDocSにおけるRestriction Set(制限セット)の共通構造、責務、登録、参照およびRestriction Context(制限コンテキスト)への適用規則を定義する。

Restriction Setは、State(状態)、Workflow(ワークフロー)またはSubFlow(サブフロー)が、その実行範囲で追加適用する制限を宣言する仕様要素である。

Core基本制限はRestriction Setではなく、Restriction Setの有無にかかわらず常時適用する。

## 2. 責務

Restriction Setは、処理の実行方法を定義するものではなく、現在の実行位置で許容してはならない操作または許容範囲を宣言する。

Restriction Setは少なくとも次の対象へ制限を表現できるものとする。

- Capability(能力)またはExecution Capability(実行能力)
- 操作種別
- 対象または対象範囲
- 副作用の有無または種類
- 必要な利用者承認その他の実行条件

特定のTool(ツール)名だけに依存する制限を基本としてはならない（MUST NOT）。同一能力を別Toolまたは別Capability Provider(能力提供手段)で実行しても、意味上同じ操作には同じ制限を適用できなければならない（MUST）。

## 3. 個別Restriction Setの最小構造

個別Restriction Setは少なくとも次を識別できなければならない（MUST）。

- restriction_set: 一意な識別子または名称
- purpose: 制限の目的
- rules: 適用する制限規則

各ruleは、制限対象と制限内容を判定できる情報を持たなければならない（MUST）。

必要に応じて次を定義してよい（MAY）。

- 対象Capability
- 対象操作
- 対象範囲
- 禁止条件
- 許容上限または許容範囲
- 必要な承認条件
- 適用判定に必要なその他の条件

Restriction Set自身がState、WorkflowまたはSubFlowの実行順序を定義してはならない（MUST NOT）。

## 4. 制限の合成

Coreは現在の実行位置に対して適用されるRestriction SetをRestriction Contextへ積み上げる。

概念上の合成は次とする。

```text
Core基本制限
 + State Restriction Set
 + Workflow Restriction Set
 + SubFlow Restriction Set
 = Restriction Context
```

下位Restriction Setは上位制限を解除または緩和してはならない（MUST NOT）。

複数の制限が同じ操作へ適用される場合、すべての制限を満たさなければならない（MUST）。禁止規則と許容規則が競合する場合は、禁止またはより厳しい制限を優先する。

Restriction Setの追加によって、Core基本制限または既に有効なRestriction Setで禁止された操作を許可してはならない（MUST NOT）。

## 5. 登録

通常運転でState、WorkflowまたはSubFlowから参照するRestriction Setは、Restriction Set登録簿へ登録されていなければならない（MUST）。

登録簿はRestriction Setの実行順序、優先順位または処理フローを定義するものではない。

登録簿は少なくとも次を識別できればよい。

- restriction_set
- 個別仕様の参照先

個別Restriction Setの内容を登録簿へ重複して保持することを要求しない。

## 6. 参照

State、WorkflowまたはSubFlowは、適用するRestriction Setを登録済み識別子で宣言する。

Coreは宣言されたRestriction Setについて、次の順序で処理しなければならない（MUST）。

1. Restriction Set登録簿で登録を確認する。
2. 登録された参照先から個別Restriction Set仕様を取得する。
3. 個別仕様を解釈し、現在の実行位置へ適用可能であることを検証する。
4. 既存のRestriction Contextへ制限を追加する。

登録されていないRestriction Setを、名称や類似仕様から推測して適用してはならない（MUST NOT）。

登録済みであっても個別仕様を取得、解釈または適用できない場合は、そのRestriction Setが不要であるものとして処理を継続してはならない（MUST NOT）。

## 7. 適用期間

Stateが宣言するRestriction Setは、そのStateがCurrent Stateである期間に適用する。

Workflowが宣言するRestriction Setは、そのWorkflowが現在の実行位置として適用対象である期間に追加する。

SubFlowが宣言するRestriction Setは、そのSubFlowの実行期間に追加する。

実行位置を離れたことにより下位Restriction Setの適用を終了する場合でも、上位Restriction SetまたはCore基本制限を解除してはならない（MUST NOT）。

SUSPENDED Workflowの制限を継続適用する必要があるかは、その制限の意味とWorkflow仕様に従う。Coreは中断を理由として、復帰条件または安全性に必要な制限を暗黙に解除してはならない（MUST NOT）。

## 8. 実行前判定

Coreは副作用を伴う操作またはCapability Provider実行の直前に、現在のRestriction Contextを用いて対象操作を再評価しなければならない（MUST）。

Capability Context(能力コンテキスト)が`AVAILABLE`であっても、Restriction Contextで許容されない操作を実行してはならない（MUST NOT）。

別Providerで同一能力を実行可能であることを、Restriction Context回避の理由としてはならない（MUST NOT）。

必要な承認、対象範囲または制限条件を確認できない場合、許可されているものとして実行してはならない（MUST NOT）。

## 9. Restriction Setが行ってはならないこと

Restriction Setは次を行ってはならない（MUST NOT）。

- Execution Contextを変更する。
- State遷移を要求または決定する。
- Workflow Planを変更する。
- WorkflowまたはSubFlowを開始する。
- ToolまたはCapability Providerを実行する。
- 利用者と直接対話する。
- Core基本制限を解除または緩和する。
- 上位Restriction Setを解除または緩和する。

Restriction Setは宣言的な制限仕様であり、実行主体ではない。

## 10. Fail-closed

現在の処理に必要と宣言されたRestriction Setについて、登録、参照、解釈または適用のいずれかを確認できない場合、Coreは対象処理を制限なしで継続してはならない（MUST NOT）。

処理継続に利用者判断が必要な場合は、Interaction(対話窓口)を介して不足または競合内容を提示する。

---

[目次](../../目次.md) > 仕様 > Restriction > Restriction Set仕様
