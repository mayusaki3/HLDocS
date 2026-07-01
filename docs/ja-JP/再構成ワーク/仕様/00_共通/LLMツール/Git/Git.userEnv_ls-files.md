<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260620-000000Z-GHLS
lang: ja-JP
canonical_title: Git.userEnv_ls-files
document_type: spec
canonical_document: true
-->

[目次](../../../../目次.md) > LLMツール > Git > Git.userEnv_ls-files

# Git.userEnv_ls-files

## 1. Tool名

Git.userEnv_ls-files

## 2. 目的

本Toolは、LLMが利用者へGitコマンドの実行を依頼し、利用者環境のGit管理下ファイル一覧を取得するためのToolである。  
本Toolは、LLM実行環境で目的を達成できない場合、利用者実行へ移行するために利用する。

本仕様は、共通仕様成立状態でのみ利用できる。  
共通仕様成立状態でない場合、本仕様を根拠として判断・生成・更新・検証を行ってはならない（MUST NOT）。  
共通仕様成立状態は、「共通仕様成立条件」に従って確認する。

## 3. 能力

本Toolは、利用者環境のGit管理下ファイル一覧を取得する。  
本Toolは、取得結果としてファイルパス一覧を返却する。  
本Toolは、Git管理下ファイル一覧取得以外を目的としない。

## 4. 利用条件

- 利用者がGitコマンドを利用可能であること
- 対象がGit管理下であること
- LLMが対象リポジトリを特定済みであること

## 5. 入力

本Toolは、次の入力を受け取る。

- repository
- branch
- path

repository は、対象リポジトリ名を指定する。  
branch は、取得対象ブランチ名を指定する。  
path は、取得対象ディレクトリのリポジトリ内相対パスを指定する。  
pathを省略した場合はリポジトリ全体を対象とする。

## 6. 出力

本Toolは、次の情報を返却する。

- repository
- branch
- path
- files
- directories
- errors

repository は、入力で指定したリポジトリ名である。  
branch は、入力で指定したブランチ名である。    
path は、入力で指定したリポジトリ内相対パスである。  
files は、取得対象配下のファイルパス一覧である。  
directories は、取得対象配下のディレクトリパス一覧である。  
errors は、取得に失敗した場合のエラー情報である。

## 7. 制約

本Toolの対象は、Git管理下でなければならない。
本Toolは、Git管理下以外を対象としてはならない。
本Toolは、取得のみを実施し、内容を変更してはならない。

## 8. 呼び出し方法

本Toolは、LLMが入力値から利用者への実行内容を生成し、利用者へGitコマンドの実行を依頼する。

### 8.1 利用者への提示内容

LLMは、入力値を使用して利用者への実行内容を生成しなければならない（MUST）。  
利用者へ提示する内容には、少なくとも次を含めなければならない（MUST）。

- 対象リポジトリ
- 対象ブランチ
- 取得対象パス
- 実行手順
- 実行コマンド

LLMは、入力値を用いて利用者がそのまま実行可能なGitコマンドを生成しなければならない（MUST）。

### 8.2 提示例

対象リポジトリ

```
HLDocS
```

対象ブランチ

```
develop
```

取得対象パス

```
docs/ja-JP
```

対象リポジトリ HLDocS の現在の作業ディレクトリへ移動し、対象ブランチが develop であることを確認したうえで、次のコマンドを順番に実行してください。

```PowerShell
git checkout develop
git pull
git ls-files "docs/ja-JP"
```

pathを省略した場合は、次のコマンドを実行する。

```PowerShell
git ls-files
```

途中でエラーが発生した場合は、それ以降のコマンドは実行せず、表示されたメッセージをそのままチャットへ貼り付けてください。  
正常終了した場合は、最後の実行結果をそのままチャットへ貼り付けてください。

### 8.3 Tool応答

LLMは、利用者から提供された実行結果をTool応答として扱わなければならない（MUST）。

## 9. 処理内容

本Toolは、次の処理を行う。

1. LLMは入力値を検証する。
2. LLMは利用者へGitコマンド提示する。
3. 利用者はGitコマンドを実行する。
4. 利用者は実行結果をコピーしてチャットに貼る。
5. LLMは利用者から提供された実行結果を確認する。
6. LLMは取得したファイル一覧から必要に応じてpath配下を抽出する。
7. LLMは応答仕様へ変換して返却する。

## 10. 応答仕様

正常終了時は、次の形式で返却する。

```json
{
  "status": "success",
  "repository": "HLDocS",
  "branch": "develop",
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

### 11.1 入力不備

入力不備時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "invalid_input",
  "message": "required input is missing",
  "files": [],
  "directories": [],
  "errors": [
    "repository is required",
    "branch is required"
  ]
}
```

### 11.2 Git実行失敗

Gitコマンドの実行に失敗した場合は、利用者から取得したエラーメッセージを保持したまま返却しなければならない（MUST）。

```json
{
  "status": "error",
  "error_type": "git_command_failed",
  "message": "git command failed",
  "files": [],
  "directories": [],
  "errors": []
}
```
errors には利用者から取得したGitエラーメッセージを、加工せずそのまま格納しなければならない（MUST）。

### 11.3 Git管理外

Git管理外時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "not_git_repository",
  "message": "target is not a git repository",
  "files": [],
  "directories": [],
  "errors": []
}
```
errors には利用者から取得したGitエラーメッセージを、加工せずそのまま格納しなければならない（MUST）。

### 11.4 利用者中止

利用者中止時は、次の形式で返却する。

```json
{
  "status": "error",
  "error_type": "user_cancelled",
  "message": "user cancelled execution",
  "files": [],
  "directories": [],
  "errors": [
    "execution cancelled by user"
  ]
}
```

## 12. 注意事項

本Toolは利用者実行を伴う。  
LLMは利用者へ実行内容を明示しなければならない（MUST）。  
利用者から提供された結果をTool応答として扱う。  
本ToolはWorkflowまたはSubFlowの判断を代替してはならない（MUST NOT）。  
本Toolの結果はWorkflow、SubFlowまたは通常会話における判断材料として利用してよい（MAY）。

---

[目次](../../../../目次.md) > LLMツール > Git > Git.userEnv_ls-files
