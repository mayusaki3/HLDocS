<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-030020Z-USG3
lang: ja-JP
canonical_title: usage 生成プロンプト
document_type: prompt
canonical_document: true
transport: [true_out]
-->

[目次](../../../目次.md) > テンプレート > document_type > usage > 生成プロンプト

# usage 生成プロンプト

## 最上位命令（MUST）
- document_type は **usage** とする。
- 合意された **usage テンプレート**を必ず使用し、**構造を変更してはならない**。
- 出力は **最終成果物のみ**。思考過程・説明・差分は出力してはならない。

## 内容制約（MUST / MUST NOT）
- 記述してよい内容：**操作手順・順序・注意事項・前提条件**のみ。
- **MUST NOT**：仕様定義、設計意図、背景説明、検証観点、推測・補完・類推。
- 他 document_type（spec / minutes / note）を**要約・代替してはならない**。

## LLM-MANAGED 規則（MUST）
- 新規作成時は doc_id を新規発行。
- transport の既定は [true_out]。
- UIコピーが指定された場合のみ [ui_copy] を使用。

## ui_copy 規則（適用時・MUST）
- 出力は **単一のコードブロックのみ**。
- コードブロック外に文字列を出力してはならない。
- **等価変換のみ許可**。削除・要約・文章化・意味改変は **MUST NOT**。

## 内部自己検査（非出力・MUST）
- テンプレート構造保持
- 禁止事項の非混入
- transport 規則遵守（ui_copy時）
- 規約文・作業指示の本文非混入

---

[目次](../../../目次.md) > テンプレート > document_type > usage > 生成プロンプト
