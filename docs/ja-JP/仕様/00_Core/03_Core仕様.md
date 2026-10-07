<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-CORE
lang: ja-JP
canonical_title: Core仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Core仕様

# Core(中核)仕様

## 1. 目的

本書は、HLDocS Core(中核)の責務と、通常運転に共通する実行制御、およびState Machine(状態遷移機構)へ移譲できない場合の復旧への移行を定義する。

## 2. Coreの責務

Coreは次を担当する。

- HLDocSシステム起動制御
- Execution Contextの正本管理
- Execution Contextに対する変更要求の検証および適用
- Restriction Context(制限コンテキスト)の構築および強制
- 登録済み仕様要素の参照機構
- HLDocS仕様/規約の正本候補および正本競合の管理
- State Machineへの制御移譲
- State Machineへ移譲できない場合の復旧制御

Coreは、作業の意味上の処理内容を決定する機構ではない。

## 3. Coreが行ってはならないこと

Coreは次を行ってはならない（MUST NOT）。

- 通常作業で利用するWorkflowを意味判断によって選択する。
- Workflow PlanへWorkflowを独断で追加、削除または並べ替える。
- WorkflowまたはSubFlowの処理内容を決定する。
- State Machineに代わって通常のState遷移可否を決定する。
- 個別Restriction Setの内容を独断で変更する。
- 制限確認を迂回して処理を実行する。
- 複数の正本候補を推測で統合し、単一の正本として扱う。

## 4. Execution Context

Coreは、実行状態をExecution Contextとして管理しなければならない（MUST）。

Execution Context(実行コンテキスト)は、少なくとも次を表現できなければならない（MUST）。

- Current State
- Current Workflow Plan
- Active Workflow
- Suspended Workflow
- Current Work
- Work Contexts
- Capability Context

Current Workflow PlanはWorkの有無に依存しない現在の実行Planとする。

Current Workflow PlanはOwnerを持たなければならない（MUST）。  
Ownerは少なくとも次を区別する。

- SYSTEM: HLDocS自身の通常運転処理
- WORK: 利用者Workに属する処理

OwnerがWORKの場合は、対応するWork IDを一意に関連付けなければならない（MUST）。  
OwnerがSYSTEMの場合は、存在しないWorkを生成してPlanの所有者としてはならない（MUST NOT）。

Work Context(作業コンテキスト)は少なくともWork ID、Purpose、Status、Issuesおよび任意のArtifacts(作業成果物)を保持できる。

ArtifactsはWork固有の中間成果物または結果であり、作業対象正本またはExecution Context(実行コンテキスト)の確定実行状態を代替しない。

Work Statusは、少なくとも次を扱う。

- ACTIVE
- SUSPENDED
- COMPLETED

同時にACTIVEとなるWorkは最大1件とする（MUST）。

同時に`ACTIVE(実行中)`となるWorkflowは最大1件とする（MUST）。`SUSPENDED(中断中)` Workflowが存在していても別WorkflowをACTIVEにできるが、その組み合わせが対応Workflow仕様で許可され、復帰先を一意に管理できなければならない（MUST）。

Workflow Planの実行状態とIssueの状態を同一の状態として扱ってはならない（MUST NOT）。

Capability Context(能力コンテキスト)は登録済みCapabilityについて現在の実行環境で確認した利用可能性を保持する。詳細はCapability Context仕様に従う。

Capability Contextの`AVAILABLE`を、現在の処理における実行許可またはRestriction Contextの代替として扱ってはならない（MUST NOT）。

## 5. LLM_WORKSPACE

LLM_WORKSPACEは、CoreがHLDocS実行中の作業継続および復元を補助するために利用できる一時記憶領域である。

LLM_WORKSPACEは独立した実行主体ではなく、Coreの補助機構として扱う。

LLM_WORKSPACEは次のいずれも代替してはならない（MUST NOT）。

- HLDocS仕様/規約（正本）
- 作業対象正本
- Execution Context(実行コンテキスト)
- Work Context内Artifactの正本性を持つ実体参照先

Coreは、LLM_WORKSPACEへ作業継続または復元に必要な補助情報を保持してよい（MAY）。

LLM_WORKSPACEに保存された情報だけを根拠としてExecution Contextの確定状態を復元してはならない（MUST NOT）。

