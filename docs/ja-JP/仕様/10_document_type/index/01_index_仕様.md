<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260116-120000Z-IDX1
lang: ja-JP
canonical_title: document_type:index 仕様
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > 仕様 > document_type > index > index 仕様

# document_type:index 仕様

本書は、HLDocS における `document_type: index` の意味・役割・制約を定義する
**正規仕様（spec）**である。

---

## 1. Purpose（存在理由）

`document_type: index` は、  
**複数ドキュメント間の構造的関係を一覧化し、参照と遷移を容易にする**
ことを唯一の目的とする。

index は以下を担う。

- ドキュメント集合の俯瞰
- 階層・分類・関係性の可視化
- 人間および LLM にとってのナビゲーション起点

---

## 2. Non-goals（対象外）

index は以下を目的としない。

- 仕様・規約・方針の説明
- 各ドキュメント内容の要約・解釈
- 判断基準・生成規則の提示
- 作業手順・更新履歴・背景説明

index は **案内役**であり、**説明役ではない**。

---

## 3. Classifier（判定条件）

以下のすべてを満たす場合のみ `document_type: index` とする。

- 主体が「一覧」「目次」「インデックス」である
- 本文の大部分が **リンクまたは参照関係の列挙**で構成される
- 個別ドキュメントの本文説明を含まない
- 他の document_type（spec / template / prompt 等）を代替しない

---

## 4. 記載内容の制約

### 4.1 許可される内容（MUST / MAY）

- ドキュメントへの相対リンク
- 階層構造（章・カテゴリ・グループ）
- ファイル名・canonical_title
- 最小限の分類ラベル（例：共通 / document_type / 仕様）

### 4.2 禁止される内容（MUST NOT）

- 本文要約・解説文
- 規約や仕様の説明
- 判断ロジック・生成ルール
- TODO・メモ・履歴・作業指示

---

## 5. ガイド文の扱い（条件付き）

原則として、index 本文はリンク列挙主体とし、
説明文・解説文を含めてはならない（MUST）。

ただし **ユーザーから明示的な指示が与えられた場合に限り**、
本文冒頭に短いガイド文を含めてもよい（MAY）。

ガイド文は、以下の制約をすべて満たさなければならない。

- 全体目的・使い方レベルに限定する
- 個別ドキュメントの説明・要約を含めない
- 判断規則・運用規約・生成方法を含めない

ユーザー指示がない場合、
ガイド文を自律的に追加してはならない（MUST NOT）。

---

## 6. 更新・再生成ルール

- 追加・削除・移動が発生した場合、index は更新対象となる。
- 更新は **追記ではなく構造再評価**として行う。
- 更新時も `doc_id` は必ず維持する。
- index 更新は、他ドキュメントの本文変更を伴ってはならない。

---

## 7. LLM-MANAGED の扱い（index 固有）

- `document_type` は常に `index`
- `canonical_document` は原則 `true`
- `transport` は既定で `[true_out]`
- 他 document_type の LLM-MANAGED 値を推測・流用してはならない

---

## 8. 内部自己検査（非出力）

- 本文がリンク列挙中心であること
- 禁止内容が含まれていないこと
- 階層リンク行が先頭・末尾で一致していること
- LLM-MANAGED ブロックが規約位置にあること

---

[目次](../../../目次.md) > 仕様 > document_type > index > index 仕様
