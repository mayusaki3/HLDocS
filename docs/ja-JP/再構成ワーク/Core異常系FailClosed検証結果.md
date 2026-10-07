# Core(中核)異常系・Fail-closed検証結果

検証日: 2026-10-03  
対象: develop

## 1. 目的

Core(中核)が異常または不確定な実行状態を検出した場合に、推測による補完、制限回避、Plan上書きその他の暗黙修復で通常処理を強行せず、Fail-closedとして安全側に停止できることを仕様横断で検証する。

本検証はScenario Validation(シナリオ検証)であり、実運用障害そのものを発生させた検証ではない。

## 2. 結果概要

結果: **10/10 PASS**

| ID | 異常シナリオ | 期待するFail-closed動作 | 結果 |
| --- | --- | --- | --- |
| FC-01 | 必要Restriction Setを取得不能 | 制限なしで続行せず対象処理を停止 | PASS |
| FC-02 | Execution Context不整合 | 推測補完せず変更・実行を停止 | PASS |
| FC-03 | State遷移がState Machineで未許可 | Core独自判断で遷移しない | PASS |
| FC-04 | 旧Stateの未完了Planが残存 | 破棄・上書きせず新Planを生成しない | PASS |
| FC-05 | WORK Plan構成変更に承認なし | 変更を確定しない | PASS |
| FC-06 | SYSTEM Plan構成変更に仕様根拠なし | 利用者承認でも代替せず変更しない | PASS |
| FC-07 | Capability AVAILABLEだがRestriction不成立 | Providerに対応するToolを実行しない | PASS |
| FC-08 | Capability evidence失効・再確認不能 | 古いAVAILABLEで実行せずUNKNOWN/再確認 | PASS |
| FC-09 | Re-run Sequenceの次要素を開始不能 | 残りを強制実行せず停止理由を引き渡す | PASS |
| FC-10 | State Machineへの起動時移譲失敗 | 通常運転を開始せずCore復旧へ入る | PASS |

## 3. シナリオ確認

### FC-01 Restriction取得不能

```text
必要Restriction Set
 ↓ 取得/検証/適用不能
対象処理 STOP
```

不足制限を「制限なし」と解釈しない。

### FC-02 Execution Context不整合

```text
Execution Context不整合
 ↓
推測補完しない
 ↓
変更要求を適用しない
```

Coreだけが確定状態を変更できることと、Core自身も根拠なしに補完できないことが両立する。

### FC-03 未許可State遷移

```text
State Transition Request
 ↓
State Machineで遷移根拠なし
 ↓
Current State維持
```

CoreはState Machineの代替判断機構にならない。

### FC-04 未完了Plan残存

```text
State進入要求
 ↓
旧Plan未完了 / ACTIVE / SUSPENDED / 解除不能
 ↓
旧Planを維持
 ↓
新default Plan生成禁止
 ↓
State進入を確定しない
```

「再利用不能」と「削除可能」を分離できる。

### FC-05 WORK Plan無承認変更

```text
Owner=WORK
 ↓
追加/削除/並べ替え/SKIPPED要求
 ↓ 承認なし
変更拒否
```

Issue発見やWorkflow判断だけを承認として扱わない。

### FC-06 SYSTEM Plan未定義変更

```text
Owner=SYSTEM
 ↓
Plan構成変更要求
 ↓
system_plan_changes等の仕様根拠なし
 ↓
変更拒否
```

利用者承認だけで内部SYSTEM Planを任意変更できない。

### FC-07 CapabilityとRestrictionの分離

```text
Capability = AVAILABLE
 ↓
Restriction Context = 不許可
 ↓
Providerに対応するTool実行禁止
```

能力存在を実行許可として扱わない。

### FC-08 Capability evidence失効

```text
Capability Entry = AVAILABLE
 ↓
Provider状態変化 / evidence再確認不能
 ↓
Entry失効
 ↓
再確認またはUNKNOWN
```

過去のAVAILABLEを恒久的な実行根拠にしない。

### FC-09 Re-run Sequence開始不能

```text
Re-run Sequence
 ↓
次Workflowの開始条件不成立
 ↓
残りを強制実行しない
 ↓
原因を要求元/Interactionへ引き渡す
```

再実行機構自身が制約を迂回しない。

### FC-10 State Machine移譲失敗

```text
Core起動
 ↓
State Machine移譲失敗
 ↓
通常運転禁止
 ↓
Core復旧
```

復旧中もCore基本制限を維持し、必要な追加制限が取得不能なら参照・状況提示・判断要求以外の変更を行わない。

## 4. 検証中に発見した仕様不整合

Core基本制限仕様のWorkflow Plan保護が、Plan Ownerを区別せず「利用者承認」を要求しており、SYSTEM Plan変更規則と競合していた。

次のように修正した。

```text
WORK Plan
  → 利用者の明示指示/承認

SYSTEM Plan
  → State/SYSTEM処理仕様に明示された変更規則
     + 現在その条件が成立する根拠
```

SYSTEM Planでは利用者承認だけを仕様上の変更規則の代替にしない。

## 5. 判定

現在のCore、Core基本制限、State、Workflow、Capability ContextおよびCore復旧仕様の組み合わせでは、主要な異常系についてFail-closed境界を構成できる。

本検証で確認したのは仕様上の状態遷移と禁止条件であり、実装コードによる障害注入試験ではない。

今後Core実装を作成する場合、本シナリオ群を実装テストへ変換する必要がある。