LLM_WORKSPACEから情報を再利用する場合、Coreは現在採用する正本、現在の実体および現在の実行環境と整合することを必要な範囲で再確認しなければならない（MUST）。

保存後に失効し得る情報は、現在も有効であることを確認できない場合、そのまま確定情報として再利用してはならない（MUST NOT）。Capability Context(能力コンテキスト)の復元または再利用はCapability Context仕様のValidity(有効性)規則にも従う。

LLM_WORKSPACEが存在しない、失われた、読み取れない、または内容を安全に再利用できないことだけを理由として、正本または現在の実体を推測で補完してはならない（MUST NOT）。

## 6. Execution Contextの変更

State Machine、選択ルール、Workflowその他のSubsystemは、Execution Contextを直接変更してはならない（MUST NOT）。  
Execution Contextを変更する場合は、Coreへ変更要求を行わなければならない（MUST）。

Coreは変更要求について、少なくとも次を確認しなければならない（MUST）。

- 現在のExecution Contextとの整合性
- 要求元が当該変更を要求できること
- 有効なRestriction Contextに違反しないこと
- 利用者承認を必要とする変更では、必要な承認根拠が存在すること

Workflow(ワークフロー)がWork Context内のArtifactを生成または更新する場合もExecution Context変更要求として扱い、Coreが対象Work、要求元および変更内容を検証して適用しなければならない（MUST）。

## 7. Workflow Plan変更

Stateのdefault_workflow_planから新規Planを生成する場合、そのState仕様で定義されたPlanを初期Planとして生成してよい（MAY）。

State進入時にCurrent Workflow Planが存在する場合、Coreは新規Plan生成より先に既存Planの再利用可能性と解除可能性を別々に検証しなければならない（MUST）。

再利用可能なPlanが存在する場合、同一State、Ownerおよび対象Workに対する重複Planを生成してはならない（MUST NOT）。

再利用不能でも安全に解除できないPlanが存在する場合、そのPlanを破棄、上書きまたは別Planで置換してState進入を強行してはならない（MUST NOT）。

Planの解除と新規生成を伴うState進入では、Current State、Current Workflow Plan、Current WorkおよびActive/Suspended Workflowの関係に矛盾する確定途中状態を残してはならない（MUST NOT）。

承認済みまたはState仕様により確定したWorkflow Plan内の通常の実行状態遷移は、各仕様の条件を満たす場合に適用してよい（MAY）。

実行中Planに対する次の変更は、利用者WorkをOwnerとする場合、利用者による明示的な指示または承認なしに確定してはならない（MUST NOT）。

- Workflowの追加
- Workflowの削除
- Workflow順序の変更
- WorkflowのSKIPPED化

SYSTEM Planの変更は、対応するStateまたはシステム仕様に明示された規則なしに確定してはならない（MUST NOT）。

SYSTEM Plan変更では利用者承認を一般的な代替根拠としてはならない（MUST NOT）。Coreは、変更対象、変更内容、仕様上の許可根拠および現在の変更条件を検証しなければならない（MUST）。

SYSTEM Planの変更規則が定義されていない場合、CoreはPlan構成を維持する。処理を継続できない場合も、Coreが未定義のPlan変更を生成して回避してはならない（MUST NOT）。

SYSTEM Plan変更によってWork(作業)を暗黙に生成または変更してはならない（MUST NOT）。

既存Plan内WorkflowのRe-run(再実行)およびRe-run Sequence(再実行列)はPlan構成変更として扱わない。CoreはRe-run要求について、対象WorkflowがCurrent Planに存在すること、再実行理由が対応仕様に適合すること、同時ACTIVE制約およびRestriction Context(制限コンテキスト)を満たすことを検証しなければならない（MUST）。

Re-run Sequenceでは、Coreは一つのSUSPENDED Workflowをreturn_toとして保持し、Sequence内Workflowを順番に再実行する。Sequenceの中間Workflowを新たなSUSPENDED復帰先として積み重ねてはならない（MUST NOT）。

## 8. Restriction Context

Coreは、常時適用する安全側の基本制御を保持しなければならない（MUST）。Core基本制限は通常運転用Restriction Setではなく、Restriction Contextの構築可否にかかわらず適用する。

通常運転では、現在の実行位置に応じてState、Workflow、SubFlowが宣言するRestriction Set(制限セット)を必要な範囲で読み込み、Restriction Contextを構築する。

