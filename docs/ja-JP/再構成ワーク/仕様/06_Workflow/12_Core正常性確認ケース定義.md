<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261020-000003Z-CV04
lang: ja-JP
canonical_title: Core正常性確認ケース定義
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core正常性確認ケース定義

# Core正常性確認ケース定義

## 1. 目的

Coreセルフ検証仕様§4.6・§4.7に定めるシナリオを、Core検証SUT実行・観測インターフェース仕様で実行可能なケース契約として整理する。本書は検証入力と期待結果の**仕様**であり、実施結果またはdocument_type=testspecではない。

## 2. 共通前提

各ケースで対象SHAを固定し、初期状態・注入点・観測手段・期待結果・残存副作用を記録する（MUST）。境界入力として再現できない異常は無理にSUT内部を書き換えず、実行不能理由を記録する（MUST）。

期待結果の判定にはCore仕様、Core復旧仕様、State Machine仕様、Workflow仕様、Restriction Set仕様、Capability Context仕様を適用する。以下の要約だけで細部を推測補完してはならない（MUST NOT）。

## 3. ケース一覧

| ケース | 境界入力・障害条件 | 期待結果 | 不変条件 |
| --- | --- | --- | --- |
| WS-01 | LLM_WORKSPACE不在 | 現在正本のみでCore検証を開始可能 | WORKSPACEの欠落を正本欠落と誤認しない |
| WS-02 | 古いExecution Context情報 | 保存済み情報のみでCurrent Contextを確定しない | 復元前の整合確認を要求 |
| WS-03 | Provider/evidence変更 | 旧AVAILABLEを再利用せず再評価する | 旧証跡を許可根拠にしない |
| WS-04 | WORKSPACEと正本の競合 | 現在採用する正本を優先する | WORKSPACEによる正本上書きを拒否 |
| FC-01 | 必須Restriction Set取得不能 | 制限なしの処理継続を拒否 | 実行を止め不足を通知 |
| FC-02 | Execution Context不整合 | 矛盾するContextを確定しない | 旧状態保持または復旧 |
| FC-03 | 未許可State遷移 | State Machineが拒否しCoreは確定変更しない | Current State保持 |
| FC-04 | 旧State未完了Plan残存 | 新Planを重ねて生成しない | 未完了Planを暗黙破棄しない |
| FC-05 | WORK Plan変更の承認なし | 構成変更を確定しない | 承認要求または拒否 |
| FC-06 | SYSTEM Plan変更の仕様根拠なし | 構成変更を確定しない | 推測による変更を拒否 |
| FC-07 | Capability AVAILABLEかつRestriction不成立 | Tool/Provider実行を拒否 | AVAILABLEを実行許可としない |
| FC-08 | Capability evidence失効 | 再確認なしにAVAILABLEを継続しない | Provider状態を再評価 |
| FC-09 | Re-run Sequence次要素開始不能 | 残要素を強行せず停止 | 原因を引渡し、同時ACTIVEを作らない |
| FC-10 | State Machine制御移譲失敗 | 通常運転を開始せずCore復旧へ | 通常Stateへの強制進入を拒否 |

## 4. 実行前のケース詳細化

各ケースは実行前に次を確定しなければならない（MUST）。

1. `case_id`、対象SHA、適用仕様と版。
2. SUTの初期状態（State、Plan、Work、Restriction、Capability evidence）と隔離fixture。
3. 障害または入力の**境界注入点**と、注入前の成立条件。
4. 期待する許可・拒否・復旧・中断、Execution Contextの前後不変条件。
5. Observerの外部観測方法、ログ・状態・副作用の証跡。
6. ケース終了時のSUT停止・隔離解除・副作用確認方法。

注入点が未定義、期待結果が正本から導けない、またはObserverが独立観測できない場合、EXECUTEDをPASSとしてはならない（MUST NOT）。必要な仕様が欠ける場合はUNDEFINED、必要な実行手段が欠ける場合はBLOCKED、未着手はUNEXECUTEDと区別する。

## 5. 正常系と横断探索

上記14ケースだけでCoreの正常性を網羅したとみなしてはならない（MUST NOT）。起動・通常運転移行、State/Plan/Workの正常完了、Restriction成立時の実行、復旧成功、Canonical Conflictの一意解決と非一意停止、および仕様間の依存循環・未定義参照・MUST/MUST NOT競合を別途検証する（MUST）。

## 6. 記録と完了条件

ケースごとにSTATIC/SIMULATED/EXECUTEDを分けて判定する。未実施をPASSとしてはならない（MUST NOT）。Core全体のPASSはCoreセルフ検証仕様とCore機能正常性確認Workflow仕様の全必須条件を満たす場合に限る。

---

[目次](../../目次.md) > 仕様 > Workflow > Core正常性確認ケース定義
