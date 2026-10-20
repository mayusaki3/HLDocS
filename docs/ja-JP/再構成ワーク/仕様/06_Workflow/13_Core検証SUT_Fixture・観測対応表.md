<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261020-000004Z-CV05
lang: ja-JP
canonical_title: Core検証SUT Fixture・観測対応表
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core検証SUT Fixture・観測対応表

# Core検証SUT Fixture・観測対応表

## 1. 目的

Core正常性確認ケース定義のWS-01〜04、FC-01〜10について、実Coreを用いた動的検証に必要な初期fixture、境界注入、外部観測点を具体化する。これは実装・実行前の**設計上の対応表**であり、実施証跡ではない。

## 2. 実行入口の調査結果と制約

2026-10-20のdevelopツリー確認では、Coreを起動する実行ファイル、Core実装ソース、SUT用テストハーネスは特定できなかった。確認できた`scripts/check_links.py`はMarkdownリンクの静的検査であり、Coreの実行入口ではない。

従って本書では特定言語・CLI名・実装済みイベント名を仮定しない。各fixtureは**必要な境界能力の契約**を表す。実行入口・入力API・Observerを特定するまでEXECUTEDは未実施とする（MUST）。

## 3. ケース別対応表

| ID | 初期fixture | 境界注入 | Observerの観測対象 | 必須不変条件 |
| --- | --- | --- | --- | --- |
| WS-01 | 正本スナップショットあり／WORKSPACEなし | 起動入力でWORKSPACE参照を省略 | 正本取得ログ・検証開始可否 | WORKSPACE生成や旧履歴の自動採用なし |
| WS-02 | 正本あり／保存された旧Contextあり | 復元候補として旧Contextを供給 | 復元検証・Current Context前後 | 旧Contextを無検証で確定しない |
| WS-03 | Provider利用可能証跡の版が旧 | Provider照合応答を変更 | 再照合要求・利用可否判断 | 旧AVAILABLEで実行しない |
| WS-04 | 正本とWORKSPACEに相反する規則 | 二情報源を別々に供給 | 採用正本ID・競合ログ | WORKSPACEで正本を書き換えない |
| FC-01 | 必須Set参照あり／Set取得先欠落 | Restriction取得スタブでnot-found | 処理拒否・Provider呼出し回数 | 対象操作を実行しない |
| FC-02 | 不整合な復元Context候補 | 復元入力でPlan/State矛盾を供給 | 復元判定・Context前後 | 不整合を確定しない |
| FC-03 | 待機State／禁止遷移先 | State遷移要求として未定義の遷移を供給 | State Machine判定・Current State | State不変 |
| FC-04 | 旧StateのACTIVE Planが残存 | 次Stateへの進入要求を供給 | Plan生成・解除イベント | Planを上書き・重複生成しない |
| FC-05 | Owner=WORK／承認記録なし | Plan追加要求を供給 | 承認判定・Plan構成差分 | Plan構成不変 |
| FC-06 | Owner=SYSTEM／変更根拠なし | Plan並べ替え要求を供給 | 仕様根拠検証・Plan構成差分 | Plan構成不変 |
| FC-07 | Capability AVAILABLE／Restriction拒否 | Provider実行要求を供給 | Restriction判定・Tool呼出し回数 | Tool呼出しゼロ |
| FC-08 | Capability evidence期限切れ | Provider実行前に失効を通知 | 再確認イベント・実行可否 | 旧証跡で実行しない |
| FC-09 | Re-run Sequence進行中／次要素不成立 | 次Workflow開始条件を拒否 | Sequence位置・ACTIVE数・停止理由 | 残要素未実行、ACTIVE最大1 |
| FC-10 | Initial State仕様取得不能 | State Machine初期化時に取得失敗 | 制御移譲・復旧遷移・通常運転開始 | 通常運転未開始 |

## 4. Fixture構成契約

各ケースのfixtureは少なくとも`fixture_id`、`case_id`、`target_sha`、`canonical_snapshot`、`initial_context`、`provider_stub`、`restriction_stub`、`fault_injection`、`expected_invariants`を識別する（MUST）。

- 正本スナップショットは対象SHAで固定し、検証ケースによる破壊的変更から分離する。
- 初期ContextはSUT自身の初期化・復元入力で構成し、OrchestratorのCurrent Execution Contextを複製・改変してはならない（MUST NOT）。
- Provider/Restrictionスタブは隔離環境内に閉じ、実リポジトリや利用者資産への書込み権限を与えない（MUST）。
- 障害注入点はSUTの実行境界に実在することを確認する。確認不能な場合は未実施とする（MUST）。

## 5. Observerの最低契約

Observerは入力イベント、拒否/許可、State/Plan/Workの前後状態、Provider/Tool呼出しの有無、復旧遷移、停止、外部副作用をケースIDに紐付けて記録する（MUST）。内部ログのみで独立観測ができない項目は、ログ以外の証跡が得られるまでEXECUTED PASSにしてはならない（MUST NOT）。

## 6. 実装着手ゲート

実装前に次を確定する（MUST）。

1. SUT実装と起動入口、対象SHAとの対応。
2. SUTを隔離実行できる具体的な環境と停止・破棄方法。
3. Fixtureの境界注入APIと、対象Coreを直接改変しない方法。
4. Observerの状態・Tool呼出し・副作用の取得手段。
5. 各ケースの初期化・期待結果・後始末を実際に再現できること。

満たせないケースはBLOCKEDまたは未実施として管理し、模擬モデルのPASSを実CoreのPASSへ昇格してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Workflow > Core検証SUT Fixture・観測対応表
