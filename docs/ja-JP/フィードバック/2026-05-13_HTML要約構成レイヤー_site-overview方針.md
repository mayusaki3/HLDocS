目次 > フィードバック > HTML要約構成レイヤー > site-overview方針

# HTML要約構成レイヤー site-overview方針

## 1. 位置付け

本書は、HLDocS の HTML ドキュメント生成における要約構成レイヤーのうち、トップページ相当となる `site-overview` の方針を記録する。

本書は正規仕様ではなく、HTML生成PoCの改善方針を整理するフィードバック文書として扱う。

---

## 2. 背景

単純な Markdown → HTML 変換では、Markdown 正本とほぼ同等の情報しか得られない。

しかし、HTMLドキュメントの当初目的は、単なる文書閲覧ではなく、以下を支援することである。

- 全体像の把握
- 構成理解
- 入門導線
- 用途別 navigation
- 仕様群の関係理解
- 詳細文書への誘導

そのため、HTML生成では用途ごとに標準的な要約構成レイヤーを定義し、その情報をもとにHTML化する方針とする。

---

## 3. 基本方針

最初に定義する要約構成レイヤーは、トップページ相当の `site-overview` とする。

`site-overview` は、HTMLドキュメント全体の入口であり、以下の役割を持つ。

- ドキュメント群の全体像を示す
- 利用者が最初に読むべき内容を示す
- 主要なインデックスへ誘導する
- 全体イメージを視覚的に示す
- Markdown 正本とは異なる、人間向け理解レイヤーを提供する

---

## 4. site-overview の標準構成

`site-overview` は、少なくとも以下の要素を持つ想定とする。

### 4.1 タイトル

HTMLドキュメント全体のタイトル。

例：

```text
HLDocS HTMLドキュメント
```

---

### 4.2 全体イメージ画像

ドキュメント群全体のイメージを表す画像。

画像は、以下の優先順位で扱う。

1. Markdown 正本側に明示された画像を使用する
2. 要約構成レイヤーに指定された画像を使用する
3. 画像指定がない場合は、自動生成候補として扱う
4. 自動生成しない場合は、画像なしまたは placeholder とする

固定化すべき画像は、Markdown 正本側の情報として管理するのが望ましい。

LLMまたは生成ツールが自動生成した画像は、generated artifact として扱い、Markdown 正本とはみなさない。

---

### 4.3 全体像の説明

ドキュメント群の目的、対象、使い方を短く説明する。

この説明は、Markdown 正本群から作成される要約であり、Markdown 正本を置き換えない。

想定内容：

- このドキュメント群が何を説明するか
- 誰が読む想定か
- どの順番で読むとよいか
- どの情報が正本か
- HTMLは generated operational representation であること

---

### 4.4 インデックス領域

利用者が詳細情報へ進むためのインデックスを配置する。

どのインデックスを用意するかは次ステップで整理する。

初期候補：

- ドキュメント一覧
- 目的別インデックス
- document_type別インデックス
- 入門用インデックス
- 仕様カテゴリ別インデックス
- 生成フェーズ別インデックス
- Traceabilityインデックス
- 検査成績表インデックス
- 更新・staleインデックス

---

### 4.5 not generated 表示

現在生成されていないHTML領域を明示する。

例：

```text
Traceability: not generated
Test Report: not generated
```

未生成領域へのリンクは作成しない。

---

### 4.6 Markdown 正本への案内

HTMLドキュメントが正本ではないことを明示し、必要に応じてMarkdown正本へ誘導する。

---

## 5. site-overview の想定データ構造

初期案として、要約構成レイヤーに以下のような情報を持たせる。

```json
{
  "type": "site-overview",
  "title": "HLDocS HTMLドキュメント",
  "hero_image": {
    "mode": "source | generated | placeholder | none",
    "source": null,
    "alt": "HLDocSの全体像"
  },
  "summary": {
    "purpose": "...",
    "audience": "...",
    "reading_guide": "...",
    "canonical_notice": "..."
  },
  "indexes": [],
  "not_generated": [
    "traceability",
    "test-report"
  ]
}
```

---

## 6. 画像の扱い

全体イメージ画像は、HTMLの見た目だけではなく、利用者がドキュメント群の目的を直感的に理解するための情報とする。

ただし、画像の扱いには以下の区別が必要である。

### 6.1 正本由来画像

Markdown 正本側で指定された画像。

この場合、画像は正本に紐づく情報として扱う。

### 6.2 要約構成レイヤー指定画像

要約構成レイヤーで指定された画像。

この場合、HTML用 operational input として扱う。

### 6.3 自動生成画像

LLMまたは画像生成ツールで生成した画像。

この場合、generated artifact として扱い、Markdown 正本とはみなさない。

### 6.4 placeholder

画像が未定義の場合の仮表示。

---

## 7. HTML tool の責務

HTML生成 tool は、`site-overview` の構造情報を受け取り、HTMLトップページを機械的に生成する。

HTML生成 tool は、説明文や画像の意味を推測生成しない。

`site-overview` が存在しない場合に限り、Markdown 正本群から最小限の overview を自動抽出してよい。

これは現行PoCの挙動と一致する。

---

## 8. LLM の責務

LLM は、必要に応じて Markdown 正本群から `site-overview` を作成する。

LLM が担当してよいもの：

- 全体像説明の要約
- 読み順の提案
- インデックス候補の整理
- 画像生成方針の提案
- not generated 項目の整理

LLM が担当してはならないもの：

- Markdown 正本にない仕様内容の確定
- 実在しないリンクの生成
- 正本画像としての自動生成画像の扱い
- 未生成ページへのリンク生成

---

## 9. 現行PoCへの反映方針

次のPoC改善では、まず以下を行う。

1. `summary-structure/site-overview.json` を任意入力として扱う
2. 存在する場合は `overview/index.html` と `index.html` の生成に使用する
3. 存在しない場合は現行どおり Markdown から最小 overview を生成する
4. 画像は placeholder から開始する
5. インデックス詳細は次ステップで整理する

---

## 10. 次ステップ

次に整理する対象は、`site-overview` に配置するインデックス種別である。

検討候補：

- 全文書インデックス
- 目的別インデックス
- document_type別インデックス
- 仕様カテゴリ別インデックス
- 入門インデックス
- 生成フローインデックス
- Traceabilityインデックス
- 検査成績表インデックス

---

目次 > フィードバック > HTML要約構成レイヤー > site-overview方針
