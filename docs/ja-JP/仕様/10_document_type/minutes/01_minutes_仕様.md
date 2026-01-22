<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-000030Z-M1N1
lang: ja-JP
canonical_title: document_type:minutes 仕様
document_type: spec
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > 仕様 > document_type > minutes > 仕様

# document_type:minutes 仕様

## 1. Purpose（存在理由）

`minutes` は、ディスカッション・会議・設計検討等の **事実記録** を残すための document_type である。  
正しさを宣言するものではなく、**「何が話され、何が合意・未決だったか」** を保存することを目的とする。

## 2. Scope（対象）

- 会議・議論の記録
- 合意事項・結論の記録
- 未決事項・次アクションの記録
- 日時・期間・参加者の記録（可能な範囲）

## 3. Non-goals（対象外）

- 合意済み仕様・規約の宣言（= spec）
- テスト条件・期待結果の定義（= testspec）
- 生成規則・判断規則の定義（= prompt）

## 4. ガード（MUST / MUST NOT）

### 4.1 MUST

- 日時（または期間）を記載する
- 議題を記載する
- 合意事項と未決事項を区別して記録する
- 背景・前提が失われない程度の情報を保持する

### 4.2 MUST NOT

- `minutes` を仕様書の代替として扱ってはならない
- 合意済み仕様を `minutes` のみで成立させてはならない
- 事実記録を正当性の主張にすり替えてはならない

## 5. 推奨構成

- 概要（日時 / 参加者）
- 議題
- 議論ログ（要約）
- 合意事項
- 未決事項
- 次アクション

---

[目次](../../../目次.md) > 仕様 > document_type > minutes > 仕様
