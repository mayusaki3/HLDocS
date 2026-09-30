<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260930-170500Z-CAPP
lang: ja-JP
canonical_title: Capability Provider仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Capability > Capability Provider仕様

# Capability Provider(能力提供手段)仕様

## 1. 目的

本書は、Execution Capability(実行能力)を実際に提供するCapability Provider(能力提供手段)の識別、登録および実行時照合を定義する。

Capability ProviderはCapabilityそのものではなく、現在のLLM実行環境またはHLDocS定義によってExecution Capabilityを実現する手段である。

## 2. Providerの種類

Capability Providerは少なくとも次を扱える。

- `ENVIRONMENT_TOOL`: LLM実行環境から提供されるTool(ツール)、Connectorその他の実行手段。
- `HLDOCS_TOOL`: HLDocSが個別仕様として定義するTool。
- `SUBFLOW`: 登録済みSubFlow(サブフロー)がExecution Capabilityを提供する場合。

実装製品名だけをProviderの意味としてはならない（MUST NOT）。

## 3. Provider Reference

Execution Capabilityの`provided_by`はProvider Reference(能力提供手段参照)を保持する。

Provider Referenceは少なくとも次を定義する。

- provider_id: HLDocS内で一意な意味識別子
- provider_type
- purpose: Providerに要求する操作
- match: 実行環境でProviderを照合するための意味条件

`ENVIRONMENT_TOOL`では、実行環境ごとにTool名、Connector名または内部識別子が変化し得るため、特定の一時的Tool名だけを恒久的なProvider識別子としてはならない（MUST NOT）。

例:

```yaml
provider_id: repository-file-read
provider_type: ENVIRONMENT_TOOL
purpose: リポジトリ上のテキストファイルを参照する
match:
  required_operations:
    - repository_file_read
```

## 4. 実行環境Providerの照合

HLDocS能力確認Workflow(ワークフロー)は、`ENVIRONMENT_TOOL`のProvider Referenceを評価する場合、現在のLLM実行環境に提供されている実行手段を確認する。

実行手段がProvider Referenceのpurposeおよびmatchを満たすことを確認できる場合、そのProviderを現在利用可能として扱ってよい（MAY）。

名称が一致することだけを利用可能性の根拠としてはならない（MUST NOT）。

逆に、特定製品名または過去のTool名が存在しないことだけを理由として、同等操作を提供する現在の実行手段を利用不能としてはならない（MUST NOT）。

照合根拠を安全に確認できない場合はUNKNOWNとして扱う。

## 5. Provider登録

Provider ReferenceはExecution Capabilityの個別仕様内に局所的に定義してよい（MAY）。

複数のExecution Capabilityから同一Provider定義を共有する必要が生じた場合は、独立したProvider Registry(能力提供手段登録簿)への分離を検討する。

共有の必要がない段階で、網羅的なProvider Registryを先行作成してはならない（MUST NOT）。

## 6. Restrictionとの境界

Providerが現在利用可能であっても、そのProviderを現在のWork(作業)で実行してよいとは限らない。

Provider実行前にはCore(中核)がRestriction Context(制限コンテキスト)、利用者承認、対象範囲その他の実行条件を検証しなければならない（MUST）。

Provider照合はRestriction判定を代替してはならない（MUST NOT）。

## 7. 検証

Execution CapabilityをAVAILABLEと判定するには、少なくとも一つの`provided_by`について、現在の実行環境またはHLDocS登録情報から利用可能性を確認できなければならない（MUST）。

Providerが複数存在する場合、一つが利用可能であれば他のProviderが利用不能であることだけを理由にExecution CapabilityをUNAVAILABLEとしてはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Capability > Capability Provider仕様
