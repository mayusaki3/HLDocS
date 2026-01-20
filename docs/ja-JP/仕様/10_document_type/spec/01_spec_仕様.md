<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260120-000000Z-SPC1
lang: ja-JP
canonical_title: document_type:spec 仕様
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > 仕様 > document_type > spec > spec 仕様

# document_type:spec 仕様

本書は、HLDocS における `document_type: spec` の役割・責務・制約を定義する  
**最小仕様（spec）**である。

---

## 1. Purpose（存在理由）

`document_type: spec` は、  
**システム・規約・構造における「正」を宣言するための文書**である。

spec は以下を担う。

- 用語・概念・構造の定義
- 不変条件・制約・前提の宣言
- 他 document_type が参照する基準点の提供

spec は **説明のための文書ではなく、宣言のための文書**である。

---

## 2. Non-goals（対象外）

spec は以下を目的としない。

- 実装手順・運用手順の説明
- テスト観点・検証方法・網羅性の記述
- テストケース・検証結果の列挙
- 生成方法・編集手順の説明

検証・確認・テストに関する内容は、  
**spec とは別の document_type** で扱う。

---

## 3. Classifier（判定条件）

以下のすべてを満たす場合、`document_type: spec` と判定される。

- 主体が「仕様」「規約」「定義」である
- 内容が **正否の基準（正を宣言する文）** で構成されている
- 他文書を評価・検証する立場にある
- テストや運用の具体的方法を含まない

---

## 4. 記載内容の制約

### 4.1 許可される内容（MUST / MAY）

- 概念・用語の定義
- 不変条件・制約条件
- 構造・関係性の宣言
- 他 spec への参照

### 4.2 禁止される内容（MUST NOT）

- テスト条件・検証観点
- 実装例・サンプルコード
- 手順書・操作説明
- TODO・メモ・履歴・差分理由

---

## 5. 他 document_type との関係

- index  
  - spec 群の一覧化・構造提示を担う
- template  
  - spec に基づく文書の構造骨格を定義する
- prompt  
  - spec に基づく生成・判断・検査を定義する

spec 自体は、生成や判断の方法を定義しない。

---

## 6. 更新・再生成ルール

- spec の更新は、**意味論の変更**を伴う。
- 更新時も `doc_id` は必ず維持する。
- spec の変更は、下位 document_type（template / prompt 等）への
  影響を考慮した上で行う。

---

## 7. LLM-MANAGED の扱い（spec 固有）

- `document_type` は常に `spec`
- `canonical_document` は原則 `true`
- `transport` は既定で `[true_out]`

---

## 8. 内部自己検査（非出力）

- 本文が宣言文主体であること
- テスト・運用・手順に関する記述が含まれていないこと
- 共通ドキュメント構造を満たしていること

---

[目次](../../../目次.md) > 仕様 > document_type > spec > spec 仕様
