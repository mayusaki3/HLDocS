<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260120-010000Z-TRC1
lang: ja-JP
canonical_title: Traceability（仕様・テスト・コード紐づけ）規約
document_type: spec
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../目次.md) > 仕様 > 共通 > Traceability規約

# Traceability（仕様・テスト・コード紐づけ）規約

本書は、HLDocS において  
**仕様（spec）・テスト仕様（testspec）・ソースコード間の対応関係**を、  
恒久的かつ再構成可能な形で管理するための **Traceability 規約**を定義する。

本規約は、以下の共通仕様を前提として成立する。

- 前提条件
- 共通ドキュメント構造
- LLM-MANAGEDブロック規約
- Transport Encoding 規約
- 生成プロンプト運用規約

---

## 1. Purpose（目的）

- 仕様・テスト・実装間の対応関係を **恒久的に識別**可能にする  
- ファイル名・章名・番号変更に影響されない **安定した紐づけ**を提供する  
- 人間および LLM が **同一の識別子体系**で検証可能にする  

---

## 2. Scope / Non-goals

### 2.1 Scope

- spec / testspec / code 間の対応関係定義  
- 章・検証単位レベルでの参照方式  
- LLM による整合性検査の前提定義  

### 2.2 Non-goals

- テスト設計手法そのものの定義  
- 自動生成・自動修正の実装  
- 採番アルゴリズムの詳細規定  

---

## 3. 基本原則（MUST）

- **文書単位の同一性**は `doc_id` のみによって保証される  
- **検証単位の同一性**は `sec_id` によって表現される  
- 一意性は **(doc_id, sec_id)** の組で成立する  
- 意味語・構造情報と識別子を混在させてはならない  

---

## 4. sec_id（検証単位識別子）

### 4.1 定義

`sec_id` は、仕様要求・振る舞い・検証観点を識別する  
**検証単位識別子**である。

`sec_id` 単体では一意性を持たず、  
`doc_id` と組み合わせることで初めて一意となる。

---

### 4.2 形式（MUST）

- `sec_id` は **sec_<random> 形式のみ許可**する  
- `<random>` は衝突確率が十分低い方式で生成されなければならない  
- 以下を **含めてはならない（MUST NOT）**
  - 意味語・章名・番号
  - テスト番号
  - document_type・役割・用途を示す語
- spc_ / tst_ 等の **接頭辞付き形式は禁止**する  

---

### 4.3 確定原則（MUST）

- `sec_id` は **testspec を起点として初出・確定**する  
- spec 単体生成時に `sec_id` を付与してはならない  
- 対応する testspec を持たない `sec_id` を定義してはならない  

---

### 4.4 役割分担（MUST）

- **testspec**
  - 検証観点単位で `sec_id` を初出・確定する主体
- **spec**
  - testspec 側で確定した `sec_id` を後追いで受け取る主体
  - 推測・自動生成により `sec_id` を付与してはならない

---

### 4.5 許可・禁止事項

**許可**

- testspec 新規作成時の `sec_id` 付与  
- 規格外 testspec を HLDocS 準拠に再構成する際の `sec_id` 付与  

**禁止**

- spec 生成時の自律的 `sec_id` 生成  
- traceability 以外の目的での `sec_id` 利用  

---

## 5. sec_id の記載方法（MUST）

### 5.1 記載形式

`sec_id` は、対象章見出し直下に **HTML コメント**として記載する。

```
## <章タイトル>
<!-- hldocs:sec_id=sec_<random> -->
```

### 5.2 制約

- 一度確定した `sec_id` は変更してはならない  
- 同一文書内で重複してはならない  
- 人間可読性は要求しない  

---

## 6. 章単位参照形式（MUST）

章・検証単位の参照は、以下の形式 **のみ許可**する。

```
doc_id#sec_id
```

章名・番号・位置情報等を含む参照形式は  
**生成・使用してはならない**。

---

## 7. 人間向けリンクと機械参照の分離（MUST）

- 人間向けナビゲーションは Markdown リンクで行う  
- 機械的同一性は HTML コメントで保持する  

```
- [章タイトル](../../path/to/doc.md)
  <!-- hldocs:ref=doc-XXXXXXXX-XXXX#sec_<random> -->
```

---

## 8. ソースコード側の参照

### 8.1 記載形式

```
@hldocs.ref doc-XXXXXXXX-XXXX#sec_<random>
```

### 8.2 制約

- 複数指定可  
- 順序は問わない  
- 言語固有のコメント規約に従う  

---

## 9. 再構成・移行時の補足規定（MAY）

- traceability 再構築目的に限り、既存 `sec_id` を一旦除去し再付与してよい  
- 恒久成果物公開前に再付与は完了していなければならない  

