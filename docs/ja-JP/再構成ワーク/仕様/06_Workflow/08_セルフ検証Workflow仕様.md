<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261009-053100Z-SW01
lang: ja-JP
canonical_title: セルフ検証Workflow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > セルフ検証Workflow仕様

# セルフ検証Workflow仕様

## 1. 目的

HLDocS自身のセルフ検証を一連の処理として管理し、対象版の正本から再現可能な検証結果を得るためのWorkflow処理設計を定義する。本書は接続前の処理仕様であり、独立WorkflowのState登録または実行可能性を保証しない。

## 2. 開始前提

Work Purpose、対象ブランチ・SHA、セルフ検証仕様、利用可能な検査手段、Restriction Context、記録先と保存許可を確定する。対象が未確定の場合、推測で検証を開始しない（MUST NOT）。

## 3. 処理順序

1. 検証対象・正本取得SubFlowを呼び出し、対象SHAにおける正本と依存を取得する。
2. 検証計画構成SubFlowで項目別の前提・期待結果・証跡を定める。
3. 検証実行SubFlowで可能な項目を実施し、実観測と未実施を区別する。
4. 検証結果判定SubFlowでPASS/FAIL/UNDEFINED/BLOCKEDを判定する。
5. 検証記録SubFlowで記録を構成し、変更権限を満たす場合のみ反映する。
6. 変更の影響があれば再検証範囲決定SubFlowを利用し、再実行対象を明示する。

SubFlowのSUCCESSを検証項目PASSと読み替えてはならない（MUST NOT）。Workflow完了はCoreへ要求し、Work完了やState遷移を独断で確定しない。

## 4. 独立性と異常系

Core・State Machine・Workflow自身の検証では、検証対象機構の実行結果だけを唯一の合格根拠としてはならない（MUST NOT）。独立した仕様照合・外部証跡と実行結果の範囲を区別する。

正本不足、競合、検証手段不足、保存権限不足、無進展の再試行は、原因を明示して停止・判断要求へ引き渡す。未実施項目を自動PASSにしない。

## 5. 既存Stateとの接続方針

現段階では独立セルフ検証Workflowを変更Stateまたは情報参照Stateのavailable_workflows/default_workflow_planへ登録しない。読み取り専用の検証は情報参照Workの範囲で行えるが、結果保存や修正は変更Workとして既存の変更調査・変更対処・変更検証を経る（MUST）。

将来の独立登録はState/Plan、Work Purpose、権限、Target List受け渡し、保存・再取得、完了条件の成立を確認したうえで別途決定する。

## 6. v0.7.0への移行ゲート

新しいチャットでv0.7.0へ切り替える前に、現在のCoreセルフ検証仕様に従い現在の対象SHAでCore検証を再実施し、必須項目のPASSと未解決阻害事項なしを記録する（MUST）。過去のCore確認結果・異常系10/10 PASSは当時の記録であり、現在SHAのPASSを代替しない。

切替時は新チャットでv0.7.0の正本と検証結果を改めて取得する。新チャットが過去の会話記憶だけを根拠にv0.7.0運用を開始してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Workflow > セルフ検証Workflow仕様
