<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260120-000100Z-SPCP
lang: ja-JP
canonical_title: document_type:spec 生成プロンプト
document_type: prompt
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > テンプレート > document_type > spec > 生成プロンプト

# document_type:spec 生成プロンプト

本プロンプトは、HLDocS における `document_type: spec` を生成・更新する際の  
**判断規則および自己検査条件**を定義する。

---

## 0. 最上位命令（MUST）

- document_type は **spec 固定**とする。
- 仕様対象・範囲が未合意の場合、生成してはならない。
- 出力は **最終成果物のみ**とする。

---

## 1. 生成判断規則（MUST）

- spec は **宣言文**として記述する。
- 「何が正か」を定義し、「どう行うか」を書いてはならない。
- 説明・背景・例示は最小限に留める。

---

## 2. 禁止事項（MUST NOT）

- テスト条件・検証観点の記述
- 実装方法・運用手順の説明
- TODO・メモ・作業指示文
- 生成方法・編集手順の説明

---

## 2.x Traceability 記法（任意・形式定義）

本プロンプトは、Traceability 規約に基づく記法を  
**「任意機能」かつ「形式定義のみ」**として扱う。

ユーザー指示、または入力文書内に既存の Traceability 記法が存在する場合に限り、  
以下の形式を使用してよい。

### sec_id（章単位ID）

- 章見出し直下に **HTML コメント**として記載する
- 形式：`<!-- hldocs:sec_id=<sec_id> -->`
- sec_id の付与は必須ではない
- 既存の sec_id は **変更してはならない**
- 新規 sec_id は、ユーザー指示がある場合にのみ付与してよい

### ref（章単位参照）

- 参照識別子の形式：`doc_id#sec_id`
- 人間向け参照として Markdown の相対パスリンクを使用してよい
- 機械向け情報として、リンク直後に HTML コメントで ref を記載してよい
- 形式：`<!-- hldocs:ref=<doc_id>#<sec_id> -->`

（例）

- [章タイトル](./path/to/doc.md)  
  <!-- hldocs:ref=doc-YYYYMMDD-HHMMSSZ-XXXX#abc123 -->

---

## 3. LLM-MANAGED 値決定規則（MUST）

- `doc_id`
  - 新規生成時のみ生成する
  - 更新時は既存値を必ず維持する
- `document_type` : `spec`
- `canonical_document` : `true`
- `transport` : `[true_out]`

---

## 4. 内部自己検査（非出力・MUST）

- 本文が宣言文主体であること
- 禁止事項が含まれていないこと
- 共通ドキュメント構造を満たすこと
- sec_id / ref を **勝手に追加・変更していないこと**

---

[目次](../../../目次.md) > テンプレート > document_type > spec > 生成プロンプト
