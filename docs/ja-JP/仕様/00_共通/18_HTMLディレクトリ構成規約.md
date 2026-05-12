<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlDirectoryStructure
lang: ja-JP
canonical_title: HTMLディレクトリ構成規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTMLディレクトリ構成規約

# HTMLディレクトリ構成規約

本書は、「HLDocS 前提条件」という仕様が参照可能である場合にのみ適用される。

- 「HLDocS 前提条件」が入力として与えられていない場合、または当該仕様に基づく適用可否が確定していない場合、本書に基づく判断・生成・再作成・工程実行を行ってはならない。
- この場合、許可されるのは、提示された文書の受理および存在確認、ならびに前提条件が未参照または未確定である旨の通知のみとする。
- 「HLDocS 前提条件」が入力文書一覧に含まれない場合、生成・再作成・成果物提示を一切行ってはならない。

---

## 1. 目的

本書は、HLDocS における HTML ドキュメント生成結果のディレクトリ構成を定義する。

本規約は、以下を安定化することを目的とする。

- generated artifact 配置
- HTML ドキュメント間 navigation
- profile 別生成
- stale representation 管理
- restructuring / migration
- 公開ツールとの分離

---

## 2. 基本方針

HTML ドキュメントは、Markdown 正本とは分離した generated artifact 領域へ出力しなければならない（MUST）。

HTML ドキュメント配置を、Markdown 正本ディレクトリと混在させてはならない（MUST NOT）。

HTML ディレクトリ構成は、論理用途・profile・navigation を基準として構成する。

物理ファイル番号や、物理ファイル順序を、HTML navigation の主軸としてはならない（MUST NOT）。

---

## 3. 既定配置

既定の HTML generated artifact 配置先は以下とする。

```text
docs/ja-JP/HTMLドキュメント
```

このディレクトリは、Markdown canonical 領域ではない。

HTML ドキュメントは、generated operational representation として扱う。

---

## 4. 推奨ディレクトリ構成

少なくとも以下の構成を想定する。

```text
HTMLドキュメント/
├── overview/
├── reference/
├── traceability/
├── reports/
├── assets/
├── manifest/
└── index.html
```

---

## 5. overview/

`overview/` は、overview profile 用 generated page を格納する。

想定例：

- overview page
- concept page
- architecture page
- beginner guide
- navigation page

---

## 6. reference/

`reference/` は、reference profile 用 generated page を格納する。

想定例：

- Document Page
- Section Page
- API reference
- usage reference
- document_type reference

reference は、Markdown 正本に最も近い閲覧用 HTML とする。

---

## 7. traceability/

`traceability/` は、Traceability 可視化用 generated page を格納する。

想定例：

```text
spec
↓
testspec
↓
code
↓
testcode
```

また、以下を含めてよい（MAY）。

- reverse traceability
- orphan relation
- missing relation
- coverage graph
- stale relation

---

## 8. reports/

`reports/` は、検査成績表・テスト結果・証跡用 generated page を格納する。

想定例：

- PASS / FAIL report
- evidence report
- CI report
- migration validation report
- restructuring validation report

---

## 9. assets/

`assets/` は、HTML 表示補助資産を格納する。

想定例：

- CSS
- JavaScript
- images
- graph data
- icons
- downloadable evidence

assets は generated artifact として扱う。

assets を canonical specification とみなしてはならない（MUST NOT）。

---

## 10. manifest/

`manifest/` は、HTML Site Manifest を格納する。

少なくとも以下を格納してよい（MAY）。

- site manifest
- page manifest
- profile manifest
- migration manifest
- stale state manifest

Manifest は generated metadata として扱う。

---

## 11. index.html

`index.html` は、HTML ドキュメント全体 navigation の入口として扱う。

少なくとも以下を表示してよい（MAY）。

- profile navigation
- generated page list
- stale page list
- preview warning
- latest generated timestamp

---

## 12. ファイル名・ディレクトリ名制約

HTML generated artifact のファイル名およびディレクトリ名には、空白文字を含めてはならない（MUST NOT）。

区切り文字には、`_` または `-` を使用してよい（MAY）。

HTML generated artifact は、URL・HTMLリンク・Manifest・公開ツール・CI処理との整合性を維持できる命名でなければならない（MUST）。

---

## 13. profile 関係

profile により、生成対象ディレクトリは変化してよい（MAY）。

例：

- `overview`
  - overview/
  - index.html

- `reference`
  - reference/
  - index.html

- `traceability`
  - traceability/

- `test-report`
  - reports/

- `full`
  - 全ディレクトリ

---

## 14. restructuring / migration

ディレクトリ構成は、restructuring / migration によって変更されてよい（MAY）。

ただし、以下を保持しなければならない（MUST）。

- Manifest relation
- reverse navigation
- stale state
- source markdown relation

---

## 15. 公開ツールとの関係

本規約は、HTML generated artifact の論理構成のみを定義する。

GitHub Pages 等の公開先構成は、本規約の直接範囲外とする。

公開ツールまたは公開先アダプタは、必要に応じて generated artifact を publish 用構成へ変換してよい（MAY）。

---

## 16. 非目標

本規約は、以下を目的としない。

- CMS
- GitHub Pages 固定
- Web framework 固定
- SPA framework 固定
- CDN 構成固定
- サーバサイドレンダリング

---

## 17. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- page hierarchy
- asset naming
- generated filename rule
- manifest filename rule
- profile inheritance
- localization directory rule
- multi-language generation
- downloadable artifact rule

---

[目次](../../目次.md) > 仕様 > 共通 > HTMLディレクトリ構成規約
