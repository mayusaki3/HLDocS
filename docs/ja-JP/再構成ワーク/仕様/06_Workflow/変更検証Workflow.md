<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-080000Z-WFCV
lang: ja-JP
canonical_title: 変更検証Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 変更検証Workflow

# 変更検証Workflow(ワークフロー)

## 1. 目的

変更対処Workflow(ワークフロー)の結果をTarget List(対処対象リスト)およびWork Purposeと照合し、要求された変更が正しく成立したかを検証する。

## 2. 開始条件

- Current Stateが変更Stateである。
- 本WorkflowがCurrent Workflow Plan内で`PENDING(未実行)`である。
- 変更対処Workflowが`COMPLETED(完了)`である。
- Target Listおよび対処結果を参照できる。

## 3. 処理

1. Target Listの各項目について現在状態を再取得する。
2. 対処結果と現在状態を照合する。
3. Work Purposeに対して必要な変更が成立したか確認する。
4. 未対処、失敗、不整合または新たなIssue(課題)を識別する。
5. 検証結果をInteraction(対話窓口)から利用者へ提示する。

## 4. 制限

検証中に追加変更を実行してはならない（MUST NOT）。

検証で問題を発見した場合、それだけを理由として変更対処Workflowを再実行したり、Workflow Plan(ワークフロー計画)を変更したりしてはならない（MUST NOT）。

追加対処が必要な場合はIssue、利用者判断、Plan変更規則その他の該当仕様に従う。

## 5. 終了

検証結果を確定し、利用者への結果提示が完了した場合にWorkflow完了要求を行う。

Plan完了後、Work完了条件を満たす場合はWork完了候補となる。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更検証Workflow
