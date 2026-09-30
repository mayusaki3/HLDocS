<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261001-082000Z-CAPV
lang: ja-JP
canonical_title: Capability外的要因検証仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Capability > Capability外的要因検証仕様

# Capability(能力)外的要因検証仕様

## 1. 目的

本書は、外部サービス、Connector、Tool、通信、認証、quotaその他のHLDocS外部要因によってCapability(能力)の利用可能性が変動する場合の検証方法を定義する。

外的要因はHLDocSだけでは制御できないため、正常時だけの検証でCapability機構が成立したと判断してはならない（MUST NOT）。

## 2. 検証の種類

検証は次を区別する。

### 2.1 Observed Validation(実環境観測検証)

現在の実行環境で実際に観測できるProvider状態およびExecution Attempt(実行試行)を使用する。

実際に発生していないrate limit、quota制限、サービス障害等を発生済みとして記録してはならない（MUST NOT）。

### 2.2 Scenario Validation(シナリオ検証)

外的状態を検証入力として明示的に模擬し、HLDocSの判定・切替・停止動作を確認する。

Scenario Validationの結果を、外部サービスそのものの挙動を実証した結果として扱ってはならない（MUST NOT）。

## 3. 必須シナリオ

少なくとも次を検証対象とする。

1. Primary Provider成功
   - 優先Providerが利用可能でCapabilityがAVAILABLEとなる。

2. Provider選択不適合
   - 最初のProviderが要求操作を満たさない。
   - 代替Providerが利用可能ならCapability全体をUNAVAILABLEにしない。

3. 一時的エラー
   - ProviderがTRANSIENT_ERRORとなる。
   - 一回の失敗を恒常的UNAVAILABLEへ昇格しない。
   - 進展のない無限再試行を行わない。

4. 一時的利用制限
   - ProviderがTEMPORARILY_LIMITEDとなる。
   - retry_afterが明示される場合、それ以前に同一条件で反復しない。
   - retry_afterが不明なら復旧時刻を推測しない。
   - 代替Providerがあれば独立に評価する。

5. 恒常的利用不能
   - PERMANENT_UNAVAILABLEと確認できるProviderを同条件で自動反復しない。
   - 他ProviderがあればCapability全体はその結果から評価する。

6. 原因不明
   - 原因を安全に分類できない場合はUNKNOWNとして扱う。
   - 推測で一時障害または恒常障害へ分類しない。

7. 既存AVAILABLEの失効
   - Capability Context(能力コンテキスト)がAVAILABLEの後にProvider状態変化を観測する。
   - 古いAVAILABLEだけを根拠に実行しない。

## 4. 検証記録

検証結果では少なくとも次を区別して記録する。

- validation_type: OBSERVED | SCENARIO
- Capability
- Provider
- 初期Capability Entry
- 入力または観測した外的状態
- Execution Attempt結果
- Provider切替の有無
- 更新後Capability Entry
- 自動再試行の判断
- 利用者判断が必要となったか

## 5. 成立条件

外的要因対応は、少なくとも次を確認できた場合に仕様上の基本成立候補とする。

- 単一Provider失敗とCapability全体失敗を分離できる。
- 代替Providerを独立評価できる。
- 一時的制限と恒常的利用不能を、確認できる根拠がある場合に区別できる。
- 原因不明をUNKNOWNとして保持できる。
- 古いAVAILABLEを無条件に再利用しない。
- 同一条件で進展のない自動再試行を無制限に行わない。

Scenario Validationだけで外部サービス固有の挙動まで検証済みとしてはならない（MUST NOT）。

## 6. 継続検証

実運用中に外的要因による新しい失敗形態を観測した場合は、観測事実を既存分類と照合する。

既存分類で安全に扱えない場合は、推測で既存分類へ押し込まず、UNKNOWNとして扱った上で仕様および検証シナリオの追加要否を検討する。

---

[目次](../../目次.md) > 仕様 > Capability > Capability外的要因検証仕様
