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

## 2.1. 検証対象の段階分離（C案）

<!-- hldocs:sec_id=sec_9c4b28f17a6d4e03b2f85d0c6139ae74 -->

検証対象はPhase A（ChatGPT上で動作するHLDocS Core）とPhase B（独立Coreプログラム）に分離し、**Phase Aの完了判定後にPhase Bへ進む**。両Phaseの結果・証跡・判定は独立に管理し、Phase AのPASSをPhase BのPASSに継承してはならない（MUST NOT）。

| 項目 | Phase A | Phase B |
| --- | --- | --- |
| 対象 | ChatGPT上でのHLDocS Coreの動作 | 独立して起動するCoreプログラム |
| 境界入力 | 検証用の会話・操作・利用可能なツール入力 | 独立ハーネスによる入力 |
| 観測 | 会話履歴、実際のツール応答、外部で取得可能な証跡 | 独立Observerによる状態・副作用の観測 |
| 判定範囲 | 観測できたChatGPT上の振る舞いに限定 | §2のEXECUTED契約に従う |
| 実行入口・隔離 | 利用可能なChatGPT環境で個別に検証 | §3〜§7の実装着手ゲートに従う |

Phase Aは§2のEXECUTEDを自動的に満たすものではない。内部状態、実際の制限適用、Tool呼出しや副作用の不存在を独立に確認できないケースは、自己申告のみでPASSとしてはならない（MUST NOT）。未実施はUNEXECUTED、実行不能はBLOCKED、観測・判定根拠が不十分な場合はUNDEFINEDとして記録する。

Phase Aの対象ケースはWS-01〜04、FC-01〜10とし、各ケースについて次を検証前に記録する（MUST）。

1. 検証入力と開始時条件。
2. 実際に取得できる証跡と、その取得元。
3. 自己申告と外部観測の区別。
4. 観測できない内部状態・副作用。
5. 実施可否、判定根拠、終了後の状態。

Phase Aの**完了**は全ケースPASSと同義ではない。全14ケースについて実施結果または実施不能理由を記録し、残るUNDEFINED/BLOCKED/UNEXECUTEDを明示して、Phase Aの検証範囲・限界・未解決Issueを確定した時点で完了判定を行う。Core正常性PASSの判定とは分離する。完了判定の具体的な承認方法とPhase B移行ゲートは、実施計画の確定時に別途定める。

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
