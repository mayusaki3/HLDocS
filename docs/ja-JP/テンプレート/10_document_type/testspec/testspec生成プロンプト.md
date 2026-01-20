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

---

## 0. 最上位命令（MUST）

- document_type は **testspec 固定**。
- spec に従属し、spec 参照のないテストケースを生成してはならない。
- 出力は **最終成果物のみ**。

---

## 1. 生成規則（MUST）

- 各テストケースは章として生成する。
- 各章に sec_id を付与する。
- spec 参照（doc_id#sec_id）を必ず含める。

---

## 2. テスト番号の扱い

- テスト番号は **ラベル**であり、同一性を担保しない。
- 既存のテスト番号がある場合は変更しない。
- リナンバーを目的としない限り、新規採番は最小限にする。

---

## 3. 禁止事項（MUST NOT）

- 実装方法・コードの記述
- テスト実行手順の詳細化
- spec の再解釈・拡張

---

## 4. 内部自己検査（非出力）

- spec 参照が欠けていないか
- sec_id を勝手に変更していないか
- テスト番号を恒久キーとして扱っていないか

---

[目次](../../../目次.md) > テンプレート > document_type > testspec > 生成プロンプト
