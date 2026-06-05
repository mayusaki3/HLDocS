# HLDocS Worklog

## 作業名

HLDocS v0.6.0-preview 要件整理

## 状態

要件確定

実装未着手

---

## 目的

v0.5.0-preview の実運用で発生した問題を反映し、

* ドキュメント参照品質向上
* コード生成品質向上
* GitHub運用強化
* チャット移行容易化
* 技術検証運用対応

を実施する。

---

## v0.6.0-preview テーマ

継続作業性の強化
(Long-Term LLM Workflow Support)

---

## 決定事項

### 新規仕様追加

追加予定

* 12_ドキュメント参照・ナビゲーション規約.md
* 13_ソースコード生成運用規約.md
* 14_LLM_WORKSPACE規約.md

---

### ドキュメント参照・ナビゲーション規約

追加理由

リンク誤生成の抑止

例

NG

```markdown
[01_前提条件](./01_前提条件.md)
```

OK

```markdown
[前提条件](./01_前提条件.md)
```

---

#### 論理ナビゲーション構造

決定事項

物理構造と論理構造は別概念とする。

```text
物理構造
≠
論理構造
```

---

例

物理構造

```text
30_検証
├─検証目次.md
├─01_検証1.md
└─02_検証2.md
```

論理構造

```text
目次
└─検証目次
   ├─検証1
   └─検証2
```

---

階層リンク生成規則

優先順位

1. 明示指定された階層リンク
2. 同階層文書の階層リンク
3. 同ディレクトリの目次文書
4. 利用者提示のフォルダ構成
5. FAIL-FAST

---

禁止事項

以下から論理構造を推測してはならない。

* フォルダ名
* 管理番号
* ファイル名
* ディレクトリ深さ

---

### ソースコード生成運用規約

目的

記憶ベース修正禁止

---

コード修正時優先順位

1. GitHub直接更新
2. ZIP等で提供
3. チャットで全文提供
4. 編集指示

---

修正対象取得優先順位

1. GitHub正本
2. 添付ファイル
3. チャット貼付

---

禁止事項

* 記憶ベース修正
* 推測による修正
* 未提示正本への編集指示
* 部分コードからの全文推測

---

FAIL-FAST

正本未取得

---

### LLM_WORKSPACE規約

標準構成

```text
LLM_WORKSPACE
├─Handover
├─Request
└─Worklog
```

---

定義

Request

未処理要求

Worklog

作業状態の正本

Handover

Worklogから生成される派生成果物

---

ライフサイクル

```text
Request
 ↓
Worklog
 ↓
Handover
```

---

チャット移行時参照順

1. Worklog
2. Handover
3. Request

---

矛盾時

Worklogを正本とする。

---

### GitHub運用強化

生成プロンプト運用規約へ追加

GitHub利用が想定される場合

作業開始前にアクセス確認を行う。

アクセス失敗時は

一時的制限の可能性を考慮する。

利用不可と断定しない。

---

### 技術検証運用

note仕様へ追加

通常運用

```text
spec
 ↓
code
 ↓
testspec
 ↓
test
```

技術検証

```text
note
 ↓
code
 ↓
結果取得
 ↓
note更新
```

---

### README多言語対応

README.md

```markdown
[日本語](./README.md) | [English](./README_en-US.md)
```

README_en-US.md 新規作成

---

目次リンク

```markdown
- [HLDocS Table of Contents](./docs/ja-JP/目次.md) (Japanese)
```

---

### VERSION

更新予定

```text
v0.6.0-preview
```

---

## 次工程

実施予定

1. VERSION更新
2. README.md更新
3. README_en-US.md作成
4. v0_6_0-preview.md作成
5. 12_ドキュメント参照・ナビゲーション規約.md作成
6. 13_ソースコード生成運用規約.md作成
7. 14_LLM_WORKSPACE規約.md作成
8. 02_生成プロンプト運用規約改訂
9. 01_note_仕様改訂
10. 目次更新

---

## 保留事項

なし

v0.6.0-preview 要件は確定。
