<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261001-081500Z-CCTX
lang: ja-JP
canonical_title: Capability Context仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Capability Context仕様

# Capability Context(能力コンテキスト)仕様

## 1. 目的

Capability Context(能力コンテキスト)は、登録済みCapability(能力)について、現在の実行環境で確認した利用可能性をExecution Context(実行コンテキスト)へ保持する実行時情報である。

Capability ContextはCapability仕様またはCapability Registry(能力登録簿)の正本を代替しない。

## 2. 所有

Capability ContextはExecution Contextの一部としてCore(中核)が管理する。

Workflow(ワークフロー)、SubFlow(サブフロー)、Tool(ツール)その他のSubsystemはCapability Contextを直接変更してはならない（MUST NOT）。

能力確認結果を反映する場合はCoreへの変更要求として扱う。

## 3. Entry

Capability ContextはCapabilityごとにCapability Entry(能力確認項目)を0..1件保持できる。

Capability Entryは少なくとも次を表現できなければならない（MUST）。

- capability: 登録済みCapabilityの識別
- status: 能力確認結果
- evidence: 判定根拠
- checked_at: 確認時点
- validity: 現在その結果を再利用できるかを判断する情報

Execution Capabilityではevidenceに、確認できたCapability Provider(能力提供手段)または確認不能理由を含められるものとする。

Practical Capabilityではevidenceに、判定に使用したrequiredおよびoptionalなExecution Capabilityの結果を含められるものとする。

Capability Entryは必要に応じて、ProviderごとのAvailability Condition(利用可能性条件)を保持できる。

Availability Conditionは少なくとも次を表現できるものとする。

- affected_provider: 影響を受けたProvider
- failure_class: 観測した失敗の分類
- retryable: 再試行可能と判断できるか
- retry_after: サービス等から明示された再試行可能時点。判明する場合のみ
- alternative_providers: 同じExecution Capabilityを提供する代替Provider候補

これらは観測結果または明示されたサービス情報を記録するものであり、根拠なく原因、復旧時刻または再試行可否を推測してはならない（MUST NOT）。

## 4. Status

Execution Capabilityは少なくとも次を扱う。

- `AVAILABLE`
- `UNAVAILABLE`
- `UNKNOWN`

Practical Capabilityは少なくとも次を扱う。

- `AVAILABLE`
- `DEGRADED`
- `UNAVAILABLE`
- `UNKNOWN`

statusは能力の利用可能性であり、現在のWork(作業)における実行許可ではない。

`AVAILABLE`をRestriction Context(制限コンテキスト)、利用者承認または対象範囲確認の代替として使用してはならない（MUST NOT）。

## 5. Validity(有効性)

Capability Entryは永続的な事実として扱ってはならない（MUST NOT）。

少なくとも次の場合、既存Entryをそのまま現在有効な判定として使用してはならない（MUST NOT）。

- Capability仕様または依存Capability定義が変更された。
- Capability Provider定義が変更された。
- 実行環境のTool、Connector、接続または認証状態が変化したことを検出した。
- 過去のProviderに対応するTool実行が利用不能、認証失敗その他の能力状態変化を示した。
- 現在の処理に必要な能力について、既存evidenceが現在も成立するか安全に確認できない。

この場合、Entryを失効扱いとし、必要なCapabilityを再確認する。

単に時間が経過したことだけで一律の固定有効期限を要求しない。Providerの性質および現在確認できる情報に基づいて再確認要否を判断する。

## 6. 実行直前の再確認

副作用を伴う操作を提供するExecution Capabilityについて、Capability Contextの`AVAILABLE`だけを根拠に、Providerに対応するToolを実行してはならない（MUST NOT）。

実行直前には少なくとも次を確認する。

- 対象Execution CapabilityのEntryが失効していない。
- 使用予定Providerが現在利用可能であることを確認できる。
- 有効なRestriction Contextに違反しない。
- 必要な利用者承認および対象範囲が成立している。

Provider利用可能性を安全に確認できない場合は、古い`AVAILABLE`を維持したまま実行せず、能力再確認または`UNKNOWN`への更新を行う。

## 7. Execution Attempt(実行試行)

Capability(能力)、Capability Provider(能力提供手段)、Execution Attempt(実行試行)は別の概念として扱う。

Execution Attemptは、特定Providerに対応するToolを今回実行した結果であり、その失敗だけをCapability全体の恒常的なUNAVAILABLEと同一視してはならない（MUST NOT）。

Providerに対応するTool実行に失敗した場合、確認できる範囲で少なくとも次を区別する。

- `TRANSIENT_ERROR`: 通信失敗、タイムアウト、一時的サービス障害等、再試行で変化し得ることを確認できる。
- `TEMPORARILY_LIMITED`: rate limit、quota、cooldown等、一定期間または条件が変わるまで利用を制限されていることを確認できる。
- `PROVIDER_MISMATCH`: 選択したProviderが要求操作を満たさない、またはProvider選択が不適切であることを確認できる。
- `PERMANENT_UNAVAILABLE`: Provider不存在、恒常的権限不足等、同条件での再試行では改善しないことを確認できる。
- `UNKNOWN`: 原因を安全に分類できない。

一時的な失敗を根拠なくPERMANENT_UNAVAILABLEへ昇格してはならない（MUST NOT）。

一つのProviderが失敗しても、同じExecution Capabilityを提供する別Providerが存在する場合は、そのProviderを独立に評価しなければならない（MUST）。

`TEMPORARILY_LIMITED`でretry_afterが明示されている場合、その時点より前に同一条件で同じProviderを無条件に反復実行してはならない（MUST NOT）。

retry_afterが明示されていない場合、復旧時刻を推測してはならない（MUST NOT）。

同一条件で進展のない自動再試行を無制限に継続してはならない（MUST NOT）。

## 8. 更新

HLDocS能力確認Workflowその他の仕様上認められた処理は、能力確認結果をCoreへ提示できる。

Coreは登録済みCapabilityとの対応、status、evidenceおよび現在のExecution Contextとの整合を確認した後、Capability Contextへ反映する。

再確認により結果が変化した場合、以前のstatusを優先してはならない（MUST NOT）。

## 9. 利用

Capabilityを必要とするWorkflowは、Capability Contextに現在有効なEntryが存在する場合、その結果を能力確認の入力として再利用してよい（MAY）。

Entryが存在しない、失効している、または必要な能力を安全に判断できない場合、未確認を`AVAILABLE`とみなしてはならない（MUST NOT）。

Capability Contextに未登録CapabilityのEntryを生成してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > Core > Capability Context仕様
