<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260120-120000Z-TSPC
lang: ja-JP
canonical_title: document_type:testspec 仕様
document_type: spec
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > 仕様 > document_type > testspec > 仕様

# document_type:testspec 仕様

本書は、HLDocS における **testspec（テスト仕様）** の役割・構造・参照規約を定義する。

---

## 1. 役割（MUST）

- testspec は **spec に従属**する検証仕様である。
- testspec は「何を、どの観点で検証するか」を定義する。
- testspec 自体は **実装コードやテストコードを含まない**。
- 実装・テストコードは testspec を参照する側である。

---

## 2. 同一性と参照（MUST）

### 2.1 検証単位の同一性

- 各テストケース（検証単位）の恒久的同一性は **sec_id** により保証される。
- sec_id は testspec において **初出・確定**する。
- sec_id は表示用ではなく、traceability を構成する検証単位キーである。

### 2.2 テスト番号との関係

- テスト番号は **ラベル**であり、同一性を担保しない。
- テスト番号は変更・再採番されてもよい。
- sec_id をテスト番号の代替として使用してはならない。

### 2.3 spec 参照

- testspec から spec への参照は **`doc_id#sec_id` のみ許可**する。
- 章名・章番号・テキスト位置等による参照は禁止する。

---

## 3. テスト番号（ラベル）の扱い

### 3.1 目的

- 人間が一覧・ログ・CI 結果から把握しやすくするための表示用識別子。
- testspec → testcode 生成時の構造整理補助として使用してよい。

### 3.2 基本フォーマット（推奨）

```
<TARGET>-<LEVEL>-<PURPOSE>-<NNN>
```

- `<TARGET>`：対象（人間可読・変更可）  
  - UT：実装・クラス等（例：COMMON_AUTH）  
  - IT / E2E：機能・ユースケース（例：USER_REGISTER）
- `<LEVEL>`：UT / IT / E2E
- `<PURPOSE>`：
  - SPEC：仕様検証目的
  - IMPL：実装・カバレッジ目的
- `<NNN>`：連番（変更・再採番可）

### 3.3 <NNN> の分割（MAY）

- testspec → testcode 生成時の都合により、`<NNN>` を **複数セグメントに分割してよい**。
- 分割後の各セグメントも **すべてラベル**であり、意味論的拘束や恒久性は持たない。
- 分割・再構成を理由に sec_id を変更してはならない。

#### 分割例（概念）

```
<TARGET>-<LEVEL>-<PURPOSE>-<AA>-<BB>-<CC>
```

- `<AA>`：分類（ラベル）
- `<BB>`：グループ（テストコード単位の整理用ラベル）
- `<CC>`：連番（ラベル）

※ `<AA> <BB> <CC>` の意味や桁数は testspec ごとに定めてよい。

### 3.4 禁止事項（MUST NOT）

- テスト番号（およびその分割セグメント）を恒久キーとして扱ってはならない。
- テスト番号を spec 参照や traceability の基準として使用してはならない。
- テスト番号の変更・再採番を理由に sec_id を変更してはならない。

---

## 4. sec_id（検証単位識別子）

### 4.1 役割

- sec_id は **検証単位の恒久識別子**である。
- testspec と spec を結び付ける唯一の検証キーである。

### 4.2 形式（MUST）

- sec_id は **`sec_<random>` 形式のみ許可**する。
- `<random>` は衝突確率が十分低い方式で生成されなければならない。
- 以下を含めてはならない：
  - 意味語・章名・番号
  - テスト番号
  - document_type・役割・用途を示す語
- `tst_` / `spc_` 等の接頭辞付き形式は禁止する。

### 4.3 管理原則（MUST）

- sec_id は testspec 側でのみ生成・確定する。
- spec 側で sec_id を新規生成してはならない。
- 一度確定した sec_id は変更してはならない。

---

## 5. testspec の構造要件（MUST）

- 各テストケースは **章（セクション）**として記述する。
- 各章には **必ず sec_id を付与**する。
- 各章には **対応する spec の参照**を明示する。

### 記載例（概念）

```
## ユーザー登録：正常系
<!-- hldocs:sec_id=sec_ab12cd34 -->
<!-- hldocs:ref=doc-YYYYMMDD-HHMMSSZ-XXXX#sec_ef56gh78 -->

### 前提条件
...

### 検証内容
...
```

---

## 6. コードとの紐づけ（MUST）

- テストコード側には、**必ず**対応する testspec の `doc_id#sec_id` を記載する。
- テスト番号は補助情報として併記してよい。
- 記載形式はコメント等とし、言語依存はしない。

### 記載例（概念）

```
@hldocs.ref doc-YYYYMMDD-HHMMSSZ-TSPC#sec_ab12cd34
@hldocs.label <TARGET>-<LEVEL>-<PURPOSE>-<...>
```

---

## 7. traceability に関する制約（要約・MUST）

- 検証トレーサビリティは **`doc_id#sec_id`** により表現する。
- sec_id は testspec 起点で確定し、spec 側はそれを受け取る。
- testspec で minutes / note 用の ref_id を生成してはならない。

---

## 8. LLM による内部自己検査（非出力・MUST）

- sec_id が `sec_<random>` 形式であること。
- 同一 testspec 文書内で sec_id が重複していないこと。
- spec 参照がすべて `doc_id#sec_id` 形式であること。
- テスト番号（および分割セグメント）が同一性判定に使用されていないこと。

---

[目次](../../../目次.md) > 仕様 > document_type > testspec > 仕様
