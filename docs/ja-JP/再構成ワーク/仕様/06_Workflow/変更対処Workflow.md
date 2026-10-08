<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-080000Z-WFCA
lang: ja-JP
canonical_title: 変更対処Workflow
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 変更対処Workflow

# 変更対処Workflow(ワークフロー)

## 1. 目的

変更調査Workflow(ワークフロー)が生成したTarget List(対処対象リスト)に従って、許可された変更を実施する。

## 2. 開始条件

- Current Stateが変更Stateである。
- 本WorkflowがCurrent Workflow Plan内で`PENDING(未実行)`である。
- 変更調査Workflowが`COMPLETED(完了)`である。
- 対象WorkのWork Context(作業コンテキスト)からArtifact Type=`TARGET_LIST`のTarget Listを参照できる。
- 対処に必要なRestriction Context(制限コンテキスト)を適用できる。

## 3. 処理

1. Target Listの各項目について最新の対象状態を確認する。
2. 調査時点から状態が変化している場合は、そのまま対処せず当該Targetを`RESEARCH_REQUIRED(再調査必要)`として記録する。
3. 対処可能かつ必要な承認根拠を満たす項目だけを処理する。
4. Core(中核)の検証を経て必要なTool(ツール)または能力提供手段を実行する。
5. 各項目の実行結果をTarget Listに対応付けたArtifact(作業成果物)として記録する。
6. `RESEARCH_REQUIRED(再調査必要)`が存在する場合、変更対処Workflow内で調査をやり直さず、後続判断へ引き渡す。

### 3.1 文書生成・更新の対処

Target Listの対処がHLDocS文書の新規生成・更新・翻訳である場合、必要に応じて文書規則取得、文書構造組立、文書内容生成、文書整合性検査の各SubFlowを呼び出してよい（MAY）。呼出し前に各SubFlow仕様と適用Restrictionを確認する（MUST）。

SubFlowの結果はTarget Listの対象項目に対応付けた対処結果Artifactとして記録し、保存・反映の許可と結果を区別する（MUST）。草稿の整合性検査が合格しても、変更権限や反映先が未確認なら保存してはならない（MUST NOT）。

SubFlowの実行は変更調査・変更検証Workflowの責務を代替しない。変更検証Workflowは反映後の対象状態を独立に確認する（MUST）。

## 4. 空のTarget List

Target List(対処対象リスト)が空の場合も、本Workflowを自動的に`SKIPPED(スキップ)`としてはならない（MUST NOT）。

空のTarget Listが有効な調査結果であることを確認した場合、変更を実行せず、対処対象が0件であったことを対処結果Artifact(作業成果物)として記録し、正常なno-opとして完了してよい（MAY）。

この場合も後続の変更検証Workflow(ワークフロー)でWork Purposeとの整合を確認する。

## 5. 制限

Target Listに存在しない変更を暗黙に追加してはならない（MUST NOT）。

Target Listの内容と実体が不一致の場合、調査結果を正しいものとして強制適用してはならない（MUST NOT）。

対処不能、失敗または追加判断が必要な項目を成功として扱ってはならない（MUST NOT）。

## 6. 再調査が必要な場合

`RESEARCH_REQUIRED(再調査必要)`は対処失敗と同一ではなく、調査時点の前提が現在状態と一致しなくなったことを示す。

変更対処Workflow(ワークフロー)は、`RESEARCH_REQUIRED`となったTargetについて次を行ってはならない（MUST NOT）。

- 古いTarget Listを強制適用する。
- 変更対処Workflow内部で変更調査処理を代行する。
- Core(中核)を介さずWorkflow状態を変更する。

再調査が現在のWork Purpose達成に必要であり、変更調査Workflow仕様の範囲内である場合、変更対処Workflowは自身を`SUSPENDED(中断中)`とする要求と、`[変更調査Workflow]`からなるRe-run Sequence(再実行列)要求をCoreへ提示してよい（MAY）。

再調査のためにWork Purposeを拡張したり、利用者が要求していない追加変更を対象へ含めたりしてはならない（MUST NOT）。その必要がある場合はInteraction(対話窓口)による利用者判断を要求する。

再調査完了後、Target List(対処対象リスト)が更新され、開始条件を再度満たす場合、Coreは中断していた変更対処Workflowを`ACTIVE(実行中)`へ復帰させてよい（MAY）。

## 7. 終了

Target Listの対処対象について、実行結果または実行不能理由を確定できた場合にWorkflow完了要求を行う。

---

[目次](../../目次.md) > 仕様 > Workflow > 変更対処Workflow
