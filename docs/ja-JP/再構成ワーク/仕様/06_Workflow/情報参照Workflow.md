<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260928-000000Z-WFIR
lang: ja-JP
canonical_title: 情報参照Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 情報参照Workflow

# 情報参照Workflow

## 1. 目的

本Workflowは、利用者が要求した情報を必要最小限の参照範囲から取得し、回答を生成してInteractionから提示する。

## 2. 開始条件

- Current Stateが情報参照Stateである。
- Current Workflow PlanのOwnerがWORKである。
- PlanのWork IDがCurrent Workと一致する。
- 本WorkflowがPlan内でPENDINGである。

## 3. 処理

1. Work Purposeから回答に必要な情報を特定する。
2. 必要な正本または登録済み参照先だけを参照する。
3. 情報が不足する場合は推測で補完せず、必要に応じInteractionへ確認を要求する。
4. 取得情報に基づいて回答を生成する。
5. Interactionから利用者へ提示する。

## 4. 制限

参照対象を変更してはならない（MUST NOT）。

問い合わせへの回答に不要な仕様・Workflow・Toolを一括参照してはならない（MUST NOT）。

## 5. 終了

要求された情報の提示が完了した場合、Workflow完了要求を行う。

Plan完了後、Work完了条件を満たす場合はWork完了候補となる。

---

[目次](../../目次.md) > 仕様 > Workflow > 情報参照Workflow
