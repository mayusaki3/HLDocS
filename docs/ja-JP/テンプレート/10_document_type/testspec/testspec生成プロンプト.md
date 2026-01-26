<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260120-120500Z-TSPP
lang: ja-JP
canonical_title: document_type:testspec 生成プロンプト
document_type: prompt
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > テンプレート > document_type > testspec > 生成プロンプト

# document_type:testspec 生成プロンプト

本プロンプトは、HLDocS 規約に準拠した **testspec（テスト仕様）** を生成するための  
**正規かつ唯一の生成プロンプト**である。  
本プロンプトは testspec 固有の生成規則のみを定義し、  
Traceability 規約・共通生成規約の内容を **再定義・上書きしない**。

---

## 0. 最上位命令（MUST）

- document_type は **testspec 固定**。
- testspec は **必ず spec に従属**する。
- spec が添付・参照されていない場合、testspec を生成してはならない。
- 出力は **完成した testspec 本文のみ**とする。
- 編集指示・理由・補足・差分・要約を出力してはならない。
- 出力（提示）は **ui_copy 方式**で行う。

---

## 1. testspec の役割（MUST）

- testspec は **検証観点の定義文書**である。
- testspec は以下を記述する。
  - 何を検証するか
  - どの条件で検証するか
  - 何をもって合格とするか
- 実装方法・テストコード・実行手順は記述してはならない。

---

## 2. sec_id の扱い（MUST）

### 2.1 基本原則

- sec_id は **検証単位識別子**である。
- sec_id は **testspec を起点として初出・確定**する。
- spec は testspec により確定した sec_id を **参照する側**である。

### 2.2 付与規則

- 各テストケース（章）には **必ず 1 つの sec_id を付与**する。
- sec_id は **`sec_<random>` 形式のみ許可**する。
- `<random>` 部分は衝突確率が十分低い方式を用いる。
- sec_id に以下を含めてはならない。
  - 意味語
  - 章名
  - 番号
  - テスト番号
  - 役割・用途・document_type を示す語
- `tst_` / `spc_` 等の prefix 使用は禁止。

### 2.3 再作成時の扱い

- 既存 testspec に sec_id が存在する場合、**変更してはならない**。
- 再構成・整形・文章修正を理由に sec_id を再生成してはならない。

---

## 3. spec 参照（MUST）

- testspec から spec への参照は **以下の形式のみ許可**する。

```
doc_id#sec_id
```

- 章名・章番号・位置・文脈説明による参照は禁止。
- spec 側の sec_id を **推測・新規生成してはならない**。

---

## 4. テスト番号（ラベル）（MAY）

### 4.1 位置付け

- テスト番号は **人間向け管理ラベル**であり、恒久識別子ではない。
- 同一性・トレーサビリティ判定に使用してはならない。
- 変更・再採番してよい。

### 4.2 基本フォーマット（推奨）

```
<TARGET>-<LEVEL>-<PURPOSE>-<NNN>
```

- `<TARGET>`：対象（人間可読）
- `<LEVEL>`：UT / IT / E2E
- `<PURPOSE>`：SPEC / IMPL
- `<NNN>`：連番（変更可）

### 4.3 分割（MAY）

- testspec → testcode 生成時の都合により `<NNN>` を分割してよい。
- 分割後の各要素も **すべてラベル**であり、意味論的拘束は持たない。
- 分割・再構成を理由に sec_id を変更してはならない。

---

## 5. 構造要件（MUST）

- 各テストケースは **章（見出し）単位**で記述する。
- 各章の見出し直下に sec_id を **HTML コメントで明示**する。
- 各章に **対応する spec 参照（doc_id#sec_id）を明示**する。

---

## 6. 記述内容（MUST）

各テストケースには、少なくとも以下を含める。

- 前提条件
- 入力／操作（抽象レベル）
- 期待結果（観測可能な振る舞い）

---

## 7. 禁止事項（MUST NOT）

- sec_id の再利用・再定義・変更
- sec_id をテスト番号・進捗管理・装飾目的で使用すること
- minutes / note 用の ref_id を生成・記載すること
- spec 内容の補完・解釈・拡張

---

## 8. 内部自己検査（非出力・MUST）

出力前に以下を内部で必ず検査せよ（本文に出力しない）。

- spec が添付・参照されている
- 各テストケースに sec_id が付与されている
- sec_id が `sec_<random>` 形式である
- spec 参照がすべて `doc_id#sec_id` 形式である
- テスト番号を同一性判定に使用していない

---

以上を満たす **testspec の完成本文のみ**を出力せよ。

---

[目次](../../../目次.md) > テンプレート > document_type > testspec > 生成プロンプト
