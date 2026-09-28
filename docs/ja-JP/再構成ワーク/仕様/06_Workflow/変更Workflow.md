<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260928-191900Z-WFCH
lang: ja-JP
canonical_title: 変更Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 変更Workflow

# 変更Workflow(ワークフロー)

## 1. 目的

本Workflow(ワークフロー)は、利用者が明示的に要求した変更を、対象仕様および現在のRestriction Context(制限コンテキスト)に従って実行し、結果を提示する。

## 2. 開始条件

- Current Stateが変更Stateである。
- Current Workflow Plan(ワークフロー計画)のOwnerが`WORK`である。
- PlanのWork IDがCurrent Workと一致する。
- 本WorkflowがPlan内で`PENDING(未実行)`である。
- 変更処理に必要なRestriction Set(制限セット)を適用できる。

## 3. 処理

1. Work Purposeから変更対象と要求された変更内容を特定する。
2. 変更に必要な正本、仕様および現在値だけを参照する。
3. 対象または変更内容が不足する場合、推測せずInteraction(対話窓口)へ確認を要求する。
4. 必要な変更方法を決定する。
5. Core(中核)による制限・承認・対象検証を経て変更能力を実行する。
6. 変更結果を検証する。
7. Interactionから利用者へ結果を提示する。

## 4. 制限

利用者が要求していない変更へ作業範囲を拡張してはならない（MUST NOT）。

変更のために必要なTool(ツール)または能力提供手段が利用不能または不明な場合、変更を実行済みとして扱ってはならない（MUST NOT）。

変更処理から新しいWork(作業)を暗黙に生成してはならない（MUST NOT）。

## 5. Issue

変更中にIssue(課題)を発見した場合、Issueの記録・影響分析と追加変更の承認を分離しなければならない（MUST）。

Issueの発見だけを理由としてWorkflow Planへ処理を追加してはならない（MUST NOT）。

## 6. 終了

要求された変更および必要な検証が完了し、結果提示が完了した場合、Workflow完了要求を行う。

Plan完了後、Work完了条件を満たす場合はWork完了候補となる。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更Workflow
