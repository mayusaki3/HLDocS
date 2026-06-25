<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260625-000000Z-A3D7
lang: ja-JP
canonical_title: 開始Workflow
document_type: spec
canonical_document: true
-->

[目次](../../../../目次.md) > 仕様 > 状態 > 開始 > 開始Workflow

# 開始Workflow

## 1. 目的

本Workflowは、新しい作業開始時または作業再開時に、現在の作業状況を確認し、次に実行すべきWorkflowを決定する。

本仕様は、共通仕様成立状態でのみ利用できる。
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

---

## 2. 状態開始時の処理内容

開始Workflow開始時は、次の手順を実施する。

1. 開始状態であることを確認する。
2. LLM_WORKSPACEの有無を確認する。
3. LLM_WORKSPACEが存在する場合は、Worklog、RequestおよびHandoverの内容を確認する。
4. 現在の作業状況を確認する。
5. 新規作業または作業再開を判定する。
6. 次に実行すべきWorkflowを決定する。
7. 決定したWorkflowへの状態遷移を要求する。

---

## 3. 実施内容

開始Workflowでは、LLM_WORKSPACE仕様に従い、現在の作業状況を確認しなければならない（MUST）。  
作業再開に必要な情報が存在する場合は、その情報を利用して作業を再開してよい（MAY）。  
LLM_WORKSPACEの情報のみを根拠として成果物を生成・更新・検証してはならない（MUST NOT）。  
作業状況が判断できない場合は、利用者へ通知して待機状態に遷移しなければならない（MUST）。  
開始Workflowは、作業内容を直接実施してはならない（MUST NOT）。  
開始Workflowは、次に実行すべきWorkflowを決定後、そのWorkflowへの状態遷移を要求しなければならない（MUST）。

---

[目次](../../../../目次.md) > 仕様 > 状態 > 開始 > 開始Workflow
