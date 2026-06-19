<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260619-000000Z-Q7N4
lang: ja-JP
canonical_title: Workflow・SubFlow仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > Workflow・SubFlow仕様

# Workflow・SubFlow仕様

## 1. 目的

本書は、HLDocSにおけるWorkflowおよびSubFlowの構成、責務、実行方法を定義する。

本仕様は、共通仕様成立状態でのみ利用できる。  
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。  
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

---

## 2. Workflow

### 2.1 定義

Workflowは、状態マシンにおける各状態で実行される処理単位である。  
Workflowは状態開始から状態終了までを管理する責務を持つ。

---

### 2.2 責務

Workflowは、次の責務を持つ。

- 状態開始時処理
- 利用者入力の受付
- 実行対象SubFlowの決定
- 状態引継ぎ情報の管理
- 状態終了判定
- 次状態への遷移要求

---

### 2.3 開始条件

Workflowは、状態マシン仕様で定義された開始条件を満たした場合のみ開始できる（MUST）。

---

### 2.4 終了条件

Workflowは、次のいずれかで終了する。

- 次状態への遷移を要求した場合
- 終了状態へ遷移した場合

Workflow終了後は、状態マシンへ制御を返さなければならない（MUST）。

---

## 3. SubFlow

### 3.1 定義

SubFlowは、Workflow内部で実行される処理単位である。  
SubFlowは単一目的の処理のみを担当する。

---

### 3.2 責務

SubFlowは次の責務を持つ。

- 単一目的の処理実施
- 処理結果生成
- Workflowへの制御返却

---

### 3.3 開始条件

SubFlowはWorkflowからのみ開始できる（MUST）。  
利用者入力または状態マシンから直接開始してはならない（MUST NOT）。

SubFlowは、共通仕様成立条件にて定義する仕様要素一覧へ登録されていなければならない（MUST）。  

---

### 3.4 終了条件

SubFlowは処理完了後、呼び出し元Workflowへ制御を返さなければならない（MUST）。  
SubFlow自身が状態遷移を行ってはならない（MUST NOT）。

---

### 3.5 内部制御

SubFlowは、自身の目的を達成するため、内部に処理手順、条件分岐、および繰り返しを定義できる。

SubFlow内部の条件分岐および繰り返しは、SubFlowの責務範囲内で完結しなければならない（MUST）。  
この内部処理では、必要に応じて他のSubFlowを呼び出してよい（MAY）。  

SubFlow内部の繰り返しは、終了条件または最大試行回数を定義しなければならない（MUST）。  
SubFlow内部の繰り返しは、終了条件または最大試行回数を満たした場合に終了しなければならない（MUST）。  
SubFlow内部の条件分岐および繰り返しは、Workflowの状態遷移を直接実施してはならない（MUST NOT）。

---

## 4. WorkflowとSubFlowの関係

### 4.1 呼び出し

Workflowは必要に応じて複数のSubFlowを呼び出すことができる。  
SubFlowは必要に応じて他のSubFlowを呼び出すことができる。

---

### 4.2 復帰

SubFlow終了後は、呼び出し元へ復帰しなければならない（MUST）。

---

### 4.3 状態受け渡し

WorkflowからSubFlowへは、処理実行に必要な状態情報のみを受け渡すものとする。  
不要な情報を受け渡してはならない（MUST NOT）。

---

### 4.4 参照境界

WorkflowおよびSubFlowは、自身の処理実行に必要な仕様のみを参照しなければならない（MUST）。  
不要なWorkflow、SubFlow、仕様書を参照してはならない（MUST NOT）。

---

## 5. 実行規則

### 5.1 Workflow実行

Workflowは状態開始時から終了時まで継続して実行される。

---

### 5.2 SubFlow実行

SubFlowは呼び出し時のみ実行される。

---

### 5.3 中断

WorkflowおよびSubFlowは、
他のWorkflowまたはSubFlowを実行するため、必要に応じて処理を中断できる。  
再開に必要な状態情報が利用可能でなければならない（MUST）。

---

### 5.4 再開

中断されたWorkflowまたはSubFlowは、中断時の状態情報を用いて再開しなければならない（MUST）。

---

## 6. 実装要求

WorkflowおよびSubFlowは、実装方法、ファイル構成、プログラミング言語、生成方法に依存してはならない（MUST NOT）。  
本仕様は実行モデルのみを規定し、更新方法、管理方法、変更手順は規定しない。  
これらは「HLDocS更新仕様」に従う。

---

[目次](../../目次.md) > 仕様 > 共通 > Workflow・SubFlow仕様
