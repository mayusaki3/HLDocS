<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-INT1
lang: ja-JP
canonical_title: Interaction仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Interaction > Interaction仕様

# Interaction仕様

## 1. 目的

本書は、HLDocSと利用者との入出力境界であるInteractionを定義する。

Interactionは利用者との入出力を担当するが、State、Work、Workflow PlanまたはIssue Policyを独断で変更する制御主体ではない。

## 2. 責務

InteractionはUser Inputの受付、Input Routing、Information/Progressの提示、Decision Requestの提示・管理、Decision Responseの受付と要求元への返却を担当する。

## 3. Interaction Context

Interaction ContextはModeとActive Decision Requestを表現できなければならない（MUST）。

ModeはNORMALまたはDECISION_REQUIREDとする。  
Active Decision Requestは同時に最大1件とする（MUST）。

## 4. Input Routing

入力は少なくとも次の観点で扱う。

- DECISION_RESPONSE
- WORKFLOW_INPUT
- WORK_CONTROL
- NEW_WORK_REQUEST
- INFORMATION_REQUEST
- UNKNOWN

## 5. ルーティング優先順位

1. Active Decision Requestへの回答か。
2. Execution Contextを変更しないInformation Requestか。
3. Active Workflowへの入力または制御か。
4. Current Workへの制御か。
5. New Work Requestか。
6. いずれにも一意に分類できない場合はUNKNOWN。

複数分類によって異なるExecution Context変更が発生し得る場合、一つを推測して実行してはならない（MUST NOT）。

## 6. Decision Request

利用者判断が必要な処理主体はInteractionへDecision Requestを発行する。

Decision RequestはRequest ID、Request Source、PromptまたはReason、および必要に応じOptionsを保持する。

利用者のDecision Responseは要求元へ返す。  
必要なContext変更は所定の仕様に従ってCoreへ変更要求として送らなければならない（MUST）。

## 7. Decision待ち

DECISION_REQUIREDはStateではない。  
Decision Requestだけを理由として待機Stateへ遷移してはならない（MUST NOT）。

Decision Requestに依存する処理は回答まで進めてはならない（MUST NOT）。  
参照情報の提示はDecision Requestを破壊しない範囲で行ってよい（MAY）。

## 8. 「進めて」「続けて」

- Active Decision Requestへの回答として一意ならDECISION_RESPONSEとしてよい。
- Active Workflowが存在する場合は当該Workflowへの継続指示として扱う。
- ACTIVE Workが存在しActive Workflowがない場合は、Current Workflow Planの次のPENDING Workflowが開始可能かをWorkflow仕様に従って確認する。
- Current WorkもSYSTEM Planも存在しない場合、新規Work要求として推測してはならない（MUST NOT）。

必要な選択内容が提示されていないDecision Requestに対し、単なる「進めて」を特定Optionとして推測してはならない（MUST NOT）。

## 9. Information Request

Execution Contextを変更しない問い合わせはInformation Requestとして処理してよい（MAY）。

Information Requestへの応答だけを理由としてExecution Contextを変更してはならない（MUST NOT）。

## 10. New Work Request

Current Workが存在しない場合、利用者入力が新規作業要求として明確であればWork生成要求へ配送してよい（MAY）。

ACTIVE Workが存在する状態で別Work候補を検出した場合、新しいWorkへ暗黙に切り替えてはならない（MUST NOT）。

## 11. Interactionが行ってはならないこと

InteractionはStateの選択・変更、Workflow生成、Workflow Plan直接変更、Issue Policyの独断決定、Workflow/SubFlow内部処理、意味判断だけによるTool直接実行、Execution Context直接変更を行ってはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Interaction > Interaction仕様
