<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-080000Z-WFCS
lang: ja-JP
canonical_title: 変更調査Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 変更調査Workflow

# 変更調査Workflow(ワークフロー)

## 1. 目的

利用者の変更要求について、実際の変更を行う前に対象、現在状態、要求との対応、適用可否および必要な対処を調査し、Target List(対処対象リスト)を生成する。

## 2. 開始条件

- Current Stateが変更Stateである。
- Current Workflow Plan(ワークフロー計画)のOwnerが`WORK`である。
- PlanのWork IDがCurrent Workと一致する。
- 本WorkflowがPlan内で`PENDING(未実行)`である。初回実行または承認済みRe-run(再実行)のどちらでもよい。

## 3. 処理

1. Work PurposeとSource User Inputから要求された変更範囲を確認する。
2. 必要最小限の正本、対象および関連仕様を参照する。
3. 変更対象の実在、位置および現在状態を確認する。
4. 要求された変更が適用可能か、制限・依存・整合性上の問題がないか調査する。
5. 必要な対処をTarget List(対処対象リスト)として整理する。
6. 不足情報または利用者判断が必要な項目は、推測せずInteraction(対話窓口)へ判断または情報を要求する。

## 4. Target List(対処対象リスト)

Target Listは本Workflowが生成するArtifact(作業成果物)であり、対象WorkのWork Context(作業コンテキスト)へ関連付ける。Work(作業)そのものの必須属性ではない。

- Artifact Type: `TARGET_LIST`
- 生成元Workflow: 変更調査

Target Listの確定生成または更新はCore(中核)へのArtifact変更要求として行わなければならない（MUST）。

Re-runの場合は既存Target Listを調査結果に基づいて更新する。過去の現在状態を最新状態として引き継いではならない（MUST NOT）。

各項目は必要に応じて、少なくとも次を表現できるものとする。

- Target ID
- 対象
- 対象箇所
- 現在状態
- 必要な対処
- 根拠
- 対処可否
- 利用者判断の要否

対象が1件だけの場合もTarget Listを生成する。

調査で変更対象が存在しないと判明した場合は、空のTarget Listを正常な調査結果として扱ってよい（MAY）。

## 5. 制限

調査中に対象を変更してはならない（MUST NOT）。

調査で新しい問題を発見したことだけを理由として、利用者要求の範囲外の項目を対処対象として確定してはならない（MUST NOT）。

## 6. 終了

Target Listを確定でき、必要な判断待ちがない場合にWorkflow完了要求を行う。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更調査Workflow
