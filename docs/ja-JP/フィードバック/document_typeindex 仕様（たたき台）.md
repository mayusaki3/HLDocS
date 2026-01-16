<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260115-020100Z-INDEX
lang: ja-JP
canonical_title: document_type:index 仕様
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../目次.md) > 仕様 > document_type > index

# document_type:index 仕様

本書は、HLDocS における **document_type:index** の責務、構造、運用上の意味を定義する。

---

## 1. 位置付け（Purpose）

document_type:index は、  
**複数ドキュメントを論理的に束ね、探索・参照・導線を提供するための文書**である。

- index は「仕様そのもの」ではない
- index は「生成物の一覧」でもない
- index は **意味的なハブ（構造的目次）**である

---

## 2. 責務（Responsibilities）

document_type:index の責務は以下に限定される。

### 2.1 含めてよいもの（MAY）

- 他ドキュメントへのリンク
- 論理階層（カテゴリ・章・節）の表現
- 簡潔な説明文（導線補助）
- 文書群の関係性（包含・分割・参照）

### 2.2 含めてはならないもの（MUST NOT）

- 仕様の詳細定義
- 振る舞い・ルール・制約の新規定義
- 他 document_type が担う責務の再記述
- 単体仕様を代替する記述

index は **説明してよいが、定義してはならない**。

---

## 3. canonical_document との関係

- document_type:index は **canonical_document = true** とする
- index 自体は正規成果物である
- ただし、index は **内容の正規性を定義しない**

正規性の定義は、リンク先の document_type:spec 等が担う。

---

## 4. transport の既定（Default）

document_type:index の既定 transport は以下とする。

- `canonical_document = true`
- 既定 transport: `[true_out]`

理由：
- index は UI 上での閲覧が主目的
- 構造が比較的単純であり、UI 崩壊リスクが低い
- download を前提としない

※ 大規模 index の場合、運用判断で `[ui_copy]` を追加してもよい（MAY）。

---

## 5. doc_id の扱い

- index も **独立した論理ドキュメント**である
- 以下の場合でも doc_id は **維持**する（MUST）：
  - 掲載リンクの追加・削除
  - 階層構造の変更
  - 見出し構成の変更
  - index が指す文書群の分割・統合

### 5.1 doc_id を変更してよい条件（MAY）

- index 自体の役割を廃止し、別 index に置換する場合
- 論理的に別概念の index を新設する場合

---

## 6. 構造要件（MUST）

document_type:index は、  
**共通ドキュメント構造**に完全準拠しなければならない。

- LLM-MANAGED ブロック
- 階層リンク行（先頭・末尾）
- 本文
- `---` 区切り

本文構造は自由だが、  
**階層とリンクの対応関係が読み取れること**を必須とする。

---

## 7. 他 document_type との関係

- index は以下の document_type を束ね得る：
  - spec
  - template
  - prompt
  - guide
  - index（入れ子）

- index ↔ spec は **参照関係**のみ
- index ↔ index は **階層関係**を形成できる

---

## 8. 設計上の原則（Design Principles）

- index は「軽い」
- index は「壊れにくい」
- index は「書き換えやすい」
- index の変更が **仕様の意味を変えてはならない**

---

## 9. 禁止事項（MUST NOT）

- index を仕様の代替として使うこと
- index に仕様変更を埋め込むこと
- index の都合で spec 側の構造を歪めること

---

[目次](../../目次.md) > 仕様 > document_type > index
