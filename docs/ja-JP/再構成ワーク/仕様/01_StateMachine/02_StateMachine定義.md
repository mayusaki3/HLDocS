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
| 能力確認 | ../02_State/能力確認State.md | 現在のHLDocSで利用可能な能力を検証し利用者へ通知する |
| 待機 | ../02_State/待機State.md | 通常運転中で、現在実行すべきWorkまたはWorkflowが存在しない状態 |

## 3. Initial State

Initial Stateは「能力確認」とする。

「開始」はStateとして定義しない。  
HLDocSシステム起動およびState Machineへの制御移譲はCoreの起動処理として扱う。

## 4. 遷移一覧

| 遷移元 | 遷移先 | 条件 |
| --- | --- | --- |
| 能力確認 | 待機 | 能力確認StateのWorkflow Planが完了していること |

Stateを追加する場合は、個別State仕様を成立させた後、本書へ登録し、必要な遷移を明示しなければならない（MUST）。

## 5. 起動時正常系

新規起動時は次の順序で通常運転を開始する。

1. CoreからState Machineへ制御を移譲する。
2. Initial Stateである能力確認Stateへ進入する。
3. 能力確認Stateのdefault_workflow_planを実行する。
4. HLDocS能力確認Workflowによる検証結果をInteractionから通知する。
5. Workflow Plan完了後、待機Stateへの遷移可否を判定する。
6. 遷移可能な場合、Coreへ待機Stateへの変更を要求する。
7. Coreが待機Stateを適用する。

---

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義
