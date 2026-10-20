<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261020-000001Z-CV02
lang: ja-JP
canonical_title: Core機能正常性確認接続・隔離仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core機能正常性確認接続・隔離仕様

# Core機能正常性確認接続・隔離仕様

## 1. 目的

本書はCore機能正常性確認Workflowの起動接続、検証対象の隔離、証跡採取、失敗時の停止、結果反映の境界を定義する。検証項目はCore機能正常性確認Workflow仕様とCoreセルフ検証仕様に従う。

本書は設計仕様であり、隔離実行環境の存在や実行検証PASSを保証しない。

## 2. 接続方針

初期接続方式は**既存Stateを利用するWorkベースの検証オーケストレーション**とする。専用Stateは現時点では新設しない。専用Core機能正常性確認WorkflowはState Machineへ登録しない。

- 読取専用の正本照合・静的検証要求は情報参照Stateの情報参照Workflowで処理する。
- 検証計画・記録の作成、正本修正、保存と再取得が必要な要求は変更Stateの変更調査→変更対処→変更検証を使用する。
- 上記の既存Workflowは、既存のセルフ検証SubFlow仕様の責務を満たす処理を組み込んでよい。ただし未登録の専用WorkflowをACTIVEとみなしたり、Current Planへ暗黙追加したりしてはならない（MUST NOT）。
- 利用者の要求が参照だけか変更を含むかはStateのwork_acceptanceに従って選択する。検証結果から変更が必要と判明しただけでWork Purposeを拡張してはならない（MUST NOT）。

独立Workflowとしての登録は、後述の接続ゲートを満たすまで保留する。

## 3. 実行主体の分離

- **Orchestrator（検証制御側）**: 現行HLDocSのCore/State/Workflow規則に従い、検証計画、隔離対象への入力、観測証跡、結果判定、保存許可を管理する。
- **SUT（検証対象Core）**: 固定SHAのCore仕様・実装に基づいて検証入力を処理する独立インスタンス。SUTのExecution Contextは検証対象の内部状態であり、OrchestratorのCurrent Execution Contextとは異なる。
- **Observer（独立観測側）**: SUTの外部出力、ログ、状態スナップショット、拒否・停止結果を取得し、入力と対応付ける。SUT自身の成功申告だけを唯一の証拠としてはならない（MUST NOT）。

SUTのState変更やPlan操作はSUT内のCore規則によってのみ行う。OrchestratorがSUTのExecution Contextを直接上書きして期待結果を捏造してはならない（MUST NOT）。

## 4. 隔離環境の要件

動的検証の開始前に次をすべて満たさなければならない（MUST）。

1. SUTを対象SHA・仕様版・設定・依存情報と結び付けて識別できる。
2. SUTのExecution Context、Work、Plan、履歴、検証用保存先がOrchestratorと分離されている。
3. Tool/Providerの実行先を検証用に制限でき、外部の実正本・本番リポジトリ・利用者資産を変更しない。
4. 起動前の初期状態を観測または再現でき、シナリオごとに初期化できる。
5. 障害注入はSUTの境界入力または検証用依存の置換で行い、SUT内部の確定状態を外部から不正変更しない。
6. Observerが入力、時刻、期待値、実観測、ログ、終了状態を紐付けて取得できる。
7. 中断・タイムアウト・予期しない実行時エラーでSUTを停止・隔離し、残存する副作用を検査できる。
8. 保存・修正を伴う場合、利用者の承認と現行Workの変更権限を満たす。

一つでも満たせない場合、その隔離方式に依存する動的検証を開始してはならない（MUST NOT）。結果は未実施またはBLOCKEDとし、静的検証の結果とは分ける。

## 5. 検証実行プロトコル

1. **準備**: 対象ブランチ・SHA、Core検証仕様、ケースID、期待結果、隔離方式、観測方法を固定する。
2. **隔離確認**: SUTの保存先、外部接続、Provider/Toolの許可先、停止方法を確認する。
3. **初期化**: ケースごとにSUTを既知状態から開始する。前ケースのExecution Contextを暗黙に再利用しない。
4. **実行**: 正常系入力または定義済み異常入力を与える。実際のSUTが処理したか、模擬規則を評価しただけかを区別する。
5. **観測**: Observerが状態遷移、拒否、停止、復旧、残存副作用を記録する。
6. **判定**: 期待結果と実観測を照合する。証跡不足はPASSにしない。
7. **終了**: SUTを停止・破棄し、残存変更を確認する。検証結果の正本反映は既存変更Workflowの承認・再取得規則を使用する。

Coreセルフ検証仕様§4.6のWS-01〜04、§4.7のFC-01〜10を対象ケースとして含める（MUST）。失敗・中断時もケースIDと未完了理由を残す（MUST）。

## 6. Fail-closedと復旧

SUTのCore起動失敗、State Machineへの制御移譲失敗、必須Restrictionの不成立、Capability evidenceの失効、復旧不能状態では、対象SUTの処理を停止し、実行を継続させてはならない（MUST NOT）。

検証対象のCore復旧規則と、Orchestratorの失敗処理は別物とする。SUT復旧の検証に失敗しても、OrchestratorのCurrent StateやPlanをSUT側へ移植・復元してはならない（MUST NOT）。

同じ原因で進展のない自動再試行を繰り返してはならない（MUST NOT）。再実行時は対象SHA・入力・初期化条件・前回との差分を記録する（MUST）。

## 7. 独立Workflow登録ゲート

専用Core機能正常性確認Workflowをavailable_workflowsまたはdefault_workflow_planへ登録する前に、次を満たす必要がある（MUST）。

- State Machineの遷移規則とState個別仕様に矛盾しない接続先Stateとwork_acceptanceが定義される。
- WORK/SYSTEMのPlan Owner、Work Purpose、Plan変更承認、Workflow開始・終了条件が確定する。
- 必須RestrictionとCapability/Provider/Toolの利用許可が定義される。
- SUT隔離・Observer証跡・異常時停止が検証される。
- Workflow実行完了とCore検証PASSの区別が維持される。
- 接続変更に伴うCoreセルフ検証の影響範囲を再検証する。

これらが成立するまでは、既存State/Planへ本Workflowを暗黙追加してはならない（MUST NOT）。専用Stateの新設は必要性が確認された場合に別途判断する。

## 8. 結果記録

各ケースは少なくとも`case_id`、`target_sha`、`test_mode`（STATIC/SIMULATED/EXECUTED）、`preconditions`、`expected`、`observed`、`evidence`、`verdict`、`unexecuted_reason`、`side_effects`を保持する（MUST）。

STATIC/SIMULATEDのPASSはEXECUTEDのPASSを意味しない（MUST NOT）。Core正常性、v0.6.1機能同等性、v0.7.0リリースは別々に判定する。

---

[目次](../../目次.md) > 仕様 > Workflow > Core機能正常性確認接続・隔離仕様
