<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260115-010010Z-C3D4
lang: ja-JP
canonical_title: LLM-MANAGEDブロック規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > LLM-MANAGEDブロック規約

# LLM-MANAGEDブロック規約

本書は、HLDocS において **LLM-MANAGED ブロック**（HTML コメント形式）の役割、配置、  
必須フィールド、値域、および管理責務を定義する。

本書は、「HLDocS 前提条件」という仕様が参照可能である場合にのみ適用される。
- 前提条件が参照できない、または前提条件に基づく適用可否が未確定な場合、  
本書に基づく判断・生成・再作成・工程実行を行ってはならず、  
提示された内容の確認のみに留めなければならない。

---

## 1. 位置付け

- LLM-MANAGED ブロックは **ドキュメント同一性**と **機械可読なメタデータ**を担保するための宣言である。
- 本ブロック内の内容は **LLM のみが編集することを前提**とする。
- 人間による直接編集は、同一性・追跡性を破壊する可能性があるため原則として禁止する。

---

## 2. 配置（MUST）

- LLM-MANAGED ブロックは **ドキュメント先頭**に配置する。
- 先頭の順序は、[共通ドキュメント構造](./03_共通ドキュメント構造.md) で定義された順序に従う。
- ドキュメント内に **1つのみ** 存在しなければならない。

---

## 3. 必須フィールド（MUST）と意味

LLM-MANAGED ブロックに記載してよいフィールドは、
本規約で明示的に定義されたフィールドに限る（closed set）。
それ以外のフィールドを追加してはならない（MUST NOT）。

- `doc_id`
  - 恒久的ドキュメント識別子。
  - 内容・ファイル名・パス・見出し構造と独立であり、**論理同一性の鍵**として用いる。
- `lang`
  - 本文の言語コード（例：ja-JP）。
  - 翻訳版は `lang` のみを変え、`doc_id` は維持する。
- `canonical_title`
  - 正規タイトル。
  - 表示・検索のための名称であり、**同一性の鍵ではない**。
- `document_type`
  - ドキュメントの役割。
  - 運用上の都合で変更され得るため、**同一性の鍵ではない**。
- `canonical_document`
  - 当該ドキュメントが **正規成果物**であるかを示す。

---

## 4. 値域（Value Domain）（MUST）

本章は、LLM-MANAGED ブロックに記載される各フィールドの **許容値（値域）**を定義する。  
検証ツールは、本章に基づき NG / WARN を判定してよい。

### 4.1 canonical_document

- 許容値：true / false
- 真偽値以外は NG とする。

### 4.2 document_type

- 許容値（ENUM）：
  - spec
  - index
  - template
  - prompt
  - testspec
  - note
  - minutes
  - usage

- document_type は **役割分類**であり、論理同一性の鍵ではない。

---

## 5. 管理責務（MUST）

### 5.1 LLM の責務

- doc_id の生成および維持
- canonical_document の設定
- 既に指定されている document_type の維持

### 5.2 人間の責務（例外規定）（MAY）

以下の場合に限り、人間が document_type を追加・変更する行為を許容する。

- 新しい document_type を **仕様として追加**する場合
- document_type 自体の意味・役割を定義・拡張する場合

この場合：

- 人間は **先に仕様（spec）を整備**しなければならない。
- LLM は、既存 ENUM に存在しない document_type を自律的に生成してはならない。

---

## 6. doc_id の定義と維持（MUST）

- doc_id は恒久的ドキュメント識別子である。
- 以下と完全に独立である：ファイル名 / ディレクトリ構成 / 言語 / 番号 / 内容・意味
- 内容更新・移動・改名でも doc_id は変更しない。
- 翻訳版は原文と同一 doc_id を使用する。

### 6.1 新規生成規則

- 値が空、または `__AUTO__` の場合は新規生成を行う。
- 形式：doc-YYYYMMDD-HHMMSSZ-XXXX
- タイムゾーン：UTC 固定
- XXXX：4桁 base36
- 衝突時：再生成

### 6.2 doc_id を変更してよい条件（MAY）

以下は **論理的に別ドキュメント**とみなすため、新しい doc_id を割り当ててよい。

- 明示的な **分割**
- 明示的な **統合**
- **置換**（内容の継承を行わない）
- **新規作成**

### 6.3 禁止（MUST NOT）

- 生成や差し替えの都合で doc_id を再生成してはならない。
- 可読性のために意味語を doc_id に含めてはならない。

---

## 7. document_type 対応 mode 定義（SUPPORTED MODES）（MUST）

本章は、各 `document_type` が **対応可能な mode** を定義する。  
ここで定義されていない mode の組み合わせは **仕様違反**とする。

### 7.1 判定規則

- `(mode, document_type)` の組が `supported_modes` に含まれない場合、
  - required inputs の判定を行う前に **FAIL-FAST** とする。
- 本章は、**required inputs 判定の前段制約**である。

### 7.2 document_type 別 supported_modes（正本）

- `spec`
  - supported_modes: { meta, apply }

- `template`
  - supported_modes: { meta, apply }

- `prompt`
  - supported_modes: { meta, apply }

- `testspec`
  - supported_modes: { apply }

- `index`
  - supported_modes: { apply }

- `note`
  - supported_modes: { apply }

- `minutes`
  - supported_modes: { apply }

- `usage`
  - supported_modes: { apply }

---

## 8. document_type 付随メタ情報（REQUIRED INPUTS）（MUST）

本章は、各 `document_type` が  
**生成時に要求する追加入力（テンプレート／生成プロンプト）**を  
**mode 別に機械判定可能な形で定義**する。

ここで定義される情報は、  
**不足チェックの正本**として使用される。

### 8.1 判定軸

required inputs は、以下の組で決定される。

- `mode`：`meta` / `apply`
- `document_type`

### 8.2 定義項目

- `requires_body_template_by_mode`
- `requires_type_prompt_by_mode`

各項目は boolean 値を持ち、  
`true` の場合は当該入力が **必須**であることを示す。

---

### 8.3 document_type 別定義（正本）

#### spec

- `requires_body_template_by_mode`
  - `meta`: false
  - `apply`: true
- `requires_type_prompt_by_mode`
  - `meta`: false
  - `apply`: true

※ `meta` モードでは、HLDocS 自身の仕様（共通仕様群）を対象とするため、  
個別テンプレート／個別生成プロンプトを要求しない。

---

#### template / prompt

- `requires_body_template_by_mode`
  - `meta`: false
  - `apply`: false
- `requires_type_prompt_by_mode`
  - `meta`: false
  - `apply`: false

---

#### testspec / index / note / minutes / usage

- `requires_body_template_by_mode`
  - `meta`: true
  - `apply`: true
- `requires_type_prompt_by_mode`
  - `meta`: true
  - `apply`: true

---

## 9. 運用上の制約（MUST）

- mode 対応可否の判定は **第7章**を正本とする。
- required inputs の判定は **第8章**を正本とする。
- 生成プロンプト・運用規約・ツール実装は、  
  これらの判定結果を **機械的に適用**しなければならない。
- 不足入力が存在する場合、  
  推測・補完・代替生成を行ってはならない。

---

[目次](../../目次.md) > 仕様 > 共通 > LLM-MANAGEDブロック規約
