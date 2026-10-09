<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261009-053000Z-SV01
lang: ja-JP
canonical_title: セルフ検証SubFlow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > セルフ検証SubFlow仕様

# セルフ検証SubFlow仕様

## 1. 目的と適用範囲

本書はHLDocS自身のセルフ検証を補助するSubFlowの責務・入出力・停止条件を定義する。セルフ検証仕様そのものはdocument_type=specで管理し、外部成果物のtestspecと混同しない。

本書はSubFlowの契約であり、実行可能なランタイム、WorkflowのState登録、Workflow Planへの所属、セルフ検証PASSを保証しない。個別SubFlowは共通起動リストへ登録しない。

## 2. 共通契約

呼出し元WorkflowはWork Purpose、対象仕様・対象SHA、検証項目、適用Restriction、参照範囲を指定する（MUST）。SubFlowは指定された単一責務のみを実行し、利用者対話、State遷移、Plan変更、正本の無断変更を行ってはならない（MUST NOT）。

SubFlow返却区分は`SUCCESS`、`INSUFFICIENT_INPUT`、`CONFLICT`、`VALIDATION_FAILED`、`EXECUTION_FAILED`とする。これらはセルフ検証項目のPASS/FAIL/UNDEFINED/BLOCKEDとは独立する。実行結果には入力、観測、証跡、取得元、未取得事項を区別して含める（MUST）。

## 3. 検証対象・正本取得SubFlow

入力: セルフ検証仕様の所在、対象ブランチ・SHA、検証範囲。

処理: 指定された現在の正本と依存仕様を取得し、取得元・版・欠落・正本競合を明示する（MUST）。過去チャット、LLM_WORKSPACE、過去PASSを現在の正本の代用としてはならない（MUST NOT）。

出力: 対象正本集合、取得証跡、欠落・競合情報。

## 4. 検証計画構成SubFlow

入力: セルフ検証仕様、対象正本、実行環境と利用可能能力。

処理: 検証項目ごとに前提、入力、期待結果、実施方法、必要な証跡を対応付ける（MUST）。実行不能な項目は前提不足として明示し、試験実施済みとみなさない（MUST NOT）。

出力: 項目別の検証計画と前提充足状況。

## 5. 検証実行SubFlow

入力: 許可された検証計画、実行手段、対象環境。

処理: 許可範囲内の検査を実行し、実観測・模擬入力・未実施を区別して証跡を取得する（MUST）。対象機構自身を使う検証では自己依存を明示し、独立した静的照合や外部観測で補完する。実行手段がない場合、実行したと報告してはならない（MUST NOT）。

出力: 項目別実観測、実行ログ、実行不能理由。

## 6. 検証結果判定SubFlow

入力: 検証仕様の期待結果、実観測、証跡、未実施情報。

処理: 項目ごとにPASS/FAIL/UNDEFINED/BLOCKEDを区別する（MUST）。PASSは対象項目に要求された方法・期待値・証跡が揃う場合のみ付与する（MUST）。実行できない項目を静的規定の存在だけでPASSにしてはならない（MUST NOT）。未実施項目は判定未付与として明記し、BLOCKEDと混同しない。

出力: 項目別判定、根拠、Issue候補、未実施項目。

## 7. 検証記録SubFlow

入力: 判定結果、対象SHA、検証開始・終了時点、修正・再実行情報、保存許可。

処理: 正本と区別した結果記録を構成する。保存権限がなければ保存せず草稿を返す（MUST）。保存後の再取得・照合は呼出し元Workflowの変更検証責務に従う。

出力: 結果記録草稿、反映状態、記録先。

## 8. 再検証範囲決定SubFlow

入力: 仕様・実装・実行環境の差分、過去結果、依存関係。

処理: 影響項目と再実行範囲を提示する（MUST）。過去SHAのPASSを新しいSHAへ自動継承してはならない（MUST NOT）。同一原因で進展のない再実行を無条件に繰り返してはならない（MUST NOT）。

出力: 再検証候補、根拠、追加判断事項。

## 9. Workflowへの接続境界

SubFlowはWorkflowからのみ呼び出す。既存の変更Stateの変更調査・変更対処・変更検証を省略して検証結果を正本へ反映してはならない。読取専用の静的照合と、検証のための変更・保存を区別する。

専用セルフ検証Workflowを独立起動するには、Stateのavailable_workflowsとCurrent Planの所属、Work Purpose、Restriction、完了条件を別途定義し検証する必要がある。本書のみを根拠にPlanへ追加してはならない（MUST NOT）。

## 10. 初期適用対象

最初の適用候補は`docs/ja-JP/仕様/00_Core/08_Coreセルフ検証仕様.md`および文書生成セルフ検証仕様のDGEN-01〜18とする。Core検証PASS前にv0.7.0通常運転へ切り替えてはならない。

---

[目次](../../目次.md) > 仕様 > Workflow > セルフ検証SubFlow仕様
