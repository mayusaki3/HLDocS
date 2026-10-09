<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261009-013000Z-DTY7
lang: ja-JP
canonical_title: document_type仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > document_type > document_type仕様

# document_type仕様

## 1. 目的

本書はv0.7.0で生成・更新する六種類のdocument_typeの役割と本文制約を定義する。共通外枠・doc_id・langは「文書共通構造仕様」、sec_id・ref_idは「Traceability仕様」に従う。旧版の常設template/promptやmeta/applyモードを要求しない。

## 2. index

indexは文書集合の階層とナビゲーションを示す。本文はリンクと分類見出しを主体とする（MUST）。個別文書の要約、規範の宣言、作業手順、TODOを混入してはならない（MUST NOT）。読者が誤った版・適用範囲・利用条件を選択しないための短い注意喚起領域を冒頭に設けてよい（MAY）。注意喚起は既存の正本仕様や利用条件への参照、および当該文書集合の状態を示す事実に限定し、新しい規範・操作手順・判断規則を宣言してはならない（MUST NOT）。個別文書の要約を含まない短い案内文は、利用者が明示的に要求した場合に限り追加してよい（MAY）。

文書の追加・削除・移動に伴う更新は階層を再評価し、既存indexのdoc_idを維持する（MUST）。

## 3. spec

specは概念、構造、制約、不変条件、正否基準を宣言する。規範として確定していない案を確定事項として記載してはならない（MUST NOT）。利用手順、テストケース、検証結果、変更履歴を規範本文の代替としてはならない（MUST NOT）。

HLDocS自身のセルフ検証仕様もdocument_type=specとして管理する（MUST）。その場合、本文冒頭の目的または同等の章で「本書はHLDocS自身のセルフ検証仕様である」と明示しなければならない（MUST）。タイトルやファイル名のみでこの宣言を代替してはならない（MUST NOT）。セルフ検証仕様には対象、前提、シナリオ、期待結果、判定方法、記録条件を含めてよい（MAY）。通常の動作仕様とセルフ検証仕様は文書の責務を分離する（MUST）。

specから検証対象を参照する場合、testspec側で確定したsec_idを受け取り、Traceability仕様に従う（MUST）。

## 4. testspec

testspecは対象specに従属し、検証対象、前提、操作・条件、期待結果を定義する（MUST）。実装コードまたはテストコードそのものを記載してはならない（MUST NOT）。

各検証ケースは独立した見出しを持ち、直下に`<!-- hldocs:sec_id=sec_<random> -->`を配置する（MUST）。sec_idはtestspecで初出・確定し、specへの参照は実在する`doc_id#sec_id`を使用する（MUST）。spec側への識別子反映前に参照が成立したものとみなしてはならない（MUST NOT）。テスト番号は表示ラベルであり恒久キーとして使用しない。

HLDocS自身のセルフ検証をtestspec文書として作成してはならない（MUST NOT）。HLDocSセルフ検証は対応するセルフ検証仕様・結果の管理規則に従う。

## 5. note

noteは未確定の仮説、設計途中の案、論点、前提、未決事項を記録する。既に規範として成立している事項をnoteのみで成立させてはならない（MUST NOT）。分類できない内容を無条件にnoteへ割り当ててはならない（MUST NOT）。

specの根拠として採用する箇所には必要に応じref_idを付与し、派生参照はTraceability仕様に従う。

## 6. minutes

minutesは会議・議論・設計検討の事実記録である。日時または期間、議題、合意事項、未決事項を区別して記載する（MUST）。確認できない参加者や決定を捏造してはならない（MUST NOT）。合意事項を記録しても、それだけで正本specが更新されたものとみなしてはならない（MUST NOT）。

仕様化の根拠となる記述には必要に応じref_idを付与し、派生参照はTraceability仕様に従う。

## 7. usage

usageは利用者が操作できるよう前提条件、入力、手順、結果、注意事項を記載する。規範仕様を新設・変更してはならない（MUST NOT）。設計議論、テストケース、規範の要約を本文の中心にしてはならない（MUST NOT）。操作が実行可能か未確認の場合は確認済みとして断言してはならない（MUST NOT）。

## 8. 共通判定

Workflowは生成前に対象document_typeを確定し、生成後に当該種別の役割、禁止内容、共通外枠、Traceability参照を検査する（MUST）。複数の役割が混在する場合は文書を分離するか、利用者判断を求める。検査に合格しても保存権限やWork完了を自動的に認めてはならない（MUST NOT）。

---

[目次](../../目次.md) > 仕様 > document_type > document_type仕様