Coreは宣言されたRestriction Setについて、Restriction Set登録簿で登録を確認した後、登録された個別仕様を参照しなければならない（MUST）。登録されていないRestriction Setを名称または類似仕様から推測して適用してはならない（MUST NOT）。

Restriction Contextは概念上、Core基本制限にState、Workflow、SubFlowの制限を順次追加したものとする。

下位のRestriction Setは上位の制限を解除または緩和してはならない（MUST NOT）。複数の制限が同じ操作へ適用される場合はすべてを満たさなければならず（MUST）、禁止規則と許容規則が競合する場合は、禁止またはより厳しい制限を適用する。

必要と宣言されたRestriction Setを登録確認、取得、解釈または適用できない場合は、制限なしとして処理を継続してはならない（MUST NOT）。

Tool(ツール)その他の副作用を伴う操作を実行する直前に、Coreは現在のRestriction Contextに対して対象Capability、選択されたCapability Provider、操作、対象範囲および必要な承認条件を再評価しなければならない（MUST）。

Restriction Setの共通構造、登録および参照規則の詳細はRestriction Set仕様に従う。

## 9. 正本候補と正本競合

Coreは、HLDocS仕様/規約または作業対象正本を参照するとき、同一の意味上の対象について複数の正本候補が存在し得ることを前提としなければならない（MUST）。

複数候補の存在自体を異常としてはならない（MUST NOT）。Version Up(バージョン更新)、移行、再構成、比較、バックアップその他の運用では、新旧候補が同時に存在してよい（MAY）。

Coreは複数候補を検出した場合、利用者が指定した情報源、版、ブランチ、配置先、登録情報その他の明示的な正本選択根拠によって、現在採用する正本を一意に確定できるか検証しなければならない（MUST）。

`canonical_document: true`は正本候補であることを示す情報として利用してよいが、それだけを理由として、同一対象の他候補より常に優先される単独の選択根拠として扱ってはならない（MUST NOT）。

正本候補が複数存在しても、現在採用する正本を明示的な根拠から一意に確定できる場合は正本競合として処理を停止する必要はない。

現在採用する正本を一意に確定できない場合をCanonical Conflict(正本競合)とする。

Canonical Conflictを検出した場合、Coreは次を行ってはならない（MUST NOT）。

- 候補の内容を推測で統合する。
- ファイル更新日時、列挙順、検索順位その他の偶然的な順序だけで正本を選択する。
- 新しい版番号らしく見えることだけを理由に正本を選択する。
- 一方の候補を暗黙に非正本化、削除または上書きする。
- 競合解消を必要とする処理を、正本が確定したものとして継続する。

Canonical Conflictが現在の処理に影響する場合、Coreは競合する候補と既知の選択根拠をInteraction(対話窓口)へ提示し、必要に応じて利用者判断を要求しなければならない（MUST）。

Canonical Conflictが現在の処理に影響しない場合、無関係な競合だけを理由としてHLDocS全体を停止することを要求しない。ただし、競合候補を現在の正本として暗黙利用してはならない（MUST NOT）。

Version Up中に旧版を比較資料として保持する場合、旧版を物理削除または`canonical_document: false`へ変更することを一律に要求しない。現在採用する版または情報源を別の明示的根拠で一意に識別できればよい。

## 10. State Machineへの移譲

Coreは起動後、State Machine仕様を必要な範囲で参照し、制御移譲を試行する。

移譲成功後は、通常のState遷移判断をState Machineへ委ねなければならない（MUST）。  
CoreはState Machineが許可した遷移要求について、Execution ContextおよびRestriction Context上の整合性を確認した後にCurrent Stateへ適用する。

## 11. Core復旧への移行

State Machineへの制御移譲に失敗した場合、Coreは通常運転を開始してはならず（MUST NOT）、Core復旧へ移行しなければならない（MUST）。

Core仕様が規定する復旧責務は、復旧へ安全に移行するまでとする。

復旧開始後の実行状態、制限、調査、変更、利用者判断、再検証およびState Machineへの再移譲はCore復旧仕様に従う。

## 12. Interactionとの関係

Coreは利用者との自然言語対話を直接担当しない。  
利用者への情報提示および判断要求はInteractionを介して行う。

Coreは、利用者承認を必要とする変更について、Interaction等から得られた承認根拠を検証してから適用しなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > Core > Core仕様
