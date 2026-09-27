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

## 2. 責務

InteractionはUser Inputの受付、Input Routing、Information/Progressの提示、Decision Request/Responseを担当する。  
InteractionはExecution Contextを直接変更しない。

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

INFORMATION_REQUESTは、現在のExecution Contextを変更せずその場で回答可能な問い合わせをいう。

問い合わせ形式であっても、回答のためにState遷移、Workflow実行、外部参照その他の作業実行が必要な場合は、INFORMATION_REQUESTではなくNEW_WORK_REQUEST候補として扱う（MUST）。

## 5. ルーティング優先順位

1. Active Decision Requestへの回答か。
2. Execution Contextを変更せずその場で回答可能なInformation Requestか。
3. Active Workflowへの入力または制御か。
4. Current Workへの制御か。
5. New Work Requestか。
6. いずれにも一意に分類できない場合はUNKNOWN。

複数分類によって異なるExecution Context変更が発生し得る場合、一つを推測して実行してはならない（MUST NOT）。

## 6. Decision Request

利用者判断が必要な処理主体はInteractionへDecision Requestを発行する。

Decision Responseは要求元へ返し、必要なContext変更は所定の仕様に従ってCoreへ変更要求として送る。

## 7. Decision待ち

DECISION_REQUIREDはStateではない。  
Decision Requestだけを理由として待機Stateへ遷移してはならない（MUST NOT）。

## 8. 「進めて」「続けて」

- Active Decision Requestへの回答として一意ならDECISION_RESPONSEとしてよい。
- Active Workflowが存在する場合は当該Workflowへの継続指示として扱う。
- ACTIVE Workが存在しActive Workflowがない場合はCurrent Workflow Planの次のPENDING Workflowが開始可能かを確認する。
- Current WorkもSYSTEM Planも存在しない場合、新規Work要求として推測してはならない（MUST NOT）。

## 9. Information Request

INFORMATION_REQUESTへの応答だけを理由としてExecution Contextを変更してはならない（MUST NOT）。

処理中に作業実行が必要と判明した場合は、そのままExecution Contextを変更せずNEW_WORK_REQUEST候補として再分類する。

## 10. New Work Request

Current Workが存在しない場合、利用者入力が新規作業要求として明確であれば、InteractionはWork生成要求をCoreへ送ってよい（MAY）。

Work生成要求には、利用者入力およびそこから確定できるPurposeを含める。

ACTIVE Workが存在する状態で別Work候補を検出した場合、新しいWorkへ暗黙に切り替えてはならない（MUST NOT）。

## 11. 禁止事項

InteractionはStateの選択・変更、Workflow生成、Workflow Plan直接変更、Issue Policyの独断決定、Workflow/SubFlow内部処理、意味判断だけによるTool直接実行、Execution Context直接変更を行ってはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Interaction > Interaction仕様
