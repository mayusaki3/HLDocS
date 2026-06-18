<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260618-000000Z-XXXX
lang: ja-JP
canonical_title: 待機Workflow
document_type: spec
canonical_document: true
-->

[目次](../../../../目次.md) > 仕様 > 状態 > 待機 > 待機Workflow

# 待機Workflow

## 1. 目的

本Workflowは、待機状態における利用者入力の受付および開始可能なWorkflowの判定を定義する。

本仕様は、共通仕様成立状態でのみ利用できる。
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

## 2. 状態開始時の処理内容

待機Workflow開始時は、次の手順を実施する。

1. 待機状態であることを報告する。
2. 状態マシン仕様の状態・Workflow一覧から、待機Workflow以外の
   開始可能なWorkflowを利用者が認識できるようにする。

## 3. 実施内容

待機Workflowでは、次の手順を実施する。

1. 利用者入力を受信し、応答する。

---

[目次](../../../../目次.md) > 仕様 > 状態 > 待機 > 待機Workflow