---

## 10. LLM による整合性検査

### 許可（MUST）

- `doc_id#sec_id` の存在確認  
- spec / testspec / code 間の対応確認  
- 未参照・孤立検証単位の検出  

### 禁止（MUST NOT）

- `sec_id` の新規生成・変更  
- 本文・コメントの自動修正  
- 規定外参照形式の生成  

---

## 11. 内部自己検査（非出力・MUST）

- `sec_id` が sec_<random> 形式であること  
- (doc_id, sec_id) で一意性が成立していること  
- 参照形式が doc_id#sec_id のみであること  

---

## 12. minutes / note ⇔ spec の派生トレーサビリティ（MAY）

### 12.1 目的と位置付け

本節は、**spec の記述が minutes / note のどの記述を根拠として導出されたか**を  
追跡可能にするための **派生（derivation）トレーサビリティ**を定義する。

本トレーサビリティは：

- **検証関係ではない**
- spec ⇔ testspec の必須トレーサビリティを **代替しない**
- spec 確定前後の段階で、根拠の追跡・説明責務を支える目的で使用する

---

### 12.2 対象 document_type

- minutes
- note

---

### 12.3 ref_id（根拠アンカー識別子）

#### 12.3.1 定義

`ref_id` は、minutes / note 内の **根拠となる記述位置**を識別するための  
**根拠アンカー識別子**である。

`ref_id` は検証単位ではなく、`sec_id` の代替ではない。

#### 12.3.2 形式（MUST）

- `ref_id` は **ref_<random> 形式のみ許可**する  
- `<random>` は衝突確率が十分低い方式で生成されなければならない  
- `ref_id` に意味語・章名・番号・用途語を含めてはならない（MUST NOT）

#### 12.3.3 一意性

- 一意性は **(doc_id, ref_id)** の組で成立する  
- `ref_id` 単体のグローバル一意性は要求しない  

---

### 12.4 ref_id の付与タイミング（MUST）

- `ref_id` は、minutes / note 作成時点で必須ではない  
- `ref_id` は、minutes / note を根拠として **spec を作成（派生を確定）する工程**において、  
  根拠として採用した minutes / note の該当箇所へ **後付けで付与してよい**  
- 既に存在する `ref_id` は変更してはならない（MUST NOT）

---

### 12.5 minutes / note 側の記載形式（MUST）

minutes / note の根拠箇所（見出し直下、または箇条書き直下等）に  
HTML コメントとして付与する。

```
<!-- hldocs:ref_id=ref_<random> -->
```

---

### 12.6 spec 側からの参照形式（MUST）

minutes / note の根拠箇所を参照する場合、以下の形式のみ許可する。

- `doc_id#ref_id`

`sec_id` は本用途で使用してはならない（MUST NOT）。

---

### 12.7 hldocs:rel（関係種別）

#### 12.7.1 定義（MUST）

spec 側で minutes / note を参照する場合、参照コメントには必ず `hldocs:rel` を付与する。

#### 12.7.2 許容値（MUST）

- `rationale`：判断理由・背景・採用理由（根拠）として参照する
- `derivation`：参照元記述の内容を仕様として取り込んだ（仕様化した）ことを示す

#### 12.7.3 付与判断（MUST）

`ref_id` を生成・付与する工程において、LLM は参照の性質を判断し、  
以下に従って `hldocs:rel` を決定しなければならない。

- spec の内容が参照元記述の内容から **直接仕様化された**場合：`derivation`
- 参照元記述が spec の判断理由・背景説明として **用いられたのみ**の場合：`rationale`

---

### 12.8 機械参照の記載形式（MAY）

spec 側の該当箇所に対し、HTML コメントとして参照を付与してよい。

- `hldocs:ref` は参照先（minutes / note）を表す  
- `hldocs:rel` は関係種別を表す（必須）

#### 記載例（spec → minutes / note）

```
<!-- hldocs:ref=doc-YYYYMMDD-HHMMSSZ-XXXX#ref_ab12cd34 hldocs:rel=derivation -->
```

---

### 12.9 制約（MUST / MUST NOT）

- 本派生トレーサビリティは **根拠の追跡目的に限定**する  
- 検証完了を意味してはならない  
- testspec 作成前に存在してよい  
- spec ⇔ testspec の検証トレーサビリティと混同してはならない  
- minutes / note 側で `sec_id` を新設してはならない（MUST NOT）  
- minutes / note 側で検証単位を表す意図の識別子を生成してはならない（MUST NOT）

---

[目次](../../目次.md) > 仕様 > 共通 > Traceability規約
