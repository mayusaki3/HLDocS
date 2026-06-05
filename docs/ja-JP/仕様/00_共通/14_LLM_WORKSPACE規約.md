<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260605-180002Z-C8Q3
lang: ja-JP
canonical_title: LLM_WORKSPACE規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > LLM_WORKSPACE規約

# LLM_WORKSPACE規約

本規約は、LLMが作業状態を保持し、チャット移行やセッション終了後も継続して作業できるようにするための運用ルールを定義する。  
また、作業状態の消失や引継ぎ漏れを防止することを目的とする。

本書は、「HLDocS 前提条件」という仕様が参照可能である場合にのみ適用される。
- 「HLDocS 前提条件」が入力として与えられていない場合、  
または当該仕様に基づく適用可否が確定していない場合、  
本書に基づく判断・生成・再作成・工程実行を行ってはならない。
- この場合、許可されるのは、  
提示された文書の受理および存在確認、  
ならびに前提条件が未参照または未確定である旨の通知のみとする。
- 「HLDocS 前提条件」が入力文書一覧に含まれない場合、生成・再作成・成果物提示を一切行ってはならない。

---

## 適用範囲

本規約は以下に適用する。

* Request
* Worklog
* Handover
* その他LLM_Workspace配下の成果物

---

## 基本原則

### LLM_Workspace

LLM_Workspaceは、LLMが作業状態を保持するための論理領域である。

---

### 論理構造と物理保存先

LLM_Workspaceは論理構造である。  
保存先は以下のいずれでもよい。

* GitHub
* 添付ファイル
* チャット
* その他利用者が管理する保存先

格納場所は、リポジトリルートまたはそれに相当する場所とする。

---

### GitHub依存禁止

LLM_WorkspaceはGitHubへ依存してはならない（MUST NOT）。  
GitHubが利用できない場合でも運用を継続できなければならない（MUST）。

---

### 正本

Worklogを作業状態の正本とする。  
HandoverおよびRequestと矛盾する場合はWorklogを優先する。

---

## ディレクトリ構造

例

```text
LLM_Workspace
├─ Request
├─ Worklog
└─ Handover
```

構造は必要に応じて拡張してよい。

---

## Request

### 目的

未処理要求を保持する。

---

### 内容

以下を記録してよい。

* 利用者要求
* 他チャットからの要求
* 運用改善案
* 問題報告
* 気付き
* 将来対応予定事項

---

### 管理主体

LLMはRequestを更新してよい（MAY）。

---

### 削除

要求が成果物へ反映された場合、Requestから削除することを推奨する。

---

## Worklog

### 目的

現在進行中の作業状態を保持する。

---

### 内容

以下を記録する。

* 作業計画
* 実施状況
* 決定事項
* 保留事項
* 次工程

---

### 正本

Worklogを作業状態の正本とする。

---

### 管理主体

LLMはWorklogを更新してよい（MAY）。

---

## Handover

### 目的

他チャットまたは他LLMへ作業内容を引継ぐ。

---

### 内容

以下を記録する。

* 現在の作業状態
* 次工程
* 注意事項
* 引継ぎ事項

---

### 正本ではない

Handoverは正本ではない。  
Worklogの要約または派生成果物として扱う。

---

## 作業再開

### 基本原則

作業再開時はWorklogを参照する。  
LLMは過去の会話記憶へ依存してはならない（MUST NOT）。

---

### 作業再開優先順位

1. Worklog
2. 利用者指示
3. Handover
4. Request
5. FAIL-FAST

---

### Worklog

Worklogは現在進行中の作業状態を保持する。  
作業再開時は最優先で参照する。

---

### Handover

Handoverは補助情報である。  
利用者から指示がない限り参照を必須としない。

---

### Request

Requestは未処理要求である。  
現在の作業が完了するまで、利用者から指示がない限り参照を必須としない。

---

## 作業再開方法

### GitHub

利用者がリポジトリおよびブランチを指定した場合、LLMはLLM_Workspaceの取得を試みることを推奨する。

---

### 添付ファイル

GitHubが利用できない場合、利用者は以下を添付できる。

* LLM_Workspace.zip
* Worklog
* Handover
* Request

---

### チャット

GitHubおよび添付が利用できない場合、利用者は以下をチャットへ貼付できる。

* Worklog
* Handover
* Request

---

## 運用フロー

```text
利用者要求
↓
Request

採用
↓
Worklog

作業実施
↓
成果物

不要化
↓
Request削除

必要時
↓
Handover生成
```

---

## 更新規則

LLM_Workspaceの更新は成果物更新運用規約に従う。

---

## FAIL-FAST

作業状態を復元できない場合、LLMは推測してはならない。  
利用者へ以下の提供を要求する。

* Worklog
* Handover
* Request
* LLM_Workspace

---

## Traceability

本規約は以下へ影響する。

* 成果物更新運用規約
* 生成プロンプト運用規約
* README
* Handover運用
* チャット移行運用

---

[目次](../../目次.md) > 仕様 > 共通 > LLM_WORKSPACE規約
