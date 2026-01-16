<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260115-010020Z-E5F6
lang: ja-JP
canonical_title: Transport Encoding 規約
document_type: spec
canonical_document: true
transport: [true_out]
-->

[目次](../../目次.md) > 仕様 > 共通 > Transport Encoding 規約

# Transport Encoding 規約

本書は、LLM が提供する UI 上で **安全に提示・回収**できる形でドキュメントを扱うための  
**Transport Encoding（搬送・提示方式）** を定義する。

本規約は、ドキュメントの内容・意味・正規性を規定するものではなく、  
**UI や回収手段の制約下で「どう提示するか」だけを定義**する。

---

## 1. 背景（Why）

### 1.1 何が問題か（Problem）
- UI 上でのコピー・貼り付け時に、Markdown が意図せず変形・欠落し、  
  正規成果物（canonical-md）の回収に失敗することがある。
- 特に、コードブロック・引用・箇条書きが混在する文書では、  
  UI の都合で構造が崩れる可能性が高い。

### 1.2 なぜ起きるか（Cause）
- UI は Markdown を「文字列」ではなく「レンダリング結果」として扱う局面がある。
- フェンス記号やインデントが UI 側で再解釈され、  
  **元のプレーンな Markdown が保持されない**場合がある。
- 長文では、セッション切れや部分コピーによる回収失敗も起こり得る。

### 1.3 何が必要か（Requirement）
- UI 上で **1つの回収単位**として扱える提示方式
- 正規成果物と提示用表現を明確に分離する仕組み
- 復元可能（roundtrip）であること

### 1.4 どう解決するか（Approach）
- 正規成果物は canonical な内容として保持する。
- UI 制約がある場合のみ Transport Encoding を適用した提示を行う。
- 回収後は提示用表現を復元し、正規内容として保存する。

---

## 2. 定義

- Transport Encoding は **提示・回収のための表現上の取り決め**である。
- Transport Encoding は **ドキュメントの意味・構造・正規性を変更しない**。
- Transport Encoding は復元可能（roundtrip）でなければならない。

---

## 3. canonical_document との関係（重要）

- `canonical_document` は **ドキュメントの立ち位置（正規成果物か否か）**を示す。
- Transport Encoding は **canonical_document と直交する**。

---

## 4. transport の評価モデル（MUST）

### 4.1 基本ルール
- `transport` は **配列で指定**する。
- **先頭に指定されたものが最優先**。
- LLM は先頭から順に適用可能性を評価し、最初に適用可能な方式で出力する。

### 4.2 transport タグ一覧

### transport = true_out
**意味**
- Transport Encoding を適用せず、**正味の内容をそのまま提示**する。

**LLM の動作**
- canonical な Markdown を変換せず出力する。
- UI 崩壊対策の整形やエスケープは行わない。

### transport = ui_copy
**意味**
- UI 上での表示・コピーが安定するよう **提示用の整形を行う**。

**LLM の動作**
- UI で崩れやすい表現を考慮した提示を行う。
- コードフェンス等、UI が破壊しやすい要素については、
  **ui_copy の責務として回避・代替してよい**（roundtrip を前提とする）。
- 意味・構造の変更は禁止。

### transport = download
**意味**
- UI コピーを前提とせず、**ファイルとして回収**する。

**LLM の動作**
- Transport Encoding を適用せず、正規内容を成果物として生成する。
- zip や単体ファイル等、回収可能な形式を提供する。

---

## 5. 既定（Default）ルール（SHOULD）

### canonical_document = true
- 既定 transport: `[download, true_out]`
- UI 提示が必要な場合：`[download, ui_copy]`

### canonical_document = false
- 既定 transport: `[ui_copy]`
- ファイル回収も必要な場合：
  - UI 優先：`[ui_copy, download]`
  - 回収優先：`[download, ui_copy]`

---

## 6. 禁止事項（MUST NOT）

- Transport Encoding により、ドキュメントの意味や構造を変更してはならない。
- transport の指定だけで canonical_document の意味を上書きしてはならない。
- 提示用表現を正規成果物として保存してはならない。

---

[目次](../../目次.md) > 仕様 > 共通 > Transport Encoding 規約
