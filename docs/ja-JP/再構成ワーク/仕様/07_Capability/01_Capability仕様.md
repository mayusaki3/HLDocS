<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260929-191300Z-CAP
lang: ja-JP
canonical_title: Capability仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Capability > Capability仕様

# Capability(能力)仕様

## 1. 目的

本書は、HLDocSが扱うCapability(能力)の共通構造を定義する。

Capabilityは「何ができるか」を宣言するものであり、現在その操作を実行してよいことを直接意味しない。

## 2. Capabilityの種類

Capabilityは次の二種類に分ける。

- Practical Capability(実務能力): 利用者から見た、HLDocSが遂行できる作業。
- Execution Capability(実行能力): 実務能力を成立させるためにHLDocSが実行できる操作。

一つのCapabilityを両方の種類として定義してはならない（MUST NOT）。

## 3. Practical Capability

Practical Capabilityは少なくとも次を定義する。

- capability: 一意な能力名または識別子
- type: PRACTICAL
- purpose: 利用者から見た能力の目的
- requires: 必須Execution Capability 0..N
- optional: 任意Execution Capability 0..N

Practical Capabilityは、特定のTool名を直接必要条件としてはならない（MUST NOT）。

例:

```yaml
capability: コード生成修正
type: PRACTICAL
purpose: コードの新規生成または既存コードの修正を行う
requires:
  - ファイル参照
  - ファイル書込
optional:
  - Git参照
  - Git書込
  - テスト実行
```

## 4. Execution Capability

Execution Capabilityは少なくとも次を定義する。

- capability: 一意な能力名または識別子
- type: EXECUTION
- purpose: 実行できる操作の意味
- provided_by: 能力提供手段 1..N

能力提供手段はTool(ツール)、SubFlow(サブフロー)その他の登録済み実行手段を参照できる。

Execution Capabilityは特定実装そのものではない。同じ能力を複数の能力提供手段が提供してよい（MAY）。

## 5. 依存方向

Capabilityの基本依存方向は次とする。

```text
Practical Capability
        ↓ requires / optional
Execution Capability
        ↓ provided_by
能力提供手段
```

下位Capabilityまたは能力提供手段へ、利用元Practical Capabilityの逆参照一覧を必須としてはならない（MUST NOT）。

循環するCapability依存を定義してはならない（MUST NOT）。

## 6. Restrictionとの境界

Execution CapabilityがAVAILABLEであることは、その操作を現在実行してよいことを意味しない。

実際の操作前にはCore(中核)が有効なRestriction Context(制限コンテキスト)、実行条件および必要な承認根拠を検証しなければならない（MUST）。

Capability定義によってRestrictionを緩和または迂回してはならない（MUST NOT）。

## 7. 個別仕様

Capabilityは原則として1 Capabilityにつき1個別仕様とし、PracticalとExecutionを分離して配置する。

```text
07_Capability/
├─ Practical/
└─ Execution/
```

個別仕様は、そのCapabilityを理解・検証するために必要な情報を局所的に保持し、無関係なCapabilityの詳細を複製しない。

---

[目次](../../目次.md) > 仕様 > Capability > Capability仕様
