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

Interactionは次を担当する。

- User Inputの受付
- Input Routing
- Informationの提示
- Progressの提示
- Decision Requestの提示および管理
- Decision Responseの受付と要求元への返却

## 3. Interaction Context

Interaction Contextは少なくとも次を表現できなければならない（MUST）。

- Mode
- Active Decision Request

Modeは当面次とする。

- NORMAL
- DECISION_REQUIRED

Active Decision Requestは同時に最大1件とする（MUST）。

複数の判断事項が存在する場合、相互に同一判断として扱える根拠がない限り、一つのDecision Requestへ無理に統合してはならない（MUST NOT）。

## 4. Input Routing

InteractionはUser Inputを、現在のExecution ContextおよびInteraction Contextを参照して適切な処理先へ配送する。

入力は少なくとも次の観点で扱う。

- DECISION_RESPONSE
- WORKFLOW_INPUT
- WORK_CONTROL
- NEW_WORK_REQUEST
- INFORMATION_REQUEST
- UNKNOWN

この分類は、利用者入力の意味上の処理をInteractionだけで完結させることを意味しない。

## 5. ルーティング優先順位

User Inputを受けた場合は、次の順序で解釈可能性を確認する。

1. Active Decision Requestへの回答か。
2. Execution Contextを変更しないInformation Requestか。
3. Active Workflowへの入力または制御か。
4. Current Workへの制御か。
5. New Work Requestか。
6. いずれにも一意に分類できない場合はUNKNOWN。

複数の分類によって異なるExecution Context変更が発生し得る場合、一つを推測して実行してはならない（MUST NOT）。

## 6. Decision Request

利用者判断が必要な処理主体は、InteractionへDecision Requestを発行する。

Decision Requestは少なくとも次を保持する。

- Request ID
- Request Source
- PromptまたはReason
- 必要に応じたOptions

InteractionはDecision Requestの内容から処理方針を独自に変更してはならない（MUST NOT）。

利用者のDecision Responseは要求元へ返し、必要なContext変更は要求元または所定の管理機構からCoreへ変更要求として送らなければならない（MUST）。

## 7. Decision待ち

DECISION_REQUIREDはStateではない。  
Decision Requestが存在することだけを理由として待機Stateへ遷移してはならない（MUST NOT）。

Decision Requestに依存する処理は、Decision Responseを得るまで進めてはならない（MUST NOT）。

ただし、現在状態、進捗、Issueその他の参照情報の提示は、Decision Requestを破壊しない範囲で行ってよい（MAY）。

## 8. 「進めて」「続けて」

「進めて」「続けて」その他これらに準ずる入力は、現在Contextに従って解釈する。

- Active Decision Requestが存在し、その回答として一意に解釈できる場合はDECISION_RESPONSEとしてよい。
- Active Workflowが存在する場合は、そのWorkflowに対する継続指示として扱う。
- ACTIVE Workが存在し、Active Workflowが存在しない場合は、承認済みWorkflow Planの継続可否をWorkflow管理へ問い合わせる。
- Current Workが存在しない場合、新規Work要求として推測してはならない（MUST NOT）。

必要な選択内容が提示されていないDecision Requestに対し、単なる「進めて」を特定Optionの選択として推測してはならない（MUST NOT）。

## 9. Information Request

Execution Contextを変更しない問い合わせはInformation Requestとして処理してよい（MAY）。

Information Requestへの応答だけを理由として、Workflow Plan、Current State、Work StatusまたはIssue Policyを変更してはならない（MUST NOT）。

## 10. New Work Request

Current Workが存在しない場合、利用者入力が新規作業要求として明確であればWork生成要求へ配送してよい（MAY）。

ACTIVE Workが存在する状態で別Work候補を検出した場合、新しいWorkへ暗黙に切り替えてはならない（MUST NOT）。  
必要な場合はDecision RequestによってWork切替の利用者判断を取得する。

## 11. Interactionが行ってはならないこと

Interactionは次を行ってはならない（MUST NOT）。

- Stateを選択または変更する。
- Workflowを生成する。
- Workflow Planを直接変更する。
- Issue Policyを独断で決定する。
- WorkflowまたはSubFlowの内部処理を実行する。
- Toolを作業上の意味判断だけで直接実行する。
- Execution Contextを直接変更する。

---

[目次](../../目次.md) > 仕様 > Interaction > Interaction仕様
