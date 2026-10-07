<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261007-CORE-VALIDATION
lang: ja-JP
canonical_title: Core検証仕様
document_type: testspec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Core検証仕様

# Core(中核)検証仕様

## 1. 目的

本書は、HLDocS Core(中核)仕様群を、過去のチャット、LLM_WORKSPACEその他の一時情報へ依存せず再検証するための検証条件を定義する。

新しいLLMセッションは、本書および本書が指定するリポジトリ上の正本だけから検証を開始できなければならない（MUST）。

過去の検証結果は比較資料として利用してよいが、現在のPASS判定の根拠としてそのまま再利用してはならない（MUST NOT）。

## 2. 検証対象

Core検証では、少なくとも次を現在採用する正本として参照する。

- `docs/ja-JP/仕様/00_Core/01_HLDocSとは.md`
- `docs/ja-JP/仕様/00_Core/02_HLDocSシステム起動条件.md`
- `docs/ja-JP/仕様/00_Core/03_Core仕様.md`
- `docs/ja-JP/仕様/00_Core/04_Core基本制限仕様.md`
- `docs/ja-JP/仕様/00_Core/05_Core復旧仕様.md`
- `docs/ja-JP/仕様/00_Core/06_用語表記規則.md`
- `docs/ja-JP/仕様/00_Core/07_CapabilityContext仕様.md`
- 本書

Coreが参照するState Machine、State、Workflow、Capability、Restriction、Tool、SubFlowその他の後続仕様は、Coreとの境界確認に必要な範囲だけ参照する。

旧仕様、再構成前仕様および過去版は比較対象として参照してよいが、現在のCore仕様の不足を暗黙に補完してはならない（MUST NOT）。

## 3. 検証独立性

検証に必要な前提、シナリオ、期待結果または判定規則がリポジトリ上の仕様から得られない場合、過去チャットまたはLLM_WORKSPACEから推測して補ってはならない（MUST NOT）。

不足を発見した場合は検証不能または仕様不足として記録する。

LLM_WORKSPACEは検証の正本、検証仕様または唯一の検証入力として扱ってはならない（MUST NOT）。

## 4. 検証区分

Core検証は少なくとも次の区分を実施する。

### 4.1 責務境界検証

次を確認する。

- CoreとState Machineの責務が逆転していない。
- CoreとWorkflow/SubFlowの意味処理責務が混在していない。
- Capability利用可能性と実行許可が分離されている。
- Capability ProviderとToolが同一概念として扱われていない。
- Execution Contextの確定変更主体がCoreへ限定されている。
- Interactionが制御主体になっていない。
- LLM_WORKSPACEが正本またはExecution Contextを代替していない。
- Core仕様の復旧責務がCore復旧への移行までであり、復旧開始後の責務がCore復旧仕様へ分離されている。

### 4.2 起動・通常運転境界検証

次を確認する。

- HLDocSシステム起動条件成立前に通常運転を開始しない。
- Core起動完了と通常運転開始を同一視しない。
- State Machineへの制御移譲成功後にのみ通常運転へ進む。
- 制御移譲失敗時は通常運転へ進まずCore復旧へ移行する。

### 4.3 Execution Context整合性検証

次を確認する。

- Current State、Current Workflow Plan、Current Work、Active/Suspended Workflowの確定途中に矛盾状態を残さない。
- 既存Planの再利用可能性と解除可能性を別々に判定する。
- 再利用不能なPlanを破棄可能と推定しない。
- WORK PlanとSYSTEM Planの構成変更根拠を混同しない。
- Re-runおよびRe-run SequenceをPlan構成変更と混同しない。

### 4.4 Restriction検証

次を確認する。

- Core基本制限は通常Restriction Setとは独立して常時適用される。
- 下位Restriction Setから上位制限を緩和できない。
- 必要なRestriction Setを取得、解釈または適用できない場合に制限なしで続行しない。
- CapabilityがAVAILABLEでもRestriction Context不成立時にToolを実行しない。
- 代替Toolまたは代替ProviderによってRestrictionを迂回できない。

