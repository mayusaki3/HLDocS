目次 > 仕様 > document_type > index > index 仕様

<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260116-120000Z-IDX1
lang: ja-JP
canonical_title: document_type:index 仕様
document_type: spec
canonical_document: true
transport: [true_out]
-->

# document_type:index 仕様

本書は、HLDocS における `document_type: index` の意味・役割・制約を定義する
**正規仕様（spec）**である。

---

## 1. Purpose（存在理由）

`document_type: index` は、  
**複数ドキュメント間の構造的な関係を一覧化し、参照・遷移を容易にする**
ことを目的とする。

index は以下を担う。

- ドキュメント集合の俯瞰
- 階層・分類・関連性の明示
- 人間および LLM にとってのナビゲーション起点

---

## 2. Non-goals（対象外）

index は、以下を目的としない。

- 仕様・規約・方針の説明
- 各ドキュメント内容の要約・解釈
- 判断規則・生成規則の提示
- 作業手順・更新履歴の記載

index は **案内役**であり、**説明役ではない**。

---

## 3. Classifier（判定条件）

以下のすべてを満たすドキュメントは `document_type: index` と判定される。

- 主体が「一覧」「目次」「インデックス」である
- 本文の大部分が **リンクまたは参照関係の列挙**で構成される
- 個別ドキュメントの内容説明を含まない
- 他の document_type（spec / template / prompt 等）の本文を代替しない

いずれかを満たさない場合、index として扱ってはならない。

---

## 4. 記載内容の制約

### 4.1 許可される内容（MUST / MAY）

- ドキュメントへの相対リンク
- 階層構造（章・カテゴリ・グループ）
- ファイル名・正式タイトル
- 簡潔な分類ラベル（例：共通 / document_type / 使い方）

### 4.2 禁止される内容（MUST NOT）

- 各ドキュメントの本文要約
- 規約・仕様の解説文
- 判断基準・生成ルール
- 作業メモ・TODO・履歴

---

## 5. 更新・再生成ルール

- 新規ドキュメントの追加・削除・移動が発生した場合、index は更新対象となる。
- index の更新は **内容追記ではなく、構造の再評価**として行う。
- 更新時も `doc_id` は **必ず維持**する。
- index の更新は、他ドキュメントの内容変更を伴ってはならない。

---

## 6. LLM-MANAGED の扱い（index 固有）

- `document_type` は常に `index` とする。
- `canonical_document` は通常 `true` とする。
- `transport` は既定で `[true_out]` とする。
- index 生成時、他 document_type の LLM-MANAGED 値を推測・流用してはならない。

---

## 7. 内部自己検査（非出力）

生成・更新時、以下を内部的に検査しなければならない。

- 本文がリンク列挙中心であること
- 禁止内容（説明文・要約）が含まれていないこと
- 階層リンク行が先頭・末尾で一致していること
- LLM-MANAGED ブロックが規約位置にあること

検査結果は **出力してはならない**。

---

