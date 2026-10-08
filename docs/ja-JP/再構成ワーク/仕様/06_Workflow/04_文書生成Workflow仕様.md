<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261008-090200Z-DWF7
lang: ja-JP
canonical_title: 文書生成Workflow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 文書生成Workflow仕様

# 文書生成Workflow仕様

## 1. 目的

本書はHLDocSによる文書の新規生成、更新、翻訳、および確認用派生成果物の提示を進行させるWorkflowの処理条件を定義する。対象document_typeに固有の本文規則は対応仕様に従う。

本Workflowは共通仕様成立状態でのみ使用できる（MUST）。Workflow開始・完了、Plan変更、State遷移の検証はCoreおよびWorkflow共通仕様に従い、本書だけで実行を開始できるものではない。

## 2. 入力と成果物

入力はWork Purpose、要求種別（新規生成・更新・翻訳・確認）、対象document_type、対象文書または生成先、利用可能な正本情報源、必要な制限・承認情報とする。

出力は要求に対応する文書成果物または確認用派生成果物、参照した正本の識別情報、検査結果、未解決事項および保存・反映結果とする。

不足する入力は利用可能な情報源を調べてから不足として扱う（MUST）。取得不能な正本を推測で補完してはならない（MUST NOT）。

## 3. 開始条件

本WorkflowはCurrent Stateのavailable_workflowsに登録され、Current Workflow Planに所属し、PENDINGであり、同時ACTIVEが存在せず、Restrictionが適用可能な場合にのみCoreが開始できる（MUST）。

利用者の要求だけでPlan外のWorkflowを自動追加してはならない（MUST NOT）。Owner=WORKのPlan変更には既存Workflow仕様の承認規則を適用する。

## 4. SubFlowの呼出し順

WorkflowはWork Purposeに応じて次のSubFlowを選択し、各呼出し前に対応仕様、入力、適用制限を確認する（MUST）。

1. 文書規則取得：対象種別の共通・固有規則、正本、変更制限を取得する。
2. 文書構造組立：新規・更新・翻訳の別に応じ、構造、メタデータ、生成指示を組み立てる。
3. 文書内容生成：根拠資料に基づき草稿を生成する。
4. 文書整合性検査：草稿と規則・参照関係の整合を判定する。

確認要求では、文書規則取得後に確認用派生成果物SubFlowを選択してよい（MAY）。確認のみの要求に対して文書内容生成、保存、仕様変更を暗黙に行ってはならない（MUST NOT）。

SubFlowの返却区分は`SUCCESS`、`INSUFFICIENT_INPUT`、`CONFLICT`、`VALIDATION_FAILED`、`EXECUTION_FAILED`とする。SUCCESS以外の場合は次段へ無条件に進めてはならない（MUST NOT）。

## 5. document_typeと識別子

対象種別は`index`、`spec`、`testspec`、`note`、`minutes`、`usage`を少なくとも扱う。各種別の正本仕様が未取得の場合は、旧版仕様をv0.7.0の正本と推定して生成してはならない（MUST NOT）。

新規文書には新規doc_idを付与し、更新・翻訳では論理同一性を維持する（MUST）。testspecとspecの検証参照、note/minutesの派生参照はTraceability仕様に従う（MUST）。

`meta/apply`の指定を要求してはならない（MUST NOT）。常設テンプレートや生成プロンプトが存在しないことだけを理由に処理を停止してはならない（MUST NOT）。

## 6. 検査・修正・再生成

文書整合性検査が失敗した場合、Workflowは違反内容、修正可能性、正本の更新有無、変更権限を評価する（MUST）。

同一Work Purposeと既存承認の範囲で修正可能な草稿の問題は、入力を更新して構造組立または内容生成から再実行してよい（MAY）。再試行では前回からの変更点と未解決条件を記録する（MUST）。有意な進展がない場合、同一条件の再試行を無条件に繰り返してはならない（MUST NOT）。

正本間の矛盾、要求範囲の拡張、権限不足、利用者判断を必要とする仕様変更は、Interactionを介して利用者へ判断を求める（MUST）。SubFlow自身が利用者と対話してはならない（MUST NOT）。

## 7. 成果物の反映

検査合格だけで保存・公開・既存正本の上書きを許可してはならない（MUST NOT）。WorkflowはWork Purpose、対象の変更権限、保存先、適用Restrictionを確認し、許可されたTool/Capabilityを使用して反映する（MUST）。

保存・反映の成否と反映先の識別情報を記録する（MUST）。反映後に取得可能な場合は対象を再取得して反映結果を確認する（MUST）。保存失敗を文書生成成功として報告してはならない（MUST NOT）。

確認用派生成果物は正本として自動保存しない（MUST NOT）。

## 8. 終了条件

Workflowは、要求された成果物の生成・検査と、要求に含まれる場合の保存・反映確認が完了し、未解決の必須判断がないとき、CoreへCOMPLETEDを要求してよい（MAY）。

SubFlow成功や検査合格をもって自動的にWorkflow完了、Work完了、State遷移完了とみなしてはならない（MUST NOT）。未解決事項がある場合は結果と不足条件を明示し、対応する中断・判断待ち・変更対処の規則に従う。

## 9. 接続と検証上の制約

本仕様は文書生成Workflowの処理定義である。Stateのavailable_workflowsとWorkflow Planへの登録は別途必要であり、本書の作成だけで到達可能にならない。

受入検証では新規生成、既存更新、翻訳、確認要求、正本欠落、正本矛盾、検査失敗、再生成、保存権限不足、保存失敗を扱う。検証未実施の項目をPASSとしてはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Workflow > 文書生成Workflow仕様
