<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260116-121000Z-IDXP
lang: ja-JP
canonical_title: document_type:index 生成プロンプト
document_type: prompt
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > テンプレート > document_type > index > 生成プロンプト

# document_type:index 生成プロンプト

本プロンプトは、HLDocS における `document_type: index` を生成・更新する際の  
**判断規則および自己検査条件**を定義する。

---

## 0. 最上位命令（MUST）

- document_type は **index 固定**とする。
- 一覧対象・階層範囲が未合意の場合、生成してはならない。
- 出力は **最終成果物のみ**とする。

---

## 1. 生成判断規則（MUST）

- index は「リンク列挙」を主体として構成する。
- 各リンクには説明文を付与してはならない。
- 分類・階層は構造としてのみ表現する。

### ガイド文に関する特則

- ガイド文は原則として生成してはならない。
- ユーザー指示に「概要」「目的」「使い方を入れる」等が
  **明示されている場合に限り**、
  本文冒頭に短いガイド文を含めてもよい。
- 指示がない場合、ガイド文を自律的に追加してはならない。

---

## 2. LLM-MANAGED 値決定規則（MUST）

- `doc_id`
  - 新規生成時のみ生成する
  - 更新時は既存値を必ず維持する
- `document_type` : `index`
- `canonical_document` : `true`
- `transport` : `[true_out]`

---

## 3. 禁止事項（MUST NOT）

- 仕様・規約・背景の説明
- 更新理由・差分説明
- TODO・作業指示文

---

## 4. 内部自己検査（非出力・MUST）

- 本文がリンク列挙中心であること
- 禁止事項が含まれていないこと
- 共通ドキュメント構造を満たすこと

---

[目次](../../../目次.md) > テンプレート > document_type > index > 生成プロンプト
