# Core仕様群確認結果

確認日: 2026-10-07  
対象: `docs/ja-JP/仕様/00_Core/`

## 1. 位置付け

本書は2026-10-07時点の検証結果記録であり、Core検証手順の正本ではない。

Coreを新しいチャットまたは新しい実行環境で再検証する場合は、`docs/ja-JP/仕様/00_Core/08_Coreセルフ検証仕様.md`を使用し、現在の正本から再判定する。

過去チャットまたはLLM_WORKSPACEの内容を、本書に不足する検証条件の補完根拠としてはならない。

## 2. 対象

- 01_HLDocSとは.md
- 02_HLDocSシステム起動条件.md
- 03_Core仕様.md
- 04_Core基本制限仕様.md
- 05_Core復旧仕様.md
- 06_用語表記規則.md
- 07_CapabilityContext仕様.md

## 3. 結果

| ID | 対象 | 結果 | 内容 |
| --- | --- | --- | --- |
| CR-01 | HLDocSとは | FIXED | 基本責務領域にCapabilityが欠落していた |
| CR-02 | HLDocSとは | FIXED | Toolを「能力提供」としていた旧表現を具体的操作インターフェースへ修正 |
| CR-03 | Core仕様 | FIXED | Capability Providerを実行主体として扱う表現をTool実行へ修正 |
| CR-04 | Capability Context | FIXED | Provider実行という旧表現をProviderに対応するTool実行へ修正 |
| CR-05 | 起動条件 | FIXED | 起動に必要なCore基本制限仕様の参照要求が明示されていなかった |
| CR-06 | Core基本制限 | FIXED | 「外部能力」に限定した表現をToolその他の実行手段へ一般化 |
| CR-07 | 正本競合 | PASS | Version Up時の複数正本候補を許容し、一意選択不能時のみCanonical Conflictとする |
| CR-08 | 起動/通常運転 | PASS | Core起動完了とState Machine移譲後の通常運転開始が分離されている |
| CR-09 | 復旧 | PASS | 起動条件不成立とState Machine移譲失敗後のCore復旧が分離されている |
| CR-10 | Execution Context | PASS | 確定状態の変更主体をCoreへ限定している |
| CR-11 | Restriction | PASS | Core基本制限と通常Restriction Setが分離され、下位から緩和できない |
| CR-12 | Capability | PASS | AVAILABLEと実行許可が分離されている |
| CR-13 | LLM_WORKSPACE | RESOLVED | 独立責務領域ではなくCoreの補助記憶としてCore仕様へ統合 |
| CR-14 | 復旧責務境界 | RESOLVED | Core仕様は復旧への移行まで、復旧開始後はCore復旧仕様の責務として分離 |

## 4. 現在のCore境界

```text
起動前
 ↓
Core基本制限
 ↓
HLDocSシステム起動条件
 ↓
Core起動
 ↓
State Machineへ移譲
 ├─ 成功
 │   ↓
 │ 通常運転
 │   ↓
 │ Execution ContextをCoreが管理
 │
 └─ 失敗
     ↓
   Core復旧
     ↓
   再検証・再移譲
```

通常運転中の実行許可は、Capability利用可能性だけでは成立しない。

```text
Capability Context
  AVAILABLE
      +
Capability Provider照合
      +
Restriction Context
      +
対象範囲
      +
必要な承認・実行条件
      ↓
Toolその他の実行手段
```

## 5. 正本

複数の正本候補の存在自体は異常ではない。

Version Up、移行、再構成、比較その他の理由で候補が併存してよい。

現在採用する正本を利用者指定、対象版、ブランチ、配置先、登録情報その他の明示的根拠で一意に確定できない場合のみCanonical Conflict(正本競合)とする。

## 6. 解決した境界

### 6.1 LLM_WORKSPACE

LLM_WORKSPACEはHLDocSの独立した実行責務領域とせず、Core(中核)が作業継続および復元を補助するために利用できる一時記憶領域とした。

LLM_WORKSPACEは正本またはExecution Context(実行コンテキスト)を代替しない。保存情報を再利用する場合は、現在採用する正本、現在の実体および現在の実行環境との整合性を必要な範囲で再確認する。

### 6.2 Core復旧

Core仕様の復旧責務は、State Machine(状態遷移機構)への制御移譲失敗を検出し、通常運転を開始せずCore復旧へ移行するまでとした。

復旧開始後の実行状態、制限、調査、変更、利用者判断、再検証およびState Machineへの再移譲はCore復旧仕様の責務とする。

このため、復旧Restriction Setの具体的な取得・登録方式はCore基本モデルの未解決事項として扱わない。

## 7. 判定

Core仕様群の起動、実行状態管理、Fail-closed、正本競合、Capability/Restriction境界について、現時点で重大な循環依存または責務逆転は確認していない。

前回OPENであったLLM_WORKSPACEおよび復旧責務境界も解決したため、Core仕様群について現時点で未解決の責務境界は確認していない。

Core復旧仕様内部の詳細設計および後続層の再構成でCore境界に変更が生じた場合は、本確認を再実施する。

## 検証履歴メタデータ

- 検証対象ブランチ: `develop`
- 検証対象コミットSHA: **未記録（当時の結果から特定不可）**
- 検証終了時コミットSHA: **未記録（当時の結果から特定不可）**
- 対応セルフ検証仕様: `docs/ja-JP/仕様/00_Core/08_Coreセルフ検証仕様.md`
- 記録区分: 過去の検証結果（新仕様による再検証は未実施）

※ 検証対象コミットを現在のHEADや移動コミットで代用してはならない。
