<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261001-082000Z-CAPV
lang: ja-JP
canonical_title: Capability外的要因セルフ検証仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Capability > Capability外的要因セルフ検証仕様

# Capability(能力)外的要因セルフ検証仕様

## 1. 目的

本書は、外部サービス、Connector、Tool、通信、認証、quotaその他のHLDocS外部要因によってCapability(能力)の利用可能性が変動する場合に、HLDocS自身のCapability仕様体系が成立するかを自己検証する方法を定義する。

本書はHLDocS自身を検証するspecであり、HLDocSが生成した成果物の検証トレーサビリティを定義するdocument_type:testspecではない。

外的要因はHLDocSだけでは制御できないため、正常時だけの検証でCapability機構が成立したと判断してはならない（MUST NOT）。

## 2. 検証独立性

本検証は、過去のチャット、LLM_WORKSPACEその他の一時情報が存在しない新しいLLMセッションから再実行できなければならない（MUST）。

検証開始時は、現在採用するCapability、Capability Context、Capability Providerおよび関連Core仕様を現在の正本から取得しなければならない（MUST）。

過去の検証結果は比較資料として利用してよいが、現在のPASS判定の根拠としてそのまま再利用してはならない（MUST NOT）。

検証に必要な前提、外的状態、期待結果または判定規則を現在の正本から確定できない場合、過去チャットまたはLLM_WORKSPACEから推測して補ってはならない（MUST NOT）。その項目は検証不能または仕様不足として記録する。

LLM_WORKSPACEに保存されたCapability Entry、Provider状態、Execution Attemptその他の情報は、現在も有効であることを現在の正本および実行環境から確認できない限り、現在の検証入力または確定結果として扱ってはならない（MUST NOT）。

既知シナリオの確認だけで検証を終了してはならない（MUST NOT）。検証時に、既存分類で安全に扱えない外的要因、Provider切替経路、古いevidenceの再利用経路、無限再試行またはFail-openとなる経路がないかも探索する。

## 3. 検証の種類

検証は次を区別する。

### 3.1 Observed Validation(実環境観測検証)

現在の実行環境で実際に観測できるProvider状態およびExecution Attempt(実行試行)を使用する。

実際に発生していないrate limit、quota制限、サービス障害等を発生済みとして記録してはならない（MUST NOT）。

### 3.2 Scenario Validation(シナリオ検証)

外的状態を検証入力として明示的に模擬し、HLDocSの判定・切替・停止動作を確認する。

Scenario Validationの結果を、外部サービスそのものの挙動を実証した結果として扱ってはならない（MUST NOT）。

## 4. 必須シナリオ

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

## 5. 検証記録

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

## 6. 成立条件

外的要因対応は、少なくとも次を確認できた場合に仕様上の基本成立候補とする。

- 単一Provider失敗とCapability全体失敗を分離できる。
- 代替Providerを独立評価できる。
- 一時的制限と恒常的利用不能を、確認できる根拠がある場合に区別できる。
- 原因不明をUNKNOWNとして保持できる。
- 古いAVAILABLEを無条件に再利用しない。
- 同一条件で進展のない自動再試行を無制限に行わない。

Scenario Validationだけで外部サービス固有の挙動まで検証済みとしてはならない（MUST NOT）。

## 7. 継続検証

実運用中に外的要因による新しい失敗形態を観測した場合は、観測事実を既存分類と照合する。

既存分類で安全に扱えない場合は、推測で既存分類へ押し込まず、UNKNOWNとして扱った上で仕様および検証シナリオの追加要否を検討する。

---

[目次](../../目次.md) > 仕様 > Capability > Capability外的要因セルフ検証仕様
