<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261020-000000Z-CV01
lang: ja-JP
canonical_title: Core機能正常性確認Workflow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core機能正常性確認Workflow仕様

# Core機能正常性確認Workflow仕様

## 1. 目的と位置付け

本書はHLDocS v0.7.0のCore機能の正常性確認を、再現可能な検証処理として行うための専用Workflowを定義する。既存のセルフ検証Workflow仕様を共通処理契約、Coreセルフ検証仕様を検証基準として再利用する。

本WorkflowはCoreの検証・回帰検証に使用するものであり、v0.6.1相当の利用者向け実務機能を実現する通常運用Workflowの代替ではない。両者の整備・合否は分離する（MUST）。

本書の作成はWorkflowのState登録、Workflow Planへの組込み、実装の存在、検証PASS、v0.7.0通常運転の許可を意味しない。

## 2. 検証対象と入力

検証基準は`docs/ja-JP/仕様/00_Core/08_Coreセルフ検証仕様.md`とし、同仕様§2のCore正本群、および責務境界の判定に必要なState Machine、State、Work、Workflow、Capability、Restriction、Tool、Interaction、SubFlow仕様を参照する（MUST）。

入力は少なくとも対象ブランチと固定コミットSHA、検証仕様の版、検証項目、実行環境、実行可能な検証手段、Restriction Context、成果物の記録先、保存許可とする（MUST）。過去のPASSやLLM_WORKSPACEを現在の検証証跡に代用してはならない（MUST NOT）。

## 3. 検証項目

少なくとも次を区別して検証する（MUST）。

1. Core起動前提、初期State、State Machineへの制御移譲と移譲失敗時の復旧。
2. Execution Contextの一貫性、Current Work、State、Workflow Plan、ACTIVE/SUSPENDEDの管理。
3. SYSTEM/WORK Planの作成・変更・再利用・解放とRe-runの区別。
4. State Machineの遷移可否判定とCoreによる確定変更の分離。
5. Core基本制限、Restriction Setの登録・取得・適用、Fail-closed。
6. Capability ContextのAVAILABLEと実行許可の分離、Provider変更・失効・代替時の再評価。
7. 正本競合とLLM_WORKSPACEの非正本性。
8. Core復旧の開始条件、通常運転への復帰条件、復旧中の制限。
9. 仕様間の未定義参照、責務重複、依存循環、MUST/MUST NOT競合の探索。

既知の正常系だけで検証を終了してはならない（MUST NOT）。Coreセルフ検証仕様§4.6の4シナリオ、§4.7の10異常系を含める（MUST）。

## 4. 処理構成

既存のセルフ検証Workflow仕様に従い、次のセルフ検証SubFlowを順に利用する。

1. 検証対象・正本取得
2. 検証計画構成
3. 検証実行
4. 検証結果判定
5. 検証記録
6. 変更の影響がある場合の再検証範囲決定

SubFlowは単一責務に限定し、State遷移、Workflow Plan変更、利用者への直接対話、無断の正本変更を行わない（MUST NOT）。SubFlowのSUCCESSを検証項目のPASSへ読み替えてはならない（MUST NOT）。

## 5. Core自己依存の回避

検証対象Core自身による状態更新や判定結果のみをCore正常性の唯一の証拠としてはならない（MUST NOT）。

検証を次の区分に分け、証跡と判定を独立して記録する（MUST）。

- 静的仕様検証: 現在正本から期待動作・責務・制限を導出し、規則衝突を探索する。
- 模擬シナリオ検証: 明示した仮定入力と期待結果を照合する。実Coreの実行結果とみなさない。
- 実行検証: 隔離された検証対象のCoreを操作し、状態遷移、異常系、復旧を外部観測・ログ等で確認する。

実行環境や安全な注入手段がない場合、実行検証をPASSとしてはならない（MUST NOT）。静的検証がPASSでもCore実装の正常性を断定してはならない（MUST NOT）。

## 6. StateとPlanへの接続

初期段階では本Workflowを既存Stateのavailable_workflowsまたはdefault_workflow_planに登録しない（MUST NOT）。現行の情報参照Stateで読み取り専用の静的検証を行い、記録の保存や仕様修正は変更Stateの変更調査→変更対処→変更検証を経る。

将来、実CoreのState/Planを変更する動的検証を行う場合は、本番のCurrent Execution Contextを検証用入力で直接書き換えてはならない（MUST NOT）。独立した検証インスタンスまたは同等の隔離環境を用意し、検証対象の初期化・観測・終了・失敗時の隔離を定義する（MUST）。隔離環境が確保できない場合、破壊的な動的検証はBLOCKEDとして扱う。

専用検証Stateを新設するか既存Stateの検証用Planとして接続するかは、隔離方式、State Machine登録、Work Purpose、Restriction、Plan所有者、承認、終了条件を設計・検証した後に決定する。接続未決定を理由に既存StateのPlanへ暗黙追加してはならない（MUST NOT）。

## 7. 判定と成果物

検証項目ごとに対象SHA、入力、期待結果、実観測、証跡、静的/模擬/実行の区分、PASS/FAIL/UNDEFINED/BLOCKEDまたは未実施を記録する（MUST）。

全体のCore正常性PASSは、要求された検証項目と実行方式の証跡が揃い、未解決のCore阻害Issueがない場合のみ判定してよい（MAY）。実行方式を欠く項目の静的PASSを全体PASSに代用してはならない（MUST NOT）。

本Workflowの完了、Core検証PASS、v0.6.1機能同等性、v0.7.0リリース判定、mainへのマージは別々の判定とする（MUST）。

## 8. 通常運用Workflowとの関係

v0.6.1機能再構成要件のCOMP-01〜15は通常運用機能の互換性確認として維持する。文書生成・更新・検証・参照・Traceability・UI/受渡し等の利用者向けWorkflowは別途整備し、Core検証専用Workflowへ置き換えてはならない（MUST NOT）。

Coreの仕様・依存・実装・実行環境が変化した場合、本Workflowを回帰検証に利用してよい（MAY）。その際は新しい対象SHAで再判定し、過去PASSを自動継承してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Workflow > Core機能正常性確認Workflow仕様
