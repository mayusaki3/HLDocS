<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260204-000001Z-a7k3
lang: ja-JP
canonical_title: 共通ドキュメント生成プロンプト
document_type: prompt
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > 共通ドキュメント生成プロンプト

# 共通ドキュメント生成プロンプト

本プロンプトは、HLDocS において  
**共通ドキュメントテンプレートおよび document_type 別テンプレートを用いて  
ドキュメントを新規生成・再作成する際に、LLM が従わなければならない判断規範および内部実行規則**を定義する。

本プロンプトは **document_type = prompt / mode = meta** として生成されており、  
HLDocS 自身の仕様・テンプレート・生成プロンプトを生成・再作成するためにのみ使用される。

本プロンプトは、仕様（spec）・規約本文が生成フェーズに与えられない状況でも、  
単体で判断規範として成立しなければならない。

---

## 0. 適用条件（MUST）

本プロンプトは、以下の条件をすべて満たす場合にのみ使用してよい。

- document_type = `prompt`
- mode = `meta`
- operation = `new` / `recreate` / `patch`
- 共通ドキュメントテンプレートが入力として与えられている

上記条件を満たさない場合、生成を開始してはならない（MUST NOT）。

---

## 1. 生成フェーズ実行順序（MUST）

LLM は、ドキュメント生成・再作成において、  
以下のフェーズを **順序を変更せず** 内部的に実行しなければならない。

1. Phase 0: 入力検証（FAIL-FAST）
2. Phase 1: テンプレート抽出
3. Phase 2: テンプレート合成
4. Phase 3: 可変スロット生成
5. Phase 4: 構造トークン実体化
6. Phase 5: Transport Encoding 適用
7. Phase 6: 最終検証（非出力）
8. Phase 7: 出力

各フェーズの詳細な振る舞いは、  
本プロンプト内の規定に **逐語で従わなければならない**。

---

## 2. Phase 0: 入力検証（FAIL-FAST / MUST）

LLM は生成処理を開始する前に、以下を機械的に検証しなければならない。

### 2.1 supported_modes 判定テーブル（再掲・正本）

```
document_type | supported_modes
--------------|-----------------
spec          | { meta, apply }
template      | { meta, apply }
prompt        | { meta, apply }
testspec      | { apply }
index         | { apply }
note          | { apply }
minutes       | { apply }
usage         | { apply }
```

- `(document_type, mode)` の組が上表に含まれない場合、FAIL-FAST とする。

---

### 2.2 required inputs 判定テーブル（再掲・正本）

```
document_type | mode  | requires_body_template | requires_type_prompt
--------------|-------|------------------------|-----------------------
spec          | meta  | false                  | false
spec          | apply | true                   | true
template      | meta  | false                  | false
template      | apply | false                  | false
prompt        | meta  | false                  | false
prompt        | apply | false                  | false
testspec      | meta  | true                   | true
testspec      | apply | true                   | true
index         | meta  | true                   | true
index         | apply | true                   | true
note          | meta  | true                   | true
note          | apply | true                   | true
minutes       | meta  | true                   | true
minutes       | apply | true                   | true
usage         | meta  | true                   | true
usage         | apply | true                   | true
```

- 必須入力が欠落している場合、FAIL-FAST とする。
- 欠落情報を推測・補完してはならない（MUST NOT）。

---

### 2.3 Transport Encoding ENUM（再掲・正本）

```
transport = true_out
transport = ui_copy
transport = download
```

- 指定された transport 値が上記 ENUM に含まれない場合、FAIL-FAST とする。

---

## 3. テンプレート合成規則（MUST）

- 共通ドキュメントテンプレートから  
  `__COMMON_TEMPLATE_BEGIN__` ～ `__COMMON_TEMPLATE_END__` の範囲のみを使用する。
- `__DOCUMENT_BODY__` 位置に本文テンプレート範囲を **無加工で差し込む**。
- テンプレート範囲内の内容を改変・再解釈してはならない。

---

## 4. document_type = prompt における判断制約（MUST）

- 生成対象となっている prompt 本文を、  
  判断根拠・制約導出・仕様補完に使用してはならない。
- 本文内容は **意味的に不可知な成果物**として扱うこと。
- 再作成（recreate / patch）の結果は、  
  同一仕様・同一テンプレート・同一規約が与えられた場合、  
  `new` と **意味等価**でなければならない。

---

## 5. 不変条件の遵守（MUST）

再作成（recreate / patch）の場合、以下を必ず保持すること。

- doc_id
- canonical_title
- document_type
- 文書全体の構造順序
- 階層リンク行（先頭・末尾）

省略表現・差分表現・参照代替表現を使用してはならない。

---

## 6. Transport Encoding = ui_copy の適用（MUST）

- 出力は **単一成果物・単一コードブロック**とする。
- コードブロック内には、当該成果物の Markdown 全文のみを含める。
- 外側フェンスは、本文中の最大連続バッククォート数 + 1 とする。
- コードブロック外に、説明・注釈・補足文を出力してはならない。

---

## 7. 最終検証（非出力 / MUST）

LLM は出力前に、以下を内部検証しなければならない。

- 共通ドキュメント構造に違反していないこと
- Phase 0 判定条件をすべて満たしていること
- 推測・補完・暗黙知を用いていないこと
- 再掲された判定テーブル・ENUM が逐語であること

検証結果を出力してはならない。

---

[目次](../../目次.md) > 仕様 > 共通 > 共通ドキュメント生成プロンプト
