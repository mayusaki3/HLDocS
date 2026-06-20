<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260620-000000Z-LT5A
lang: ja-JP
canonical_title: LLMツール仕様
document_type: spec
canonical_document: true
-->

[目次](../../../目次.md) > 仕様 > 共通 > LLMツール仕様

# LLMツール仕様

## 1. 目的

本書は、HLDocSにおいてLLMが利用するToolの考え方、責務、一覧および利用方法を定義する。

本仕様は、共通仕様成立状態でのみ利用できる。  
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。  
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

---

## 2. LLMツール

### 2.1 定義

LLMツール（以下、Tool）は、LLMが利用可能な能力を提供する仕様要素である。  
Toolは、Workflow、SubFlowまたは通常会話から利用してよい（MAY）。  
Toolは、処理を実施する能力を提供する。  
Toolは、WorkflowまたはSubFlowの処理内容を定義するものではない。  
Toolの実装方法は規定しない。

---

### 2.2 特性

Toolは、LLMが目的達成のために利用できる能力である。  
LLMが利用可能なToolには、LLM標準ToolおよびHLDocS Toolが含まれる。  
HLDocS Toolは、HLDocSがTool一覧および個別Tool仕様により管理するToolである。  
LLM標準Toolは、LLM実行環境から提供されるToolである。  
Toolは、利用者から見た場合、LLMが利用可能な内部能力として扱う。  
Toolは、再利用可能でなければならない（MUST）。  
Toolは、実装方法に依存してはならない（MUST NOT）。

---

### 2.3 責務

Toolは、次の責務を持つ。

- 能力の提供
- 入力仕様の提供
- 出力仕様の提供
- 利用条件の提供
- 制約事項の提供
- 応答仕様の提供

Toolは、利用者との対話を担当してはならない（MUST NOT）。  
Toolは、WorkflowまたはSubFlowの状態管理を行ってはならない（MUST NOT）。  
Toolは、WorkflowまたはSubFlowの処理内容を決定してはならない（MUST NOT）。

---

### 2.4 利用対象

Toolは、次のいずれかから利用できる。

- Workflow
- SubFlow
- 通常会話

利用者は、Toolを直接実行するのではなく、LLMへ要求する。  
LLMは、目的に応じて適切なToolを選択して利用する。

---

## 3. Tool一覧

### 3.1 概要

HLDocSで提供されるToolは、Tool一覧で管理する。  
LLMは、LLMに提供されている標準Toolに加え、Tool一覧で提供されたToolを利用できる。  
Tool一覧は、LLMがToolを選択するために必要な情報を定義する。  

---

### 3.2 登録項目

Tool一覧には、次の項目が定義されている。

- Tool名
- 能力
- 利用条件
- 優先度（優先=HLDocS Toolを優先、標準=LLM標準Toolを優先）
- 個別Tool仕様名

Tool名は、Tool一覧内で一意でなければならない（MUST）。  
Tool名は、「カテゴリ名.Tool名」の形式で定義しなければならない（MUST）。  
能力は、Toolが提供する機能を表現しなければならない（MUST）。  
利用条件は、Toolを利用できる条件および制約の概要を示さなければならない（MUST）。  
優先度は、LLMに提供されている標準Toolと同一能力を提供するToolが存在する場合の推奨順位を示す。  
個別Tool仕様名は、Toolの詳細仕様への参照を示す。

特定のToolを表す場合は、以下の表記を使用する。

- HLDocS.Tool名

例:
```text
HLDocS.GitHub.ls-files
```

---

### 3.3 Tool一覧

| Tool名 | 能力 | 利用条件 | 優先度 | 個別Tool仕様 |
| ---- | ---- | ---- | ---- | ---- |
| GitHub.ls-files | GitHub上のファイル一覧を取得する | リポジトリ、パス、参照先が特定できる場合 | 標準 | [GitHub.ls-files](./LLMツール/GitHub/GitHub.ls-files.md) |

本一覧は、HLDocSで管理するToolを示す。  
本一覧に存在しないLLM標準Toolの利用を禁止してはならない（MUST NOT）。

---

### 3.4 個別Tool仕様

Tool一覧へ登録するToolは、個別Tool仕様を定義しなければならない（MUST）。  
個別Tool仕様は、LLMツール仕様更新ルールに従って作成する。  
個別Tool仕様は、Tool一覧から参照できなければならない（MUST）。

---

## 4. Tool利用

### 4.1 Workflowからの利用

Workflowは、状態管理および処理順序の管理に必要な範囲でToolを利用してよい（MAY）。  
Workflowは、Tool利用結果を状態遷移判断の入力として利用してよい（MAY）。  
Workflowは、Toolに状態遷移を実施させてはならない（MUST NOT）。

---

### 4.2 SubFlowからの利用

SubFlowは、自身の目的を達成するために必要な範囲でToolを利用してよい（MAY）。  
SubFlowは、Tool利用結果を処理結果の生成に利用してよい（MAY）。  
SubFlowは、ToolにWorkflowの状態遷移を実施させてはならない（MUST NOT）。

---

### 4.3 通常会話からの利用

LLMは、通常会話において必要に応じてToolを利用してよい（MAY）。  
通常会話でToolを利用する場合も、Toolの利用条件および制約に従わなければならない（MUST）。

---

## 5. Tool選択

### 5.1 選択原則

LLMは、目的を達成するために適切なToolを選択しなければならない（MUST）。  
Tool選択時は、次の事項を考慮しなければならない（MUST）。

- 能力
- 利用条件
- 制約
- 取得可能な情報
- 実行環境
- 優先度

---

### 5.2 LLM標準Tool

LLM標準Toolで目的を達成できる場合は、LLM標準Toolを利用してよい（MAY）。  
LLM標準Toolの利用は、HLDocS Toolの存在によって禁止されない。

---

### 5.3 HLDocS Tool

HLDocS Toolは、HLDocSがTool一覧および個別Tool仕様で管理するToolである。  
LLM標準Toolで目的を達成できない場合は、HLDocS Toolを利用してよい（MAY）。  
HLDocS Toolは、LLM標準Toolの不足を補うために定義してよい（MAY）。

---

### 5.4 代替Tool

同一目的を達成可能なToolが複数存在する場合、LLMは目的達成に最も適したToolを選択しなければならない（MUST）。  
Tool一覧に優先度が定義されている場合は、優先度を考慮しなければならない（MUST）。  
ただし、優先度よりも利用条件、制約、取得可能な情報が適合するToolがある場合は、そのToolを選択してよい（MAY）。

---

## 6. Workflow・SubFlowとの責務境界

Workflowは、処理順序および状態管理を担当する。  
SubFlowは、処理仕様および処理結果生成を担当する。  
Toolは、能力の提供を担当する。

Toolは、Workflowの代替であってはならない（MUST NOT）。  
Toolは、SubFlowの代替であってはならない（MUST NOT）。  
WorkflowおよびSubFlowは、必要に応じてToolの能力を利用してよい（MAY）。

---

## 7. 実装要求

本仕様は、Tool利用モデルのみを規定する。  
Python、GitHub、Web、MCP、専用Tool等の実装方法は規定しない。  
Toolの実装方法は、個別Tool仕様または実行環境に委ねる。  
Toolは、実装環境で許可された範囲でのみ利用しなければならない（MUST）。

---

[目次](../../../目次.md) > 仕様 > 共通 > LLMツール仕様