### 4.5 Canonical Conflict検証

次を確認する。

- 複数の正本候補の存在だけでは異常としない。
- 明示的根拠から現在採用する正本を一意に選択できる場合は継続できる。
- 一意に選択できない場合はCanonical Conflictとして扱う。
- 更新日時、列挙順、検索順位または版番号らしさだけで暗黙選択しない。
- 競合候補を推測統合しない。

### 4.6 LLM_WORKSPACE検証

少なくとも次のシナリオを確認する。

1. LLM_WORKSPACEが存在しない状態から、正本だけでCore検証を開始できる。
2. LLM_WORKSPACEに古いExecution Context相当情報が存在しても、その情報だけで確定状態を復元しない。
3. 保存後にCapability Providerまたは実行環境が変化した場合、古いAVAILABLEを無条件に再利用しない。
4. LLM_WORKSPACEの内容と現在の正本が競合した場合、現在採用する正本を優先し、LLM_WORKSPACEで正本を上書きしない。

### 4.7 Fail-closed検証

少なくとも次のシナリオを再実行する。

- 必要Restriction Set取得不能
- Execution Context不整合
- State Machineで許可されないState遷移
- 旧Stateの未完了Plan残存
- WORK Plan構成変更に必要な利用者承認なし
- SYSTEM Plan構成変更に仕様根拠なし
- Capability AVAILABLEかつRestriction不成立
- Capability evidence失効または再確認不能
- Re-run Sequenceの次要素を開始不能
- State Machineへの起動時移譲失敗

各シナリオでは、推測補完、制限回避、暗黙破棄または未定義変更によって処理を強行しないことを確認する。

## 5. 問題点探索

既知シナリオのPASS確認だけで検証を終了してはならない（MUST NOT）。

検証時は仕様群を横断し、少なくとも次を探索する。

- 同一概念の異なる定義
- 同一責務を複数Subsystemが持つ記述
- 循環依存
- 未定義参照
- 登録簿に存在しない参照
- MUST/MUST NOTの競合
- Fail-openとなる経路
- 一時情報を正本として扱う経路
- Provider/Tool/Capabilityの責務混同
- State/State Machine/Coreの責務混同
- Work/Workflow/Workflow Planの責務混同
- 復旧処理から通常運転制限を迂回できる経路

新しい問題を発見した場合は、既知検証項目に含まれていなかったこと自体を理由として無視してはならない（MUST NOT）。

## 6. 判定

各検証項目は少なくとも次で判定する。

- PASS: 現在の正本から期待動作を一意に導出でき、競合する規則が確認されない。
- FAIL: 現在の正本から期待動作と競合する規則またはFail-open経路を確認した。
- UNDEFINED: 必要な規則が正本に存在せず、期待動作を一意に導出できない。
- BLOCKED: 必要な正本または参照先を取得できず検証できない。

UNDEFINEDまたはBLOCKEDをPASSとして扱ってはならない（MUST NOT）。

## 7. 検証結果の記録

検証結果には少なくとも次を記録する。

- 検証日
- 対象ブランチまたは対象版
- 検証対象
- 各項目のPASS / FAIL / UNDEFINED / BLOCKED
- 発見した問題
- 問題の根拠となる仕様箇所
- 実施した修正
- 未解決事項
- 再検証が必要となる条件

検証中に仕様を修正した場合は、修正後の正本に対して影響範囲を再検証しなければならない（MUST）。

## 8. 再検証条件

少なくとも次の場合、Core検証を再実施する。

- Core仕様群を変更した。
- State Machine、State、Workflow、Capability、Restriction、Tool、SubFlowその他の後続仕様変更がCore境界へ影響し得る。
- Core復旧方法または復旧制限を変更した。
- Execution Context構造を変更した。
- Capability ContextまたはCapability Providerモデルを変更した。
- 新しいFail-closedシナリオまたは責務競合を発見した。
- v0.7.0完成判定を行う。

---

[目次](../../目次.md) > 仕様 > Core > Core検証仕様
