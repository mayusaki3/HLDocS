<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260115-010010Z-C3D4
lang: ja-JP
canonical_title: LLM-MANAGEDブロック規約
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../目次.md) > 仕様 > 共通 > LLM-MANAGEDブロック規約

# LLM-MANAGEDブロック規約

本書は、HLDocS における **LLM-MANAGED ブロック**（HTML コメント）の役割、配置、  
必須フィールド、値域、および管理責務を定義する。

---

## 1. 位置付け

- LLM-MANAGED ブロックは **ドキュメント同一性**と  
  **機械可読なメタデータ**を担保するための宣言である。
- 本ブロック内の内容は **LLM のみが編集することを前提**とする。
- 人間による直接編集は、同一性・追跡性を破壊する可能性があるため  
  原則として禁止する。

## 2. 配置（MUST）

- LLM-MANAGED ブロックは **ドキュメント先頭**に配置する。
- 先頭の順序は、共通ドキュメント構造で定義された順序に従う。
- ドキュメント内に **1つのみ** 存在しなければならない。

## 3. 必須フィールド（MUST）と意味

- `doc_id`
  - 恒久的ドキュメント識別子。
  - 内容・ファイル名・パス・見出し構造と独立であり、  
    **論理同一性の鍵**として用いる。
- `lang`
  - 本文の言語コード（例：ja-JP）。
  - 翻訳版は `lang` のみを変え、`doc_id` は維持する。
- `canonical_title`
  - 正規タイトル。
  - 表示・検索のための名称であり、**同一性の鍵ではない**。
- `document_type`
  - ドキュメントの役割（spec / index / template / prompt / note）。
  - 運用上の都合で変更され得るため、**同一性の鍵ではない**。
- `canonical_document`
  - 当該ドキュメントが **正規成果物**であるかを示す。
- `transport`
  - 提示・回収方法の候補を示す I/F 属性。
  - 配列で指定し、先頭要素を既定とする。

## 4. 値域（Value Domain）（MUST）

本章は、LLM-MANAGED ブロックに記載される各フィールドの  
**許容値（値域）**を定義する。  
検証ツールは、本章に基づき NG / WARN を判定してよい。

### 4.1 canonical_document

- 許容値：`true` / `false`
- 真偽値以外は NG とする。

### 4.2 document_type

- 許容値（ENUM）：
  - `spec`
  - `index`
  - `template`
  - `prompt`
  - `note`

- document_type は **役割分類**であり、論理同一性の鍵ではない。

### 4.3 transport

- 許容値（ENUM）：
  - `true_out`
  - `ui_copy`
  - `download`

- transport は **配列**で指定する。
- 配列でない指定、または値域外の要素を含む場合は NG とする。
- transport は **判断規則を含まない**。

#### transport 値の意味（I/F 定義）

- `true_out`  
  ドキュメント本文を **そのまま** 最終成果物として出力する。

- `ui_copy`  
  UI 表示用の加工が行われても、  
  **利用者がコピー不能にならないようガード**された出力を行う。

- `download`  
  ドキュメントを **ファイルとしてダウンロード**可能な形で提供する。

## 5. 管理責務（MUST）

### 5.1 LLM の責務

- doc_id の生成および維持
- canonical_document / transport の設定
- 既に指定されている document_type の維持

### 5.2 人間の責務（例外規定）（MAY）

以下の場合に限り、人間が document_type を追加・変更する行為を許容する。

- 新しい document_type を **仕様として追加**する場合
- document_type 自体の意味・役割を定義・拡張する場合

この場合：

- 人間は **先に仕様（spec）を整備**しなければならない。
- LLM は、既存 ENUM に存在しない document_type を  
  自律的に生成してはならない。

## 6. doc_id の定義と維持（MUST）

- doc_id は恒久的ドキュメント識別子である。
- 以下と完全に独立である：  
  ファイル名 / ディレクトリ構成 / 言語 / 番号 / 内容・意味
- 内容更新・移動・改名でも doc_id は変更しない。
- 翻訳版は原文と同一 doc_id を使用する。

### 6.1 新規生成規則

- 値が空、または `__AUTO__` の場合は新規生成を行う。
- 形式：`doc-YYYYMMDD-HHMMSSZ-XXXX`
- タイムゾーン：UTC 固定
- `XXXX`：4桁 base36
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

[目次](../../目次.md) > 仕様 > 共通 > LLM-MANAGEDブロック規約
