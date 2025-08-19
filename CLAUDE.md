# CLAUDE.md - AI作業ガイド

> **バーチャルオフィス契約管理プロジェクト**  
> Claude（AI）の作業ルールとGitHub連携

## 🤖 Claude（AI）への重要指示

**【必須】Todo-Issue同期ルール**: Claude含む全AI作業時は以下を実行

### Todo-Issue同期の基本フロー
1. **TodoWrite実行時**: Epic/Story自動作成
2. **進捗変更時**: Issue状態同期
3. **完了時**: Issue自動クローズ

### 実行手順
```bash
# Epic作成
gh issue create --title "Epic: [タスク概要]" --body "[詳細]" --assignee "@me"

# Story作成（各Todo毎）
gh issue create --title "Story: [Todo内容]" --body "Epic: #[epic_number]\nTodo ID: [id]" --assignee "@me"

# 進捗コメント
gh issue comment [story_number] --body "🔄 作業開始: [内容] ($(date))"

# 完了時クローズ
gh issue close [story_number]
gh issue comment [story_number] --body "✅ Todo完了により自動クローズ: [内容] ($(date))"
```

## 🌳 基本Git操作

### ブランチ作成・管理
```bash
# AI用ブランチ作成
git checkout -b ai/epic-[number]-[description]

# 基本操作
git add .
git commit -m "説明文"
git push origin [branch-name]

# PR作成
gh pr create --title "タイトル" --body "説明"
```

### Issue管理
- **Epic**: 大きなタスクの管理単位
- **Story**: 個別のTodo項目
- **Bug**: 問題の修正
- **Task**: 運用タスク

## 🔧 AI作業手順

### 1. 作業開始
1. TodoWriteでタスク定義
2. Epic/Story作成（自動同期）
3. AIブランチ作成
4. 作業実施

### 2. 進捗管理
1. Todo状態更新（pending → in_progress → completed）
2. Issue状態同期（コメント・クローズ）
3. PR作成・レビュー依頼

### 3. 完了時
1. 全Todo完了確認
2. Epic完了
3. 人間確認依頼（必須）

## 📁 プロジェクト構造

### 契約書類管理
- `10_legal-documents/current/` - 使用中の契約書
- `10_legal-documents/templates/` - テンプレート
- `20_legal-compliance/` - 法令チェック

### 作業の重点
- 契約書類のバージョン管理
- GitHubでの変更履歴追跡
- シンプルな運用体制

---

**最終更新**: 2025年8月19日