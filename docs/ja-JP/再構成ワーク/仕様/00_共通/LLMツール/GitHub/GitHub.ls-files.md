<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260620-000000Z-GHLS
lang: ja-JP
canonical_title: GitHub.ls-files
document_type: spec
canonical_document: true
-->

[目次](../../../../目次.md) > LLMツール > GitHub > GitHub.ls-files

# GitHub.ls-files

## 1. Tool名

GitHub.ls-files

## 2. 目的

本Toolは、GitHub上の公開リポジトリからファイル一覧を取得するためのToolである。  
本Toolは、LLM標準Toolでリポジトリのディレクトリ・ファイル一覧を取得できない場合に利用する。

本仕様は、共通仕様成立状態でのみ利用できる。  
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。  
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

## 3. 能力

本Toolは、指定されたGitHub公開リポジトリ、ブランチ、パス配下のファイル一覧を取得する。  
本Toolは、取得結果としてファイルパス一覧を返却する。  
本Toolは、ファイル内容の取得を目的としない。

## 4. 利用条件

本Toolは、対象リポジトリがpublicリポジトリである場合に利用できる。  
本Toolは、GitHubへネットワーク接続できる実行環境でのみ利用できる。  
本Toolは、対象リポジトリ、参照先、および取得対象パスが指定されている場合に利用できる。

## 5. 入力

本Toolは、次の入力を受け取る。

- repository
- ref
- path

repository は、`owner/repository` 形式で指定する。  
ref は、ブランチ名、タグ名、またはコミットハッシュを指定する。  
path は、取得対象ディレクトリのリポジトリ内パスを指定する。  
path を省略する場合は、リポジトリルートを対象とする。

## 6. 出力

本Toolは、次の情報を返却する。

- repository
- ref
- path
- files
- directories
- errors

files は、取得対象配下のファイルパス一覧である。  
directories は、取得対象配下のディレクトリパス一覧である。  
errors は、取得に失敗した場合のエラー情報である。

## 7. 制約

本Toolは、privateリポジトリを対象としてはならない（MUST NOT）。  
本Toolは、認証情報を必要とする処理を行ってはならない（MUST NOT）。  
本Toolは、リポジトリの内容を変更してはならない（MUST NOT）。  
本Toolは、ファイル一覧取得以外のGit操作を行ってはならない（MUST NOT）。

## 8. 呼び出し方法

本Toolは、LLMが利用可能なSandbox上で実行する。  
本Toolは、Pythonスクリプトとして実装してよい（MAY）。  
本Toolは、GitHub API、git ls-tree、またはGitHubの公開URL取得を用いて実装してよい（MAY）。  
実装方法は、実行環境で利用可能な手段に従って選択してよい（MAY）。

## 9. 処理内容

本Toolは、次の処理を行う。

1. 入力値を検証する。
2. 対象リポジトリがpublicとして取得可能であることを確認する。
3. 指定されたrefを対象としてファイル一覧を取得する。
4. 指定されたpath配下のファイルおよびディレクトリを抽出する。
5. 結果を応答仕様に従って返却する。

## 10. 応答仕様

正常終了時は、次の形式で返却する。

```json
{
  "status": "success",
  "repository": "owner/repository",
  "ref": "develop",
  "path": "docs/ja-JP",
  "files": [
    "docs/ja-JP/目次.md"
  ],
  "directories": [
    "docs/ja-JP/仕様"
  ],
  "errors": []
}
```

files および directories は、リポジトリルートからの相対パスで返却しなければならない（MUST）。

## 11. エラー応答

入力不備時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "invalid_input",
  "message": "required input is missing",
  "files": [],
  "directories": [],
  "errors": [
    "repository is required"
  ]
}
```

取得失敗時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "fetch_failed",
  "message": "failed to fetch repository tree",
  "files": [],
  "directories": [],
  "errors": [
    "repository not found or ref not found"
  ]
}
```

未対応時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "unsupported",
  "message": "requested operation is not supported",
  "files": [],
  "directories": [],
  "errors": [
    "private repository is not supported"
  ]
}
```

## 12. 注意事項

本Toolは、LLM標準Toolにリポジトリ一覧取得能力がない場合の補完Toolである。  
LLM標準Toolで同等の能力を利用できる場合は、LLM標準Toolを利用してよい（MAY）。  
本Toolは、WorkflowまたはSubFlowの処理判断を代替してはならない（MUST NOT）。  
本Toolの出力は、Workflow、SubFlow、または通常会話における判断材料として利用してよい（MAY）。

---

[目次](../../../../目次.md) > LLMツール > GitHub > GitHub.ls-files
