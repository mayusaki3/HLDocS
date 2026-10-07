# Core仕様群確認結果

確認日: 2026-10-07  
対象: `docs/ja-JP/再構成ワーク/仕様/00_Core/`

## 1. 対象

- 01_HLDocSとは.md
- 02_HLDocSシステム起動条件.md
- 03_Core仕様.md
- 04_Core基本制限仕様.md
- 05_Core復旧仕様.md
- 06_用語表記規則.md
- 07_CapabilityContext仕様.md

## 2. 結果

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
| CR-13 | LLM_WORKSPACE | OPEN | 基本構成から参照されるが、新構造側の個別仕様は未再構成 |
| CR-14 | 復旧Restriction Set | OPEN | Core復旧固有の追加制限と通常Restriction Set登録機構の関係を後続Restriction設計で確認する |

## 3. 現在のCore境界

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

## 4. 正本

複数の正本候補の存在自体は異常ではない。

Version Up、移行、再構成、比較その他の理由で候補が併存してよい。

現在採用する正本を利用者指定、対象版、ブランチ、配置先、登録情報その他の明示的根拠で一意に確定できない場合のみCanonical Conflict(正本競合)とする。

## 5. 未解決事項

### 5.1 LLM_WORKSPACE

`01_HLDocSとは.md`では基本責務領域として定義されているが、新構造側にはまだ個別仕様がない。

旧仕様を暗黙利用せず、後続再構成で必要性、責務およびExecution Contextとの境界を再確認する。

### 5.2 復旧Restriction Set

Core復旧仕様では任意の「復旧Restriction Set」を利用できる。

新Restriction Set仕様では通常運転中にState、Workflow、SubFlowから参照する登録モデルを定義しているため、Core復旧固有Restriction Setについて次のどちらとするかをRestriction層確定時に明示する必要がある。

- 通常Restriction Set登録簿を利用する。
- Core復旧専用の制限として別経路で定義する。

どちらかを現時点で推測確定しない。

## 6. 判定

Core仕様群の起動、実行状態管理、Fail-closed、正本競合、Capability/Restriction境界について、現時点で重大な循環依存または責務逆転は確認していない。

CR-13およびCR-14は後続仕様への未解決参照であり、Core基本モデルそのものを不成立とする問題とは判定しない。

後続層の再構成でCore境界に変更が生じた場合は、本確認を再実施する。
