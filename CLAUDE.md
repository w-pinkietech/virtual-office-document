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

### 【必須】ブランチ運用ルール
**作業開始前**: 必ずfeatureブランチを作成
**作業終了時**: featureブランチにpushして人間レビュー依頼

### ブランチ作成・管理
```bash
# 1. 作業開始：featureブランチ作成（必須）
git checkout main
git pull origin main
git checkout -b feature/epic-[number]-[description]

# 2. 作業実施
git add .
git commit -m "説明文"

# 3. 作業終了：featureブランチにpush（必須）
git push origin feature/epic-[number]-[description]

# 4. PR作成（人間レビュー依頼）
gh pr create --title "Epic #[number]: [タイトル]" --body "Epic: #[epic_number]

## 変更内容
[詳細な変更内容]

## 完了したStories
- ✅ #[story1] - [Story1名]
- ✅ #[story2] - [Story2名]

人間レビューをお願いします。"
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
3. **featureブランチ作成（必須）**
4. 作業実施

### 2. 進捗管理
1. Todo状態更新（pending → in_progress → completed）
2. Issue状態同期（コメント・クローズ）
3. **featureブランチにコミット**

### 3. 完了時
1. 全Todo完了確認
2. **featureブランチにpush（必須）**
3. PR作成・人間レビュー依頼（必須）
4. Epic完了

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