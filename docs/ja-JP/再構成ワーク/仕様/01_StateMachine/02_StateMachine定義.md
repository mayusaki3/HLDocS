<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-SM02
lang: ja-JP
canonical_title: State Machine定義
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義

# State Machine定義

## 1. 目的

本書は、HLDocS v0.7.0再構成時点のState登録および遷移関係を定義する。

本書は再構成と検証の進行に合わせてStateを追加する。  
未定義のStateを存在するものとして扱ってはならない（MUST NOT）。

## 2. State一覧

| State | 個別仕様 | 用途 |
| --- | --- | --- |
| 待機 | ../02_State/待機State.md | 通常運転中で、現在実行すべきWorkまたはWorkflowが存在しない状態 |

## 3. Initial State

Initial Stateは「待機」とする。

「開始」はStateとして定義しない。  
HLDocSシステム起動およびState Machineへの制御移譲はCoreの起動処理として扱う。

## 4. 遷移一覧

現時点では待機State以外の通常運転Stateを再構成していないため、State間遷移は定義しない。

Stateを追加する場合は、個別State仕様を成立させた後、本書へ登録し、必要な遷移を明示しなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義
