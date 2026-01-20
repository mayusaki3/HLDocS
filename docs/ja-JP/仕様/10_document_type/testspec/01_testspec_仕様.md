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

本書は、HLDocS における **testspec（テスト仕様）** の役割・構造・規約を定義する。

---

## 1. 役割（MUST）

- testspec は **spec に従属**する検証仕様である。
- 各テストケースは、必ず対応する spec の章を参照する。
- testspec 自体は実装やテストコードを含まない。

---

## 2. 同一性と参照（MUST）

- テストケースの恒久的同一性は **sec_id** により保証される。
- テスト番号は **ラベル**であり、同一性を担保しない。
- spec 参照は `doc_id#sec_id` により行う。

---

## 3. テスト番号（ラベル）の扱い

### 3.1 目的

- 人間が一覧・ログ・CI 結果から把握しやすくするための表示用識別子。

### 3.2 フォーマット（推奨）

```
<TARGET>-<LEVEL>-<PURPOSE>-<NNN>
```

- `<TARGET>`：対象（人間可読・変更可）
  - UT/UI：実装・クラス等（例：COMMON_AUTH）
  - IT/E2E：機能・ユースケース（例：USER_REGISTER）
- `<LEVEL>`：UT / IT / E2E
- `<PURPOSE>`：SPEC（仕様検証） / IMPL（実装・カバレッジ目的）
- `<NNN>`：連番（リナンバー可）

### 3.3 禁止事項（MUST NOT）

- テスト番号を恒久キーとして扱ってはならない。
- 既存の sec_id を変更してはならない。

---

## 4. コードとの紐づけ（MUST）

- テストコード側には、**必ず**対応する testspec の `doc_id#sec_id` を記載する。
- 記載形式はコメント等とし、言語依存はしない。

（例：概念）

```text
@hldocs.ref doc-YYYYMMDD-HHMMSSZ-XXXX#tst_xxxxxxxx
@hldocs.label COMMON_AUTH-UT-SPEC-001
```

---

## 5. 構造要件（MUST）

- 各テストケースは章として記述する。
- 各章には sec_id を付与する。
- 参照先 spec を明示する。

---

[目次](../../../目次.md) > 仕様 > document_type > testspec > 仕様
