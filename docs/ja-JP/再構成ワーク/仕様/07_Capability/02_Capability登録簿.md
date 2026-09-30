<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-191301Z-CAPR
lang: ja-JP
canonical_title: Capability登録簿
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Capability > Capability登録簿

# Capability Registry(能力登録簿)

## 1. 目的

Capability Registry(能力登録簿)は、HLDocSに登録されたCapabilityを発見するための軽量な索引を定義する。

## 2. 責務

登録簿は少なくとも次を区別して列挙できるものとする。

- Practical Capability(実務能力)
- Execution Capability(実行能力)

登録簿はCapabilityの詳細仕様を内包する巨大な一括定義としてはならない（MUST NOT）。

Capabilityの意味、依存および能力提供手段は個別Capability仕様を正本とする。

## 3. 参照

能力確認その他の処理は、まず登録簿から候補Capabilityを発見し、必要な個別仕様だけを参照する。

すべての個別Capability仕様を無条件に一括読込することを前提としてはならない（MUST NOT）。

登録簿に存在しないCapabilityを、名称推測だけで登録済みとして扱ってはならない（MUST NOT）。

## 4. 登録

Capabilityを登録する場合は、個別Capability仕様と登録簿の対応が成立していなければならない（MUST）。

登録簿だけを追加して個別仕様が存在しない状態、または個別仕様だけを追加して登録簿へ反映されない状態を、能力追加完了として扱ってはならない（MUST NOT）。

## 5. 登録済みCapability

### 5.1 Practical Capability

- [コード生成修正](./Practical/コード生成修正.md)
- [仕様調査](./Practical/仕様調査.md)
- [仕様変更](./Practical/仕様変更.md)

### 5.2 Execution Capability

- [ファイル参照](./Execution/ファイル参照.md)
- [ファイル書込](./Execution/ファイル書込.md)

## 6. 段階的登録

再構成中のため、具体的なCapability一覧は個別能力仕様の追加と検証に合わせて段階的に登録する。

存在しない能力を網羅目的で推測して先行登録してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Capability > Capability登録簿
