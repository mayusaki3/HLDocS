<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261020-000002Z-CV03
lang: ja-JP
canonical_title: Core検証SUT実行・観測インターフェース仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core検証SUT実行・観測インターフェース仕様

# Core検証SUT実行・観測インターフェース仕様

## 1. 目的

Core機能正常性確認接続・隔離仕様に基づき、SUT（検証対象Core）の実行方式、検証入力、独立観測、証跡、後始末を定義する。本書は検証ハーネスの**契約仕様**であり、HLDocS Coreの実行可能な実装が存在することを意味しない。

## 2. 実行方式と採用順

検証方式を次の三つに分離する（MUST）。

| mode | 対象 | PASSの意味 |
| --- | --- | --- |
| STATIC | 正本仕様 | 規則・依存・期待結果の静的整合 |
| SIMULATED | 明示した状態モデル・入力 | モデルに対する期待結果の一致。実Core正常性ではない |
| EXECUTED | 独立SUT上の実Core実装 | 実入力に対する外部観測結果の一致 |

実Core実装の実行入口、初期化方法、状態観測手段が確認できない場合、EXECUTEDを実施済みとしてはならない（MUST NOT）。その場合はSTATIC/SIMULATEDを独立して進め、EXECUTEDを未実施またはBLOCKEDとして記録する。

初期採用方式は**外部ハーネスが独立したSUTインスタンスを起動し、境界入力を与え、Observerが観測する方式**とする。実行言語、OS、プロセス形態、CLI/APIは実Core実装が特定できるまで固定しない。隔離されたプロセス、コンテナ、別セッションなどは候補だが、名前だけで隔離成立とみなしてはならない（MUST NOT）。

## 3. インターフェース契約

ハーネスは少なくとも次の論理操作を提供する（MUST）。実際のCLI/API名は実装時に決める。

| 操作 | 入力 | 出力 |
| --- | --- | --- |
| prepare | target_sha、仕様版、依存、隔離設定 | run_id、検証可能性、準備失敗理由 |
| reset | run_id、case_id、初期状態定義 | 初期化証跡、状態識別子 |
| inject | run_id、case_id、定義済み境界入力・障害条件 | 入力受理/拒否、操作識別子 |
| observe | run_id、case_id、操作識別子 | 状態遷移、拒否、ログ、副作用の外部観測 |
| terminate | run_id、終了理由 | 停止証跡、残存副作用 |
| report | case_id、期待結果、観測、検証方式 | 判定、証跡参照、未実施理由 |

SUT内部のCurrent StateやWorkflow Planを直接書き換える操作をinjectの一般機能として公開してはならない（MUST NOT）。不整合・欠落の異常系は隔離された起動入力、依存スタブ、復元候補、失効したProvider証跡等の境界入力から再現する。

## 4. ケース入力と証跡スキーマ

ケース入力の論理構造を次とする。

```yaml
case_id: FC-01
target_sha: "<fixed-commit-sha>"
mode: EXECUTED
initial_state: "<documented-fixture>"
preconditions: []
stimulus:
  operation: "<boundary-operation>"
  fault: "<optional-injected-fault>"
expected:
  decision: "<allow|deny|recover|suspend|other>"
  state_constraints: []
  side_effect_constraints: []
```

結果の論理構造を次とする。

```yaml
run_id: "<unique-run-id>"
case_id: FC-01
target_sha: "<fixed-commit-sha>"
mode: EXECUTED
observed:
  decision: "<observed-decision>"
  state_before: "<observed-state-reference>"
  state_after: "<observed-state-reference>"
  events: []
  side_effects: []
evidence: []
verdict: "<PASS|FAIL|UNDEFINED|BLOCKED|UNEXECUTED>"
reason: "<required-when-not-PASS>"
```

上記のプレースホルダーは例示であり実測結果ではない。証跡はrun_id、case_id、対象SHA、入力、観測時点、取得元に結び付ける（MUST）。SUTの自己申告とObserverの外部観測を別フィールドまたは識別可能な証跡として区別する（MUST）。

## 5. 初期化・副作用・失敗時処理

各ケースは既知の隔離初期状態から開始する（MUST）。ケース間のExecution Context、Plan、Work、Capability evidence、保存済み結果を暗黙に引き継いではならない（MUST NOT）。

外部接続、ファイル書込、Provider呼出しは検証用の許可先へ制限する（MUST）。終了時はSUT停止と残存副作用の検査を行う（MUST）。Observerが停止または副作用の有無を確認できない場合、当該実行ケースをPASSとしてはならない（MUST NOT）。

隔離の破綻、想定外の実資産への副作用、SUT停止不能、証跡取得不能を検出した場合は実行を中止し、影響範囲を記録する（MUST）。

## 6. ケース定義と判定

Coreセルフ検証仕様§4.6の4ケースと§4.7の10ケースを、少なくとも以下の識別子で管理する（MUST）。ケース別の入力・期待結果は別紙「Core正常性確認ケース定義」に定める。

検証項目の判定はPASS/FAIL/UNDEFINED/BLOCKEDを使用する。未実施は判定を付けず、記録上UNEXECUTEDと明示する。UNEXECUTEDをBLOCKEDやPASSへ読み替えてはならない（MUST NOT）。

Core全体PASSには必要な検証方式の実観測が揃わなければならない（MUST）。STATIC/SIMULATEDのPASSはEXECUTEDのPASSを代替しない。

## 7. 独立Workflow接続ゲート

本インターフェース契約だけでは専用Core正常性確認WorkflowをState/Planに登録しない。SUT実装の特定、ハーネス実装、隔離・観測の実証、実行時Restriction、開始・終了条件、必要な承認、State/Plan整合の検証後に登録可否を判定する。

---

[目次](../../目次.md) > 仕様 > Workflow > Core検証SUT実行・観測インターフェース仕様
