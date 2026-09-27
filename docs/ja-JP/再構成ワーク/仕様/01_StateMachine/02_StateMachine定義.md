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
未定義のStateを存在するものとして扱ってはならない（MUST NOT）。

## 2. State一覧

| State | 個別仕様 | 用途 |
| --- | --- | --- |
| 能力確認 | ../02_State/能力確認State.md | 現在のHLDocSで利用可能な能力を検証し利用者へ通知する |
| 待機 | ../02_State/待機State.md | 現在実行すべきWorkまたはWorkflowが存在しない通常運転 |
| 情報参照 | ../02_State/情報参照State.md | 正本を変更せず情報を参照、確認、説明または分析する |

## 3. Initial State

Initial Stateは「能力確認」とする。

「開始」はStateとして定義しない。  
HLDocSシステム起動およびState Machineへの制御移譲はCoreの起動処理として扱う。

## 4. 遷移一覧

| 遷移元 | 遷移先 | 条件 |
| --- | --- | --- |
| 能力確認 | 待機 | 能力確認StateのSYSTEM Workflow Planが完了していること |
| 待機 | 情報参照 | ACTIVE Workが存在し、State選択ルールにより情報参照が候補となり、当該Workが情報参照Stateのwork_acceptanceに適合すること |
| 情報参照 | 待機 | 対象WorkがCOMPLETEDであり、情報参照StateのWorkflow Planが終了していること |

## 5. 起動時正常系

1. CoreからState Machineへ制御を移譲する。
2. Initial Stateである能力確認Stateへ進入する。
3. Owner=SYSTEMのdefault Workflow Planを生成する。
4. HLDocS能力確認Workflowによる検証結果をInteractionから通知する。
5. Plan完了後、待機Stateへ遷移する。

## 6. 情報参照Work正常系

1. 待機StateでInteractionが情報参照要求をNEW_WORK_REQUESTとして分類する。
2. Workを生成する。
3. State選択ルールが登録Stateから候補を抽出する。
4. 情報参照StateがUNIQUE候補となる場合、State Machineが待機→情報参照の遷移可否を判定する。
5. Coreが遷移を適用する。
6. Owner=WORKのdefault Workflow Planを生成する。
7. 情報参照Workflowを実行する。
8. 回答提示後、WorkflowおよびWorkを完了する。
9. State Machineの判定を経て待機Stateへ戻る。

---

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義
