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
- 対象WorkのWork Context(作業コンテキスト)からTarget Listおよび対処結果のArtifact(作業成果物)を参照できる。

## 3. 処理

1. Target Listの各項目について現在状態を再取得する。
2. 対処結果と現在状態を照合する。
3. Work Purposeに対して必要な変更が成立したか確認する。
4. 未対処、失敗、不整合または新たなIssue(課題)を識別する。
5. 要求が成立していない場合は原因を分類し、必要なRe-run(再実行)候補を決定する。
6. 検証結果をInteraction(対話窓口)から利用者へ提示する。

## 4. 検証不成立時の分類

Work Purposeに対する変更が成立していない場合、少なくとも次に分類する。

- `RESEARCH_REQUIRED(再調査必要)`: Target Listの前提、対象、現在状態または必要な対処を再確認する必要がある。
- `RETREATMENT_REQUIRED(再対処必要)`: Target Listは現在も有効だが、対処が未実行、失敗または不完全である。
- `USER_DECISION_REQUIRED(利用者判断必要)`: Work Purposeの範囲、追加変更、制限その他について利用者判断が必要である。
- `NO_RERUN_REQUIRED(再実行不要)`: 要求は成立しており、再実行を必要としない。

`RESEARCH_REQUIRED`の場合は変更調査Workflow(ワークフロー)を、`RETREATMENT_REQUIRED`の場合は変更対処WorkflowをRe-run候補とする。

原因を一意に分類できない場合、推測してRe-run先を選択してはならない（MUST NOT）。必要な追加確認を行うか、利用者判断が必要なら`USER_DECISION_REQUIRED`として扱う。

## 5. 制限

検証中に追加変更を実行してはならない（MUST NOT）。

検証で問題を発見した場合、原因分類を行わずに変更調査Workflowまたは変更対処WorkflowをRe-runしてはならない（MUST NOT）。

Re-runが現在のWork Purpose達成に必要であり、既存Workflow仕様の範囲内である場合、本Workflowは自身を`SUSPENDED(中断中)`とする要求と、分類結果に対応するWorkflowのRe-run要求をCore(中核)へ提示してよい（MAY）。

Re-runによってWork Purposeを拡張したり、利用者が要求していない追加変更を実行したりしてはならない（MUST NOT）。その必要がある場合はInteraction(対話窓口)へ利用者判断を要求する。

Re-run対象が完了した後、本Workflowの開始条件を再度満たす場合、Coreは本Workflowを`ACTIVE(実行中)`へ復帰させてよい（MAY）。

## 6. 終了

検証結果を確定し、利用者への結果提示が完了した場合にWorkflow完了要求を行う。

Plan完了後、Work完了条件を満たす場合はWork完了候補となる。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更検証Workflow
