<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260619-000000Z-X5P8
lang: ja-JP
canonical_title: Workflow・SubFlow仕様更新ルール
document_type: spec
canonical_document: true
-->

[目次](../目次.md) > HLDocS更新ルール > Workflow・SubFlow仕様更新ルール

# Workflow・SubFlow仕様更新ルール

## 1. 目的

本書は、Workflow・SubFlow仕様に定義するWorkflowおよびSubFlowの更新条件を定義する。  
本書はHLDocS仕様/規約の作成・更新時のみ参照する。  
HLDocS利用時には参照しない。

## 2. 適用範囲

本書はHLDocS仕様/規約に適用する。  
作業対象正本には適用しない。

## 3. 更新条件

以下のいずれかを行う場合は、Workflow・SubFlow仕様を更新しなければならない（MUST）。

- Workflowを追加する場合
- Workflowを削除する場合
- Workflowを変更する場合
- SubFlowを追加する場合
- SubFlowを削除する場合
- SubFlowを変更する場合
- WorkflowとSubFlowの参照関係を追加・削除・変更する場合

## 4. 更新規則

Workflowを追加・削除・変更する場合は、共通仕様成立条件更新ルールに従い、仕様要素一覧を更新しなければならない（MUST）。  
Workflowを追加・削除・変更する場合は、状態マシン仕様更新ルールに従い、状態・Workflow一覧を更新しなければならない（MUST）。

SubFlowを追加・削除・変更する場合は、共通仕様成立条件更新ルールに従い、仕様要素一覧を更新しなければならない（MUST）。  
Workflowが参照するSubFlowは、共通仕様成立条件に定義する仕様要素一覧へ登録されていなければならない（MUST）。

SubFlowの参照関係は循環してはならない（MUST NOT）。  
SubFlowは、自身を直接または間接に呼び出してはならない（MUST NOT）。  
SubFlowを追加・変更する場合は、循環参照が存在しないことを確認しなければならない（MUST）。

利用者実行を許可するHLDocS Toolは、
利用者実行へ移行する条件を個別Tool仕様に定義しなければならない（MUST）。
WorkflowまたはSubFlowは、個別Tool仕様に定義されていない利用者実行を行ってはならない（MUST NOT）。

---

[目次](../目次.md) > HLDocS更新ルール > Workflow・SubFlow仕様更新ルール
