<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261008-090000Z-TRC7
lang: ja-JP
canonical_title: Traceability仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > Traceability仕様

# Traceability仕様

## 1. 目的

本仕様は、HLDocS文書・検証単位・根拠記述・実装間の識別と参照関係を定義する。検証関係と仕様導出の根拠関係を混同してはならない（MUST NOT）。

## 2. 識別子

文書の論理同一性は`doc_id`で識別する（MUST）。検証単位は`(doc_id, sec_id)`、根拠アンカーは`(doc_id, ref_id)`の組で識別する（MUST）。ファイル名、章番号、見出し文字列を恒久識別子の代用としてはならない（MUST NOT）。

`sec_id`は`sec_<random>`、`ref_id`は`ref_<random>`形式とし、十分な衝突回避を行う（MUST）。識別子に意味語、章名、番号、文書種別を埋め込んではならない（MUST NOT）。確定済み識別子は通常の編集・移動・改名で変更してはならない（MUST NOT）。

## 3. 検証Traceability

`sec_id`はtestspecで検証単位を定義する際に初出・確定する（MUST）。spec単体の生成時に`sec_id`を自律生成してはならない（MUST NOT）。testspecの各検証ケースは見出し直下に`<!-- hldocs:sec_id=sec_<random> -->`を持つ（MUST）。

testspecから対応specへの検証参照は、実在する`doc_id#sec_id`を使用する（MUST）。参照先specに対応する識別子が未配置の場合、存在しない参照を捏造してはならない（MUST NOT）。testspec側で確定した識別子をspecの対応する検証対象箇所へ反映する工程を実施し、両側の整合性を確認する（MUST）。spec側の対応箇所にも同じ`<!-- hldocs:sec_id=sec_<random> -->`アンカーを配置する（MUST）。同一`sec_id`のtestspec/spec間の対応出現は許可するが、同一文書内の重複、および異なる検証単位への再利用は禁止する（MUST NOT）。参照先`doc_id#sec_id`の実在判定は、対象`doc_id`の文書内に対応アンカーが存在することを確認する（MUST）。

テスト番号は表示用ラベルであり恒久識別子ではない（MUST）。実装・テストコードは対応するtestspecの`doc_id#sec_id`をコメント等で参照する（MUST）。

## 4. 派生Traceability

noteまたはminutesの記述をspecの根拠として採用する場合、根拠箇所に`ref_id`を付与してよい（MAY）。根拠アンカーは`<!-- hldocs:ref_id=ref_<random> -->`で表す。

specからnote/minutesへの派生参照には`doc_id#ref_id`を用いる（MUST）。関係種別は`hldocs:rel=derivation`（直接仕様化）または`hldocs:rel=rationale`（背景・判断理由）とする（MUST）。派生参照を検証完了の証拠として扱ってはならない（MUST NOT）。note/minutesに検証用`sec_id`を付与してはならない（MUST NOT）。

## 5. 参照形式と用途の分離

- 検証参照：`doc_id#sec_id`。spec、testspec、実装の検証関係に用いる。
- 派生参照：`doc_id#ref_id`。note/minutesからspecへの根拠関係に用いる。
- 人間向けナビゲーション：Markdownリンク。文書間移動に用い、機械的同一性を代替しない。

機械参照には識別子形式を使用する（MUST）。URL、相対パス、UI固有の引用形式を検証・派生の恒久識別子として使用してはならない（MUST NOT）。ただし人間向けリンク、正本取得元の指定、外部情報の出典表示まで一律に禁止するものではない。

## 6. 生成・更新・検査

Workflowは文書生成・更新の要求と必要な参照関係を判定し、正本を取得する（MUST）。参照先が取得できない場合、推測で識別子を生成して整合したものとみなしてはならない（MUST NOT）。

整合性検査では少なくとも、識別子形式、文書内重複、参照先の実在、参照用途、spec/testspec/codeの対応、note/minutesの派生関係を確認する（MUST）。検査だけを目的とする処理は文書や識別子を無断変更してはならない（MUST NOT）。

通常の更新では既存識別子を維持する（MUST）。移行時の識別子再付与は、対象・影響・承認・再検証を明示した独立の移行処理でのみ扱い、通常の文書生成の暗黙処理に含めてはならない（MUST NOT）。

## 7. 適用境界

本仕様はv0.7.0の共通仕様成立条件、Core、Workflow、Restrictionおよび文書共通構造仕様の下で適用する。旧版の`meta/apply`モード、常設テンプレートまたは生成プロンプトの存在を成立条件として要求してはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > 共通 > Traceability仕様
