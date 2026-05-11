<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260110-010000Z-UI01
lang: ja-JP
canonical_title: ChatGPT UIでの使い方
document_type: note
canonical_document: true
-->

[目次](../目次.md) > 使い方 > ChatGPT UIでの使い方

# ChatGPT UIでの使い方

本書は、HLDocS 規約に基づくドキュメント生成・再作成を  
**ChatGPT の UI 上で人間が安定して実行するための操作手順書**である。

テンプレートや生成プロンプト自体の仕様ではなく、  
「どのファイルを、どの順で添付し、どのような指示を書くか」を明示する。

---

## 現時点の推奨運用（Preview Release）

HLDocS は現在、Preview Release（v0.x 系）として公開されている。

現時点では、共通テンプレート・共通生成プロンプトのみでの  
完全自己完結生成は未完成である。

そのため、現在は以下を推奨する。

1. `docs/ja-JP/仕様` を LLM に提示する
2. 共通生成プロンプト・共通テンプレートを利用する
3. document_type 別テンプレート・生成プロンプトを利用する
4. HLDocS 規約に従って生成・検証・再構成を行う

現時点では、以下の URL を ChatGPT に提示することで、  
添付を行わずに HLDocS 仕様を参照させることが可能。

```text
HLDocS仕様
https://github.com/mayusaki3/HLDocS/tree/main/docs/ja-JP/仕様
```

将来的には、prompt/template のみで成立する構成を目標としている。

---

## 1. 本書の位置付け（人間向け）

- 本書は **人間の操作を支援するための UI 手順書**である
- 規約（spec）や生成プロンプトでは扱わない
  - 操作順
  - 判断ポイント
  - 典型的なミス回避
  を明文化する
- 正確な構文よりも **迷わず再現できること**を優先する

---

## 2. document_type をどう選ぶか（操作前に確認）

指示を書く前に、**何を作りたいのか**を明確にする。

- spec  
  要件・振る舞い・I/F を確定させる仕様書
- testspec  
  spec を検証するためのテスト観点・期待結果
- usage  
  利用者向けの使い方・操作説明
- minutes  
  議論・検討・意思決定の記録（後から spec を作成する元情報）
- note  
  方針・補足・運用知見・検討途中の整理
- index  
  目次・リンク集
- template / prompt  
  LLM に渡すための入力定義（テンプレート・生成指示）

※ document_type は **役割分類**であり、論理同一性（doc_id）とは別である。

---

## 3. 推奨される基本フロー（最重要）

### 手順 1：新しいチャットを開始する

原則として **1 文書 = 1 チャット**。

次のような挙動が出た場合は、  
同じチャットを続けるより **新しいチャットへ移動することを推奨**する。

- 指示していない document_type が選ばれる
- transport 指定が無視される
- 再作成なのに doc_id が変更される
- 「ui_copy ではできない」等を理由に内容が省略される
- 説明文のみが返り、生成に入らない

---

## 4. ケース別「添付セット＋指示文」

以下は **実際にそのまま使用できる完成形**である。  
ファイルを添付した後、指示文を貼り付ける。

---

### A. 新規作成（単独 document_type）

対象 document_type：
- note
- index
- template
- prompt

※ spec / testspec / usage は、他 document_type との関係性を持つことが多いため  
　ここでは単独ケースとして分けて扱う。

**添付するもの**

- 共通ドキュメントテンプレート（必須）
- 共通ドキュメント生成プロンプト（必須）
- 対象 document_type のテンプレート
- 対象 document_type の生成プロンプト

（以下既存内容維持）

---

[目次](../目次.md) > 使い方 > ChatGPT UIでの使い方
