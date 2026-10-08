<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261008-090100Z-SFG1
lang: ja-JP
canonical_title: 文書生成SubFlow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > 文書生成SubFlow仕様

# 文書生成SubFlow仕様

## 1. 目的と適用条件

本書は文書生成Workflowが使用する単一目的SubFlowの入出力、処理境界、失敗時の返却条件を定義する。SubFlowはWorkflowからのみ呼び出し、利用者との対話、State遷移、Workflow Plan変更を行ってはならない（MUST NOT）。

本書に定義するSubFlowは仕様案としての定義であり、実行登録・Stateからの到達性が確認されるまで稼働可能と判断してはならない（MUST NOT）。

## 2. 共通呼出し契約

呼出し元WorkflowはSubFlow ID、Work Purposeに必要な入力、参照範囲、適用Restrictionを指定する（MUST）。SubFlowは`SUCCESS`、`INSUFFICIENT_INPUT`、`CONFLICT`、`VALIDATION_FAILED`、`EXECUTION_FAILED`のいずれかと、根拠・成果物または不足事項を返す（MUST）。これらはSubFlowの返却区分であり、Workflow実行状態やセルフ検証PASSを意味しない。

SubFlowは必要な情報だけを参照し、既存文書・正本を無断変更してはならない（MUST NOT）。入力不足や矛盾を推測で補完してはならない（MUST NOT）。

## 3. 文書規則取得SubFlow

入力：対象document_type、要求種別、対象文書、正本参照先。

処理：利用可能な正本を取得し、文書共通構造、document_type別規則、Traceability、変更制限を抽出する（MUST）。常設テンプレートや生成プロンプトの有無を成功条件としてはならない（MUST NOT）。

出力：取得元と版を識別できる規則集合、未取得事項、衝突事項。

## 4. 文書構造組立SubFlow

入力：規則集合、要求内容、新規/更新/翻訳区分。

処理：共通外枠、メタデータ、種別固有の本文構造、識別子維持条件を組み立てる（MUST）。既存文書更新ではdoc_idを保持する（MUST）。`meta/apply`モードを要求してはならない（MUST NOT）。

出力：構造定義と、取得した規則から構成した生成指示。

## 5. 文書内容生成SubFlow

入力：構造定義、生成指示、根拠資料、対象文書。

処理：適用仕様の範囲で草稿を生成する（MUST）。testspecのsec_id確定、specへの反映、派生参照の扱いはTraceability仕様に従う（MUST）。仕様が未確定の場合、未確定内容を確定事項として記述してはならない（MUST NOT）。

出力：草稿と、根拠・識別子の対応情報。直接公開・保存・利用者提示はしない。

## 6. 文書整合性検査SubFlow

入力：草稿、規則集合、参照先情報。

処理：共通外枠、必須メタデータ、種別固有制約、識別子の形式・維持・参照先実在・参照用途を検査する（MUST）。検査のみの呼出しでは草稿を自動修正してはならない（MUST NOT）。

出力：合否区分、違反箇所、再生成のための具体的な指摘。合格は文書整合性の判定であり、HLDocSセルフ検証PASSではない。

## 7. 確認用派生成果物SubFlow

入力：規則集合、確認対象（テンプレート構造または生成指示）。

処理：利用者が明示的に確認を要求した場合に限り、適用仕様から確認用の構造または説明可能な生成指示を構成する（MUST）。内部の非公開推論過程や隠された逐語プロンプトを再現するものではない。

出力：確認用派生成果物。正本仕様または常設生成ファイルとして自動登録してはならない（MUST NOT）。

## 8. Workflowによる統合と再試行

Workflowは規則取得、構造組立、内容生成、整合性検査の順で必要なSubFlowを選択する。確認要求では確認用派生成果物SubFlowを選択し、文書生成を必須としない。

検査違反が修正可能ならWorkflowが再生成の要否を判断する。再試行時は違反内容と変更した入力を記録し、同じ条件で無限に再実行してはならない（MUST NOT）。正本変更、Work Purpose拡張、利用者承認を要する変更はWorkflowがInteraction経由で判断を求める（MUST）。

SubFlowの返却結果だけでWorkflowをCOMPLETEDへ変更してはならない（MUST NOT）。完了要求はWorkflowがCoreへ行う。

## 9. 登録・整合性に関する未完了事項

現行の共通「Workflow・SubFlow仕様」には、SubFlowは共通仕様成立条件の仕様要素一覧へ登録される必要がある旨の規定がある。一方、現行の共通仕様成立条件の一覧は起動に必要な仕様要素を列挙しており、個別SubFlowの登録簿として扱うかは未確定である。この矛盾は登録方式を確認して解消する必要がある。

本書の作成だけではSubFlowの登録、実行可能性、Workflow Planへの組込み、セルフ検証完了を意味しない。

---

[目次](../../目次.md) > 仕様 > Workflow > 文書生成SubFlow仕様
