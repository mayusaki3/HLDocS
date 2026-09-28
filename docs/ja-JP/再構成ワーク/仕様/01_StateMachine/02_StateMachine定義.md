<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-SM02
lang: ja-JP
canonical_title: State Machine定義
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義

# State Machine(状態遷移機構)定義

## 1. 目的

本書はHLDocS v0.7.0再構成時点のState登録および遷移関係を定義する。

## 2. State一覧

| State | 個別仕様 | 用途 |
| --- | --- | --- |
| 能力確認 | ../02_State/能力確認State.md | 現在利用可能な能力を検証し通知する |
| 待機 | ../02_State/待機State.md | 実行すべきWork/Workflowがない通常運転 |
| 情報参照 | ../02_State/情報参照State.md | 正本を変更せず情報を参照、確認、説明または分析する |

## 3. Initial State

Initial Stateは「能力確認」とする。

## 4. 遷移一覧

| 遷移元 | 遷移先 | 条件 |
| --- | --- | --- |
| 能力確認 | 待機 | 能力確認のSYSTEM Workflow Planが完了 |
| 待機 | 情報参照 | 情報参照がUNIQUE候補で、Work Candidateがwork_acceptanceに適合し、CoreがWork生成とState進入を適用可能 |
| 情報参照 | 待機 | 対象WorkがCOMPLETEDで、情報参照のWorkflow Planが終了 |

## 5. 起動時正常系

Core → 能力確認 → SYSTEM Plan → 能力通知 → 待機 とする。

## 6. 新規Work正常系

1. InteractionがNEW_WORK_REQUESTを識別する。
2. Work Candidate(作業候補)を構成する。
3. State選択ルールを適用する。
4. UNIQUEの場合、State Machineが遷移可否を判定する。
5. CoreがWork生成、State遷移、State進入準備を検証する。
6. 整合した一つの変更としてWorkをACTIVE化し対象Stateへ進入する。
7. Owner=WORKのPlanを生成してWorkflowを実行する。
8. Work完了後、定義された遷移で待機へ戻る。

## 7. State選択異常系

### 7.1 NONE

例: 現在未定義の「仕様を修正して」。

処理可能なStateが存在しない場合、Workを生成しない。  
Interactionから現在処理できない旨を通知して待機を維持する。

### 7.2 UNKNOWN

例: 「これを確認して」のように、対象または目的が不足して情報参照適合性を判断できない場合。

Workを生成せずDecision Requestまたは追加情報要求を行う。  
回答後、同じWork Candidateを再評価する。

### 7.3 MULTIPLE

複数のwork_acceptanceへ同時に適合し一意に選択できない場合、Workを生成せず候補選択のDecision Requestを行う。

利用者選択後もState MachineおよびCoreの検証を行う。

現時点ではWork処理Stateが情報参照のみであるため、実構成上MULTIPLEは発生しない。  
MULTIPLEを検証するためだけに重複Stateを追加してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > State Machine > State Machine定義
