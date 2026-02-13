<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260213-000000Z-A1B2
lang: ja-JP
canonical_title: 共通ドキュメントテンプレート
document_type: template
canonical_document: true
-->

[目次](../../目次.md) > テンプレート > 共通 > 共通ドキュメントテンプレート

# 共通ドキュメントテンプレート

本テンプレートは、HLDocS 管理下ドキュメントの**構造（骨格）**を定義する。

本テンプレートは、構造のみを定義し、
判断ロジック・生成手順・検査規則・出力方式選択規則を含まない。

LLM が意味論として解釈してよいのは、
`__COMMON_TEMPLATE_BEGIN__` と `__COMMON_TEMPLATE_END__`
で囲まれた範囲のみである。

---

__COMMON_TEMPLATE_BEGIN__

<!--
HLDocS:LLM-MANAGED
doc_id: {doc_id}
lang: {lang}
canonical_title: {canonical_title}
document_type: {document_type}
canonical_document: {canonical_document}
-->

[目次](../../目次.md) > {breadcrumb_path}

# {document_title}

## 1. {section_title}

{section_body}

## 2. {section_title}

{section_body}

---

[目次](../../目次.md) > {breadcrumb_path}

__COMMON_TEMPLATE_END__

---

## テンプレート使用上の注意（人間向け補足）

- LLM はテンプレートマーカー内のみを構造定義として扱う。
- 本補足文は、人間の理解補助を目的とするものであり、
  生成・判断・検証の根拠として解釈してはならない。
- 階層リンク行は、先頭および末尾に**同一内容・同一位置**で再掲される。
- LLM-MANAGED ブロックは、必ずドキュメント先頭に配置される。

---

[目次](../../目次.md) > テンプレート > 共通 > 共通ドキュメントテンプレート
